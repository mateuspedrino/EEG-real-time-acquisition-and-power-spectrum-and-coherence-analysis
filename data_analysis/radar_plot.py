# Estimating band's average power considering EEG captured signals from Montreal and Stroop tasks
# and generating starplots
# Author : Mateus Camargo Pedrino
# Digital Signal Processing laboratory : University of São Paulo (SEL/EESC/USP)

# Libraries
import pandas as pd
import scipy.signal as sg
import scipy.stats as ss
import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import simps
from math import pi

# Compute absolute power in band
def abs_power_of_band(freq,PSD,band):
    idx=np.logical_and(freq >= band[0], freq <= band[1])
    power=simps(PSD[idx], dx=(freq[1]-freq[0])) # Simpson rule
    return power

# Leitura dos raw files
df_norm=np.transpose(np.loadtxt('normal.txt'))
df_montreal=np.transpose(np.loadtxt('montreal.txt'))
df_stroop=np.transpose(np.loadtxt('stroop.txt'))

# Retira a janela de interesse no sinal
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

# ------- PART 1: Create background
ch_name = ['Fp2','Fpz','F8','Cz','F4','P3','T6','T4']

# number of variable
N=len(ch_name)
 
# What will be the angle of each axis in the plot? (we divide the plot / number of variable)
angles = [n / float(len(ch_name)) * 2 * pi for n in range(N)]
angles += angles[:1]
 
# Initialise the spider plot
ax = plt.subplot(111, polar=True)
 
# If you want the first axis to be on top:
ax.set_theta_offset(pi / 2)
ax.set_theta_direction(-1)
 
# Draw one axe per variable + add labels labels yet
plt.xticks(angles[:-1], ch_name)
 
# Draw ylabels
ax.set_rlabel_position(0)
plt.yticks(color="grey", size=7)
#plt.ylim(0,40)
 
# # ------- PART 2: Add plots
 
# # Plot each individual = each line of the data
# # I don't do a loop, because plotting more than 3 groups makes the chart unreadable
 
##### Really important : this kind of plot needs the user to comment or uncomment one 
##### of the three bands code below according to what the user wants to analyse. 
##### For instance : if you want to analyse the radar plot of theta activity (norma, stroop
##### and montreal) you should uncomment line 126 until line 138 and comment everything below
##### with exception of lines 176 and 178.

# Theta 
# Normal
theta_power_norm+=theta_power_norm[:1]
ax.plot(angles, theta_power_norm, color ='y', linewidth=1, linestyle='solid', label="Normal")
ax.fill(angles, theta_power_norm, 'y', alpha=0.1)
# Stroop
theta_power_stroop+=theta_power_stroop[:1]
ax.plot(angles, theta_power_stroop, color ='g', linewidth=1, linestyle='solid', label="Stroop")
ax.fill(angles, theta_power_stroop, 'g', alpha=0.1)
# Montreal
theta_power_montreal+=theta_power_montreal[:1]
ax.plot(angles, theta_power_montreal, color ='r', linewidth=1, linestyle='solid', label="Montreal")
ax.fill(angles, theta_power_montreal, 'r', alpha=0.1)

plt.title('Potências médias na banda theta [V²/Ω]')

# # Alfa 
# # Normal
# alpha_power_norm+=alpha_power_norm[:1]
# ax.plot(angles, alpha_power_norm, color ='y', linewidth=1, linestyle='solid', label="Normal")
# ax.fill(angles, alpha_power_norm, 'y', alpha=0.1)
# # Stroop
# alpha_power_stroop+=alpha_power_stroop[:1]
# ax.plot(angles, alpha_power_stroop, color ='g', linewidth=1, linestyle='solid', label="Stroop")
# ax.fill(angles, alpha_power_stroop, 'g', alpha=0.1)
# # Montreal
# alpha_power_montreal+=alpha_power_montreal[:1]
# ax.plot(angles, alpha_power_montreal, color ='r', linewidth=1, linestyle='solid', label="Montreal")
# ax.fill(angles, alpha_power_montreal, 'r', alpha=0.1)

# plt.title('Potências médias na banda alfa [V²/Ω]')

# # Beta
# # Normal
# beta_power_norm+=beta_power_norm[:1]
# ax.plot(angles, beta_power_norm, color ='y', linewidth=1, linestyle='solid', label="Normal")
# ax.fill(angles, beta_power_norm, 'y', alpha=0.1)
# # Stroop
# beta_power_stroop+=beta_power_stroop[:1]
# ax.plot(angles, beta_power_stroop, color ='g', linewidth=1, linestyle='solid', label="Stroop")
# ax.fill(angles, beta_power_stroop, 'g', alpha=0.1)
# # Montreal
# beta_power_montreal+=beta_power_montreal[:1]
# ax.plot(angles, beta_power_montreal, color ='r', linewidth=1, linestyle='solid', label="Montreal")
# ax.fill(angles, beta_power_montreal, 'r', alpha=0.1)

# plt.title('Potências médias na banda beta [V²/Ω]')


####### This part the user should never comment
# # Add legend
plt.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1))

plt.show()