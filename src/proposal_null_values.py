#!/usr/bin/env python
# coding: utf-8

# In[7]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# In[2]:


df = pd.read_csv("../data/ASCII_2020/processeddataCA/processeddataCA/ComputedElements_CA.csv", encoding= "UTF-8")
df.head()


# In[3]:


df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)
df.replace([".", ""], np.nan, inplace=True)
df.head()


# In[5]:


df.isnull().sum()


# In[11]:


null_counts = df.isnull().sum()
plt.figure(figsize=(15,8)) 
null_counts.plot(kind='bar')
plt.title('Number of Null Values in Each Column')
plt.ylabel('Number of Null Values')
plt.xlabel('Column Names')
plt.xticks(rotation=45)  
plt.tight_layout()

plt.savefig("../fig/null_values_chart.jpg", dpi=300, bbox_inches='tight')
plt.show()


# In[ ]:




