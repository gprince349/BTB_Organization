# file: variant_sensitivity.ipynb
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

trace_file="Champsim-Prefetcher-Thesis/scripts/micro_trace_list.txt"

micro_results_folder="Champsim-Prefetcher-Thesis/micro_sota_50M/"

before_pref="-hashed_perceptron-"
after_pref_cvp="-ipcp_isca-ipcp_isca-no-no-no-no-lru-lru-lru-srrip-drrip-lru-lru-lru-1core-cvp_trace.txt"

pref = ['mbtb_4k_2variants_2cycle','mbtb_4k','mbtb_4k_4variants']

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

params = {'legend.fontsize': 'x-large',
          'figure.figsize': (15, 5),
         'axes.labelsize': 'x-large',
         'axes.titlesize':'x-large',
         'xtick.labelsize':'x-large',
         'ytick.labelsize':'x-large'}
pylab.rcParams.update(params)

cache_configs=["512KB_2MB", "256KB_2.5MB", "1MB_1.375MB"]

#data.head()
#data.iat[2,2]

policy = ["Non Inclusive", "Seclusive"]
pdist = [-0.5,0.5]
width = 0.4

x_labels = ["SPEC 2017 traces", "Client traces", "Server traces", "CVP traces"]
colors = ["black", "white"]

fig, cells = plt.subplots(nrows = 1, ncols = 2,figsize=(10,3))

#-----------Perf------------------

cell = cells[0]

temp_df = []
for i in range(0,len(pref)):
    temp_df.append((server_df[pref[i]]-1)*100)
ind = np.arange(len(pref))

cell.bar(ind, temp_df,width,edgecolor='black',color='grey',label = 'BASELINE SYSTEM')

#cell.axvline(2.5,linestyle = '--', color='black')
    
cell.yaxis.set_major_formatter(formatter)
#cell.set_xticklabels([])
cell.set_ylim(0,25)
#cell.set_xlim(-1,len(pref)-1)
cell.set_ylabel('Performance\nImprovement(%)')
#cell.grid(True, axis = 'y')

cell.set_xticks(ind)

x_label = ['MBTB-4K\n2 variants', 'MBTB-4K\n3 variants','MBTB-4K\n4 variants']
cell.set_xticklabels(x_label, rotation = 0)

def mformat(num):
    return "{0:.2f}".format(math.floor(num*100)/100)

for i in range(len(x_label)):
    cell.text(i-0.21,temp_df[i]+1,mformat(temp_df[i]),fontsize='x-large',rotation = 0)

    
#---------Number of Evictions-----------    

cell = cells[1]

temp_df = [29153, 32102, 98914]
ind = np.arange(len(temp_df))

cell.bar(ind, temp_df,width,edgecolor='black',color='grey',label = 'BASELINE SYSTEM')
    
cell.yaxis.set_major_formatter(formatter)
#cell.set_xticklabels([])
cell.set_ylim(0,125000)
#cell.set_xlim(-1,3)
cell.set_ylabel('Number of\nEvictions')
#cell.grid(True, axis = 'y')

cell.set_xticks(ind)

x_label = ['MBTB-4K\n2 variants', 'MBTB-4K\n3 variants','MBTB-4K\n4 variants']
cell.set_xticklabels(x_label, rotation = 0)

for i in range(len(x_label)):
    cell.text(i-0.21,temp_df[i]+5000,temp_df[i],fontsize='x-large',rotation = 0)

fig.text(0.13,0.02,"(a) Performance Improvement",fontsize='x-large')
fig.text(0.68,0.02,"(b) Number of Evictions",fontsize='x-large')
    
#cell.set_xlabel('\nL2BTB and L1I Prefetchers')
#fig.legend(loc = (0.85,0.75))
fig.tight_layout()
plt.subplots_adjust(bottom=0.3)
fig.savefig("variant_sensitivity.pdf")
os.system("pdfcrop variant_sensitivity.pdf")
plt.show()

