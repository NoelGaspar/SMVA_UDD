# -*- coding: utf-8 -*-
# SMVA-Client: implement client code
#               use socket lib for manager the web socket comunication.
# wac@iowlabs
#

import socket
import signal
import sys
import os
import subprocess
import RPi.GPIO as GPIO
import time

TRIGGER_GPIO = 19

SERVER_IP_ADDR = '192.168.0.12'
SERVER_PORT = 777

SAMPLE_RATE = 3200 # [Hz]
SMAPLE_TIME = 2  # [s]

BUFF_SIZE = 4096
SEPARATOR = ","

PATH_DATA = "./sended_data/"

def signal_handler(sig,frame):
  GPIO.cleanup()
  client_socket.close() 
  sys.exit(0)

def trigger_callback(channel):
  print("triggered")
  
  client_socket = socket.socket()
  client_socket.connect((SERVER_IP_ADDR,SERVER_PORT))

  #file name
  send_filename =PATH_DATA+str(int(time.time()))+".csv"
  #read sensor
  os.system(f'sudo adxl345spi -t {SMAPLE_TIME} -f {SAMPLE_RATE} -s {send_filename}')
  #file size to send
  send_file_size = os.path.getsize(send_filename)
  
  #send header
  #client_socket.send(f"{send_filename}{SEPARATOR}{send_file_size}".encode())

  #send the complete file
  send_file = open(send_filename, "rb")

  SendData = send_file.read(BUFF_SIZE)

  while SendData:
    
    client_socket.send(SendData)
    SendData = send_file.read(BUFF_SIZE)    
  
  send_file.close()
  client_socket.close()

if __name__ == '__main__':
  
  GPIO.setmode(GPIO.BCM)
  GPIO.setup(TRIGGER_GPIO,GPIO.IN)

  GPIO.add_event_detect(TRIGGER_GPIO,GPIO.RISING,callback = trigger_callback, bouncetime=100)
  signal.signal(signal.SIGINT,signal_handler)
  signal.pause()


  while(1): 
    pass
