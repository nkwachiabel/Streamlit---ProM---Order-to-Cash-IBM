import streamlit as st
import pandas as pd
from prom_functions import load_parquet, datetime_format, earliest_time, latest_time, get_unique_items


# # @st.cache_data
# # def load_data(path: str):
# #     df = pd.read_csv(path)
# #     return df

# # dataset = 'https://raw.githubusercontent.com/nkwachiabel/Streamlit---ProM---Order-to-Cash-IBM/main/dataset/o2c_crypted.csv'
# parquet_dataset = 'https://github.com/nkwachiabel/Streamlit---ProM---Order-to-Cash-IBM/raw/main/dataset/df.parquet.gzip'
# full_df_edited = 'https://github.com/nkwachiabel/Streamlit---ProM---Order-to-Cash-IBM/raw/main/dataset/full_dataset_edited.parquet.gzip'
# filtered_df = 'https://github.com/nkwachiabel/Streamlit---ProM---Order-to-Cash-IBM/raw/main/dataset/filtered_dataset.parquet.gzip'

parquet_dataset = 'dataset/df.parquet.gzip'
full_df_edited = 'dataset/full_dataset_edited.parquet.gzip'
filtered_df = 'dataset/filtered_dataset.parquet.gzip'

# # df = load_data(parquet_datadet)
parquet_dataset = load_parquet(parquet_dataset)
full_df_edited = load_parquet(full_df_edited)
filtered_df = load_parquet(filtered_df)


case_id = 'Key'
activity = 'Activity'
timestamp = 'Date'
resources = 'User'
product = 'Product_hierarchy'
customer = 'Customer'
workgroup = 'Role'
first_activities = ['Line Creation']
last_activities = ['Good Issue','Schedule Line Rejected']
unique_activities = get_unique_items(parquet_dataset,activity)

# parquet_dataset = datetime_format(parquet_dataset, timestamp)
# start_time = earliest_time(df,timestamp)
# end_time = latest_time(df,timestamp)

@st.cache_data
def full_dataset():
    return parquet_dataset

@st.cache_data
def full_dataset_edited():
    return full_df_edited

@st.cache_data
def filtered_dataset():
    return filtered_df

# columns_to_convert = ['User', 'Activity', 'Role', 'Product_hierarchy','Customer', 'OrderType','Delayed', 'User_Type',
#        'Change_Status', 'ID_Change_Status', 'Block_Status', 'ID_Block_Status']

# df2 = df.copy()
# for column in columns_to_convert:
#     df2[column] = df2[column].astype('category')

# df2 = df2[['Key', 'Date', 'User', 'Activity', 'Role', 'Product_hierarchy',
#        'NetValue', 'Customer', 'OrderType', 'Delayed', 'User_Type',
#        'Change_Status', 'ID_Change_Status', 'Block_Status', 'ID_Block_Status']]

# def case_id_column():
#     return case_id

# def activity_column():
#     return activity

# def timestamp_column():
#     return timestamp

# def first_activity():
#     return first_activities

# def last_activity():
#     return last_activities

# def resources_col():
#     return resources

# def product_col():
#     return product

# def customer_col():
#     return customer

# def workgroup_col():
#     return workgroup



# columns_to_convert = ['User', 'Activity', 'Role', 'Product_hierarchy','Customer', 'OrderType','Delayed', 'User_Type',
#        'Change_Status', 'ID_Change_Status', 'Block_Status', 'ID_Block_Status']

# df2 = df.copy()
# # Convert each specified column to categorical
# for column in columns_to_convert:
#     df2[column] = df2[column].astype('category')

# df2 = df2[['Key', 'Date', 'User', 'Activity', 'Role', 'Product_hierarchy',
#        'NetValue', 'Customer', 'OrderType', 'Delayed', 'User_Type',
#        'Change_Status', 'ID_Change_Status', 'Block_Status', 'ID_Block_Status']]

# def determine_status(row):
#     if row['First_Activity'] in first_activities:
#         if row['Last_Activity'] in last_activities:
#             return 'Closed'
#         else:
#             return 'Open'
#     else:
#         if row['Last_Activity'] in last_activities:
#             return 'Closed'
#         else:
#             return 'Wrong first activity'

# # with st.expander(":point_right: Data View"):

# df2 = initial_dataset_csv(df2, case_id_column(), activity_column(), timestamp_column())
# df2['Case_Status'] = df2.apply(determine_status, axis=1)

# # df2 = df2[(df2[timestamp_column()]>=start_date) & (df2[timestamp_column()]< end_date + pd.Timedelta(days=1))].copy()
# filtered_df = df2.copy()
# filtered_df = filtered_df[filtered_df['First_Activity'].isin(first_activities) & filtered_df['Last_Activity'].isin(last_activities)]
# filtered_df = initial_dataset_filtered_df(filtered_df, case_id_column(), activity_column(), timestamp_column())

