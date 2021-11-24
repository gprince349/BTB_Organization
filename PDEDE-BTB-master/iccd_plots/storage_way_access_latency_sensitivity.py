# file: storage_way_access_latency_sensitivity.ipynb
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
#----------------------------Storage------------------------

import re
from scipy.stats.mstats import gmean
import pandas as pd

trace_file="Champsim-Prefetcher-Thesis/scripts/micro_trace_list.txt"

micro_results_folder="Champsim-Prefetcher-Thesis/micro_sota_50M/"

before_pref="-hashed_perceptron-"
after_pref_cvp="-ipcp_isca-ipcp_isca-no-no-no-no-lru-lru-lru-srrip-drrip-lru-lru-lru-1core-cvp_trace.txt"

pref_storage = ['mbtb_2k_2variants','mbtb_3k_2variants','mbtb_4k_2variants_2cycle','mbtb_6k_2variants'\
        ,'mbtb_8k_2variants_2cycle','perfect_btb']

server = []

for i in range(len(pref_storage)):
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
    for i in range(len(pref_storage)):
        curr_ipc = get_ipc(micro_results_folder+line.strip()+before_pref+pref_storage[i]+after_pref_cvp)
        if curr_ipc == 0:
            continue
        server[i].append(curr_ipc/base_ipc)
        
server_df_storage = {}
for i in range(len(server)):
    server_df_storage[pref_storage[i]] = gmean(server[i])

print(server_df_storage)


# -------- code --------
#----------------------------Way------------------------

import re
from scipy.stats.mstats import gmean
import pandas as pd

trace_file="Champsim-Prefetcher-Thesis/scripts/micro_trace_list.txt"

micro_results_folder="Champsim-Prefetcher-Thesis/micro_sota_50M/"

before_pref="-hashed_perceptron-"
after_pref_cvp="-ipcp_isca-ipcp_isca-no-no-no-no-lru-lru-lru-srrip-drrip-lru-lru-lru-1core-cvp_trace.txt"

pref_way = ['mbtb_4k_2way_2variants_2cycle','mbtb_4k_2variants_2cycle','mbtb_4k_8way_2variants_2cycle',\
        'mbtb_4k_16way_2variants_2cycle','perfect_btb']

server = []

for i in range(len(pref_way)):
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
    for i in range(len(pref_way)):
        curr_ipc = get_ipc(micro_results_folder+line.strip()+before_pref+pref_way[i]+after_pref_cvp)
        if curr_ipc == 0:
            continue
        server[i].append(curr_ipc/base_ipc)
        
server_df_way = {}
for i in range(len(server)):
    server_df_way[pref_way[i]] = gmean(server[i])

print(server_df_way)


# -------- code --------
#----------------------------Latency------------------------

import re
from scipy.stats.mstats import gmean
import pandas as pd

trace_file="Champsim-Prefetcher-Thesis/scripts/micro_trace_list.txt"

micro_results_folder="Champsim-Prefetcher-Thesis/micro_sota_50M/"

before_pref="-hashed_perceptron-"
after_pref_cvp="-ipcp_isca-ipcp_isca-no-no-no-no-lru-lru-lru-srrip-drrip-lru-lru-lru-1core-cvp_trace.txt"

pref_latency = ['mbtb_4k_2variants_1cycle','mbtb_4k_2variants_2cycle','mbtb_4k_2variants_3cycle',\
        'mbtb_4k_2variants_4cycle','mbtb_4k_2variants_5cycle','perfect_btb']

server = []

for i in range(len(pref_latency)):
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
    for i in range(len(pref_latency)):
        curr_ipc = get_ipc(micro_results_folder+line.strip()+before_pref+pref_latency[i]+after_pref_cvp)
        if curr_ipc == 0:
            continue
        server[i].append(curr_ipc/base_ipc)
        
server_df_latency = {}
for i in range(len(server)):
    server_df_latency[pref_latency[i]] = gmean(server[i])

print(server_df_latency)

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

font_size = 15
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

fig, cells = plt.subplots(nrows = 1, ncols = 3,figsize=(15,4),sharey=True)
#----------------------------Storage------------------------

cell = cells[0]

temp_df = []
for i in range(0,len(pref_storage)):
    temp_df.append((server_df_storage[pref_storage[i]]-1)*100)
ind = np.arange(len(pref_storage))

cell.bar(ind, temp_df,width,edgecolor='black',color='lightgrey',label = 'BASELINE SYSTEM')

cell.axhline(0,linestyle = '-', color='black')
    
cell.yaxis.set_major_formatter(formatter)
cell.set_ylim(-25,30)
cell.set_ylabel('Performance\nImprovement(%)')

cell.set_xticks(ind)

x_label = ['MBTB\n- 2K','MBTB\n- 3K','MBTB\n- 4K', 'MBTB\n - 6K','MBTB\n - 8K','IDEAL\nBTB']
cell.set_xticklabels(x_label, rotation = 90)

def mformat(num):
    return "{0:.2f}".format(math.floor(num*100)/100)

for i in range(len(x_label)):
    if temp_df[i] < 0:
        cell.text(i-0.15,1.8,mformat(temp_df[i]),fontsize=font_size,rotation = 90)
    else:
        cell.text(i-0.15,temp_df[i]+1.8,mformat(temp_df[i]),fontsize=font_size,rotation = 90)

bb = mtransforms.Bbox([[1.85, 0], [2.15, 28]])

p_fancy = FancyBboxPatch((bb.xmin, bb.ymin),
                         abs(bb.width), abs(bb.height),
                         boxstyle="round,pad=0.18",
                         fc="none",
                         ec="black")

cell.add_patch(p_fancy)    

#----------------------------Way------------------------        
        
cell = cells[1]

temp_df = []
for i in range(0,len(pref_way)):
    temp_df.append((server_df_way[pref_way[i]]-1)*100)
ind = np.arange(len(pref_way))

cell.bar(ind, temp_df,width,edgecolor='black',color='lightgrey',label = 'BASELINE SYSTEM')

cell.yaxis.set_major_formatter(formatter)
cell.set_ylim(0,30)
cell.axhline(0,linestyle = '-', color='black')
cell.set_xticks(ind)

x_label = ['MBTB-4K\n2 way', 'MBTB-4K\n4 way','MBTB-4K\n8 way','MBTB-4K\n16 way','IDEAL\nBTB']
cell.set_xticklabels(x_label, rotation = 90)

def mformat(num):
    return "{0:.2f}".format(math.floor(num*100)/100)

for i in range(len(x_label)):
    if i == 0:
        cell.text(i-0.1,temp_df[i]+1.8,mformat(temp_df[i]),fontsize=font_size,rotation = 90)
    else:
        cell.text(i-0.1,temp_df[i]+1.8,mformat(temp_df[i]),fontsize=font_size,rotation = 90)

bb = mtransforms.Bbox([[0.85, 0], [1.15, 28]])

p_fancy = FancyBboxPatch((bb.xmin, bb.ymin),
                         abs(bb.width), abs(bb.height),
                         boxstyle="round,pad=0.18",
                         fc="none",
                         ec="black")

cell.add_patch(p_fancy)    
        
#----------------------------Latency------------------------


cell = cells[2]

temp_df = []
for i in range(0,len(pref_latency)):
    temp_df.append((server_df_latency[pref_latency[i]]-1)*100)
ind = np.arange(len(pref_latency))

cell.bar(ind, temp_df,width,edgecolor='black',color='lightgrey')

cell.yaxis.set_major_formatter(formatter)
cell.set_ylim(-5,30)
cell.axhline(0,linestyle = '-', color='black')
cell.set_xticks(ind)

x_label = ['MBTB-4K\n1 cycle','MBTB-4K\n2 cycle', 'MBTB-4K\n3 cycle','MBTB-4K\n4 cycle','MBTB-4K\n5 cycle','IDEAL\nBTB']
cell.set_xticklabels(x_label, rotation = 90)

def mformat(num):
    return "{0:.2f}".format(math.floor(num*100)/100)

for i in range(len(x_label)):
    cell.text(i-0.15,temp_df[i]+1.8,mformat(temp_df[i]),fontsize=font_size,rotation = 90)

bb = mtransforms.Bbox([[0.85, 0], [1.15, 28]])

p_fancy = FancyBboxPatch((bb.xmin, bb.ymin),
                         abs(bb.width), abs(bb.height),
                         boxstyle="round,pad=0.18",
                         fc="none",
                         ec="black")

cell.add_patch(p_fancy)        
        
fig.text(0.2,0.02,"(a)",fontsize=font_size,rotation = 0)
fig.text(0.55,0.02,"(b)",fontsize=font_size,rotation = 0)
fig.text(0.83,0.02,"(c)",fontsize=font_size,rotation = 0)
        
fig.tight_layout()
plt.subplots_adjust(bottom=0.35)
fig.savefig("storage_way_access_latency_sensitivity.pdf")
plt.show()


