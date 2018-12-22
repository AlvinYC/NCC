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
date_news = pd.DataFrame(columns=['date']+oper_list)
#date_news = pd.DataFrame(columns=oper_list)
date_news.set_index(['date'])
date_news.drop('date',axis=1,inplace=True)

#category_dict_num = dict()
#title_dict = dict()
oper_name = 'LTN'
channel_plot = []
#def get_oper_count(oper_name,focus):
for year in range(2010,2019):
    focus = str(year)
    total_element = 0
    #category_dict_num[oper_name] = dict()
    title_dict = dict()
    json_list = list(Path(PATH+oper_name).glob(focus+'*/*.json'))
    for idx,json_file in enumerate(json_list):
        fn        = open(str(json_file))
        json_data = fn.read()                                             # for extrieve news number from a json, loading it first
        data      = json.loads(json_data)
        date_info = re.search('.*/(\d+)\.json',str(json_file)).group(1)   # get date information from file name

        for idy,j_item in enumerate(data):

            if data[j_item]['Title'] in title_dict.keys():
                title_dict[data[j_item]['Title']] += 1
            else:
                title_dict[data[j_item]['Title']] = 1

            total_element += 1    
        #print(str(idx) + '\t' + str(json_file))
        #print('total number of data = ' + str(len(data)))
        fn.close()
    over300 = 0
    equalone = 0
    duparticle = 0
    for key in title_dict.keys():
        if title_dict[key] > 1:
            over300 += title_dict[key]
            duparticle += 1
        if title_dict[key] == 1:
            equalone += 1

    print('total item ' + str(total_element))
    print('total uniq item ' + str(len(title_dict)))
    print('over300 ' + str(over300))
    print('dup article ' + str(duparticle))
    print('equalone ' + str(equalone))
    equalone_p    = round(equalone/total_element,3)
    duparticle_p  = round(duparticle / total_element,3)
    redundent     = total_element-duparticle-equalone
    redundent_p   = round(redundent / total_element,3)
    date_news = pd.DataFrame(columns=['oper_name','category','year','value','total','percentage','angle','color'])
    date_news.loc[0]=[oper_name,'Uniq',2010,equalone,total_element,equalone_p,equalone_p*2*pi,Category20c[20][0]]
    date_news.loc[1]=[oper_name,'Dup',2010,duparticle,total_element,duparticle_p,duparticle_p*2*pi,Category20c[20][1]]
    date_news.loc[2]=[oper_name,'Redundent',2010,redundent,total_element,redundent_p,redundent_p*2*pi,Category20c[20][2]]
    #print(date_news)
    
    #banner = '{:,}'.format(oper_name)
    p = figure(plot_height=380, plot_width=380, title=oper_name, toolbar_location=None, x_range=(-0.5, 1.0),tools="hover",
               tooltips=[("category", "@category"),("article number","@value{,}"),("percentage","@percentage{0.00%}")])
    p.wedge(x=0, y=1, radius= 0.4,
                start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
                line_color="white", fill_color='color', legend='category',source=date_news)
    #output_file("foo.html")
    mytext = Label(x=-0.1, y=1.85, text=focus+'({:,})'.format(total_element), text_font_size='15pt')
    p.add_layout(mytext)
    p.title.text_font_size = '14pt'  # title size
    p.axis.axis_label = None
    p.axis.visible = False
    p.grid.grid_line_color = None
    channel_plot.append(p)

grid = gridplot(channel_plot, ncols=5)
show(grid)
#get_oper_count(oper_list[1],'2011')
