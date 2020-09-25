# -*- coding: utf-8 -*-

# serial com: implement low level serial comunications functions 
# wac@iowlabs
#

print("Access-Control-Allow-Origin: *")
print("Content-Type: application/json; charset=UTF-8")
print()

import serial
import numpy as np
import time

#default parameters
COM_PORT = 'COM4'
#COM_PORT = '/dev/ttyUSB0'
BAUDRATE = 115200
NEWLINE  = '\n'
TIMEOUT  = 1.0

# Extra parameters
PARITY   = serial.PARITY_NONE
STOPBITS = serial.STOPBITS_ONE
BYTESIZE = serial.EIGHTBITS

# Error codes
ERROR_CONN  = np.uint8(1 << 0)  # 1
ERROR_SEND  = np.uint8(1 << 1)  # 2
ERROR_RECV  = np.uint8(1 << 2)  # 4
ERROR_CLOSE = np.uint8(1 << 3)  # 8
ERROR_PARSE = np.uint8(1 << 4)  # 16
ERROR_ECHO  = np.uint8(1 << 5)  # 32


def list_ports():
  import serial.tools.list_ports
  return serial.tools.list_ports.comports()

class serial_com(object):

  def __init__(self, com_name = COM_PORT, baudrate = BAUDRATE, newline = NEWLINE, timeout = TIMEOUT, parity = PARITY, stopbits = STOPBITS, bytesize = BYTESIZE):
    self.com_name  = com_name
    self.baudrate  = baudrate
    self.newline   = newline
    self.timeout   = timeout
    self.parity    = parity
    self.stopbits  = stopbits
    self.bytesize  = bytesize

    self.error     = 0
    self.last_send = ''
    self.last_recv = ''
    #self.connect()


  def connect(self,com_name ):
    try:
      self.com_name = com_name
      self.com = serial.Serial( port = self.com_name,baudrate = self.baudrate, parity   = self.parity, stopbits = self.stopbits, bytesize = self.bytesize, timeout  = self.timeout)
      self.error = 0
      print('Connected to: ', self.com_name)
      return True
    except Exception as e:
      print(e)
      self.error |= ERROR_CONN
      return False

  def send(self, msg, delay=0):
    #print("msg to send",msg)
    if delay > 0:
      time.sleep(delay)
    self.last_send = msg
    try:
      #self.com.write(msg + self.newline)
      #self.com.write(str(msg).encode())
      self.com.write(msg)
      return True
    except:
      self.error |= ERROR_SEND
      return False

  def receive(self):
    try:
      self.last_recv = self.com.readline()
      return self.last_recv
    except:
      self.error |= ERROR_RECV
      return ''

  def close(self):
    try:
      self.com.close()
      return True
    except:
      self.error |= ERROR_CLOSE
      return False

if __name__ == '__main__':  
  print('List of available ports')
  print( list_ports())