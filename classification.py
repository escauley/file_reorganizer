## Jan20,2022
# Tianyi Wang

#%%
import pandas as pd
import os
import shutil

#%%
# import csv file
df = pd.read_csv('glycan_classification.csv')
df.head()

# %%
# CSV clean-up
df_modified = df.drop(['glycan_type_source','glycan_type_source_id','glycan_subtype_source','glycan_subtype_source_id'],axis=1)
df_modified.head()

# %%
df_modified.duplicated(subset='glytoucan_ac').sum()
# total of 13803 duplicates 

# %%
