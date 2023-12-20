import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from prom_functions import *
from visuals_prom import *
from dataset_details import *

colCase = case_id_column()
colActivity = activity_column()
colTimestamp = timestamp_column()
colResources = resources_col()
colProduct = product_col()
first_activities = first_activity()
last_activities = last_activity()
colCustomer = customer_col()
filtered_df = filtered_dataset()
original_df = full_dataset()
full_df = full_dataset_edited()

st.title("Timing Analysis")
st.divider()

with st.sidebar:
    st.markdown('<span style="font-size: 16px; font-weight: bold;">Select calculation metric</span>', unsafe_allow_html=True)
    calculation_metric = st.selectbox("Metric", ['Median', 'Average'], index=0)

# calculations
no_of_cases = unique_count(filtered_df,colCase) # no of cases
no_of_activities = unique_count(filtered_df,colActivity) # no of activities
case_dur = case_duration(filtered_df, colCase, colTimestamp).drop('Max', axis=1) # case duration
min_dur = case_dur['Case_Duration_days'].min() # minimum case duration
med_dur = case_dur['Case_Duration_days'].median() # median case duration
avg_dur = round(case_dur['Case_Duration_days'].mean(),0) # average case duration
max_dur = case_dur['Case_Duration_days'].max() # maximum case duration

if calculation_metric == 'Median':
    sla_rate1 = case_dur[case_dur['Case_Duration_days'] > med_dur][colCase].count()
    sla_rate = (sla_rate1/no_of_cases)*100
else:
    sla_rate = case_dur[case_dur['Case_Duration_days'] > avg_dur][colCase].count()
    sla_rate = (sla_rate/no_of_cases)*100

case_dur_df = case_dur.groupby(['Case_Duration_days'])[colCase].count().reset_index() # case duration graph
process_details_df = process_details(filtered_df, colCase, colTimestamp, colActivity) # transtion matrix
process_details_df['Duration'] = (process_details_df[colTimestamp+'_2'] - process_details_df[colTimestamp]).dt.days
if calculation_metric == 'Median':
    transition_matrix_df = process_details_df.pivot_table(index=colActivity, columns=colActivity+'_2', values='Duration', aggfunc='median').fillna(0)
else:
    transition_matrix_df = process_details_df.pivot_table(index=colActivity, columns=colActivity+'_2', values='Duration', aggfunc='mean').fillna(0)
case_duration_dataframe = case_duration_df(filtered_df, colCase, colTimestamp, event_id = 'Event_ID') # start date, end date and duration
if calculation_metric == 'Median':
    activity_duration = filtered_df.groupby([colActivity])['Activity_Duration'].median().round(0).reset_index()
else:
    activity_duration = filtered_df.groupby([colActivity])['Activity_Duration'].mean().round(0).reset_index()
activity_duration = activity_duration.sort_values(by=['Activity_Duration'], ascending=False)

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
        st.subheader('Duration of each case')
        st.dataframe(case_duration_dataframe, hide_index=True, use_container_width=True)

    with activities_duration_column:
        if calculation_metric == 'Median':
            st.subheader('Median duration of activities')
        else:
            st.subheader('Average duration of activities')
        st.dataframe(activity_duration, hide_index=True, use_container_width=True)


# st.write(case_dur[case_dur['Case_Duration_days']>med_dur][colCase].count())


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
'''
st.markdown(f'<style>{css}</style>',unsafe_allow_html=True)