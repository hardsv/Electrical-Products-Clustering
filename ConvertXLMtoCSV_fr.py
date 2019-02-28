# -*- coding: utf-8 -*-
"""
Created on Thu Aug 30 15:08:29 2018

@author: Shishir
"""
import pandas as pd
import xml.etree.cElementTree as et

filename_in = 'Système_domotique.xml'
filename_out = 'Système_domotique.csv'

with open(filename_in) as filein, open('fout.xml','w') as fileout:
    for line in filein:
        line=line.replace("'","")
        fileout.write(line)

parsedXML = et.parse( 'fout.xml' )
dfcols = ['ref_rexel','vendor_name','product_name','product_cat','tech_name','tech_value']
dfcols_notechs = ['ref_rexel','vendor_name','product_name']
df_appended = pd.DataFrame(columns=dfcols)
df_appended_notechs = pd.DataFrame(columns=dfcols_notechs)
def getvalueofnode( node ):
    return node.text if node is not None else None
for node in parsedXML.getroot():
    ref_rexel = node.find('ref_rexel')
    vendor_name = node.find('vendor_name') 
    product_name = node.find('product_name')
    product_cat = node.find('product_cat')
    tech_name = node.find('tech_name')
    tech_value = node.find('tech_value') 
    if getvalueofnode(tech_name):
        if getvalueofnode(product_cat):         
            df_appended = df_appended.append( pd.Series(
                [getvalueofnode(ref_rexel), getvalueofnode(vendor_name), getvalueofnode(product_name), getvalueofnode(product_cat), getvalueofnode(tech_name), getvalueofnode(tech_value).replace("'",'')],
                index=dfcols) ,ignore_index=True) 
        else:
            df_appended = df_appended.append( pd.Series(
                [getvalueofnode(ref_rexel), getvalueofnode(vendor_name), getvalueofnode(product_name),"no_cat", getvalueofnode(tech_name), getvalueofnode(tech_value).replace("'",'')],
                index=dfcols) ,ignore_index=True)
    elif not tech_name:
        df_appended = df_appended.append( pd.Series(
                [getvalueofnode(ref_rexel), getvalueofnode(vendor_name), getvalueofnode(product_name), "unknown","non", "non" ],
                index=dfcols) ,ignore_index=True)

df_duplicated = df_appended.duplicated() 
df_appended = df_appended.drop_duplicates()
df_appended['tech_details'] = df_appended[['tech_name','tech_value']].apply(lambda x: ':'.join(x), axis=1)
df1 = df_appended.drop(['tech_name','tech_value'],axis =1)
df1 = df1.groupby(['vendor_name','product_name','ref_rexel','product_cat']).agg(lambda x: tuple(x)).applymap(list).reset_index()

##Remove NULL featers products

##End NULL


df1.to_csv(filename_out)
#df1.to_csv(filename_out, index=False)