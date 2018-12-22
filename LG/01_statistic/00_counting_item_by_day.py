import json
import os
import numpy as np
import re
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as ticker
from pathlib import Path



oper_list = ['AppleDaily', 'LTN', 'DogNews', 'BusinessTimes','ChinaElectronicsNews','Chinatimes']
#==================================================
#   there are only two required input by user
#   focus : focus year, corpus year range is 2010~2018 (tatally 9 year), 
#           complexity is hug if accounting all 9 year, 
#           we prefer to accounting single one year, so user should assign a specific year
#   PATH  : corpus path, since we have two corpus (small/completed),
#           basically, samll corpus is saved on local storage for testing
#           compledted corpus is saved on remote storage for all data
#==================================================
focus  = '2018'
PATH   = '../00_corpus1/'          # testing (small) corpus
#PATH = '/data2/Dslab_News/'        # full corpus


#==================================================
# input(string): one of oper_list
# return(hash):  null
# function purpose: to fill global dict 'dat_news_num' by input one of string list (oper_list)
#==================================================
date_news_num = dict()

def get_oper_count(oper_name):
    json_list = list(Path(PATH+oper_name).glob(focus+'*/*.json'))
    for json_file in json_list:
        fn        = open(str(json_file))
        json_data = fn.read()                                             # for extrieve news number from a json, loading it first
        data      = json.loads(json_data)                           
        date_info = re.search('.*/(\d+)\.json',str(json_file)).group(1)   # get date information from file name
        
        if date_info in date_news_num.keys():
            date_news_num[date_info][oper_list.index(oper_name)] = len(data)
        else:
            date_news_num[date_info] = [float('nan')] * len(oper_list)
            date_news_num[date_info][oper_list.index(oper_name)] = len(data)
        fn.close()
        #print(date_info + ' ==> ' + str(len(data)))

#==========================================================================================================
#  ooo        ooooo            .o.            ooooo      ooooo      ooo      
#  `88.       .888'           .888.           `888'      `888b.     `8'      
#   888b     d'888           .8"888.           888        8 `88b.    8       
#   8 Y88. .P  888          .8' `888.          888        8   `88b.  8       
#   8  `888'   888         .88ooo8888.         888        8     `88b.8       
#   8    Y     888        .8'     `888.        888        8       `888       
#  o8o        o888o      o88o     o8888o      o888o      o8o        `8       
#==========================================================================================================
for i in range(len(oper_list)):
    print('------------------------ ' + oper_list[i] + ' ---------------------------')
    get_oper_count(oper_list[i])

#======= Debug Show ==========
'''
for item in sorted(date_news_num.keys()):
    print(item + ' ==> ' + str(date_news_num[item]))
'''
# display
operkey = sorted(date_news_num.keys())
for i in range(len(oper_list)):
    value1 = [date_news_num[date_key][i] for date_key in operkey]
    plt.plot(operkey,value1)

ax = plt.gca()
ax.xaxis.set_major_locator(ticker.MultipleLocator(7))
plt.title(focus+' news counting (day)')
plt.xticks(rotation=70,fontsize=10)
plt.legend(oper_list)
plt.grid(True)
plt.show()

