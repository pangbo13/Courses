import json
import socket
import logging
import argparse

from os import urandom
from os.path import getsize as getfilesize
from io import BytesIO
from threading import Thread,Lock
from configparser import ConfigParser
from time import time

from utils import *


class Server(object):
    def __init__(self, file_path = None, file_size = None):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(
            socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.file_lock = Lock()
        self.file_checksum = None
        self.file_size = 0
        self.chunk_size = 1024*128

        self.peer_list = []
        self.peer_server_dict = {}
        
        self.client_socket = []

        if file_path:
            self.file_size = getfilesize(file_path)
            self.file = open(file_path,'rb')
        else:
            if file_size and file_size > 0:
                self.file_size = file_size
            else:
                self.file_size = 10 * 1024 * 1024
            self.file = BytesIO()
            self.generate_random_file()

        self.file_lock.acquire()
        self.file.seek(0)
        self.file_checksum = MD5_checksum(self.file)
        self.file_lock.release()
        logging.debug(f"md5 checksum of file is {self.file_checksum}")
    
    def bind(self, port, interface = ""):
        self.server_socket.bind((interface, port))
        logging.info(f"server is bonded to port {port}")
        return self

    def generate_random_file(self):
        self.file_lock.acquire()
        self.file.seek(0)
        left_size = self.file_size
        while left_size > 0:
            self.file.write(urandom(min(left_size,1024*10)))
            left_size -= min(left_size,1024*10)
        self.file_lock.release()
        
        
    def start(self):
        self.server_socket.listen(128)
        try:
            while True:
                client_socket,client_addr = self.server_socket.accept()
                logging.info("accept connection from {}.".format(client_addr[0]))
                handle_client_process = Thread(
                    target=self.handle_client, args=(client_socket,client_addr))
                handle_client_process.start()
        except KeyboardInterrupt:
            logging.warning("KeyboardInterrupt recived!")
    

    def send_peerlist(self, client_socket):
        msg = f'SHEL {self.file_size} {self.chunk_size}\r\n'.encode() + json.dumps(self.peer_list).encode()
        client_socket.send(msg)

    def handle_client(self, client_socket, client_addr):
        recv_buffer = client_socket.recv(1024)
        recv = P2PParser.parse(recv_buffer)
        if not recv.op == OPType.CHEL:
            client_socket.close()
            return
        else:
            # self.boardcast_newpeer(client_addr)
            self.send_peerlist(client_socket)
            client_p2p_server_addr = (client_addr[0],recv.args)
            self.peer_list.append(client_p2p_server_addr)
            self.peer_server_dict[client_addr] = client_p2p_server_addr
        try:
            while True:
                recv_buffer = client_socket.recv(1024)
                if not recv_buffer:
                    break
                recv = P2PParser.parse(recv_buffer)
                if recv.op == OPType.DREQ:
                    # op, chunk_id = recv_buffer.split(b' ')
                    # chunk_id = int(chunk_id)
                    chunk_id = recv.args
                    chunk_offset = chunk_id * self.chunk_size
                    cur_chunksize = min(self.chunk_size,self.file_size-chunk_offset)
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
                    
                elif recv.op == OPType.CHECK:
                    checksum = recv.args
                    if checksum == self.file_checksum:
                        #文件校验通过，重复返回校验值
                        msg = f"CHECK {self.file_checksum}\r\n".encode()
                        client_socket.send(msg)
                    else:
                        #文件校验不通过
                        msg = f"ERROR CHECKSUM_NOT_FIT\r\n{self.file_checksum}".encode()
                        client_socket.send(msg)
                elif recv.op == OPType.CHEL:
                    self.send_peerlist(client_socket)
                else:
                    client_socket.send(b'ERROR UNKONWN_COMMAND\r\n')
        except ConnectionResetError:
            pass
        finally:
            client_socket.close()
        logging.info(f"connection from {client_addr[0]} lost.")
        self.peer_list.remove(self.peer_server_dict[client_addr])
        del self.peer_server_dict[client_addr]
        logging.debug(f"current connected peers: {len(self.peer_list)}")


        
if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG,
        format='[%(asctime)s][%(levelname)s] - %(message)s',datefmt='%H:%M:%S')

    ip = ''
    port = 52000
    file_path = ''
    config_file = "config.ini"

    parser = argparse.ArgumentParser()
    parser.description = 'A implementation of a server in P2P model.'
    parser.add_argument("-p","--port",help="Listening port.",type=int)
    parser.add_argument("-f","--file",help="File path.",type=str)
    parser.add_argument("--config",help="Path of configure file.",type=str)
    args = parser.parse_args()

    if args.config:
        config_file = args.config

    config = ConfigParser()
    config.read(config_file)
    ip = config.get("Server","ip",fallback='')
    port = config.getint("Server","port",fallback=52000)
    file_path = config.get("Server","file_path",fallback='')
    file_size = config.getint("Server","file_size",fallback = -1)

    if args.port:
        port = args.port
    if args.file:
        file_path = args.file

    Server(file_path,file_size).bind(port,ip).start()
       