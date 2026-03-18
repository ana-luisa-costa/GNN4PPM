#%%
import pandas as pd
import math,random
import time, os, csv
import numpy as np


sample = False
inputpath = r'../../data/csv/BPI_2014/'
outputpath = r''

change = pd.read_csv(inputpath+f'Detail_Change.csv', keep_default_na=True, sep=';')
incident = pd.read_csv(inputpath+f'Detail_Incident.csv', keep_default_na=True, sep=';')
incidentDetail = pd.read_csv(inputpath+f'Detail_Incident_Activity.csv', keep_default_na=True, sep=';')
interaction = pd.read_csv(inputpath+f'Detail_Interaction.csv', keep_default_na=True, sep=';')

incident.drop(incident.iloc[:, 28:78], inplace=True, axis=1) #drop all empty columns
incident = incident.dropna(thresh=19) #drops all 'nan-only' rows

#%%
#case ID: caseID_...
#case level: case_...
#event level: event_...
#activity (always event level): event_activity_...
#timestamp (always event level): event_timestamp_...
#otherC: string dependent (completely string or if there are values containing different strings)
#otherN: non string dependent (completely numerical or if all the values contain the same strings)
#spaces are taken out

incidentDetail.rename(columns={
    'Incident ID':'caseID_IncidentID', #caseID
    'DateStamp':'event_timestamp_DateStamp', #timestamp
    'IncidentActivity_Number':'event_otherN_IncidentActivity_Number',
    'IncidentActivity_Type':'event_activity_IncidentActivity_Type', #activity
    'Assignment Group':'event_otherN_AssignmentGroup',
    'KM number':'case_otherN_KMnumber',
    'Interaction ID':'case_otherN_InteractionID' ## Dorp column #fill 5643 distinct values ['#N/B'] missing. Update: filled some and now 780 are missing with 28 distinct IncidentIDs that could not be correlated anywhere. In interaction is called MULTIVALUE
}, inplace=True)

#interaction ID is also here unique, therefore not an event log, needs to be combined to form a log
interaction.rename(columns={
    'CI Name (aff)': 'case_otherC_CIName(aff)',
    'CI Type (aff)': 'case_otherC_CIType(aff)',
    'CI Subtype (aff)': 'case_otherC_CISubtype(aff)',
    'Service Component WBS (aff)': 'case_otherN_ServiceComponentWBS(aff)',
    'Interaction ID': 'case_otherN_InteractionID', #possible caseID if there was caseID
    'Status': 'case_otherC_Status', #dropcolumn
    'Impact': 'case_otherN_Impact', #dropcolumn
    'Urgency': 'case_otherN_Urgency', #dropcolumn
    'Priority': 'case_otherN_Priority', #dropcolumn
    'Category': 'case_otherC_Category', #dropcolumn
    'KM number': 'case_otherN_KMnumber',
    'Open Time (First Touch)': 'case_otherN_OpenTime(FirstTouch)', #timestamp
    'Close Time': 'case_otherN_CloseTime', #timestamp
    'Closure Code': 'case_otherC_ClosureCode',
    'First Call Resolution': 'case_otherC_FirstCallResolution',
    'Handle Time (secs)': 'case_otherN_HandleTime(secs)',
    'Related Incident': 'case_otherN_RelatedIncident'
}, inplace=True)

change.rename(columns={
    'CI Name (aff)': 'event_otherC_CIName(aff)',
    'CI Type (aff)': 'event_otherC_CIType(aff)',
    'CI Subtype (aff)': 'event_activity_CISubtype(aff)', #activity
    'Service Component WBS (aff)': 'event_otherN_ServiceComponentWBS(aff)',
    'Change ID': 'caseID_ChangeID', #caseID
    'Change Type': 'case_otherC_ChangeType', 
    'Risk Assessment': 'event_otherC_RiskAssessment',
    'Emergency Change': 'case_otherC_EmergencyChange',
    'CAB-approval needed': 'case_otherC_CAB-approvalneeded',
    'Planned Start': 'event_otherN_PlannedStart',
    'Planned End': 'event_otherN_PlannedEnd',
    'Scheduled Downtime Start': 'case_otherN_ScheduledDowntimeStart', #dropcolumn
    'Scheduled Downtime End': 'case_otherN_ScheduledDowntimeEnd', #dropcolumn
    'Actual Start': 'event_timestamp_ActualStart', #timestamp
    'Actual End': 'event_timestamp_ActualEnd', #timestamp
    'Requested End Date': 'event_otherN_RequestedEndDate',
    'Change record Open Time': 'case_otherN_ChangerecordOpenTime',
    'Change record Close Time': 'event_otherN_ChangerecordCloseTime', #many distinct values therefore: event level
    'Originated from': 'event_otherC_Originatedfrom',
    '# Related Interactions': 'case_otherN_#RelatedInteractions', #dropcolumn
    '# Related Incidents': 'case_otherN_#RelatedIncidents' #dropcolumn #one distinct value in Change ID C00015040 considered typo therefore: case level
}, inplace=True)

#maybe this log is not relevant because there is no caseID, if caseID is considered IncidentID, everything is case level
#the problem is that all IncidentID are unique
incident.rename(columns={  
    'CI Name (aff)': 'case_otherC_CIName(aff)', ## Add items in the log
    'CI Type (aff)': 'case_otherC_CIType(aff)', ## Add items in the log
    'CI Subtype (aff)': 'case_otherC_CISubtype(aff)', ## Add items in the log
    'Service Component WBS (aff)': 'case_otherN_ServiceComponentWBS(aff)',
    'Incident ID': 'case_otherN_IncidentID', #possible caseID if there was caseID ## Add items in the log
    'Status': 'case_otherC_Status', #dropcolumn
    'Impact': 'case_otherN_Impact', #dropcolumn  ## Add items in the log
    'Urgency': 'case_otherN_Urgency', #dropcolumn  ## Add items in the log
    'Priority': 'case_otherN_Priority', #dropcolumn  ## Add items in the log
    'Category': 'case_otherC_Category', #dropcolumn
    'KM number': 'case_otherN_KMnumber',
    'Alert Status': 'case_otherC_AlertStatus',
    '# Reassignments': 'case_otherN_#Reassignments',
    'Open Time': 'case_otherN_OpenTime', #possible timestamp if there was caseID
    'Reopen Time': 'case_otherN_ReopenTime',
    'Resolved Time': 'case_otherN_ResolvedTime', #possible timestamp if there was caseID
    'Close Time': 'case_otherN_CloseTime',  
    'Handle Time (Hours)': 'case_otherN_HandleTime(Hours)',
    'Closure Code': 'event_otherC_ClosureCode', ## Add items in the log
    '# Related Interactions': 'case_otherN_#RelatedInteractions',
    'Related Interaction': 'case_otherN_RelatedInteraction',
    '# Related Incidents': 'case_otherN_#RelatedIncidents',
    '# Related Changes': 'case_otherN_#RelatedChanges',
    'Related Change': 'case_otherN_RelatedChange',
    'CI Name (CBy)': 'event_otherC_CIName(CBy)', ## Add items in the log # Event level
    'CI Type (CBy)': 'event_otherC_CIType(CBy)', ## Add items in the log # Event level
    'CI Subtype (CBy)': 'event_otherC_CISubtype(CBy)', ## Add items in the log # Event level
    'ServiceComp WBS (CBy)': 'event_otherN_ServiceCompWBS(CBy)' ## Add items in the log # Event level
}, inplace=True)

#%%
# Processing Incidents Log

incidentDetail = incidentDetail.drop(columns=["case_otherN_InteractionID"])
keep_cols = [
    'case_otherC_CIName(aff)',
    'case_otherC_CIType(aff)',
    'case_otherC_CISubtype(aff)',
    'case_otherN_IncidentID',
    'case_otherN_Impact',
    'case_otherN_Urgency',
    'case_otherN_Priority',
    'event_otherC_ClosureCode',
    'event_otherC_CIName(CBy)',
    'event_otherC_CIType(CBy)',
    'event_otherC_CISubtype(CBy)',
    'event_otherN_ServiceCompWBS(CBy)'
]

incident = incident[keep_cols]
incidentDetail = incidentDetail.merge(
    incident,
    how="left",
    left_on="caseID_IncidentID",
    right_on="case_otherN_IncidentID"
)

incidentDetail.loc[
    incidentDetail["event_activity_IncidentActivity_Type"] != "Closed",
    "event_otherC_ClosureCode"
] = np.nan

incidentDetail.loc[
    incidentDetail["event_activity_IncidentActivity_Type"] != "Caused By CI",
    ["event_otherC_CIName(CBy)", "event_otherC_CIType(CBy)", "event_otherC_CISubtype(CBy)", "event_otherN_ServiceCompWBS(CBy)"]
] = np.nan

#%%

#Processing first log of IncidentDetail
# in this log there are 780 NA values in the last column case:otherN:InteractionID that i didnt take of, these values are unknown
"""
interaction_to_incident = interaction.set_index("case_otherN_RelatedIncident")["case_otherN_InteractionID"].to_dict()
incidentDetail["case_otherN_InteractionID"] = incidentDetail.apply(
    lambda row: interaction_to_incident.get(row["caseID_IncidentID"], row["case_otherN_InteractionID"]),
    axis=1
)
"""

#incidentDetail = incidentDetail.replace('#N/B', np.nan)
incidentDetail['event_timestamp_DateStamp'] = pd.to_datetime(incidentDetail['event_timestamp_DateStamp'], format='%d-%m-%Y %H:%M:%S')
incidentDetail['event_timestamp_DateStamp'] = incidentDetail['event_timestamp_DateStamp'].map(lambda x: x.strftime('%Y%m%d%H%M%S')+'0000')
incidentDetail = incidentDetail.reset_index(drop=True)

filename = 'BPIC14_Incident.csv'

incidentDetail.insert(0, "eventID", (incidentDetail.groupby("caseID_IncidentID").cumcount() + 1).astype(str) + "_" + incidentDetail["caseID_IncidentID"].astype(str))
incidentDetail.to_csv(outputpath + filename, index=False)


#Processing second log of Change
"""
for i in change.index:
    if change.at[i, 'event_timestamp_ActualStart'] != change.at[i, 'event_timestamp_ActualStart']:
        change.at[i, 'event_timestamp_ActualStart'] = change.at[i, 'case_otherN_ChangerecordOpenTime']
    if change.at[i, 'event_timestamp_ActualEnd'] != change.at[i, 'event_timestamp_ActualEnd']:
        change.at[i, 'event_timestamp_ActualEnd'] = change.at[i, 'event_otherN_ChangerecordCloseTime']
    if change.at[i, 'event_otherN_PlannedEnd'] != change.at[i, 'event_otherN_PlannedEnd']:
        change.at[i, 'event_otherN_PlannedEnd'] = change.at[i, 'event_otherN_RequestedEndDate']

change = change.drop(change.columns[[11, 12, 19, 20]], axis=1)

#Change timestamps to standardized format
cols = [
    "event_otherN_PlannedStart",
    "event_otherN_PlannedEnd",
    "event_timestamp_ActualStart",
    "event_timestamp_ActualEnd",
    "event_otherN_RequestedEndDate",
    "case_otherN_ChangerecordOpenTime",
    "event_otherN_ChangerecordCloseTime"
]
for col in cols:
    change[col] = pd.to_datetime(change[col], format='%d-%m-%Y %H:%M')
    change[col] = change[col].dt.strftime("%Y%m%d%H%M") + "000000"

change = change.reset_index(drop=True)

filename = 'BPIC14_Change.csv'

change.insert(0, "eventID", change.groupby("caseID_ChangeID").cumcount() + 1)
change.to_csv(outputpath + filename, index=False)

"""
#possibility here of creating a sample for testing further steps
#%%
sample = True

if sample:
    random.seed(1)

    logs = {
        'Sample_BPIC14_Incident.csv': (incidentDetail, 'caseID_IncidentID'),
       # 'Sample_BPIC14_Change.csv': (change, 'caseID_ChangeID'),
    }

    for filename, (df, case_col) in logs.items():
        sampled_cases = random.sample(df[case_col].unique().tolist(), 10)
        sampled = df[df[case_col].isin(sampled_cases)]
        sampled.to_csv(outputpath + filename, index=False)



# %%
