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

st.title("Open Orders")
st.divider()


open_cases = full_df[full_df['Case_Status'] == 'Open'].reset_index()

unique_product_list = get_unique_items(open_cases,colProduct)
unique_product_list = sorted(unique_product_list, reverse=False)

unique_ordertype_list = get_unique_items(open_cases,'OrderType')
unique_ordertype_list = sorted(unique_ordertype_list, reverse=False)

unique_last_act_list = get_unique_items(open_cases,'Last_Activity')
unique_last_act_list = sorted(unique_last_act_list, reverse=False)

# Product filter
with st.sidebar:
    product_list = st.multiselect(options=unique_product_list, label="Products", placeholder="Select product")

with st.sidebar:
    ordertype_list = st.multiselect(options=unique_ordertype_list, label="Order type", placeholder="Select order type")

with st.sidebar:
    last_act_list = st.multiselect(options=unique_last_act_list, label="Order type", placeholder="Select last activity")

open_cases = open_cases.copy()

if product_list:
    open_cases = open_cases[open_cases[colProduct].isin(product_list)]

if ordertype_list:
    open_cases = open_cases[open_cases['OrderType'].isin(ordertype_list)]

if last_act_list:
    open_cases = open_cases[open_cases['Last_Activity'].isin(last_act_list)]

distinct_log = open_cases[open_cases['Event_ID'] == 1].reset_index(drop=True)
last_act_table = activity_occurrence(open_cases, colCase, 'Last_Activity')

order_type_count = open_cases.groupby(['OrderType'])['NetValue'].sum().reset_index()
product_hierarchy_count = open_cases.groupby([colProduct])['NetValue'].sum().reset_index()

# with variants_column:
st.markdown('<span style="font-size: 16px; font-weight: bold;">Number of tickets by products</span>', unsafe_allow_html=True)
fig = px.pie(last_act_table, values = "Percent", names = 'Last_Activity', template = "gridon")
fig.update_traces(text = last_act_table["Number of Cases"], textposition = "inside")
st.plotly_chart(fig,use_container_width=True)

st.dataframe(open_cases)