# Simulation of power espctral density estimation : Welch vs Periodogram
# Author : Mateus Camargo Pedrino
# Digital Signal Processing laboratory : University of São Paulo (SEL/EESC/USP)

import numpy as np 
import scipy.signal as sg
import matplotlib.pyplot as plt
import math as m

# Generate sine + SNR with less cicles in order to be comfortably shown in time domain
def noisy_sine_to_plot(sine_amplitude,f,Fs,Ncycles,snr_db):
    var_noise=((sine_amplitude**2)/2)*(10**(-snr_db/10))
    mean=0
    std=m.sqrt(var_noise)
    t=np.linspace(0,Ncycles*1/f,Fs*Ncycles)
    y=sine_amplitude*np.sin(2 * np.pi * f * t)
    n=np.random.normal(mean, std, len(y))
    return t,y+n

# Sine that will be indeed used for power spectrum analysis
def noisy_sine(sine_amplitude,f,Fs,N,snr_db):
    var_noise=((sine_amplitude**2)/2)*(10**(-snr_db/10))
    mean=0
    std=m.sqrt(var_noise)
    t=np.arange(N) / Fs
    y=sine_amplitude*np.sin(2 * np.pi * f * t)
    n=np.random.normal(mean, std, len(y))
    return t,y+n

# Setup
A=10
f=60
Fs=5*f
N=1e5
Ncycles=5
snrs=[40,20,10]
t=[]
y=[]
for i in range(len(snrs)):
    t_aux , y_aux = noisy_sine(A,f,Fs,N,snrs[i])
    t.append(t_aux)
    y.append(y_aux)

# Power spectrum
# Welch
f_welch=[]
P_welch=[]
for i in range(len(snrs)):
    f_aux, P_aux = sg.welch(y[i],Fs,'flattop', 1024, scaling='spectrum')
    f_welch.append(f_aux)
    P_welch.append(P_aux)

# Regular periodogram
f_periodogram=[]
P_periodogram=[]
for i in range(len(snrs)):
    f_aux, P_aux = sg.periodogram(y[i],Fs,'flattop', scaling='spectrum')
    f_periodogram.append(f_aux)
    P_periodogram.append(P_aux)
       
# Plots
fig, ax = plt.subplots(len(snrs),2)
for i in range(len(snrs)):
    taux,yaux=noisy_sine_to_plot(A,f,Fs,Ncycles,snrs[i])
    ax[i,0].plot(taux,yaux)
    ax[i,0].set_xlabel('t [s]')
    ax[i,0].set_ylabel('Amp [V]')
    ax[i,0].set_title('SNR de '+str(snrs[i])+'dB')
    ax[i,1].semilogy(f_welch[i],P_welch[i])
    ax[i,1].set_xlabel('f [Hz]')
    ax[i,1].set_ylabel('P [V²/Ω*Hz]')
    ax[i,1].set_xlim(0,100)
    if i==0:
       ax[i,1].set_title('Espectros lineares - Welch')

fig2, ax2 = plt.subplots(len(snrs),2)
for i in range(len(snrs)):
    taux,yaux=noisy_sine_to_plot(A,f,Fs,Ncycles,snrs[i])
    ax2[i,0].plot(taux,yaux)
    ax2[i,0].set_xlabel('t [s]')
    ax2[i,0].set_ylabel('Amp [V]')
    ax2[i,0].set_title('SNR de '+str(snrs[i])+'dB')
    ax2[i,1].semilogy(f_periodogram[i],P_periodogram[i])
    ax2[i,1].set_xlabel('f [Hz]')
    ax2[i,1].set_ylabel('P [V²/Ω*Hz]')
    ax2[i,1].set_xlim(0,100)
    if i==0:
       ax2[i,1].set_title('Espectros lineares - Periodograma')

fig.tight_layout()
fig2.tight_layout()
plt.show()
