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


open_cases = full_df[full_df['Case_Status'] == 'Open'].reset_index(drop=True)

unique_product_list = get_unique_items(open_cases,colProduct)
unique_product_list = sorted(unique_product_list, reverse=False)

unique_ordertype_list = get_unique_items(open_cases,'OrderType')
unique_ordertype_list = sorted(unique_ordertype_list, reverse=False)

unique_last_act_list = get_unique_items(open_cases,'Last_Activity')
unique_last_act_list = sorted(unique_last_act_list, reverse=False)

unique_case_list = get_unique_items(open_cases,colCase)
unique_case_list = sorted(unique_case_list, reverse=False)

with st.sidebar:
    st.markdown('<span style="font-size: 16px; font-weight: bold;">Filters</span>', unsafe_allow_html=True)

# Product filter
with st.sidebar:
    product_list = st.multiselect(options=unique_product_list, label="Products", placeholder="Select product")

with st.sidebar:
    ordertype_list = st.multiselect(options=unique_ordertype_list, label="Order type", placeholder="Select order type")

with st.sidebar:
    last_act_list = st.multiselect(options=unique_last_act_list, label="Last activities", placeholder="Select last activity")

with st.sidebar:
    case_list = st.multiselect(options=unique_case_list, label="Order ID", placeholder="Select order id")

open_cases = open_cases.copy()

if product_list:
    open_cases = open_cases[open_cases[colProduct].isin(product_list)]

if ordertype_list:
    open_cases = open_cases[open_cases['OrderType'].isin(ordertype_list)]

if last_act_list:
    open_cases = open_cases[open_cases['Last_Activity'].isin(last_act_list)]

if case_list:
    open_cases = open_cases[open_cases[colCase].isin(case_list)]

no_of_cases = unique_count(open_cases,colCase)
no_of_customers = unique_count(open_cases,colCustomer)
distinct_log = open_cases[open_cases['Event_ID'] == 1].reset_index(drop=True)
total_net_value = distinct_log['NetValue'].sum()
last_act_table = activity_occurrence(open_cases, colCase, 'Last_Activity')
cases_bar_df = cases_graph_fn(open_cases,colTimestamp,'Month/Year')
order_type_count = open_cases.groupby([colProduct,'OrderType']).agg({colCase: ['nunique'], 'NetValue': ['sum']})
order_type_count = order_type_count.sort_values(by=('NetValue', 'sum'), ascending=False).reset_index()

with st.container(border=True):
    cases_metric, customer_metric, net_value_metric = st.columns(3)

    with cases_metric:
        no_of_cases = format(no_of_cases, ",.0f")
        st.metric(label="Number of cases", value=no_of_cases)

    with customer_metric:
        no_of_customers = format(no_of_customers, ",.0f")
        st.metric(label="Number of cases", value=no_of_customers)

    with net_value_metric:
        total_net_value = round(total_net_value/1000000,2)
        total_net_value = format(total_net_value, ",.2f")
        st.metric(label="Net Value of orders", value=f"${total_net_value}M")

with st.container(border=True):
    st.markdown('<span style="font-size: 16px; font-weight: bold;">Count of open cases per month by start date</span>', unsafe_allow_html=True)
    vertical_bar(cases_bar_df,'Month/Year','Count','',color_graph="rgba(49, 51, 60)")

with st.container(border=True):
    pie_column, table_column = st.columns(2)

    with pie_column:
        st.markdown('<span style="font-size: 16px; font-weight: bold;">Number of orders by Last activity</span>', unsafe_allow_html=True)
        fig = px.pie(last_act_table, values = "Percent", names = 'Last_Activity', template = "gridon")
        fig.update_traces(text = last_act_table["Number of Cases"], textposition = "inside")
        st.plotly_chart(fig,use_container_width=True)

    with table_column:
        st.markdown('<span style="font-size: 16px; font-weight: bold;">Number and Net value of orders by product hierarchy and order type</span>', unsafe_allow_html=True)
        st.data_editor(order_type_count, hide_index=True, use_container_width=True)

with st.container(border=True):
    st.markdown('<span style="font-size: 16px; font-weight: bold;">Order details</span>', unsafe_allow_html=True)
    selected_cases = distinct_log[[colCase, colProduct,colTimestamp,colCustomer,'Last_Activity']]
    st.data_editor(selected_cases, hide_index=True, use_container_width=True)

with st.expander(':point_right: View Selected Cases'):
    case_ids_filtered = open_cases[colCase].unique()
    filtered_df_view = original_df[original_df[colCase].isin(case_ids_filtered)]
    st.dataframe(filtered_df_view, hide_index=True)

css='''
[data-testid="stMetricValue"], [data-testid="stMetricLabel"] {
    width: fit-content;
    margin: auto;
}

[data-testid="stMetricValue"] > div, [data-testid="stMetricLabel"] > div {
    width: fit-content;
    margin: auto;
}

[data-testid="stMetricValue"] label, [data-testid="stMetricLabel"] label {
    width: fit-content;
    margin: auto;
}
[data-testid="stMetricValue"] > div {
    font-size: 1.5rem;
}
[data-testid="stCheckbox"] > p {
    font-size: 13px;
}
'''
st.markdown(f'<style>{css}</style>',unsafe_allow_html=True)