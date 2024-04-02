#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# In[2]:


df = pd.read_csv("../data/ASCII_2020/processeddataCA/processeddataCA/Pub_PCREvents_CA.csv", encoding= "UTF-8")
pd.set_option('display.max_columns', None)


# In[3]:


df = df.astype(str)

df.replace({
    r'\s*Not\s+Recorded\s*': np.nan, 
    r'\s*Not\s+Applicable\s*': np.nan,
    r'\s*Unknown\s*': np.nan,
    r'\s*7701001\s*': np.nan,
    r'\s*7701003\s*': np.nan
}, regex=True, inplace=True)


# In[4]:


null_counts = df.isnull().sum()
print(null_counts)


# In[5]:


df['eOutcome_01'] = df['eOutcome_01'].fillna('7701003')
df['eOutcome_02'] = df['eOutcome_02'].fillna('7701003')


# In[6]:


missing_percentage = df.isnull().mean() * 100
print(missing_percentage)


# In[7]:


missing_percentage.sort_values(ascending=False).plot(kind='bar', figsize=(12,7))
plt.title('Percentage of Missing Values by Column')
plt.ylabel('Percentage')
plt.savefig('../fig/Percentage_of_Missing_Values_by_Column.png')
plt.show()


# In[8]:


missing_series = pd.Series(missing_percentage)
cols_to_drop = missing_series[missing_series > 40].index.tolist()

df = df.drop(columns=cols_to_drop)


# In[9]:


# Count the occurrences of each category
category_counts = df['ePatient_13'].value_counts()


plt.figure(figsize=(8, 4))
category_counts.plot(kind='bar')
plt.title('ePatient_13 Distribution')
plt.xlabel('Categories')
plt.ylabel('Frequency')
plt.xticks(rotation=0)
plt.savefig('../fig/ePatient_13_Distribution.png')
plt.show()


# In[10]:


def fill_custom_proportions(column_name, value1, proportion1, value2, proportion2):
    
    num_nans = df[column_name].isna().sum()

    allocation1 = int(num_nans * proportion1)
    allocation2 = num_nans - allocation1

    nan_indices = df[df[column_name].isna()].index
    chosen_indices1 = np.random.choice(nan_indices, size=allocation1, replace=False)
    df.loc[chosen_indices1, column_name] = float(value1)

    chosen_indices2 = list(set(nan_indices) - set(chosen_indices1))
    df.loc[chosen_indices2, column_name] = float(value2)

    df[column_name] = df[column_name].astype('int64')

fill_custom_proportions('ePatient_13', '9906003', 0.60, '9906001', 0.40)


# In[11]:


# Count the occurrences of each category
category_counts = df['ePatient_16'].value_counts()

plt.figure(figsize=(8, 4))
category_counts.plot(kind='bar')
plt.title('ePatient_16 Distribution')
plt.xlabel('Categories')
plt.ylabel('Frequency')
plt.xticks(rotation=0)
plt.savefig('../fig/ePatient_16_Distribution.png')
plt.show()


# In[12]:


# Count the occurrences of each category
category_counts = df['eScene_06'].value_counts()

plt.figure(figsize=(8, 4))
category_counts.plot(kind='bar')
plt.title('eScene_06 Distribution')
plt.xlabel('Categories')
plt.ylabel('Frequency')
plt.xticks(rotation=0)
plt.savefig('../fig/eScene_06_Distribution.png')
plt.show()


# In[13]:


# Count the occurrences of each category
category_counts = df['eScene_07'].value_counts()

plt.figure(figsize=(8, 4))
category_counts.plot(kind='bar')
plt.title('eScene_07 Distribution')
plt.xlabel('Categories')
plt.ylabel('Frequency')
plt.xticks(rotation=0)
plt.savefig('../fig/eScene_07_Distribution.png')
plt.show()


# In[14]:


mode_ePatient_16 = df['ePatient_16'].mode()[0]
df['ePatient_16'].fillna(mode_ePatient_16, inplace=True)

mode_eScene_06 = df['eScene_06'].mode()[0]
df['eScene_06'].fillna(mode_eScene_06, inplace=True)

mode_eScene_07 = df['eScene_07'].mode()[0]
df['eScene_07'].fillna(mode_eScene_07, inplace=True)


# In[15]:


# Count the occurrences of each category
category_counts = df['eResponse_07'].value_counts()

plt.figure(figsize=(15, 5))
category_counts.plot(kind='bar')
plt.title('eResponse_07 Distribution')
plt.xlabel('Categories')
plt.ylabel('Frequency')
plt.xticks(rotation=0)
plt.savefig('../fig/eResponse_07_Distribution.png')
plt.show()


# In[16]:


mode_eResponse_07 = df['eResponse_07'].mode()[0]
df['eResponse_07'].fillna(mode_eResponse_07, inplace=True)


# In[17]:


# Count the occurrences of each category
category_counts = df['eSituation_07'].value_counts()

plt.figure(figsize=(10, 4))
category_counts.plot(kind='bar')
plt.title('eSituation_07 Distribution')
plt.xlabel('Categories')
plt.ylabel('Frequency')
plt.xticks(rotation=0)
plt.savefig('../fig/eSituation_07_Distribution.png')
plt.show()


# In[18]:


# Count the occurrences of each category
category_counts = df['eSituation_08'].value_counts()

plt.figure(figsize=(15, 8))
category_counts.plot(kind='bar')
plt.title('eSituation_08 Distribution')
plt.xlabel('Categories')
plt.ylabel('Frequency')
plt.xticks(rotation=0)
plt.savefig('../fig/eSituation_08_Distribution.png')
plt.show()


# In[19]:


def fill_na_proportionally(column_name):
    
    value_counts = df[column_name].value_counts()

    # Get the first and second most common values and their counts
    top_values = value_counts.index[:2].astype(float)
    top_counts = value_counts.iloc[:2]

    if len(top_values) == 2:
        print(f"First mode value for {column_name}: {top_values[0]}")
        print(f"Second mode value for {column_name}: {top_values[1]}")
    elif len(top_values) == 1:
        print(f"Only one mode value for {column_name}: {top_values[0]}")
    else:
        print(f"No mode values found for {column_name}")
        return

    total_counts = top_counts.sum()
    proportions = top_counts / total_counts

    num_nans = df[column_name].isna().sum()

    nan_allocations = (num_nans * proportions).astype(int)
    nan_indices = df[df[column_name].isna()].index

    # Fill NaNs for each top value
    for value, allocation in zip(top_values, nan_allocations):
        chosen_indices = np.random.choice(nan_indices, size=allocation, replace=False)
        df.loc[chosen_indices, column_name] = float(value)
        nan_indices = list(set(nan_indices) - set(chosen_indices))

    # Ensure the column remains as float64
    df[column_name] = df[column_name].astype('float64')

fill_na_proportionally('eSituation_07')
fill_na_proportionally('eSituation_08')


# In[20]:


cols_to_impute_cat = ["eArrest_05", "eArrest_02", "eArrest_07", "eArrest_11", "eArrest_18",
    "eScene_01", "eSituation_02", "eSituation_13"]

cols_to_impute_con = ['ePatient_15', 'eScene_09', 'eArrest_14', 'eSituation_01', 'eTimes_01',
               'eTimes_05', 'eTimes_06', 'eTimes_07','eTimes_13']


# In[21]:


df = df.rename(columns={"Unnamed: 0": "ID"})


# In[22]:


col_int = ["ID", "PcrKey", "eDispatch_01",
           "eArrest_01", "eArrest_05", "eArrest_02", "eArrest_07", "eArrest_11", "eArrest_18",
           "eDisposition_12", "eOutcome_01", "eOutcome_02", "ePatient_13", "ePatient_15", "ePatient_16",
           "eResponse_05", "eResponse_07", "eResponse_15", "eResponse_23", 
           "eScene_01", "eScene_06", "eScene_07", "eSituation_02", "eSituation_07",
           "eSituation_08", "eSituation_13"]


# In[23]:


df[col_int] = df[col_int].astype('Int64')


# In[24]:


df.to_csv('../data/filtered_data/PCR_Event_filter.csv')





