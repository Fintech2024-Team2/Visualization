import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import os

def show():
    # CSV 파일을 읽어오는 부분
    df = pd.read_csv("labeled_data.csv")

    # 노드 리스트 생성
    nodes = df['class'].unique()
    node_indices = {node: i for i, node in enumerate(nodes)}  # 노드 이름을 인덱스로 매핑

    # Streamlit 사이드바에서 인물 선택 UI 추가
    selected_person = st.sidebar.selectbox("인물을 선택하세요", nodes)

    # 시간을 기준으로 그룹핑하여 데이터 준비
    grouped = df.groupby('timestamp')

    # 애니메이션을 위한 프레임 생성
    frames = []
    for time, group in grouped:
        sources = []
        targets = []
        values = []

        for person in group['class'].unique():
            if person != selected_person:
                count = group[(group['class'] == selected_person) & (group['filename'].isin(group[group['class'] == person]['filename']))].shape[0]
                if count > 0:
                    sources.append(node_indices[selected_person])  # 선택된 인물의 인덱스
                    targets.append(node_indices[person])  # 관련된 인물의 인덱스
                    values.append(count)  # 만난 횟수

        frame = go.Frame(data=[go.Sankey(
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
        )], name=str(time))
        frames.append(frame)

    # Sankey 다이어그램 초기 설정
    fig = go.Figure(data=[go.Sankey(
        node=dict(
            pad=15,
            thickness=20,
            line=dict(color="black", width=0.5),
            label=nodes,
            color="blue"
        ),
        link=dict(
            source=[],
            target=[],
            value=[],
            color='rgba(150, 200, 250, 0.4)'
        )
    )])

    fig.update_layout(
        title_text=f"{selected_person}의 관계 다이어그램",
        font_size=10,
        updatemenus=[{
            "buttons": [
                {
                    "args": [None, {"frame": {"duration": 500, "redraw": True}, "fromcurrent": True}],
                    "label": "Play",
                    "method": "animate"
                },
                {
                    "args": [[None], {"frame": {"duration": 0, "redraw": True}, "mode": "immediate", "transition": {"duration": 0}}],
                    "label": "Pause",
                    "method": "animate"
                }
            ],
            "direction": "left",
            "pad": {"r": 10, "t": 87},
            "showactive": False,
            "type": "buttons",
            "x": 0.1,
            "xanchor": "right",
            "y": 0,
            "yanchor": "top"
        }],
        sliders=[{
            "active": 0,
            "yanchor": "top",
            "xanchor": "left",
            "currentvalue": {
                "font": {"size": 20},
                "prefix": "시간:",
                "visible": True,
                "xanchor": "right"
            },
            "transition": {"duration": 300, "easing": "cubic-in-out"},
            "pad": {"b": 10, "t": 50},
            "len": 0.9,
            "x": 0.1,
            "y": 0,
            "steps": [{"args": [[frame.name], {"frame": {"duration": 300, "redraw": True}, "mode": "immediate", "transition": {"duration": 300}}], "label": frame.name, "method": "animate"} for frame in frames]
        }]
    )

    fig.frames = frames

    # Streamlit에 Sankey 다이어그램 표시
    st.plotly_chart(fig)
