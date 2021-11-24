# file: with_without_skewed_indexing.ipynb
# vi: filetype=python

# -------- code --------
from matplotlib.ticker import FuncFormatter

def my_formatter(x, pos):
    if x.is_integer():
        return "%d " % int(x)
    else:
        return "{0:.1f} ".format(x)
    
def my_formatter1(x, pos):
    return ""

formatter = FuncFormatter(my_formatter)
formatter1 = FuncFormatter(my_formatter1)

# -------- code --------
import re
from scipy.stats.mstats import gmean
import pandas as pd

trace_file="../Champsim-Prefetcher-Thesis/scripts/micro_trace_list.txt"

micro_results_folder="../Champsim-Prefetcher-Thesis/micro_sota_50M/"

before_pref="-hashed_perceptron-"
after_pref_cvp="-ipcp_isca-ipcp_isca-no-no-no-no-lru-lru-lru-srrip-drrip-lru-lru-lru-1core-cvp_trace.txt"

pref = ['csbtb_4k','csbtb_8k','mbtb_4k_noskew_2variants_2cycle', 'mbtb_8k_noskew_2variants_2cycle','mbtb_4k_2variants_2cycle',\
        'mbtb_8k_2variants_2cycle','perfect_btb']

server = []

for i in range(len(pref)):
    server.append([])

def get_ipc(file_name):
    temp_file = open(file_name)
    for line1 in temp_file:
        if re.search("CPU 0 cumulative IPC:", line1):
            return float(line1.split(" ")[4].strip())
    return 0.0

trace_file_ptr = open(trace_file, "r")
for line in trace_file_ptr:
    base_ipc = get_ipc(micro_results_folder+line.strip()+before_pref+"baseline"+after_pref_cvp)
    for i in range(len(pref)):
        curr_ipc = get_ipc(micro_results_folder+line.strip()+before_pref+pref[i]+after_pref_cvp)
        if curr_ipc == 0:
            continue
        server[i].append(curr_ipc/base_ipc)
        
server_df = {}
for i in range(len(server)):
    server_df[pref[i]] = gmean(server[i])

print(server_df)


# -------- code --------
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter
from scipy.stats.mstats import gmean
import matplotlib.transforms as mtransforms
from matplotlib.patches import FancyBboxPatch
import os
import math
import matplotlib.pylab as pylab

font_size=18

params = {'legend.fontsize': font_size,
          'figure.figsize': (15, 5),
         'axes.labelsize': font_size,
         'axes.titlesize':font_size,
         'xtick.labelsize':font_size,
         'ytick.labelsize':font_size}
pylab.rcParams.update(params)

cache_configs=["512KB_2MB", "256KB_2.5MB", "1MB_1.375MB"]

#data.head()
#data.iat[2,2]

policy = ["Non Inclusive", "Seclusive"]
pdist = [-0.5,0.5]
width = 0.4

x_labels = ["SPEC 2017 traces", "Client traces", "Server traces", "CVP traces"]
colors = ["black", "white"]

fig, cells = plt.subplots(nrows = 1, ncols = 1,figsize=(8,4),sharex=True)


cell = cells

temp_df = []
for i in range(0,len(pref)):
    temp_df.append((server_df[pref[i]]-1)*100)
ind = np.arange(len(pref))

cell.bar(ind, temp_df,width,edgecolor='black',color='grey',label = 'BASELINE SYSTEM')

cell.axvline(1.5,linestyle = '--', color='black')
cell.axvline(3.5,linestyle = '--', color='black')
cell.axvline(5.5,linestyle = '--', color='black')
cell.axhline(0,linestyle = '-', color='black')
    
cell.yaxis.set_major_formatter(formatter)
#cell.set_xticklabels([])
cell.set_ylim(-10,40)
#cell.set_xlim(-1,len(pref)-1)
cell.set_ylabel('Performance\nImprovement(%)')
#cell.grid(True, axis = 'y')

fig.text(0.23,0.1,"Skewed\nIndexing",fontsize=font_size)
fig.text(0.42,0.1,"Compression",fontsize=font_size)
fig.text(0.67,0.02,"Skewed\nIndexing +\nCompression",fontsize=font_size)

cell.set_xticks(ind)

x_label = ['MBTB\n- 4K', 'MBTB\n - 8K','MBTB\n- 4K', 'MBTB\n - 8K','MBTB\n - 4K','MBTB -\n8K','IDEAL\nBTB']
cell.set_xticklabels(x_label, rotation = 0)

def mformat(num):
    return "{0:.2f}".format(math.floor(num*100)/100)

for i in range(len(x_label)):
    if temp_df[i] < 0:
        cell.text(i-0.15,3,mformat(temp_df[i]),fontsize=font_size,rotation = 90)
    else:
        cell.text(i-0.15,temp_df[i]+3,mformat(temp_df[i]),fontsize=font_size,rotation = 90)

#cell.set_xlabel('\nL2BTB and L1I Prefetchers')
#fig.legend(loc = (0.85,0.75))
fig.tight_layout()
plt.subplots_adjust(bottom=0.4)
fig.savefig("with_without_skewed_indexing.pdf")
os.system("pdfcrop with_without_skewed_indexing.pdf")
plt.show()


