import streamlit as st
import pandas as pd
import graphviz
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

st.title("Process Analysis")

st.divider()

# First row and column
vartant_column, conn_column, graph_type_column, rankdir_column, = st.columns([2,2,2,2])

# Get the unique variants list and unique connections list
first_activity_list = get_unique_items(filtered_df, 'First_Activity')
last_activity_list = get_unique_items(filtered_df, 'Last_Activity')
unique_variant_list = get_unique_items(filtered_df,'Variants')
process_details_df = process_details(filtered_df, case_id_column, timestamp_column, activity_column)
unique_connections = get_unique_items(process_details_df,'Connection')

# Filters
# Activity filter
with st.sidebar:
    st.markdown('<span style="font-size: 16px; font-weight: bold;">Filter by Activity</span>', unsafe_allow_html=True)
    activity_list = get_unique_items(filtered_df,activity_column)
    selected_activities = []
    for activ in activity_list:
        is_selected = st.checkbox(activ, key=activ, value=True)
        if is_selected:
            selected_activities.append(activ)

# First activity filter
with st.sidebar:
    st.markdown('<span style="font-size: 16px; font-weight: bold;">Filter by First Activity</span>', unsafe_allow_html=True)
    selected_first_activities = st.multiselect(options=first_activity_list, label="First activities", placeholder="Select activity")

# Last activity filter
with st.sidebar:
    st.markdown('<span style="font-size: 16px; font-weight: bold;">Filter by Last Activity</span>', unsafe_allow_html=True)
    selected_last_activities = st.multiselect(options=last_activity_list, label="Last activities", placeholder="Select activity")

# Variants filter
with vartant_column:
    unique_variant_list = sorted(unique_variant_list, reverse=False)
    variant_list = st.multiselect(options=unique_variant_list, label="Variants", placeholder="Select variants")

# Connections filter
with conn_column:
    unique_connections = sorted(unique_connections, reverse=False)
    filtered_connections = st.multiselect(options=unique_connections, key=unique_connections, label="Connections", placeholder="Filter for cases that follows a certain connection") #"Select the first activities in the process"

# Graph details - duration or case count
with graph_type_column:
    graph_type = st.selectbox("Process graph type", ['Show duration and case count', 'Show duration only', 'Show case count only'], index=0)

# Graph type - Top-botom or Left-right
with rankdir_column:
    rankdir = st.selectbox("Process graph flow direction", ['LR', 'TB'], index=0)

filtered_df_updated = filtered_df.copy()
# Activity filter, # First activity filter, # Last activity filter, # Variants filter, # Connections filter
if selected_activities:
    filtered_df_updated = filtered_df_updated[filtered_df_updated[activity_column].isin(selected_activities)]

if selected_first_activities:
    filtered_df_updated = filtered_df_updated[filtered_df_updated['First_Activity'].isin(selected_first_activities)]

if selected_last_activities:
    filtered_df_updated = filtered_df_updated[filtered_df_updated['Last_Activity'].isin(selected_last_activities)]

if variant_list:
    filtered_df_updated = filtered_df_updated[filtered_df_updated['Variants'].isin(variant_list)]

if filtered_connections:
    filtered_b = process_details_df[process_details_df['Connection'].isin(filtered_connections)]
    case_ids = filtered_b[case_id_column].unique()
    filtered_df_updated = filtered_df_updated[filtered_df_updated[case_id_column].isin(case_ids)]

# Update process details DataFrame based on filtered cases
if not filtered_df_updated.empty:
    process_details_df = process_details(filtered_df_updated, case_id_column, timestamp_column, activity_column)
else:
    process_details_df = process_details_df

# filtered_df_updated = filtered_df_updated[filtered_df_updated[activity_column].isin(selected_activities) & filtered_df_updated['First_Activity'].isin(selected_first_activities) & filtered_df_updated['Last_Activity'].isin(selected_last_activities)]
filtered_df_updated = filtered_df_updated.sort_values(by=[case_id_column, timestamp_column], ascending=True).reset_index(drop=True)

no_of_cases = unique_count(filtered_df_updated,case_id_column)
no_of_activities = unique_count(filtered_df_updated,activity_column)
no_of_events = total_count(filtered_df_updated,activity_column)
no_of_variants = unique_count(filtered_df_updated,'Variants')

start_act = start_and_end_activities(filtered_df_updated, case_id_column, activity_column, grouping='First_Activity',level='Start')
end_act = start_and_end_activities(filtered_df_updated, case_id_column, activity_column, grouping='Last_Activity',level='End')
pro_det = graph_group_timing(process_details_df, case_id_column, timestamp_column, activity_column)
gra_coun = graph_count(filtered_df_updated, activity_column)


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
    process_graph_column, variant_column = st.columns([4,2])

    with process_graph_column:
        st.subheader(" :curly_loop: Process flow Graph")
        # st.divider()
        if graph_type == 'Show duration and case count':
            process_flow_timing(start_act, end_act,pro_det,gra_coun,start='Start',end='End',activity=activity_column,f_activity='First_Activity',l_activity='Last_Activity', rankdirection=rankdir)
        elif graph_type == 'Show case count only':
            process_flow(start_act, end_act,pro_det,gra_coun,start='Start',end='End',activity=activity_column,f_activity='First_Activity',l_activity='Last_Activity', rankdirection=rankdir)
        else:
            process_flow_duration(start_act, end_act,pro_det,gra_coun,start='Start',end='End',activity=activity_column,f_activity='First_Activity',l_activity='Last_Activity', rankdirection=rankdir)

    with variant_column:
        st.subheader('Variants')
        # st.divider()
        variant_tab = var_table_process_analysis(filtered_df_updated,'Variants',case_id_column)
        # st.markdown('<span style="font-size: 16px; font-weight: bold;">Variants</span>', unsafe_allow_html=True)
        st.data_editor(
        variant_tab,
        column_config={
            "Percent": st.column_config.ProgressColumn(
                "Percent",
                help="Percentage of Occurrence",
                format="%.2f %%",
                min_value=variant_tab['Percent'].min(),
                max_value=variant_tab['Percent'].max(),
            ),
        },
        hide_index=True,
        use_container_width=True,
        height=400
    )

with st.container(border=True):
    transition_matrix_df = process_details_df.pivot_table(index=activity_column, columns=activity_column+'_2', values=case_id_column, aggfunc='count').fillna(0)
    st.subheader("Transition Matrix")
    st.write(transition_matrix_df.style.format("{:.0f}").background_gradient(cmap='Greens'))

with st.expander(':point_right: View Selected Cases'):
    case_ids_filtered = filtered_df_updated[case_id_column].unique()
    filtered_df_view = original_dataset[original_dataset[case_id_column].isin(case_ids_filtered)]
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
'''
st.markdown(f'<style>{css}</style>',unsafe_allow_html=True)