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
total_no_of_closed_cases = full_df[full_df['Case_Status'] == 'Open'][colCase].nunique()
total_no_of_events = total_count(full_df,colActivity)
incorrect_start_cases = full_df[~full_df['First_Activity'].isin(first_activities) & full_df['Last_Activity'].isin(last_activities)][colCase].nunique()
first_activities_table = activity_occurrence_count(full_df, colActivity, 'First_Activity')
last_activities_table = activity_occurrence_count(full_df, colActivity, 'Last_Activity')
distinct_log = filtered_df[filtered_df['Event_ID'] == 1].reset_index(drop=True)
no_of_cases = unique_count(filtered_df,colCase)
no_of_activities = unique_count(filtered_df,colActivity)
no_of_events = total_count(filtered_df,colActivity)
no_of_users = unique_count(filtered_df, colResources)
no_of_products = unique_count(filtered_df, colProduct)
total_net_value = distinct_log['NetValue'].sum()
event_bar_df = event_graph_fn(filtered_df,colTimestamp,'Month/Year')
cases_bar_df = cases_graph_fn(filtered_df,colTimestamp,'Month/Year')
event_df = activity_occurrence(filtered_df, colCase, colActivity)
customer_df = activity_occurrence(filtered_df, colCase, colCustomer)
variants_sum = activities_trace(filtered_df, colCase, colActivity,colTimestamp)
no_of_variants = unique_count(filtered_df,'Variants')
var_table = var_table_process_analysis(filtered_df,'Variants',colCase)
products_table = activity_occurrence(filtered_df, colCase, colProduct)
order_type_table = distinct_log.groupby(by=['Product_hierarchy','OrderType'])['NetValue'].sum().sort_values(ascending=False).reset_index()
event_per_case_df = event_per_case_analysis(filtered_df, colCase, colTimestamp,colActivity,event_id='Event_ID',case_length='Case_Length')
closed_first_activities_table = activity_occurrence_count(filtered_df, colActivity, 'First_Activity')
closed_last_activities_table = activity_occurrence_count(filtered_df, colActivity, 'Last_Activity')

data_overview, open_close = st.tabs(['Data Overview', 'Open/closed cases'])
with data_overview:
    with st.container(border=True):
        cases_metric, activity_metric, event_metric, users_metric, product_metric, net_value_metric, variant_metric = st.columns(7)
        
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

        with net_value_metric:
            total_net_value = round(total_net_value/1000000,2)
            total_net_value = format(total_net_value, ",.2f")
            st.metric(label="Net Value of orders", value=f"${total_net_value}M")

        # No. of variants
        with variant_metric:
            no_of_variants = format(no_of_variants, ",.0f")
            st.metric(label="Number of variants", value=no_of_variants)
    
    with st.container(border=True):
        visCasesGraph, colVariantTable = st.columns([5,3])
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
        visEventsGraph, colActivityTable = st.columns([5,3])
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
        variants_column, activity_distribution_column  = st.columns([3, 3])
                
        # Activity distribution
        with activity_distribution_column:
            st.markdown('<span style="font-size: 16px; font-weight: bold;">Net value of orders by product hierarchy and order type</span>', unsafe_allow_html=True)
            st.data_editor(order_type_table, hide_index=True, use_container_width=True)

        # Activity distribution
        with variants_column:
            st.markdown('<span style="font-size: 16px; font-weight: bold;">Number of orders by products</span>', unsafe_allow_html=True)
            fig = px.pie(products_table, values = "Percent", names = colProduct, template = "gridon")
            fig.update_traces(text = products_table["Number of Cases"], textposition = "inside")
            st.plotly_chart(fig,use_container_width=True)

with open_close:
    with st.container(border=True):
        total_cases, cases_metric_2, open_cases_2, wrong_start_activitty, total_events = st.columns(5)
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

        with total_events:
            total_no_of_events = format(total_no_of_events, ",.0f")
            st.metric(label="Total number of events", value=total_no_of_events)
    
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
    
with st.container(border=True):
    st.subheader('Findings')
    st.write('The Data Overview tab shows the completed cases alone, while the Open/Closed cases tab shows the details of all cases in the eventlog', unsafe_allow_html=True)
    st.markdown('<span style="font-size: 20px; font-weight: bold;">Data Overview tab</span>', unsafe_allow_html=True)
    findings_col1, findings_col2 = st.columns(2)
    with findings_col1:
        data_summary = '''
            After the data quality check and transformation, the eventlog comprises 21,159 cases, encompassing 17 different activities and 110,125 events.
            There are 69 users involved in the process, interacting with 4 different products.
            The total net value of the orders is approximately $241.83 million, and there are 800 distinct process variants identified.  
        '''
        number_of_orders_by_products = '''
            **Number of Orders by Products:**
            The pie chart shows the number of orders divided among different product categories.
            TLC Optical Cables constitute the majority with 57.9% of orders.
            TLC Optical Fibres account for 41.5% of the total orders.
            TLC Connectivity and TLC Optical Ground Cables represent a much smaller portion of orders, with 0.4% and 0.23% of the orders respectively.  
        '''
        net_value_of_orders = '''
            **Net Value of Orders by Product Hierarchy and Order Type:**
            The table provides a detailed breakdown of the net value of orders, grouped by product hierarchy and order type.
            TLC Optical Cables with US-Std. Order type have the highest net value at over USD133 million. 
            TLC Optical Fibres with US-IC Order Fiber type follow, with a net value of approximately USD74 million. 
            Other significant net values are associated with TLC Optical Fibres with US-Internal Transfer and US-Std. Order Fiber types, and TLC Optical Cables with US-Std. IV/C Order and US-Return Order types.
            Asides the US-Consignm.Fill-Up and US-Free of charge, the least net value is associated with TLC Optical Fibres with order type US-Return Order and ZUH2.
            TLC Optical Ground Cables and TLC Connectivity are at the lower end of the net value spectrum compared to the other categories.  
        '''
        st.markdown(data_summary, unsafe_allow_html=True)
        st.markdown(number_of_orders_by_products, unsafe_allow_html=True)
        st.markdown(net_value_of_orders, unsafe_allow_html=True)

    with findings_col2:
        cases_and_events_over_time = '''
            **Cases and Events Over Time:** The "Count of cases per month by start date" bar chart shows a high number of cases starting in January 2016 (2,284 cases), with a general declining trend over time, notably with a significant decrease starting from July 2017.
            The "Count of events per month" bar chart displays a consistent number of events per month without drastic changes over time until July 2017, similar to the number of cases.  
        '''
        process_variants_findings = '''
            **Process Variants:** The "Variants" table illustrates the distribution of cases across different process variants.
              Variant 1 is the most common, accounting for 29.51% of cases, followed by Variant 2 with 22.30%, and so forth.
                The top 5 variants accounts for approximately 60% of these cases.  
        '''
        activity_distribution_findings = '''
            **Activity Distribution:**
            The "Activity Distribution" table shows that every case includes the "Line Creation" activity (100% occurrence). This is due to the fact that the line creation activity is the first activity in the process.
            The next most frequent activity is "LgstCheckOnConfDat Removed" with over 92% occurrence,
            "Delivery" and "Good Issue" are common activities, both with over 82% occurrence among the cases.
            "Header Block Removed" activity occurs in approximately 50.89% of cases.
            Less frequent activities include "Schedule Line Rejected" at 11.76%, "Document released for credit" at 7.43%, "LgstCheckOnConfDat Set" at 2.18% etc.  
        '''
        st.markdown(cases_and_events_over_time, unsafe_allow_html=True)
        st.markdown(process_variants_findings, unsafe_allow_html=True)
        st.markdown(activity_distribution_findings, unsafe_allow_html=True)

    st.markdown('<span style="font-size: 20px; font-weight: bold;">Open/closed cases tab</span>', unsafe_allow_html=True)
    summary2 = '''
        From the eventlog, the first activity is "Line Creation", while the last activity can either be "Goods Issue" or "Schedule Line Rejected" (for orders that were rejected).  
        **Closed cases** - These are cases that start with "Line Creation" and ends with either "Goods Issue" or "Schedule Line Rejected". There were 21,159 cases that falls into this category. Our analysis is focused on these completed cases.  
        **Open cases** - These are cases which starts with "Line Creation" but does not end with either "Goods Issue" or "Schedule Line Rejected".  There were 8,908 open cases and a dashboard has been created to analyse and monitor these cases.  
        **Wrong start activity** - These are cases which ends with either "Goods Issue" or "Schedule Line Rejected", but do not start with "Line Creation". 5,464 cases fell into this category and were not considered in the analysis. This can be due to the way the eventlog was extracted.  
        **Other cases** - There were 10,294 cases which did not start with "Line Creation" and did not also end with either "Goods Issue" or "Schedule Line Rejected". It was assumed that these cases were included irrespective of the stages there were when the eventlog was extracted and were not considered in the analysis.  
    '''
    st.markdown(summary2, unsafe_allow_html=True)
    first_activities_findings = '''
        **First Activities:**
        The most common first activity for cases is "Line Creation," making up 65.61% of the cases.
        "Delivery" is the next most frequent starting activity, accounting for 15.47%.
        Other activities such as "Header Block Removed" and "LgstCheckOnConfDat Removed" are less common, with 6.23% and 5.90% respectively.
        Less frequent initial activities include "Sched.Line Changed Delivery Date," "Good Issue," and "Document released for credit."  
    '''
    last_activities_findings = '''
        **Last Activities:**
        The most frequent last activity is "Good Issue," which concludes 52.43% of cases.
        "LgstCheckOnConfDat Removed" is the final activity in 16.23% of cases.
        "Line Creation" and "Delivery" also appear as the last activities in 10.16% and 7.54% of cases, respectively.
        Activities like "Schedule Line Rejected" and "Header Block Removed" are the final steps in a smaller portion of cases.
    '''
    findings_col3, findings_col4 = st.columns(2)
    with findings_col3:
        st.markdown(first_activities_findings, unsafe_allow_html=True)

    with findings_col4:
        st.markdown(last_activities_findings, unsafe_allow_html=True)


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