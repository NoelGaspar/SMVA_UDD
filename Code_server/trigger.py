# -*- coding: utf-8 -*-
# trigger: implement trigger functions
# wac@iowlabs
#

print("Access-Control-Allow-Origin: *")
print("Content-Type: application/json; charset=UTF-8")
print()

import sys,getopt 
import time
import serial_com
import threading

#smvaCOM_PORT = 'COM5'
#COM_BYID = 'usb-Silicon_Labs_CP2102_USB_to_UART_Bridge_Controller_0001-if00-port0'
COM_PORT = '/dev/serial/by-id/usb-Silicon_Labs_CP2102_USB_to_UART_Bridge_Controller_0001-if00-port0'
CMD_TRIGGER = b'1'
CMD_STOP    = b'2'
CMD_START   = b'3'
CMD_IDLE    = b'0'

esp = serial_com.serial_com(COM_PORT,timeout = None)

def com_init(com_port = COM_PORT, timeout = None):
  esp.connect(com_port)
  time.sleep(5) #wait for setup
  if esp.error !=0:
    print("Error connecting:",esp.error)
    esp.close()
    sys.exit()
  print("Connected to ESP32")

def receive_and_print():
  while True:
    print( '< ', esp.receive())

def triggerOnce():
  esp.send(CMD_TRIGGER)
  print("tirggering single sample")

def triggerAuto( start ):
  if start == True:
    esp.send(CMD_START)
  else:
    esp.send(CMD_STOP)

def com_close( ):
  esp.close()
  sys.exit()


def triggerMenu():
  print("------Menu------")
  print("1. single trigger")
  print("2. start triggering")
  print("3. stop triggering")
  print("4. menu")
  print("5. close")




if __name__ == '__main__':

  #start = False

  start = False
#  try:
#    opts,args = getopt.getopt(sys.argv[1:],"hps:",["port="])
#  except getopt.GetoptError:
#    print('try trigger.py -p <port>')
#    sys.exit(2)

#  for opt, arg in opts:
#    if opt == '-h':
#      print('trigger.py -p <port>')
#    elif opt in ("-p", "--port"):
#      print("port",arg)
#      COM_PORT =  arg
#      start = True
#    elif opt in ("-s", "--start"):
#      start = True

  if start :
    com_init(COM_PORT)
    triggerAuto(False)
    #com_close()
  
    triggerMenu()
    while True:
      command =  int(input("ingrese opción"))
      if command == 1:
        triggerOnce()
      elif command == 2:  
        triggerAuto(True)
      elif command == 3:  
        triggerAuto(False)
      elif command == 4:   
        triggerMenu()
      elif command == 5:
        esp.close()
        sys.exit()
      else:
        triggerMenu()
