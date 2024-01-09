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

@st.cache_data(ttl=3600*2)
def full_dataset():
    return parquet_dataset

@st.cache_data(ttl=3600*2)
def full_dataset_edited():
    return full_df_edited

@st.cache_data(ttl=3600*2)
def filtered_dataset():
    return filtered_df