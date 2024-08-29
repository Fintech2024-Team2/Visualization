import streamlit as st
from PIL import Image


def show():
    # 사이드바 설정
    st.sidebar.title("About")
    
    # 링크 이모지를 사이드바에 추가 (크게 표시)
    st.sidebar.markdown("<h1 style='text-align: center; font-size: 100px;'>🌎</h1>", unsafe_allow_html=True)    
    # GitHub 링크 추가
    st.sidebar.markdown("**GitHub URL**")
    st.sidebar.write("[Visit our GitHub](https://github.com/Fintech2024-Team2/Visualization)")

    # 메인 페이지 내용
    st.title("🎈 Workshop Visualization Project")
    st.write("""안녕하세요! 저희는 워크숍 사진을 기반으로 인물 간 네트워크 시각화 프로젝트를 진행한 2조입니다.""")
    st.write("""사이드바를 통해 원하시는 메뉴를 선택해주세요!""")

    # 메인 페이지 이미지 로드 및 표시
    image_path = "/Users/chaewon/Desktop/snukdt/시각화웹개발/project/Visualization/사진첩구현/체육대회/KakaoTalk_20240814_체육대회단체.jpg"
    img = Image.open(image_path)
    st.image(img, use_column_width=True)

if __name__ == "__main__":
    show()
