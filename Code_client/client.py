# -*- coding: utf-8 -*-
# SMVA-Client: implement client code
#               use socket lib for manager the web socket comunication.
# wac@iowlabs
#

import socket
import signal
import sys
import os
import RPi.GPIO as GPIO
import time

TRIGGER_GPIO = 19

SERVER_IP_ADDR = '192.168.0.3'
SERVER_PORT = 777

SAMPLE_RATE = 3200 # [Hz]
SMAPLE_TIME = 2.5  # [s]

BUFF_SIZE = 4000


def signal_handler(sig,frame):
  GPIO.cleanup()
  client_socket.close() 
  sys.exit(0)

def trigger_callback(channel):
  print("triggered")
  send_filename =str(int( time.time()))+".csv"
  os.system(f'sudo adxl345spi -t {SMAPLE_TIME} -f {SAMPLE_RATE} -s {send_filename}')
  send_file = open(send_filename, "rb")
  SendData = send_file.read(BUFF_SIZE)
  client_socket.send(SendData)
  send_file.close()

if __name__ == '__main__':
  
  GPIO.setmode(GPIO.BCM)
  GPIO.setup(TRIGGER_GPIO,GPIO.IN)

  client_socket = socket.socket()
  client_socket.connect((SERVER_IP_ADDR,SERVER_PORT))

  GPIO.add_event_detect(TRIGGER_GPIO,GPIO.RISSING,callback = trigger_callback, bouncetime=100)
  signal.signal(signal.SIGINT,signal_handler)
  signal.pause()

 
  while(1): 
    pass