import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Olhar esses pdfs
# https://pdfs.semanticscholar.org/2bb5/53438cd587bc8b0a8d53f6aa493dcb8b7f35.pdf
# https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4427585/

# Data to plot at correlogram
# Stroop / Norm compared mean coherence
ratio_stroop_norm_theta=np.loadtxt('ratio_stroop_norm_theta.txt')
ratio_stroop_norm_alpha=np.loadtxt('ratio_stroop_norm_alpha.txt')
ratio_stroop_norm_beta=np.loadtxt('ratio_stroop_norm_beta.txt')

# Montreal / Norm compared mean coherence
ratio_montreal_norm_theta=np.loadtxt('ratio_montreal_norm_theta.txt')
ratio_montreal_norm_alpha=np.loadtxt('ratio_montreal_norm_alpha.txt')
ratio_montreal_norm_beta=np.loadtxt('ratio_montreal_norm_beta.txt')

# Labels of channels
N = ['FP2','FPz','F8','Cz','F4','P3','T6','T4']

# Mask to plot only the triangular matrix (because coherence is commutative)
minimo=min(np.min(ratio_stroop_norm_theta),np.min(ratio_montreal_norm_theta),np.min(ratio_stroop_norm_alpha),np.min(ratio_montreal_norm_alpha),np.min(ratio_stroop_norm_beta),np.min(ratio_montreal_norm_beta))
maximo=max(np.max(ratio_stroop_norm_theta),np.max(ratio_montreal_norm_theta),np.max(ratio_stroop_norm_alpha),np.max(ratio_montreal_norm_alpha),np.max(ratio_stroop_norm_beta),np.max(ratio_montreal_norm_beta))

# Theta
# Stroop/Norm
fig_t, ax_t = plt.subplots(1,2)
mask = np.zeros_like(ratio_stroop_norm_theta)
mask[np.triu_indices_from(mask)] = True
sns.heatmap(ratio_stroop_norm_theta, cbar=True, vmin=minimo, vmax=maximo ,ax=ax_t[0], mask=mask, square=True, xticklabels=N,yticklabels=N,cmap='seismic',center=1)
ax_t[0].set_title('Stroop/Normal')
# Montreal/Norm
mask = np.zeros_like(ratio_montreal_norm_theta)
mask[np.triu_indices_from(mask)] = True
sns.heatmap(ratio_montreal_norm_theta,  cbar=True, vmin=minimo, vmax=maximo, ax=ax_t[1], mask=mask, square=True, xticklabels=N,yticklabels=N,cmap='seismic',center=1)
ax_t[1].set_title('Montreal/Normal')
fig_t.suptitle('Theta - MSC ratios')

# Alpha
# Stroop/Norm
fig_a, ax_a = plt.subplots(1,2)
mask = np.zeros_like(ratio_stroop_norm_alpha)
mask[np.triu_indices_from(mask)] = True
sns.heatmap(ratio_stroop_norm_alpha, cbar=True, vmin=minimo, vmax=maximo ,ax=ax_a[0], mask=mask, square=True, xticklabels=N,yticklabels=N,cmap='seismic',center=1)
ax_a[0].set_title('Stroop/Normal')
# Montreal/Norm
mask = np.zeros_like(ratio_montreal_norm_alpha)
mask[np.triu_indices_from(mask)] = True
sns.heatmap(ratio_montreal_norm_alpha,  cbar=True, vmin=minimo, vmax=maximo, ax=ax_a[1], mask=mask, square=True, xticklabels=N,yticklabels=N,cmap='seismic',center=1)
ax_a[1].set_title('Montreal/Normal')
fig_a.suptitle('Alpha - MSC ratios')

# Beta
# Stroop/Norm
fig_b, ax_b = plt.subplots(1,2)
mask = np.zeros_like(ratio_stroop_norm_beta)
mask[np.triu_indices_from(mask)] = True
sns.heatmap(ratio_stroop_norm_beta, cbar=True, vmin=minimo, vmax=maximo ,ax=ax_b[0], mask=mask, square=True, xticklabels=N,yticklabels=N,cmap='seismic',center=1)
ax_b[0].set_title('Stroop/Normal')
# Montreal/Norm
mask = np.zeros_like(ratio_montreal_norm_beta)
mask[np.triu_indices_from(mask)] = True
sns.heatmap(ratio_montreal_norm_beta,  cbar=True, vmin=minimo, vmax=maximo, ax=ax_b[1], mask=mask, square=True, xticklabels=N,yticklabels=N,cmap='seismic',center=1)
ax_b[1].set_title('Montreal/Normal')
fig_b.suptitle('Beta - MSC ratios')






plt.show()
