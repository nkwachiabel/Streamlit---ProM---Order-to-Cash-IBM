import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from prom_functions import get_unique_items,case_duration,start_and_end_activities,process_details,graph_group_timing,graph_count,activity_gant_chart
from visuals_prom import process_flow_timing,process_flow,process_flow_duration
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

st.title("Case Details")
st.write('This page shows information relating to a particular case by using the filter at the sidebar to select a case.')
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

unique_case_id = get_unique_items(filtered_df,colCase)

# Case Filter
with st.sidebar:
    unique_case_id = sorted(unique_case_id, reverse=False)
    st.markdown('<span style="font-size: 16px; font-weight: bold;">Filters</span>', unsafe_allow_html=True)
    case_id_list = st.selectbox(options=unique_case_id, label="Case", placeholder="Select case", index=0) #index=0

filtered_case_df = filtered_df.copy()
filtered_case_df = filtered_df[filtered_df[colCase]==case_id_list]
filtered_case_df = filtered_case_df.sort_values(by=[colCase, colTimestamp], ascending=True).reset_index(drop=True)

case_dur = case_duration(filtered_case_df, colCase, colTimestamp).drop('Max', axis=1)
min_dur = case_dur['Case_Duration_days'].min() # minimum case duration
med_dur = case_dur['Case_Duration_days'].median() # median case duration
avg_dur = round(case_dur['Case_Duration_days'].mean(),0) # average case duration
max_dur = case_dur['Case_Duration_days'].max() # maximum case duration

variant_metric_detail = filtered_case_df['Variants'].unique()
variant_metric_detail = str(variant_metric_detail[0]) if len(variant_metric_detail) > 0 else ""
event_count = filtered_case_df[colActivity].count()

start_act_1 = start_and_end_activities(filtered_case_df, colCase, colActivity, grouping='First_Activity',level='Start')
end_act_1 = start_and_end_activities(filtered_case_df, colCase, colActivity, grouping='Last_Activity',level='End')
process_details_df_1 = process_details(filtered_case_df, colCase, colTimestamp, colActivity)
pro_det_1 = graph_group_timing(process_details_df_1, colCase, colTimestamp, colActivity)
gra_coun_1 = graph_count(filtered_case_df, colActivity)
activity_chart_df = activity_gant_chart(filtered_case_df,colCase,colTimestamp,colActivity)

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
    st.subheader(" :curly_loop: Process flow Graph")
    _, _, graph_type_column, rankdir_column = st.columns(4)

    # # Graph details - duration or case count
    with graph_type_column:
        graph_type = st.selectbox("Process graph type", ['Show duration only', 'Show duration and case count', 'Show case count only'], index=0)

    # Graph type - Top-botom or Left-right
    with rankdir_column:
        rankdir = st.selectbox("Process graph flow direction", ['LR', 'TB'], index=0)

    if graph_type == 'Show duration and case count':
        process_flow_timing(start_act_1, end_act_1,pro_det_1,gra_coun_1,colActivity,start='Start',end='End',f_activity='First_Activity',l_activity='Last_Activity', rankdirection=rankdir)
    elif graph_type == 'Show case count only':
        process_flow(start_act_1, end_act_1,pro_det_1,gra_coun_1,colActivity,start='Start',end='End',f_activity='First_Activity',l_activity='Last_Activity', rankdirection=rankdir)
    else:
        process_flow_duration(start_act_1, end_act_1,pro_det_1,gra_coun_1,colActivity,start='Start',end='End',f_activity='First_Activity',l_activity='Last_Activity', rankdirection=rankdir)

with st.container(border=True):
    st.subheader(" :bar_chart: Activity gantt chart")
    activity_chart_df[colActivity] = activity_chart_df[colActivity].astype(str)
    fig = px.timeline(activity_chart_df, x_start="Start", x_end="End", y=colActivity,color=colActivity)#, )
    fig.update_layout(
        height=300
    )
    # fig.update_yaxes(
    #     autorange='reversed'
    # )
    st.plotly_chart(fig, use_container_width=True)

with st.container(border=True):
    st.data_editor(activity_chart_df)
