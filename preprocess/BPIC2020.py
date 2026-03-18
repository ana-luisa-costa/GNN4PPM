#%%
import pandas as pd
import math,random
import time, os, csv
import numpy as np
import random


sample = False
inputpath = r'../../data/csv/BPI_2020/'
outputpath = r''

#%%
domestic = pd.read_csv(inputpath+f'BPI_Challenge_2020_DomesticDeclarations.csv', keep_default_na=True, sep=',')
international = pd.read_csv(inputpath+f'BPI_Challenge_2020_InternationalDeclarations.csv', keep_default_na=True, sep=',')
permit = pd.read_csv(inputpath+f'BPI_Challenge_2020_PermitLog.csv', keep_default_na=True, sep=',')
prepaid = pd.read_csv(inputpath+f'BPI_Challenge_2020_PrepaidTravelCost.csv', keep_default_na=True, sep=',')
request = pd.read_csv(inputpath+f'BPI_Challenge_2020_RequestForPayment.csv', keep_default_na=True, sep=',')

#%%
#Drop not relevant columns in international
#'case:Permit travel permit number', #drop, same as travel permit number
#'case:RequestedAmount', #drop Check if its the same as amount
#'case:Permit TaskNumber', #drop Too many Unkown values
#'case:OriginalAmount', #drop Check if its the same as amount
#'case:Permit ProjectNumber', #drop Too many Unkown values
#'case:id', #drop Same as ca:concept:name
#'case:Permit id', #drop Same as Permit ID
domestic = domestic.drop(columns=['case:id','case:BudgetNumber'])
international = international.drop(columns=['case:Permit ActivityNumber','case:Permit travel permit number', 'case:RequestedAmount', 'case:Permit TaskNumber', 'case:OriginalAmount', 'case:Permit ProjectNumber', 'case:Permit id', 'case:id'])
permit = permit.drop(columns=['case:TaskNumber','case:ProjectNumber','case:dec_id_0','case:ActivityNumber','case:id','case:DeclarationNumber_0','case:dec_id_5', 'case:dec_id_6', 'case:dec_id_3', 'case:dec_id_4', 'case:dec_id_1', 'case:dec_id_2', 'case:DeclarationNumber_10', 'case:RequestedAmount_16', 'case:RequestedAmount_14', 'case:RequestedAmount_15', 'case:dec_id_9', 'case:RequestedAmount_12', 'case:DeclarationNumber_14', 'case:DeclarationNumber_13', 'case:RequestedAmount_13', 'case:dec_id_7', 'case:RequestedAmount_10', 'case:DeclarationNumber_12', 'case:dec_id_8', 'case:DeclarationNumber_11', 'case:RequestedAmount_11', 'case:DeclarationNumber_16', 'case:DeclarationNumber_15', 'case:DeclarationNumber_8', 'case:DeclarationNumber_9', 'case:DeclarationNumber_4', 'case:DeclarationNumber_5', 'case:DeclarationNumber_6', 'case:DeclarationNumber_7', 'case:RequestedAmount_4', 'case:DeclarationNumber_1', 'case:RequestedAmount_3', 'case:DeclarationNumber_2', 'case:RequestedAmount_2', 'case:RequestedAmount_1', 'case:DeclarationNumber_3', 'case:RequestedAmount_8', 'case:RequestedAmount_7', 'case:RequestedAmount_6', 'case:RequestedAmount_5', 'case:RequestedAmount_9', 'case:dec_id_16', 'case:dec_id_13', 'case:dec_id_12', 'case:dec_id_15', 'case:dec_id_14', 'case:dec_id_11', 'case:dec_id_10', 'case:Activity_1', 'case:Activity_0', 'case:RfpNumber_0', 'case:OrganizationalEntity_0', 'case:Rfp_id_0', 'case:RfpNumber_1', 'case:OrganizationalEntity_1', 'case:Cost Type_1', 'case:Cost Type_0', 'case:Task_1', 'case:Task_0', 'case:Project_0', 'case:Rfp_id_1', 'case:Project_1', 'case:Activity_3', 'case:Activity_2', 'case:Cost Type_3', 'case:Cost Type_2', 'case:RfpNumber_2', 'case:RfpNumber_3', 'case:OrganizationalEntity_2', 'case:OrganizationalEntity_3', 'case:Project_2', 'case:Project_3', 'case:Rfp_id_3', 'case:Rfp_id_2', 'case:Task_3', 'case:Task_2', 'case:Rfp_id_10', 'case:Rfp_id_11', 'case:Rfp_id_12', 'case:Rfp_id_13', 'case:Rfp_id_14', 'case:Project_11', 'case:Project_12', 'case:Project_10', 'case:Project_13', 'case:Project_14', 'case:Cost Type_7', 'case:Cost Type_6', 'case:Cost Type_9', 'case:Cost Type_8', 'case:Cost Type_5', 'case:Cost Type_4', 'case:OrganizationalEntity_8', 'case:OrganizationalEntity_9', 'case:Task_10', 'case:OrganizationalEntity_6', 'case:Task_11', 'case:OrganizationalEntity_7', 'case:Task_12', 'case:Task_13', 'case:Task_14', 'case:RfpNumber_10', 'case:RfpNumber_12', 'case:RfpNumber_11', 'case:OrganizationalEntity_4', 'case:Project_6', 'case:RfpNumber_14', 'case:OrganizationalEntity_5', 'case:Project_7', 'case:RfpNumber_13', 'case:Project_8', 'case:Project_9', 'case:Project_4', 'case:Project_5', 'case:Activity_12', 'case:Activity_11', 'case:Activity_14', 'case:Activity_13', 'case:Activity_10', 'case:OrganizationalEntity_14', 'case:OrganizationalEntity_13', 'case:RfpNumber_8', 'case:RfpNumber_9', 'case:RfpNumber_6', 'case:RfpNumber_7', 'case:RfpNumber_4', 'case:RfpNumber_5', 'case:OrganizationalEntity_12', 'case:OrganizationalEntity_11', 'case:OrganizationalEntity_10', 'case:Rfp_id_7', 'case:Rfp_id_8', 'case:Rfp_id_5', 'case:Rfp_id_6', 'case:Rfp_id_4', 'case:Rfp_id_9', 'case:Activity_9', 'case:Activity_8', 'case:Activity_5', 'case:Activity_4', 'case:Activity_7', 'case:Activity_6', 'case:Cost Type_13', 'case:Cost Type_14', 'case:Cost Type_10', 'case:Cost Type_11', 'case:Cost Type_12', 'case:Task_5', 'case:Task_4', 'case:Task_9', 'case:Task_8', 'case:Task_7', 'case:Task_6'])
prepaid = prepaid.drop(columns=['case:Permit ActivityNumber','case:Project','case:Permit travel permit number','case:Rfp_id', 'case:Permit TaskNumber', 'case:Permit ProjectNumber', 'case:Task', 'case:Activity', 'case:Cost Type'])
request = request.drop(columns=['case:Rfp_id', 'case:Task', 'case:Cost Type', 'case:Activity'])

#%%
#case ID: caseID_... 'caseID_case_concept_name'
#case level: case_...
#event level: event_...
#activity (always event level): event_activity_... 'event_activity_concept_name'
#timestamp (always event level): event_timestamp_... 'event_timestamp_time_timestamp'
#otherC: string dependent (completely string or if there are values containing different strings)
#otherN: non string dependent (completely numerical or if all the values contain the same strings)
#spaces are taken out

domestic.rename(columns={
    'id':'event_OtherC_id', 
    'org:resource':'event_OtherC_org_resource', 
    'concept:name':'event_activity_concept_name', #Activity
    'time:timestamp':'event_timestamp_time_timestamp', #Timestamp
    'org:role':'event_OtherC_org_role', 
    'case:concept:name':'caseID_case_concept_name', #CaseID #remove 'declaration '
    'case:DeclarationNumber':'case_OtherN_case_DeclarationNumber', #remove 'declaration number '
    'case:Amount':'case_Other_N_case_Amount'
},inplace=True)

international.rename(columns={
    'id':'event_OtherC_id', 
    'org:resource':'event_OtherC_org_resource', 
    'concept:name':'event_activity_concept_name', #Activity
    'time:timestamp':'event_timestamp_time_timestamp', #Timestamp
    'org:role':'event_OtherC_org_role', 
    'case:DeclarationNumber':'case_OtherN_case_DeclarationNumber', #remove 'declaration number '
    'case:Amount':'case_OtherN_case_Amount',
    'case:Permit BudgetNumber':'case_OtherN_case_Permit_BudgetNumber', #remove 'budget '
    'case:concept:name':'caseID_case_concept_name', #CaseID #remove 'declaration '
    'case:Permit OrganizationalEntity':'case_OtherN_case_Permit_OrganizationalEntity', #remove 'organizational unit '
    'case:travel permit number':'case_OtherN_case_travel_permit_number', #remove 'travel permit number '
    'case:Permit RequestedBudget': 'case_OtherN_case_Permit_RequestedBudget', 
    'case:Permit ID':'case_OtherN_case_Permit_ID', #remove 'travel permit '
    'case:BudgetNumber':'case_OtherN_case_BudgetNumber', #remove 'budget '
    'case:AdjustedAmount':'case_OtherN_case_AdjustedAmount'
}, inplace=True)

permit.rename(columns={
    'id':'event_OtherC_id', 
    'org:resource':'event_OtherC_org_resource', 
    'concept:name':'event_activity_concept_name', #Activity
    'time:timestamp':'event_timestamp_time_timestamp', #Timestamp
    'org:role':'event_OtherC_org_role', 
    'case:OrganizationalEntity':'case_OtherN_case_OrganizationalEntity', #remove 'organizational unit '
    'case:TotalDeclared':'case_OtherN_case_TotalDeclared', 
    'case:concept:name':'caseID_case_concept_name', #CaseID
    'case:RequestedAmount_0':'case_OtherN_case_RequestedAmount_0', 
    'case:Overspent':'case_OtherC_case_Overspent', 
    'case:travel permit number':'case_OtherN_case_travel_permit_number', #remove 'travel permit number '
    'case:RequestedBudget':'case_OtherN_case_RequestedBudget', 
    'case:BudgetNumber':'case_OtherN_case_BudgetNumber', #remove 'budget '
    'case:OverspentAmount': 'case_OtherN_case_OverspentAmount'
}, inplace=True)

prepaid.rename(columns={
    'id':'event_OtherC_id', 
    'org:resource':'event_OtherC_org_resource', 
    'concept:name':'event_activity_concept_name', #Activity
    'time:timestamp':'event_timestamp_time_timestamp', #Timestamp
    'org:role':'event_OtherC_org_role', 
    'case:OrganizationalEntity':'case_OtherN_case_OrganizationalEntity', #remove 'organizational unit '
    'case:RequestedAmount':'case_OtherN_case_RequestedAmount', 
    'case:Permit BudgetNumber':'case_OtherN_case_Permit_BudgetNumber', #remove 'budget '
    'case:concept:name':'caseID_case_concept_name', #CaseID #remove request for payment
    'case:Permit OrganizationalEntity':'case_OtherN_case_Permit_OrganizationalEntity', #remove 'organizational unit '
    'case:Permit RequestedBudget': 'case_OtherN_case_Permit_RequestedBudget', 
    'case:Permit id':'case_OtherN_case_Permit_id', #remove 'travel permit ', 
    'case:RfpNumber':'case_OtherN_case_RfpNumber', #remove 'request for payment number ' 
}, inplace=True)

request.rename(columns={
    'id':'event_OtherC_id', 
    'org:resource':'event_OtherC_org_resource', 
    'concept:name':'event_activity_concept_name', #Activity
    'time:timestamp':'event_timestamp_time_timestamp', #Timestamp
    'org:role':'event_OtherC_org_role', 
    'case:Project':'case_OtherN_case_Project', #remove 'project ' 
    'case:concept:name':'caseID_case_concept_name', #CaseID
    'case:OrganizationalEntity':'case_OtherN_case_OrganizationalEntity', #remove 'organizational unit '
    'case:RequestedAmount':'case_OtherN_case_RequestedAmount', 
    'case:RfpNumber':'case_OtherN_case_RfpNumber', #remove 'request for payment number ' 
}, inplace=True)

#%%
#Remove unecessary names from some columns

domestic["case_OtherN_case_DeclarationNumber"] = domestic["case_OtherN_case_DeclarationNumber"].astype(str).str.replace("^declaration number ", "", regex=True)
domestic["caseID_case_concept_name"] = domestic["caseID_case_concept_name"].astype(str).str.replace("^declaration ", "", regex=True)

international["case_OtherN_case_DeclarationNumber"] = international["case_OtherN_case_DeclarationNumber"].astype(str).str.replace("^declaration number ", "", regex=True)
international["case_OtherN_case_Permit_OrganizationalEntity"] = international["case_OtherN_case_Permit_OrganizationalEntity"].astype(str).str.replace("^organizational unit ", "", regex=True)
international["case_OtherN_case_travel_permit_number"] = international["case_OtherN_case_travel_permit_number"].astype(str).str.replace("^travel permit number ", "", regex=True)
international["case_OtherN_case_BudgetNumber"] = international["case_OtherN_case_BudgetNumber"].astype(str).str.replace("^budget ", "", regex=True)
international["case_OtherN_case_Permit_ID"] = international["case_OtherN_case_Permit_ID"].astype(str).str.replace("^travel permit ", "", regex=True)
international["case_OtherN_case_Permit_BudgetNumber"] = international["case_OtherN_case_Permit_BudgetNumber"].astype(str).str.replace("^budget ", "", regex=True)
international["caseID_case_concept_name"] = domestic["caseID_case_concept_name"].astype(str).str.replace("^declaration ", "", regex=True)

permit["case_OtherN_case_OrganizationalEntity"] = permit["case_OtherN_case_OrganizationalEntity"].astype(str).str.replace("^organizational unit ", "", regex=True)
permit["case_OtherN_case_travel_permit_number"] = permit["case_OtherN_case_travel_permit_number"].astype(str).str.replace("^travel permit number ", "", regex=True)
permit["case_OtherN_case_BudgetNumber"] = permit["case_OtherN_case_BudgetNumber"].astype(str).str.replace("^budget ", "", regex=True)
permit["caseID_case_concept_name"] = domestic["caseID_case_concept_name"].astype(str).str.replace("^travel permit ", "", regex=True)

prepaid["case_OtherN_case_OrganizationalEntity"] = prepaid["case_OtherN_case_OrganizationalEntity"].astype(str).str.replace("^organizational unit ", "", regex=True)
prepaid["case_OtherN_case_Permit_BudgetNumber"] = prepaid["case_OtherN_case_Permit_BudgetNumber"].astype(str).str.replace("^budget ", "", regex=True)
prepaid["case_OtherN_case_RfpNumber"] = prepaid["case_OtherN_case_RfpNumber"].astype(str).str.replace("^request for payment number ", "", regex=True)
prepaid["case_OtherN_case_Permit_id"] = prepaid["case_OtherN_case_Permit_id"].astype(str).str.replace("^travel permit ", "", regex=True)
prepaid["case_OtherN_case_Permit_OrganizationalEntity"] = prepaid["case_OtherN_case_Permit_OrganizationalEntity"].astype(str).str.replace("^organizational unit ", "", regex=True)
prepaid["caseID_case_concept_name"] = domestic["caseID_case_concept_name"].astype(str).str.replace("^request for payment ", "", regex=True)

request["case_OtherN_case_OrganizationalEntity"] = request["case_OtherN_case_OrganizationalEntity"].astype(str).str.replace("^organizational unit ", "", regex=True)
request["case_OtherN_case_RfpNumber"] = request["case_OtherN_case_RfpNumber"].astype(str).str.replace("^request for payment number ", "", regex=True)
request["caseID_case_concept_name"] = request["caseID_case_concept_name"].astype(str).str.replace("^request for payment ", "", regex=True)
request["case_OtherN_case_Project"] = request["case_OtherN_case_Project"].astype(str).str.replace("^project ", "", regex=True)

#%%
#Drop in all datasets all rows with NA in caseID
domestic = domestic.dropna(subset=['caseID_case_concept_name'])
international = international.dropna(subset=['caseID_case_concept_name'])
permit = permit.dropna(subset=['caseID_case_concept_name'])
prepaid = prepaid.dropna(subset=['caseID_case_concept_name'])
request = request.dropna(subset=['caseID_case_concept_name'])

# %%
#Adjust timestamp
#2017-01-09 08:49:50+00:00 - event_timestamp_time_timestamp

datasets = [domestic, international, permit, prepaid, request]
cols_to_convert = ['event_timestamp_time_timestamp']

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
    'BPIC20_Domestic.csv',
    'BPIC20_International.csv',
    'BPIC20_Permit.csv',
    'BPIC20_Prepaid.csv',
    'BPIC20_Request.csv'
]

for i, df in enumerate(datasets):
    print(f"\nMissing values in challenge_{i+1}:")
    print(df.isna().sum())

    df.insert(0, "eventID", (df.groupby("caseID_case_concept_name").cumcount() + 1).astype(str) + "_" + df["caseID_case_concept_name"].astype(str))
    df.to_csv(outputpath + filenames[i], index=False)

#possibility here of creating a sample for testing further steps

# %%
# Sample of the 10 cases
sample = True

if sample:
    random.seed(1)
    for i, df in enumerate(datasets):
        sampled_cases = random.sample(df['caseID_case_concept_name'].unique().tolist(), 10)
        sampled = df[df['caseID_case_concept_name'].isin(sampled_cases)]
        sampled.to_csv(outputpath + f'Sample_{filenames[i]}', index=False)

# %%
