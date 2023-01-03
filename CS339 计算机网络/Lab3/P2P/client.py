import json
import socket
import logging
import sys
import argparse

from io import BytesIO
from threading import Thread,Lock
from time import time,sleep
from math import ceil
from random import choice
from configparser import ConfigParser

from utils import *

class Client(object):
    def __init__(self, server_ip, server_port, 
            upload_ip = '', upload_port = 51000 ,file_path = None,):

        self.server_addr = (server_ip,int(server_port))
        self.peer_upload_addr = (upload_ip, int(upload_port))
        
        self.file_lock = Lock()

        self.start_download_time = None
        self.end_download_time = None

        if file_path:
            self.file = open(file_path,'w+b')
        else:
            self.file = BytesIO()


        self.chunk_size = 1024*8
        self.file_size = 1024*1024*10
        self.chunk_num = 0

        self.peer_server_port = 51000
        self.peer_list = []

        self.server_socket = None
        self.p2p_server_socket = None
        self.peer_upload_sockets = []
        self.peer_download_sockets = []

        self.peer_upload_threads = []       #向peer上传的线程
        self.peer_download_threads = []     #从peer下载的线程
        
        self.peer_server_thread = None #本地服务器监听线程
        self.server_download_thread = None

        self.chunk_downloaded_size = []
        self.chunk_status = []  #0:未开始 1：下载中 2：已下载
        self.downloaded_chunk_id = set()

    def start(self):
        self.start_peer_server(self.peer_upload_addr)

        self.server_socket = self.connect_server(self.server_addr)
        # s = self.connect_server(('localhost', 52000))
        self.server_download_thread = Thread(target=self.server_download,daemon=True)
        self.server_download_thread.start()
        for peer_download_thread in self.peer_download_threads:
            peer_download_thread.start()
        
        try:
            self.server_download_thread.join()
            #等待所有peer下载进程结束
            for t in self.peer_download_threads:
                t.join()
        except KeyboardInterrupt:
            logging.warning('receive KeyboardInterrupt')
            return

        if self.check_download():
            logging.info(f"download complete, time used: {round(self.end_download_time-self.start_download_time,2)} sec")
        else:
            logging.error("file checksum does not match!")
        
        self.server_socket.close()
        
        print()
    
    def start_peer_server(self, addr = ("",51000)):
        interface, port = addr
        self.p2p_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.p2p_server_socket.setsockopt(
            socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        for i in range(100):
            attempt_port = port + i
            try:
                self.p2p_server_socket.bind((interface, attempt_port))
            except OSError as err:
                if err.errno == 98: #addr already in use
                    continue
                else:
                    raise
            else:
                break
        ip, port = self.p2p_server_socket.getsockname()
        self.peer_server_port = port
        self.p2p_server_socket.listen(128)
        logging.debug(f"peer server working on {(ip,port)}")
        peer_server_thread = Thread(target=self.peer_server,
            args=tuple(),daemon=True)
        peer_server_thread.start()
        self.peer_server_thread = peer_server_thread


    def peer_server(self, port = 51000, interface = ""):
        while True:
            client_socket,client_addr = self.p2p_server_socket.accept()
            logging.info(f"accept connection from {client_addr[0]}.")
            handle_client_thread = Thread(
                target=self.p2p_upload, args=(client_socket,client_addr),daemon=True)
            handle_client_thread.start()
            self.peer_upload_threads.append(handle_client_thread)

    def connect_server(self, server_addr):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.connect(server_addr)
        msg = f"CHEL {self.peer_server_port}\r\n".encode()
        self.server_socket.send(msg)
        recv_buffer = self.server_socket.recv(1024)
        recv = P2PParser.parse(recv_buffer)
        if recv.op == OPType.SHEL:
            self.file_size, self.chunk_size = recv.args
            self.chunk_num = ceil(self.file_size / self.chunk_size)
            #初始化chunk列表
            self.chunk_downloaded_size = [0 for _ in range(self.chunk_num)]
            self.chunk_status = [ChunkStatus.UNDOWNLOAD for _ in range(self.chunk_num)]
            #连接peers
            self.peer_list = list(map(lambda addr:tuple(addr),recv.json))
            for peer_addr in self.peer_list:
                peer_download_thread = Thread(target=self.p2p_download,args=(peer_addr,),daemon=True)
                self.peer_download_threads.append(peer_download_thread)
        else:
            raise P2PException.ProtocolNotCompatible()
        return self.server_socket

    def server_download(self):
        self.start_download_time = time()
        try:
            while len(self.downloaded_chunk_id) < self.chunk_num:
                undownload_chunk_id = [i for i in range(self.chunk_num) if self.chunk_status[i] == ChunkStatus.UNDOWNLOAD]
                if len(undownload_chunk_id) == 0:
                    sleep(0.5)
                    continue                #不要直接退出，直到确认全部下载完才退出
                next_chunk_id = choice(undownload_chunk_id)
                self.download_chunk(next_chunk_id,self.server_socket)
        except (BrokenPipeError,ConnectionResetError):
            logging.error("connection to central server lost!")
            raise
        finally:
            self.end_download_time = time()

    def p2p_download(self, client_addr):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(tuple(client_addr))
        msg = f"CHEL {self.peer_server_port}\r\n".encode()
        s.send(msg)
        recv_buffer = s.recv(1024)
        recv = P2PParser.parse(recv_buffer)
        if recv.op != OPType.PHEL:
            raise P2PException.ProtocolNotCompatible()
        try:
            while len(self.downloaded_chunk_id) < self.chunk_num:
                msg = b"CLREQ\r\n"
                try:
                    s.send(msg)
                except BrokenPipeError:
                    raise
                recv_buffer = s.recv(1024)
                recv = P2PParser.parse(recv_buffer)
                if recv.op == OPType.CLRES:
                    peer_available_chunk = recv.json
                    available_chunk = tuple(filter(lambda cid:self.chunk_status[cid]==ChunkStatus.UNDOWNLOAD,peer_available_chunk))
                    if len(available_chunk) == 0:
                        sleep(1)
                        continue
                    next_chunk_id = choice(available_chunk)
                    self.download_chunk(next_chunk_id,s)
        except (BrokenPipeError,ConnectionResetError,P2PException.RecvEmptyExcption):
            #peer连接断开是可以恢复的异常，没有下载完的内容之后会重新下载
            logging.info(f"connection from {client_addr[0]} lost.")
            logging.debug(f"current connected peers: {len(self.peer_list)}")
        else:
            logging.debug(f"no more to download, disconnect from {client_addr[0]}")
        finally:
            s.close()
            self.peer_list.remove(client_addr)

    def download_chunk(self,chunk_id,conn_socket):
        downloaded = 0
        self.chunk_downloaded_size[chunk_id] = 0
        self.chunk_status[chunk_id] = ChunkStatus.DOWNLOADING
        try:
            msg = f"DREQ {chunk_id}\r\n".encode()
            conn_socket.send(msg)
            recv_buffer = conn_socket.recv(2048)
            recv = P2PParser.parse(recv_buffer)
            if recv.op == OPType.DATA:
                chunk_offset, chunk_size = recv.args
                content = recv.content
                if chunk_offset != chunk_id * chunk_size:
                    pass    #offset不一致
                elif chunk_size > self.chunk_size:
                    pass    #chunk_size不一致
                elif chunk_offset + chunk_size > self.file_size:
                    pass    #末尾chunk过大
                
                downloaded = 0
                left_size = chunk_size      #chunk剩下需要下载的大小
                
                while True:
                    content_len = len(content)
                    if content_len <= left_size:
                        self.file_lock.acquire()
                        self.file.seek(chunk_id*self.chunk_size + downloaded)
                        self.file.write(content)
                        self.file_lock.release()

                        downloaded += content_len
                        left_size -= content_len
                        self.chunk_downloaded_size[chunk_id] = downloaded
                    else:
                        pass    #chun_size不一致

                    if left_size > 0:
                        content = conn_socket.recv(2048)
                        if not content:
                            raise P2PException.RecvEmptyExcption    #链接丢失
                    else:
                        break
        except (BrokenPipeError,ConnectionResetError,P2PException.RecvEmptyExcption):
            logging.debug(f"connection loss while downloading chunk {chunk_id}")
            logging.debug(f"chunk {chunk_id} download fail")
            self.chunk_status[chunk_id] = ChunkStatus.UNDOWNLOAD
            raise
        else:
            self.downloaded_chunk_id.add(chunk_id)
            self.chunk_status[chunk_id] = ChunkStatus.DOWNLOADED
            logging.debug(f"chunk {chunk_id} downloaded from {conn_socket.getpeername()}")


    def p2p_upload(self, client_socket, client_addr):
        recv_buffer = client_socket.recv(1024)
        recv = P2PParser.parse(recv_buffer)
        if not recv.op == OPType.CHEL:
            client_socket.close()
            return
        else:                   #连接peer的服务端口
            peer_server_addr = (client_addr[0],recv.args)
            if peer_server_addr not in self.peer_list:
                self.peer_list.append(peer_server_addr)
                p2p_download_thread = Thread(
                        target=self.p2p_download, args=(peer_server_addr,), daemon=True)
                p2p_download_thread.start()
                self.peer_download_threads.append(p2p_download_thread)
            client_socket.send(b'PHEL\r\n')
        try:
            while True:
                try:
                    recv_buffer = client_socket.recv(1024)
                except OSError as err:
                    if err.errno == 104:    #connection reset
                        break
                    else:
                        raise
                if not recv_buffer:        #连接断开
                    client_socket.close()
                    break
                recv = P2PParser.parse(recv_buffer)
                if recv.op == OPType.DREQ:
                    chunk_id = recv.args
                    chunk_offset = chunk_id * self.chunk_size
                    cur_chunksize = min(self.chunk_size,self.file_size-chunk_offset)
                    if chunk_offset >= self.file_size:             #offset过大
                        client_socket.send(b'ERROR OFFSET_OVERFLOW\r\n')
                        continue
                    elif self.chunk_status[chunk_id] != ChunkStatus.DOWNLOADED:  #chunck还未下载完
                        client_socket.send(b'ERROR CHUNK_UNDOWNLOADED\r\n')
                        continue
                    
                    msg = f'DATA {chunk_offset} {cur_chunksize}\r\n'.encode()
                    client_socket.send(msg)

                    uploaded = 0
                    while uploaded < cur_chunksize:
                        buffer_size = min(1024,cur_chunksize - uploaded)
                        self.file_lock.acquire()
                        self.file.seek(chunk_offset+uploaded)
                        buffer = self.file.read(buffer_size)
                        self.file_lock.release()
                        client_socket.send(buffer)
                        uploaded += buffer_size
                elif recv.op == OPType.CLREQ:     #返回已下载的chunk列表
                    msg = f'CLRES {len(self.downloaded_chunk_id)}\r\n'\
                        f'{json.dumps(tuple(self.downloaded_chunk_id))}'.encode()
                    client_socket.send(msg)
                else:
                    client_socket.send(b'ERROR UNKNOWN_COMMAND\r\n')
        finally:
            client_socket.close()
    
    def check_download(self):
        self.file_lock.acquire()
        self.file.seek(0)
        checksum = MD5_checksum(self.file)
        self.file_lock.release()
        logging.debug(f'local file checksum: {checksum}')
        msg = f"CHECK {checksum}\r\n".encode()
        self.server_socket.send(msg)
        recv_buffer = self.server_socket.recv(1024)
        recv = P2PParser.parse(recv_buffer)
        if recv.op == OPType.CHECK:
            return True
        else:
            return False


        
if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG,
        format='[%(asctime)s][%(levelname)s] - %(message)s',datefmt='%H:%M:%S')

    server_ip = '10.0.0.1'
    server_port = 52000
    port = 51000
    file_path = ''
    config_file = "config.ini"

    parser = argparse.ArgumentParser()
    parser.description = 'A implementation of a client in P2P model.'
    parser.add_argument("-s","--server",help="IP address of the server.",type=str)
    parser.add_argument("-sp","--server_port",help="Server port.",type=int)
    parser.add_argument("-p","--port",help="Listening port.",type=int)
    parser.add_argument("-o","--output_path",help="Output path.",type=str)
    parser.add_argument("--config",help="Path of configure file.",type=str)
    args = parser.parse_args()

    if args.config:
        config_file = args.config

    config = ConfigParser()
    config.read(config_file)
    ip = config.get("Client","ip",fallback='')
    port = config.getint("Client","port",fallback=51000)
    file_path = config.get("Client","file_path",fallback='')
    server_ip = config.get("Client","server_ip",fallback='')
    server_port = config.getint("Client","server_port",fallback=52000)

    if args.server:
        server_ip = args.server
    if args.server_port:
        server_port = args.server_port
    if args.port:
        port = args.port
    if args.output_path:
        file_path = args.output_path

    Client(server_ip,server_port,ip,port,file_path).start()
       