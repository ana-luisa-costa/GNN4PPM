#%%
import pandas as pd
import math,random
import time, os, csv
import numpy as np
import random


sample = False
inputpath = r'../../data/csv/BPI_2012/'
outputpath = r''

#%%
application = pd.read_csv(inputpath+f'BPI_Challenge_2012.csv', keep_default_na=True, sep=',')

#%%
#case ID: caseID_...
#case level: case_...
#event level: event_...
#activity (always event level): event_activity_...
#timestamp (always event level): event_timestamp_...
#otherC: string dependent (completely string or if there are values containing different strings)
#otherN: non string dependent (completely numerical or if all the values contain the same strings)
#spaces are taken out

application.rename(columns={
    'org:resource':'event_otherN_org_resource', #18010 values missing, 7%
    'lifecycle:transition':'event_otherC_lifecycle_transition',
    'concept:name':'event_activity_concept_name', #activity
    'time:timestamp':'event_timestamp_time_timestamp', #timestamp
    'case:REG_DATE':'case_otherN_case_REG_DATE',
    'case:concept:name':'caseID_case_concept_name', #caseID
    'case:AMOUNT_REQ':'case_otherN_case_AMOUNT_REQ'
},inplace=True)
# %%
#2011-10-01 00:38:44.546000+00:00 - event:activity:timestamp
#2011-10-01 00:38:44.546000+00:00 - case:otherN:case:REG_DATE

for col in ['event_timestamp_time_timestamp', 'case_otherN_case_REG_DATE']:
    application[col] = pd.to_datetime(application[col], format='mixed', utc=True)
    application[col] = application[col].map(lambda x: x.strftime('%Y%m%d%H%M%S') + x.strftime('%f')[:4]
        if x.microsecond > 0
        else x.strftime('%Y%m%d%H%M%S') + '0000')
application = application.reset_index(drop=True)

# %%
subprocess_application = application[application['event_activity_concept_name'].str.startswith('A')].copy()
subprocess_work = application[application['event_activity_concept_name'].str.startswith('W')].copy()
subprocess_offer = application[application['event_activity_concept_name'].str.startswith('O')].copy()


# %%
logs = {
    'Application': application,
    'Subprocess_Application': subprocess_application,
    'Subprocess_Work': subprocess_work,
    'Subprocess_Offer': subprocess_offer
}

for name, df in logs.items():
    df.insert(0, "eventID", (df.groupby("caseID_case_concept_name").cumcount() + 1).astype(str) + "_" + df["caseID_case_concept_name"].astype(str))
    df.to_csv(outputpath + f"BPIC12_{name}.csv", index=False)

#possibility here of creating a sample for testing further steps

# %%
sample = True

if sample:
    logs = {
        'Application': application,
        'Subprocess_Application': subprocess_application,
        'Subprocess_Work': subprocess_work,
        'Subprocess_Offer': subprocess_offer
    }

    random.seed(1)
    sampled_cases = random.sample(application['caseID_case_concept_name'].unique().tolist(), 10)

    for name, df in logs.items():
        sampled = df[df['caseID_case_concept_name'].isin(sampled_cases)]
        sampled.to_csv(outputpath + f"Sample_BPIC12_{name}.csv", index=False)
# %%
