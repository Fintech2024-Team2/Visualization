import streamlit as st
import os
from PIL import Image

# Helper function to load images
def load_image(image_path):
    return Image.open(image_path)

def show():
    st.title("워크숍 갤러리")
    st.write("행사를 선택하세요:")

    # 각 행사별 사진 경로를 딕셔너리로 관리
    events = {
        "버스": "사진첩구현/버스",
        "체육대회": "사진첩구현/체육대회",
        "교육": "사진첩구현/교육",
        "뒷풀이": "사진첩구현/술자리",
        "오대산": "사진첩구현/오대산"
    }

    # 한 줄에 2개의 이벤트 버튼을 만들기 위해 컬럼 사용
    cols = st.columns(2)

    # 이벤트별로 버튼 생성
    event_selected = None
    for i, (event_name, event_path) in enumerate(events.items()):
        if cols[i % 2].button(event_name):
            event_selected = event_name

    # 선택된 이벤트에 대한 사진 표시
    if event_selected:
        st.subheader(f"{event_selected} 사진:")
        image_dir = events[event_selected]

        if os.path.exists(image_dir):
            photo_files = [f for f in os.listdir(image_dir) if f.endswith(('.JPG', '.PNG', '.jpg', '.png', '.jpeg'))]

            if photo_files:
                cols = st.columns(3)
                for i, img_file in enumerate(photo_files):
                    img = load_image(os.path.join(image_dir, img_file))
                    with cols[i % 3]:
                        st.image(img, use_column_width=True)
            else:
                st.write(f"{event_selected}에 대한 사진이 없습니다.")
        else:
            st.write(f"{event_selected}에 대한 이미지 폴더가 존재하지 않습니다.")

if __name__ == "__main__":
    show()
