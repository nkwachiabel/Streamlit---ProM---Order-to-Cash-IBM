import streamlit as st
from streamlit_agraph import agraph, Node, Edge, Config
import random
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

def process_flow_agraph(start_activity_df, end_activity_df, process_details_df, graph_count_df, start='Start', end='End', activity='Activity', f_activity='First_Activity', l_activity='Last_Activity'):
    nodes = []
    edges = []
    added_nodes = set()

    max_node = 3
    max_case_id = process_details_df['Duration'].max()

    # Function to safely add nodes (avoid duplicates)
    def add_node(node_id, label, color=None):
        if node_id not in added_nodes:
            nodes.append(Node(id=node_id, label=label, color=color))
            added_nodes.add(node_id)

    # Add start activities
    for index, row in start_activity_df.iterrows():
        node_id = row[f_activity]
        node_label = f"{node_id}\n{start_activity_df[start_activity_df[f_activity] == node_id]['Count'].sum()}"
        add_node(node_id, node_label, color='green')
        edges.append(Edge(source=start, target=node_id, label=f"  {row['Count']}"))

    # Process details
    for index, row in process_details_df.iterrows():
        start_node = row[activity]
        end_node = row[activity+'_2']
        start_label = f"{start_node}\n{graph_count_df[graph_count_df[activity] == start_node]['Count'].sum()}"
        end_label = f"{end_node}\n{graph_count_df[graph_count_df[activity] == end_node]['Count'].sum()}"
        add_node(start_node, start_label)
        add_node(end_node, end_label)
        edges.append(Edge(source=start_node, target=end_node, label=f"  {row['Duration']} day(s)", weight=int(row['Duration'])/max_case_id*max_node+1))

    # Add end activities
    for index, row in end_activity_df.iterrows():
        node_id = row[l_activity]
        node_label = f"{node_id}\n{graph_count_df[graph_count_df[activity] == node_id]['Count'].sum()}"
        add_node(node_id, node_label, color='red')
        edges.append(Edge(source=node_id, target=end, label=f"  {row['Count']}"))

    agraph(nodes=nodes, edges=edges, config={'height': 500, 'width': 700, 'directed': True})

def create_agraph(df):
    max_node = 5
    max_case_id = df['Count'].max()

    nodes = []
    edges = []


    for idx, row in df.iterrows():
        node11, node22, weight2 = [str(i) for i in row]

        if node11 not in nodes:
            nodes.append(Node(id=node11, label=node11))
            # nodes.add(node11)
        if node22 not in nodes:
            nodes.append(Node(id=node22, label=node22))
            # nodes.add(node22)

        edges.append(Edge(source=node11, target=node22, label=weight2, weight=int(weight2)/max_case_id*max_node))

    # Display the graph
    return_value = agraph(nodes=nodes, edges=edges, config={'height': 600, 'width': 800, 'directed': True})
    return return_value

def process_graph_agraph(start_act_df, process_details_df, end_act_df, graph_count_df, activiti_column, rankdir='TB'):
    nodes = []
    edges = []
    node_ids = set()

    for idx, row in start_act_df.iterrows():
        node1, node2, weight1 = row['Start'], row['First_Activity'], row['Count']

        if node1 not in node_ids:
            nodes.append(Node(id=node1,label=node1 + '\n' + str(graph_count_df[graph_count_df[activiti_column]== row['Start']]['Count'].sum()), title=node1, color='green', shape='circle', font = '14px arial green', x=-60, y=-500))#fixed=True, 
            node_ids.add(node1)
        if node2 not in node_ids:
            nodes.append(Node(id=node2,label=node2 + '\n' + str(graph_count_df[graph_count_df[activiti_column]== row['First_Activity']]['Count'].sum()), title=node2, shape='box'))
            node_ids.add(node2)

        edges.append(Edge(source=node1, target=node2, weight=weight1, type="CURE_SMOOTH"))

    for idx, row in process_details_df.iterrows():
        node11, node22, weight11 = row[activiti_column], row[activiti_column+'_2'], row['Count']

        if node11 not in node_ids:
            nodes.append(Node(id=node11,label=node11 + '\n' + str(graph_count_df[graph_count_df[activiti_column]== row[activiti_column]]['Count'].sum()), title=node11, shape='box'))
            node_ids.add(node11)
        if node22 not in node_ids:
            nodes.append(Node(id=node22,label=node22 + '\n' + str(graph_count_df[graph_count_df[activiti_column]== row[activiti_column+'_2']]['Count'].sum()), title=node22, shape='box', shapeProperties={'borderRadius':10}))
            node_ids.add(node22)
        edges.append(Edge(source=node11, target=node22, label=weight11, smooth={'type':'cubicBezier', 'roundness':1}, font = {'size': '14px', 'color':'red', 'face':'arial'})) #type="CURVE_SMOOTH",

    for idx, row in end_act_df.iterrows():
        node111, node222, weight111 = row['Last_Activity'], row['End'], row['Count']

        if node111 not in node_ids:
            nodes.append(Node(id=node111,label=node111 + '\n' + str(graph_count_df[graph_count_df[activiti_column]== row['End']]['Count'].sum()), title=node111, shape='box'))
            node_ids.add(node111)
        if node222 not in node_ids:
            nodes.append(Node(id=node222,label=node222 + '\n' + str(graph_count_df[graph_count_df[activiti_column]== row['Last_Activity']]['Count'].sum()), title=node222, color='red', shape='doublecircle', font = '14px arial red', style='filled'))
            node_ids.add(node222)

        edges.append(Edge(source=node111, target=node222, weight=weight111, type="CURE_SMOOTH"))
    configur=Config(width=1200, height=1000, directed=True, graphviz_config = {"rankdir": rankdir})
    return_value = agraph(nodes=nodes, edges=edges, config=configur)
    return return_value

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