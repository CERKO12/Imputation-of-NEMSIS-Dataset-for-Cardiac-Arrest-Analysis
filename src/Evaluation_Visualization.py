#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde
from scipy.stats import ks_2samp
from scipy.stats import entropy


# In[2]:


df_imputed = pd.read_csv('../data/Imputed_Data_MICE&MissForest/df_imputed.csv', encoding= "UTF-8", index_col=0)
df_imputed_2 = pd.read_csv('../data/Imputed_Data_MICE/df_imputed_2.csv', encoding= "UTF-8", index_col=0)
pd.set_option('display.max_columns', None)

df_CE = pd.read_csv('../data/filtered_data/ComputedElement_filter.csv', encoding= "UTF-8", index_col=0)
df_CE = df_CE.drop('ID', axis=1)

df_Event = pd.read_csv('../data/filtered_data/PCR_Event_filter.csv', encoding= "UTF-8", index_col=0)
df_Event = df_Event.drop('ID', axis=1)

df_merge = pd.merge(df_CE, df_Event, on=['PcrKey'])


# In[3]:


cols_to_drop_imputed = ['eSituation_01', 'eTimes_01', 'eTimes_03', 'eTimes_05', 
                        'eTimes_06', 'eTimes_07', 'eTimes_13','eScene_09']
cols_to_drop_merge = ['eSituation_01', 'eTimes_01', 'eTimes_03', 'eTimes_05', 
                      'eArrest_11', 'ePatient_15', 'eTimes_06', 'eTimes_07', 
                      'eTimes_13', 'eArrest_14', 'eScene_09']
df_merge = df_merge.drop(cols_to_drop_merge, axis=1)
df_imputed = df_imputed.drop(cols_to_drop_imputed, axis=1)
df_imputed_2 = df_imputed_2.drop(cols_to_drop_imputed, axis=1)


# In[4]:


columns_to_plot = ['USCensusRegion', 'USCensusDivision', 'NasemsoRegion', 'Urbanicity',
                   'eDispatch_01', 'eArrest_01', 'eArrest_02', 'eArrest_05', 'eArrest_07', 'eArrest_18', 
                   'eDisposition_12', 'eOutcome_01', 'eOutcome_02', 'ePatient_13', 'ePatient_16', 
                   'eResponse_05', 'eResponse_07', 'eResponse_15', 'eResponse_23', 'eScene_01', 
                   'eScene_06', 'eScene_07', 'eSituation_02', 'eSituation_07', 'eSituation_08', 'eSituation_13']

n_cols = 3
n_rows = len(columns_to_plot) // n_cols + (len(columns_to_plot) % n_cols > 0)
fig, axes = plt.subplots(n_rows, n_cols, figsize=(15, 5 * n_rows))

axes = axes.flatten()

for i, col in enumerate(columns_to_plot):
    ax = axes[i]

    # Bar plot
    counts_imputed = df_imputed[col].value_counts().sort_index()
    counts_original = df_merge[col].value_counts().sort_index()
    
    counts_imputed.plot(kind='bar', ax=ax, color='green', alpha=0.6, label='Imputed')
    counts_original.plot(kind='bar', ax=ax, color='blue', alpha=0.4, label='Original')
    
    # Line plot without markers
    ax.plot(np.arange(len(counts_imputed)), counts_imputed.values, color='green', linewidth=2)
    ax.plot(np.arange(len(counts_original)), counts_original.values, color='darkblue', linewidth=2)

    ax.set_title(f'Distribution of {col}')
    ax.set_xlabel('Groups in ' + col)
    ax.set_ylabel('Count')
    ax.legend()

for j in range(i + 1, len(axes)):
    axes[j].set_visible(False)

plt.tight_layout()
plt.savefig('../fig/Distribution_of_Imputed&Original_Dataset.png')
plt.show()


# In[5]:


columns_to_plot = ['USCensusRegion', 'USCensusDivision', 'NasemsoRegion', 'Urbanicity',
                   'eDispatch_01', 'eArrest_01', 'eArrest_02', 'eArrest_05', 'eArrest_07', 'eArrest_18', 
                   'eDisposition_12', 'eOutcome_01', 'eOutcome_02', 'ePatient_13', 'ePatient_16', 
                   'eResponse_05', 'eResponse_07', 'eResponse_15', 'eResponse_23', 'eScene_01', 
                   'eScene_06', 'eScene_07', 'eSituation_02', 'eSituation_07', 'eSituation_08', 'eSituation_13']

n_cols = 3
n_rows = len(columns_to_plot) // n_cols + (len(columns_to_plot) % n_cols > 0)
fig, axes = plt.subplots(n_rows, n_cols, figsize=(15, 5 * n_rows))

axes = axes.flatten()

for i, col in enumerate(columns_to_plot):
    ax = axes[i]

    counts_imputed_2 = df_imputed_2[col].value_counts().sort_index()
    counts_original = df_merge[col].value_counts().sort_index()
    
    counts_imputed_2.plot(kind='bar', ax=ax, color='green', alpha=0.6, label='Imputed')
    counts_original.plot(kind='bar', ax=ax, color='blue', alpha=0.4, label='Original')
    
    ax.plot(np.arange(len(counts_imputed_2)), counts_imputed_2.values, color='green', linewidth=2)
    ax.plot(np.arange(len(counts_original)), counts_original.values, color='darkblue', linewidth=2)

    ax.set_title(f'Distribution of {col}')
    ax.set_xlabel('Groups in ' + col)
    ax.set_ylabel('Count')
    ax.legend()

for j in range(i + 1, len(axes)):
    axes[j].set_visible(False)

plt.tight_layout()
plt.savefig('../fig/Distribution_of_Imputed&Original_Dataset_2.png')
plt.show()


# In[6]:


continuous_columns = ['EMSDispatchCenterTimeSec', 'EMSChuteTimeMin', 'EMSSystemResponseTimeMin', 
                      'EMSSceneResponseTimeMin', 'EMSSceneToPatientTimeMin', 'EMSTotalCallTimeMin',
                      'ageinyear']

n_cols = 2
n_rows = len(continuous_columns) // n_cols + (len(continuous_columns) % n_cols > 0)
fig, axes = plt.subplots(n_rows, n_cols, figsize=(15, 5 * n_rows))

axes = axes.flatten()

for i, col in enumerate(continuous_columns):
    ax = axes[i]

    density_imputed = gaussian_kde(df_imputed[col].dropna())
    density_original = gaussian_kde(df_merge[col].dropna())

    x = np.linspace(0, 250, 50)

    ax.plot(x, density_imputed(x), label='Imputed', color='blue')
    ax.plot(x, density_original(x), label='Original', color='green')

    ax.set_title(f'Density Plot of {col}')
    ax.set_xlabel('Value')
    ax.set_xlim(0, 250) 
    ax.legend()

for j in range(i + 1, len(axes)):
    axes[j].set_visible(False)

plt.tight_layout()

plt.savefig('../fig/Density_Plots.png')


# In[7]:


continuous_variables = ['ageinyear', 'EMSDispatchCenterTimeSec', 'EMSChuteTimeMin', 
                        'EMSSystemResponseTimeMin', 'EMSSceneResponseTimeMin', 
                        'EMSSceneToPatientTimeMin', 'EMSTotalCallTimeMin']

print("Impact on Continuous Variables:")
for var in continuous_variables:
    original_data = df_merge[var].dropna()
    imputed_data = df_imputed[var]

    mean_diff = imputed_data.mean() - original_data.mean()
    median_diff = imputed_data.median() - original_data.median()
    std_diff = imputed_data.std() - original_data.std()
    ks_statistic, ks_pvalue = ks_2samp(original_data, imputed_data)

    print(f"\nVariable: {var}")
    print(f"Mean difference: {mean_diff}")
    print(f"Median difference: {median_diff}")
    print(f"Standard deviation difference: {std_diff}")
    print(f"KS statistic: {ks_statistic}, P-value: {ks_pvalue}")


# In[8]:


categorical_columns = ['USCensusRegion', 'USCensusDivision', 'NasemsoRegion', 'Urbanicity', 
                       'eDispatch_01', 'eArrest_01', 'eArrest_02', 'eArrest_05', 'eArrest_07', 
                       'eArrest_18', 'eDisposition_12', 'eOutcome_01', 'eOutcome_02', 
                       'ePatient_13', 'ePatient_16', 'eResponse_05', 'eResponse_07', 
                       'eResponse_15', 'eResponse_23', 'eScene_01', 'eScene_06', 
                       'eScene_07', 'eSituation_02', 'eSituation_07', 'eSituation_08', 'eSituation_13']


print("Entropy Changes for Categorical Variables of Imputed Dataset 1:")
for var in categorical_columns:
    original_entropy = entropy(df_merge[var].value_counts())
    imputed_entropy = entropy(df_imputed[var].value_counts())
    entropy_change = imputed_entropy - original_entropy
    print(f"{var}: Entropy Change = {entropy_change}")
    
print("Entropy Changes for Categorical Variables of Imputed Dataset 2:")
for var in categorical_columns:
    original_entropy = entropy(df_merge[var].value_counts())
    imputed_entropy = entropy(df_imputed_2[var].value_counts())
    entropy_change = imputed_entropy - original_entropy
    print(f"{var}: Entropy Change = {entropy_change}")







