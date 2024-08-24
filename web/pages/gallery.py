import streamlit as st
import os
from utils.image_utils import load_image

def show():
    st.title("갤러리")
    st.write("워크숍 갤러리")

    image_dir = 'image'
    for img_file in os.listdir(image_dir):
        img = load_image(os.path.join(image_dir, img_file))
        st.image(img, caption=img_file, use_column_width=True)

# 이 함수는 페이지를 실행할 때 호출됩니다.
if __name__ == "__main__":
    show()