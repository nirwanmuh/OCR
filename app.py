# app.py
import streamlit as st
from doctr.io import DocumentFile
from doctr.models import ocr_predictor
import cv2
from PIL import Image
import numpy as np

st.set_page_config(page_title="OCR Dokumen Identitas", layout="centered")
st.sidebar.title("📸 Input Gambar")
input_method = st.sidebar.radio("Pilih metode input:", ["📷 Kamera", "📁 Upload File"])

# Load OCR model (deteksi + rekognisi)
@st.cache_resource
def load_model():
    return ocr_predictor(pretrained=True)

model = load_model()

def read_image(img):
    return DocumentFile.from_images([np.array(img)])

if input_method == "📷 Kamera":
    img_file = st.camera_input("Ambil gambar KTP/SIM/Paspor")
elif input_method == "📁 Upload File":
    img_file = st.file_uploader("Unggah gambar dokumen (JPG/PNG)", type=["jpg", "png", "jpeg"])

if img_file:
    image = Image.open(img_file).convert("RGB")
    st.image(image, caption="Dokumen Diterima", use_column_width=True)

    with st.spinner("🔍 Menjalankan OCR..."):
        doc = read_image(image)
        result = model(doc)
        extracted_text = result.render()
        st.subheader("📄 Hasil OCR")
        st.code(extracted_text, language="text")
