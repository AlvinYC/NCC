import json
import os
import numpy as np
import pandas as pd
import re
import datetime
from bokeh.palettes import Spectral11, Category20c
from bokeh.plotting import figure, show, output_file, ColumnDataSource
from bokeh.models.widgets import Panel, Tabs
from bokeh.models import  HoverTool,WheelZoomTool, PanTool, ResetTool
from pathlib import Path
from bokeh.models import DataRange1d, LinearAxis, Range1d


oper_list = ['AppleDaily', 'LTN', 'DogNews', 'BusinessTimes','ChinaElectronicsNews','Chinatimes']
#oper_list = ['AppleDaily', 'LTN', 'DogNews', 'BusinessTimes','Chinatimes']
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
#focus  = ''
#PATH   = '../00_corpus1/'          # testing (small) corpus
PATH = '/data2/Dslab_News/'        # full corpus




def get_oper_count(oper_name,focus):
    json_list = list(Path(PATH+oper_name).glob(focus+'*/*.json'))

    for json_file in json_list:
        fn        = open(str(json_file))
        json_data = fn.read()                                             # for extrieve news number from a json, loading it first
        data      = json.loads(json_data)                           
        date_info = re.search('.*/(\d+)\.json',str(json_file)).group(1)   # get date information from file name
        find_date = re.search(r'(\d{4})(\d{2})(\d{2})',date_info)
        if find_date:
            find_date = list(map(int,list(find_date.groups())))
            date_info = datetime.datetime(find_date[0],find_date[1],find_date[2])
            #date_info = str(find_date[0]) + '-' + str(find_date[1]) + '-' + str(find_date[2])

        else:
            print('error to decode date_info for ' + str(date_info))

        if date_info in date_news.index:
            #date_news_num[date_info][oper_list.index(oper_name)] = len(data)
            date_news.ix[date_info][oper_name] = len(data)
        else:
            date_news.ix[date_info] = 'nan'
            date_news.ix[date_info][oper_name] = len(data)


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
tab_oo_list = []
for focus in list(map(str,list(range(2010,2019)))):
    print('\n=========================' + focus + '=============================')
    #focus = '2018'

    #==================================================
    # input(string): one of oper_list
    # return(hash):  null
    # function purpose: to fill global dict 'dat_news_num' by input one of string list (oper_list)
    #==================================================
    date_news_num = dict()
    date_news = pd.DataFrame(columns=['date']+oper_list)
    date_news.set_index(['date'])
    date_news.drop('date',axis=1,inplace=True)

    for i in range(len(oper_list)):
        print('------------------------ ' + oper_list[i] + ' ---------------------------')
        get_oper_count(oper_list[i],focus)

    #======= Debug Show ==========
    date_news = date_news.sort_index()
    date_news.to_pickle('xxx.pd')
    numlines  = len(date_news.columns)
    #print(date_news)
    #mypalette =Category20c[20][0:numlines]
    mypalette = Spectral11

    ############################################################################################################
    # method three: p.multi_line w/ ColumnDataSource
    ############################################################################################################
    date_news_dict = {'xs':[date_news.index.values for x in range(numlines)],
                      'ys':[date_news[oper_list[x]].values for x in range(numlines)],
                      'labels': oper_list,
                      'color': Category20c[20][0:numlines*2:2]
                      #'color': Spectral11[1:numlines+1]
                      }
    data = ColumnDataSource(date_news_dict)
    hover = HoverTool(
        tooltips=[
            ('date', 'xs'),
            ('article', '$ys'),
        ]
    )

    #tools = [PanTool(), WheelZoomTool(), ResetTool(), hover]
    #p = figure(x_axis_type="datetime",tools="hover",y_range=Range1d(0,1500))
    p = figure(x_axis_type="datetime", y_range=Range1d(0, 1500), plot_width=1500)
    #p = figure(x_axis_type="datetime", tools=tools, y_range=Range1d(0, 1500))
    p.multi_line(xs='xs',
                    ys='ys',
                    legend='labels',
                    line_color='color',
                    line_width=3,
                    source=data)
    #p.add_tools(HoverTool(tooltips=[('article', '@ys')]))
    tab = Panel(child=p, title=focus)
    tab_oo_list.append(tab)

tabs = Tabs(tabs=tab_oo_list)
show(tabs)