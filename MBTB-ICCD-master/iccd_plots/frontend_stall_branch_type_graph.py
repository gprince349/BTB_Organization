# file: frontend_stall_branch_type_graph.ipynb
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
import math
import statistics

trace_file="../Champsim-Prefetcher-Thesis/scripts/micro_trace_list.txt"

micro_results_folder="../Champsim-Prefetcher-Thesis/micro_sota_50M/"

configs = ['baseline','baseline_lowconfig']
before_cvp_trace="-hashed_perceptron-"
after_cvp_trace="-ipcp_isca-ipcp_isca-no-no-no-no-lru-lru-lru-srrip-drrip-lru-lru-lru-1core-cvp_trace.txt"

branch_type = ['DIRECT_JUMP', 'DIRECT_CALL', 'CONDITIONAL', 'INDIRECT_CALL', 'INDIRECT', 'RETURN']

split_param = ' '

def get_frontend_stall(filename,search_param):
    temp_file = open(filename, 'r')
    stall = [0] * 6
    for line in temp_file:
        for i in range(len(branch_type)):
            if re.search('L2BTB BRANCH_'+branch_type[i], line):
                old_line = line
                line = line[line.find(search_param)+len(search_param):].split(split_param)[0]
                stall[i] = float(line.strip())
                #print(old_line, branch_type[i],stall[i])
                if math.isnan(stall[i]):
                    stall[i] = 0
                break
    return stall

total_stall = {}

stall_name = ["fetch","fetch_queue","decode","decode_queue","execute"]

for config in configs:
    total_stall[config] = {}
    for name in stall_name:
        temp = []
        for i in range(6):
            temp.append([])
        total_stall[config][name] = temp
    
def filter_stall(num):
    return 0 if (num > 1000 or num < 0 ) else num
        
split_params = {'baseline':' ','baseline_lowconfig':' '}
for config in configs:
    split_param = split_params[config]
    trace_file_ptr = open(trace_file, "r")
    for line in trace_file_ptr:
        fetch_stall = get_frontend_stall(micro_results_folder+line.strip()+before_cvp_trace+config+after_cvp_trace,"AVERAGE FETCH STALL: ")
        fetch_queue_stall = get_frontend_stall(micro_results_folder+line.strip()+before_cvp_trace+config+after_cvp_trace,"AVERAGE FETCH QUEUE STALL: ")
        decode_stall = get_frontend_stall(micro_results_folder+line.strip()+before_cvp_trace+config+after_cvp_trace,"AVERAGE DECODE STALL: ")
        execute_stall = get_frontend_stall(micro_results_folder+line.strip()+before_cvp_trace+config+after_cvp_trace,"AVERAGE EXECUTE STALL: ")
        for i in range(6):
            total_stall[config][stall_name[0]][i].append(filter_stall(fetch_stall[i]))
            total_stall[config][stall_name[1]][i].append(filter_stall(fetch_queue_stall[i]))
            total_stall[config][stall_name[2]][i].append(filter_stall(4))
            total_stall[config][stall_name[3]][i].append(filter_stall(decode_stall[i]-4))
            total_stall[config][stall_name[4]][i].append(filter_stall(execute_stall[i]))
    print(config)

dict_total_stall = {}

for config in configs:
    dict_total_stall[config] = {}
    for name in stall_name:
        temp = [0 for j in range(6)]
        for i in range(6):
            temp[i] = statistics.mean(total_stall[config][name][i])
        dict_total_stall[config][name] = temp
    
print(dict_total_stall)

top_val = {}
for config in configs:
    temp1 = []
    for i in range(0,len(stall_name)):
        temp = [0 for j in range(6)]
        for j in range(0,i):
            for k in range(6):
                temp[k] += dict_total_stall[config][stall_name[j]][k]
        temp1.append(temp)
    top_val[config]=temp1

print(top_val)

# -------- code --------
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter
from scipy.stats.mstats import gmean
import os

import matplotlib.pylab as pylab

font_size = 18

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

branch_type = ['DIRECT_JUMP', 'INDIRECT_CALL', 'CONDITIONAL', 'INDIRECT_CALL','INDIRECT', 'RETURN']



x_labels = ['DIRECT\nJUMP', 'DIRECT\nCALL', 'CONDITIONAL', 'INDIRECT\nJUMP','INDIRECT\nCALL', 'RETURN']
colors = ["black", "white"]

fig, cells = plt.subplots(nrows = 1, ncols = 1,figsize=(15,4),sharex=True)


ind = np.arange(6)
cell = cells

width = 0.4

shift = [-0.2,0.2]

label_df = ['FETCH STAGE', 'FETCH QUEUE', 'DECODE STAGE', 'DECODE QUEUE','EXECUTE STAGE']
colors = ['white','lightgrey','white','grey','white']
hatches_df = ['/o','oo','xx','','*']

for i in range(len(x_labels)):
    x_labels[i] = 'A     B\n\n'+x_labels[i]

for i in range(len(stall_name)):
    for j in range(len(configs)):
        if j == 0:
            cell.bar(ind+shift[j],dict_total_stall[configs[j]][stall_name[i]],width,\
                     bottom=top_val[configs[j]][i],edgecolor='black',color=colors[i],label=label_df[i],hatch=hatches_df[i])
        else:
            cell.bar(ind+shift[j],dict_total_stall[configs[j]][stall_name[i]],width,\
                     bottom=top_val[configs[j]][i],edgecolor='black',color=colors[i],hatch=hatches_df[i])
    
cell.yaxis.set_major_formatter(formatter)
cell.set_xticks(ind)
cell.set_xticklabels(x_labels, rotation = 0)
cell.set_ylim(0,60)
cell.set_xlim(-0.5,len(branch_type)-0.5)
cell.set_ylabel('Cycles')
#cell.grid(True, axis = 'y')

def mformat(num):
    return "{0:.2f}".format(math.floor(num*100)/100)

for j in range(len(configs)):
    for i in range(len(x_labels)):
        total = 0
        for k in range(len(stall_name)):
            total += dict_total_stall[configs[j]][stall_name[k]][i]
        if total >= 60:
            cell.text(i+shift[j]-0.1,61,int(total),fontsize=font_size,rotation = 0)
        else:
            cell.text(i+shift[j]-0.1,total+1,int(total),fontsize=font_size,rotation = 0)

fig.text(0.78,0.27,"A: 192-instruction FTQ\n60-instruction Decode\nQueue",fontsize=font_size)
fig.text(0.78,0.03,"B: 18-instruction FTQ\n12-instruction Decode\nQueue",fontsize=font_size)

fig.legend(loc='upper right', ncol = 1)
fig.tight_layout()
plt.subplots_adjust(right=0.77,bottom=0.3)
fig.savefig("frontend_stall_branch_type.pdf")
#fig.savefig("frontend_stall_branch_type.png")
os.system("pdfcrop frontend_stall_branch_type.pdf")
plt.show()


# -------- code --------


