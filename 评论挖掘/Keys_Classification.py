# -*- coding: utf-8 -*-
"""
Created on Sat Oct 20 15:50:18 2018

@author: Administrator
"""


import pandas as pd
import os
current_path=os.getcwd()
os.chdir(current_path)
from discover_feature_new import *



def result(id_list):
    global jj
    jj = ['全部评价','质量','颜值','物流','客服','商品','价格','无主语','未使用','气味','未分类']
    for spID in id_list:
        data = pd.read_excel('./评论//%s.xlsx'%spID,encoding = 'UTF-8')
        data1 = pd.DataFrame.drop_duplicates(data[['评价内容']], subset=None, keep='first', inplace=False)
        data1.dropna(axis=0, how='any', inplace=True)
        data1 = delect(data1)
        global data_list    
        data_list = data1.评价内容.values.tolist()
        df_all = pd.DataFrame(columns = ['评价内容'])
        df_pl_all = pd.DataFrame()
        dic_all = {
                '全部评价好评数':None,
                '全部评价差评数':None,
                '质量好评数':None,
                '质量差评数':None,
                '颜值好评数':None,
                '颜值差评数':None,
                '物流好评数':None,
                '物流差评数':None,
                '客服好评数':None,
                '客服差评数':None,
                '商品好评数':None,
                '商品差评数':None,
                '价格好评数':None,
                '价格差评数':None,
                '无主语好评数':None,
                '无主语差评数':None,
                '未使用好评数':None,
                '未使用差评数':None,
                '气味好评数':None,
                '气味差评数':None,
                '未分类好评数':None,
                '未分类差评数':None,
                }
        dic_cf = {
               '质量':['质量','品质','质地','材质'],
               '颜值':['外观','造型','颜值','色','样子','外形','漂亮','可爱'],
               '物流':['快递','物流','发货','包装'],
               '客服':['客服'],
               '商品':['东西','宝贝','商品','产品'],
               '价格':['价','贵','便宜'],
               '未使用':['囤货','没用','送人','没使用','没有用','备货']
               }
    
        for key in dic_cf:
            text = dic_cf[key]
            data_zl = jbj(data_list,text)                      #找出某类评论
            df_pos,df_neg = keys_classification(data_zl,text)  #情感判断
            df_neg1 = df_neg.copy()
            df_neg1.columns = ['%s差评'%(key)]
            df_pl_all = pd.concat([df_pl_all,df_neg1],axis=1) 
            dic_all['%s好评数'%key] = len(df_pos)
            dic_all['%s差评数'%key] = len(df_neg)
            df_all = pd.concat([df_all,df_pos])
            df_all = pd.concat([df_all,df_neg])
            writer = pd.ExcelWriter('./评论分析//%s//%s//%s好评.xlsx'%(spID,key,key))
            df_pos.to_excel(writer,'sheet1')
            writer.save()
            writer = pd.ExcelWriter('./评论分析//%s//%s//%s差评.xlsx'%(spID,key,key))
            df_neg.to_excel(writer,'sheet1')
            writer.save()
            print('已完成%s评价'%(key))
        wupinglun = []
        for i in data_list:
            words = pseg.cut(i)
            qq = []
            for word,flag in words:
                qq.append(flag)
            if 'n' not in qq and 'ns' not in qq and 'an' not in qq and  'ng' not in qq and  'nr' not in qq and  'r' not in qq:
                wupinglun.append(i)
        df_pos,df_neg = nokey(wupinglun)
        df_neg1 = df_neg.copy()
        df_neg1.columns = ['无主语差评']
        df_neg1 = df_neg1.reset_index(drop = True)
        df_pl_all = pd.concat([df_pl_all,df_neg1],axis=1)
        df_all = pd.concat([df_all,df_pos])
        df_all = pd.concat([df_all,df_neg])
        dic_all['无主语好评数'] = len(df_pos)
        dic_all['无主语差评数'] = len(df_neg)    
        writer = pd.ExcelWriter('./评论分析//%s//无主语评价//无主语好评.xlsx'%spID)
        df_pos.to_excel(writer,'sheet1')
        writer.save()
        writer = pd.ExcelWriter('./评论分析//%s//无主语评价//无主语差评.xlsx'%spID)
        df_neg.to_excel(writer,'sheet1')
        writer.save()
        print('已完成无主语评价')
        qw = jbj(data_list,['味'])
        pos = []
        neg = []
        for key in qw:
            keys = re.split('[，～。！？、,. ]',key)
            for i in keys:
                if '味' in i:
                    if '无' in i or '没' in i:
                        pos.append(key)
                    else:
                        neg.append(key)
        pos = list(set(pos))
        neg = list(set(neg))
        df_pos = pd.DataFrame(pos,columns = ['评价内容'])
        df_neg = pd.DataFrame(neg,columns = ['评价内容'])
        df_neg1 = df_neg.copy()
        df_neg1.columns = ['气味差评']
        df_pl_all = pd.concat([df_pl_all,df_neg1],axis=1)
        df_all = pd.concat([df_all,df_pos])
        df_all = pd.concat([df_all,df_neg])
        dic_all['气味好评数'] = len(df_pos)
        dic_all['气味差评数'] = len(df_neg)    
        writer = pd.ExcelWriter('./评论分析//%s//气味//气味好评.xlsx'%spID)
        df_pos.to_excel(writer,'sheet1')
        writer.save()
        writer = pd.ExcelWriter('./评论分析//%s//气味//气味差评.xlsx'%spID)
        df_neg.to_excel(writer,'sheet1')
        writer.save()
        print('已完成气味评价')
        all_list = df_all['评价内容'].values.tolist() 
        all_list = list(set(all_list))
        final = []
        for i in data_list:
            if i not in all_list:
                final.append(i)
        df_pos,df_neg = nokey(final)
        df_neg1 = df_neg.copy()
        df_neg1.columns = ['未分类差评']
        df_neg1 = df_neg.reset_index(drop = True)
        df_pl_all = pd.concat([df_pl_all,df_neg1],axis=1)    
        dic_all['未分类好评数'] = len(df_pos)
        dic_all['未分类差评数'] = len(df_neg)
        writer = pd.ExcelWriter('./评论分析//%s//未分类评价//未分类好评.xlsx'%spID)
        df_pos.to_excel(writer,'sheet1')
        writer.save()
        writer = pd.ExcelWriter('./评论分析//%s//未分类评价//未分类差评.xlsx'%spID)
        df_neg.to_excel(writer,'sheet1')
        print('已完成未分类评价')
        df_pos,df_neg = nokey(data_list)
    
    
        dic_all['全部评价好评数'] = len(df_pos)
        dic_all['全部评价差评数'] = len(df_neg)
        writer = pd.ExcelWriter('./评论分析//%s//全部评价//全部好评.xlsx'%spID)
        df_pos.to_excel(writer,'sheet1')
        writer.save()
        writer = pd.ExcelWriter('./评论分析//%s//全部评价//全部差评.xlsx'%spID)
        df_neg.to_excel(writer,'sheet1')
        writer.save()
        dic_all = list(dic_all.items())
        dic1 = clss_list(dic_all,jj)   #统计数据
        df_fk = pd.DataFrame(dic1)
        df_fk.index = ['全部评价数','好评数','差评数']
        df_fk.loc['差评率'] = [df_fk.iloc[2,i]/df_fk.iloc[0,i] for i in range(len(jj))]
        df_fk.loc['占比'] = [df_fk.iloc[0,i]/df_fk.iloc[0,0] for i in range(len(jj))]
        writer = pd.ExcelWriter('./评论分析//%s//%s商品概括.xlsx'%(spID,spID))
        df_fk.to_excel(writer,'sheet1')
        writer.save()
        writer = pd.ExcelWriter('./评论分析//%s//%s差评汇总.xlsx'%(spID,spID))
        df_pl_all.to_excel(writer,'sheet1')
        writer.save()

