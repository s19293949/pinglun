# -*- coding: utf-8 -*-
"""
Created on Tue Dec 25 14:11:20 2018

@author: Administrator
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Oct 10 10:47:24 2018

@author: Administrator
"""
import re
import pandas as pd
import jieba
import jieba.analyse
import jieba.posseg as pseg
import os
current_path=os.getcwd()
os.chdir(current_path)
from lstm_test import *

pos = pd.read_table('./data/pos_text.txt')
print('已导入正向词库')
neg = pd.read_table('./data/neg_text.txt')
print('已导入负向词库')
pos_list = pos.好评.values.tolist()
neg_list = neg.差评.values.tolist()
#发现某类特征
def discover_feature(data,key_list):
    '''
    提取关键词
    '''
    key_list1 = []
    for key in data:
        #句子根据标点符号分句
        keys = re.split('[，～。！？、,. ]',key)
        for i in keys:
            for keyword in key_list:
                if keyword in i:
                    try:
                        #re匹配关键词之后的字段
                        match=re.compile(r"(?<=%s).+" %keyword).search(i)
                        words = match.group()
                        words = pseg.cut(words)
                        for word,flag in words:
                            #匹配修饰词
                            if 'a' in flag  or flag == 'vd' or flag == 'l' or flag == 'z' :
                                word1 = keyword+str(word)
                                key_list1.append(word1)
                                break
                    except AttributeError:
                        pass
                    continue
    return key_list1
def jbj(data,key_list):
    '''
    找出某类关键词的评论
    '''
    data_list1 = []
    for i in data:
        for j in key_list:
            if j in i:
                data_list1.append(i)
    data_list1 = list(set(data_list1))
    return data_list1


def cut(data):
    '''
    分词
    '''
    data_cut=[]
    for i in range(0,len(data)):
        data_cut.append('/'.join(jieba.cut(data[i])).split('/'))
    return data_cut

def delect(data):
    '''
    删除模板评价
    '''
    query = '模板/积分/仙女/淘气值/没用/没有用/積分/繁荣昌盛/复制/年级/京东/网购/模块/闲鱼/领导/阿里巴巴/乾隆/复制粘贴/合格/村/燕窝/七经八脉/凑/年纪轻轻'
    query1 = query.split('/')
    for i in query1:
        bool = data.评价内容.str.contains(i)
        data = data[~bool]
    return data
def sentiment_mine(sen):
    '''
    评论舆情分析第一层算法
    '''
    pos_value = 0
    neg_value = 0
    try:
        for i in pos_list:
            if i in sen:
                pos_value +=1
        for j in neg_list:
            if j in sen:
                neg_value +=1
#        print(neg_value)
        if pos_value/neg_value > 1:
                return '好评'
        elif pos_value/neg_value <= 1:
                return '差评'
    except ZeroDivisionError:
        if pos_value>0:
            return '好评'
        return '其他'
def difference(left,right):
    '''
    对两个dataframe取差集
    '''
    left_list = left.评价内容.values.tolist()
    right_list = right.评价内容.values.tolist()
    final = []
    for i in left_list:
        if i not in right_list:
            final.append(i)
    df_final = pd.DataFrame(final,columns = ['评价内容'])
    return df_final

def sen(data_list):
    '''
    评论舆情分析第二层算法
    '''
    senti,sorce = get_lstm_result(data_list)
    c={"评价内容":data_list,"系数":senti}
    df = pd.DataFrame(c)
    pl_neg = df[['评价内容']][df['系数'] == 0]
    pl_pos = df[['评价内容']][df['系数'] == 1]
    return pl_pos,pl_neg



def keys_classification(data,text):
    '''
    评论舆情分析最终算法
    '''
    data_pos = []
    data_neg = []
    data_text = []
    for key in data:
        keys = re.split('[，～。！？、,. ]',key)
        for i in keys:
            for j in text:
                if j in i :
                    result = sentiment_mine(i)
                    if result == '好评':
                        data_pos.append(key)
                    elif result == '差评':
                        data_neg.append(key)
                    elif result == '中评':
                        try:
                            #re匹配关键词之后的字段
                            match=re.compile(r"(?<=%s).+" %j).search(i)
                            words = match.group()
                            results = sentiment_mine(words)
                            if results == '好评':
                                data_pos.append(key)
                            elif results == '差评':
                                data_neg.append(key)
                            elif results == '中评' or results == '其他':
                                data_text.append(key)
                        except AttributeError:
                            pass
                        continue
                    elif result == '其他':
                        data_text.append(key)

    df_pos = pd.DataFrame(data_pos,columns = ['评价内容'])
    df_neg = pd.DataFrame(data_neg,columns = ['评价内容'])
    pl_pos,pl_neg = sen(data_text)
    #整合评论
    df_pos = pd.concat([df_pos,pl_pos])
    df_neg = pd.concat([df_neg,pl_neg])
    #去重
    df_pos = pd.DataFrame.drop_duplicates(df_pos, subset='评价内容', keep='first', inplace=False)
    df_neg = pd.DataFrame.drop_duplicates(df_neg, subset='评价内容', keep='first', inplace=False)
    #取差集
    df_neg = difference(df_neg,df_pos)
    return df_pos,df_neg

def nokey(wupinglun):
    '''
    无主语评论处理
    '''
    data_pos = []
    data_neg = []
    data_text = []
    for key in wupinglun:
        result = sentiment_mine(key)
        if result == '好评':
            data_pos.append(key)
        elif result == '差评':
            data_neg.append(key)
        elif result == '中评' or result == '其他':
            data_text.append(key)
    df_pos = pd.DataFrame(data_pos,columns = ['评价内容'])
    df_neg = pd.DataFrame(data_neg,columns = ['评价内容'])

    pl_pos,pl_neg = sen(data_text)
    df_pos = pd.concat([df_pos,pl_pos])
    df_neg = pd.concat([df_neg,pl_neg])
    df_pos = pd.DataFrame.drop_duplicates(df_pos, subset='评价内容', keep='first', inplace=False)
    df_neg = pd.DataFrame.drop_duplicates(df_neg, subset='评价内容', keep='first', inplace=False)
    return df_pos,df_neg
def list_sum(list1):
    num = 0
    for i in list1:
        num = num+i
    return num
def clss_list(dic_all,jj):
    num = 0
    list_big = []
    dic1 = {}
    for i in range(len(jj)):
        exec('a%s = []' % i)
        for j in range(2):
            exec('a%s.append(dic_all[%s][1])'%(i,num))
            num +=1
        exec('a%s.insert(0,list_sum(a%s))'%(i,i))
        exec('list_big.append(a%s)'%i)
    for t,p in zip(list_big, jj):
        dic1.update({p:t})
    return dic1