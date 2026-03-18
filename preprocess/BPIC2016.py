#%%
import pandas as pd
import math,random
import time, os, csv
import numpy as np
import random


sample = False
inputpath = r'../../data/csv/BPI_2016/'
outputpath = r''

#%%
clicks_logged = pd.read_csv(inputpath+f'BPI2016_Clicks_Logged_In.csv', keep_default_na=True, sep=';', encoding='latin1')
clicks_NOT_logged = pd.read_csv(inputpath+f'BPI2016_Clicks_NOT_Logged_In.csv', keep_default_na=True, sep=';', encoding='latin1')
complaints = pd.read_csv(inputpath+f'BPI2016_Complaints.csv', keep_default_na=True, sep=';', encoding='latin1')
questions = pd.read_csv(inputpath+f'BPI2016_Questions.csv', keep_default_na=True, sep=';', encoding='latin1')
werkmap = pd.read_csv(inputpath+f'BPI2016_Werkmap_Messages.csv', keep_default_na=True, sep=';', encoding='latin1')

#drop not relevant columns
complaints = complaints.drop(columns=[
    'ComplaintSubthemeID', 'ComplaintTopicID', 'ComplaintTheme', 'ComplaintSubtheme', 'ComplaintTheme_EN', 
    'ComplaintSubtheme_EN', 'ComplaintTopic_EN'])
clicks_logged = clicks_logged.drop(columns=['VHOST','URL_FILE','REF_URL_category', 'page_action_detail', 'tip',
       'service_detail', 'xps_info', 'page_action_detail_EN',
       'service_detail_EN', 'tip_EN'])

#%%
#case ID: caseID_... 'caseID_case_concept_name'
#case level: case_...
#event level: event_...
#activity (always event level): event_activity_... 'event_activity_concept_name'
#timestamp (always event level): event_timestamp_... 'event_timestamp_time_timestamp'
#otherC: string dependent (completely string or if there are values containing different strings)
#otherN: non string dependent (completely numerical or if all the values contain the same strings)
#spaces are taken out

#complaints log not relevant, consider only clicks logged
"""
complaints.rename(columns={
    'CustomerID', #caseID
    'AgeCategory', 
    'Gender', 
    'Office_U', 
    'Office_W',
    'ComplaintDossierID',
    'ComplaintID',
    'ContactDate', #timestamp
    'ContactChannelID',
    'ComplaintThemeID',
    'ComplaintTopic', #activity
},inplace=True)
"""

clicks_logged.rename(columns={
    'CustomerID':'caseID_CustomerID', #caseID
    'AgeCategory':'case_otherN_AgeCategory', 
    'Gender':'case_otherC_Gender', 
    'Office_U':'case_otherN_Office_U', 
    'Office_W':'case_otherN_Office_W',
    'SessionID':'event_otherN_SessionID', 
    'IPID':'event_otherN_IPID', 
    'TIMESTAMP':'event_timestamp_TIMESTAMP', #timestamp
    'PAGE_NAME':'event_activity_PAGE_NAME', #activity
    'page_load_error':'event_otherN_page_load_error'
},inplace=True)
# %%
#2015-10-05 10:12:56.880000000 - event_timestamp_TIMESTAMP

clicks_logged['event_timestamp_TIMESTAMP'] = clicks_logged['event_timestamp_TIMESTAMP'].astype(str).str[:-5]
clicks_logged = clicks_logged[~pd.to_datetime(clicks_logged['event_timestamp_TIMESTAMP'], errors='coerce').isna()]
clicks_logged['event_timestamp_TIMESTAMP'] = pd.to_datetime(clicks_logged['event_timestamp_TIMESTAMP'], format='mixed')
clicks_logged['event_timestamp_TIMESTAMP'] = clicks_logged['event_timestamp_TIMESTAMP'].map(lambda x: x.strftime('%Y%m%d%H%M%S%f'))
clicks_logged = clicks_logged.reset_index(drop=True)

# %%
filename = 'BPIC16_Clicks.csv'

clicks_logged.insert(0, "eventID", (clicks_logged.groupby("caseID_CustomerID").cumcount() + 1).astype(str) + "_" + clicks_logged["caseID_CustomerID"].astype(str))
clicks_logged.to_csv(outputpath + filename, index=False)

# Sample of the 10 cases
sample = True

if sample:
    random.seed(1)
    sampled_cases = random.sample(clicks_logged['caseID_CustomerID'].unique().tolist(), 10)
    sampled = clicks_logged[clicks_logged['caseID_CustomerID'].isin(sampled_cases)]
    sampled.to_csv(outputpath + 'Sample_BPIC16_Clicks.csv', index=False)


# %%
