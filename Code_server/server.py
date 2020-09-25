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
import sys
import trigger
#imports for do math and plot
import numpy as np
from matplotlib import mlab
import matplotlib.pyplot as plt


PORT = 777
BUFF_SIZE = 4000

SAMPLE_RATE = 3200 # [Hz]
SMAPLE_TIME = 2.5  # [s]

PATH_DATA = "./recived_data/"
TYPE_DATA_ACC = "acc/"
TYPE_DATA_FFT = "fft/"

server_socket = socket.socket()

print("\n Server is listing on port:",PORT,"\n")

server_socket.bind(('',PORT))
server_socket.listen(10)
server_socket.settimeout(5.0)

time_now = datetime.now()
time_unix = str(int(time.mktime(time_now.timetuple())))

rcv_filename = PATH_DATA+TYPE_DATA_ACC+time_unix+".csv"

if __name__ == '__main__':
  while True:
    rcv_file = open(rcv_filename,"wb")
    print("\n data will be recived be ",rcv_filename," at server side")
    myconn,addr_conn = server_socket.accept()
    print("reciving data")
    myconn.settimeout(5.0)
    RecivedData = myconn.recv(BUFF_SIZE)
    print(RecivedData)
    while RecivedData:
      print("writing data")
      rcv_file.write(RecivedData)
      print("reciving another bounch of data")
      myconn.settimeout(5.0)
      RecivedData = myconn.recv(BUFF_SIZE)
      print(RecivedData)
    
    rcv_file.close()
    print("\n File has been copied successfully \n")
    
    myconn.close()
    print("\n Server closed the connection \n")
    server_socket.close()
    print("\n Plotting... \n")
    acc_data = np.genfromtxt(rcv_filename, delimiter=',', names=True)
    acc_x, freq_x, _ = mlab.specgram(acc_data['x'], Fs=SAMPLE_RATE, NFFT=SAMPLE_RATE * SMAPLE_TIME)
    acc_y, freq_y, _ = mlab.specgram(acc_data['y'], Fs=SAMPLE_RATE, NFFT=SAMPLE_RATE * SMAPLE_TIME)
    acc_z, freq_z, _ = mlab.specgram(acc_data['z'], Fs=SAMPLE_RATE, NFFT=SAMPLE_RATE * SMAPLE_TIME)
    plt.plot(freq_x[10:], acc_x[10:], label='x', linewidth=0.5)
    plt.plot(freq_y[10:], acc_y[10:], label='y', linewidth=0.5)
    plt.plot(freq_z[10:], acc_z[10:], label='z', linewidth=0.5)
    plt.yscale('log')
    plt.xlim((0, 160))
    plt.legend(loc='upper right')
    plt.show()
    plt.savefig('spectrum.png')

    break
