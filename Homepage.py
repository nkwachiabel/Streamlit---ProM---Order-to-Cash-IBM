import streamlit as st
import pandas as pd
from prom_functions import *
from visuals_prom import *
from dataset_details import *

st.set_page_config(page_title="Process Mining O2C", page_icon=":bar_chart:", layout="wide")

st.title("Process Mining: Analysing the helpdesk process log of an Italian company")
st.divider()

with st.container(border=True):
    st.subheader('Project Overview')
    st.write('This project explores the use of data analytics techniques and process mining methodology to analyse the ticketing management process of the Help desk of an Italian software company. The dataset contains 21,348 events, 4580 cases and 14 activities spaning 4 years from 13th January 2010 to 3rd January 2014. The dataset was gotten from [here](https://doi.org/10.4121/uuid:0c60edf1-6f83-4e75-9367-4c63b3e9d5bb).')
    col_eventlog1, col_eventlog2 = st.columns(2)
    with col_eventlog1:
        st.write('The event log contains the following list of attributes with their meaning:')
        attributes_list1 = '''
        **Case ID:** the case identifier  
        **Activity**: the activity name  
        **Resource**: the resource who performed the action  
        **Complete Timestamp:** the timestamp of the event    
        **Variant:** case variant  
        **Variant index:** case variant in integer format  
        **seriousness:** a seriousness level for the ticket  
        **customer:** name of the customer  
        **product:** name of the product  
        **responsible_section:** name of the responsible section  
        **seriousness_2:** a sub-seriousness level  
        **service_level:** level of the service  
        **service_type:** type of the service  
        **support_section:** name of the support section  
        **workgroup:** name of the workgroup
        '''
        st.markdown(attributes_list1)

    with col_eventlog2:
        st.markdown('<span style="font-size: 20px; font-weight: bold;">Dataset Credits</span>', unsafe_allow_html=True)
        credits_line = '''
            **Publisher:** University of Padova  
            **Organisation:** University of Padova, Department of Mathematics  
            **Reerences**: https://doi.org/10.1007/s00607-015-0441-1
        '''
        st.markdown(credits_line)

with st.container(border=True):
    colGoals, colMethodology, colTechUsed = st.columns(3)
    with colGoals:
        st.markdown('<span style="font-size: 20px; font-weight: bold;">Project Goal</span>', unsafe_allow_html=True)
        project_goals = '''
        The goal of this project is to utilize process mining techniques to:  
        1. Discover the actual helpdesk process process.  
        2. Identify inefficiencies and bottlenecks in the process.  
        3. Generate insights to improve process efficiency.  
        '''
        st.markdown(project_goals)
    with colMethodology:
        st.markdown('<span style="font-size: 20px; font-weight: bold;">Methodology</span>', unsafe_allow_html=True)
        project_methodology = ''' 
        1. Data collection  
        2. Data transformation  
        3. Process analysis  
        4. Timing analysis  
        5. Users analysis  
        '''
        st.markdown(project_methodology)
    with colTechUsed:
        st.markdown('<span style="font-size: 20px; font-weight: bold;">Technologies used</span>', unsafe_allow_html=True)
        project_techused = ''' 
        1. Python  
        2. Pandas library  
        3. Graphviz library  
        4. Streamlit  
        5. Plotly  
        '''
        st.markdown(project_techused)

with st.expander(":point_right: Data View"):
    st.dataframe(df)

