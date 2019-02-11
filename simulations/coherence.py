# Coherence analysis using Welch's method with sine examples
# Author : Mateus Camargo Pedrino
# Digital Signal Processing laboratory : University of São Paulo (SEL/EESC/USP)

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy import signal
import math as m

#### Test signals
A=10
f=20
f2=30
Fs=20*f
N=1e6
t=np.arange(N) / Fs

####
y1=A*np.sin(2*np.pi*f*t) 
y2=4*A*np.sin(2*np.pi*f*t) # Modifica amplitude somente (em 4x A)
y3=A*np.sin(2*np.pi*f*t-np.pi/3) # Modifica fase (de 60 graus)
y4=A*np.sin(2*np.pi*f2*t) # Sinal de outra frequência
y5=A*np.sin(2*np.pi*f*t)+A*np.sin(2*np.pi*f2*t) # Sinal composto por duas senóides de freq distintas

y=[y1,y2,y3,y4,y5]

# Coherence computing
fc=[]
C=[]
for i in range(len(y)-1):
    faux,Caux=signal.coherence(y[0],y[i+1],fs=Fs)
    fc.append(faux)
    C.append(Caux)

# Plots
fig , ax = plt.subplots(len(C),2)
for i in range(len(C)):
    if i==0:
        ax[i,0].set_title('Sinais no tempo')
        ax[i,1].set_title('MSC de cada sinal')
    ax[i,0].plot(t[0:round((Fs/f)*2)],y[0][0:round((Fs/f)*2)],\
        t[0:round((Fs/f)*2)],y[i+1][0:round((Fs/f)*2)])
    ax[i,0].set_ylabel('('+str(i+1)+') A [V]')
    ax[i,0].set_xlabel('t [s]')
    ax[i,1].plot(fc[i],C[i])
    ax[i,1].set_ylabel('Coh')
    ax[i,1].set_xlabel('f [Hz]')
    ax[i,1].set_xlim(0,3*f)
    ax[i,1].set_ylim(-0.2,1.2)

fig.tight_layout()
plt.show()
