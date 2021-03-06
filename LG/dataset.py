
import json
import re
import pandas as pd
import datetime
import jieba
import codecs
import time
from pathlib import Path

class NewsDataset():
    def __init__(self, transform=None, news_folder=None, op_list=None,force_rebuild=False, pkl_name='./News_PD.pkl', FnStopword=None):
        self.transform = transform
        self.news_folder = news_folder
        self.op_list = op_list
        self.pkl_name = pkl_name
        self.News_PD = pd.DataFrame(columns=['uid','op_name', 'date', 'Title', 'BigCateogy', 'Category', 'URL', 'WordSeg'])
        self.uid = 0
        self.FnStopword = FnStopword
        self.ParaChecker()
        self.stopwords = codecs.open(FnStopword, 'r', 'utf-8').read().split('\n') if self.FnStopword != None else None

        # force to rebuild (reset) pandas if force_build flag is TRUE
        # otherwise to read pandas pickle
        if force_rebuild == False:
            if Path(self.pkl_name).exists():
                self.News_PD = pd.read_pickle(self.pkl_name)
                return None

        for op_name in op_list:
            p = Path(self.news_folder +  op_name)
            json_list = list(p.glob('*/*.json'))
            print('------- this op_name = ' + op_name)
            for json_file in json_list:
                date_info = self.RetrieveDateFromFname(json_file)
                fn        = open(str(json_file))
                json_data = fn.read()
                Jdata     = json.loads(json_data)

                for Jitem in Jdata:
                    # skip this item because pandas already exists same title
                    if self.Duplicate_Check(op_name, Jdata[Jitem]['Title']) == True:
                        continue

                    one_news = pd.Series([self.News_PD.__len__(),
                                          op_name,
                                          date_info,
                                          Jdata[Jitem]['Title'],
                                          Jdata[Jitem]['BigCategory'],
                                          Jdata[Jitem]['Category'],
                                          Jitem,
                                          ''],index=self.News_PD.columns)
                    self.News_PD = self.News_PD.append(one_news, ignore_index=True)
                fn.close()
        self.update_segmentation(method='Jieba', apply_stop=True)
        self.News_PD.to_pickle(self.pkl_name)
        return None

    def Duplicate_Check(self,op_name,Title):
        return self.News_PD[self.News_PD['op_name']==op_name]['Title'].isin([Title]).any()

    def RetrieveDateFromFname(self,json_file_name):
        date_info = re.search('.*/(\d+)\.json', str(json_file_name)).group(1)  # get date information from file name
        find_date = re.search(r'(\d{4})(\d{2})(\d{2})', date_info)
        if find_date:
            find_date = list(map(int, list(find_date.groups())))
            date_info = datetime.datetime(find_date[0], find_date[1], find_date[2])
        else:
            print('error to decode date_info for ' + str(date_info))
        return date_info

    def ParaChecker(self):
        if not Path(self.news_folder).exists():
            print('news_folder is NOT exist ==> ' + str(news_folder))
            raise ValueError

        if not Path(self.news_folder).exists():
            print('news_folder is NOT exist ==> ' + str(news_folder))
            raise ValueError

        if len(self.op_list) == 0:
            print('news_folder is NOT exist ==> ' + str(news_folder))
            raise ValueError

        for op_name in self.op_list:
            if not Path(self.news_folder, op_name).exists():
                print('op_name is NOT exist ==> ' + str(Path(self.news_folder , op_name)))
                raise ValueError

        if self.FnStopword != None:
            if not Path(self.FnStopword).exists():
                print('stopword not found ==> ' + str(self.FnStopword))
                raise ValueError


    def __len__(self):
        return self.News_PD.__len__()


    def __getitem__(self,idx):
        try:
            self.News_PD.iloc[idx]
        except:
            return IndexError

    def update_segmentation(self,method='Jieba', apply_stop=True):
        def seg_apply_stopword(x):
            befor_stopword = jieba.lcut(x)
            if (apply_stop == True) and (self.FnStopword != None):
                after_stopword = list(filter(lambda word: word not in self.stopwords, befor_stopword))
            else:
                after_stopword = befor_stopword
            return after_stopword

        if method == 'Jieba':
            segmentation = lambda x: seg_apply_stopword(x)
        else:
            # reserve for other segmentation method such as CKIP
            segmentation = lambda x: jieba.lcut(x)

        self.News_PD['WordSeg'] = self.News_PD['Title'].map(segmentation)



if __name__=='__main__':
    news_folder = './corpus/'
    pkl_name    = './News_PD.pkl'
    FnStopword  = './stopwords/stopwords357'
    op_list     = ['AppleDaily', 'LTN', 'DogNews', 'BusinessTimes', 'ChinaElectronicsNews', 'Chinatimes']
    #op_list    = ['AppleDaily']


    start = time.time()
    dataset = NewsDataset(news_folder=news_folder,op_list=op_list,force_rebuild=True, pkl_name=pkl_name, FnStopword=FnStopword)
    print('dataset size = ' + str(dataset.__len__()))
    end = time.time()
    print('execution time = ' + str(end-start))