import pandas as pd
import streamlit as st
import numpy as np

months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September','October', 'November','December']

def initial_dataset_prep(df, case_column, activity_column, timestamp_column):
    df[timestamp_column] = pd.to_datetime(df[timestamp_column])
    df['Year'] = df[timestamp_column].dt.year
    df['Month_Number'] = df[timestamp_column].dt.month
    df['Month_Name'] = df[timestamp_column].dt.strftime('%B')
    df['Day'] = df[timestamp_column].dt.day
    df['Month_Name'] = pd.Categorical(df['Month_Name'], categories=months, ordered=True)
    df = df.sort_values(by=[case_column,timestamp_column],ascending=True).reset_index(drop=True)
    df['Event_ID'] = df.groupby(case_column).cumcount()+1
    df['Activity_Duration'] = df.groupby([case_column])[timestamp_column].diff().dt.days # Duration in days
    df['Activity_Duration'] = df['Activity_Duration'].fillna(0)
    df_2 = variant_analysis(df,case_column, activity_column, timestamp_column)
    first_last = get_first_last_activities(df_2)
    variant_trace = df_2.copy()
    variant_trace.drop(['First_Activity','Last_Activity'], axis=1, inplace=True)
    variant_trace = activities_trace_only(variant_trace)
    variant_trace = variant_trace[['Trace']]
    variant_trace = variant_trace.reset_index()
    variants_sum = activities_trace(df, case_column, activity_column,timestamp_column)
    variants_sum = pd.merge(variants_sum, variant_trace, right_on='Trace', left_on='Trace')
    variants_sum = pd.merge(variants_sum, first_last, right_index=True, left_on=case_column)
    df = pd.merge(df, variants_sum, right_on=case_column, left_on=case_column)
    return df

def datetime_format(df, col_name):
    df[col_name] = pd.to_datetime(df[col_name])
    return df

def earliest_time(df,col_name):
    return df[col_name].min()

def latest_time(df,col_name):
    return df[col_name].max()

def unique_count(df, col_name):
    return df[col_name].nunique()

def total_count(df, col_name):
    return df[col_name].count()

def get_unique_items(df, col_name):
    return df[col_name].unique()

def percent_column(df,col_name,count_column_name,new_column='Percent'):
    event_df = df.groupby(by=[col_name])[count_column_name].count().reset_index(name='Count')
    event_df[new_column] = round((event_df['Count']/event_df['Count'].sum())*100,2)
    return event_df

def event_graph_fn(df, col_name, new_column_name):
    event_df = df.copy()
    # Convert to period for month-level grouping
    event_df[new_column_name] = event_df[col_name].dt.to_period('M')

    # Group by the datetime period
    grouped = event_df.groupby(new_column_name)

    # Create a new DataFrame with correct chronological order
    sorted_event_df = pd.DataFrame({
        'Month/Year': [period.strftime("%Y-%b") for period in grouped.groups.keys()],
        'Count': grouped.size().values
    })

    return sorted_event_df

def cases_graph_fn(df, col_name, new_column_name):
    event_df = df.copy()
    event_df = event_df[event_df['Event_ID'] == 1].reset_index()
    # Convert to period for month-level grouping
    event_df[new_column_name] = event_df[col_name].dt.to_period('M')

    # Group by the datetime period
    grouped = event_df.groupby(new_column_name)

    # Create a new DataFrame with correct chronological order
    sorted_event_df = pd.DataFrame({
        'Month/Year': [period.strftime("%Y-%b") for period in grouped.groups.keys()],
        'Count': grouped.size().values
    })

    return sorted_event_df

def variant_analysis(df,case_id, activities, timestamp):
    # Get the process variants
    variants = df.copy()
    variants = variants.sort_values(by=[case_id,timestamp],ascending=True).reset_index(drop=True)
    variants['Count'] = variants.groupby(case_id).cumcount()+1
    variants = variants.pivot(index=case_id, columns='Count', values=activities)
    return variants

def get_first_last_activities(df):
    df['Last_Activity'] = df.apply(last_activity, axis=1)
    df['First_Activity'] = df[1]
    df = df[['First_Activity','Last_Activity']]
    return df

def activities_trace_only(df):
    # Get the process variants
    # variants = variant_analysis(df,case_id, activities, timestamp)
    # Fill the empty cells (NaN) with 'X'
    variants = df.fillna('X')
    variants = variants.astype('str')
    
    # Get the trace of each case by joining all the columns together, separated by a comma (,) and replace ',X' with nothing to delete the ',X'
    variants['Trace'] = variants.apply(lambda x: ','.join(x),axis=1)
    variants['Trace'] = variants['Trace'].apply(lambda x: x.replace(',X',''))
    return variants

# @st.cache_data
def activities_trace(df,case_id, activities, timestamp):
    # Get the process variants
    variants = variant_analysis(df,case_id, activities, timestamp)
    # Fill the empty cells (NaN) with 'X'
    variants = variants.fillna('X')
    variants = variants.astype('str')
    
    # Get the trace of each case by joining all the columns together, separated by a comma (,) and replace ',X' with nothing to delete the ',X'
    variants['Trace'] = variants.apply(lambda x: ','.join(x),axis=1)
    variants['Trace'] = variants['Trace'].apply(lambda x: x.replace(',X',''))
    
    # Group the similar variants and get the count
    variants_sum = variants[['Trace',1]].groupby(['Trace'], as_index=False).count()
    variants_sum = variants_sum.sort_values(by=1, ascending=False).reset_index()
    del variants_sum['index']
    variants_sum = variants_sum.reset_index()
    variants_sum['index'] = variants_sum['index']+1
    variants_sum = variants_sum.rename(columns={'index':'Variant_no',1:'Number of Cases'})
    variants_sum['Variants'] = 'Variant ' +variants_sum['Variant_no'].astype(str)
    variants_sum['Percent'] = round((variants_sum['Number of Cases']/variants_sum['Number of Cases'].sum())*100,2)
    # variants_sum = variants_sum['Variants'].count()
    return variants_sum

def event_per_case_analysis(df, case_id, timestamp,activity,event_id='Event_ID',case_length='Case_Length'):
    event_per_case = df.copy()
    event_per_case = event_per_case.sort_values(by=[case_id,timestamp],ascending=True).reset_index(drop=True)
    event_per_case[event_id] = event_per_case.groupby([case_id]).cumcount()+1
    event_per_case = event_per_case.pivot(index=case_id, columns=event_id, values=activity)
    event_per_case[case_length] = event_per_case.apply(lambda row: row[pd.notnull(row)].count(), axis=1)
    event_per_case = percent_column(event_per_case,case_length,case_length)
    return event_per_case

def activity_occurrence(df, case_column, activity_column):
    total_cases = df.copy()
    total_cases_count = total_cases[case_column].nunique()
    activity_occurrence = total_cases.groupby(activity_column)[case_column].nunique().reset_index(name='Number of Cases')
    activity_occurrence['Percent'] = round((activity_occurrence['Number of Cases'] / total_cases_count) * 100,2)
    activity_occurrence = activity_occurrence[[activity_column,'Percent','Number of Cases']]
    activity_occurrence = activity_occurrence.sort_values(by=['Percent'],ascending=False).reset_index(drop=True)
    return activity_occurrence

def activity_occurrence_count(df, case_column, activity_column):
    total_cases = df.copy()
    total_cases = total_cases[total_cases['Event_ID'] == 1].reset_index()
    total_cases_count = total_cases[case_column].count()
    activity_occurrence = total_cases.groupby(activity_column)[case_column].count().reset_index(name='Number of Cases')
    activity_occurrence['Percent'] = round((activity_occurrence['Number of Cases'] / total_cases_count) * 100,2)
    activity_occurrence = activity_occurrence[[activity_column,'Percent','Number of Cases']]
    activity_occurrence = activity_occurrence.sort_values(by=['Percent'],ascending=False).reset_index(drop=True)
    return activity_occurrence

def last_activity(a):
    if a.last_valid_index() is None:
        return np.nan
    else:
        return a[a.last_valid_index()]

def variant_table(df):
    df = df.copy()
    df = df[['Variants', 'Percent', 'Number of Cases']]
    return df

# Process analysis functions
def func(x):
    # Get the last valid index (last activity per case)
    if x.last_valid_index() is None:
        return np.nan
    else:
        return x[x.last_valid_index()]

def activity_list(df, case_id, activities):
    # Get the last and first activity for each case
    activities_list = df.copy()
    activities_list['Count'] = activities_list.groupby(case_id).cumcount()+1
    activities_list = activities_list.pivot(index=case_id, columns='Count', values=activities)

    activities_list['Last_Activity'] = activities_list.apply(last_activity, axis=1)
    activities_list['First_Activity'] = activities_list[1]
    return activities_list

def start_and_end_activities(df, case_id, activities, grouping = 'First_Activity',level='Start'):
    # activities_list = activity_list(df, case_id, activities)
    start_act = df.groupby([grouping])[case_id].nunique()
    start_act = start_act.to_frame(name='Count').reset_index()
    start_act[level] = level
    start_act = start_act[[level, grouping,'Count']]
    start_act = start_act.sort_values(by='Count', ascending=False).reset_index(drop=True)
    return start_act

def process_details(df, case_id, timestamp, activities):
    # Get the dataframe
    df_1 = df.copy()
    df_1 = df_1[[case_id, timestamp, activities]]
    df_1 = df_1.merge(df_1.shift(-1), left_index=True, right_index=True, suffixes=('', '_2'))
    df_1 = df_1[df_1[case_id] == df_1[case_id+'_2']]
    df_1['Connection'] = df_1[activities] + " --> " + df_1[activities+'_2']
    return df_1

def graph_group(df,case_id, activities):
    df = df[[case_id, activities, activities+'_2']]
    df = df.groupby([activities,activities+'_2'], sort=False).size()
    df = df.to_frame(name='Count').reset_index()
    return df

#Process details timing
def process_details_timing(df, case_id, timestamp, activities):
    # Get the dataframe
    df_1 = df.copy()
    df_1 = df_1[[case_id, timestamp, activities]]
    df_1 = df_1.merge(df_1.shift(-1), left_index=True, right_index=True, suffixes=('', '_2'))
    df_1 = df_1[df_1[case_id] == df_1[case_id+'_2']]
    return df_1

def graph_group_timing(df,case_id, timestamp,activities):
    df['Duration'] = (df[timestamp+'_2'] - df[timestamp]).dt.days
    df = df[[case_id, activities, activities+'_2','Duration']]
    df = df.groupby([activities,activities+'_2']).agg({'Duration': ['median'], activities:['count']}).reset_index()
    df.columns = [activities,activities+'_2', 'Duration', 'Count']
    df = df.sort_values(by=['Count'], ascending=False)
    df['Duration'] = df['Duration'].astype('int')
    return df

def graph_count(df, activities):
    graph_count = df.copy()
    graph_count = graph_count[activities].value_counts().to_frame().reset_index().rename(columns={'index':activities, activities:'Count'})
    return graph_count

def case_duration(df, case_id, dates):
    case_dur = df.copy()
    case_dur['Count'] = case_dur.groupby(case_id).cumcount()+1
    case_dur = case_dur.pivot(index=case_id, columns='Count', values=dates)
    case_dur_col = case_dur.columns
    case_dur['Max'] = case_dur.apply(max, axis=1)
    case_dur['Case_Duration_days'] = (case_dur['Max'] - case_dur[1]).dt.days
    case_dur = case_dur.drop(case_dur_col, axis=1)
    case_dur.reset_index(inplace=True)    
    return case_dur

def var_table_process_analysis(df,column_name,unique_col):
    var_table = df.groupby([column_name])[unique_col].nunique().reset_index()
    var_table = var_table.sort_values(by=unique_col, ascending=False)
    var_table['Percent'] = round((var_table[unique_col]/var_table[unique_col].sum())*100,2)
    var_table = var_table[[column_name,'Percent',unique_col]]
    return var_table

def activity_list_dates(df, case_id, timestamp, event_id = 'Event_ID'):
    # Get the last and first activity for each case
    activities_list = df.copy()
    # activities_list['Count'] = activities_list.groupby(case_id).cumcount()+1
    activities_list = activities_list.pivot(index=case_id, columns=event_id, values=timestamp)

    activities_list['End_Date'] = activities_list.apply(last_activity, axis=1)
    activities_list['Start_Date'] = activities_list[1]
    return activities_list

def case_duration_df(filtered_df, case_id_column, timestamp_column, event_id = 'Event_ID'):
    start_end_dates = activity_list_dates(filtered_df, case_id_column, timestamp_column, event_id = 'Event_ID')
    start_end_dates = start_end_dates.reset_index()
    start_end_dates['Duration'] = (start_end_dates['End_Date'] - start_end_dates['Start_Date']).dt.days
    start_end_dates = start_end_dates[[case_id_column, 'Start_Date','End_Date','Duration']]
    start_end_dates = start_end_dates.sort_values(by=['Duration'], ascending=False).reset_index(drop=True)
    return start_end_dates

def initial_dataset_csv(df, case_column, activity_column, timestamp_column):
    df[timestamp_column] = pd.to_datetime(df[timestamp_column])
    df['Year'] = df[timestamp_column].dt.year
    df['Month_Number'] = df[timestamp_column].dt.month
    df['Month_Name'] = df[timestamp_column].dt.strftime('%B')
    df['Day'] = df[timestamp_column].dt.day
    df['Month_Name'] = pd.Categorical(df['Month_Name'], categories=months, ordered=True)
    df = df.sort_values(by=[case_column,timestamp_column],ascending=True).reset_index(drop=True)
    df['Event_ID'] = df.groupby(case_column).cumcount()+1
    variants = df.pivot(index=case_column, columns='Event_ID', values=activity_column)
    variants = get_first_last_activities(variants)
    df = pd.merge(df, variants, right_on=case_column, left_on=case_column)
    return df

def initial_dataset_filtered_df(df, case_column, activity_column, timestamp_column):
    df['Activity_Duration'] = df.groupby([case_column])[timestamp_column].diff().dt.days # Duration in days
    df['Activity_Duration'] = df['Activity_Duration'].fillna(0)
    df.drop(['First_Activity','Last_Activity'], axis=1, inplace=True)
    df_2 = variant_analysis(df,case_column, activity_column, timestamp_column)
    first_last = get_first_last_activities(df_2)
    variant_trace = df_2.copy()
    variant_trace.drop(['First_Activity','Last_Activity'], axis=1, inplace=True)
    variant_trace = activities_trace_only(variant_trace)
    variant_trace = variant_trace[['Trace']]
    variant_trace = variant_trace.reset_index()
    variants_sum = activities_trace(df, case_column, activity_column,timestamp_column)
    variants_sum = pd.merge(variants_sum, variant_trace, right_on='Trace', left_on='Trace')
    variants_sum = pd.merge(variants_sum, first_last, right_index=True, left_on=case_column)
    df = pd.merge(df, variants_sum, right_on=case_column, left_on=case_column)
    return df

def activity_gant_chart(df,case_id,timestamp,activity):
    df_1 = df.copy()
    df_1 = df_1[[case_id, timestamp, activity]]
    df_1['Start'] = df_1[timestamp].shift(1)
    df_1.rename(columns={timestamp: 'End'}, inplace=True)
    df_1 = df_1[[case_id, activity, 'Start', 'End']]
    return df_1

def change_label_style(font_size=30,line_height=15):
    st.markdown("""
    <style>
    [data-testid="stSidebar"][aria-expanded="true"]{
           min-width: 450px;
           max-width: 450px;
       }
    </style>
    """, unsafe_allow_html=True)