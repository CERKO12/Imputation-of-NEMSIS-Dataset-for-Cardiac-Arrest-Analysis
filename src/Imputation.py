#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# In[2]:


df_CE = pd.read_csv('../data/filtered_data/ComputedElement_filter.csv', encoding= "UTF-8", index_col=0)
pd.set_option('display.max_columns', None)
df_CE = df_CE.drop('ID', axis=1)
df_CE.head()


# In[3]:


df_Event = pd.read_csv('../data/filtered_data/PCR_Event_filter.csv', encoding= "UTF-8", index_col=0)
pd.set_option('display.max_columns', None)
df_Event = df_Event.drop('ID', axis=1)
df_Event.head()


# In[4]:


df_PS = pd.read_csv('../data/filtered_data/FACTPCRPRIMARYSYMPTOM_CA_filter.csv', encoding= "UTF-8", index_col=0)
pd.set_option('display.max_columns', None)
df_PS = df_PS.drop('ID', axis=1)
df_PS.head()


# In[5]:


df_AS = pd.read_csv('../data/filtered_data/FACTPCRADDITIONALSYMPTOM_CA_filter.csv', encoding= "UTF-8", index_col=0)
pd.set_option('display.max_columns', None)
df_AS = df_AS.drop('ID', axis=1)
df_AS.head()


# In[6]:


df_PI = pd.read_csv('../data/filtered_data/FACTPCRPRIMARYIMPRESSION_CA_filter.csv', encoding= "UTF-8", index_col=0)
pd.set_option('display.max_columns', None)
df_PI = df_PI.drop('ID', axis=1)
df_PI.head()


# In[7]:


df_SI = pd.read_csv('../data/filtered_data/FACTPCRSECONDARYIMPRESSION_CA_filter.csv', encoding= "UTF-8", index_col=0)
pd.set_option('display.max_columns', None)
df_SI = df_SI.drop('ID', axis=1)
df_SI.head()


# In[8]:


df_merge = pd.merge(df_CE, df_Event, on=['PcrKey'])


# In[9]:


col_to_drop = ['ePatient_15','eArrest_14', 'eArrest_11']
df_merge = df_merge.drop(col_to_drop, axis=1)


# In[10]:


df_merge.head(50)


# In[11]:


df_merge.info()


# In[12]:


df_encode = df_merge.copy()

cat_columns = ['eSituation_01','eTimes_01','eTimes_03', 
               'eTimes_05','eTimes_06','eTimes_07','eTimes_13',
               'USCensusRegion','USCensusDivision','NasemsoRegion','Urbanicity']

for col in cat_columns:
    df_encode[col] = df_encode[col].astype('category').cat.codes

# Replace -1 with np.nan:
df_encode.replace({col: {-1: np.nan} for col in cat_columns}, inplace=True)


# In[13]:


df_encode.head(50)


# In[14]:


from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression


# In[15]:


cols_to_impute_cat = ['USCensusRegion','USCensusDivision','NasemsoRegion','Urbanicity',
                      'eArrest_02','eArrest_05','eArrest_07','eArrest_18',
                      "eScene_01", "eSituation_02", "eSituation_13"]

cols_to_impute_con = ['ageinyear','EMSDispatchCenterTimeSec',
                      'EMSChuteTimeMin','EMSSystemResponseTimeMin',
                      'EMSSceneResponseTimeMin','EMSSceneToPatientTimeMin',
                      'EMSTotalCallTimeMin','eSituation_01', 'eTimes_01',
                      'eTimes_05', 'eTimes_06', 'eTimes_07','eTimes_13']


# In[16]:


df_imputed_con = df_encode.copy(deep=True)

mice_imputer = IterativeImputer(initial_strategy="mean", 
                                max_iter=10, 
                                random_state=1, 
                                verbose=2)


previous_imputation = None
for i in range(mice_imputer.max_iter):
    imputed_data = mice_imputer.fit_transform(df_encode[cols_to_impute_con])
    df_imputed_con[cols_to_impute_con] = imputed_data
    
    # Check for convergence
    if previous_imputation is not None:
        change = np.abs(imputed_data - previous_imputation).max()
        print(f"Iteration {i}, Max change in imputed values: {change}")
        if change < 15000:
            print("Convergence reached.")
            break

    previous_imputation = imputed_data.copy()


# In[17]:


df_imputed_con_copy = df_imputed_con.copy()
df_imputed_con_copy_2 = df_imputed_con.copy()


# In[18]:


def miss_forest_impute(df, cols_to_impute, max_iter=10, tolerance=0.01):
    df_imputed = df[cols_to_impute].copy()

    missing_mask = {col: df[col].isnull() for col in cols_to_impute}

    for i in range(max_iter):
        change_count = 0
        total_count = 0

        for col in cols_to_impute:
            X = df_imputed.drop(col, axis=1)
            y = df_imputed[col]
            missing = missing_mask[col]  

            if not missing.any():
                continue
       
            imputer = SimpleImputer(strategy='most_frequent')
            X_imputed = imputer.fit_transform(X)

            model = RandomForestClassifier(n_estimators=100)
            model.fit(X_imputed[~missing], y[~missing])

            predictions = model.predict(X_imputed[missing])
            prev_values = df_imputed.loc[missing, col].copy()
            df_imputed.loc[missing, col] = predictions

            change_count += np.sum(prev_values != predictions)
            total_count += missing.sum()

        change_ratio = change_count / total_count if total_count > 0 else 0
        print(f"Iteration {i+1} complete. Change ratio: {change_ratio:.4f}")

        # Check for overall accuracy change
        if total_count == 0 or change_ratio < tolerance:
            print(f"Stopping early at iteration {i+1}, change below tolerance.")
            break

    return df_imputed

df_imputed_cat = miss_forest_impute(df_imputed_con_copy, cols_to_impute_cat, max_iter=5, tolerance=0.035)


# In[19]:


logistic_mice_imputer = IterativeImputer(
    estimator=LogisticRegression(solver='lbfgs', multi_class='multinomial', max_iter=500),
    max_iter=10,
    random_state=1,
    verbose=2
)

df_imputed_con_copy_2[cols_to_impute_cat] = logistic_mice_imputer.fit_transform(df_imputed_con_copy_2[cols_to_impute_cat])


# In[20]:


for col in cols_to_impute_cat:
    df_imputed_con_copy[col] = df_imputed_cat[col]


# In[21]:


df_encode_imputed = df_imputed_con_copy.copy()
df_encode_imputed_2 = df_imputed_con_copy_2.copy()


# In[22]:


cat_columns = ['eSituation_01','eTimes_01','eTimes_03', 
               'eTimes_05','eTimes_06','eTimes_07','eTimes_13',
               'USCensusRegion','USCensusDivision','NasemsoRegion','Urbanicity']

# Recreate category mappings from the original DataFrame
category_mappings = {}
for col in cat_columns:
    category_mappings[col] = dict(enumerate(df_merge[col].astype('category').cat.categories))

# Decode each Date column in df_encode_imputed
for col in cat_columns:
    if col in df_encode_imputed.columns:
        df_encode_imputed[col] = df_encode_imputed[col].apply(
            lambda x: category_mappings[col].get(int(round(x))) if pd.notna(x) and int(round(x)) in category_mappings[col] else np.nan
        )
        
# Decode each categorical column in df_encode_imputed_2
for col in cat_columns:
    if col in df_encode_imputed_2.columns:
        df_encode_imputed_2[col] = df_encode_imputed_2[col].apply(
            lambda x: category_mappings[col].get(int(round(x))) if pd.notna(x) and int(round(x)) in category_mappings[col] else np.nan
        )


df_decode_imputed = df_encode_imputed.copy()
df_decode_imputed_2 = df_encode_imputed_2.copy()


# In[23]:


df_decode_imputed = df_decode_imputed.dropna()
df_filtered = df_decode_imputed[df_decode_imputed['ageinyear'] >= 0]

df_decode_imputed_2 = df_decode_imputed_2.dropna()
df_filtered_2 = df_decode_imputed_2[df_decode_imputed_2['ageinyear'] >= 0]


# In[24]:


# List of columns to convert to int64
columns_to_convert = ['ageinyear', 'eArrest_02', 'eArrest_05', 'eArrest_07', 'eArrest_18', 
                      'eSituation_02', 'eSituation_07', 'eSituation_08', 'eSituation_13']

# Convert each column to int64
for column in columns_to_convert:
    df_filtered[column] = df_filtered[column].astype('int64')
    df_filtered_2[column] = df_filtered_2[column].astype('int64')


# In[25]:


df_filtered_copy = df_filtered.copy()

df_filtered_copy = pd.merge(df_filtered_copy, df_PS, on=['PcrKey'])
df_filtered_copy = pd.merge(df_filtered_copy, df_AS, on=['PcrKey'])
df_filtered_copy = pd.merge(df_filtered_copy, df_PI, on=['PcrKey'])
df_filtered_copy = pd.merge(df_filtered_copy, df_SI, on=['PcrKey'])

df_filtered_copy_2 = df_filtered_2.copy()

df_filtered_copy_2 = pd.merge(df_filtered_copy_2, df_PS, on=['PcrKey'])
df_filtered_copy_2 = pd.merge(df_filtered_copy_2, df_AS, on=['PcrKey'])
df_filtered_copy_2 = pd.merge(df_filtered_copy_2, df_PI, on=['PcrKey'])
df_filtered_copy_2 = pd.merge(df_filtered_copy_2, df_SI, on=['PcrKey'])


# In[26]:


columns_to_replace = ['eSituation_09','eSituation_10','eSituation_11','eSituation_12']

# Replace null values in these columns with '7701003'
for column in columns_to_replace:
    df_filtered_copy[column].fillna('7701003', inplace=True)
    df_filtered_copy_2[column].fillna('7701003', inplace=True)


# In[27]:


df_filtered_copy.to_csv('../data/Imputed_Data_MICE&MissForest/df_imputed_all.csv')
df_filtered_copy_2.to_csv('../data/Imputed_Data_MICE/df_imputed_all_2.csv')


# In[28]:


df_filtered.to_csv('../data/Imputed_Data_MICE&MissForest/df_imputed.csv')
df_filtered_2.to_csv('../data/Imputed_Data_MICE/df_imputed_2.csv')





