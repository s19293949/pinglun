# -*- coding: utf-8 -*-
"""
Created on Wed Nov 14 09:53:31 2018

@author: Administrator
"""
import shutil
import pandas as pd
import os 
current_path=os.getcwd()
os.chdir(current_path)

'''
删除并创建新的文件夹
'''
def Create_folder():
    #删除原有文件
    file_name = os.listdir('./评论分析')
    if file_name != []:
        print('正在删除原有文件........')
        for i in file_name:
            try:
                os.remove("./评论分析/%s"%(i))
            except Exception as e:
                shutil.rmtree('./评论分析/%s'%(i))
                pass
        print('删除成功........')
    #创建新的文件
    file_name_replace = [i.replace('.xlsx','') for i in os.listdir('./评论')]
    print('创建新文件........')
    for i in file_name_replace:
    	os.makedirs('./评论分析/%s'%(i))
    for i in file_name_replace:
        for j in ['质量','物流','颜值','商品','价格','无主语评价','客服','未分类评价','气味','未使用','全部评价']:
            os.makedirs('./评论分析/%s/%s'%(i,j))
    return file_name_replace
    print('新文件创建完成........')

