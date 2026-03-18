#%%
import pandas as pd
import math,random
import time, os, csv
import numpy as np


sample = False
inputpath = r'../../data/csv/BPI_2013/'
outputpath = r''


closedprob = pd.read_csv(inputpath+f'BPI_Challenge_2013_closed.csv', keep_default_na=True, sep=',')
incidentsprob = pd.read_csv(inputpath+f'BPI_Challenge_2013_incidents.csv', keep_default_na=True, sep=',')
openprob = pd.read_csv(inputpath+f'BPI_Challenge_2013_open.csv', keep_default_na=True, sep=',')

#%%
closedprob.rename(columns={
    'org:group':'event_otherC_org_group',
    'resource country':'event_otherC_resourcecountry',
    'organization country':'case_otherC_organizationcountry',
    'org:resource':'event_otherC_org_resource',
    'organization involved':'event_otherC_organizationinvolved',
    'org:role':'event_otherC_org_role', #missing 31% of the data, 2078 values
    'concept:name':'event_activity_concept_name', #activity#activity
    'impact':'case_otherC_impact', #4 distinct values: High, Medium, Low, Other
    'product':'case_otherN_product', #substitute 2 values 'OTHERS' to missing values
    'lifecycle:transition':'event_otherC_lifecycle_transition',
    'time:timestamp':'event_timestamp_time_timestamp', #timestamp
    'case:concept:name':'caseID_case_concept_name' #caseID
},inplace=True)

incidentsprob.rename(columns={
    'org:group':'event_otherC_org_group',
    'resource country':'event_otherC_resourcecountry',
    'organization country':'case_otherC_organizationcountry',
    'org:resource':'event_otherC_org_resource',
    'organization involved':'event_otherC_organizationinvolved',
    'org:role':'event_otherC_org_role', #missing 11% of the data, 6950 values
    'concept:name':'event_activity_concept_name', #activity
    'impact':'case_otherC_impact',
    'product':'case_otherN_product', #substitute 61 values 'OTHERS' or '- -' or 'OTHER' to missing values
    'lifecycle:transition':'event_otherC_lifecycle_transition',
    'time:timestamp':'event_timestamp_time_timestamp',  #timestamp
    'case:concept:name':'caseID_case_concept_name' #caseID
},inplace=True)

openprob.rename(columns={
    'org:group':'event_otherC_org_group',
    'resource country':'event_otherC_resourcecountry',
    'org:resource':'event_otherC_org_resource',
    'oranization country':'case_otherC_organizationcountry',
    'org:role':'event_otherC_org_role', #22% of missing values (506)
    'concept:name':'event_activity_concept_name', #activity
    'impact':'case_otherC_impact',
    'product':'case_otherN_product', #substitute 1 value 'OTHERS' to missing values
    'time:timestamp':'event_timestamp_time_timestamp',  #timestamp
    'lifecycle:transition':'event_otherC_lifecycle_transition',
    'case:concept:name':'caseID_case_concept_name' #caseID
},inplace=True)


#replace unknown values to NA
closedprob = closedprob.replace('OTHERS', np.nan)
incidentsprob = incidentsprob.replace(['OTHERS','- -','OTHER'], np.nan)
openprob = openprob.replace('OTHERS', np.nan)

#2006-01-11 14:49:42+00:00 - event:timestamp:time:timestamp

for df in [closedprob, incidentsprob, openprob]:
    df['event_timestamp_time_timestamp'] = pd.to_datetime(
        df['event_timestamp_time_timestamp'], format='%Y-%m-%d %H:%M:%S%z'
    ).map(lambda x: x.strftime('%Y%m%d%H%M%S') + '0000')


#remove '-' in caseID
for df in [closedprob, incidentsprob, openprob]:
    df['caseID_case_concept_name'] = df['caseID_case_concept_name'].astype(str).str.replace('-', '', regex=False)


datasets = [
    (closedprob, 'BPIC13_ClosedProblems.csv'),
    (incidentsprob, 'BPIC13_Incidents.csv'),
    (openprob, 'BPIC13_OpenProblems.csv')
]

for df, filename in datasets:
    df.insert(0, "eventID", (df.groupby("caseID_case_concept_name").cumcount() + 1).astype(str) + "_" + df["caseID_case_concept_name"].astype(str))
    df.to_csv(outputpath + filename, index=False)

#possibility here of creating a sample for testing further steps

# %%
# Sample of the 10 cases
sample = True

if sample:
    random.seed(1)

    logs = {
        'Sample_BPIC13_ClosedProblems.csv': closedprob,
        'Sample_BPIC13_Incidents.csv': incidentsprob,
        'Sample_BPIC13_OpenProblems.csv': openprob
    }

    for filename, df in logs.items():
        sampled_cases = random.sample(df['caseID_case_concept_name'].unique().tolist(), 10)
        sampled = df[df['caseID_case_concept_name'].isin(sampled_cases)]
        sampled.to_csv(outputpath + filename, index=False)

