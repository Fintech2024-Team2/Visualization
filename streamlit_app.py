import streamlit as st
import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from PIL import Image, ExifTags
import os

# CSV 파일로부터 DataFrame 읽기
df = pd.read_csv('/Users/chaewon/Desktop/snukdt/시각화웹개발/project/exdata.csv')
df['timestamp'] = pd.to_datetime(df['timestamp'])

# 한글 폰트 설정
font_path = "/System/Library/Fonts/AppleSDGothicNeo.ttc"  # macOS의 다른 한글 폰트 경로
font_prop = fm.FontProperties(fname=font_path)
plt.rc('font', family=font_prop.get_name())
plt.rcParams['axes.unicode_minus'] = False

# Streamlit 사이드바 메뉴
st.sidebar.title("메뉴")
menu_selection = st.sidebar.selectbox("메뉴 선택", ("HOME", "갤러리", "인물 관계도", "마니또"))

# 시작 페이지
if menu_selection == "HOME":
    st.title("HOME")
    st.write("반갑습니다!")
    st.write("저희는 워크숍에서 찍은 사진을 이용해 시간 순서대로 인물 간 관계 그래프를 시각화 해보았습니다.")
    st.write("왼쪽 사이드바에서 다른 메뉴를 선택해보세요 :>")

# 갤러리 페이지
elif menu_selection == "갤러리":
    st.title("갤러리")
    st.write("워크숍 갤러리")
    
    # 예시로 몇 개의 이미지를 표시 (실제 이미지를 여기에 추가할 수 있습니다)
    image_dir = '/Users/chaewon/Desktop/snukdt/시각화웹개발/project/image'
    for img_file in os.listdir(image_dir):
        img_path = os.path.join(image_dir, img_file)
        st.image(img_path, caption=img_file, use_column_width=True)

# 그래프 페이지
elif menu_selection == "인물 관계도":
    st.title("9기의 워크샵 인물 관계 그래프 시각화")
    st.write("아직 제가 갖고 있는 사진 6장만 쓴 상태입니다!")

    # Streamlit 슬라이더로 시간 조정
    time_point = st.slider(
        '시간 선택',
        min_value=df['timestamp'].min().to_pydatetime(),
        max_value=df['timestamp'].max().to_pydatetime(),
        value=df['timestamp'].min().to_pydatetime(),
        format="YYYY-MM-DD HH:mm:ss"
    )

    # 그래프 생성 및 정보 저장
    G = nx.Graph()
    sub_df = df[df['timestamp'] <= time_point]
    for filename, group in sub_df.groupby('filename'):
        persons = list(group['class'])
        for i in range(len(persons)):
            for j in range(i + 1, len(persons)):
                if G.has_edge(persons[i], persons[j]):
                    G[persons[i]][persons[j]]['weight'] += 1
                else:
                    G.add_edge(persons[i], persons[j], weight=1)

    pos = nx.spring_layout(G)
    weights = [G[u][v]['weight'] for u, v in G.edges()]

    # 그래프 그리기
    fig, ax = plt.subplots(figsize=(10, 7))
    nx.draw(G, pos, ax=ax, with_labels=False, width=weights, node_color='lightblue', edge_color='gray')

    # 노드에 이미지와 이름 추가 함수
    def add_image_to_node(node, pos, ax, img, bbox, zoom=0.2):
        # 바운딩 박스 좌표로 이미지 자르기
        xmin, ymin, xmax, ymax = bbox
        face = img.crop((xmin, ymin, xmax, ymax))
        imagebox = OffsetImage(face, zoom=zoom)  # 이미지 크기 조절
        ab = AnnotationBbox(imagebox, pos, frameon=False)
        ax.add_artist(ab)
        # 이름을 이미지 아래에 추가
        ax.text(pos[0], pos[1] - 0.2, node, ha='center', fontproperties=font_prop, fontsize=12, fontweight='bold')

    # 노드에 사진 추가 (df의 filename을 사용하여 이미지 경로를 가져옴)
    for node, (x, y) in pos.items():
        row = sub_df[sub_df['class'] == node].iloc[0]  # 해당 노드에 해당하는 데이터 행
        img_file = row['filename']
        img_path = os.path.join('/Users/chaewon/Desktop/snukdt/시각화웹개발/project/image', img_file)
        
        if os.path.exists(img_path):
            img = Image.open(img_path)

            # EXIF 데이터에 따라 이미지 회전
            try:
                for orientation in ExifTags.TAGS.keys():
                    if ExifTags.TAGS[orientation] == 'Orientation':
                        break
                exif = dict(img._getexif().items())

                if exif[orientation] == 3:
                    img = img.rotate(180, expand=True)
                elif exif[orientation] == 6:
                    img = img.rotate(270, expand=True)
                elif exif[orientation] == 8:
                    img = img.rotate(90, expand=True)
            except (AttributeError, KeyError, IndexError):
                # EXIF 정보가 없으면 기본적으로 회전하지 않음
                pass

            bbox = (row['xmin'], row['ymin'], row['xmax'], row['ymax'])  # 바운딩 박스 좌표
            add_image_to_node(node, (x, y), ax, img, bbox, zoom=0.2)
        else:
            ax.text(x, y, s=node, bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.3'),
                    horizontalalignment='center', fontproperties=font_prop, fontsize=12, fontweight='bold')

    # 제목 설정
    ax.set_title(f"시간: {time_point.strftime('%Y-%m-%d %H:%M:%S')}", fontsize=16, fontproperties=font_prop)

    # Streamlit에 그래프 출력
    st.pyplot(fig)

    # 현재 시간과 일치하는 이미지 파일명 가져오기
    current_image_filenames = df[df['timestamp'] == time_point]['filename'].unique()

    # 현재 시간에 해당하는 이미지들을 Streamlit에 표시
    st.subheader('사용된 이미지')
    for img_file in current_image_filenames:
        img_path = os.path.join('/Users/chaewon/Desktop/snukdt/시각화웹개발/project/image', img_file)
        if os.path.exists(img_path):
            st.image(img_path, caption=img_file, use_column_width=True)

    # 노드 선택 기능
    selected_node = st.selectbox('인물을 선택하세요', options=list(G.nodes))
    if selected_node:
        st.subheader(f"{selected_node}와 많이 연결된 상위 3명의 인물")
        neighbors = sorted(G[selected_node].items(), key=lambda x: x[1]['weight'], reverse=True)[:3]
        for neighbor, attr in neighbors:
            st.write(f"{neighbor} (연결 횟수: {attr['weight']})")

elif menu_selection == "마니또":
    st.title("마니또")
    st.write("당신의 마니또를 검색하세요!")

    # 노드 검색 기능
    search_query = st.text_input('마니또 검색')
    if search_query:
        search_results = [node for node in G.nodes if search_query in node]
        if search_results:
            st.subheader('검색 결과:')
            for result in search_results:
                st.write(result)
        else:
            st.write('검색 결과가 없습니다.')
    
    st.write("마니또 검색하면 뭐가 나오게 하면 좋을까용")
    st.write("마니또 데이터프레임도 만들어야 해요")