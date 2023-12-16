import streamlit as st
import pandas as pd
from prom_functions import *
from visuals_prom import *

st.set_page_config(page_title="Process Mining O2C", page_icon=":bar_chart:", layout="wide")

st.title("Process Mining with Streamlit")

st.header("Upload dataset")
uploaded_file = st.file_uploader("Choose a file")

if uploaded_file is None:
    st.info("Upload a dataset", icon="ℹ️")
    st.stop()

@st.cache_data
def load_data(path: str):
    df = pd.read_csv(path)
    return df

df = load_data(uploaded_file)

with st.expander("Data Preview", expanded=True):
    st.dataframe(df)

st.write('')
defaulf_option = "Select an option"
defaulf_options = "Select activities"
column_names = df.columns.to_list()

st.subheader("Select the case identifier, activity and timestamp columns from your eventlog")

case_col, activity_col, timestamp_col = st.columns(3)

with case_col:
    case_id = st.selectbox(options=[defaulf_option]+column_names, label="Case ID", index=0)

with activity_col:
    activity = st.selectbox(options=[defaulf_option]+column_names, label="Activity", index=0)

with timestamp_col:
    timestamp = st.selectbox(options=[defaulf_option]+column_names, label="Timestamp", index=0)

if case_id == defaulf_option or activity == defaulf_option or timestamp == defaulf_option:
    st.stop()

def case_id_column():
    return case_id

def activity_column():
    return activity

def timestamp_column():
    return timestamp

unique_activities = get_unique_items(df,activity_column())

st.subheader("Select the first and last activities")
first_act_col, last_act_col = st.columns(2)

with first_act_col:
    first_activities = st.multiselect(options=unique_activities, label="First activities", placeholder="Select the first activities in the process") #"Select the first activities in the process"

with last_act_col:
    last_activities = st.multiselect(options=unique_activities, label="Last activities", placeholder="Select the last activities in the process") #"Select the last activities in the process"

if st.button('Analyse dataset'):
    if not first_activities or not last_activities:
        st.warning('Please select both first and last activities')
        st.stop()
    else:
        df = datetime_format(df, timestamp_column())
        start_time = earliest_time(df,timestamp_column())
        end_time = latest_time(df,timestamp_column())

        # Date row and columns
        _, _, _, date1, date2 = st.columns(5)

        # Date filters
        with date1:
            start_date = st.date_input("Start Date", start_time)
            start_date = pd.to_datetime(start_date)

        with date2:
            end_date = st.date_input("End Date", end_time)
            end_date = pd.to_datetime(end_date)

        def determine_status(row):
            if row['First_Activity'] in first_activities:
                if row['Last_Activity'] in last_activities:
                    return 'Closed'
                else:
                    return 'Open'
            else:
                if row['Last_Activity'] in last_activities:
                    return 'Closed'
                else:
                    return 'Wrong first activity'


        with st.expander("Data View"):
            df2 = df.copy()
            df2 = initial_dataset_csv(df2, case_id_column(), activity_column(), timestamp_column())
            df2['Status'] = df2.apply(determine_status, axis=1)
            st.dataframe(df2)

        df2 = df2[(df2[timestamp_column()]>=start_date) & (df2[timestamp_column()]< end_date + pd.Timedelta(days=1))].copy()
        
        filtered_df = df2.copy()
        filtered_df = filtered_df[filtered_df['First_Activity'].isin(first_activities) & filtered_df['Last_Activity'].isin(last_activities)]
        filtered_df = initial_dataset_filtered_df(filtered_df, case_id_column(), activity_column(), timestamp_column())


        st.session_state['full_df'] = df2
        st.session_state['filtered_df'] = filtered_df
        st.session_state['case_id'] = case_id_column()
        st.session_state['activity'] = activity_column()
        st.session_state['timestamp'] = timestamp_column()
        st.session_state['first_activities'] = first_activities
        st.session_state['last_activities'] = last_activities
        st.session_state['original_dataset'] = df
