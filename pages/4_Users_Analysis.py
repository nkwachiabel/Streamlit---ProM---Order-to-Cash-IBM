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
colWorkgroup = workgroup_col()
first_activities = first_activity()
last_activities = last_activity()
colCustomer = customer_col()
filtered_df = filtered_dataset()
original_df = full_dataset()
full_df = full_dataset_edited()

st.title("Users Analysis")
st.divider()

no_of_cases = unique_count(filtered_df,colCase)
no_of_activities = unique_count(filtered_df,colActivity)
no_of_events = total_count(filtered_df,colActivity)
no_of_users = unique_count(filtered_df, colResources)
users_activities = activities_per_user(filtered_df,colResources,colActivity)
workgroup_activities = activities_per_user(filtered_df,colWorkgroup,colActivity)
user_process_df = process_details(filtered_df, colCase, colTimestamp, colResources)
workgroup_process_df = process_details(filtered_df, colCase, colTimestamp, colWorkgroup)
hand_over_workgroups = activities_per_user(workgroup_process_df,colWorkgroup,colWorkgroup+'_2')

event_df = filtered_df.groupby(by=[colResources, colActivity])['Activity_Duration'].median().reset_index(name='Duration')
event_df.sort_values(by='Duration', ascending=False, inplace=True)

with st.container(border=True):
    # layout
    cases_metric, activity_metric, event_metric, users_metric = st.columns(4) #event_metric, variant_metric,
    # No. of closed cases
    with cases_metric:
        no_of_cases = format(no_of_cases, ",.0f")
        st.metric(label="Number of cases", value=no_of_cases)

    # No of activities
    with activity_metric:
        no_of_activities = format(no_of_activities, ",.0f")
        st.metric(label="Number of activities", value=no_of_activities)

    # Minimum duration
    with event_metric:
        no_of_events = format(no_of_events, ",.0f")
        st.metric(label="Number of events", value=no_of_events)

    # Maximum duration
    with users_metric:
        no_of_users = format(no_of_users, ",.0f")
        st.metric(label="Number of users", value=no_of_users)

with st.container(border=True):
    st.subheader('Activities by users')
    fig1 = px.bar(users_activities.sort_values(by=[colResources], ascending=True), x=colResources, y='Weight', color=colActivity)
    st.plotly_chart(fig1, use_container_width=True)

with st.container(border=True):
    user_trans_matrix_col, med_dur_user_col = st.columns([4,2])
    with user_trans_matrix_col:
        transition_matrix_df = user_process_df.pivot_table(index=colResources, columns=colResources+'_2', values=colCase, aggfunc='count').fillna(0)
        st.subheader("Transition matrix between users", help='This shows the transitions between various users in the process. The rows are the starting user (source), the columns are the end user (target) and the numbers are the number of times a particular transition occurs')
        st.write(transition_matrix_df.style.format("{:.0f}").background_gradient(cmap='Greens'))

    with med_dur_user_col:
        st.subheader('Median duration of activities per user')
        st.data_editor(event_df, hide_index=True, use_container_width=True)

with st.container(border=True):
    st.subheader('Segregation of duties between users')
    user_activity_graph(users_activities)

with st.container(border=True):
    trans_matrix_col, handover_col = st.columns(2)
    
    with trans_matrix_col:
        workgroup_transition_matrix_df = workgroup_process_df.pivot_table(index=colWorkgroup, columns=colWorkgroup+'_2', values=colCase, aggfunc='count').fillna(0)
        st.subheader("Transition matrix between workgroups")
        st.write(workgroup_transition_matrix_df.style.format("{:.0f}").background_gradient(cmap='Greens'))

    with handover_col:
        st.subheader('Handover of work between workgroups')
        workgroup_activity_graph(hand_over_workgroups)

with st.container(border=True):
    st.subheader('Segregation of duties between workgroups')
    user_activity_graph(workgroup_activities)

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