from utils.graph_utils import create_graph, plot_graph, add_image_to_node
import matplotlib.font_manager as fm
import pandas as pd
import streamlit as st
import os

# 한글 폰트 설정
font_path = "/System/Library/Fonts/AppleSDGothicNeo.ttc"  # macOS의 다른 한글 폰트 경로
font_prop = fm.FontProperties(fname=font_path)

# 데이터 로드
df = pd.read_csv('labeled_data.csv')
df['timestamp'] = pd.to_datetime(df['timestamp'])

def show():
    st.title("9기의 워크샵 인물 관계 그래프 시각화")
    st.write("아직 제가 갖고 있는 사진 6장만 쓴 상태입니다!")

    time_point = st.slider(
        '시간 선택',
        min_value=df['timestamp'].min().to_pydatetime(),
        max_value=df['timestamp'].max().to_pydatetime(),
        value=df['timestamp'].min().to_pydatetime(),
        format="YYYY-MM-DD HH:mm:ss"
    )

    G, pos, sub_df = create_graph(time_point, df)
    fig = plot_graph(G, pos, sub_df, font_prop)  # 여기에 font_prop 추가

    st.pyplot(fig)

# 현재 시간과 일치하는 이미지 파일명 가져오기
    current_image_filenames = df[df['timestamp'] == time_point]['filename'].unique()

    # 현재 시간에 해당하는 이미지들을 Streamlit에 표시
    st.subheader('사용된 이미지')
    for img_file in current_image_filenames:
        img_path = os.path.join('image', img_file)
        if os.path.exists(img_path):
            st.image(img_path, caption=img_file, use_column_width=True)

    # 노드 선택 기능
    selected_node = st.selectbox('인물을 선택하세요', options=list(G.nodes))
    if selected_node:
        st.subheader(f"{selected_node}와 많이 연결된 상위 3명의 인물")
        neighbors = sorted(G[selected_node].items(), key=lambda x: x[1]['weight'], reverse=True)[:3]
        for neighbor, attr in neighbors:
            st.write(f"{neighbor} (연결 횟수: {attr['weight']})")

# 이 함수는 페이지를 실행할 때 호출됩니다.
if __name__ == "__main__":
    show()