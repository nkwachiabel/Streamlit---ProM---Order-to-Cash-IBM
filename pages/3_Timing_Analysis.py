import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from prom_functions import *
from visuals_prom import *

st.set_page_config(page_title="Process Mining O2C", page_icon=":bar_chart:", layout="wide")

if 'filtered_df' not in st.session_state or 'case_id' not in st.session_state or 'activity' not in st.session_state or 'timestamp' not in st.session_state or 'first_activities' not in st.session_state or 'last_activities' not in st.session_state:
    st.warning("Please upload a dataset and select the required column from the homepage")
    st.stop()
else:
    filtered_df = st.session_state['filtered_df']
    full_df = st.session_state['full_df']
    case_id_column = st.session_state['case_id']
    activity_column = st.session_state['activity']
    timestamp_column = st.session_state['timestamp']
    first_activities = st.session_state['first_activities']
    last_activities = st.session_state['last_activities']
    original_dataset = st.session_state['original_dataset']
# filtered_df = get_dataframe()

st.title("Timing Analysis")
st.divider()



with st.sidebar:
    st.markdown('<span style="font-size: 16px; font-weight: bold;">Select calculation metric</span>', unsafe_allow_html=True)
    calculation_metric = st.selectbox("Metric", ['Median', 'Average'], index=0)

# calculations
no_of_cases = unique_count(filtered_df,case_id_column) # no of cases
no_of_activities = unique_count(filtered_df,activity_column) # no of activities
case_dur = case_duration(filtered_df, case_id_column, timestamp_column).drop('Max', axis=1) # case duration
min_dur = case_dur['Case_Duration_days'].min() # minimum case duration
med_dur = case_dur['Case_Duration_days'].median() # median case duration
avg_dur = round(case_dur['Case_Duration_days'].mean(),0) # average case duration
max_dur = case_dur['Case_Duration_days'].max() # maximum case duration
case_dur_df = case_dur.groupby(['Case_Duration_days'])[case_id_column].count().reset_index() # case duration graph
process_details_df = process_details(filtered_df, case_id_column, timestamp_column, activity_column) # transtion matrix
process_details_df['Duration'] = (process_details_df[timestamp_column+'_2'] - process_details_df[timestamp_column]).dt.days
if calculation_metric == 'Median':
    transition_matrix_df = process_details_df.pivot_table(index=activity_column, columns=activity_column+'_2', values='Duration', aggfunc='median').fillna(0)
else:
    transition_matrix_df = process_details_df.pivot_table(index=activity_column, columns=activity_column+'_2', values='Duration', aggfunc='mean').fillna(0)
case_duration_dataframe = case_duration_df(filtered_df, case_id_column, timestamp_column, event_id = 'Event_ID') # start date, end date and duration
if calculation_metric == 'Median':
    activity_duration = filtered_df.groupby([activity_column])['Activity_Duration'].median().round(0).reset_index()
else:
    activity_duration = filtered_df.groupby([activity_column])['Activity_Duration'].mean().round(0).reset_index()
activity_duration = activity_duration.sort_values(by=['Activity_Duration'], ascending=False)

with st.container(border=True):
    # layout
    cases_metric, activity_metric, min_dur_metric, med_dur_metric, max_dur_metric = st.columns(5) #event_metric, variant_metric,
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
        st.metric(label="Min. duration (days)", value=min_dur)

    # Median duration
    with med_dur_metric:
        if calculation_metric == 'Median':
            med_dur = format(med_dur, ",.0f")
            st.metric(label="Med. duration (days)", value=med_dur)
        else:
            avg_dur = format(avg_dur, ",.0f")
            st.metric(label="AVg. duration (days)", value=avg_dur)

    # Maximum duration
    with max_dur_metric:
        max_dur = format(max_dur, ",.0f")
        st.metric(label="Max. duration (days)", value=max_dur)

# case duration graph
with st.container(border=True):
    st.subheader("Case Duration")
    if calculation_metric == 'Median':
        med_dur = float(med_dur.replace(",", ""))
        vertical_bar_case_duration(case_dur_df,'Case_Duration_days',case_id_column,'',med_dur,color_graph="rgba(49, 51, 60)", vline_text="Median duration")
    else:
        avg_dur = float(avg_dur.replace(",", ""))
        vertical_bar_case_duration(case_dur_df,'Case_Duration_days',case_id_column,'',avg_dur,color_graph="rgba(49, 51, 60)", vline_text="Average duration")

# transition matrix
with st.container(border=True):
    if calculation_metric == 'Median':
        st.subheader("Median duration between activities")    
    else:
        st.subheader("Average duration between activities")

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