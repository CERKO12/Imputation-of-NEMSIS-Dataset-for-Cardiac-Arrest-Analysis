#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import rpy2.robjects as robjects
from rpy2.robjects.packages import importr


# In[2]:


df_CE = pd.read_csv('../data/filtered_data/ComputedElement_filter.csv', encoding= "UTF-8", index_col=0)
df_CE = df_CE.drop('ID', axis=1)

df_Event = pd.read_csv('../data/filtered_data/PCR_Event_filter.csv', encoding= "UTF-8", index_col=0)
df_Event = df_Event.drop('ID', axis=1)

df_merge = pd.merge(df_CE, df_Event, on=['PcrKey'])


# In[3]:


cols_to_drop_merge = ['eArrest_11', 'eArrest_14']
df_merge = df_merge.drop(cols_to_drop_merge, axis=1)


# In[4]:


df_encode = df_merge.copy()

cat_columns = ['eSituation_01','eTimes_01','eTimes_03', 'eScene_09', 
               'eTimes_05','eTimes_06','eTimes_07','eTimes_13',
               'USCensusRegion','USCensusDivision','NasemsoRegion','Urbanicity']

for col in cat_columns:
    df_encode[col] = df_encode[col].astype('category').cat.codes

df_encode.replace({col: {-1: np.nan} for col in cat_columns}, inplace=True)


# In[5]:


sample_df = df_encode.sample(n=40000, random_state=42)

data_for_r = {}
for col_name, col_data in sample_df.items():
    is_na = col_data.isna()
    col_data = col_data.astype(str)
    col_data[is_na] = robjects.NA_Character
    data_for_r[col_name] = robjects.StrVector(col_data)

rdf_sample = robjects.DataFrame(data_for_r)


# In[6]:


naniar = importr('naniar')
result = naniar.mcar_test(rdf_sample)

print(result)


# In[ ]:




