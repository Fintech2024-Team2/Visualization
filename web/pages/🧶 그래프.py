import streamlit as st
import pandas as pd
import networkx as nx
from streamlit_agraph import agraph, Node, Edge, Config
from utils.graph_utils import create_graph

# 데이터 로드
df = pd.read_csv('finaldata.csv')
df['timestamp'] = pd.to_datetime(df['timestamp'])

# 8월 7일 이후의 타임스탬프 필터링
start_date = pd.to_datetime("2023-08-08")
filtered_df = df[df['timestamp'] > start_date]

def create_agraph(G, pos):
    nodes = []
    edges = []

    for node in G.nodes(data=True):
        node_name = node[0][1:]  # 첫 글자를 제외한 이름으로 설정
        nodes.append(Node(id=node[0], label=node_name, size=10, color="lightblue"))

    for edge in G.edges(data=True):
        edges.append(Edge(source=edge[0], target=edge[1], type="CURVED"))

    config = Config(
        width=1000,
        height=800,
        directed=False,
        nodeHighlightBehavior=True,
        highlightColor="#F7A7A6",  # 강조할 때 노드의 색상
        collapsible=True,
        node={'labelProperty': 'label'},
        link={'labelProperty': 'label', 'renderLabel': True}
    )

    return nodes, edges, config

def show():
    st.title("9기의 워크샵 인물 관계 그래프 시각화")

    time_point = st.select_slider(
        '시간 선택',
        options=filtered_df['timestamp'].unique(),
        value=filtered_df['timestamp'].min()
    )

    G, pos, sub_df = create_graph(time_point, df)
    nodes, edges, config = create_agraph(G, pos)

    agraph(nodes=nodes, edges=edges, config=config)

if __name__ == "__main__":
    show()
