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
    st.write('This project explores the use of data analytics and process mining techniques to analyse the order to cash process of a company.')

    colGoals, colMethodology, colTechUsed = st.columns([3,1.5,1.5])
    with colGoals:
        st.markdown('<span style="font-size: 20px; font-weight: bold;">Project Goal</span>', unsafe_allow_html=True)
        project_goals = '''
        The goal of this project is to utilize data analytics and process mining techniques to:  
        1. Discover the actual order-to-cash management process.  
        2. Identify inefficiencies and bottlenecks in the process.  
        3. Generate insights to improve process efficiency.  
        4. Develop a dashboard to monitor uncompleted cases.  
        '''
        st.markdown(project_goals)
    with colMethodology:
        st.markdown('<span style="font-size: 20px; font-weight: bold;">Methodology</span>', unsafe_allow_html=True)
        project_methodology = ''' 
        1. Data collection  
        2. Data transformation  
        3. Process discovery and analysis  
        4. Recommendations  
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

with st.container(border=True):
    st.subheader('Data collection')
    
    attributes_list1 = '''
    The dataset, referred to as 'eventlog,' was obtained from IBM during coursework for the IBM Process Mining Analyst and IBM Process Mining Data Analyst certifications. The initial event log consists of 45,825 order requests, encompassing 19 distinct activities and 251,478 events, recorded between January 2nd, 2016, and December 7th, 2017. The 'Key' column serves as the unique case identifier, the 'Activity' column details the events, and the 'Date' column records the timestamp for each event. Additionally, the dataset comprises various attributes that enrich the analysis:

    **User:** Identifies the individual who performed each event.  
    **Role:** Specifies the role of the user within the organization.  
    **User_Type:** Distinguishes whether the event was performed by a Human or a Robot.  
    **Product_hierarchy:** Classifies the product involved in the order request.  
    **NetValue:** Represents the financial value of the order request.  
    **Customer:** Names the customer who placed the order.  
    **OrderType:** Indicates the categorization of the order.  
    **Delayed:** Denotes whether the order was delivered on time or experienced delays.  
    
    This information forms the foundation for a comprehensive process mining analysis, enabling a deep dive into the order-to-cash process at IBM.        
    '''
    st.markdown(attributes_list1)

    col_eventlog1, col_eventlog2 = st.columns(2)
    with col_eventlog1:
        st.markdown('<span style="font-size: 20px; font-weight: bold;">Dataset Credits</span>', unsafe_allow_html=True)
        credits_line = '''
            **Publisher:** IBM  
            **Organisation:** University of Padova, Department of Mathematics  
            **Reerences**: [IBM Process Mining GitHub repository](https://github.com/IBM/processmining)
        '''
        st.markdown(credits_line)
        st.markdown('<span style="font-size: 20px; font-weight: bold;">GitHub Repository</span>', unsafe_allow_html=True)
        personal_details = '''
            **[Github repository for Analysis](https://github.com/nkwachiabel/Process-Mining-Order-to-cash-IBM)**  
            **Contribution:** Contributions to this repository are welcome! If you encounter any issues or have suggestions for improvement, please get in touch with me using the contact form below.  
        '''
        st.markdown(personal_details)
    
    with col_eventlog2:
        st.markdown('<span style="font-size: 20px; font-weight: bold;">:mailbox: Get in touch with me!</span>', unsafe_allow_html=True)
        contact_form = """
        <form action="https://formsubmit.co/3b046e55c482e13b27281f351ab6b27e" method="POST">
            <input type="hidden" name="_captcha" value="false">
            <input type="text" name="Name" placeholder="Your name" required>
            <input type="email" name="Email" placeholder="Your email" required>
            <textarea name="message" placeholder="Message"></textarea>
            <button type="submit">Send</button>
        </form>
        """
        st.markdown(contact_form, unsafe_allow_html=True)


with st.container(border=True):
    st.subheader('Data quality check and transformation')



with st.expander(":point_right: Data View"):
    st.dataframe(df)

css = '''
input[type=text], input[type=email], textarea {
  width: 100%; /* Full width */
  padding: 12px; /* Some padding */ 
  border: 1px solid #ccc; /* Gray border */
  border-radius: 4px; /* Rounded borders */
  box-sizing: border-box; /* Make sure that padding and width stays in place */
  margin-top: 6px; /* Add a top margin */
  margin-bottom: 16px; /* Bottom margin */
  resize: vertical /* Allow the user to vertically resize the textarea (not horizontally) */
}

/* Style the submit button with a specific background color etc */
button[type=submit] {
  background-color: #04AA6D;
  color: white;
  padding: 12px 20px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

/* When moving the mouse over the submit button, add a darker green color */
button[type=submit]:hover {
  background-color: #45a049;
}
'''
st.markdown(f'<style>{css}</style>',unsafe_allow_html=True)
