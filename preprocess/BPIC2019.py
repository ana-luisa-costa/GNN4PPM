
#%%
import pandas as pd
import math,random
import time, os, csv
import numpy as np
import random


sample = False
inputpath = r'../../data/csv/BPI_2019/'
outputpath = r''

#%%
procuretopay = pd.read_csv(inputpath+f'BPI_Challenge_2019.csv', keep_default_na=True, sep=',')

#%%
#drop not relevant columns
procuretopay = procuretopay.drop(columns=['User','case:Company','case:Document Type',
                                          'case:Purch. Doc. Category name','case:Spend classification text',
                                          'case:Source','case:Name'])

#%%
#case ID: caseID_... 'caseID_case_concept_name'
#case level: case_...
#event level: event_...
#activity (always event level): event_activity_... 'event_activity_concept_name'
#timestamp (always event level): event_timestamp_... 'event_timestamp_time_timestamp'
#otherC: string dependent (completely string or if there are values containing different strings)
#otherN: non string dependent (completely numerical or if all the values contain the same strings)
#spaces are taken out

procuretopay.rename(columns={
    'org:resource': 'event_OtherC_org_resource',
    'concept:name': 'event_activity_concept_name', #Activity
    'Cumulative net worth (EUR)': 'event_OtherN_Cumulative_net_worth_EUR',
    'time:timestamp': 'event_timestamp_time_timestamp', #Timestamp
    'case:Spend area text': 'case_OtherC_case_Spend_area_text',
    'case:Sub spend area text':'case_OtherC_case_Sub_spend_area_text',
    'case:Purchasing Document': 'case_OtherN_case_Purchasing_Document', 
    'case:Vendor': 'case_OtherN_case_Vendor', #check if all values start vendorID and remove it
    'case:Item Type':'case_OtherC_case_Item_Type',
    'case:Item Category': 'case_OtherC_case_Item_Category',
    'case:GR-Based Inv. Verif.': 'case_OtherC_case_GRBased_Inv_Verif',
    'case:Item': 'case_OtherN_case_Item',
    'case:concept:name': 'caseID_case_concept_name', #CaseID #check if all values have _ in the middle and remove it
    'case:Goods Receipt': 'case_OtherC_case_Goods_Receipt'
},inplace=True)

#%%
procuretopay["case_OtherN_case_Vendor"] = procuretopay["case_OtherN_case_Vendor"].astype(str).str.replace("^vendorID_", "", regex=True)
procuretopay["caseID_case_concept_name"] = procuretopay["caseID_case_concept_name"].astype(str).str.replace("_", "", regex=True)

# %%
#2018-01-02 12:53:00+00:00 - event_timestamp_time_timestamp

procuretopay['event_timestamp_time_timestamp'] = pd.to_datetime(procuretopay['event_timestamp_time_timestamp'], format='%Y-%m-%d %H:%M:%S%z')
procuretopay['event_timestamp_time_timestamp'] = procuretopay['event_timestamp_time_timestamp'].map(lambda x: x.strftime('%Y%m%d%H%M%S')+'0000')
procuretopay = procuretopay.reset_index(drop=True)

# %%
filename = 'BPIC19_ProcureToPay.csv'

procuretopay.insert(0, "eventID", (procuretopay.groupby("caseID_case_concept_name").cumcount() + 1).astype(str) + "_" + procuretopay["caseID_case_concept_name"].astype(str))
procuretopay.to_csv(outputpath + filename, index=False)

# Sample of the 10 cases
sample = True

if sample:
    random.seed(1)
    sampled_cases = random.sample(procuretopay['caseID_case_concept_name'].unique().tolist(), 10)
    sampled = procuretopay[procuretopay['caseID_case_concept_name'].isin(sampled_cases)]
    sampled.to_csv(outputpath + 'Sample_BPIC19_ProcureToPay.csv', index=False)



# %%
