import matplotlib    
print(matplotlib.matplotlib_fname())
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

import numpy as np
import cartopy.crs as ccrs
import random
import cartopy.feature as cf
import pandas as pd
from geopy.geocoders import Nominatim
import matplotlib.cm as cm
from matplotlib.colors import ListedColormap
import matplotlib.ticker as ticker

font_path = '/home/aobo/Operation-aware/Times New Roman.ttf'
prop = fm.FontProperties(fname=font_path)
df = pd.read_csv('world_map_city_fuel.csv')

# geolocator = Nominatim(user_agent="my_app")

# df['Dep longitude'] = None
# df['Dep latitude'] = None
# df['Arr longitude'] = None
# df['Arr latitude'] = None

# # 获取每行的出发地和目的地的经纬度信息
# for index, row in df.iterrows():
#     print(index)
#     dep_location = geolocator.geocode(row['Dep'])
#     arr_location = geolocator.geocode(row['Arr'])
#     if dep_location is not None:
#         df.loc[index, 'Dep longitude'] = dep_location.longitude
#         df.loc[index, 'Dep latitude'] = dep_location.latitude
#     if arr_location is not None:
#         df.loc[index, 'Arr longitude'] = arr_location.longitude
#         df.loc[index, 'Arr latitude'] = arr_location.latitude

# df.to_csv('world_map_city_fuel.csv', index=False)

fig = plt.figure(figsize=(40, 18), dpi=180)
ax = plt.axes(projection=ccrs.Robinson())
ax.set_global()

cmap = ListedColormap(cm.plasma.colors[::-1])
# cmap = cm.get_cmap('plasma')


normalize = plt.Normalize(vmin=50, vmax=1400)
scalar_map = cm.ScalarMappable(cmap=cmap, norm=normalize)

for index, row in df.iterrows():
    dep_lon = row['Dep longitude']
    dep_lat = row['Dep latitude']
    arr_lon = row['Arr longitude']
    arr_lat = row['Arr latitude']
    fuel = row['Fuel'] / 1000
    max_fuel = df['Fuel'].max() / 1000
    alpha = fuel / max_fuel
    color = scalar_map.to_rgba(fuel)
    # cmap = ListedColormap(cm.plasma.colors[::-1])
    # cmap = cm.get_cmap('seismic')
    color = cmap(alpha) 
    ax.plot([dep_lon, arr_lon], [dep_lat, arr_lat], transform=ccrs.Geodetic(), color=color, linewidth=2)
    ax.scatter([dep_lon, arr_lon], [dep_lat, arr_lat], transform=ccrs.Geodetic(), color=color, s=60)
    
    
ax.add_feature(cf.COASTLINE, linewidth=0.5, alpha=0.3)
ax.add_feature(cf.BORDERS, linewidth=0.5, alpha=0.3)
cax = fig.add_axes([0.87, 0.1, 0.01, 0.7])
cbar = plt.colorbar(scalar_map, cax=cax, format=ticker.ScalarFormatter(useOffset=False))
cbar.ax.tick_params(labelsize=30)
cbar.set_ticks(np.linspace(50, 1400, 8))
formatter = ticker.ScalarFormatter(useMathText=True)
formatter.set_powerlimits((-4, 4)) 

cbar.formatter = formatter

cbar.update_ticks()

# cbar.set_clim(50e3, 1400e3)
plt.title('Fuel (t)', fontproperties=prop, fontsize=40, y=1.05)

plt.savefig('world_map.pdf',bbox_inches='tight',pad_inches=0.2)