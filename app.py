import streamlit as st
import cv2
from utils import load_image, preprocess_image, extract_text_fields, classify_doc

st.set_page_config(page_title="OCR KTP, SIM, PASPOR", layout="wide")

st.title("📄 Pembaca Dokumen KTP, SIM, PASPOR Berbasis AI")
st.markdown("Upload gambar dokumen dan sistem akan mengekstrak informasi penting secara otomatis.")

uploaded_file = st.file_uploader("📷 Upload Gambar Dokumen (JPG/PNG)", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = load_image(uploaded_file)

    st.image(image, caption='Dokumen Diupload', use_column_width=True)

    with st.spinner("🔍 Mendeteksi dan Membaca Dokumen..."):
        processed_image = preprocess_image(image)
        text, fields = extract_text_fields(processed_image)
        tipe_dokumen = classify_doc(text)

    st.subheader("📌 Jenis Dokumen")
    st.success(tipe_dokumen)

    st.subheader("📋 Hasil Ekstraksi Data")
    for k, v in fields.items():
        st.text(f"{k}: {v if v else '-'}")

    st.subheader("📝 Teks Lengkap (OCR)")
    st.code(text)
