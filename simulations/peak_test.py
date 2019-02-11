# Peak espectral analysis using Welch's modified periodogram
# Author : Mateus Camargo Pedrino
# Digital Signal Processing laboratory : University of São Paulo (SEL/EESC/USP)

import pandas as pd
import scipy.signal as sg
import scipy.stats as ss
import matplotlib.pyplot as plt
import numpy as np

# Setup sine
N=1e5
A=10
f=60
Fs=5*f
t=np.arange(N) / Fs
y_sine=A*np.sin(2 * np.pi * f * t)

# Insert peaks in random places
num_peaks=[10,20,30]
prop=[10,15,20]
peaked_signal=[]
for i in range(len(num_peaks)):
    aux=list(y_sine)
    idx_aux=np.random.randint(0,N,num_peaks[i])
    for j in range(num_peaks[i]): aux[idx_aux[j]]=aux[idx_aux[j]]+y_sine[idx_aux[j]]*prop[i]
    peaked_signal.append(aux)

# Power espctrum through Welch's method
f=[]
P=[]
for i in range(len(num_peaks)):
    f_aux, P_aux = sg.welch(peaked_signal[i],Fs,'flattop', 1024, scaling='spectrum')
    f.append(f_aux)
    P.append(P_aux)

# Plots
fig,ax=plt.subplots(len(num_peaks),2)
for i in range(len(num_peaks)):
    ax[i,0].plot(t,peaked_signal[i])
    ax[i,0].set_xlabel('t [s]')
    ax[i,0].set_ylabel('Amp [V]')
    ax[i,0].set_title(str(num_peaks[i])+' picos com prop='+str(prop[i]))
    ax[i,1].plot(f[i],P[i])
    if i==0:
        ax[i,1].set_title('Respectivos espectros')
    ax[i,1].set_xlabel('f [Hz]')
    ax[i,1].set_ylabel('P [V²/Ω*Hz]')
    ax[i,1].set_xlim(0,100)

fig.tight_layout()

plt.show()



