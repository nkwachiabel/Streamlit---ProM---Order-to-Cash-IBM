import streamlit as st
import pandas as pd
from prom_functions import get_unique_items, unique_count, case_duration, process_details, case_duration_df
from visuals_prom import *
from dataset_details import filtered_dataset, full_dataset, full_dataset_edited

colCase = 'Key'
colActivity = 'Activity'
colTimestamp = 'Date'
colResources = 'User'
colProduct = 'Product_hierarchy'
colCustomer = 'Customer'
workgroup = 'Role'
first_activities = ['Line Creation']
last_activities = ['Good Issue','Schedule Line Rejected']
filtered_df = filtered_dataset()
original_df = full_dataset()
full_df = full_dataset_edited()

first_activity_list = get_unique_items(filtered_df, 'First_Activity')
last_activity_list = get_unique_items(filtered_df, 'Last_Activity')

unique_product_list = get_unique_items(filtered_df,colProduct)
unique_product_list = sorted(unique_product_list, reverse=False)

unique_ordertype_list = get_unique_items(filtered_df,'OrderType')
unique_ordertype_list = sorted(unique_ordertype_list, reverse=False)

st.title("Timing Analysis")
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

with st.sidebar:
    st.markdown('<span style="font-size: 16px; font-weight: bold;">Select calculation metric</span>', unsafe_allow_html=True)
    calculation_metric = st.selectbox("Metric", ['Median', 'Average'], index=0)

# Product filter
with st.sidebar:
    product_list = st.multiselect(options=unique_product_list, label="Products", placeholder="Select product")

with st.sidebar:
    ordertype_list = st.multiselect(options=unique_ordertype_list, label="Order type", placeholder="Select order type")

with st.sidebar:
    selected_first_activities = st.multiselect(options=first_activity_list, label="First activities", placeholder="Select activity")

# Last activity filter
with st.sidebar:
    selected_last_activities = st.multiselect(options=last_activity_list, label="Last activities", placeholder="Select activity")

filtered_df = filtered_df.copy()

if product_list:
    filtered_df = filtered_df[filtered_df[colProduct].isin(product_list)]

if ordertype_list:
    filtered_df = filtered_df[filtered_df['OrderType'].isin(ordertype_list)]

if selected_first_activities:
    filtered_df = filtered_df[filtered_df['First_Activity'].isin(selected_first_activities)]

if selected_last_activities:
    filtered_df = filtered_df[filtered_df['Last_Activity'].isin(selected_last_activities)]

# calculations
no_of_cases = unique_count(filtered_df,colCase) # no of cases
no_of_activities = unique_count(filtered_df,colActivity) # no of activities
case_dur = case_duration(filtered_df, colCase, colTimestamp).drop('Max', axis=1) # case duration
min_dur = case_dur['Case_Duration_days'].min() # minimum case duration
med_dur = case_dur['Case_Duration_days'].median() # median case duration
avg_dur = round(case_dur['Case_Duration_days'].mean(),0) # average case duration
max_dur = case_dur['Case_Duration_days'].max() # maximum case duration

distinct_log = filtered_df[filtered_df['Event_ID'] == 1].reset_index(drop=True)
distinct_log = pd.merge(distinct_log, case_dur, right_on=colCase, left_on=colCase)

if calculation_metric == 'Median':
    product_hierarchy_timing = distinct_log.groupby([colProduct], observed=True)['Case_Duration_days'].median().reset_index()
else:
    product_hierarchy_timing = distinct_log.groupby([colProduct], observed=True)['Case_Duration_days'].mean().reset_index()
product_hierarchy_timing = product_hierarchy_timing.sort_values(by=['Case_Duration_days'], ascending=False)

if calculation_metric == 'Median':
    order_type_timing = distinct_log.groupby(['OrderType'], observed=True)['Case_Duration_days'].median().reset_index()
else:
    order_type_timing = distinct_log.groupby(['OrderType'], observed=True)['Case_Duration_days'].mean().reset_index()
order_type_timing = order_type_timing.sort_values(by=['Case_Duration_days'], ascending=False)

if calculation_metric == 'Median':
    sla_rate1 = case_dur[case_dur['Case_Duration_days'] > med_dur][colCase].count()
    sla_rate = (sla_rate1/no_of_cases)*100
else:
    sla_rate = case_dur[case_dur['Case_Duration_days'] > avg_dur][colCase].count()
    sla_rate = (sla_rate/no_of_cases)*100

if calculation_metric == 'Median':
    change_status_timing = distinct_log.groupby(['ID_Change_Status'], observed=True)['Case_Duration_days'].median().reset_index()
else:
    change_status_timing = distinct_log.groupby(['ID_Change_Status'], observed=True)['Case_Duration_days'].mean().reset_index()
change_status_timing = change_status_timing.sort_values(by=['Case_Duration_days'], ascending=False)

if calculation_metric == 'Median':
    block_status_timing = distinct_log.groupby(['ID_Block_Status'], observed=True)['Case_Duration_days'].median().reset_index()
else:
    block_status_timing = distinct_log.groupby(['ID_Block_Status'], observed=True)['Case_Duration_days'].mean().reset_index()
block_status_timing = block_status_timing.sort_values(by=['Case_Duration_days'], ascending=False)

case_dur_df = case_dur.groupby(['Case_Duration_days'])[colCase].count().reset_index() # case duration graph
process_details_df = process_details(filtered_df, colCase, colTimestamp, colActivity) # transtion matrix
process_details_df['Duration'] = (process_details_df[colTimestamp+'_2'] - process_details_df[colTimestamp]).dt.days
if calculation_metric == 'Median':
    transition_matrix_df = process_details_df.pivot_table(index=colActivity, columns=colActivity+'_2', values='Duration', aggfunc='median', observed=True).fillna(0)
else:
    transition_matrix_df = process_details_df.pivot_table(index=colActivity, columns=colActivity+'_2', values='Duration', aggfunc='mean', observed=True).fillna(0)
case_duration_dataframe = case_duration_df(filtered_df, colCase, colTimestamp, event_id = 'Event_ID') # start date, end date and duration
if calculation_metric == 'Median':
    activity_duration = filtered_df.groupby([colActivity], observed=True)['Activity_Duration'].median().round(0).reset_index()
else:
    activity_duration = filtered_df.groupby([colActivity], observed=True)['Activity_Duration'].mean().round(0).reset_index()
activity_duration = activity_duration.sort_values(by=['Activity_Duration'], ascending=False)

if calculation_metric == 'Median':
    connection_duration = process_details_df.groupby(by='Connection', observed=True)['Duration'].median().round(0).reset_index()
else:
    connection_duration = process_details_df.groupby(by='Connection', observed=True)['Duration'].mean().round(0).reset_index()
connection_duration = connection_duration.sort_values(by=['Duration'], ascending=False)

with st.container(border=True):
    # layout
    cases_metric, activity_metric, min_dur_metric, med_dur_metric, max_dur_metric, sla_metric = st.columns(6) #event_metric, variant_metric,
    # No. of closed cases
    with cases_metric:
        no_of_cases = format(no_of_cases, ",.0f")
        st.metric(label="Number of cases", value=no_of_cases)

    # No of activities
    with activity_metric:
        no_of_activities = format(no_of_activities, ",.0f")
        st.metric(label="Number of activities", value=no_of_activities)

    # Minimum duration
    with min_dur_metric:
        min_dur = format(min_dur, ",.0f")
        st.metric(label="Min. duration (days)", value=min_dur, help='The minimum case duration from the cases in the event log')

    # Median duration
    with med_dur_metric:
        if calculation_metric == 'Median':
            med_dur = format(med_dur, ",.0f")
            st.metric(label="Med. duration (days)", value=med_dur, help='The median time it takes to complete a case')
        else:
            avg_dur = format(avg_dur, ",.0f")
            st.metric(label="AVg. duration (days)", value=avg_dur, help='The average time it takes to complete a case')

    # Maximum duration
    with max_dur_metric:
        max_dur = format(max_dur, ",.0f")
        st.metric(label="Max. duration (days)", value=max_dur, help='The maximum case duration from the cases in the event log')

    # Maximum duration
    with sla_metric:
        sla_rate = "{:.2f}%".format(sla_rate)
        st.metric(label="SLA breach rate", value=sla_rate, help='The percent of cases which breach the SLA')

# case duration graph
with st.container(border=True):
    st.subheader("Case Duration")
    if calculation_metric == 'Median':
        med_dur = float(med_dur.replace(",", ""))
        vertical_bar_case_duration(case_dur_df,'Case_Duration_days',colCase,'',med_dur,color_graph="rgba(49, 51, 60)", vline_text="Median duration")
    else:
        avg_dur = float(avg_dur.replace(",", ""))
        vertical_bar_case_duration(case_dur_df,'Case_Duration_days',colCase,'',avg_dur,color_graph="rgba(49, 51, 60)", vline_text="Average duration")

# transition matrix
with st.container(border=True):
    if calculation_metric == 'Median':
        st.subheader("Median duration between activities", help='This shows the transitions between various activities in the process. The rows are the starting point (source), the columns are the end point (target) and the numbers are the duration in days spent between particular activities')    
    else:
        st.subheader("Average duration between activities", help='This shows the transitions between various activities in the process. The rows are the starting point (source), the columns are the end point (target) and the numbers are the duration in days spent between particular activities')

    st.write()
    st.write(transition_matrix_df.style.format("{:.0f}").background_gradient(cmap='Greens'))
    
with st.container(border=True):
    case_duration_column, activities_duration_column = st.columns(2)
    # case duration column
    with case_duration_column:
        st.subheader('Duration of each connection')
        st.dataframe(connection_duration, hide_index=True, use_container_width=True)

    with activities_duration_column:
        if calculation_metric == 'Median':
            st.subheader('Median duration of activities')
        else:
            st.subheader('Average duration of activities')
        st.dataframe(activity_duration, hide_index=True, use_container_width=True)

with st.container(border=True):
    order_type_col, product_hierar_col = st.columns(2)
    with order_type_col:
        st.subheader('Duration per order type')
        st.dataframe(order_type_timing, hide_index=True, use_container_width=True)

    with product_hierar_col:
        st.subheader('Duration per product hierarchy')
        st.dataframe(product_hierarchy_timing, hide_index=True, use_container_width=True)

with st.container(border=True):
    change_status_col, block_status_col = st.columns(2)
    with change_status_col:
        st.subheader('Changes')
        st.dataframe(change_status_timing, hide_index=True, use_container_width=True)

    with block_status_col:
        st.subheader('Blocked')
        st.dataframe(block_status_timing, hide_index=True, use_container_width=True)

with st.container(border=True):
    st.subheader('Findings')
    st.write('This detailed analysis is aimed at identifying time-related bottlenecks in the order-to-cash process, focused on completed orders, utilizing the median duration as a more robust measure against outliers than the average.  ')
    duration_findings = '''
        The aggregate median duration for completing an order across 21,159 cases is 48 days. This timeframe is dissected into two segments: rejected cases, with a swift median duration of 3 days, suggesting rapid decision-making in rejection scenarios; and non-rejected cases, with a median duration of 55 days, indicating a longer commitment to fulfilling orders.
    '''
    product_hierarchy_findings = '''
        **TLC Optical Ground Cables:** The notably lengthy median duration of 166 days could imply a complex production or delivery process, possibly due to the product's specifications or supply chain challenges.  
        **TLC Connectivity:** At 81 days median duration, and with all orders completed on time, this category might benefit from a streamlined process or less complex order requirements.  
        **TLC Optical Cables and Fibres:** Median durations of 60 and 44 days, respectively, suggest varying degrees of process efficiency, possibly influenced by factors like product demand, production complexity, or logistical considerations.

    '''
    order_type_findings = '''
        The extended duration for US-Consignm.Fill-Up (147 days) and US-Std. I/C Order (117.5 days) might be indicative of specific challenges or inefficiencies inherent to these order types, warranting a deeper investigation into their respective processes.

    '''
    changes_findings = '''
        The stark contrast in median durations between orders with (70 days) and without (45 days) delivery date changes underscores the significant impact of such modifications. This aspect suggests a need for rigorous schedule adherence and predictive planning to mitigate delays.

    '''
    blocks_findings = '''
        The zero-day median duration for orders without blocks contrasts sharply with the 26-day median for blocked orders. This disparity calls for a proactive approach in block management, particularly in addressing frequent causes like address inaccuracies or credit issues, which can severely impede the order timeline.

    '''
    activity_findings = '''
        The Delivery activity and Address Missing Block are identified as major time-consuming steps. Streamlining the delivery process and ensuring accurate customer data upfront can substantially reduce these delays.
        The transitions with the longest durations reveal critical junctures where process improvement can significantly impact overall efficiency, especially in logistics and credit management areas. Addressing these areas could dramatically enhance the overall speed and efficiency of the order-to-cash process.

    '''
    findings_col1, findings_col2 = st.columns(2)

    with findings_col1:
        st.markdown('<span style="font-size: 20px; font-weight: bold;">Overall Process Duration</span>', unsafe_allow_html=True)
        st.markdown(duration_findings, unsafe_allow_html=True)
        st.markdown('<span style="font-size: 20px; font-weight: bold;">Product Hierarchy Insights</span>', unsafe_allow_html=True)
        st.markdown(product_hierarchy_findings, unsafe_allow_html=True)
        st.markdown('<span style="font-size: 20px; font-weight: bold;">Order Type Variations</span>', unsafe_allow_html=True)
        st.markdown(order_type_findings, unsafe_allow_html=True)

    with findings_col2:
        st.markdown('<span style="font-size: 20px; font-weight: bold;">Delivery Date Changes</span>', unsafe_allow_html=True)
        st.markdown(changes_findings, unsafe_allow_html=True)
        st.markdown('<span style="font-size: 20px; font-weight: bold;">Blocks and Their Impacts</span>', unsafe_allow_html=True)
        st.markdown(blocks_findings, unsafe_allow_html=True)
        st.markdown('<span style="font-size: 20px; font-weight: bold;">Activity-Specific Delays</span>', unsafe_allow_html=True)
        st.markdown(activity_findings, unsafe_allow_html=True)
