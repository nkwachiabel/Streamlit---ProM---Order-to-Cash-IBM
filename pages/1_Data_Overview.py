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
colCustomer = customer_col()
filtered_df = filtered_dataset()
original_df = full_dataset()
full_df = full_dataset_edited()

st.title("Data Overview")
st.divider()

# Calculated metrics
start_time = earliest_time(full_df,colTimestamp)
end_time = latest_time(full_df,colTimestamp)

# Date row and columns
_, _, _, date1, date2 = st.columns(5)

# Date filters
with date1:
    start_date = st.date_input("Start Date", start_time)
    start_date = pd.to_datetime(start_date)

with date2:
    end_date = st.date_input("End Date", end_time)
    end_date = pd.to_datetime(end_date)

total_no_of_cases = unique_count(full_df,colCase)
total_no_of_closed_cases = full_df[full_df['Status'] == 'Open'][colCase].nunique()
incorrect_start_cases = full_df[~full_df['First_Activity'].isin(first_activities) & full_df['Last_Activity'].isin(last_activities)][colCase].nunique()
first_activities_table = activity_occurrence_count(full_df, colActivity, 'First_Activity')
last_activities_table = activity_occurrence_count(full_df, colActivity, 'Last_Activity')

no_of_cases = unique_count(filtered_df,colCase)
no_of_activities = unique_count(filtered_df,colActivity)
no_of_events = total_count(filtered_df,colActivity)
no_of_users = unique_count(filtered_df, colResources)
no_of_products = unique_count(filtered_df, colProduct)
event_bar_df = event_graph_fn(filtered_df,colTimestamp,'Month/Year')
cases_bar_df = cases_graph_fn(filtered_df,colTimestamp,'Month/Year')
event_df = activity_occurrence(filtered_df, colCase, colActivity)
customer_df = activity_occurrence(filtered_df, colCase, colCustomer)
variants_sum = activities_trace(filtered_df, colCase, colActivity,colTimestamp)
no_of_variants = unique_count(filtered_df,'Variants')
var_table = var_table_process_analysis(filtered_df,'Variants',colCase)
products_table = activity_occurrence(filtered_df, colCase, colProduct)

event_per_case_df = event_per_case_analysis(filtered_df, colCase, colTimestamp,colActivity,event_id='Event_ID',case_length='Case_Length')
closed_first_activities_table = activity_occurrence_count(filtered_df, colActivity, 'First_Activity')
closed_last_activities_table = activity_occurrence_count(filtered_df, colActivity, 'Last_Activity')

data_overview, open_close = st.tabs(['Data Overview', 'Open/closed cases'])

with data_overview:
    with st.container(border=True):
        cases_metric, activity_metric, event_metric, users_metric, product_metric, variant_metric = st.columns(6)
        
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

        # No. of users
        with users_metric:
            # no_of_users = format(no_of_events, ",.0f")
            st.metric(label="Number of users", value=no_of_users)

        # No. of products
        with product_metric:
            # no_of_users = format(no_of_events, ",.0f")
            st.metric(label="Number of products", value=no_of_products)

        # No. of variants
        with variant_metric:
            no_of_variants = format(no_of_variants, ",.0f")
            st.metric(label="Number of variants", value=no_of_variants)
    
    with st.container(border=True):
        visCasesGraph, colVariantTable = st.columns([4,2])
        with visCasesGraph:
            st.markdown('<span style="font-size: 16px; font-weight: bold;">Count of cases per month by start date</span>', unsafe_allow_html=True)
            vertical_bar(cases_bar_df,'Month/Year','Count','',color_graph="rgba(49, 51, 60)")

        with colVariantTable:
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
    
    with st.container(border=True):
        visEventsGraph, colActivityTable = st.columns([4,2])
        with visEventsGraph:
            st.markdown('<span style="font-size: 16px; font-weight: bold;">Count of events per month</span>', unsafe_allow_html=True)
            vertical_bar(event_bar_df,'Month/Year','Count','',color_graph="rgba(49, 51, 60)")
        with colActivityTable:
            # with activity_distribution_column:
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

    with st.container(border=True):
        events_per_case_column, variants_column, activity_distribution_column  = st.columns([2, 2, 2])
        
        with events_per_case_column:
            st.markdown('<span style="font-size: 16px; font-weight: bold;">Event per case</span>', unsafe_allow_html=True)
            vertical_bar(event_per_case_df,'Case_Length','Percent','',color_graph="rgba(49, 51, 60)")
        
        # Activity distribution
        with activity_distribution_column:
            st.markdown('<span style="font-size: 16px; font-weight: bold;">Number of tickets by customers</span>', unsafe_allow_html=True)
            st.data_editor(
                customer_df,
                column_config={
                    "Percent": st.column_config.ProgressColumn(
                        "Percent",
                        help="Percentage of Occurrence",
                        format="%.2f %%",
                        min_value=customer_df['Percent'].min(),
                        max_value=customer_df['Percent'].max(),
                    ),
                },
                hide_index=True,
                use_container_width=True,
                height=400
            )

        # Activity distribution
        with variants_column:
            st.markdown('<span style="font-size: 16px; font-weight: bold;">Number of tickets by products</span>', unsafe_allow_html=True)
            fig = px.pie(products_table, values = "Percent", names = colProduct, template = "gridon")
            fig.update_traces(text = products_table["Number of Cases"], textposition = "inside")
            st.plotly_chart(fig,use_container_width=True)

       

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