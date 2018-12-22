import json
import os
import re
import itertools
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as ticker
from bokeh.plotting import figure, output_file, show
from bokeh.transform import cumsum
#from bokeh.models.glyphs import Text
from bokeh.models import Label, LabelSet
from bokeh.models.widgets import Panel, Tabs
#from bokeh.models.glyphs import Text   #fail
#from bokeh.palettes import Spectral11  #Spectral11 only contatin 11 color
#from bokeh.charts import Donut, show   #boken.charts is not maintain for a long time
from bokeh.palettes import Category20c
from bokeh.layouts import gridplot, column, row
from pathlib import Path
from math import pi



oper_list = ['AppleDaily', 'LTN', 'DogNews', 'BusinessTimes','ChinaElectronicsNews','Chinatimes']
#oper_list = ['AppleDaily','DogNews']
#==================================================
#   there are 3 required input by user
#   focus : focus year, corpus year range is 2010~2018 (tatally 9 year), 
#           complexity is hug if accounting all 9 year, 
#           we prefer to accounting single one year, so user should assign a specific year
#   PATH  : corpus path, since we have two corpus (small/completed),
#           basically, samll corpus is saved on local storage for testing
#           compledted corpus is saved on remote storage for all data
#==================================================
focus_y  = '2018'                  # [option] focus year, if assigned, only plot this year
focus_c  = ''                      # [option] category name rather than bigcategory flag, if assigned, only plot this category
focus_o  = ''                      # [option] operator, if assigned, only plot this operator
#PATH   = '../00_corpus1/'          # testing (small) corpus
PATH = '/data2/Dslab_News/'        # full corpus


#==================================================
# input(string): one of oper_list
# return(hash):  null
# function purpose: to fill global dict 'dat_news_num' by input one of string list (oper_list)
#==================================================

def get_oper_count(oper_name,focus_y):
    json_list = list(Path(PATH+oper_name).glob(focus_y+'*/*.json'))
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

        oper_number[oper_name] = (oper_number[oper_name]+len(data)) if oper_name in oper_number.keys() else len(data)
        #print(date_info + ' ==> ' + str(len(data)))

def get_oper_category_count(oper_name,big_or_sub,focus_y):
    #---- init 2rd dict
    category_dict_num[oper_name] = dict()

    json_list = list(Path(PATH+oper_name).glob(focus_y+'*/*.json'))
    for json_file in json_list:
        #print(str(json_file))
        fn        = open(str(json_file))
        json_data = fn.read()                                             # for extrieve news number from a json, loading it first
        data      = json.loads(json_data)
        date_info = re.search('.*/(\d+)\.json',str(json_file)).group(1)   # get date information from file name
        for j_item in data:
            #print( date_info + ' j_item[BigCategory] = ' + data[j_item]['BigCategory'] +'\n')
            cate_name = data[j_item][big_or_sub]
            if cate_name not in category_dict_num[oper_name].keys():
                category_dict_num[oper_name][cate_name] = 1
            else:
                category_dict_num[oper_name][cate_name] += 1
        fn.close()
    #for cate_name in category_dict[oper_name]:
    #    print('category_dict['+oper_name+']['+cate_name+'] = ' + str(category_dict_num[oper_name][cate_name]))


def get_oper_category(oper_name,big_or_sub,focus_y):
    category_dict[oper_name] = list() 
    json_list = list(Path(PATH+oper_name).glob(focus_y+'*/*.json'))
    for json_file in json_list:
        #print(str(json_file))
        fn        = open(str(json_file))
        json_data = fn.read()                                             # for extrieve news number from a json, loading it first
        data      = json.loads(json_data)
        date_info = re.search('.*/(\d+)\.json',str(json_file)).group(1)   # get date information from file name
        for j_item in data:
            #print( date_info + ' j_item[BigCategory] = ' + data[j_item]['BigCategory'] +'\n')
            #if oper_name == 'DogNews':
                #print( date_info + ' j_item[Category] = ' + data[j_item]['Category'] + '\tbig_or_sub=' + str(big_or_sub) +'\n')
            if data[j_item][big_or_sub] not in category_dict[oper_name]:
                category_dict[oper_name].append(data[j_item][big_or_sub])
        fn.close()
    #print('category_dict['+oper_name+'] = ' + str(category_dict[oper_name]))
#==========================================================================================================
#  ooo        ooooo            .o.            ooooo      ooooo      ooo      
#  `88.       .888'           .888.           `888'      `888b.     `8'      
#   888b     d'888           .8"888.           888        8 `88b.    8       
#   8 Y88. .P  888          .8' `888.          888        8   `88b.  8       
#   8  `888'   888         .88ooo8888.         888        8     `88b.8       
#   8    Y     888        .8'     `888.        888        8       `888       
#  o8o        o888o      o88o     o8888o      o888o      o8o        `8       
#==========================================================================================================

tab_oo_list = []
for focus in list(map(str,list(range(2010,2019)))):
    print('\n\nfocus ==> ' + focus)
    date_news_num = dict()
    #oper_number   = dict()
    oper_number = dict.fromkeys(oper_list,0)
    category_dict = dict()
    category_dict_num = dict()

    for i in range(len(oper_list)):

        #print('------------------------ ' + oper_list[i] + ' ---------------------------')
        get_oper_count(oper_list[i],focus)
        #big_or_sub = 'BigCategory' if oper_list[i] in ['AppleDaily','LTN'] else 'Category'
        big_or_sub = 'BigCategory'
        get_oper_category(oper_list[i],big_or_sub,focus)
        get_oper_category_count(oper_list[i],big_or_sub, focus)

    # way 2
    if sum(oper_number.values()) == 0: continue
    max_oper_name = max(oper_number.keys(), key=lambda k: oper_number[k])


    for op_idx in range(len(oper_list)):
        data = pd.Series(category_dict_num[oper_list[op_idx]]).reset_index(name='value').rename(columns={'index':'category'})
        data = data.sort_values(by=['value'])

        #data['angle'] = data['value']/data['value'].sum() * 2*pi
        data['percent'] = data['value']/data['value'].sum()
        this_category = category_dict_num[oper_list[op_idx]]
        #print(focus + '\t' + str(op_idx) + "\t{:20s}".format(oper_list[op_idx]))
        #print(focus + '\t' + str(op_idx) + "{:20s}".format(oper_list[op_idx]) + '\t' + str(len(category_dict[oper_list[op_idx]]) )
        print(focus + '\t' + str(op_idx) + "\t{:16s}".format(oper_list[op_idx]) + '\t' + str(len(category_dict[oper_list[op_idx]])) + '\t' + str(category_dict[oper_list[op_idx]]))
