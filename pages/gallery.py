import streamlit as st
import os
from utils.image_utils import load_image

def show():
    st.title("갤러리")
    st.write("워크숍 갤러리")

    image_dir = '/Users/chaewon/Desktop/snukdt/시각화웹개발/project/image'
    for img_file in os.listdir(image_dir):
        img = load_image(os.path.join(image_dir, img_file))
        st.image(img, caption=img_file, use_column_width=True)
