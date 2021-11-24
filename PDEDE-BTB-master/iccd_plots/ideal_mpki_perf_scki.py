# file: ideal_mpki_perf_scki.ipynb
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
import re

trace_file="Champsim-Prefetcher-Thesis/scripts/micro_trace_list.txt"

micro_results_folder="Champsim-Prefetcher-Thesis/micro_sota_50M/"

before_pref="-hashed_perceptron-"
after_pref_cvp="-ipcp_isca-ipcp_isca-no-no-no-no-lru-lru-lru-srrip-drrip-lru-lru-lru-1core-cvp_trace.txt"

server_total_mpki = []
server_count = 0

pref_mpki = ['btb_4k','baseline','btb_16k','btb_32k']

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
import re
import os.path
from scipy.stats.mstats import gmean

trace_file="Champsim-Prefetcher-Thesis/scripts/micro_trace_list.txt"

micro_results_folder="Champsim-Prefetcher-Thesis/micro_sota_50M/"

before_pref="-hashed_perceptron-"
after_pref="-ipcp_isca-ipcp_isca-no-no-no-no-lru-lru-lru-srrip-drrip-lru-lru-lru-1core-cvp_trace.txt"

pref_perf = ['perfect_btb','perfect_l1i','perfect_btb_l1i']

micro_traces = [[],[],[]]

def get_ipc(file_name):
    temp_file = open(file_name)
    for line1 in temp_file:
        if re.search("CPU 0 cumulative IPC:", line1):
            return float(line1.split(" ")[4].strip())
    return 0.0

trace_file_ptr = open(trace_file, "r")
for line in trace_file_ptr:
    base_ipc = get_ipc(micro_results_folder+line.strip()+before_pref+"baseline"+after_pref)
    for i in range(len(pref_perf)):
        curr_ipc = get_ipc(micro_results_folder+line.strip()+before_pref+pref_perf[i]+after_pref)
        micro_traces[i].append(curr_ipc/base_ipc)
    
for i in range(len(pref_perf)):
    micro_traces[i] = gmean(micro_traces[i])
    micro_traces[i] = (micro_traces[i]-1)*100
    
print(micro_traces)

# -------- code --------
import re

trace_file="Champsim-Prefetcher-Thesis/scripts/micro_trace_list.txt"

micro_results_folder="Champsim-Prefetcher-Thesis/micro_sota_50M/"

before_pref="-hashed_perceptron-"
after_pref_cvp="-ipcp_isca-ipcp_isca-no-no-no-no-lru-lru-lru-srrip-drrip-lru-lru-lru-1core-cvp_trace.txt"

server_total_scki = []
server_count = 0

pref_scki = ['baseline','perfect_btb','perfect_l1i','perfect_btb_l1i']

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
    for i in range(len(pref_scki)):
        search_param = "Starvation_cycles_per_kilo_instr_0:"
        mpki_val = get_mpki(micro_results_folder+line.strip()+before_pref+pref_scki[i]+after_pref_cvp,search_param)
        for j in range(len(mpki_val)):
            server_total_scki[j][i] += mpki_val[j]
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
import math
import os

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
width = 0.35

x_labels = ["4K","8K", "16K","32K"]
colors = ["black", "white"]

fig, cells = plt.subplots(nrows = 1, ncols = 2,figsize=(7.5,3))


ind = np.arange(4)

width = 0.4

cell = cells[0]

shift = [-1.5*width, -0.5*width , 0.5*width, 1.5*width]

color = ['white','lightgrey','grey','black']

#cell.bar(ind, [server_total_mpki[0][0],server_total_mpki[0][1],server_total_mpki[0][2],server_total_mpki[0][3],server_total_mpki[0][4]] ,width,edgecolor='black',color="grey")
cell.bar(ind, [server_total_mpki[0][0],server_total_mpki[0][1],server_total_mpki[0][2],server_total_mpki[0][3]] ,width,edgecolor='black',color="lightgrey")


def mformat(num):
    return "{0:.2f}".format(math.floor(num*100)/100)

cell.set_xlim(-0.5,3.5)
cell.set_ylim(0,45)
cell.set_xticks(ind)
cell.set_xticklabels(x_labels)
cell.set_ylabel('L2BTB MPKI')

for i in range(4):
    cell.text(ind[i]-0.15,server_total_mpki[0][i]+2,mformat(server_total_mpki[0][i]),fontsize='x-large',rotation = 90)



# x_labels = ["IDEAL\nBTB", "IDEAL\nL1I","IDEAL\nFRONT-END"]
# ind = np.arange(len(x_labels))

# width = 0.25

# cell = cells[1]

# dist = [-width,0,width]
# color = ['white','lightgrey','grey']
# #for i in range(len(pref)):
# cell.bar(ind, [micro_traces[0],micro_traces[1],micro_traces[2]],width,edgecolor='black',color=color[1])

# def mformat(num):
#     return "{0:.2f}".format(math.floor(num*100)/100)

# def mformat1(num):
#     return "{0:.1f}".format(math.floor(num*100)/100)

# for i in range(3):
#     cell.text(ind[i]-0.2,micro_traces[i]+1,mformat(micro_traces[i]),fontsize='x-large',rotation = 0)

# cell.set_xticks(ind)
# cell.set_ylim(0,30)
# cell.yaxis.set_major_formatter(formatter)
# cell.set_xticklabels(x_labels)
# cell.set_ylabel('Performance\nImprovement(%)')


x_labels = ["BASE-\nLINE","IDEAL\nBTB", "IDEAL\nL1I","IDEAL\nFRONT-\nEND"]
ind = np.arange(4)

width = 0.4

cell = cells[1]

shift = [-1.5*width, -0.5*width , 0.5*width, 1.5*width]

color = ['white','lightgrey','grey','black']

#cell.bar(ind, [server_total_mpki[0][0],server_total_mpki[0][1],server_total_mpki[0][2],server_total_mpki[0][3],server_total_mpki[0][4]] ,width,edgecolor='black',color="grey")
cell.bar(ind, [server_total_scki[0][0],server_total_scki[0][1],server_total_scki[0][2],server_total_scki[0][3]] ,width,edgecolor='black',color="lightgrey")


def mformat(num):
    return "{0:.2f}".format(math.floor(num*100)/100)
    
for i in range(4):
    cell.text(ind[i]-0.15,server_total_scki[0][i]+20,mformat(server_total_scki[0][i]),fontsize='x-large',rotation = 90)
# cell.text(0.25,0.75,mformat(server_total_scki[0][0]),fontsize='x-large')
# cell.text(0.43,0.44,mformat(server_total_scki[0][1]),fontsize='x-large')
# cell.text(0.62,0.58,mformat(server_total_scki[0][2]),fontsize='x-large')
# cell.text(0.81,0.37,mformat(server_total_scki[0][3]),fontsize='x-large')
#fig.text(0.83,0.25,mformat(server_total_mpki[0][4]),fontsize='x-large')

cell.set_xlim(-0.5,3.5)
cell.set_ylim(0,470)
cell.set_xticks(ind)
cell.set_xticklabels(x_labels, rotation = 90)
cell.set_ylabel('Starvation Cycles\nPer Kilo Instructions')

fig.text(0.25,0.02,"(a)",fontsize='x-large',rotation = 0)
fig.text(0.77,0.02,"(b)",fontsize='x-large',rotation = 0)
#fig.text(0.85,0.02,"(c)",fontsize='x-large',rotation = 0)

policy = ['4K', '8K', '16K','32K']
#fig.legend(policy,loc='upper center',ncol=4)
fig.tight_layout()
#plt.subplots_adjust(top=0.8)
fig.savefig("ideal_mpki_perf_scki.pdf")
plt.show()


