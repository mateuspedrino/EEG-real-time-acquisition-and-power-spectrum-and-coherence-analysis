# Estimating band's average power considering EEG captured signals from Montreal and Stroop tasks
# Author : Mateus Camargo Pedrino
# Digital Signal Processing laboratory : University of São Paulo (SEL/EESC/USP)

import pandas as pd
import scipy.signal as sg
import scipy.stats as ss
import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import simps

# Compute absolute power in band
def abs_power_of_band(freq,PSD,band):
    idx=np.logical_and(freq >= band[0], freq <= band[1])
    power=simps(PSD[idx], dx=(freq[1]-freq[0])) # Simpson rule
    return power


# Raw files reading
df_norm=np.transpose(np.loadtxt('normal.txt'))
df_montreal=np.transpose(np.loadtxt('montreal.txt'))
df_stroop=np.transpose(np.loadtxt('stroop.txt'))

# Window the interest part in signals
aux_norm=[]
aux_stroop=[]
aux_montreal=[]
for i in range(0,8):
    aux_norm.append(df_norm[i][56*250:106*250])
    aux_montreal.append(df_montreal[i][536*250:586*250])
    aux_stroop.append(df_stroop[i][15*250:65*250])

df_norm=[i*10E-6 for i in aux_norm]
df_stroop=[i*10E-6 for i in aux_stroop]
df_montreal=[i*10E-6 for i in aux_montreal]

# Compute PSD 
SampleRate = 250
P_norm=[]
f_norm=[]
P_montreal=[]
f_montreal=[]
P_stroop=[]
f_stroop=[]

for i in range(0,8):
    f_aux,P_aux = sg.welch(df_norm[i],SampleRate)
    f_norm.append(f_aux)
    P_norm.append(P_aux)
    f_aux,P_aux = sg.welch(df_montreal[i],SampleRate)
    f_montreal.append(f_aux)
    P_montreal.append(P_aux)
    f_aux,P_aux = sg.welch(df_stroop[i],SampleRate)
    f_stroop.append(f_aux)
    P_stroop.append(P_aux)

# Absolute power computing
# Bands
theta = [4,7]
alpha = [8,12]
beta = [12, 30]

# Normal
theta_power_norm=[]
alpha_power_norm=[]
beta_power_norm=[]

# Montreal
theta_power_montreal=[]
alpha_power_montreal=[]
beta_power_montreal=[]

# Stroop
theta_power_stroop=[]
alpha_power_stroop=[]
beta_power_stroop=[]

for i in range(0,8):
    # Normal
    theta_power_norm.append(abs_power_of_band(f_norm[i],P_norm[i],theta))
    alpha_power_norm.append(abs_power_of_band(f_norm[i],P_norm[i],alpha))
    beta_power_norm.append(abs_power_of_band(f_norm[i],P_norm[i],beta))
    # Montreal
    theta_power_montreal.append(abs_power_of_band(f_montreal[i],P_montreal[i],theta))
    alpha_power_montreal.append(abs_power_of_band(f_montreal[i],P_montreal[i],alpha))
    beta_power_montreal.append(abs_power_of_band(f_montreal[i],P_montreal[i],beta))
    # Stroop
    theta_power_stroop.append(abs_power_of_band(f_stroop[i],P_stroop[i],theta))
    alpha_power_stroop.append(abs_power_of_band(f_stroop[i],P_stroop[i],alpha))
    beta_power_stroop.append(abs_power_of_band(f_stroop[i],P_stroop[i],beta))


# Generate results
print('\n\n\n')
print('Razao de potencia de montreal em relacao a normal (abs) :')
print('Theta :')
for i in range(0,8):
    print('Canal '+str(i)+' = '+str(theta_power_montreal[i]/theta_power_norm[i]))
print('Alpha :')
for i in range(0,8):
    print('Canal '+str(i)+' = '+str(alpha_power_montreal[i]/alpha_power_norm[i]))
print('Beta :')
for i in range(0,8):
    print('Canal '+str(i)+' = '+str(beta_power_montreal[i]/beta_power_norm[i]))

print('\n\n\n')

print('Razao de potencia de stroop em relacao a normal (abs) :')
print('Theta :')
for i in range(0,8):
    print('Canal '+str(i)+' = '+str(theta_power_stroop[i]/theta_power_norm[i]))
print('Alpha :')
for i in range(0,8):
    print('Canal '+str(i)+' = '+str(alpha_power_stroop[i]/alpha_power_norm[i]))
print('Beta :')
for i in range(0,8):
    print('Canal '+str(i)+' = '+str(beta_power_stroop[i]/beta_power_norm[i]))

