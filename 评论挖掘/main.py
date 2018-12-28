# -*- coding: utf-8 -*-
"""
Created on Fri Dec 28 14:19:15 2018

@author: Administrator
"""

import os
current_path=os.getcwd()
os.chdir(current_path)
import Createfolder
import Keys_Classification




if __name__=="__main__":
    file_list = Createfolder.Create_folder()
    Keys_Classification.result(file_list)