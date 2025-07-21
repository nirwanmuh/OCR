import streamlit as st
import easyocr
import numpy as np
import cv2
from PIL import Image
import tempfile
import os

st.set_page_config(page_title="OCR KTP/SIM/PASPOR", layout='centered')
st.sidebar.title("Input Dokumen")
st.title("OCR KTP/SIM/PASPOR")
option = st.sidebar.radio("Pilih metode input:", ("Kamera", "Upload File"))

reader = easyocr.Reader(['en', 'id'])

def load_image(image_file):
    img = Image.open(image_file)
    return img

def read_text(img_array):
    result = reader.readtext(img_array)
    text = "\n".join([res[1] for res in result])
    return text

if option == "Kamera":
    picture = st.camera_input("Ambil foto dokumen")
    if picture:
        img = load_image(picture)
        img_array = np.array(img)
        st.image(img, caption="Gambar yang diproses", use_column_width=True)
        st.subheader("Hasil OCR:")
        st.text(read_text(img_array))

elif option == "Upload File":
    uploaded_file = st.file_uploader("Unggah gambar dokumen", type=["png", "jpg", "jpeg"])
    if uploaded_file is not None:
        img = load_image(uploaded_file)
        img_array = np.array(img)
        st.image(img, caption="Gambar yang diproses", use_column_width=True)
        st.subheader("Hasil OCR:")
        st.text(read_text(img_array))
