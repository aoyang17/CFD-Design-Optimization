import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# airlines_facts = pd.read_excel(r"C:/Users/aobo/Desktop/Facts_2014-2017_UST-yuan-ubuntu.xlsx")
# AC_list = ['77H', '74N', '777P', '774F', '773P', '74K', '77G', '7RF',  '744A', 'ABYF', 'LD7', '74CF', '5Y8', '5Y4', '76Y' ]
# airlines_77 = airlines_facts[airlines_facts["AC Type"].isin(AC_list)]

airlines_77 = pd.read_csv("Facts_airlines_77.csv")

airlines_77['category'] = pd.cut(airlines_77.iloc[:, 12], bins=[0, 300, 600, 1200, np.inf], labels=['Short haul', 'Medium haul', 'Long haul', 'Ultra long haul'])
sample = airlines_77.sample(n=100)
sample = sample[['Dep','Arr','Flt Time','category']]

busiest_airlines = pd.read_excel("busiest_airlines.xlsx")

busiest_airlines['category'] = pd.cut(busiest_airlines.iloc[:, 4], bins=[0, 1100, 3500, np.inf], labels=['Short haul', 'Medium haul', 'Long haul'])

count_busiest = busiest_airlines['category'].value_counts()
labels_busiest = count_busiest.index.tolist()
sizes_busiest = count_busiest.tolist()
colors_busiest = ["#B9DDF1", "#9FCAE6", "#73A4CA", "#497AA7"]

count_2 = busiest_airlines['category'].value_counts()
labels_2 = count_2.index.tolist()
sizes_2 = count_2.tolist()

colors_2 = ["#B9DDF1", "#9FCAE6", "#73A4CA", "#497AA7"]


airlines_77['category'] = pd.cut(airlines_77.iloc[:, 12], bins=[0, 300, 600, 1200, np.inf], labels=['Short haul', 'Medium haul', 'Long haul', 'Ultra long haul'])

count_77 = airlines_77['category'].value_counts()
labels_77 = count_77.index.tolist()
sizes_77 = count_77.tolist()
colors_77 = ["#B9DDF1", "#9FCAE6", "#73A4CA", "#497AA7", "#2E5B88"]



fig = plt.figure(figsize=(20,10),dpi=180)

font2 = {'family': 'Times New Roman', 'weight': 'normal','size': 30}

ax1 = fig.add_subplot(121)
ax1.pie(sizes_77, labels = labels_77, colors = colors_77, autopct='%1.1f%%', 
    wedgeprops = {"linewidth": 3, "edgecolor": "white"}, textprops={'fontsize': 40})


ax2 = fig.add_subplot(122)
ax2.pie(sizes_2, labels = labels_2, colors = colors_2, autopct='%1.1f%%', 
    wedgeprops = {"linewidth": 3, "edgecolor": "white"}, textprops={'fontsize': 40})

plt.savefig('Pie_concerns_flights.pdf',bbox_inches='tight',dpi=fig.dpi,pad_inches=0.2)
plt.savefig('Pie_concerns_flights.png',bbox_inches='tight',dpi=fig.dpi,pad_inches=0.2)
plt.show()


