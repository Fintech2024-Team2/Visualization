import pandas as pd
import streamlit as st
import plotly.graph_objects as go
import networkx as nx
from PIL import Image
import time

# Function to create the full network graph and positions
def create_full_network_graph(df):
    G = nx.DiGraph()
    for idx, row in df.iterrows():
        src = row['from']
        dst = row['to']
        power_category = row['power']
        G.add_edge(src, dst, category=power_category)
    pos = nx.spring_layout(G, seed=42)  # Fix the seed for consistent layout
    return G, pos

# Function to create subgraph based on current index
def create_subgraph(G, df, end_index):
    edges = [(row['from'], row['to']) for idx, row in df.iloc[:end_index+1].iterrows()]
    G_sub = G.edge_subgraph(edges).copy()
    return G_sub

# Function to plot the graph using Plotly
def plot_graph(G, pos):
    # Create edge traces for each category
    edge_traces = []
    category_colors = {
        '음료': 'red',
        '응원': 'blue',
        '물건': 'green',
    }

    for edge in G.edges(data=True):
        src, dst, data = edge
        x0, y0 = pos[src]
        x1, y1 = pos[dst]
        color = category_colors.get(data['category'], 'gray')

        edge_trace = go.Scatter(
            x=[x0, x1],
            y=[y0, y1],
            line=dict(width=2, color=color),
            hoverinfo='text',
            text=f"{src} → {dst} ({data['category']})",
            mode='lines'
        )
        edge_traces.append(edge_trace)

    # Create node trace
    node_x = [pos[node][0] for node in G.nodes()]
    node_y = [pos[node][1] for node in G.nodes()]
    node_text = [node for node in G.nodes()]

    node_trace = go.Scatter(
        x=node_x,
        y=node_y,
        text=node_text,
        mode='markers+text',
        textposition="top center",
        hoverinfo='text',
        marker=dict(
            size=20,
            color='lightskyblue',
            line=dict(width=2, color='DarkSlateGrey')
        )
    )

    # Combine all traces
    fig = go.Figure(data=edge_traces + [node_trace])

    fig.update_layout(
        showlegend=False,
        hovermode='closest',
        title_text="마니또 관계 그래프",
        title_x=0.5,
        margin=dict(l=20, r=20, t=40, b=20),
        height=700,
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )

    return fig

# Streamlit app
def show():
    st.title("마니또 관계 시각화")
    st.write("시간에 따라 변하는 마니또 관계를 확인하세요.")
    
    # Load data
    df = pd.read_csv('/Users/chaewon/Desktop/manito.csv')
    
    # Initialize full graph and positions
    if 'full_G' not in st.session_state or 'pos' not in st.session_state:
        full_G, pos = create_full_network_graph(df)
        st.session_state['full_G'] = full_G
        st.session_state['pos'] = pos
    else:
        full_G = st.session_state['full_G']
        pos = st.session_state['pos']
    
    max_index = len(df) - 1
    current_index = st.slider("순서", 0, max_index + 1, 0, help="슬라이더를 움직여 시간에 따른 변화를 확인하세요.")
    
    # Display images at specific timestamps
    if current_index == 0:
        st.image('/Users/chaewon/Downloads/IMG_2947.JPG', use_column_width=True)
    elif current_index == 10:
        placeholder = st.empty()
        image_path2 = '/Users/chaewon/Downloads/IMG_2948.JPG'  # 두 번째 이미지 경로
        img2 = Image.open(image_path2)
        placeholder.image(img2, use_column_width=True)
        time.sleep(0.5)  # 이미지가 0.5초 동안 표시됨
        placeholder.empty()  # 이미지를 제거
    
    # If current_index is 0, do not show the graph and data
    if current_index > 0:
        # Create subgraph based on current index
        G_sub = create_subgraph(full_G, df, current_index - 1)
        
        # Plot graph
        fig = plot_graph(G_sub, pos)
        st.plotly_chart(fig, use_container_width=True)
        
        # Display data
        st.write("현재까지의 마니또 데이터:")
        st.dataframe(df.iloc[:current_index], height=600)

if __name__ == '__main__':
    show()
