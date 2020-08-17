"""
SMVA-Server code testing
using socket. 

"""

from datetime import datetime
import numpy as np
from matplotlib import mlab
import matplotlib.pyplot as plt


PORT = 777
BUFF_SIZE = 1024

SAMPLE_RATE = 2000 # [Hz]
SMAPLE_TIME = 1    # [s]

acc_data = np.genfromtxt("03-08-2020_03-05-59_PM.CSV", delimiter=',', names=True)
acc_x, freq_x, _ = mlab.specgram(acc_data['x'], Fs=SAMPLE_RATE, NFFT=SAMPLE_RATE * SMAPLE_TIME)
acc_y, freq_y, _ = mlab.specgram(acc_data['y'], Fs=SAMPLE_RATE, NFFT=SAMPLE_RATE * SMAPLE_TIME)
acc_z, freq_z, _ = mlab.specgram(acc_data['z'], Fs=SAMPLE_RATE, NFFT=SAMPLE_RATE * SMAPLE_TIME)
#plt.plot(freq_x[10:], acc_x[10:], label='x', linewidth=0.5)
#plt.plot(freq_y[10:], acc_y[10:], label='y', linewidth=0.5)
#plt.plot(freq_z[10:], acc_z[10:], label='z', linewidth=0.5)
#plt.yscale('log')
#plt.xlim((0, 160))
#plt.legend(loc='upper right')
#plt.show()
#plt.savefig('spectrum.png')

plt.plot(acc_data['time'][10:], acc_data['x'][10:], label='x', linewidth=0.5)
plt.plot(acc_data['time'][10:], acc_data['y'][10:], label='y', linewidth=0.5)
plt.plot(acc_data['time'][10:], acc_data['z'][10:], label='z', linewidth=0.5)
plt.legend(loc='upper right')
plt.ylim((0,4))
plt.xlim((0, 1))
plt.show()