#!/usr/bin/env python3

"""
SMVA-Server code testing
https://python-socketio.readthedocs.io/en/latest/

"""
import socket
import sys
import os
from datetime import datetime



SERVER_IP_ADDR = '192.168.0.8'
SERVER_PORT = 777

SAMPLE_RATE = 2000 # [Hz]
SMAPLE_TIME = 1    # [s]

send_filename = datetime.now().strftime("%d-%m-%Y_%I-%M-%S_%p")+".csv"
os.system(f'sudo adxl345spi -t {SMAPLE_TIME} -f {SAMPLE_RATE} -s {send_filename}')


client_socket = socket.socket()
client_socket.connect((SERVER_IP_ADDR,SERVER_PORT))


send_file = open(send_filename, "rb")
SendData = send_file.read(4096)

while SendedData:
  print("\n msg from server", client_socket.recv(1024),decode("utf-8"))
  client_socket.send(SendData)
  SendData = send_file.read(1024)

client_socket.close() 