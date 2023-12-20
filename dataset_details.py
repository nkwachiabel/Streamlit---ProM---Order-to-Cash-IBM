import streamlit as st
import pandas as pd
from prom_functions import *


# @st.cache_data
# def load_data(path: str):
#     df = pd.read_csv(path)
#     return df

dataset = 'https://raw.githubusercontent.com/nkwachiabel/Streamlit---ProM---Helpdesk-log/main/dataset/finale.csv'

df = load_data(dataset)

case_id = 'Case ID'
activity = 'Activity'
timestamp = 'Complete Timestamp'
resources = 'Resource'
product = 'product'
customer = 'customer'
workgroup = 'workgroup'
first_activities = ['Assign seriousness','Insert ticket']
last_activities = ['Closed']

def case_id_column():
    return case_id

def activity_column():
    return activity

def timestamp_column():
    return timestamp

def first_activity():
    return first_activities

def last_activity():
    return last_activities

def resources_col():
    return resources

def product_col():
    return product

def customer_col():
    return customer

def workgroup_col():
    return workgroup

unique_activities = get_unique_items(df,activity_column())

df = datetime_format(df, timestamp_column())
start_time = earliest_time(df,timestamp_column())
end_time = latest_time(df,timestamp_column())

def determine_status(row):
    if row['First_Activity'] in first_activities:
        if row['Last_Activity'] in last_activities:
            return 'Closed'
        else:
            return 'Open'
    else:
        if row['Last_Activity'] in last_activities:
            return 'Closed'
        else:
            return 'Wrong first activity'

# with st.expander(":point_right: Data View"):
df2 = df.copy()
df2 = initial_dataset_csv(df2, case_id_column(), activity_column(), timestamp_column())
df2['Status'] = df2.apply(determine_status, axis=1)
# st.dataframe(df)

# df2 = df2[(df2[timestamp_column()]>=start_date) & (df2[timestamp_column()]< end_date + pd.Timedelta(days=1))].copy()
filtered_df = df2.copy()
filtered_df = filtered_df[filtered_df['First_Activity'].isin(first_activities) & filtered_df['Last_Activity'].isin(last_activities)]
filtered_df = initial_dataset_filtered_df(filtered_df, case_id_column(), activity_column(), timestamp_column())

def full_dataset():
    return df

def full_dataset_edited():
    return df2

def filtered_dataset():
    return filtered_df