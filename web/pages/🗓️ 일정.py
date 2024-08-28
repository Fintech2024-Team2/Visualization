import streamlit as st
import pandas as pd
import os
from PIL import Image

# Helper function to load images
def load_image(image_path):
    return Image.open(image_path)

def show_timeline_with_gallery():
    st.title("워크숍 타임라인 및 갤러리")

    # 주요 일정 데이터
    schedule_data = {
        "날짜": [
            "8.12", "8.12", "8.12", "8.12", "8.12", "8.13", "8.13", "8.13", "8.13"
        ],
        "시간": [
             "10:00", "12:00", "14:00", "19:00", "22:00",  "07:00", "08:30", "11:30", "13:00"
        ],
        "일정": [
            "버스 출발", 
            "횡성축협 점심", 
            "교육 및 캡스톤 케이스 스터디", 
            "OX 퀴즈 및 미니 체육대회", 
            "술(조별로)", 
            "기상",
            "강의 시작(이재욱 교수님 특강)", 
            "오대산 도착 및 등산",
            "점심식사"
        ],
        "사진폴더": [
            "버스", "점심", "교육", "체육대회", "술자리", 
            None, "강의", "오대산", "점심식사"
        ]
    }

    df_schedule = pd.DataFrame(schedule_data)

    # 일정과 갤러리 표시
    for _, row in df_schedule.iterrows():
        st.subheader(f"{row['날짜']} {row['시간']} - {row['일정']}")

        # 사진 폴더가 있을 때만 갤러리 표시
        if row['사진폴더']:
            st.write(f"{row['일정']} 관련 사진들:")
            image_dir = f"사진첩구현/{row['사진폴더']}"
            
            if os.path.exists(image_dir):
                photo_files = [f for f in os.listdir(image_dir) if f.endswith(('.JPG', '.PNG', '.jpg', '.png', '.jpeg'))]

                if photo_files:
                    cols = st.columns(3)
                    for i, img_file in enumerate(photo_files):
                        img = load_image(os.path.join(image_dir, img_file))
                        with cols[i % 3]:
                            st.image(img, use_column_width=True)
                else:
                    st.write("사진이 없습니다.")
            else:
                st.write("이미지 폴더가 존재하지 않습니다.")
        else:
            st.write("관련 사진 없음.")

if __name__ == "__main__":
    show_timeline_with_gallery()
