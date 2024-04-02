#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np


# In[2]:


df = pd.read_csv("../data/ASCII_2020/processeddataCA/processeddataCA/FACTPCRADDITIONALSYMPTOM_CA.csv", encoding= "UTF-8")
pd.set_option('display.max_columns', None)
df.head()


# In[3]:


df = df.rename(columns={"Unnamed: 0": "ID"})


# In[4]:


df.to_csv('../data/filtered_data/FACTPCRADDITIONALSYMPTOM_CA_filter.csv')





