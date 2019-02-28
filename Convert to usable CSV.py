# -*- coding: utf-8 -*-
"""
Created on Sat Sep  1 18:00:52 2018

@author: Shishir
"""
import pandas as pd
import re
import numpy as np

filename_in = 'Système_domotique.csv'
filename_out = 'Système_domotique_workable.csv'

with open(filename_in) as filein, open('fout_workable.csv','w') as fileout:
    for line in filein:
        line=line.replace('«', '')
        line=line.replace('»', '')
        line=line.replace('\\xa0', '')
        fileout.write(line)

dataset = pd.read_csv('fout_workable.csv', engine='python', encoding = "ISO-8859-1")
dataset1 = dataset.drop(dataset.columns[[0]], axis=1)
dataset_tech_details = dataset1['tech_details']
dataset_product_name = dataset1['product_name']
dataset_vendors = dataset1[['ref_rexel','vendor_name', 'product_name','product_cat']]
#dataset_vendors = dataset1[['ref_rexel','vendor_name', 'product_name']]
dataset3 = dataset1.iloc[0,2:-2].to_frame().transpose()

for index, t_data in dataset1.iterrows():
    single_param_list = re.findall(r"'(.*?)'", t_data['tech_details'], re.DOTALL)
    single_param_list = np.array([x.replace("'",'') for x in single_param_list])
    single_param_transpose = np.array([x.split(':') for x in single_param_list])
    # To memove duplicate feature names... it will also remove values which may be duplicate or not
    unique_keys, indices = np.unique(single_param_transpose[:,0], return_index=True)
    single_param_transpose = single_param_transpose[indices]
    single_param_matrix = single_param_transpose.transpose()
    df = pd.DataFrame(single_param_matrix)
    header = df.iloc[0]
    df = df[1:]
    single_param_matrix_df = df.rename(columns = header)
    single_param_matrix_df.insert(0, column = 'ref_rexel', value= t_data['ref_rexel'])
    dataset3 = dataset3.merge(single_param_matrix_df, how='outer', sort = 'False')

dataset_to_write = dataset_vendors.merge(dataset3, on = 'ref_rexel')
dataset_to_write.to_csv(filename_out, index=False)