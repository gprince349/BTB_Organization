# file: Starvation_cycles_per_kilo_instr.ipynb
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

pref = ['baseline','perfect_btb','perfect_l1i','perfect_btb_l1i']

for i in range(1):
    temp = []
    for j in range(len(pref)):
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
    for i in range(len(pref)):
        search_param = "Starvation_cycles_per_kilo_instr_0:"
        mpki_val = get_mpki(micro_results_folder+line.strip()+before_pref+pref[i]+after_pref_cvp,search_param)
        for j in range(len(mpki_val)):
            server_total_mpki[j][i] += mpki_val[j]
    server_count = server_count + 1
    
for i in range(1):
    for j in range(len(pref)):
        server_total_mpki[i][j] /= server_count

print(server_total_mpki)

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

x_labels = ["BASELINE","IDEAL\nBTB", "IDEAL\nL1I","IDEAL\nFRONTEND"]
colors = ["black", "white"]

fig, cells = plt.subplots(nrows = 1, ncols = 1,figsize=(5,3),sharex=True)


ind = np.arange(4)

width = 0.4

cell = cells

shift = [-1.5*width, -0.5*width , 0.5*width, 1.5*width]

color = ['white','lightgrey','grey','black']

#cell.bar(ind, [server_total_mpki[0][0],server_total_mpki[0][1],server_total_mpki[0][2],server_total_mpki[0][3],server_total_mpki[0][4]] ,width,edgecolor='black',color="grey")
cell.bar(ind, [server_total_mpki[0][0],server_total_mpki[0][1],server_total_mpki[0][2],server_total_mpki[0][3]] ,width,edgecolor='black',color="grey")


def mformat(num):
    return "{0:.2f}".format(math.floor(num*100)/100)
    

fig.text(0.25,0.75,mformat(server_total_mpki[0][0]),fontsize='x-large')
fig.text(0.43,0.44,mformat(server_total_mpki[0][1]),fontsize='x-large')
fig.text(0.62,0.58,mformat(server_total_mpki[0][2]),fontsize='x-large')
fig.text(0.81,0.37,mformat(server_total_mpki[0][3]),fontsize='x-large')
#fig.text(0.83,0.25,mformat(server_total_mpki[0][4]),fontsize='x-large')

cell.set_xlim(-0.5,3.5)
cell.set_ylim(0,400)
cell.set_xticks(ind)
cell.set_xticklabels(x_labels)
cell.set_ylabel('Starvation Cycles\nPer Kilo Instructions')

policy = ['4K', '8K', '16K','32K']
#fig.legend(policy,loc='upper center',ncol=4)
fig.tight_layout()
#plt.subplots_adjust(top=0.8)
fig.savefig("scki.pdf")
os.system("pdfcrop scki.pdf")
plt.show()


# -------- code --------
import re

trace_file="Champsim-Prefetcher-Thesis/scripts/micro_trace_list.txt"

micro_results_folder="Champsim-Prefetcher-Thesis/micro_sota_50M/"

before_pref="-hashed_perceptron-"
after_pref_cvp="-ipcp_isca-ipcp_isca-no-no-no-no-lru-lru-lru-srrip-drrip-lru-lru-lru-1core-cvp_trace.txt"

server_total_mpki = []
server_count = 0

pref = ['baseline','shotgun','div_conq','csbtb_8k','fdipx_8k','mbtb_4k_2variants_2cycle',\
        'mbtb_8k_2variants_2cycle','perfect_btb']

for i in range(1):
    temp = []
    for j in range(len(pref)):
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
    for i in range(len(pref)):
        search_param = "Starvation_cycles_per_kilo_instr_0:"
        mpki_val = get_mpki(micro_results_folder+line.strip()+before_pref+pref[i]+after_pref_cvp,search_param)
        for j in range(len(mpki_val)):
            server_total_mpki[j][i] += mpki_val[j]
    server_count = server_count + 1
    
for i in range(1):
    for j in range(len(pref)):
        server_total_mpki[i][j] /= server_count

print(server_total_mpki)

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

colors = ["black", "white"]

fig, cells = plt.subplots(nrows = 1, ncols = 1,figsize=(11,3),sharex=True)


ind = np.arange(4)

width = 0.4

cell = cells

shift = [-1.5*width, -0.5*width , 0.5*width, 1.5*width]

color = ['white','lightgrey','grey','black']

temp_df = []
for i in range(0,len(pref)):
    temp_df.append(server_total_mpki[0][i])
ind = np.arange(len(pref))

cell.bar(ind, temp_df ,width,edgecolor='black',color="grey")


def mformat(num):
    return "{0:.2f}".format(num)
    

x_label = ['BASELINE','SHOTGUN\n- 8K', 'SN4L+DIS+\nBTB - 8K','SKEWED\nBTB - 8K','FDIPX\n - 8K',
           'MBTB -\n4K', 'MBTB -\n8K','IDEAL\nBTB']

cell.axvline(0.5,linestyle = '--', color='black')
cell.axvline(4.5,linestyle = '--', color='black')
cell.axvline(6.5,linestyle = '--', color='black')

for i in range(len(x_label)):
    cell.text(i-0.30,temp_df[i]+10,mformat(temp_df[i]),fontsize='x-large',rotation = 0)


#cell.set_xlim(-0.5,3.5)
cell.set_ylim(0,400)
cell.set_xticks(ind)
cell.set_xticklabels(x_label, rotation = 0)
cell.set_ylabel('L2BTB MPKI')
cell.set_ylabel('Starvation Cycles\nPer Kilo Instructions')

policy = ['4K', '8K', '16K','32K']
#fig.legend(policy,loc='upper center',ncol=4)
fig.tight_layout()
#plt.subplots_adjust(top=0.8)
fig.savefig("scki_sota.pdf")
os.system("pdfcrop scki_sota.pdf")
plt.show()


