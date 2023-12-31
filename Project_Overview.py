import streamlit as st

st.set_page_config(page_title="Process Mining Order-to-Cash", page_icon=":twisted_rightwards_arrows:", layout="wide")

st.title("Process Mining: Analysing the Order-to-Cash process of a cable company")
st.divider()

with st.sidebar:
    st.write('Made with :green_heart: by [Nkwachi Abel](https://www.linkedin.com/in/nkwachi-abel)')

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
        2. Data quality check and transformation  
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
    
    This information forms the foundation for a comprehensive process mining analysis, enabling a deep dive into the order-to-cash process.        
    '''
    st.markdown(attributes_list1)

    col_eventlog1, col_eventlog2 = st.columns(2)
    with col_eventlog1:
        st.markdown('<span style="font-size: 20px; font-weight: bold;">Dataset Credits</span>', unsafe_allow_html=True)
        credits_line = '''
            **Publisher:** IBM  
            **Organisation:** IBM  
            **References**: [IBM Process Mining GitHub repository](https://github.com/IBM/processmining)
        '''
        st.markdown(credits_line)

    # with col_eventlog2:
    #     st.markdown('<span style="font-size: 20px; font-weight: bold;">GitHub Repository</span>', unsafe_allow_html=True)
    #     personal_details = '''
    #         **[Github repository for Analysis](https://github.com/nkwachiabel/Process-Mining-Order-to-cash-IBM)**    
    #     '''
    #     st.markdown(personal_details)

with st.container(border=True):
    st.subheader('Data quality check and transformation')
    st.write('The event log was reviewed to ensure the data contained were suitable for process mining anslysis.')
    col_ev_log, col_empty_values = st.columns(2)

    with col_ev_log:
        st.markdown('<span style="font-size: 20px; font-weight: bold;">Event Log Overview</span>', unsafe_allow_html=True)
        st.write('The event log initially contained 15 different start activities and 14 different end activities, indicating a variety of entry and exit points in the process. The data captures all order requests from January 2, 2016, to July 16, 2017, without considering the stages the order requests were in the order to cash process.')

        st.markdown('<span style="font-size: 20px; font-weight: bold;">Filtering for End-to-End Analysis</span>', unsafe_allow_html=True)
        st.write('In order to understand the process completely, it is important to focus on completed orders. To focus on completed order requests, the event log was filtered to include only those orders that started with "Line creation" and ended with either "Goods Issue" or "Schedule Line Rejected". These two activities were selected to gain proper understanding of those cases that were rejected and those that were completed. This would help in understanding the reasons for rejection and also improve understanding of the overall process')

    with col_empty_values:
        st.markdown('<span style="font-size: 20px; font-weight: bold;">Handling of Empty Values</span>', unsafe_allow_html=True)
        st.write('Certain columns in the dataset had empty values. This is attributed to the nature of specific activities that do not require input in those columns. For instance, the "Delivery" and "Delivery_date" column has some empty rows. This was because the activity performed was not related to the delivery of goods. Columns with many empty rows were not utilized in the analysis, suggesting a focus on data completeness and relevance.')

        st.markdown('<span style="font-size: 20px; font-weight: bold;">Limitations Due to Data Source</span>', unsafe_allow_html=True)
        st.write('The event log was obtained online, and no direct contact was made with process owners for further understanding of the process or additional insights into the dataset. The analysis might not highlight manual events or specific nuances of the process due to the lack of direct engagement with process owners.')

with st.container(border=True):
    st.subheader('Process discovery and analysis')
    process_discov = '''
    See the following pages for the findings on process discovery and analysis:  
    1. Process Analysis - Findings on the organisation perspective  
    2. Timing Analysis - Findings on the timing perspective  
    3. Users Analysis - Findings on users involved in the process  
    4. Case Details - A dashboard for users to be able to filter individual orders  
    5. Open Orders - A dashboard to view and monitor open order requests  
    '''
    st.markdown(process_discov, unsafe_allow_html=True)

with st.container(border=True):
    st.subheader('Recommendations')
    recommendations = '''
        **Addressing Bottlenecks:**  
        **Customer Address Updates:** Implement a proactive system to regularly verify and update customer address information. This could involve automated reminders to customers to confirm or update their addresses periodically or when placing an order.  
        **Inventory Planning:** Enhance inventory management systems to accurately forecast demand and ensure timely replenishment. Utilize predictive analytics to identify trends and optimize inventory levels.  

        **Improving System Controls:**  
        **Prevent Incorrect Goods Issuance:** Establish stricter validation checks within the system to ensure goods are not issued under incorrect conditions. This could involve multi-level verification processes and automated alerts for irregularities.  

        **Analyzing Rejection Rates:**  
        **Identify Causes of High Rejection:** Conduct a detailed analysis of orders in categories with high rejection rates to understand underlying causes. This might involve reviewing process steps, quality control measures, and customer feedback.  
        **Implement Corrective Actions:** Based on the analysis, take corrective measures such as process re-engineering, quality improvement initiatives, product modifications, or customer communication enhancements.  
        **Root Cause Analysis:** Delve into the specific reasons for order rejections, using data analytics and feedback from relevant departments.  

        **Optimizing User Role Distribution and Workload:**  
        **Role Analysis and Distribution:** Conduct a thorough review of user roles and responsibilities to ensure a balanced distribution of workload. Consider reallocating tasks or hiring additional staff where necessary.  
        **Efficiency Training:** Provide training and resources to enhance the efficiency of existing staff, especially in roles with a high volume of activities.  

        **Investigating Automatic Activities:**  
        **Impact Assessment:** Study the impact of automatic activities on the process flow, particularly those related to delivery and goods issuance. Assess whether these activities align with the intended process outcomes.  
        **Process Calibration:** Adjust the settings of automatic activities to better align with process requirements and reduce instances of error or inefficiency.        

        **Open orders**  
        To manage these open orders effectively, the implementation of Microsoft Power Automate for setting up periodic reminders is recommended. These reminders could be directed to the last user who performed an activity on the order or to the head of procurement, ensuring that the status of each order is regularly reviewed and followed up on. This automation could be scheduled on a fortnightly basis to maintain consistent oversight of open orders and to expedite their resolution.  

        **Continuous Monitoring and Benchmarking:**  
        **Regular Process Review:** Establish a routine for monitoring process performance, focusing on the timeliness and efficiency of order fulfillment.
        **Benchmarking Against Standards:** Compare your process performance against industry standards or benchmarks to identify gaps and opportunities for improvement.  
        **Iterative Improvement:** Utilize findings from regular monitoring and benchmarking to implement continuous improvement initiatives, aiming for higher efficiency and customer satisfaction.  

    '''
    st.markdown(recommendations, unsafe_allow_html=True)

with st.container(border=True):
    st.markdown('<span style="font-size: 20px; font-weight: bold;">Contributions</span>', unsafe_allow_html=True)
    contribuions = '''  
            Contributions to this projects are welcome! If you encounter any issues or have suggestions for improvement, please get in touch with me using the contact form.  
        '''
    st.markdown(contribuions)
    
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
