# file: intro_sota_ideal_graph.ipynb
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
from scipy.stats.mstats import gmean
import pandas as pd

part1_trace_file="Champsim-Prefetcher-Thesis/scripts/cvp_srv_part1_trace_list.txt"
part2_trace_file="Champsim-Prefetcher-Thesis/scripts/cvp_secret_srv_part2_trace_list.txt"
ipc_trace_file="Champsim-Prefetcher-Thesis/scripts/ipc_trace_list.txt"

part1_results_folder="Champsim-Prefetcher-Thesis/cvp_sota_srv_part1_20M/"
part2_results_folder="Champsim-Prefetcher-Thesis/cvp_sota_srv_part2_results_20M/"
ipc_results_folder="Champsim-Prefetcher-Thesis/ipc_sota_results_50M/"

before_pref="-hashed_perceptron-"
after_pref="-no-no-no-no-no-no-lru-lru-lru-srrip-drrip-lru-lru-lru-1core.txt"
after_pref_cvp="-no-no-no-no-no-no-lru-lru-lru-srrip-drrip-lru-lru-lru-1core-cvp_trace.txt"

other_pref = ['rdip', 'pif', 'shotgun']

pref = ['rdip', 'pif','gang_4k_pif','shotgun','btb_8k_shotgun','div_conq','btb_8k','btb_8k_div_conq','fnlmma_ipc',\
        'fnlmma_under_10KB','entangled_under_10KB',\
        'fnlmma_under_32KB','entangled_ipc','entangled_under_32KB','cfnlmma_16KB', 'l1i_16KB_btb_6K_cfnlmma_16KB',\
        'l1i_16KB_cfnlmma_32KB','perfect_btb','perfect_l1i','perfect_btb_l1i','gang_baseline_itlb']


server = []
client = []

for i in range(len(pref)):
    server.append([])
    client.append([])

def get_ipc(file_name):
    temp_file = open(file_name)
    for line1 in temp_file:
        if re.search("CPU 0 cumulative IPC:", line1):
            return float(line1.split(" ")[4].strip())
    return 0.0

part1_file = open(part1_trace_file, "r")
for line in part1_file:
    base_ipc = get_ipc(part1_results_folder+line.strip()+before_pref+"no"+after_pref_cvp)
    for i in range(len(pref)):
        if pref[i] == None:
            server[i].append(0)
            continue
        curr_ipc = get_ipc(part1_results_folder+line.strip()+before_pref+pref[i]+after_pref_cvp)
        if curr_ipc == 0:
            continue
        server[i].append(curr_ipc/base_ipc)
    
part2_file = open(part2_trace_file, "r")
for line in part2_file:
    base_ipc = get_ipc(part2_results_folder+line.strip()+before_pref+"no"+after_pref_cvp)
    for i in range(len(pref)):
        if pref[i] == None:
            server[i].append(0)
            continue
        curr_ipc = get_ipc(part2_results_folder+line.strip()+before_pref+pref[i]+after_pref_cvp)
        if curr_ipc == 0:
            continue
        server[i].append(curr_ipc/base_ipc)

ipc_file = open(ipc_trace_file, "r")
for line in ipc_file:
    base_ipc = get_ipc(ipc_results_folder+line.strip()+before_pref+"no"+after_pref)
    for i in range(len(pref)):
        if pref[i] == None:
            server[i].append(0)
            continue
        curr_ipc = get_ipc(ipc_results_folder+line.strip()+before_pref+pref[i]+after_pref)
        if curr_ipc == 0:
            continue
#         if "client" in line:
#             client[i].append(curr_ipc/base_ipc)
#         else:
        server[i].append(curr_ipc/base_ipc)

# -------- code --------
server_df = {}
for i in range(len(server)):
    server_df[pref[i]] = gmean(server[i])
    print(pref[i], len(server[i]),server_df[pref[i]])

storage_df = {'rdip':131072,'pif':0,'shotgun':896,'div_conq':7168,'cfnlmma_16KB':-8041,'fnlmma_ipc':99328,\
              'perfect_btb_l1i':0,'shotgun_fnlmma_under_32KB': 38912,'shotgun_entangled_under_32KB': 38912,\
             'confluence':76800,'fdipx':36864,'phantom':27648,'perfect_btb':0,'perfect_l1i':0,\
              'l1i_16KB_cfnlmma_32KB':19824,'fnlmma_under_32KB':31318,'entangled_under_32KB':32768,\
             'gang_4k_pif':0}
#prev-> 36864
print(server_df)
print(storage_df)

# -------- code --------


# -------- code --------
import re
from scipy.stats.mstats import gmean
import pandas as pd

trace_file="../Champsim-Prefetcher-Thesis/scripts/micro_trace_list.txt"

micro_results_folder="../Champsim-Prefetcher-Thesis/micro_sota_50M/"

before_pref="-hashed_perceptron-"
after_pref_cvp="-ipcp_isca-ipcp_isca-no-no-no-no-lru-lru-lru-srrip-drrip-lru-lru-lru-1core-cvp_trace.txt"

pref = ['shotgun','div_conq','csbtb_8k','fdipx_8k','mbtb_4k_2variants_2cycle',\
        'perfect_btb','perfect_l1i','perfect_btb_l1i']

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

# -------- code --------
server_df_8k = {}
for i in range(len(server)):
    server_df_8k[pref[i]] = gmean(server[i])
    print(pref[i], len(server[i]),server_df_8k[pref[i]])

storage_df_8k = {'shotgun':-1792,'div_conq':7782.4,'csbtb_8k':-2048,\
              'perfect_btb_l1i':0,'perfect_btb':0,'perfect_l1i':0,'fdipx_8k':-26704,\
              'mbtb_4k_2variants_2cycle':-48128,'skewed_mbtb_6k_return_optimized':-24576}
    
print(server_df_8k)
print(storage_df_8k)

# -------- code --------
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter
from scipy.stats.mstats import gmean
import os

import matplotlib.pylab as pylab

font_size=20
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

fig, cells = plt.subplots(nrows = 1, ncols = 1,figsize=(12,5),sharey=True)

baseline_storage = 58368.0

ind = np.arange(len(server_df_8k))

cell = cells
baseline_storage = 95232.0

marker_df = {'csbtb_8k':'<','fdipx_8k':'.','shotgun':'4','div_conq':'o','btb_8k_cfnlmma_32KB':'d','fnlmma_ipc':'^','perfect_btb_l1i':'s',\
             'mbtb_4k_2variants_2cycle': 'd','skewed_mbtb_6k_return_optimized': '>',"confluence":"<","fdipx":">",\
            'phantom':'2','perfect_btb':'x','perfect_l1i':'P','l1i_16KB_cfnlmma_32KB':'o','btb_8k_entangled_under_32KB':'3',\
            'btb_8k_fnlmma_under_32KB':'1','gang_8k_pif':'o'}

label_df = {'csbtb_8k':'8K entry SKEWED BTB','fdipx_8k':'8K entry FDIPX','shotgun':'SHOTGUN','div_conq':'SN4L+DIS+BTB','l1i_16KB_cfnlmma_32KB':'GANG-\nCOMPETITIVE',\
            'fnlmma_ipc':'FNL+MMA','perfect_btb_l1i':'IDEAL FRONTEND','shotgun_fnlmma_under_32KB': "SHOTGUN-BTB+FNL+MMA",\
            'mbtb_4k_2variants_2cycle': "4K entry MBTB","confluence":"CONFLUENCE","fdipx":"FDIP-X",\
           'phantom':'SHIFT+PHANTOM','perfect_btb':'IDEAL BTB','perfect_l1i':'IDEAL L1I',\
           'skewed_mbtb_6k_return_optimized':'6K entry MBTB','btb_8k_entangled_under_32KB':'EIP',\
           'btb_8k_fnlmma_under_32KB':'FNL+MMA','btb_8k_cfnlmma_32KB':'GANG FRONTEND',\
           'gang_8k_pif':'GANG BTB + FDIP'}

for i in range(len(pref)):
    if "mbtb" in pref[i]:
        cell.scatter((storage_df_8k[pref[i]] + baseline_storage )/ baseline_storage,server_df_8k[pref[i]],s=200,marker=marker_df[pref[i]],label=label_df[pref[i]],edgecolor='black',color='blue')
    elif "perfect" in pref[i]:
        cell.scatter((storage_df_8k[pref[i]] + baseline_storage )/ baseline_storage,server_df_8k[pref[i]],s=200,marker=marker_df[pref[i]],label=label_df[pref[i]],edgecolor='black',color='red')
    else:
        cell.scatter((storage_df_8k[pref[i]] + baseline_storage )/ baseline_storage,server_df_8k[pref[i]],s=200,marker=marker_df[pref[i]],label=label_df[pref[i]],edgecolor='black',color='green')
cell.axvline(1,linestyle = '--', color='black')
cell.axhline(1,linestyle = '--', color='black')

cell.yaxis.set_major_formatter(formatter)
cell.xaxis.set_major_formatter(formatter)
cell.set_ylim(0.95,1.25)
cell.set_xlim(0.4,1.1)
#cell.set_xticklabels([])
cell.set_ylabel('Normalized\nPerformance')
cell.set_xlabel('Normalized Area')

fig.legend(loc='upper center', ncol = 3,borderpad=0.1,columnspacing=1,labelspacing=0.2,handletextpad=1)
fig.tight_layout()
plt.subplots_adjust(top=0.75)
fig.savefig("intro_sota_ideal.pdf")
os.system("pdfcrop intro_sota_ideal.pdf")
plt.show()


# -------- code --------


