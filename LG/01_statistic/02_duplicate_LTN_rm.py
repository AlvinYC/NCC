import json
import os
import numpy as np
import pandas as pd
import re
import datetime
from bokeh.palettes import Spectral11, Category20c
from bokeh.transform import cumsum
from bokeh.plotting import figure, show, output_file, ColumnDataSource
from bokeh.models import Label, LabelSet
from bokeh.models import HoverTool,WheelZoomTool, PanTool, ResetTool
from bokeh.layouts import gridplot, column, row
from pathlib import Path
from math import pi



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
focus  = '2010'
#focus  = ''
PATH   = '../corpus/'          # testing (small) corpus
#PATH = '/data2/Dslab_News/'        # full corpus


#==================================================
# input(string): one of oper_list
# return(hash):  null
# function purpose: to fill global dict 'dat_news_num' by input one of string list (oper_list)
#==================================================
date_news_num = dict()
dup_storage   = dict()

date_news = pd.DataFrame(columns=['date']+oper_list)
date_news.set_index(['date'])
date_news.drop('date',axis=1,inplace=True)

oper_name = 'LTN'
for year in range(2010,2018):
    focus = str(year)
    total_element = 0
    title_one_year = dict()
    json_list = list(Path(PATH+oper_name).glob(focus+'*/*.json'))
    json_out  = {}
    for idx,json_file in enumerate(json_list):
        fn        = open(str(json_file))
        json_data = fn.read()                                             # for extrieve news number from a json, loading it first
        data      = json.loads(json_data)
        date_info = re.search('.*/(\d+)\.json',str(json_file)).group(1)   # get date information from file name

        for idy,j_item in enumerate(data):
            thisT = data[j_item]['Title']
            if thisT in title_one_year.keys():
                # notify this key is duplicate, append to dup_storage
                dup_storage[thisT] += 1
                #------------------ remove physical file --------
            else:
                # this key appear in this year first time
                # but it doesn't mean it don't duplicate from another year.
                if thisT in dup_storage.key();
                    # we still need remove this item because it duplicate from another year
                    title_one_year[thisT] = 1 #

                else:

                    # output this item to json
                    json_out[j_item] = data[j_item]
                    dup_storage[thisT] = 1

            total_element += 1    
        #print(str(idx) + '\t' + str(json_file))
        #print('total number of data = ' + str(len(data)))
        fn.close()
    #over300 = 0
    #equalone = 0
    #duparticle = 0

    #print('total item ' + str(total_element))
    #print('total uniq item ' + str(len(title_dict)))
    #print('over300 ' + str(over300))
    #print('dup article ' + str(duparticle))
    #print('equalone ' + str(equalone))
