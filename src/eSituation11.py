#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np


# In[2]:


df = pd.read_csv("../data/ASCII_2020/processeddataCA/processeddataCA/FACTPCRPRIMARYIMPRESSION_CA.csv", encoding= "UTF-8")
pd.set_option('display.max_columns', None)


# In[3]:


df = df.rename(columns={"Unnamed: 0": "ID"})


# In[4]:


df = df.astype(str)

df.replace({
    r'\s*Not\s+Recorded\s*': np.nan, 
    r'\s*Not\s+Applicable\s*': np.nan,
    r'\s*Unknown\s*': np.nan,
    r'\s*7701001\s*': np.nan,
    r'\s*7701003\s*': np.nan
}, regex=True, inplace=True)


# In[5]:


df.to_csv('../data/filtered_data/FACTPCRPRIMARYIMPRESSION_CA_filter.csv')




