# file: fetch_retire_diff.ipynb
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

file_name = '../baseline.txt'

baseline_diff = []
total_baseline_diff = 0
total_baseline_cnt = 0

for line in open(file_name,'r'):
    if re.search('FETCH_RETIRE_ID',line):
        diff = int(line.strip().split()[-1])
        baseline_diff.append(diff)
        total_baseline_diff += diff
        total_baseline_cnt += 1
        
print(total_baseline_diff / total_baseline_cnt,total_baseline_cnt,max(baseline_diff),min(baseline_diff))

file_name = '../lowconfig.txt'

lowconfig_diff = []
total_lowconfig_diff = 0
total_lowconfig_cnt = 0

for line in open(file_name,'r'):
    if re.search('FETCH_RETIRE_ID',line):
        diff = int(line.strip().split()[-1])
        lowconfig_diff.append(diff)
        total_lowconfig_diff += diff
        total_lowconfig_cnt += 1
        if total_lowconfig_cnt == total_baseline_cnt:
            break
        
print(total_lowconfig_diff / total_lowconfig_cnt, total_lowconfig_cnt,max(lowconfig_diff),min(lowconfig_diff))

# -------- code --------
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter
from scipy.stats.mstats import gmean
import os
import matplotlib.pylab as pylab
import statistics

font_size = 20

params = {'legend.fontsize': font_size,
          'figure.figsize': (15, 5),
         'axes.labelsize': font_size,
         'axes.titlesize':font_size,
         'xtick.labelsize':font_size,
         'ytick.labelsize':font_size}
pylab.rcParams.update(params)

fig, cells = plt.subplots(nrows = 1, ncols = 1,figsize=(15,4),sharex=True)


ind = np.arange(total_baseline_cnt)
cell = cells

linestyle = [':',':',':','solid','solid']
color = ['grey','grey','black','grey','black']
color = ['grey','m','blue','red','black','black']

cell.plot(ind, baseline_diff,label="Baseline",linestyle='solid',color='black')
cell.plot(ind, lowconfig_diff,label="Low config",linestyle='solid',color='grey')

cell.yaxis.set_major_formatter(formatter)
cell.yaxis.set_major_formatter(formatter)

cell.axhline(total_baseline_diff / total_baseline_cnt,color='black',linestyle='--')
cell.axhline(total_lowconfig_diff / total_lowconfig_cnt, color='grey',linestyle='--')

cell.set_xlim(97000,98000)
cell.set_ylim(0,600)

cell.set_ylabel('Number of in-flight\ninstructions')
#cell.set_xlabel('Traces')

policy=['Sunny Cove','Broadwell']

fig.legend(policy,loc=[0.1,0.7],ncol=1)
fig.tight_layout()
#plt.subplots_adjust(top = 0.85,bottom=0.2)
fig.savefig("fetch_retire_diff.pdf")
fig.savefig("fetch_retire_diff.png")
os.system("pdfcrop fetch_retire_diff.pdf")
plt.show()


