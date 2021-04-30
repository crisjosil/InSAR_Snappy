# -*- coding: utf-8 -*-
"""
Created on Fri Apr 23 15:50:35 2021

@author: crisj
"""


import json
import subprocess
import os
import time

#filename_1 = os.path.join(r'D:\PhD Info\InSAR\Examples\Ecuador_Galapagos','S1A_IW_SLC__1SDV_20170319T002614_20170319T002644_015753_019EFB_FA12.zip')
#filename_2 = os.path.join(r'D:\PhD Info\InSAR\Examples\Ecuador_Galapagos','S1A_IW_SLC__1SDV_20170331T002615_20170331T002645_015928_01A42E_7662.zip')
#out_filename =os.path.join(r'D:\PhD Info\InSAR\Examples\SNAPPY_Ecuador_Galapagos','InSAR_pipeline_I')
#
#IW='IW3'
#firstBurstIndex = 1
#lastBurstIndex = 4
# Extract dates
path='D:\PhD Info\InSAR\Examples\Ecuador_Galapagos'
name1='S1A_IW_SLC__1SDV_20170319T002614_20170319T002644_015753_019EFB_FA12.zip'
name2='S1A_IW_SLC__1SDV_20170331T002615_20170331T002645_015928_01A42E_7662.zip'
filename_1=os.path.join(path,name1)
filename_2=os.path.join(path,name1)

def get_date_name(name1,name2):
    date1=name1.split(sep='_')
    date1=date1[5].split(sep='T')
    date1=date1[0]
    
    date2=name2.split(sep='_')
    date2=date2[5].split(sep='T')
    date2=date2[0]
    
    return (date1+'_'+date2)

date_name=get_date_name(name1,name2)
print(date_name)
#%%
print ('Pipeline I ...')
mydict =  dict(
     pipeline ='I',
     filename_1=filename_1,
     filename_2=filename_2,
     out_filename=os.path.join(r'D:\PhD Info\InSAR\Examples\SNAPPY_Ecuador_Galapagos','InSAR_pipeline_I'),
     IW='IW3',
     firstBurstIndex=1,
     lastBurstIndex=4,
     in_filename = os.path.join(r'D:\PhD Info\InSAR\Examples\SNAPPY_Ecuador_Galapagos','InSAR_pipeline_I'),
     ML_nRgLooks=6,
     out_filename_II=os.path.join(r'D:\PhD Info\InSAR\Examples\SNAPPY_Ecuador_Galapagos','InSAR_pipeline_II'),

)
mydict_str = json.dumps(mydict)   # encode dictionnary to json string
pipeline_out = subprocess.check_output(['python', 'InSAR_Pipeline.py', mydict_str], stderr=subprocess.STDOUT)
#%%
print ('Pipeline II ...')
# 18 minutes
start = time.time()
mydict =  dict(
     pipeline ='II',
     filename_1=os.path.join(r'D:\PhD Info\InSAR\Examples\Ecuador_Galapagos','S1A_IW_SLC__1SDV_20170319T002614_20170319T002644_015753_019EFB_FA12.zip'),
     filename_2=os.path.join(r'D:\PhD Info\InSAR\Examples\Ecuador_Galapagos','S1A_IW_SLC__1SDV_20170331T002615_20170331T002645_015928_01A42E_7662.zip'),
     out_filename=os.path.join(r'D:\PhD Info\InSAR\Examples\SNAPPY_Ecuador_Galapagos','InSAR_pipeline_I'),
     IW='IW3',
     firstBurstIndex=1,
     lastBurstIndex=4,
     in_filename = os.path.join(r'D:\PhD Info\InSAR\Examples\SNAPPY_Ecuador_Galapagos','InSAR_pipeline_I.dim'),
     ML_nRgLooks=6,
     out_filename_II=os.path.join(r'D:\PhD Info\InSAR\Examples\SNAPPY_Ecuador_Galapagos','InSAR_pipeline_II')
)
mydict_str = json.dumps(mydict)   # encode dictionnary to json string
pipeline_out = subprocess.check_output(['python', 'InSAR_Pipeline.py', mydict_str], stderr=subprocess.STDOUT)
end = time.time()
print("--- %s seconds ---" % (end - start))
#%%
print ('Pipeline III ...')
# 16 minutes
start = time.time()
mydict =  dict(
     pipeline ='III',
     in_filename_III = os.path.join(r'D:\PhD Info\InSAR\Examples\SNAPPY_Ecuador_Galapagos','InSAR_pipeline_II.dim'),
     out_filename_III= os.path.join(r'D:\PhD Info\InSAR\Examples\SNAPPY_Ecuador_Galapagos',date_name))
mydict_str = json.dumps(mydict)   # encode dictionnary to json string
pipeline_out = subprocess.check_output(['python', 'InSAR_Pipeline.py', mydict_str], stderr=subprocess.STDOUT)
end = time.time()
print("--- %s seconds ---" % (end - start))