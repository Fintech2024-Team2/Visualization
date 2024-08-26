import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import networkx as nx

def show():
    # CSV 파일을 읽어오는 부분
    df = pd.read_csv("labeled_data.csv")

    # 노드 리스트 생성
    nodes = df['class'].unique()

    # Streamlit 사이드바에서 인물 선택 UI 추가
    selected_person = st.sidebar.selectbox("인물을 선택하세요", nodes)

    # 시간을 기준으로 그룹핑하여 데이터 준비
    grouped = df.groupby('timestamp')

    # 네트워크 그래프를 위한 네트워크 생성
    G = nx.DiGraph()

    # 애니메이션을 위한 프레임 생성
    frames = []
    accumulated_edges = []

    for time, group in grouped:
        for person in group['class'].unique():
            if person != selected_person:
                common_files = group[(group['class'] == selected_person) & (group['filename'].isin(group[group['class'] == person]['filename']))]
                count = len(common_files)
                if count > 0:
                    G.add_edge(selected_person, person, weight=count)

        # 현재까지의 엣지 데이터를 누적
        accumulated_edges.append((time, G.copy()))

    # 노드 레이아웃 고정 (노드 추가 후 위치 지정)
    pos = nx.spring_layout(G, seed=42)  # 노드 레이아웃 고정

    # Plotly를 이용한 네트워크 그래프 생성
    for time, G_snapshot in accumulated_edges:
        edge_x = []
        edge_y = []
        for edge in G_snapshot.edges():
            if edge[0] in pos and edge[1] in pos:  # 노드가 pos에 있는지 확인
                x0, y0 = pos[edge[0]]
                x1, y1 = pos[edge[1]]
                edge_x.append(x0)
                edge_x.append(x1)
                edge_x.append(None)
                edge_y.append(y0)
                edge_y.append(y1)
                edge_y.append(None)

        edge_trace = go.Scatter(
            x=edge_x, y=edge_y,
            line=dict(width=1, color='#888'),
            hoverinfo='none',
            mode='lines'
        )

        node_x = []
        node_y = []
        for node in G_snapshot.nodes():
            if node in pos:  # 노드가 pos에 있는지 확인
                x, y = pos[node]
                node_x.append(x)
                node_y.append(y)

        node_trace = go.Scatter(
            x=node_x, y=node_y,
            text=list(G_snapshot.nodes),
            mode='markers+text',
            textposition="top center",
            hoverinfo='text',
            marker=dict(
                size=20,
                color='lightblue',
                line_width=2
            )
        )

        frame = go.Frame(data=[edge_trace, node_trace], name=str(time))
        frames.append(frame)

    # 초기 네트워크 그래프 설정
    fig = go.Figure(
        data=[go.Scatter(x=[], y=[])],
        layout=go.Layout(
            title=f"{selected_person}의 네트워크 그래프",
            title_x=0.5,
            showlegend=False,
            hovermode='closest',
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
        ),
        frames=frames
    )

    # Streamlit에 네트워크 그래프 표시
    st.plotly_chart(fig)

# 이 함수는 페이지를 실행할 때 호출됩니다.
if __name__ == "__main__":
    show()
