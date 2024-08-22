import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import os

def show():
    # CSV 파일을 읽어오는 부분
    df = pd.read_csv("labeled_data.csv")

    # 노드 리스트 생성
    nodes = df['class'].unique()

    # source, target, value를 저장할 리스트 초기화
    sources = []
    targets = []
    values = []

    # 모든 가능한 조합에 대해 source, target 계산
    for i, person1 in enumerate(nodes):
        for j, person2 in enumerate(nodes):
            if person1 != person2:
                # 두 인물이 함께 등장한 횟수를 계산
                count = df[(df['class'] == person1) & (df['filename'].isin(df[df['class'] == person2]['filename']))].shape[0]
                if count > 0:
                    sources.append(i)  # person1의 인덱스
                    targets.append(j)  # person2의 인덱스
                    values.append(count)  # 만난 횟수

    # Sankey 다이어그램 생성
    fig = go.Figure(data=[go.Sankey(
        node=dict(
            pad=15,
            thickness=20,
            line=dict(color="black", width=0.5),
            label=nodes,
            color="blue"
        ),
        link=dict(
            source=sources,  # source 리스트
            target=targets,  # target 리스트
            value=values,    # value 리스트
            color='rgba(150, 200, 250, 0.4)'
        )
    )])

    fig.update_layout(title_text="인물 간 관계 다이어그램", font_size=10)

    # Streamlit에 Sankey 다이어그램 표시
    st.plotly_chart(fig)

