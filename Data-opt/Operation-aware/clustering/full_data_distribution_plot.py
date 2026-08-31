import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import pandas as pd
import seaborn as sns
import numpy as np
from sklearn.mixture import GaussianMixture
from matplotlib.pyplot import figure
from matplotlib.patches import Rectangle
import matplotlib
import matplotlib.pyplot as plt

# print(matplotlib.get_cachedir())
plt.rc('font',family='Times New Roman')
pd = pd.read_csv('data.csv')
data = pd[['mach','aoa','alt']]

data = data[data.replace([np.inf, -np.inf], np.nan).notnull().all(axis=1)] 
data = data.dropna(how = 'all') 
# data = data[np.isfinite(data[['mach','aoa','alt']])]
# mach = data['mach']
# aoa = data['aoa']
# data['alt'] = data['alt'] * 0.3048

def pandas_filter(data):
    result = data.drop(data[(data['mach']>0.88) | (data['mach']<0.6)].index)
    result = result.drop(result[(result['alt']>41338.583) | (result['alt']<9842.52)].index)
    result = result.drop(result[(result['aoa']>3.5) | (result['aoa']<0.5)].index)
    data['alt'] = data['alt'] * 0.3048
    return result

df_data = pandas_filter(data)

df_data.to_csv("full_data_distribution.csv")

fig, axs = plt.subplots(1, 2, figsize=(50, 18), dpi=180)
# fig.suptitle('Axes values are scaled individually by default')
# axs.ticklabel_format(style='sci', scilimits=(-1,2), axis='both')
font1 = {'family': 'Times New Roman', 'weight': 'normal','size': 20}
font2 = {'family': 'Times New Roman', 'weight': 'normal','size': 50}

h = axs[0].hist2d(df_data['mach'], df_data['aoa'],norm=LogNorm(),density=True,bins=30,cmap='viridis')
# axs[0].ticklabel_format(style='sci', scilimits=(-1,2), axis='both', labelsize=30)

xmin, xmax, ymin, ymax = 0.6, 0.88, 0.5, 3.5
rect_1 = Rectangle((xmin, ymin), xmax-xmin, ymax-ymin,
             linewidth=2, edgecolor='r', facecolor='none')
axs[0].add_patch(rect_1)

axs[0].tick_params(axis='both', which='major', labelsize=30)
axs[0].set_xlabel('Mach number', font2)
axs[0].set_ylabel('Angle of attack ($^\circ$)', font2)

h = axs[1].hist2d(df_data['mach'], df_data['alt'],norm=LogNorm(),density=True,bins=30,cmap='viridis')

xmin_2, xmax_2, ymin_2, ymax_2 = 0.6, 0.88, 3000, 12600
rect_1 = Rectangle((xmin_2, ymin_2), xmax_2-xmin_2, ymax_2-ymin_2,
             linewidth=2, edgecolor='r', facecolor='none')
axs[0].add_patch(rect_1)

# axs[1].ticklabel_format(style='sci', scilimits=(-1,2), axis='both', labelsize=30)
axs[1].tick_params(axis='both', which='major', labelsize=30)
axs[1].set_xlabel('Mach number', font2)
axs[1].set_ylabel('Altitude ($m$)', font2)

rect = Rectangle((2.5, 7.5), 1.5, 2.5, linewidth=2, edgecolor='r', facecolor='none')
ax.add_patch(rect)

cbar = plt.colorbar(h[3], ax=axs)
cbar.ax.set_yticklabels(fontdict=font1)
plt.savefig('Aero_parameter_density_distributution.pdf',bbox_inches='tight',dpi=fig.dpi,pad_inches=0.2)
plt.show()
