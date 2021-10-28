# file: Sota_MPKI_SCKI_Perf.ipynb
# vi: filetype=python

# -------- code --------
from matplotlib.ticker import FuncFormatter

def my_formatter(x, pos):
    if x.is_integer():
        return "%d " % abs(int(x))
    else:
        return "{0:.1f} ".format(abs(x))
    
def my_formatter1(x, pos):
    return ""

formatter = FuncFormatter(my_formatter)
formatter1 = FuncFormatter(my_formatter1)

# -------- code --------
#----------------------------PERF------------------------

import re
from scipy.stats.mstats import gmean
import pandas as pd

trace_file="Champsim-Prefetcher-Thesis/scripts/micro_trace_list.txt"

micro_results_folder="Champsim-Prefetcher-Thesis/micro_sota_50M/"

before_pref="-hashed_perceptron-"
after_pref_cvp="-ipcp_isca-ipcp_isca-no-no-no-no-lru-lru-lru-srrip-drrip-lru-lru-lru-1core-cvp_trace.txt"

pref_perf = ['shotgun','div_conq','csbtb_8k','fdipx_8k','mbtb_4k_2variants_2cycle','mbtb_8k_2variants_2cycle',\
        'perfect_btb']

server = []

for i in range(len(pref_perf)):
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
    for i in range(len(pref_perf)):
        curr_ipc = get_ipc(micro_results_folder+line.strip()+before_pref+pref_perf[i]+after_pref_cvp)
        if curr_ipc == 0:
            continue
        server[i].append(curr_ipc/base_ipc)

server_df = {}
for i in range(len(server)):
    server_df[pref_perf[i]] = gmean(server[i])

print(server_df)


# -------- code --------
#----------------------------MPKI------------------------

import re

trace_file="Champsim-Prefetcher-Thesis/scripts/micro_trace_list.txt"

micro_results_folder="Champsim-Prefetcher-Thesis/micro_sota_50M/"

before_pref="-hashed_perceptron-"
after_pref_cvp="-ipcp_isca-ipcp_isca-no-no-no-no-lru-lru-lru-srrip-drrip-lru-lru-lru-1core-cvp_trace.txt"

server_total_mpki = []
server_count = 0

pref_mpki = ['baseline','shotgun','div_conq','csbtb_8k','fdipx_8k','mbtb_4k_2variants_2cycle',\
        'mbtb_8k_2variants_2cycle']

for i in range(1):
    temp = []
    for j in range(len(pref_mpki)):
        temp.append(0)
    server_total_mpki.append(temp)

def get_mpki(filename,search_param):
    temp = [0]
    temp_file = open(filename)
    for line1 in temp_file:
        if re.search(search_param, line1):
            temp[0] = float(line1.split(" ")[-1].strip())
    return temp
    
trace_file_ptr = open(trace_file, "r")
for line in trace_file_ptr:
    for i in range(len(pref_mpki)):
        if pref_mpki[i] == 'fdipx_8k':
            search_param = 'L2BTB1 TOTAL     ACCESS:'
        else:
            search_param = "BTB TOTAL     ACCESS:"
        mpki_val = get_mpki(micro_results_folder+line.strip()+before_pref+pref_mpki[i]+after_pref_cvp,search_param)
        for j in range(len(mpki_val)):
            server_total_mpki[j][i] += mpki_val[j]
    server_count = server_count + 1
    
for i in range(1):
    for j in range(len(pref_mpki)):
        server_total_mpki[i][j] /= server_count

print(server_total_mpki)


# -------- code --------
#----------------------------SCKI------------------------

import re

trace_file="Champsim-Prefetcher-Thesis/scripts/micro_trace_list.txt"

micro_results_folder="Champsim-Prefetcher-Thesis/micro_sota_50M/"

before_pref="-hashed_perceptron-"
after_pref_cvp="-ipcp_isca-ipcp_isca-no-no-no-no-lru-lru-lru-srrip-drrip-lru-lru-lru-1core-cvp_trace.txt"

server_total_scki = []
server_count = 0

pref = ['baseline','shotgun','div_conq','csbtb_8k','fdipx_8k','mbtb_4k_2variants_2cycle',\
        'mbtb_8k_2variants_2cycle','perfect_btb']

for i in range(1):
    temp = []
    for j in range(len(pref)):
        temp.append(0)
    server_total_scki.append(temp)

def get_mpki(filename,search_param):
    temp = [0]
    temp_file = open(filename)
    for line1 in temp_file:
        if re.search(search_param, line1):
            temp[0] = float(line1.split(" ")[-1].strip())
    return temp
    
trace_file_ptr = open(trace_file, "r")
for line in trace_file_ptr:
    for i in range(len(pref)):
        search_param = "Starvation_cycles_per_kilo_instr_0:"
        scki_val = get_mpki(micro_results_folder+line.strip()+before_pref+pref[i]+after_pref_cvp,search_param)
        for j in range(len(scki_val)):
            server_total_scki[j][i] += scki_val[j]
    server_count = server_count + 1
    
for i in range(1):
    for j in range(len(pref)):
        server_total_scki[i][j] /= server_count

print(server_total_scki)


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

font_size=14

params = {'legend.fontsize': font_size,
          'figure.figsize': (15, 5),
         'axes.labelsize': font_size,
         'axes.titlesize':font_size,
         'xtick.labelsize':font_size,
         'ytick.labelsize':font_size}
pylab.rcParams.update(params)

width = 0.4

x_labels = ["SPEC 2017 traces", "Client traces", "Server traces", "CVP traces"]
colors = ["black", "white"]

fig, cells = plt.subplots(nrows = 1, ncols = 3,figsize=(15,3))



#----------------------------PERF------------------------



cell = cells[2]

temp_df = []
for i in range(0,len(pref_perf)):
    temp_df.append((server_df[pref_perf[i]]-1)*100)
ind = np.arange(len(pref_perf))

cell.bar(ind, temp_df,width,edgecolor='black',color='lightgrey',label = 'BASELINE SYSTEM')

# cell.axvline(3.5,linestyle = '--', color='black')
# cell.axvline(5.5,linestyle = '--', color='black')
cell.axhline(0,linestyle = '-', color='black')
    
cell.yaxis.set_major_formatter(formatter)
#cell.set_xticklabels([])
cell.set_ylim(-3,40)
#cell.set_xlim(-1,len(pref)-1)
cell.set_ylabel('Performance\nImprovement(%)')
#cell.grid(True, axis = 'y')

#fig.text(0.25,0.02,"4K entry BTB",fontsize='x-large')
#fig.text(0.62,0.02,"8K entry BTB",fontsize='x-large')

cell.set_xticks(ind)

x_label = ['SHOTGUN\n- 8K', 'SN4L+DIS+\nBTB - 8K','SKEWED\nBTB - 8K','FDIPX - 8K',\
           'MBTB - 4K', 'MBTB - 8K','IDEAL BTB']
cell.set_xticklabels(x_label, rotation = 90)

def mformat(num):
    return "{0:.2f}".format(math.floor(num*100)/100)

for i in range(len(x_label)):
    if temp_df[i] <= 0:
        cell.text(i-0.15,3,mformat(temp_df[i]),fontsize=font_size,rotation = 90)
    else:
        cell.text(i-0.15,temp_df[i]+3,mformat(temp_df[i]),fontsize=font_size,rotation = 90)

bb = mtransforms.Bbox([[3.85, 0], [4.15, 37]])

p_fancy = FancyBboxPatch((bb.xmin, bb.ymin),
                         abs(bb.width), abs(bb.height),
                         boxstyle="round,pad=0.18",
                         fc="none",
                         ec="black")

cell.add_patch(p_fancy)

        

#----------------------------MPKI------------------------
        

ind = np.arange(len(pref_mpki))
cell = cells[0]

temp_df = []
for i in range(0,len(pref_mpki)):
    temp_df.append(server_total_mpki[0][i])
ind = np.arange(len(pref_mpki))

cell.bar(ind, temp_df ,width,edgecolor='black',color="lightgrey")


def mformat(num):
    return "{0:.2f}".format(num)
    

x_label = ['BASELINE','SHOTGUN\n- 8K', 'SN4L+DIS+\nBTB - 8K','SKEWED\nBTB - 8K','FDIPX - 8K','MBTB - 4K'\
           , 'MBTB - 8K']

# cell.axvline(0.5,linestyle = '--', color='black')
# cell.axvline(4.5,linestyle = '--', color='black')

for i in range(len(x_label)):
    cell.text(i-0.15,temp_df[i]+1.5,mformat(temp_df[i]),fontsize=font_size,rotation = 90)


#cell.set_xlim(-0.5,3.5)
cell.set_ylim(0,20)
cell.set_xticks(ind)
cell.set_xticklabels(x_label, rotation = 90)
cell.set_ylabel('L2BTB MPKI')

bb = mtransforms.Bbox([[4.85, 0], [5.15, 9]])

p_fancy = FancyBboxPatch((bb.xmin, bb.ymin),
                         abs(bb.width), abs(bb.height),
                         boxstyle="round,pad=0.18",
                         fc="none",
                         ec="black")

cell.add_patch(p_fancy)

#----------------------------SCKI------------------------        

cell = cells[1]

temp_df = []
for i in range(0,len(pref)):
    temp_df.append(server_total_scki[0][i])
ind = np.arange(len(pref))

cell.bar(ind, temp_df ,width,edgecolor='black',color="lightgrey")


def mformat(num):
    return "{0:.2f}".format(num)
    

x_label = ['BASELINE','SHOTGUN\n- 8K', 'SN4L+DIS+\nBTB - 8K','SKEWED\nBTB - 8K','FDIPX - 8K',
           'MBTB - 4K', 'MBTB - 8K','IDEAL BTB']

# cell.axvline(0.5,linestyle = '--', color='grey')
# cell.axvline(4.5,linestyle = '--', color='grey')
# cell.axvline(6.5,linestyle = '--', color='grey')

for i in range(len(x_label)):
    cell.text(i-0.15,temp_df[i]+40,mformat(temp_df[i]),fontsize=font_size,rotation = 90)


#cell.set_xlim(-0.5,3.5)
cell.set_ylim(0,650)
cell.set_xticks(ind)
cell.set_xticklabels(x_label, rotation = 90)
cell.set_ylabel('L2BTB MPKI')
cell.set_ylabel('Starvation Cycles\nPer Kilo\nInstructions')

bb = mtransforms.Bbox([[4.85, 0], [5.15, 500]])

p_fancy = FancyBboxPatch((bb.xmin, bb.ymin),
                         abs(bb.width), abs(bb.height),
                         boxstyle="round,pad=0.18",
                         fc="none",
                         ec="black")

cell.add_patch(p_fancy)

fig.text(0.18,0.01,"(a)",fontsize=font_size,rotation = 0)
fig.text(0.52,0.01,"(b)",fontsize=font_size,rotation = 0)
fig.text(0.85,0.01,"(c)",fontsize=font_size,rotation = 0)

fig.tight_layout()
#plt.subplots_adjust(bottom=0.2)
fig.savefig("sota_perf_mpki_scki.pdf")
plt.show()

