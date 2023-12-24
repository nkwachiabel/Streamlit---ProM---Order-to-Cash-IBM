import streamlit as st
import pandas as pd
from prom_functions import *
from visuals_prom import *
from dataset_details import *

colCase = case_id_column()
colActivity = activity_column()
colTimestamp = timestamp_column()
colResources = resources_col()
colProduct = product_col()
colCustomer = customer_col()
filtered_df = filtered_dataset()
original_df = full_dataset()
full_df = full_dataset_edited()

# distinct_log = filtered_df.copy()
distinct_log = filtered_df[filtered_df['Event_ID'] == 1].reset_index(drop=True)
order_type = distinct_log.groupby(by=['Product_hierarchy','OrderType'])['NetValue'].sum().sort_values(ascending=False)


st.dataframe(order_type)