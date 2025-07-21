import streamlit as st
import easyocr
import numpy as np
import cv2
from PIL import Image
import tempfile
import os
from spellchecker import SpellChecker

# Inisialisasi OCR dan spellchecker
reader = easyocr.Reader(['id'], paragraph=True)
spell = SpellChecker(language=None)

# Load file kamus kata bahasa Indonesia
try:
    spell.word_frequency.load_text_file("indonesian_words.txt")
    use_spellcheck = True
except:
    st.warning("File 'indonesian_words.txt' tidak ditemukan. Spellcheck dinonaktifkan.")
    use_spellcheck = False

# Fungsi koreksi ejaan
def clean_text(text):
    words = text.split()
    corrected = [spell.correction(w) or w for w in words]
    return ' '.join(corrected)

# Fungsi konversi image
def load_image(image_file):
    image = Image.open(image_file)
    return np.array(image)

st.set_page_config(page_title="OCR KTP", layout="wide")

# === SIDEBAR ===
st.sidebar.title("OCR Dokumen Identitas")
st.sidebar.write("Gunakan kamera atau unggah gambar dokumen identitas.")

input_method = st.sidebar.radio("Pilih metode input:", ("Kamera", "Upload File"))

# === INPUT GAMBAR ===
image = None

if input_method == "Kamera":
    img_file = st.camera_input("Ambil gambar melalui kamera")
    if img_file is not None:
        image = load_image(img_file)
elif input_method == "Upload File":
    img_file = st.file_uploader("Unggah gambar dokumen (JPG/PNG)", type=['png', 'jpg', 'jpeg'])
    if img_file is not None:
        image = load_image(img_file)

# === OCR & OUTPUT ===
if image is not None:
    st.image(image, caption="Gambar yang Diproses", use_column_width=True)

    with st.spinner("🔍 Sedang memproses OCR..."):
        results = reader.readtext(image, detail=0, paragraph=True)
        text_raw = "\n".join(results)

        st.subheader("📄 Hasil OCR (tanpa koreksi)")
        st.text_area("Teks Mentah:", text_raw, height=200)

        if use_spellcheck:
            cleaned = clean_text(text_raw)
            st.subheader("✅ Teks Setelah Koreksi")
            st.text_area("Teks Final:", cleaned, height=200)
        else:
            st.info("Spellcheck tidak tersedia karena kamus tidak ditemukan.")

