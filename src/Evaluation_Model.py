#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix
import seaborn as sns
from sklearn.metrics import roc_curve, auc
from sklearn.preprocessing import label_binarize


# In[2]:


df_imputed = pd.read_csv('../data/Imputed_Data_MICE&MissForest/df_imputed_all.csv', encoding= "UTF-8", index_col=0)
df_imputed_2 = pd.read_csv('../data/Imputed_Data_MICE/df_imputed_all_2.csv', encoding= "UTF-8", index_col=0)
pd.set_option('display.max_columns', None)


# In[3]:


df_CE = pd.read_csv('../data/filtered_data/ComputedElement_filter.csv', encoding= "UTF-8", index_col=0)
df_CE = df_CE.drop('ID', axis=1)
df_Event = pd.read_csv('../data/filtered_data/PCR_Event_filter.csv', encoding= "UTF-8", index_col=0)
df_Event = df_Event.drop('ID', axis=1)

df_merge = pd.merge(df_CE, df_Event, on=['PcrKey'])


# In[4]:


cols_to_drop_imputed = ['eSituation_01', 'eTimes_01', 'eTimes_03', 'eTimes_05', 
                        'eTimes_06', 'eTimes_07', 'eTimes_13', 'eScene_09', 
                        'eSituation_09', 'eSituation_10', 'eSituation_11', 'eSituation_12']
cols_to_drop_merge = ['eSituation_01', 'eTimes_01', 'eTimes_03', 'eTimes_05', 
                      'eArrest_11', 'ePatient_15', 'eTimes_06', 'eTimes_07', 
                      'eTimes_13', 'eArrest_14', 'eScene_09']
df_merge = df_merge.drop(cols_to_drop_merge, axis=1)
df_imputed = df_imputed.drop(cols_to_drop_imputed, axis=1)
df_imputed_2 = df_imputed_2.drop(cols_to_drop_imputed, axis=1)


# In[5]:


df_sample_imputed = df_merge.copy()


# In[6]:


categorical_columns = ['USCensusRegion', 'USCensusDivision', 'NasemsoRegion', 'Urbanicity', 
                       'eDispatch_01', 'eArrest_01', 'eArrest_02', 'eArrest_05', 'eArrest_07', 
                       'eArrest_18', 'eDisposition_12', 'eOutcome_01', 'eOutcome_02', 
                       'ePatient_13', 'ePatient_16', 'eResponse_05', 'eResponse_07', 
                       'eResponse_15', 'eResponse_23', 'eScene_01', 'eScene_06', 
                       'eScene_07', 'eSituation_02', 'eSituation_07', 'eSituation_08', 'eSituation_13']

continuous_columns = ['ageinyear', 'EMSDispatchCenterTimeSec', 'EMSChuteTimeMin', 
                      'EMSSystemResponseTimeMin', 'EMSSceneResponseTimeMin', 
                      'EMSSceneToPatientTimeMin', 'EMSTotalCallTimeMin']

# Fill missing values in categorical columns with mode
for column in categorical_columns:
    mode_value = df_sample_imputed[column].mode()[0]
    df_sample_imputed[column].fillna(mode_value, inplace=True)

# Fill missing values in continuous columns with mean
for column in continuous_columns:
    mean_value = df_sample_imputed[column].mean()
    df_sample_imputed[column].fillna(mean_value, inplace=True)


# In[7]:


from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score


# In[8]:


target = 'eArrest_18'
columns_to_encode = ['USCensusRegion', 'USCensusDivision', 
                     'NasemsoRegion', 'Urbanicity']


# In[9]:


label_encoder = LabelEncoder()
for col in columns_to_encode:
    combined_data = pd.concat([df_imputed[col], df_merge[col], df_sample_imputed[col], df_imputed_2[col]], axis=0)
    
    label_encoder.fit(combined_data.astype(str))
    df_imputed[col] = label_encoder.transform(df_imputed[col].astype(str))
    df_merge[col] = label_encoder.transform(df_merge[col].astype(str))
    df_sample_imputed[col] = label_encoder.transform(df_sample_imputed[col].astype(str))
    df_imputed_2[col] = label_encoder.transform(df_imputed_2[col].astype(str))


# In[10]:


df_merge = df_merge.dropna()


# In[11]:


X_sample_imputed = df_sample_imputed.drop(target, axis=1)
y_sample_imputed = df_sample_imputed[target]

X_imputed = df_imputed.drop(target, axis=1)
y_imputed = df_imputed[target]

X_imputed_2 = df_imputed_2.drop(target, axis=1)
y_imputed_2 = df_imputed_2[target]

X_merge = df_merge.drop(target, axis=1)
y_merge = df_merge[target]

X_train_smp, X_test_smp, y_train_smp, y_test_smp = train_test_split(X_sample_imputed, y_sample_imputed, test_size=0.2, random_state=42)
X_train_imp, X_test_imp, y_train_imp, y_test_imp = train_test_split(X_imputed, y_imputed, test_size=0.2, random_state=42)
X_train_imp_2, X_test_imp_2, y_train_imp_2, y_test_imp_2 = train_test_split(X_imputed_2, y_imputed_2, test_size=0.2, random_state=42)
X_train_mrg, X_test_mrg, y_train_mrg, y_test_mrg = train_test_split(X_merge, y_merge, test_size=0.2, random_state=42)


# In[12]:


model = RandomForestClassifier(random_state=42)

model.fit(X_train_smp, y_train_smp)
predictions_smp = model.predict(X_test_smp)
accuracy_smp = accuracy_score(y_test_smp, predictions_smp)

model.fit(X_train_imp, y_train_imp)
predictions_imp = model.predict(X_test_imp)
accuracy_imp = accuracy_score(y_test_imp, predictions_imp)

model.fit(X_train_imp_2, y_train_imp_2)
predictions_imp_2 = model.predict(X_test_imp_2)
accuracy_imp_2 = accuracy_score(y_test_imp_2, predictions_imp_2)

model.fit(X_train_mrg, y_train_mrg)
predictions_mrg = model.predict(X_test_mrg)
accuracy_mrg = accuracy_score(y_test_mrg, predictions_mrg)

print("Accuracy with sample-imputed data:", accuracy_smp)
print("Accuracy with imputed data(mice&missforest):", accuracy_imp)
print("Accuracy with imputed data(mice):", accuracy_imp_2)
print("Accuracy with original data:", accuracy_mrg)


# In[13]:


classes = np.unique(y_train_imp)
y_train_imp_bin = label_binarize(y_train_imp, classes=classes)
y_test_imp_bin = label_binarize(y_test_imp, classes=classes)
y_train_imp_2_bin = label_binarize(y_train_imp_2, classes=classes)
y_test_imp_2_bin = label_binarize(y_test_imp_2, classes=classes)
y_train_mrg_bin = label_binarize(y_train_mrg, classes=classes)
y_test_mrg_bin = label_binarize(y_test_mrg, classes=classes)
y_train_smp_bin = label_binarize(y_train_smp, classes=classes)
y_test_smp_bin = label_binarize(y_test_smp, classes=classes)

n_classes = y_train_imp_bin.shape[1]

model.fit(X_train_imp, y_train_imp)
y_score_imp = model.predict_proba(X_test_imp)

model.fit(X_train_imp_2, y_train_imp_2)
y_score_imp_2 = model.predict_proba(X_test_imp_2)

model.fit(X_train_mrg, y_train_mrg)
y_score_mrg = model.predict_proba(X_test_mrg)

model.fit(X_train_smp, y_train_smp)
y_score_smp = model.predict_proba(X_test_smp)

fpr_imp = dict()
tpr_imp = dict()
roc_auc_imp = dict()
for i in range(n_classes):
    fpr_imp[i], tpr_imp[i], _ = roc_curve(y_test_imp_bin[:, i], y_score_imp[:, i])
    roc_auc_imp[i] = auc(fpr_imp[i], tpr_imp[i])

fpr_imp_2 = dict()
tpr_imp_2 = dict()
roc_auc_imp_2 = dict()
for i in range(n_classes):
    fpr_imp_2[i], tpr_imp_2[i], _ = roc_curve(y_test_imp_2_bin[:, i], y_score_imp_2[:, i])
    roc_auc_imp_2[i] = auc(fpr_imp_2[i], tpr_imp_2[i])    
    
fpr_mrg = dict()
tpr_mrg = dict()
roc_auc_mrg = dict()
for i in range(n_classes):
    fpr_mrg[i], tpr_mrg[i], _ = roc_curve(y_test_mrg_bin[:, i], y_score_mrg[:, i])
    roc_auc_mrg[i] = auc(fpr_mrg[i], tpr_mrg[i])
    
fpr_smp = dict()
tpr_smp = dict()
roc_auc_smp = dict()
for i in range(n_classes):
    fpr_smp[i], tpr_smp[i], _ = roc_curve(y_test_smp_bin[:, i], y_score_smp[:, i])
    roc_auc_smp[i] = auc(fpr_smp[i], tpr_smp[i])

plt.figure(figsize=(12, 8))
for i in range(n_classes):
    plt.plot(fpr_imp[i], tpr_imp[i], label=f'{classes[i]} (area = {roc_auc_imp[i]:.2f})')
plt.plot([0, 1], [0, 1], 'k--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('ROC for Model-Imputed-MICE&MissForest Data')
plt.legend(loc="lower right")
plt.savefig('../fig/ROC_Model_MICE&MissForest_Imputed.png')
plt.show()

plt.figure(figsize=(12, 8))
for i in range(n_classes):
    plt.plot(fpr_imp_2[i], tpr_imp_2[i], label=f'{classes[i]} (area = {roc_auc_imp_2[i]:.2f})')
plt.plot([0, 1], [0, 1], 'k--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('ROC for Model-Imputed-MICE Data')
plt.legend(loc="lower right")
plt.savefig('../fig/ROC_Model_MICE_Imputed.png')
plt.show()

plt.figure(figsize=(12, 8))
for i in range(n_classes):
    plt.plot(fpr_mrg[i], tpr_mrg[i], label=f'{classes[i]} (area = {roc_auc_mrg[i]:.2f})')
plt.plot([0, 1], [0, 1], 'k--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('ROC for Original Data')
plt.legend(loc="lower right")
plt.savefig('../fig/ROC_Original.png')
plt.show()

plt.figure(figsize=(12, 8))
for i in range(n_classes):
    plt.plot(fpr_smp[i], tpr_smp[i], label=f'Sample-Imputed - Class {classes[i]} (AUC = {roc_auc_smp[i]:.2f})')
plt.plot([0, 1], [0, 1], 'k--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('ROC for Simple-Imputed Data')
plt.legend(loc="lower right")
plt.savefig('../fig/ROC_Simple_Imputed.png')
plt.show()







