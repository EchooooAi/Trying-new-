import re
import requests
import pandas as pd

def retrieve_dji_list():
    url = 'http://money.cnn.com/data/dow30/'
    req= requests.get(url)
    # company
    company_simp = 'class="wsod_symbol">(.*?)</a>'
    company_full = '<span title="(.*?)">.*?</span>'
    # price
    price = '<span.*?class="wsod_stream">(.*?)</span>'
    # 中间用.*?连接
    search_pattern = re.compile(r'class="wsod_symbol">(.*?)</a>.*?<span title="(.*?)">.*?</span>.*?<span.*?class="wsod_stream">(.*?)</span>',re.S)
    #返回列表，每一项都是一个元组
    dji_list_in_text = re.findall(search_pattern,req.text)
    dji_list =[]
    for item in dji_list_in_text:
        dji_list.append([item[0],item[1],float(item[2])])
        #append(obj) 添加的对象是列表
        #对应pd.DataFrame([[1],[2]]) 数组形式[[],[],[]]
    return dji_list
if __name__=='__main__':
    dji_list = retrieve_dji_list()
    djidf = pd.DataFrame(dji_list)
    # dataframe 形式 [{}{}{}]
    print(djidf)

    '''
    djidf.columns = ['1','2','3']
    djidf.index=range(1,len(djidf)+1)
    
    '''

# -*- coding: utf-8 -*-
"""
Get quotesdf
 
@author: Dazhuang
"""
 
import requests
import re
import json
import pandas as pd
 
def retrieve_quotes_historical(stock_code):
    quotes = []
    url = 'https://finance.yahoo.com/quote/%s/history?p=%s' % (stock_code, stock_code)
    # % 输出模板类似于c
    r = requests.get(url)
    m = re.findall('"HistoricalPriceStore":{"prices":(.*?),"isPending"', r.text)
    if m:
        quotes = json.loads(m[0])
        quotes = quotes[::-1]
        # [::-1] -->[开始:结束:步速]
    return  [item for item in quotes if not 'type' in item]
    # 如果‘type’不在该item中，则返回item（quotes中的每一项）形成列表 
 
quotes = retrieve_quotes_historical('AXP')
quotesdf = pd.DataFrame(quotes)
# quotesdf = quotesdf_ori.drop(['unadjclose'], axis = 1)  原先的网站数据有 unadjclose 列，目前已删除
print(quotesdf)
'''
import datetime
list1 = []
for item in range(len(quotes)):
    date1 = datetime.date.fromtimestamp(quotes[item]['date'])
    date2 = datetime.date.strftime(date1,"%Y-%m-%d")
    list1.append(date2)
quotesdf = quotesdf.drop(['date'],axis=1)
quotesdf.index = list1
'''

'''
数据选择
1
.loc  .at  标签
2
.iloc  .iat 位置 (表示物理位置，左闭右开，如[1:5,]指的是第二行到第四行)
'a':'d':遍历abcd 1:4遍历123
3
条件筛选
df[(df.index>?)&()&()]
'''

'''
简单统计与筛选
np.sign() ---> 大于0 返回1，==0 返回0 ， 小于0 返回-1；
np.diff() 当前元素的后一个元素减去当前元素
np.where(condition[,x,y]) (三个数组,维度相同)：条件真返回x，假返回y
————————
只给条件则： （原句 If only condition is given, return the tuple condition.nonzero(), the indices where condition is True.）
  a,如：           （如果仅给出条件，则返回元组condition.nonzero（），其中条件为True的索引。）
np.where([[True, False], [True, True]],
         [[1, 2], [3, 4]], #x
         [[9, 8], [7, 6]]) #y
  结果：（根据条件的返回形式[真,假],[真,真]）【真假是从x角度看】位置上真填x，假填y(y此时为true)
array([[1, 8],
       [3, 4]])
  b，如：
        np.where([[0, 1], [1, 0]])
  结果：(array([0, 1]), array([1, 0]))
————————

***************
nonzeron(a) 返回数组中不为零（或false）的元素下标，返回值是元组(长a.ndim)，每一个值都是数组(array0,array1...)
其中array0是a中不为零（false）元素的 0轴下标， 以此类推，所以第一个不为零（false）元素应该是 返回值元组中 每个数组的 第一个（下标0）值 (array0[0],array1[0].....)【详细如下】

拓：array 用元素做下标 其实是取元组中 每一个数组值 的相同位置【where nonzero返回的都是这一类】
np.nonzero(?) = array_index = (array([1,2,3]),array([1,2,2]),array([2,3,4]),array([1,1,1]))
如上：array_a[array_index] 分别取 (1,1,2,1),(2,2,3,1),(3,2,4,1)
np.transpose(np.nonzero(?))可得到上述（以数组形式array([1,1,2,1],[],[]）
***************

sort_values(by=,ascending=False) #降序
sort_index

time.strftime(df.index[i],"%Y-%m-%d") #时间格式化（-）成字符串输出
time.strptime(df.index[i],"%Y-%m-%d") #字符串转成时间格式
'''