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

st.title("Data Overview")
st.divider()

# Calculated metrics
start_time = earliest_time(full_df,timestamp_column)
end_time = latest_time(full_df,timestamp_column)

# Date row and columns
_, _, _, date1, date2 = st.columns(5)

# Date filters
with date1:
    start_date = st.date_input("Start Date", start_time)
    start_date = pd.to_datetime(start_date)

with date2:
    end_date = st.date_input("End Date", end_time)
    end_date = pd.to_datetime(end_date)

total_no_of_cases = unique_count(full_df,case_id_column)
total_no_of_closed_cases = full_df[full_df['Status'] == 'Open'][case_id_column].nunique()
incorrect_start_cases = full_df[~full_df['First_Activity'].isin(first_activities) & full_df['Last_Activity'].isin(last_activities)][case_id_column].nunique()
first_activities_table = activity_occurrence_count(full_df, activity_column, 'First_Activity')
last_activities_table = activity_occurrence_count(full_df, activity_column, 'Last_Activity')

no_of_cases = unique_count(filtered_df,case_id_column)
no_of_activities = unique_count(filtered_df,activity_column)
no_of_events = total_count(filtered_df,activity_column)
event_bar_df = event_graph_fn(filtered_df,timestamp_column,'Month/Year')
cases_bar_df = cases_graph_fn(filtered_df,timestamp_column,'Month/Year')
event_df = activity_occurrence(filtered_df, case_id_column, activity_column)
variants_sum = activities_trace(filtered_df, case_id_column, activity_column,timestamp_column)
no_of_variants = unique_count(filtered_df,'Variants')
var_table = var_table_process_analysis(filtered_df,'Variants',case_id_column)

event_per_case_df = event_per_case_analysis(filtered_df, case_id_column, timestamp_column,activity_column,event_id='Event_ID',case_length='Case_Length')
closed_first_activities_table = activity_occurrence_count(filtered_df, activity_column, 'First_Activity')
closed_last_activities_table = activity_occurrence_count(filtered_df, activity_column, 'Last_Activity')

data_overview, open_close = st.tabs(['Data Overview', 'Open/closed cases'])

with data_overview:
    with st.container(border=True):
        cases_metric, activity_metric, event_metric, variant_metric = st.columns(4)
        
        # No. of closed cases
        with cases_metric:
            no_of_cases = format(no_of_cases, ",.0f")
            st.metric(label="Number of cases", value=no_of_cases)

        # No of activities
        with activity_metric:
            no_of_activities = format(no_of_activities, ",.0f")
            st.metric(label="Number of activities", value=no_of_activities)

        # No. of events
        with event_metric:
            no_of_events = format(no_of_events, ",.0f")
            st.metric(label="Number of events", value=no_of_events)

        # No. of variants
        with variant_metric:
            no_of_variants = format(no_of_variants, ",.0f")
            st.metric(label="Number of variants", value=no_of_variants)
    
    with st.container(border=True):
        st.markdown('<span style="font-size: 16px; font-weight: bold;">Count of cases per month by start date</span>', unsafe_allow_html=True)
        vertical_bar(cases_bar_df,'Month/Year','Count','',color_graph="rgba(49, 51, 60)")
    
    with st.container(border=True):
        st.markdown('<span style="font-size: 16px; font-weight: bold;">Count of events per month</span>', unsafe_allow_html=True)
        vertical_bar(event_bar_df,'Month/Year','Count','',color_graph="rgba(49, 51, 60)")

    with st.container(border=True):
        events_per_case_column, variants_column, activity_distribution_column  = st.columns([2, 2, 2])
        
        with events_per_case_column:
            st.markdown('<span style="font-size: 16px; font-weight: bold;">Event per case</span>', unsafe_allow_html=True)
            vertical_bar(event_per_case_df,'Case_Length','Percent','',color_graph="rgba(49, 51, 60)")
        
        # Activity distribution
        with activity_distribution_column:
            st.markdown('<span style="font-size: 16px; font-weight: bold;">Activity Distribution</span>', unsafe_allow_html=True)
            st.data_editor(
                event_df,
                column_config={
                    "Percent": st.column_config.ProgressColumn(
                        "Percent",
                        help="Percentage of Occurrence",
                        format="%.2f %%",
                        min_value=event_df['Percent'].min(),
                        max_value=event_df['Percent'].max(),
                    ),
                },
                hide_index=True,
                use_container_width=True,
                height=400
            )

        with variants_column:
            st.markdown('<span style="font-size: 16px; font-weight: bold;">Variants</span>', unsafe_allow_html=True)
            st.data_editor(
            var_table,
            column_config={
                "Percent": st.column_config.ProgressColumn(
                    "Percent",
                    help="Percentage of Occurrence",
                    format="%.2f %%",
                    min_value=var_table['Percent'].min(),
                    max_value=var_table['Percent'].max(),
                ),
            },
            hide_index=True,
            use_container_width=True,
            height=400
        )


with open_close:
    with st.container(border=True):
        total_cases, cases_metric_2, open_cases_2, wrong_start_activitty = st.columns(4)
        # total no. of cases
        with total_cases:
            total_no_of_cases = format(total_no_of_cases, ",.0f")
            st.metric(label="Total number of cases", value=total_no_of_cases)

        # No. of closed cases
        with cases_metric_2:
            st.metric(label="Closed cases", value=no_of_cases)


        # No. of open cases
        with open_cases_2:
            total_no_of_closed_cases = format(total_no_of_closed_cases, ",.0f")
            st.metric(label="Open cases", value=total_no_of_closed_cases)

        # No. of incorrect start activity
        with wrong_start_activitty:
            incorrect_start_cases = format(incorrect_start_cases, ",.0f")
            st.metric(label="Incorrect start cases", value=incorrect_start_cases)

    
    with st.container(border=True):
        first_activities_2, last_activities_3 = st.columns([2,2])
        with first_activities_2:
            st.markdown('<span style="font-size: 16px; font-weight: bold;">First Activities</span>', unsafe_allow_html=True)
            st.data_editor(
            first_activities_table,
            column_config={
                "Percent": st.column_config.ProgressColumn(
                    "Percent",
                    help="Percentage of Occurrence",
                    format="%.2f %%",
                    min_value=event_df['Percent'].min(),
                    max_value=event_df['Percent'].max(),
                ),
            },
            hide_index=True,
            use_container_width=True,
            height=400
        )
            
        with last_activities_3:
            st.markdown('<span style="font-size: 16px; font-weight: bold;">Last Activities</span>', unsafe_allow_html=True)
            st.data_editor(
            last_activities_table,
            column_config={
                "Percent": st.column_config.ProgressColumn(
                    "Percent",
                    help="Percentage of Occurrence",
                    format="%.2f %%",
                    min_value=event_df['Percent'].min(),
                    max_value=event_df['Percent'].max(),
                ),
            },
            hide_index=True,
            use_container_width=True,
            height=400
        )
    
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