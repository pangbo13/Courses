from socket import socket, AF_INET, SOCK_STREAM
from io import BytesIO
from time import time
import sys
import argparse

def download(addr,file_path = None):
    try:
        if file_path:
            f = open(file_path,'wb')
        else:
            f = BytesIO()
        s = socket(AF_INET, SOCK_STREAM)
        s.connect(addr)
        while True:
            buffer = s.recv(8192)
            if not buffer:
                break
            f.write(buffer)
    finally:
        s.close()

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.description = 'A simple implementation of a client in C/S model.'
    parser.add_argument("-s","--server",help="IP address of the server.",type=str)
    parser.add_argument("-p","--port",help="Server port.",type=int)
    parser.add_argument("-o","--output_path",help="Output path.",type=str)
    args = parser.parse_args()

    ip = '10.0.0.1'
    port = 52000
    path = None
    if args.server:
        ip = args.server
    if args.port:
        port = args.port
    if args.output_path:
        path = args.output_path

    start_time = time()
    download((ip, port),path)
    end_time = time()
    print(f"time used: {round(end_time-start_time,2)} sec")