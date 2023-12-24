import streamlit as st
import pandas as pd
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

st.title("Process Analysis")
st.divider()

# First row and column
product_column, vartant_column, conn_column = st.columns([2,2,2])

# Get the unique variants list and unique connections list
first_activity_list = get_unique_items(filtered_df, 'First_Activity')
last_activity_list = get_unique_items(filtered_df, 'Last_Activity')
unique_variant_list = get_unique_items(filtered_df,'Variants')
process_details_df = process_details(filtered_df, colCase, colTimestamp, colActivity)
unique_connections = get_unique_items(process_details_df,'Connection')
unique_product_list = get_unique_items(filtered_df,colProduct)

# Filters
# Activity filter
with st.sidebar:
    st.markdown('<span style="font-size: 16px; font-weight: bold;">Filters</span>', unsafe_allow_html=True)
    st.write('Activities')
    activity_list = get_unique_items(filtered_df,colActivity)
    selected_activities = []
    for activ in activity_list:
        is_selected = st.checkbox(activ, key=activ, value=True)
        if is_selected:
            selected_activities.append(activ)

# First activity filter
with st.sidebar:
    selected_first_activities = st.multiselect(options=first_activity_list, label="First activities", placeholder="Select activity")

# Last activity filter
with st.sidebar:
    selected_last_activities = st.multiselect(options=last_activity_list, label="Last activities", placeholder="Select activity")

# Product filter
with product_column:
    unique_product_list = sorted(unique_product_list, reverse=False)
    product_list = st.multiselect(options=unique_product_list, label="Products", placeholder="Select product")

# Variants filter
with vartant_column:
    unique_variant_list = sorted(unique_variant_list, reverse=False)
    variant_list = st.multiselect(options=unique_variant_list, label="Variants", placeholder="Select variants")

# Connections filter
with conn_column:
    unique_connections = sorted(unique_connections, reverse=False)
    filtered_connections = st.multiselect(options=unique_connections, key=unique_connections, label="Connections", placeholder="Filter for cases that follows a certain connection") #"Select the first activities in the process"

filtered_df_updated = filtered_df.copy()
# Activity filter, # First activity filter, # Last activity filter, # Variants filter, # Connections filter
if selected_activities:
    filtered_df_updated = filtered_df_updated[filtered_df_updated[colActivity].isin(selected_activities)]

if product_list:
    filtered_df_updated = filtered_df_updated[filtered_df_updated[colProduct].isin(product_list)]

if selected_first_activities:
    filtered_df_updated = filtered_df_updated[filtered_df_updated['First_Activity'].isin(selected_first_activities)]

if selected_last_activities:
    filtered_df_updated = filtered_df_updated[filtered_df_updated['Last_Activity'].isin(selected_last_activities)]

if variant_list:
    filtered_df_updated = filtered_df_updated[filtered_df_updated['Variants'].isin(variant_list)]

if filtered_connections:
    filtered_b = process_details_df[process_details_df['Connection'].isin(filtered_connections)]
    case_ids = filtered_b[colCase].unique()
    filtered_df_updated = filtered_df_updated[filtered_df_updated[colCase].isin(case_ids)]

# Update process details DataFrame based on filtered cases
if not filtered_df_updated.empty:
    process_details_df = process_details(filtered_df_updated, colCase, colTimestamp, colActivity)
else:
    process_details_df = process_details_df

# filtered_df_updated = filtered_df_updated[filtered_df_updated[colActivity].isin(selected_activities) & filtered_df_updated['First_Activity'].isin(selected_first_activities) & filtered_df_updated['Last_Activity'].isin(selected_last_activities)]
filtered_df_updated = filtered_df_updated.sort_values(by=[colCase, colTimestamp], ascending=True).reset_index(drop=True)

no_of_cases = unique_count(filtered_df_updated,colCase)
no_of_activities = unique_count(filtered_df_updated,colActivity)
no_of_events = total_count(filtered_df_updated,colActivity)
no_of_variants = unique_count(filtered_df_updated,'Variants')
distinct_log = filtered_df_updated[filtered_df_updated['Event_ID'] == 1].reset_index(drop=True)
total_net_value = distinct_log['NetValue'].sum()
ontime_order_rate = (distinct_log[distinct_log['Delayed'] == 'IN TIME'][colCase].count()/distinct_log[colCase].count())*100
rejected_orders = (distinct_log[distinct_log['Last_Activity'] == 'Schedule Line Rejected'][colCase].count()/distinct_log[colCase].count())*100
order_type_pie_df = activity_occurrence(filtered_df_updated, colCase, 'OrderType')
analysis_process_df = filtered_df_updated.groupby(['OrderType', colCustomer]).agg({colCase: ['nunique'], 'NetValue': ['sum']})
analysis_process_df = analysis_process_df.sort_values(by=('NetValue', 'sum'), ascending=False).reset_index()
start_act = start_and_end_activities(filtered_df_updated, colCase, colActivity, grouping='First_Activity',level='Start')
end_act = start_and_end_activities(filtered_df_updated, colCase, colActivity, grouping='Last_Activity',level='End')
pro_det = graph_group_timing(process_details_df, colCase, colTimestamp, colActivity)
gra_coun = graph_count(filtered_df_updated, colActivity)

with st.container(border=True):
    cases_metric, activity_metric, event_metric, net_value_metric, ontime_metric, rejected_order_metric, variant_metric = st.columns(7)

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

    with net_value_metric:
        total_net_value = round(total_net_value/1000000,2)
        total_net_value = format(total_net_value, ",.2f")
        st.metric(label="Net Value of orders", value=f"${total_net_value}M")

    with ontime_metric:
        ontime_order_rate = "{:.2f}%".format(ontime_order_rate)
        st.metric(label="On-time order rate", value=ontime_order_rate, help='The percent of orders that were delivered on time')

    with rejected_order_metric:
        rejected_orders = "{:.2f}%".format(rejected_orders)
        st.metric(label="Rejected order rate", value=rejected_orders, help='The percent of orders that were rejected')

with st.container(border=True):
    process_graph_column, variant_column = st.columns([4,2])

    with process_graph_column:
        st.subheader(" :curly_loop: Process flow Graph")
        graph_type_column, rankdir_column = st.columns(2)
        # Graph details - duration or case count
        with graph_type_column:
            graph_type = st.selectbox("Process graph type", ['Show duration and case count', 'Show duration only', 'Show case count only'], index=0)

        # Graph type - Top-botom or Left-right
        with rankdir_column:
            rankdir = st.selectbox("Process graph flow direction", ['LR', 'TB'], index=0)

        if graph_type == 'Show duration and case count':
            process_flow_timing(start_act, end_act,pro_det,gra_coun,start='Start',end='End',activity=colActivity,f_activity='First_Activity',l_activity='Last_Activity', rankdirection=rankdir)
        elif graph_type == 'Show case count only':
            process_flow(start_act, end_act,pro_det,gra_coun,start='Start',end='End',activity=colActivity,f_activity='First_Activity',l_activity='Last_Activity', rankdirection=rankdir)
        else:
            process_flow_duration(start_act, end_act,pro_det,gra_coun,start='Start',end='End',activity=colActivity,f_activity='First_Activity',l_activity='Last_Activity', rankdirection=rankdir)

    with variant_column:
        st.subheader('Variants')
        variant_tab = var_table_process_analysis(filtered_df_updated,'Variants',colCase)
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
    transition_matrix_df = process_details_df.pivot_table(index=colActivity, columns=colActivity+'_2', values=colCase, aggfunc='count').fillna(0)
    st.subheader("Transition Matrix", help='This shows the transitions between various activities in the process. The rows are the starting point (source), the columns are the end point (target) and the numbers are the number of times a particular transition occurs')
    st.write(transition_matrix_df.style.format("{:.0f}").background_gradient(cmap='Greens'))


with st.container(border=True):
    order_type_pie_col, analysis_process_col = st.columns(2)
    with order_type_pie_col:
        st.markdown('<span style="font-size: 16px; font-weight: bold;">Number of tickets by products</span>', unsafe_allow_html=True)
        fig = px.pie(order_type_pie_df, values = "Percent", names = 'OrderType', template = "gridon")
        fig.update_traces(text = order_type_pie_df["Number of Cases"], textposition = "inside")
        st.plotly_chart(fig,use_container_width=True)

    with analysis_process_col:
        st.markdown('<span style="font-size: 16px; font-weight: bold;">Net value by product hierarchy and order type</span>', unsafe_allow_html=True)
        st.data_editor(analysis_process_df, hide_index=True, use_container_width=True)


with st.expander(':point_right: View Selected Cases'):
    case_ids_filtered = filtered_df_updated[colCase].unique()
    filtered_df_view = original_df[original_df[colCase].isin(case_ids_filtered)]
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
[data-testid="stMetricValue"] > div {
    font-size: 1.5rem;
}
[data-testid="stCheckbox"] > p {
    font-size: 13px;
}
'''
st.markdown(f'<style>{css}</style>',unsafe_allow_html=True)