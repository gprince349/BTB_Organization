# file: Branch_Offset_Variation.ipynb
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

trace_file="../Champsim-Prefetcher-Thesis/scripts/micro_trace_list.txt"

micro_results_folder="../Champsim-Prefetcher-Thesis/micro_sota_50M/"

before_pref="-hashed_perceptron-"
after_pref_cvp="-ipcp_isca-ipcp_isca-no-no-no-no-lru-lru-lru-srrip-drrip-lru-lru-lru-1core-cvp_trace.txt"

total_offset_freq = [[0 for i in range(65)] for j in range(6)]
bottom_val = [[0 for i in range(65)] for j in range(6)]
trace_cnt = 0
    
trace_file_ptr = open(trace_file, "r")
for line in trace_file_ptr:
    total = 0
    for i in range(1,7,1):
        temp_file = open(micro_results_folder+line.strip()+before_pref+'baseline'+after_pref_cvp)
        for line1 in temp_file:
            if re.search("Branch_type_"+str(i)+" ", line1):
                for j in range(65):
                    m = re.search('\('+str(j)+',\d+',line1)
                    if m:
                        total_offset_freq[i-1][j] += int(m.group(0).split(",")[-1])
                break
    trace_cnt += 1

for i in range(6):
    for j in range(65):
        total_offset_freq[i][j] /= trace_cnt
    if i == 0:
        continue
    for j in range(0,i,1):
        for k in range(65):
            bottom_val[i][k] += total_offset_freq[j][k]
                
print(total_offset_freq)
print(bottom_val)
                
#                 curr_val[i] = int(line1.split(" ")[-1].strip())
#                 total += curr_val[i]
#                 break
#     for i in range(65):
#         curr_val[i] = curr_val[i] / total * 100
#         total_offset_freq[i] += curr_val[i]
#     trace_cnt += 1

# for i in range(65):
#     total_offset_freq[i] = total_offset_freq[i] / trace_cnt
    
# print(total_offset_freq)

# -------- code --------
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter
from scipy.stats.mstats import gmean
import os
import math

import matplotlib.pylab as pylab

font_size = 30

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
width = 0.35

x_labels = ["IDEAL\nBTB", "IDEAL\nL1I","IDEAL\nFRONT-END"]
colors = ["black", "white"]

fig, cells = plt.subplots(nrows = 1, ncols = 1,figsize=(20,5),sharex=True)

ind = np.arange(len(total_offset_freq[0]))

width = 0.7

cell = cells

dist = [-width,0,width]
colors = ['white','black','lightgrey','lightgrey','white','grey']
hatches_df = ['/o','ooo','xxx','\\\\','**','']

for i in range(6):
    cell.bar(ind, total_offset_freq[i],width,bottom=bottom_val[i],edgecolor='black',color=colors[i],hatch=hatches_df[i])

def mformat(num):
    return "{0:.2f}".format(math.floor(num*100)/100)

# #fig.text(0.21,0.2,"{0:.2f}".format(client[0]),fontsize='x-large')
# fig.text(0.3,0.72,mformat(micro_traces[0]),fontsize='x-large')

# #fig.text(0.31,0.24,"{0:.2f}".format(client[1]),fontsize='x-large')
# fig.text(0.54,0.6,mformat(micro_traces[1]),fontsize='x-large')

# #fig.text(0.4,0.24,"{0:.2f}".format(client[2]),fontsize='x-large')
# fig.text(0.78,0.78,mformat(micro_traces[2]),fontsize='x-large')

cell.set_xticks(ind)
cell.set_xlim(1, 48)
cell.set_yscale('log')
cell.set_ylim(1,10000)
cell.yaxis.set_major_formatter(formatter)

x_labels=[]
for i in range(len(total_offset_freq[0])):
    if i % 2 == 1:
        x_labels.append(str(i))
    else:
        x_labels.append("")

cell.set_xticklabels(x_labels)
cell.set_ylabel('Frequency of\noccurence')
cell.set_xlabel('Bits for encoding branch target offset')

policy = ['Direct Branch', 'Indirect Branch', 'Conditional Branch', 'Direct Call', 'Indirect Call','Return']
fig.legend(policy,loc='upper center',ncol=3)
fig.tight_layout()
plt.subplots_adjust(top=0.68)
fig.savefig("offset_freq.pdf")
os.system("pdfcrop offset_freq.pdf")
plt.show()


