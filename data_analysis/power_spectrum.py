# Estimating Welch's periodogram of EEG captured signals from Montreal and Stroop tasks
# Author : Mateus Camargo Pedrino
# Digital Signal Processing laboratory : University of São Paulo (SEL/EESC/USP)

import pandas as pd
import scipy.signal as sg
import scipy.stats as ss
import matplotlib.pyplot as plt
import numpy as np


# Raw files reading
df_norm=np.transpose(np.loadtxt('normal.txt'))
df_montreal=np.transpose(np.loadtxt('montreal.txt'))
df_stroop=np.transpose(np.loadtxt('stroop.txt'))


# Remove first 256 data samples from each channel (size of filtering mask)
# The temporal windows were chosen considering intervals where the fenomenum is proved to be more
# perceptible e instervals with less amount of noise.

aux_norm=[]
aux_stroop=[]
aux_montreal=[]
for i in range(0,8):
    aux_norm.append(df_norm[i][56*250:106*250])
    aux_montreal.append(df_montreal[i][536*250:586*250])
    aux_stroop.append(df_stroop[i][15*250:65*250])

df_norm=[i*10E-6 for i in aux_norm]   # Compute PSD considering amplitude in uV
df_stroop=[i*10E-6 for i in aux_stroop]
df_montreal=[i*10E-6 for i in aux_montreal]

# Temporal vectors of each channel
SampleRate=250
# Normal activity
t_norm=[]
for i in range(0,8):
    t_norm.append((1/SampleRate)*np.arange(0,len(df_norm[i]),1))

# Stroop test
t_stroop=[]
for i in range(0,8):
    t_stroop.append((1/SampleRate)*np.arange(0,len(df_stroop[i]),1))

# Montreal test
t_montreal=[]
for i in range(0,8):
    t_montreal.append((1/SampleRate)*np.arange(0,len(df_montreal[i]),1))

# Temporal plots

# Normal activity
figt_norm, axest_norm = plt.subplots(8, 1)
for i in range(0,8):
    axest_norm[i].plot(t_norm[i],df_norm[i])
figt_norm.suptitle("Sinais no dominio do tempo - Atividade normal", fontsize="x-large")

# Stroop test
figt_stroop, axest_stroop = plt.subplots(8, 1)
for i in range(0,8):
    axest_stroop[i].plot(t_stroop[i],df_stroop[i])
figt_stroop.suptitle("Sinais no dominio do tempo - Stroop test", fontsize="x-large")

# Montreal test
figt_montreal, axest_montreal = plt.subplots(8, 1)
for i in range(0,8):
    axest_montreal[i].plot(t_montreal[i],df_montreal[i])
figt_montreal.suptitle("Sinais no dominio do tempo - Montreal test", fontsize="x-large")

# Power spectrum

# Normal acitivity 
fige_norm, axese_norm = plt.subplots(8, 1)
P_norm=[]
f_norm=[]
for i in range(0,8):
    f_aux,P_aux = sg.welch(df_norm[i],SampleRate)
    f_norm.append(f_aux)
    P_norm.append(P_aux)
    axese_norm[i].plot(f_norm[i],P_norm[i])
    axese_norm[i].set_xlim(0,60)
fige_norm.suptitle("Espectro de potencia - Atividade Normal", fontsize="x-large")

# Stroop test
fige_stroop, axese_stroop = plt.subplots(8, 1)
P_stroop=[]
f_stroop=[]
for i in range(0,8):
    f_aux,P_aux = sg.welch(df_stroop[i],SampleRate)
    f_stroop.append(f_aux)
    P_stroop.append(P_aux)
    axese_stroop[i].plot(f_stroop[i],P_stroop[i])
    axese_stroop[i].set_xlim(0,60)
fige_stroop.suptitle("Espectro de potencia - Stroop test", fontsize="x-large")

# Montreal test
fige_montreal, axese_montreal = plt.subplots(8, 1)
P_montreal=[]
f_montreal=[]
for i in range(0,8):
    f_aux,P_aux = sg.welch(df_montreal[i],SampleRate)
    f_montreal.append(f_aux)
    P_montreal.append(P_aux)
    axese_montreal[i].plot(f_montreal[i],P_montreal[i])
    axese_montreal[i].set_xlim(0,60)
fige_montreal.suptitle("Espectro de potencia - Montreal test", fontsize="x-large")

# All spectrums together 
fige_junto, axese_junto = plt.subplots(8, 1, sharex=True)
for i in range(0,8):
    axese_junto[i].plot(f_norm[i],P_norm[i],f_montreal[i],P_montreal[i],f_stroop[i],P_stroop[i])
    if i==0: # In order to plot clearer
        axese_junto[i].legend(('Normal','Montreal','Stroop'))
    if i==7:
        axese_junto[i].set_xlabel('f [Hz]')
    axese_junto[i].set_xlim(4,30)
    axese_junto[i].set_ylabel('P'+str(i+1))
fige_junto.suptitle("PSD [V²/Ω*Hz]", fontsize="x-large")
#fige_junto.tight_layout()

#####################################################
plt.show()
#####################################################


