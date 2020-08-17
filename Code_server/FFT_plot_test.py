"""
FFT plot test

"""

import matplotlib.pyplot as plt
from matplotlib import mlab
import numpy as np
#from scipy.fft import fft # alternative form

f1    = 10    # frecuencia menor detectable. [hz]
f2    = 1500  # frecuencia mayor detectable. [hz]

f_s = 3200    # frecuencia de muestreo [hz]
t_s = 1.0/f_s # Tiempo de sampleo.[s]

T = 2.5           #Tiempo total de sampleo. [s]
N = int(T/t_s)  #Cantidad de muestras. [#]
print(N)



t = np.linspace(0,T,int(N), endpoint =False)
x = np.sin(f1*2*np.pi*t)+np.sin(f2*2*np.pi*t)


fig1 = plt.figure(1)
plt.plot(t,x)

plt.xlabel('Time [s]')
plt.ylabel('Signal amplitude')

##Alternative form using scipy lib
#X = fft(x) # the result have shifted the output so yo need reordenate it
#X_pos = X[0:int(N/2)]
#X_neg = X[int(N/2):int(N)]
#X = np.concatentate((X_neg,X_pos)) 
#f = np.linspace(-f_s/2, f_s/2,int(N)) #scaling frecuency vector

X = np.fft.fft(x)
f =(1/t_s)*np.fft.fftfreq(int(N))

fig2 = plt.figure(2)

#plt.plot(f,(2.0/N)*np.abs(X))
plt.plot(f,(2.0/N)*np.abs(X))
plt.xlabel('frecuency [s]')
plt.ylabel('Magnitude')


fig3 = plt.figure(3)

P, freqs, _ = mlab.specgram(x,Fs=f_s,NFFT=N)

plt.plot(freqs[10:], P[10:],linewidth = 1)


plt.show()
