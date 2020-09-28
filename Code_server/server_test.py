# -*- coding: utf-8 -*-
# SMVA-Server: implement server main functions. 
#               use socket lib for manager the web socket comunication.
# wac@iowlabs
#

import eventlet
import socket
from datetime import datetime
import time 
import threading
from _thread import *
import sys,getopt
#imports for do math and plot
import numpy as np
from matplotlib import mlab
import matplotlib.pyplot as plt


PORT = 777
BUFF_SIZE = 4096
SEPARATOR = ","

SAMPLE_RATE = 3200 # [Hz]
SMAPLE_TIME = 2  # [s]

PATH_DATA = "./recived_data/"
TYPE_DATA_ACC = "acc/"
TYPE_DATA_FFT = "fft/"

#COM_PORT = 'COM5' #on windows
COM_PORT = '/dev/serial/by-id/usb-Silicon_Labs_CP2102_USB_to_UART_Bridge_Controller_0001-if00-port0'

plot_en = False

server_socket = socket.socket()

print("\n Server is listing on port:",PORT,"\n")

server_socket.bind(('',PORT))
server_socket.listen(10)

def threaded_recv(recv_conn, plt_en):
  time_now = datetime.now()
  time_unix = str(int(time.mktime(time_now.timetuple())))

  rcv_filename = PATH_DATA+TYPE_DATA_ACC+time_unix+".csv"
  fft_filename = PATH_DATA+TYPE_DATA_FFT+time_unix+".csv"
  rcv_file = open(rcv_filename,"wb")

  
  #read header
  #recv_header = recv_conn.recv(BUFF_SIZE).decode()
  #filname,recv_filesize = recv_header.split(SEPARATOR)
  #recv_filesize = int(recv_filesize)
  #
  #print(f"reciving data. file size:{recv_filesize}")
  
  RecivedData = recv_conn.recv(BUFF_SIZE)
  while RecivedData:
    #print("writing data")
    rcv_file.write(RecivedData)
    #print("reciving another bounch of data")
    #myconn.settimeout(5.0)
    RecivedData = recv_conn.recv(BUFF_SIZE)

  rcv_file.close()
  print("\n File has been copied successfully \n")
  recv_conn.close()
  if plt_en:
    print("\n Plotting... \n")
  
    plt.clf()

    plt.figure(1)
    plt.subplot(211)

    acc_data = np.genfromtxt(rcv_filename, delimiter=',', names=True)
    acc_x, freq_x, _ = mlab.specgram(acc_data['x'], Fs=SAMPLE_RATE, NFFT=SAMPLE_RATE * SMAPLE_TIME)
    acc_y, freq_y, _ = mlab.specgram(acc_data['y'], Fs=SAMPLE_RATE, NFFT=SAMPLE_RATE * SMAPLE_TIME)
    acc_z, freq_z, _ = mlab.specgram(acc_data['z'], Fs=SAMPLE_RATE, NFFT=SAMPLE_RATE * SMAPLE_TIME)
  
    data_fft = np.column_stack((freq_x,acc_x,acc_y,acc_z))
    np.savetxt(fft_filename, data_fft, delimiter=',', header="f,ax,ay,az")
  
    plt.plot(freq_x[10:], acc_x[10:], label='x', linewidth=0.5)
    plt.plot(freq_y[10:], acc_y[10:], label='y', linewidth=0.5)
    plt.plot(freq_z[10:], acc_z[10:], label='z', linewidth=0.5)
  
    plt.yscale('log')
    plt.xlim((0, 200))
    plt.legend(loc='upper right')
    plt.title('FFT')
  
    #PLOT THE ACCELERATIONS
    plt.subplot(212)

    plt.plot(acc_data['time'][10:],acc_data['x'][10:],label='x', linewidth=0.5)
    plt.plot(acc_data['time'][10:],acc_data['y'][10:],label='y', linewidth=0.5)
    plt.plot(acc_data['time'][10:],acc_data['z'][10:],label='z', linewidth=0.5)
    plt.legend(loc='upper right')
    plt.title("Acceleration")
  
    plt.show()


if __name__ == '__main__':

  try:
    opts,args = getopt.getopt(sys.argv[1:],"hp",["--plot"])
  except getopt.GetoptError:
    print('try trigger.py -p')
    sys.exit(2)
  
  print("plot disabled")
  plot_en = False
  
  for opt, arg in opts:
    if opt == '-p':
      print("plot enabled")
      plot_en = True
      
  print("starting process")
  while True: 
    myconn,addr_conn = server_socket.accept()
    print(f"connected to {addr_conn}")
    start_new_thread(threaded_recv,(myconn, plot_en, ) )
  server_socket.close()
