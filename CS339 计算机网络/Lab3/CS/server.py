import socket
import logging
import sys
import argparse

from os import urandom
from io import BytesIO
from threading import Thread,Lock
from time import time


class Server(object):
    def __init__(self,file = None):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(
            socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.lock = Lock()
        self.chunk_size = 1024*128
        self.file_size = 1024*1024*10
        self.__exit_sig = False
        self.time_list = []
        
        if file is None:
            self.file = BytesIO()
            self.generate_random_file()
        else:
            self.file = open(file,'rb')

    def bind(self, port, interface = ""):
        self.server_socket.bind((interface, port))
        logging.info(f"server is bonded to port {port}")
        return self

    def generate_random_file(self):
        for i in range(10*1024):
            self.file.write(urandom(1024))

    def start(self):
        self.server_socket.listen(128)
        try:
            while not self.__exit_sig:
                client_socket,client_addr = self.server_socket.accept()
                logging.info("accept connection from {}.".format(client_addr[0]))
                handle_client_process = Thread(
                    target=self.handle_client, args=(client_socket,client_addr))
                handle_client_process.start()
        except KeyboardInterrupt:
            logging.warning("KeyboardInterrupt recived!")
            if len(self.time_list) > 0:
                logging.info(f"average download time: {sum(self.time_list)/len(self.time_list)} sec")

    def handle_client(self, client_socket, client_addr):
        """
        处理客户端请求
        """
        # 获取客户端请求数据
        sent_data = 0
        logging.info(f"{client_addr[0]} begin downloading file.")
        start_time = time()
        try:
            while True:
                self.lock.acquire()
                self.file.seek(sent_data)
                buffer = self.file.read(self.chunk_size)
                self.lock.release()
                try:
                    if not buffer:
                        client_socket.close()
                        break
                    client_socket.send(buffer)
                    sent_data += self.chunk_size
                except ConnectionResetError:
                    logging.warning(f"{client_addr[0]} reset connection while downloading.")
                    raise
        except Exception:
            pass
        else:
            end_time = time()
            logging.info(f"{client_addr[0]} finished downloading.")
            logging.info(f"time used: {round(end_time-start_time,2)} sec.")
            self.time_list.append(end_time-start_time)
        finally:
            client_socket.close()
        
if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG,
        format='[%(asctime)s][%(levelname)s] - %(message)s',datefmt='%H:%M:%S')
    
    parser = argparse.ArgumentParser()
    parser.description = 'A simple implementation of a server in C/S model.'
    parser.add_argument("-p","--port",help="Listening port.",type=int)
    parser.add_argument("-f","--file",help="File path.",type=str)
    args = parser.parse_args()

    if args.file:
        server = Server(file=args.file)
    else:
        server = Server()

    port = 52000
    if args.port:
        port = args.port
    
    server.bind(port).start()
       