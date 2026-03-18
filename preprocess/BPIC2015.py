#%%
import pandas as pd
import math,random
import time, os, csv
import numpy as np
import random


sample = False
inputpath = r'../../data/csv/BPI_2015/'
outputpath = r''

#%%
municipality_1 = pd.read_csv(inputpath+f'BPI_Challenge_2015_Municipality_1.csv', keep_default_na=True, sep=',')
municipality_2 = pd.read_csv(inputpath+f'BPI_Challenge_2015_Municipality_2.csv', keep_default_na=True, sep=',')
municipality_3 = pd.read_csv(inputpath+f'BPI_Challenge_2015_Municipality_3.csv', keep_default_na=True, sep=',')
municipality_4 = pd.read_csv(inputpath+f'BPI_Challenge_2015_Municipality_4.csv', keep_default_na=True, sep=',')
municipality_5 = pd.read_csv(inputpath+f'BPI_Challenge_2015_Municipality_5.csv', keep_default_na=True, sep=',')

#%%
#case ID: caseID_...
#case level: case_...
#event level: event_...
#activity (always event level): event_activity_...
#timestamp (always event level): event_timestamp_...
#otherC: string dependent (completely string or if there are values containing different strings)
#otherN: non string dependent (completely numerical or if all the values contain the same strings)
#spaces are taken out

municipality_1.rename(columns={
    'question':'event_otherC_question', #change EMPTY and other to NA #due to the number of empty values dropped from all datasets
    'dateFinished':'event_otherN_dateFinished', #dropped from all datasets
    'dueDate':'event_otherN_dueDate', #94% missing values maybe drop #dropped from all datasets
    'action_code':'event_otherC_action_code', #The same as activity, drop #dropped from all datasets
    'activityNameEN':'event_otherC_activityNameEN',
    'planned':'event_otherN_planned', 
    'time:timestamp':'event_timestamp_time_timestamp', #Timestamp
    'monitoringResource':'event_otherN_monitoringResource', 
    'org:resource':'event_otherN_org_resource',
    'activityNameNL':'event_otherC_activityNameNL', #Same as activity name in english, maybe drop #dropped from all datasets
    'concept:name':'event_activity_concept_name', #Activity
    'lifecycle:transition':'case_otherC_lifecycle_transition', #All are complete, maybe drop #dropped from all datasets
    'case:endDate':'case_otherN_case_endDate', #dropped from all datasets
    'case:caseStatus':'case_otherC_case_caseStatus', 
    'case:SUMleges':'case_otherN_case_SUMleges', 
    'case:last_phase':'case_otherC_case_last_phase',
    'case:case_type':'case_otherN_case_case_type', #All are 55769, maybe drop #dropped from all datasets
    'case:concept:name':'caseID_case_concept_name', #CaseID
    'case:Responsible_actor':'case_otherN_case_Responsible_actor',
    'case:parts':'case_otherC_case_parts', 
    'case:termName':'case_otherC_case_termName', #dropped from all datasets
    'case:endDatePlanned':'case_otherN_case_endDatePlanned', #86% missing values maybe drop #dropped from all datasets
    'case:startDate':'case_otherN_case_startDate', #dropped from all datasets
    'case:requestComplete':'case_otherC_case_requestComplete', #True or false values
    'case:IDofConceptCase':'case_otherN_case_IDofConceptCase', #dropped from all datasets
    'case:landRegisterID':'case_otherN_case_landRegisterID', #85% missing values maybe drop #dropped from all datasets
    'case:caseProcedure':'case_otherC_case_caseProcedure', #89% missing values maybe drop #dropped from all datasets
    'case:Includes_subCases':'case_otherC_case_Includes_subCases', #dropped from all datasets
    'dateStop':'case_otherN_dateStop' #99% missing values maybe drop #dropped from all datasets
},inplace=True)

municipality_2.rename(columns={
    'monitoringResource':'event_otherN_monitoringResource',
    'org:resource':'event_otherN_org_resource',
    'activityNameNL':'event_otherC_activityNameNL', #Same as activity name in english, maybe drop
    'concept:name':'event_activity_concept_name', #Activity
    'question':'event_otherC_question', #change EMPTY and other to NA
    'dateFinished':'event_otherN_dateFinished', 
    'action_code':'event_otherC_action_code', #The same as activity, drop 
    'activityNameEN':'event_otherC_activityNameEN',
    'planned':'event_otherN_planned', 
    'lifecycle:transition':'case_otherC_lifecycle_transition', #All are complete, maybe drop
    'time:timestamp':'event_timestamp_time_timestamp', #Timestamp
    'case:Includes_subCases':'case_otherC_case_Includes_subCases',
    'case:concept:name':'caseID_case_concept_name', #CaseID 
    'case:Responsible_actor':'case_otherN_case_Responsible_actor', 
    'case:endDate':'case_otherN_case_endDate', 
    'case:caseStatus':'case_otherC_case_caseStatus', 
    'case:parts':'case_otherC_case_parts', 
    'case:caseProcedure':'case_otherC_case_caseProcedure', #69% missing values maybe drop
    'case:last_phase':'case_otherC_case_last_phase', 
    'case:case_type':'case_otherN_case_case_type', #All are 55769, maybe drop
    'case:startDate':'case_otherN_case_startDate',
    'case:requestComplete':'case_otherC_case_requestComplete', #True or false values 
    'case:SUMleges':'case_otherN_case_SUMleges',  
    'case:IDofConceptCase':'case_otherN_case_IDofConceptCase', #61% missing values maybe drop
    'case:termName':'case_otherC_case_termName', #90% missing values maybe drop 
    'case:landRegisterID':'case_otherN_case_landRegisterID', #74% missing values maybe drop
    'dueDate':'event_otherN_dueDate', #99% missing values maybe drop 
    'dateStop':'case_otherN_dateStop' #99% missing values maybe drop
}, inplace=True)

municipality_3.rename(columns={
    'question':'event_otherC_question', #change EMPTY and other to NA
    'dateFinished':'event_otherN_dateFinished',  
    'dueDate':'event_otherN_dueDate', #94% missing values maybe drop 
    'action_code':'event_otherC_action_code', #The same as activity, drop
    'activityNameEN':'event_otherC_activityNameEN',
    'planned':'event_otherN_planned', 
    'time:timestamp':'event_timestamp_time_timestamp', #Timestamp
    'monitoringResource':'event_otherN_monitoringResource', 
    'org:resource':'event_otherN_org_resource',
    'activityNameNL':'event_otherC_activityNameNL', #Same as activity name in english, maybe drop
    'concept:name':'event_activity_concept_name', #Activity
    'lifecycle:transition':'case_otherC_lifecycle_transition', #All are complete, maybe drop
    'case:Includes_subCases':'case_otherC_case_Includes_subCases', 
    'case:concept:name':'caseID_case_concept_name', #CaseID 
    'case:Responsible_actor':'case_otherN_case_Responsible_actor', 
    'case:caseStatus':'case_otherC_case_caseStatus', 
    'case:last_phase':'case_otherC_case_last_phase', 
    'case:case_type':'case_otherN_case_case_type', #All are 55769, maybe drop
    'case:termName':'case_otherC_case_termName', #14% missing values
    'case:startDate':'case_otherN_case_startDate',
    'case:requestComplete':'case_otherC_case_requestComplete', #True or false values 
    'case:endDate':'case_otherN_case_endDate',  #6% missing values
    'case:parts':'case_otherC_case_parts', #2% missing values
    'case:SUMleges':'case_otherN_case_SUMleges',  #34% missing values
    'case:caseProcedure':'case_otherC_case_caseProcedure', #86% missing values maybe drop
    'case:IDofConceptCase':'case_otherN_case_IDofConceptCase', #41% missing values maybe drop
    'case:endDatePlanned':'case_otherN_case_endDatePlanned', #98% missing values maybe drop
    'dateStop':'case_otherN_dateStop', #99% missing values maybe drop
    'case:landRegisterID':'case_otherN_case_landRegisterID' #80% missing values maybe drop
}, inplace=True)

municipality_4.rename(columns={
    'question':'event_otherC_question', #change EMPTY and other to NA
    'dateFinished':'event_otherN_dateFinished',   
    'dueDate':'event_otherN_dueDate', #97% missing values maybe drop  
    'action_code':'event_otherC_action_code', #The same as activity, drop
    'activityNameEN':'event_otherC_activityNameEN',
    'planned':'event_otherN_planned', #15% missing values
    'time:timestamp':'event_timestamp_time_timestamp', #Timestamp
    'monitoringResource':'event_otherN_monitoringResource', 
    'org:resource':'event_otherN_org_resource',
    'activityNameNL':'event_otherC_activityNameNL', #Same as activity name in english, maybe drop
    'concept:name':'event_activity_concept_name', #Activity
    'lifecycle:transition':'case_otherC_lifecycle_transition', #All are complete, maybe drop
    'case:concept:name':'caseID_case_concept_name', #CaseID 
    'case:Responsible_actor':'case_otherN_case_Responsible_actor', 
    'case:endDate':'case_otherN_case_endDate', 
    'case:caseStatus':'case_otherC_case_caseStatus', 
    'case:parts':'case_otherC_case_parts', 
    'case:SUMleges':'case_otherN_case_SUMleges', #19% missing values
    'case:last_phase':'case_otherC_case_last_phase',
    'case:case_type':'case_otherN_case_case_type', #All are 55769, maybe drop
    'case:startDate':'case_otherN_case_startDate',
    'case:requestComplete':'case_otherC_case_requestComplete', #True or false values
    'case:IDofConceptCase':'case_otherN_case_IDofConceptCase', #41% missing values
    'case:termName':'case_otherC_case_termName', #84% missing values, maybe drop
    'case:caseProcedure':'case_otherC_case_caseProcedure', #85% missing values maybe drop
    'case:landRegisterID':'case_otherN_case_landRegisterID', #90% missing values maybe drop
    'case:Includes_subCases':'case_otherC_case_Includes_subCases', #17% missing values
    'dateStop':'case_otherN_dateStop', #99% missing values maybe drop
    'case:endDatePlanned':'case_otherN_case_endDatePlanned' #99% missing values maybe drop
}, inplace=True)

municipality_5.rename(columns={
    'question':'event_otherC_question', #change EMPTY and other to NA
    'dateFinished':'event_otherN_dateFinished',   
    'dueDate':'event_otherN_dueDate', #95% missing values maybe drop  
    'action_code':'event_otherC_action_code', #The same as activity, drop
    'activityNameEN':'event_otherC_activityNameEN',
    'planned':'event_otherN_planned', #17% missing values
    'time:timestamp':'event_timestamp_time_timestamp', #Timestamp
    'monitoringResource':'event_otherN_monitoringResource', 
    'org:resource':'event_otherN_org_resource',
    'activityNameNL':'event_otherC_activityNameNL', #Same as activity name in english, maybe drop
    'concept:name':'event_activity_concept_name', #Activity
    'lifecycle:transition':'case_otherC_lifecycle_transition', #All are complete, maybe drop
    'case:endDate':'case_otherN_case_endDate', 
    'case:caseStatus':'case_otherC_case_caseStatus',  
    'case:SUMleges':'case_otherN_case_SUMleges', #14% missing values 
    'case:last_phase':'case_otherC_case_last_phase',
    'case:case_type':'case_otherN_case_case_type', #All are 55769, maybe drop 
    'case:concept:name':'caseID_case_concept_name', #CaseID  
    'case:Responsible_actor':'case_otherN_case_Responsible_actor', 
    'case:landRegisterID':'case_otherN_case_landRegisterID', #2% missing values
    'case:parts':'case_otherC_case_parts',  
    'case:termName':'case_otherC_case_termName', #79% missing values, maybe drop 
    'case:startDate':'case_otherN_case_startDate',
    'case:requestComplete':'case_otherC_case_requestComplete', #True or false values 
    'case:IDofConceptCase':'case_otherN_case_IDofConceptCase', #44% missing values 
    'case:caseProcedure':'case_otherC_case_caseProcedure', #89% missing values maybe drop
    'case:Includes_subCases':'case_otherC_case_Includes_subCases', #25% missing values 
    'case:endDatePlanned':'case_otherN_case_endDatePlanned', #99% missing values maybe drop 
    'dateStop':'case_otherN_dateStop' #99% missing values maybe drop
}, inplace=True)

#%%
cols_to_drop = [
    'event_otherN_dueDate',
    'event_otherC_action_code',
    'event_otherC_activityNameNL',
    'case_otherC_lifecycle_transition',
    'case_otherN_case_case_type',
    'case_otherC_case_termName',
    'case_otherN_case_endDatePlanned',
    'case_otherN_case_IDofConceptCase',
    'case_otherN_case_landRegisterID',
    'case_otherC_case_caseProcedure',
    'case_otherN_dateStop',
    'event_otherN_dateFinished',
    'case_otherN_case_endDate',
    'case_otherC_case_Includes_subCases',
    'case_otherN_case_startDate',
    'event_otherC_question'
]

for df in [municipality_1, municipality_2, municipality_3, municipality_4, municipality_5]:
    df.drop(columns=[col for col in cols_to_drop if col in df.columns], inplace=True)
# %%
#Adjust timestamp
#2014-04-15 09:30:39+00:00 - event_otherN_planned
#2014-04-11 00:00:00+00:00 - event_timestamp_time_timestamp

datasets = [municipality_1, municipality_2, municipality_3, municipality_4, municipality_5]
cols_to_convert = ['event_otherN_planned', 'event_timestamp_time_timestamp']

for df in datasets:
    for col in cols_to_convert:
        if col in df.columns:
            # Convert to datetime with timezone
            df[col] = pd.to_datetime(df[col], format='%Y-%m-%d %H:%M:%S%z', errors='coerce')
            # Reformat to 'YYYYMMDDHHMMSS0000'
            df[col] = df[col].map(lambda x: x.strftime('%Y%m%d%H%M%S') + '0000' if pd.notnull(x) else None)
    df.reset_index(drop=True, inplace=True)


# %%

filenames = [
    'BPIC15_Municipality1.csv',
    'BPIC15_Municipality2.csv',
    'BPIC15_Municipality3.csv',
    'BPIC15_Municipality4.csv',
    'BPIC15_Municipality5.csv'
]

for i, df in enumerate(datasets):
    print(f"\nMissing values in municipality_{i+1}:")
    print(df.isna().sum())

    df.insert(0, "eventID", (df.groupby("caseID_case_concept_name").cumcount() + 1).astype(str) + "_" + df["caseID_case_concept_name"].astype(str))
    df.to_csv(outputpath + filenames[i], index=False)

#possibility here of creating a sample for testing further steps

# %%
# Sample of the 10 cases
sample = True

if sample:
    random.seed(1)
    for i, df in enumerate(datasets, 1):
        sampled_cases = random.sample(df['caseID_case_concept_name'].unique().tolist(), 10)
        sampled = df[df['caseID_case_concept_name'].isin(sampled_cases)]
        sampled.to_csv(outputpath + f'Sample_BPIC15_Municipality{i}.csv', index=False)

# %%
