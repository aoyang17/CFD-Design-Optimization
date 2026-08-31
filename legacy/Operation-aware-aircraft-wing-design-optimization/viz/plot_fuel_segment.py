import os
import matplotlib    
print(matplotlib.matplotlib_fname())
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from prettytable import PrettyTable
import numpy as np
import cartopy.crs as ccrs
import random
import cartopy.feature as cf
import pandas as pd
from geopy.geocoders import Nominatim
import matplotlib.cm as cm
from matplotlib.colors import ListedColormap
import matplotlib.ticker as ticker
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
from matplotlib.ticker import FixedLocator, FixedFormatter

font_path = '/home/aobo/Operation-aware/Times New Roman.ttf'
prop = fm.FontProperties(fname=font_path)

df = pd.read_csv('/home/aobo/Operation-aware/mission_analysis/mission_analysis_database/GMM_entire_17pts/p3_short_88.csv')

weight_data = df['Weight']

# # 将每行的两个数字拆分开来
# split_weight_data = []
# for row in weight_data:
#     numbers = row.strip('[]').split(',')
#     split_weight_data.append(numbers)

# float_vectorize = np.vectorize(float)
# num_array = float_vectorize(split_weight_data[0][1])
# print(num_array)

def vertor_array(str):
    float_vectorize = np.vectorize(float)
    num_array = float_vectorize(str)
    return num_array


# print(vertor_array(split_weight_data[0][0])- vertor_array(split_weight_data[0][1]))

def process_file(df):
    segType = df["segType"]
    weight_data = df["Weight"]
    split_weight_data = []
    for row in weight_data:
        numbers = row.strip('[]').split(', ')
        split_weight_data.append(numbers)
    
    fuel_burn_segment = []
    for row , value in enumerate(split_weight_data):
        fuel_burn = vertor_array(split_weight_data[row][0])- vertor_array(split_weight_data[row][1])
        fuel_burn_segment.append(fuel_burn)
        
    return segType, fuel_burn_segment

def segment_fuel(df):
    segType, fuel_burn_segment = process_file(df)
    interval_values = fuel_burn_segment / np.sum(fuel_burn_segment)
    segment_relative_fuel = 1 - np.cumsum(interval_values)
    df_new = pd.DataFrame(columns=['Seg', 'relFuel'])
    df_new['Seg'] = segType
    df_new['relFuel'] = segment_relative_fuel
    return df_new


dfs = []
folder_path = "/home/aobo/Operation-aware/mission_analysis/mission_analysis_database/GMM_entire_17pts"
for file_name in os.listdir(folder_path):
    if file_name.endswith(".csv"): 
        file_path = os.path.join(folder_path, file_name)
        df = pd.read_csv(file_path) 
        df_new = segment_fuel(df)
        dfs.append(df_new)


cmap = ListedColormap(cm.plasma.colors[::-1])
normalize = plt.Normalize(vmin=50, vmax=1400)
scalar_map = cm.ScalarMappable(cmap=cmap, norm=normalize)

fig,ax = plt.subplots(1, figsize = (40, 18), dpi=180)

# ax.plot(df_new["relFuel"], '-o', markersize=15, alpha=1, c='b')
sorted_dfs = sorted(dfs, key=lambda df: df["relFuel"][4])
colors = cm.plasma(np.linspace(0, 1, len(dfs)))


for i, df in enumerate(sorted_dfs):
    color = colors[i]
    selected_indices = [0, 1, 2, 4, 5, 9]
    relFuel_selected = [df["relFuel"][index] for index in selected_indices]
    ax.plot(relFuel_selected, '-o', markersize=5, alpha=1, color=color)

ax.tick_params(axis='x', labelsize=25)
ax.tick_params(axis='y', labelsize=25)

ax.annotate('', xytext=(0,-0.05) , xy=(1, -0.05), arrowprops=dict(arrowstyle='|-|', linewidth=2))
ax.text(0.5, -0.1, 'Take off', ha='center', va='center', fontproperties=prop, fontsize=40)

ax.annotate('', xytext=(1,-0.05) , xy=(2,-0.05), arrowprops=dict(arrowstyle='|-|', linewidth=2))
ax.text(1.5, -0.1, 'Climb (accelerate)', ha='center', va='center', fontproperties=prop, fontsize=40)

ax.annotate('', xytext=(2,-0.05) , xy=(3,-0.05), arrowprops=dict(arrowstyle='|-|', linewidth=2))
ax.text(2.5, -0.1, 'Climb (constant mach)', ha='center', va='center', fontproperties=prop, fontsize=40)

ax.annotate('', xytext=(3,-0.05) , xy=(4,-0.05), arrowprops=dict(arrowstyle='|-|', linewidth=2))
ax.text(3.5, -0.1, 'Cruise', ha='center', va='center', fontproperties=prop, fontsize=40)

ax.annotate('', xytext=(4,-0.05) , xy=(5,-0.05), arrowprops=dict(arrowstyle='|-|', linewidth=2))
ax.text(4.5, -0.1, 'Descent', ha='center', va='center', fontproperties=prop, fontsize=40)

ax.set_xticks([])
ax.set_xticklabels([])
ax.set_ylim(bottom=-0.05)

ax.set_xlabel(r'Fuel segment', fontproperties=prop, fontsize=40)
ax.xaxis.set_label_coords(0.5, -0.10)
ax.set_ylabel('Fuel consumption proportion (%)', fontproperties=prop, fontsize=40)

relFuel_selected_all = [df["relFuel"][index] for df in sorted_dfs for index in selected_indices]
norm = plt.Normalize(min(relFuel_selected_all), max(relFuel_selected_all))
sm = plt.cm.ScalarMappable(cmap='plasma', norm=norm)
sm.set_array([])

cax = fig.add_axes([0.92, 0.1, 0.02, 0.75])
cbar = fig.colorbar(sm, cax=cax)
ticks = np.linspace(0, 1, 16) 
min_output = 1
max_output = 15.5

mapped_value = (ticks * (max_output - min_output)) + min_output

tick_labels = [str(value) for value in mapped_value]

tick_labels = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
cbar.ax.tick_params(labelsize=30)
plt.gca().get_yaxis().set_major_locator(FixedLocator(ticks))
plt.gca().get_yaxis().set_major_formatter(FixedFormatter(tick_labels))
plt.title('Flight hour (h)', fontproperties=prop, fontsize=40, y=1.05)
plt.savefig("relFuel_burn_segment.pdf",bbox_inches='tight',pad_inches=0.2)