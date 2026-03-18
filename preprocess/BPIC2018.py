
#%%
import pandas as pd
import math,random
import time, os, csv
import numpy as np
import random


sample = False
inputpath = r'../../data/csv/BPI_2018/'
outputpath = r''

#%%
agriculture = pd.read_csv(inputpath+f'BPI_Challenge_2018.csv', keep_default_na=True, sep=',')

#%%
#drop not relevant columns
drop_cols = [
    'note', 'case:penalty_AJLP', 'case:penalty_AUVP', 'case:penalty_BGKV',
    'case:small farmer', 'case:penalty_BGP', 'case:penalty_C16', 'case:penalty_BGK', 
    'case:penalty_AVUVP', 'case:penalty_AVJLP', 'case:penalty_C9','case:cross_compliance', 
    'case:rejected', 'case:greening', 'case:penalty_C4', 'case:penalty_AVGP', 'case:penalty_ABP',
    'case:penalty_B6', 'case:penalty_B4', 'case:penalty_B5', 'case:penalty_B3', 'case:penalty_AVBP', 
    'case:penalty_B2', 'case:penalty_AGP', 'case:penalty_B16', 'case:penalty_GP1', 'case:basic payment',
    'case:penalty_B5F', 'case:penalty_V5', 'case:selected_manually','case:penalty_JLP5', 'case:penalty_JLP2', 
    'case:penalty_JLP6', 'case:penalty_JLP7', 'case:penalty_JLP3', 'case:penalty_JLP1', 'case:redistribution',
    'case:penalty_amount1', 'case:payment_actual1', 'case:amount_applied1', 'case:penalty_amount2', 'case:payment_actual2', 
    'case:amount_applied2', 'case:penalty_amount3', 'case:payment_actual3', 'case:amount_applied3', 
    'case:young farmer', 'case:selected_random','case:penalty_CC','docid_uuid', 'doctype', 'docid', 'lifecycle:transition',
    'eventid','case:risk_factor','case:identity:id','success','activity','case:program-id'
]

agriculture = agriculture.drop(columns=drop_cols, errors='ignore')

#%%
#case ID: caseID_... 'caseID_case_concept_name'
#case level: case_...
#event level: event_...
#activity (always event level): event_activity_... 'event_activity_concept_name'
#timestamp (always event level): event_timestamp_... 'event_timestamp_time_timestamp'
#otherC: string dependent (completely string or if there are values containing different strings)
#otherN: non string dependent (completely numerical or if all the values contain the same strings)
#spaces are taken out

agriculture.rename(columns={
    'org:resource':'event_OtherC_org_resource', 
    'subprocess':'event_OtherC_subprocess', 
    'identity:id':'event_OtherC_identity_id', 
    'concept:name':'event_activity_concept_name', #Activity
    'time:timestamp':'event_timestamp_time_timestamp', #Timestamp
    'case:application':'case_OtherC_case_application', 
    'case:penalty_amount0':'case_OtherN_case_penalty_amount0',
    'case:applicant':'case_OtherC_case_applicant', 
    'case:department':'case_OtherC_case_department', 
    'case:selected_risk':'case_OtherC_case_selected_risk', 
    'case:area':'case_OtherN_case_area',
    'case:payment_actual0':'case_OtherN_case_payment_actual0', 
    'case:amount_applied0':'case_OtherN_case_amount_applied0', 
    'case:year':'case_OtherN_case_year',
    'case:number_parcels':'case_OtherN_case_number_parcels', 
    'case:concept:name':'caseID_case_concept_name' #CaseID
},inplace=True)

# %%
#2015-05-07 22:00:00+00:00 
# 2015-10-26 12:27:10.390000+00:00 - event_timestamp_time_timestamp

agriculture['event_timestamp_time_timestamp'] = pd.to_datetime(agriculture['event_timestamp_time_timestamp'], format='mixed', errors='coerce', utc=True)
agriculture['event_timestamp_time_timestamp'] = (agriculture['event_timestamp_time_timestamp'].dt.strftime('%Y%m%d%H%M%S%f').str.slice(0, 18))
agriculture = agriculture.reset_index(drop=True)

# %%
filename = 'BPIC18_Agriculture.csv'

agriculture.insert(0, "eventID", (agriculture.groupby("caseID_case_concept_name").cumcount() + 1).astype(str) + "_" + agriculture["caseID_case_concept_name"].astype(str))
agriculture.to_csv(outputpath + filename, index=False)

# Sample of the 10 cases
sample = True

if sample:
    random.seed(1)
    sampled_cases = random.sample(agriculture['caseID_case_concept_name'].unique().tolist(), 10)
    sampled = agriculture[agriculture['caseID_case_concept_name'].isin(sampled_cases)]
    sampled.to_csv(outputpath + 'Sample_BPIC18_Agriculture.csv', index=False)


# %%
