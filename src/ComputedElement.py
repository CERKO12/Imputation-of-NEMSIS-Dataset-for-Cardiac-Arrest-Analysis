#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# In[2]:


df = pd.read_csv("../data/ASCII_2020/processeddataCA/processeddataCA/ComputedElements_CA.csv", encoding= "UTF-8")
pd.set_option('display.max_columns', None)


# In[3]:


df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)
df.replace({'': pd.NA, '.': pd.NA}, inplace=True)


# In[4]:


null_counts = df.isnull().sum()
print(null_counts)


# In[5]:


missing_percentage = df.isnull().mean() * 100
print(missing_percentage)


# In[6]:


# Filter columns with missing percentage over 40%
missing_series = pd.Series(missing_percentage)
cols_to_drop = missing_series[missing_series > 40].index.tolist()
df = df.drop(columns=cols_to_drop)


# In[7]:


# Count the occurrences of each category
category_counts = df['USCensusRegion'].value_counts()

plt.figure(figsize=(8, 4))
category_counts.plot(kind='bar')
plt.title('USCensusRegion Distribution')
plt.xlabel('Categories')
plt.ylabel('Frequency')
plt.xticks(rotation=0)
plt.savefig('../fig/USCensusRegion_Distribution.png')
plt.show()


# In[8]:


# Count the occurrences of each category
category_counts = df['USCensusDivision'].value_counts()

plt.figure(figsize=(15, 8))
category_counts.plot(kind='bar')
plt.title('USCensusDivision Distribution')
plt.xlabel('Categories')
plt.ylabel('Frequency')
plt.xticks(rotation=0)
plt.savefig('../fig/USCensusDivision_Distribution.png')
plt.show()


# In[9]:


# Count the occurrences of each category
category_counts = df['NasemsoRegion'].value_counts()

plt.figure(figsize=(8, 4))
category_counts.plot(kind='bar')
plt.title('NasemsoRegion Distribution')
plt.xlabel('Categories')
plt.ylabel('Frequency')
plt.xticks(rotation=0)
plt.savefig('../fig/NasemsoRegion_Distribution.png')
plt.show()


# In[10]:


# Count the occurrences of each category
category_counts = df['Urbanicity'].value_counts()

plt.figure(figsize=(8, 4))
category_counts.plot(kind='bar')
plt.title('Urbanicity Distribution')
plt.xlabel('Categories')
plt.ylabel('Frequency')
plt.xticks(rotation=0)
plt.savefig('../fig/Urbanicity_Distribution.png')
plt.show()


# In[11]:


cols_to_impute_con = ["ageinyear","EMSDispatchCenterTimeSec",
                      "EMSChuteTimeMin","EMSSystemResponseTimeMin",
                      "EMSSceneResponseTimeMin","EMSSceneToPatientTimeMin",
                      "EMSTotalCallTimeMin"]
cols_to_impute_cat = ["USCensusRegion","USCensusDivision","NasemsoRegion","Urbanicity"]


# In[12]:


df = df.rename(columns={"Unnamed: 0": "ID"})


# In[13]:


col_int = ["ageinyear","EMSDispatchCenterTimeSec"]
col_float = ["EMSChuteTimeMin","EMSSystemResponseTimeMin",
             "EMSSceneResponseTimeMin","EMSSceneToPatientTimeMin",
             "EMSTotalCallTimeMin"]


# In[14]:


df = df.replace({pd.NA: np.nan})

df[col_int] = df[col_int].astype('Int64')
df[col_float] = df[col_float].astype('float64')


# In[15]:


for col in df.columns:
    if df[col].dtype == 'float64':
        df[col] = df[col].round(2)


# In[16]:


df.to_csv('../data/filtered_data/ComputedElement_filter.csv')




