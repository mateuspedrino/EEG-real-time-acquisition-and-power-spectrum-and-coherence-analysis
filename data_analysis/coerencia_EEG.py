# Estimating Welch's coherence of EEG captured signals from Montreal and Stroop tasks
# Author : Mateus Camargo Pedrino
# Digital Signal Processing laboratory : University of São Paulo (SEL/EESC/USP)

import pandas as pd
import scipy.signal as sg
import scipy.stats as ss
import matplotlib.pyplot as plt
import numpy as np

# Mean coherence of a band
def mean_coh_band(freq,Cxy,band):
    idx=np.logical_and(freq >= band[0], freq <= band[1])
    mean_coh=np.mean(Cxy[idx]) # Simpson rule
    return mean_coh

# Leitura dos raw files
df_norm=np.transpose(np.loadtxt('teste4/normal1.txt'))
df_montreal=np.transpose(np.loadtxt('teste4/montreal1.txt'))
df_stroop=np.transpose(np.loadtxt('teste4/stroop1.txt'))

# Remove first 256 data samples from each channel (size of filtering mask)
# The temporal windows were chosen considering intervals where the fenomenum is proved to be more
# perceptible e instervals with less amount of noise.

aux_norm=[]
aux_stroop=[]
aux_montreal=[]
inorm=90
istroop=100 
imontreal=490
dt=20
for i in range(0,8):
    aux_norm.append(df_norm[i][inorm*250:(inorm+dt)*250])
    aux_stroop.append(df_stroop[i][istroop*250:(istroop+dt)*250])
    aux_montreal.append(df_montreal[i][imontreal*250:(imontreal+dt)*250])

df_norm=[i*10E-6 for i in aux_norm]   # Considering amplitude in uV
df_stroop=[i*10E-6 for i in aux_stroop]
df_montreal=[i*10E-6 for i in aux_montreal]

Fa=250 # Sample Rate

NumChan=8 # Number of channels

theta = [4,7]
alpha = [8,12]
beta = [12, 30]

# Channels and positions :
# 0 ---- FP2
# 1 ---- FPz
# 2 ---- F8
# 3 ---- Cz
# 4 ---- F4
# 5 ---- P3
# 6 ---- T6
# 7 ---- T4

# Initialization : Coherence Matrixes (3D)
# Normal
f_aux, C_aux = sg.coherence(df_norm[0],df_norm[1],fs=Fa) # Extract size of Coh arrays
Coh_norm=np.zeros((NumChan,NumChan,len(C_aux))) 
f_norm=np.zeros((NumChan,NumChan,len(f_aux)))
# Stroop
f_aux, C_aux = sg.coherence(df_stroop[0],df_stroop[1],fs=Fa) # Extract size of Coh arrays
Coh_stroop=np.zeros((NumChan,NumChan,len(C_aux)))
f_stroop=np.zeros((NumChan,NumChan,len(f_aux)))
# Montreal
f_aux, C_aux = sg.coherence(df_montreal[0],df_montreal[1],fs=Fa) # Extract size of Coh arrays
Coh_montreal=np.zeros((NumChan,NumChan,len(C_aux)))
f_montreal=np.zeros((NumChan,NumChan,len(f_aux)))

# Compute coherence for each combination of each activity
for i in range(NumChan):
    for j in range(NumChan):
        f_norm[i,j], Coh_norm[i,j]=sg.coherence(df_norm[i],df_norm[j],fs=Fa)
        f_stroop[i,j], Coh_stroop[i,j]=sg.coherence(df_stroop[i],df_stroop[j],fs=Fa)
        f_montreal[i,j], Coh_montreal[i,j]=sg.coherence(df_montreal[i],df_montreal[j],fs=Fa)
        

# Initialize mean coherence matrixes (2D)
theta_mean_Coh_norm=np.zeros((NumChan,NumChan))
alpha_mean_Coh_norm=np.zeros((NumChan,NumChan))
beta_mean_Coh_norm=np.zeros((NumChan,NumChan))
theta_mean_Coh_stroop=np.zeros((NumChan,NumChan))
alpha_mean_Coh_stroop=np.zeros((NumChan,NumChan))
beta_mean_Coh_stroop=np.zeros((NumChan,NumChan))
theta_mean_Coh_montreal=np.zeros((NumChan,NumChan))
alpha_mean_Coh_montreal=np.zeros((NumChan,NumChan))
beta_mean_Coh_montreal=np.zeros((NumChan,NumChan))

# Compute mean coherence for each combination of each activity of each band
for i in range(NumChan):
    for j in range(NumChan):
        theta_mean_Coh_norm[i,j]=mean_coh_band(f_norm[i,j],Coh_norm[i,j],theta)
        alpha_mean_Coh_norm[i,j]=mean_coh_band(f_norm[i,j],Coh_norm[i,j],alpha)
        beta_mean_Coh_norm[i,j]=mean_coh_band(f_norm[i,j],Coh_norm[i,j],beta)
        theta_mean_Coh_stroop[i,j]=mean_coh_band(f_stroop[i,j],Coh_stroop[i,j],theta)
        alpha_mean_Coh_stroop[i,j]=mean_coh_band(f_stroop[i,j],Coh_stroop[i,j],alpha)
        beta_mean_Coh_stroop[i,j]=mean_coh_band(f_stroop[i,j],Coh_stroop[i,j],beta)
        theta_mean_Coh_montreal[i,j]=mean_coh_band(f_montreal[i,j],Coh_montreal[i,j],theta)
        alpha_mean_Coh_montreal[i,j]=mean_coh_band(f_montreal[i,j],Coh_montreal[i,j],alpha)
        beta_mean_Coh_montreal[i,j]=mean_coh_band(f_montreal[i,j],Coh_montreal[i,j],beta)

# Ratio between mean coherences to check increase or decrease with stress stimuli
# Initialization
ratio_stroop_norm_theta=np.zeros((NumChan,NumChan))
ratio_montreal_norm_theta=np.zeros((NumChan,NumChan))
ratio_stroop_norm_alpha=np.zeros((NumChan,NumChan))
ratio_montreal_norm_alpha=np.zeros((NumChan,NumChan))
ratio_stroop_norm_beta=np.zeros((NumChan,NumChan))
ratio_montreal_norm_beta=np.zeros((NumChan,NumChan))

# Compute ratios 
for i in range(NumChan):
    for j in range(NumChan):
        ratio_stroop_norm_theta[i,j]=theta_mean_Coh_stroop[i,j]/theta_mean_Coh_norm[i,j]
        ratio_montreal_norm_theta[i,j]=theta_mean_Coh_montreal[i,j]/theta_mean_Coh_norm[i,j]
        ratio_stroop_norm_alpha[i,j]=alpha_mean_Coh_stroop[i,j]/alpha_mean_Coh_norm[i,j]
        ratio_montreal_norm_alpha[i,j]=alpha_mean_Coh_montreal[i,j]/alpha_mean_Coh_norm[i,j]
        ratio_stroop_norm_beta[i,j]=beta_mean_Coh_stroop[i,j]/beta_mean_Coh_norm[i,j]
        ratio_montreal_norm_beta[i,j]=beta_mean_Coh_montreal[i,j]/beta_mean_Coh_norm[i,j]

# Save ratio matrix to generate conectogram
np.savetxt('ratio_stroop_norm_theta.txt',ratio_stroop_norm_theta,fmt='%.2f')
np.savetxt('ratio_stroop_norm_alpha.txt',ratio_stroop_norm_alpha,fmt='%.2f')
np.savetxt('ratio_stroop_norm_beta.txt',ratio_stroop_norm_beta,fmt='%.2f')
np.savetxt('ratio_montreal_norm_theta.txt',ratio_montreal_norm_theta,fmt='%.2f')
np.savetxt('ratio_montreal_norm_alpha.txt',ratio_montreal_norm_alpha,fmt='%.2f')
np.savetxt('ratio_montreal_norm_beta.txt',ratio_montreal_norm_beta,fmt='%.2f')

# Show Increase or decrease mean coherence rate during stress stimuli
print('\n')
print('Razoes - theta')
print('\n')

print('Stroop/Normal \n')
for i in range(NumChan):
    print(np.round_(ratio_stroop_norm_theta[i],2))
print('\n')

print('Montreal/Normal \n')
for i in range(NumChan):
    print(np.round_(ratio_montreal_norm_theta[i],2))
print('\n')

print('\n')
print('Razoes - alpha')
print('\n')
        
print('Stroop/Normal \n')
for i in range(NumChan):
    print(np.round_(ratio_stroop_norm_alpha[i],2))
print('\n')

print('Montreal/Normal \n')
for i in range(NumChan):
    print(np.round_(ratio_montreal_norm_alpha[i],2))
print('\n')

print('\n')
print('Razoes - beta')
print('\n')
        
print('Stroop/Normal \n')
for i in range(NumChan):
    print(np.round_(ratio_stroop_norm_beta[i],2))
print('\n')

print('Montreal/Normal \n')
for i in range(NumChan):
    print(np.round_(ratio_montreal_norm_beta[i],2))
print('\n')   