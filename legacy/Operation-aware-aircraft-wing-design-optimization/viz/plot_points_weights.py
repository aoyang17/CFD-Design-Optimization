import os
import pandas as pd
import numpy as np
import seaborn as sns

from matplotlib.colors import Normalize

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
from matplotlib.colors import LogNorm, Normalize
import matplotlib.font_manager as fm

font_path = '/home/aobo/Operation-aware/Times New Roman.ttf'
fm.fontManager.addfont(font_path)
# prop = fm.FontProperties(fname=font_path)

prop = fm.FontProperties(fname=font_path, weight='normal', size=30)

plt.rcParams['font.family'] = prop.get_family()
plt.rcParams['font.size'] = prop.get_size()


adodg_1 = pd.read_csv("/home/aobo/Operation-aware/Points_csv/ADODG_1pt.csv").sort_values(by='w', ascending=False)
adodg_9 = pd.read_csv("/home/aobo/Operation-aware/Points_csv/ADODG_9pt.csv").sort_values(by='w', ascending=False)
gmm_cruise_9 = pd.read_csv("/home/aobo/Operation-aware/Points_csv/GMM_cruise_9pts.csv").sort_values(by='w', ascending=False).iloc[:-1]
gmm_entire_9 = pd.read_csv("/home/aobo/Operation-aware/Points_csv/GMM_entire_9pts.csv").sort_values(by='w', ascending=False).iloc[:-1]
gmm_entire_17 = pd.read_csv("/home/aobo/Operation-aware/Points_csv/GMM_entire_17pts.csv").sort_values(by='w', ascending=False).iloc[:-1]
gmm_entire_22 = pd.read_csv("/home/aobo/Operation-aware/Points_csv/GMM_entire_22pts.csv").sort_values(by='w', ascending=False).iloc[:-1]

print(gmm_entire_22)

fig, axs = plt.subplots(1, 1, figsize=(26, 18), dpi=180)

# axs.plot(np.arange(len(adodg_1)),adodg_1[['w']], '-o', markersize=5, alpha=1, color='r')
axs.plot(np.arange(len(adodg_9)),adodg_9[['w']], '-o', markersize=8, linewidth= 3, alpha=1, color='red', label='9pt-ADODGCruise')
axs.plot(np.arange(len(gmm_cruise_9)),gmm_cruise_9[['w']], '-o', markersize=8, linewidth= 3, alpha=1, color='orange', label='9pt-CBCruise')
axs.plot(np.arange(len(gmm_entire_9)),gmm_entire_9[['w']], '-o', markersize=8, linewidth= 3, alpha=1, color='green', label='9pt-CBMission')
axs.plot(np.arange(len(gmm_entire_17)),gmm_entire_17[['w']], '-o', markersize=8, linewidth= 3, alpha=1, color='purple', label='17pt-CBMission')
axs.plot(np.arange(len(gmm_entire_22)), gmm_entire_22[['w']], '-o', markersize=8, linewidth= 3, alpha=1, color='brown', label='22pt-CBMission')

axs.set_xlabel('Point index', fontproperties=prop, fontsize=40)
axs.set_ylabel('Weight',fontproperties=prop, fontsize=40)
axs.tick_params(axis='both', which='major', labelsize=30)
axs.set_ylim(0, 0.32)
axs.legend(prop=prop,fontsize=40)
plt.savefig('Points_weights.pdf',bbox_inches='tight',dpi=fig.dpi,pad_inches=0.2)

