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

unique_product_list = get_unique_items(filtered_df,colProduct)
unique_product_list = sorted(unique_product_list, reverse=False)

unique_ordertype_list = get_unique_items(filtered_df,'OrderType')
unique_ordertype_list = sorted(unique_ordertype_list, reverse=False)

unique_usertype_list = get_unique_items(filtered_df,'User_Type')

process_details_df = process_details(filtered_df, colCase, colTimestamp, colActivity)
unique_connections = get_unique_items(process_details_df,'Connection')

# Product filter
with st.sidebar:
    product_list = st.multiselect(options=unique_product_list, label="Products", placeholder="Select product")

with st.sidebar:
    ordertype_list = st.multiselect(options=unique_ordertype_list, label="Order type", placeholder="Select order type")

with st.sidebar:
    usertype_list = st.multiselect(options=unique_usertype_list, label="User type", placeholder="Select user type")

with st.sidebar:
    unique_connections = sorted(unique_connections, reverse=False)
    filtered_connections = st.multiselect(options=unique_connections, key=unique_connections, label="Connections", placeholder="Filter for cases that follows a certain connection") #"Select the first activities in the process"

filtered_df = filtered_df.copy()

if product_list:
    filtered_df = filtered_df[filtered_df[colProduct].isin(product_list)]

if ordertype_list:
    filtered_df = filtered_df[filtered_df['OrderType'].isin(ordertype_list)]

if usertype_list:
    filtered_df = filtered_df[filtered_df['User_Type'].isin(usertype_list)]

if filtered_connections:
    filtered_b = process_details_df[process_details_df['Connection'].isin(filtered_connections)]
    case_ids = filtered_b[colCase].unique()
    filtered_df = filtered_df[filtered_df[colCase].isin(case_ids)]

# Update process details DataFrame based on filtered cases
if not filtered_df.empty:
    process_details_df = process_details(filtered_df, colCase, colTimestamp, colActivity)
else:
    process_details_df = process_details_df


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
        st.subheader('Med. dur. of activities per user')
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
        st.subheader('Handover of work between dept')
        workgroup_activity_graph(hand_over_workgroups)

with st.container(border=True):
    st.subheader('Segregation of duties between dept')
    user_activity_graph(workgroup_activities)


with st.container(border=True):
    st.subheader('Findings')
    st.markdown('<span style="font-size: 20px; font-weight: bold;">Overview</span>', unsafe_allow_html=True)
    st.write('A total of 69 users are analyzed, differentiated as Humans or System automatic jobs (Robots). Roles are distinct per user, with no user holding multiple roles, implying a clear delineation of responsibilities within the system.')

    robot_findings = '''
        7 robot users (User17, User60-65) are identified, mostly handling automated tasks like Delivery and Goods Issue.
        User60 and User61 are the most active robot users, suggesting a significant reliance on automation for these processes.

    '''
    human_findings = '''
        Human users perform a wider array of activities, with User9, a human, notably engaging in more activities than the robots, which may highlight an imbalance in workload distribution.
        The role of Customer Service Representative is the most staffed, indicating a high touchpoint with customers in the process.

    '''
    activity_specific_findings = '''
        "Schedule Line Rejected" is solely performed by User56, whose user type is not recorded, leaving ambiguity regarding human or robot execution.

    '''
    segregation_findings = '''
        The transition matrix exhibits instances of users handing over work to themselves, which could pose a risk for fraudulent activities and calls into question the effectiveness of segregation of duties.

    '''
    detailed_product_findings = '''
        **TLC Connectivity**: Comprises 2 robots and 7 human users across 2 roles: Customer Service Representative and Logistic Operator. Logistic Operator's sole activity is "Header Block Removed," while Customer Service Representatives perform all other activities except for those automated by robots. User20, a Customer Service Representative, appears to undertake the majority of the tasks, which might indicate an overload or inefficiency in task distribution.  

        **TLC Optical Cables**: With 6 robot users and 61 humans, activities such as Delivery and Goods Issue are largely automated. Humans are involved in more nuanced tasks, with User43 handling a significant volume of Delivery and Goods Issue activities.  

        **TLC Optical Fibres**: Characterized by a high level of automation with 6 robots and 7 humans. The roles are diverse, including a Corporate Credit Manager and Customer Service Representatives, among others. User9 emerges as a key human actor, undertaking the bulk of activities, with delivery and header block activities as notable bottlenecks.  

        **TLC Optical Ground Cables**: A mix of 2 robots and 16 humans, with a wider array of roles, including Design Engineers and Master Scheduler. This product line shows better segregation of duties, with User6 being a primary actor in non-automated activities.  

    '''

    findings_col1, findings_col2 = st.columns(2)
    with findings_col1:
        st.markdown('<span style="font-size: 20px; font-weight: bold;">Robot Users</span>', unsafe_allow_html=True)
        st.markdown(robot_findings, unsafe_allow_html=True)

        st.markdown('<span style="font-size: 20px; font-weight: bold;">Human Users</span>', unsafe_allow_html=True)
        st.markdown(human_findings, unsafe_allow_html=True)

        st.markdown('<span style="font-size: 20px; font-weight: bold;">Activity-Specific Observations</span>', unsafe_allow_html=True)
        st.markdown(activity_specific_findings, unsafe_allow_html=True)

        st.markdown('<span style="font-size: 20px; font-weight: bold;">Segregation of Duties and Fraud Risk</span>', unsafe_allow_html=True)
        st.markdown(segregation_findings, unsafe_allow_html=True)

    with findings_col2:
        st.markdown('<span style="font-size: 20px; font-weight: bold;">Detailed Product Hierarchy Analysis</span>', unsafe_allow_html=True)
        st.markdown(detailed_product_findings, unsafe_allow_html=True)




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
'''
st.markdown(f'<style>{css}</style>',unsafe_allow_html=True)