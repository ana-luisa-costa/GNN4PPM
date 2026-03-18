
#%%
import pandas as pd
import math,random
import time, os, csv
import numpy as np
import random


sample = False
inputpath = r'../../data/csv/BPI_2017/'
outputpath = r''

#%%
loan = pd.read_csv(inputpath+f'BPI_Challenge_2017.csv', keep_default_na=True, sep=',')
offer = pd.read_csv(inputpath+f'BPI_Challenge_2017_O.csv', keep_default_na=True, sep=',')
#drop not relevant columns
loan = loan.drop(columns=['FirstWithdrawalAmount', 'NumberOfTerms', 'Accepted', 'MonthlyCost',
       'Selected', 'CreditScore', 'OfferedAmount', 'OfferID'])
offer = offer.drop(columns=['EventOrigin','lifecycle:transition','OfferID']) #Removed OfferID since duplicated with caseID, removed eventOrigin and lifecycle since 100% of the values are the ssame

#%%
#case ID: caseID_... 'caseID_case_concept_name'
#case level: case_...
#event level: event_...
#activity (always event level): event_activity_... 'event_activity_concept_name'
#timestamp (always event level): event_timestamp_... 'event_timestamp_time_timestamp'
#otherC: string dependent (completely string or if there are values containing different strings)
#otherN: non string dependent (completely numerical or if all the values contain the same strings)
#spaces are taken out

loan.rename(columns={
    'Action':'event_OtherC_Action', 
    'org:resource':'event_OtherN_org_resource', #remove User_
    'concept:name':'event_activity_concept_name', #Activity
    'EventOrigin':'event_OtherC_EventOrigin', 
    'EventID':'event_OtherC_EventIDOther',
    'lifecycle:transition':'event_OtherC_lifecycle_transition', 
    'time:timestamp':'event_timestamp_time_timestamp', #Timestamp
    'case:LoanGoal':'case_OtherC_case_LoanGoal',
    'case:ApplicationType':'case_OtherC_case_ApplicationType', 
    'case:concept:name':'caseID_case_concept_name', #caseID #Is Application_ in everything? If yes remove it 
    'case:RequestedAmount':'case_OtherN_case_RequestedAmount'
},inplace=True)

offer.rename(columns={
    'Action':'event_OtherC_Action', 
    'org:resource':'event_OtherN_org_resource', #remove User_
    'concept:name':'event_activity_concept_name', #Activity #Does all start with O_? If yes remove it 
    'EventID':'event_OtherC_EventIDOther',
    'time:timestamp':'event_timestamp_time_timestamp', #Timestamp
    'case:concept:name':'caseID_case_concept_name', #caseID #Is Offer_ in everything? If yes remove it
    'case:MonthlyCost':'case_OtherN_case_MonthlyCost',
    'case:Selected':'case_OtherC_case_Selected',
    'case:ApplicationID':'case_OtherN_case_ApplicationID', #Is Application_ in everything? If yes remove it
    'case:FirstWithdrawalAmount':'case_OtherN_case_FirstWithdrawalAmount',
    'case:CreditScore':'case_OtherN_case_CreditScore',
    'case:OfferedAmount':'case_OtherN_case_OfferedAmount',
    'case:NumberOfTerms':'case_OtherN_case_NumberOfTerms',
    'case:Accepted':'case_OtherC_case_Accepted'
},inplace=True)

#%%
loan["event_OtherN_org_resource"] = loan["event_OtherN_org_resource"].astype(str).str.replace("^User_", "", regex=True)
loan["caseID_case_concept_name"] = loan["caseID_case_concept_name"].astype(str).str.replace("^Application_", "", regex=True)

offer["event_OtherN_org_resource"] = offer["event_OtherN_org_resource"].astype(str).str.replace("^User_", "", regex=True)
offer["event_activity_concept_name"] = offer["event_activity_concept_name"].astype(str).str.replace("^O_", "", regex=True)
offer["caseID_case_concept_name"] = offer["caseID_case_concept_name"].astype(str).str.replace("^Offer_", "", regex=True)
offer["case_OtherN_case_ApplicationID"] = offer["case_OtherN_case_ApplicationID"].astype(str).str.replace("^Application_", "", regex=True)

# %%
#2016-01-01 09:51:15.304000+00:00 - event_timestamp_time_timestamp

loan['event_timestamp_time_timestamp'] = pd.to_datetime(loan['event_timestamp_time_timestamp'], format='mixed')
loan['event_timestamp_time_timestamp'] = loan['event_timestamp_time_timestamp'].map(lambda x: x.strftime('%Y%m%d%H%M%S%f')[:-3])
loan = loan.reset_index(drop=True)

offer['event_timestamp_time_timestamp'] = pd.to_datetime(offer['event_timestamp_time_timestamp'], format='mixed')
offer['event_timestamp_time_timestamp'] = offer['event_timestamp_time_timestamp'].map(lambda x: x.strftime('%Y%m%d%H%M%S%f')[:-3])
offer = offer.reset_index(drop=True)

# %%
filename = 'BPIC17_Loan.csv'

loan.insert(0, "eventID", (loan.groupby("caseID_case_concept_name").cumcount() + 1).astype(str) + "_" + loan["caseID_case_concept_name"].astype(str))
loan.to_csv(outputpath + filename, index=False)

filename = 'BPIC17_Offer.csv'

offer.insert(0, "eventID", (offer.groupby("caseID_case_concept_name").cumcount() + 1).astype(str) + "_" + offer["caseID_case_concept_name"].astype(str))
offer.to_csv(outputpath + filename, index=False)

# Sample of the 10 cases
sample = True

if sample:
    random.seed(1)
    sampled_cases = random.sample(loan['caseID_case_concept_name'].unique().tolist(), 10)
    sampled = loan[loan['caseID_case_concept_name'].isin(sampled_cases)]
    sampled.to_csv(outputpath + 'Sample_BPIC17_Loan.csv', index=False)
    sampled = offer[offer['caseID_case_concept_name'].isin(sampled_cases)]
    sampled.to_csv(outputpath + 'Sample_BPIC17_Offer.csv', index=False)

