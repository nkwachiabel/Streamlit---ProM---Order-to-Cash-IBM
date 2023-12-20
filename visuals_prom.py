import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import graphviz

def plot_metric(label, value, prefix="", suffix="", show_graph=False, color_graph=""):
    fig = go.Figure()

    fig.add_trace(
        go.Indicator(
            value=value,
            gauge={"axis":{"visible":False}},
            number={
                "prefix":prefix,
                "suffix":suffix,
                "font.size":28,
                "valueformat": ",.0f",
                "font.color":"rgba(205,33,42,1)"
            },
            title={
                "text":label,
                "font":{"size":16},
                "font.color": "rgba(0,140,69,1)"
            },
        )
    )

    if show_graph:
        fig.update_layout(
        margin=dict(t=30, b=0),
        showlegend=False,
        # plot_bgcolor="white",
        paper_bgcolor="rgba(240,242,246,1)",
        height=100,
        )

    st.plotly_chart(fig, use_container_width=True)

def horizontal_bar(df, x_col,y_col,label,color_graph=""):
        fig = px.bar(
             df, 
             x=x_col, 
             y=y_col, 
             text=x_col, 
             orientation='h',
             color_continuous_scale=px.colors.sequential.Viridis
             )
        fig.update_layout(
            xaxis_title = x_col,
            yaxis_title = y_col,
            yaxis={'categoryorder':'total ascending'},
            title = {
                "text":label,
                "font":{"size":15},
            },
            margin=dict(l=20, r=20, t=50, b=0),  # Adjust margins (left, right, top, bottom)
            xaxis=dict(range=[0, max(df[x_col]) * 1.2]),
            # title_x=0.1,
            plot_bgcolor="rgba(240,242,246,1)",
            paper_bgcolor="rgba(240,242,246,1)",
            height=400
        )
        fig.update_traces(
             texttemplate='%{text:.2f}%',
             textposition='outside',
             marker_color='rgba(0,140,69,1)',
             textfont=dict(
                  size=14,
                  color="rgba(205,33,42,1)"
             )
        )
        st.plotly_chart(fig, use_container_width=True)

def vertical_bar(df, x_col,y_col,label,color_graph=""):
        fig = px.bar(
             df, 
             x=x_col, 
             y=y_col, 
             text=y_col, 
             color_continuous_scale=px.colors.sequential.Viridis
             )
        fig.update_layout(
            xaxis_title = x_col,
            yaxis_title = y_col,
            title = {
                "text":label,
                "font":{"size":15}
            },
            margin=dict(l=20, r=20, t=50, b=0),  # Adjust margins (left, right, top, bottom)
            yaxis=dict(range=[0, max(df[y_col]) * 1.2]),
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            height=400,
        )
        fig.update_traces(
             textposition='outside',
             marker_color='rgba(0,140,69,1)',
             textfont=dict(
                  size=14,
                  color="rgba(205,33,42,1)"
             )
        )
        st.plotly_chart(fig, use_container_width=True)

def process_flow(start_activity_df, end_activity_df,process_details_df,graph_count_df,start='Start',end='End',activity='Activity',f_activity='First_Activity',l_activity='Last_Activity', rankdirection='TB'):
    g = graphviz.Digraph(engine='dot') # format='png'
    g.attr('node', shape='rectangle', height='0',width='0', fontname="Segoe UI Semibold", fontcolor="#023047", fontsize='10')
    g.attr('edge', arrowhead='vee', arrowtail='inv', fontname="Segoe UI Semibold", fontcolor="#023047",fontsize='10')
    g.attr(rankdir=rankdirection, splines='true')

    max_node = 3
    max_case_id = process_details_df['Count'].max()

    for index, row in start_activity_df.iterrows():
        g.node(row[start], _attributes={'color':'green', 'fontcolor':'green','shape':'circle','style':'filled','fontsize':'0'}, rank='source')#label="  S  ",
        g.node(row[f_activity],label=row[f_activity] + '\n '+ str(start_activity_df[start_activity_df[f_activity] == row[f_activity]]['Count'].sum()))

    for index, row in start_activity_df.iterrows():
        starrt, firstact, count = [str(i) for i in row]
        g.edge(str(row[start]), str(row[f_activity]), label="  " + count)

    for index, row in process_details_df.iterrows():
        g.node(row[activity],label=row[activity] + '\n '+ str(graph_count_df[graph_count_df[activity] == row[activity]]['Count'].sum()))
        g.node(row[activity+'_2'],label=row[activity+'_2'] + '\n '+ str(graph_count_df[graph_count_df[activity] == row[activity+'_2']]['Count'].sum()))

    for index, row in process_details_df.iterrows():
        startevent, endevent, duration, count = [str(i) for i in row]
        g.edge(str(row[activity]), str(row[activity+'_2']), label= "  " +  count + " case(s)", penwidth=str(int(count)/max_case_id*max_node+1)) #+'\n '+ "  " + duration + " day(s)"

    for index, row in end_activity_df.iterrows():
        g.node(row[l_activity],label=row[l_activity] + '\n '+ str(graph_count_df[graph_count_df[activity] == row[l_activity]]['Count'].sum()))
        g.node(row[end], _attributes={'color':'red', 'fontcolor':'red','shape':'doublecircle','style':'filled','fontsize':'0'}, rank='sink')#label="  S  " ,

    for index, row in end_activity_df.iterrows():
        lastact, endact, count = [str(i) for i in row]
        g.edge(str(row[l_activity]), str(row[end]), label= "  " + count)

    st.graphviz_chart(g, use_container_width=True)

def process_flow_timing(start_activity_df, end_activity_df,process_details_df,graph_count_df,start='Start',end='End',activity='Activity',f_activity='First_Activity',l_activity='Last_Activity', rankdirection='TB'):
    g = graphviz.Digraph() # format='png'
    g.attr('node', shape='rectangle', height='0',width='0', nodesep='1.5',  fontname="Segoe UI Semibold", fontcolor="#023047", fontsize='10')
    g.attr('edge', arrowhead='vee', arrowtail='inv', fontname="Segoe UI Semibold", fontcolor="#023047",fontsize='10')
    g.attr(rankdir=rankdirection, splines='true')

    max_node = 3
    max_case_id = process_details_df['Duration'].max()

    for index, row in start_activity_df.iterrows():
        g.node(row[start], _attributes={'color':'green', 'fontcolor':'green','shape':'circle','style':'filled','fontsize':'0'})#label="  S  ",
        g.node(row[f_activity],label=row[f_activity] + '\n '+ str(start_activity_df[start_activity_df[f_activity] == row[f_activity]]['Count'].sum()))

    for index, row in start_activity_df.iterrows():
        starrt, firstact, count = [str(i) for i in row]
        g.edge(str(row[start]), str(row[f_activity]), label="  " + count)

    for index, row in process_details_df.iterrows():
        g.node(row[activity],label=row[activity] + '\n '+ str(graph_count_df[graph_count_df[activity] == row[activity]]['Count'].sum()))
        g.node(row[activity+'_2'],label=row[activity+'_2'] + '\n '+ str(graph_count_df[graph_count_df[activity] == row[activity+'_2']]['Count'].sum()))

    for index, row in process_details_df.iterrows():
        startevent, endevent, duration, count = [str(i) for i in row]
        g.edge(str(row[activity]), str(row[activity+'_2']), label= "  " +  count + " case(s)" +'\n '+ "  " + duration + " day(s)", penwidth=str(int(duration)/max_case_id*max_node+1))

    for index, row in end_activity_df.iterrows():
        g.node(row[l_activity],label=row[l_activity] + '\n '+ str(graph_count_df[graph_count_df[activity] == row[l_activity]]['Count'].sum()))
        g.node(row[end], _attributes={'color':'red', 'fontcolor':'red','shape':'doublecircle','style':'filled','fontsize':'0'})#label="  S  " ,

    for index, row in end_activity_df.iterrows():
        lastact, endact, count = [str(i) for i in row]
        g.edge(str(row[l_activity]), str(row[end]), label= "  " + count)

    st.graphviz_chart(g, use_container_width=True)

def process_flow_duration(start_activity_df, end_activity_df,process_details_df,graph_count_df,start='Start',end='End',activity='Activity',f_activity='First_Activity',l_activity='Last_Activity', rankdirection='TB'):
    g = graphviz.Digraph() # format='png'
    g.attr('node', shape='rectangle', height='0',width='0', fontname="Segoe UI Semibold", fontcolor="#023047", fontsize='10')
    g.attr('edge', arrowhead='vee', arrowtail='inv', fontname="Segoe UI Semibold", fontcolor="#023047",fontsize='10')
    g.attr(rankdir=rankdirection, splines='true')

    max_node = 3
    max_case_id = process_details_df['Duration'].max()

    for index, row in start_activity_df.iterrows():
        g.node(row[start], _attributes={'color':'green', 'fontcolor':'green','shape':'circle','style':'filled','fontsize':'0'})#label="  S  ",
        g.node(row[f_activity],label=row[f_activity] + '\n '+ str(start_activity_df[start_activity_df[f_activity] == row[f_activity]]['Count'].sum()))

    for index, row in start_activity_df.iterrows():
        starrt, firstact, count = [str(i) for i in row]
        g.edge(str(row[start]), str(row[f_activity]), label="  " + count)

    for index, row in process_details_df.iterrows():
        g.node(row[activity],label=row[activity] + '\n '+ str(graph_count_df[graph_count_df[activity] == row[activity]]['Count'].sum()))
        g.node(row[activity+'_2'],label=row[activity+'_2'] + '\n '+ str(graph_count_df[graph_count_df[activity] == row[activity+'_2']]['Count'].sum()))

    for index, row in process_details_df.iterrows():
        startevent, endevent, duration, count = [str(i) for i in row]
        g.edge(str(row[activity]), str(row[activity+'_2']), label=  "  " + duration + " day(s)", penwidth=str(int(duration)/max_case_id*max_node+1))

    for index, row in end_activity_df.iterrows():
        g.node(row[l_activity],label=row[l_activity] + '\n '+ str(graph_count_df[graph_count_df[activity] == row[l_activity]]['Count'].sum()))
        g.node(row[end], _attributes={'color':'red', 'fontcolor':'red','shape':'doublecircle','style':'filled','fontsize':'0'})#label="  S  " ,

    for index, row in end_activity_df.iterrows():
        lastact, endact, count = [str(i) for i in row]
        g.edge(str(row[l_activity]), str(row[end]), label= "  " + count)

    st.graphviz_chart(g, use_container_width=True)

def vertical_bar_case_duration(df, x_col,y_col,label,medianduration, color_graph="", vline_text=''):
        fig = px.bar(
             df, 
             x=x_col, 
             y=y_col, 
             text=y_col, 
            #  orientation='h',
             color_continuous_scale=px.colors.sequential.Viridis
             )
        fig.update_layout(
            xaxis_title = x_col,
            yaxis_title = y_col,
            # yaxis={'categoryorder':'total ascending'},
            title = {
                "text":label,
                "font":{"size":15,
                        "color":"rgba(0,140,69,1)"},
                
            },
            margin=dict(l=0, r=20, t=10, b=0),  # Adjust margins (left, right, top, bottom)
            # xaxis=dict(range=[min(df[x_col]), max(df[x_col])]),
            # title_x=0.1,
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            height=400,
        )
        fig.update_traces(
             textposition='outside',
             marker_color='rgba(0,140,69,1)',
             textfont=dict(
                  size=14,
                  color="rgba(205,33,42,1)"
             )
        )
        # fig.update_yaxes(
        #     title_font_color='black',
        #     tickfont = dict(color='black')
        # )
        # fig.update_xaxes(
        #     title_font_color='black',
        #     tickfont = dict(color='black')
        # )
        fig.add_vline(
            x=medianduration,
            line_width=2,
            line_dash="dash",
            line_color="red",
            annotation=dict(
                text= vline_text +": "+str(medianduration),
                # size=14
                # color='black'
                )
        )
        st.plotly_chart(fig, use_container_width=True)

def user_activity_graph(df):
    ZA = graphviz.Digraph(format='png')
    ZA.attr(rankdir='TB')
    ZA.attr('node', shape='rectangle', height='0.3',width='0.3', fontname="Sans Bold")
    ZA.attr('edge', arrowhead='vee', arrowtail='inv',fontname="Sans Bold Italic")

    max_node = 3
    max_case_id = df['Weight'].max()
    nodelist2 = []
    for idx, row in df.iterrows():
        node11, node22, weight2 = [str(i) for i in row]
        
        if node11 not in nodelist2:
            ZA.node(node11)
            nodelist2.append(node22)
        if node22 not in nodelist2:
            ZA.node(node22)
            nodelist2.append(node22)
            
        ZA.edge(node11, node22)

    st.graphviz_chart(ZA, use_container_width=True)

def workgroup_activity_graph(df):
    ZA = graphviz.Digraph(format='png')
    ZA.attr(rankdir='TB')
    ZA.attr('node', shape='rectangle', height='0.3',width='0.3', fontname="Sans Bold")
    ZA.attr('edge', arrowhead='vee', arrowtail='inv',fontname="Sans Bold Italic")

    max_node = 3
    max_case_id = df['Weight'].max()
    nodelist2 = []
    for idx, row in df.iterrows():
        node11, node22, weight2 = [str(i) for i in row]
        
        if node11 not in nodelist2:
            ZA.node(node11)
            nodelist2.append(node22)
        if node22 not in nodelist2:
            ZA.node(node22)
            nodelist2.append(node22)
            
        ZA.edge(node11, node22, label=str(weight2))

    st.graphviz_chart(ZA, use_container_width=True)