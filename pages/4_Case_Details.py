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

st.title("Case Details")
st.divider()

unique_case_id = get_unique_items(filtered_df,case_id_column)

# Case Filter
with st.sidebar:
    unique_case_id = sorted(unique_case_id, reverse=False)
    st.markdown('<span style="font-size: 16px; font-weight: bold;">Filters</span>', unsafe_allow_html=True)
    case_id_list = st.selectbox(options=unique_case_id, label="Case", placeholder="Select case", index=0) #index=0

filtered_df_updated = filtered_df.copy()
filtered_df_updated = filtered_df_updated[filtered_df_updated[case_id_column]==case_id_list]
filtered_df_updated = filtered_df_updated.sort_values(by=[case_id_column, timestamp_column], ascending=True).reset_index(drop=True)
case_dur = case_duration(filtered_df_updated, case_id_column, timestamp_column).drop('Max', axis=1)
min_dur = case_dur['Case_Duration_days'].min() # minimum case duration
med_dur = case_dur['Case_Duration_days'].median() # median case duration
avg_dur = round(case_dur['Case_Duration_days'].mean(),0) # average case duration
max_dur = case_dur['Case_Duration_days'].max() # maximum case duration

variant_metric_detail = filtered_df_updated['Variants'].unique()
variant_metric_detail = str(variant_metric_detail[0]) if len(variant_metric_detail) > 0 else ""
event_count = filtered_df_updated[activity_column].count()

start_act = start_and_end_activities(filtered_df_updated, case_id_column, activity_column, grouping='First_Activity',level='Start')
end_act = start_and_end_activities(filtered_df_updated, case_id_column, activity_column, grouping='Last_Activity',level='End')
process_details_df = process_details(filtered_df_updated, case_id_column, timestamp_column, activity_column)
pro_det = graph_group_timing(process_details_df, case_id_column, timestamp_column, activity_column)
gra_coun = graph_count(filtered_df_updated, activity_column)
activity_chart_df = activity_gant_chart(filtered_df_updated,case_id_column,timestamp_column,activity_column)    

# No. of closed cases
with st.container(border=True):
    cases_metric, activity_metric, event_metric, variant_metric = st.columns(4)

    with cases_metric:
        st.metric(label="Selected case", value=case_id_list)

    with activity_metric:
        st.metric(label="Duration", value=max_dur)

    with event_metric:
        st.metric(label="No. of events", value=event_count)

    with variant_metric:
        st.metric(label="Variants", value=variant_metric_detail)

# with process_graph_column:
with st.container(border=True):
    _, _, graph_type_column, rankdir_column = st.columns(4)

    # # Graph details - duration or case count
    with graph_type_column:
        graph_type = st.selectbox("Process graph type", ['Show duration only', 'Show duration and case count', 'Show case count only'], index=0)

    # Graph type - Top-botom or Left-right
    with rankdir_column:
        rankdir = st.selectbox("Process graph flow direction", ['LR', 'TB'], index=0)

    st.subheader(" :curly_loop: Process flow Graph")
    if graph_type == 'Show duration and case count':
        process_flow_timing(start_act, end_act,pro_det,gra_coun,start='Start',end='End',activity=activity_column,f_activity='First_Activity',l_activity='Last_Activity', rankdirection=rankdir)
    elif graph_type == 'Show case count only':
        process_flow(start_act, end_act,pro_det,gra_coun,start='Start',end='End',activity=activity_column,f_activity='First_Activity',l_activity='Last_Activity', rankdirection=rankdir)
    else:
        process_flow_duration(start_act, end_act,pro_det,gra_coun,start='Start',end='End',activity=activity_column,f_activity='First_Activity',l_activity='Last_Activity', rankdirection=rankdir)

gantt_data_filtered = activity_chart_df.dropna(subset=['Start'])
with st.container(border=True):
    st.subheader(" :bar_chart: Activity gantt chart")
    fig = px.timeline(gantt_data_filtered, x_start="Start", x_end="End", y=activity_column, color=activity_column)
    fig.update_layout(
        height=300
    )
    st.plotly_chart(fig, use_container_width=True)


with st.expander(':point_right: View Selected Case'):
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