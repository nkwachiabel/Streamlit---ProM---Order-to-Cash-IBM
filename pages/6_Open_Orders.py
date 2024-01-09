import streamlit as st
# import pandas as pd
import plotly.express as px
from prom_functions import get_unique_items,unique_count,activity_occurrence,cases_graph_fn
from visuals_prom import vertical_bar
from dataset_details import filtered_dataset,full_dataset,full_dataset_edited


colCase = 'Key'
colActivity = 'Activity'
colTimestamp = 'Date'
colResources = 'User'
colProduct = 'Product_hierarchy'
colCustomer = 'Customer'
colWorkgroup = 'Role'
first_activities = ['Line Creation']
last_activities = ['Good Issue','Schedule Line Rejected']
filtered_df = filtered_dataset()
original_df = full_dataset()
full_df = full_dataset_edited()

st.title("Open Orders")
st.divider()

metric_css='''
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
st.markdown(f'<style>{metric_css}</style>',unsafe_allow_html=True)

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
order_type_count = open_cases.groupby([colProduct,'OrderType'], observed=True).agg({colCase: ['nunique'], 'NetValue': ['sum']})
order_type_count = order_type_count.sort_values(by=('NetValue', 'sum'), ascending=False).reset_index()

with st.container(border=True):
    cases_metric, customer_metric, net_value_metric = st.columns(3)

    with cases_metric:
        no_of_cases = format(no_of_cases, ",.0f")
        st.metric(label="Number of cases", value=no_of_cases)

    with customer_metric:
        no_of_customers = format(no_of_customers, ",.0f")
        st.metric(label="Number of customers", value=no_of_customers)

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

with st.container(border=True):
    st.subheader('Findings')
    st.write('This section details the current status of incomplete cases, which began with the Line Creation activity but have not concluded with Goods Issue nor been marked as rejected. The event log indicates there are 8,908 open orders, amounting to a total value of USD126.61 million. These can be classified into two main categories: Services and Products.')
    services_findings = '''
        The Services category encompasses orders related to service delivery, involving two product lines: TLC Services and TLC Other.  

        **TLC Services:**  
        Comprises 180 orders from 7 customers.  
        Most of these orders (172 out of 180) have a net value of zero.  

        **TLC Other:**  
        Contains 11 orders from a single customer, valued at USD55,290.99.  
        The earliest order is dated November 2, 2016.  

        Notably, the only recorded activity for these service orders is Line Creation, and they have remained open for an extended period. With a combined net value of $0.11 million, the validity and status of these orders should be reassessed. It's critical to determine whether these orders are still active and whether they warrant remaining open. A regular review process should be established to update the scope and confirm the completion or closure of these services.  

    '''
    product_findings = '''
        The Products category aligns with the products identified in the process analysis, including Optical Cables, Optical Fibres, Connectivity, and Optical Ground Cables.

        **General Overview:**  
        Consists of 8,717 orders from 192 customers, totaling a value of $126.50 million.  

        **Specific Observations:**  
        **Line Creation as Last Activity:** There are 3,149 cases where the last recorded activity is Line Creation, with Optical Fibres making up 2,887 of these orders. Some cases date back to January 2, 2016, and require investigation to determine if they should be closed, especially if they are effectively rejected orders.  

        **LgstCheckOnConfDat Removed:** This is the final activity for 2,073 cases, predominantly involving Optical Cables and Optical Fibres, with 1,053 and 1,013 orders respectively. These cases should undergo a similar review process to the Line Creation group for potential closure.  

        **Delivery as Last Activity:** There are 1,929 cases with Delivery as the last step, with Optical Cables accounting for 1,486 orders. It is necessary to verify if these orders have indeed been issued and, if so, to proceed with closure.  

    '''
    findings_col1, findings_col2 = st.columns(2)
    with findings_col1:
        st.markdown('<span style="font-size: 20px; font-weight: bold;">Services Category</span>', unsafe_allow_html=True)
        st.markdown(services_findings, unsafe_allow_html=True)

    with findings_col2:
        st.markdown('<span style="font-size: 20px; font-weight: bold;">Products Category</span>', unsafe_allow_html=True)
        st.markdown(product_findings, unsafe_allow_html=True)
