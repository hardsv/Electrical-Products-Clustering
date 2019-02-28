# -*- coding: utf-8 -*-
"""
Created on Thu Sep 20 14:30:39 2018

@author: Shishir
"""

import pandas as pd
from pandas import concat
import matplotlib.pyplot as plt
import numpy as np

filename_out = 'Système_domotique_with_clusters.csv'
filename_in = 'Système_domotique_workable.csv'

# Return the Hamming distance between string1 and string2.
# string1 and string2 should be the same length.
def hamming_distance(string1, string2): 
    # Start with a distance of zero, and count up
    distance = 0
    # Loop over the indices of the string
    L = len(string1)
    for i in range(L):
        # Add 1 to the distance if these two characters are not equal
        if string1[i] != string2[i]:
            distance += 1
    # Return the final count of differences
    return distance

df = pd.read_csv(filename_in, engine='python',encoding = "ISO-8859-1", index_col = 0)
#Removing Products with NO tech parameters 
df_drop = df[df.non != 'non']
df_drop = df_drop.drop(['non'], axis =1)

#Removing Product Name Columns 
df_drop = df_drop.drop(['product_name'], axis =1)
#X = df_drop.iloc[:,:].values
#Z = pd.DataFrame(X)

#Drop Vendor Name
df_drop_temp = df_drop.drop(['vendor_name'], axis =1)

#Convert DF to boolean
df_drop_temp2 = df_drop_temp.fillna('NA')
df_drop_temp2[df_drop_temp2 != 'NA'] = 1 
df_drop_temp2 = df_drop_temp2.replace('NA',0)
#df_drop_temp = df_drop_temp.astype('bool')
X = df_drop_temp2.iloc[:,:].values
#Convert to Strings
#vals = pd.DataFrame(index=df_drop_temp2.index)
x = df_drop_temp2.to_string(header=False, index=False, index_names=False).split('\n')

vals = pd.DataFrame([''.join(ele.split()) for ele in x])
vals = concat([df_drop_temp2, vals.set_index(df_drop_temp2.index[:len(vals)])], axis=1)
vals = vals[0]
df_drop_temp3 = df_drop_temp2

##Test Model
no_of_clusters = 90
#Applyting k-means to the dataset
from sklearn.cluster import KMeans
kmeans = KMeans(n_clusters = no_of_clusters, init = 'k-means++', max_iter =300, n_init =10, random_state =0)
y_kmeans = kmeans.fit_predict(df_drop_temp3)

y_kmeans_indexed = pd.DataFrame(index=df_drop_temp3.index)
y_kmeans_indexed[0] = y_kmeans
y_kmeans_indexed.columns = ['kmeans_clusters']

from sklearn.cluster import KMeans
kmeans = KMeans(n_clusters = no_of_clusters, init = 'random', max_iter =300, n_init =10, random_state =0)
y_kmeans_random = kmeans.fit_predict(df_drop_temp3)

y_kmeans_random_indexed = pd.DataFrame(index=df_drop_temp3.index)
y_kmeans_random_indexed[0] = y_kmeans_random
y_kmeans_random_indexed.columns = ['kmeans_random_clusters']
# End KMeans

#fitting HC in data set
from sklearn.cluster import AgglomerativeClustering
hc = AgglomerativeClustering(n_clusters = no_of_clusters, affinity = 'euclidean', linkage = 'ward' )
y_hc = hc.fit_predict(df_drop_temp3)

y_hc_indexed = pd.DataFrame(index=df_drop_temp3.index)
y_hc_indexed[0] = y_hc
y_hc_indexed.columns = ['hierarchical_clusters']
# End HC
##Test model End

df_to_write = pd.concat([y_hc_indexed,y_kmeans_indexed,y_kmeans_random_indexed,df_drop], axis = 1)
df_to_write.to_csv(filename_out)
















##df_drop_temp3['my_sum'] = df_drop_temp3.iloc[:,:].sum(1)
#
## select numeric columns and calculate the sums
#sums = df_drop_temp3.select_dtypes(include=['number']).sum().rename('total')
#
#
###Check HammingDistance 
#HD_mat = pd.DataFrame(np.zeros((vals.shape[0], vals.shape[0])),index = vals.index)
#for row, index in HD_mat.iterrows():
##    print(index)
#    for x in range(HD_mat.shape[0]):
#        HD_mat.at[row,x] = hamming_distance(vals[x],vals[row])
#
##HD_mat1  = HD_mat
#HD_mat.columns  = HD_mat.index


















#df_drop_temp4 = df_drop_temp2.T.drop_duplicates().T 
df_drop_temp3 = df_drop_temp2[df_drop_temp2.duplicated(keep=False)]

df_drop_temp5 = df_drop_temp3.sort_values(by=list(df_drop_temp3.columns),axis=0)

df_drop_temp_total = df_drop_temp5.sum(axis=1)
df_drop_temp5.insert(0,'Total', df_drop_temp_total)







