import streamlit as st
from streamlit_agraph import Config, Node, Edge, agraph
import pandas as pd

# 데이터 로드
df = pd.read_csv('/Users/chaewon/Desktop/manito.csv')

# Streamlit App
st.title("마니또 관계 시각화 with AGraph")

# AGraph Nodes and Edges
nodes = {}
edges = []

for _, row in df.iterrows():
    # 노드 이름을 두 글자로 줄이기 (첫 두 글자를 사용)
    from_name = row['from'][1:]
    to_name = row['to'][1:]

    # 노드 추가 (중복 방지)
    if from_name not in nodes:
        nodes[from_name] = Node(id=from_name, label=from_name, size=40, shape="circle", font={"size": 20})
    if to_name not in nodes:
        nodes[to_name] = Node(id=to_name, label=to_name, size=40, shape="circle", font={"size": 20})
    
    # 엣지 추가 (클릭 시 표시될 툴팁 내용 설정)
    description_text = f"{row['from']} -> {row['to']} : {row['description']}"
    edges.append(Edge(source=from_name, target=to_name, label="", title=description_text, font={"size": 12}))

# AGraph 구성
config = Config(
    width=1000, 
    height=800, 
    directed=True,
    nodeHighlightBehavior=True, 
    highlightColor="#F7A7A6", 
    collapsible=False, 
    node={'labelProperty': 'label'},
    link={'labelProperty': 'title', 'renderLabel': False},
    **{
        "linkTitleBehavior": "onClick",  # 엣지를 클릭할 때만 툴팁이 나타나도록 설정
    },
    staticGraphWithDragAndDrop=True,  # 레이아웃 고정
    staticGraph=True  # 그래프를 움직이지 않도록 고정
)

# 그래프 그리기
agraph(nodes=list(nodes.values()), edges=edges, config=config)
