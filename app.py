import streamlit as st
import easyocr
import numpy as np
from PIL import Image
import re

st.set_page_config(page_title="OCR KTP/SIM/Paspor", layout="centered")

st.title("📷 OCR KTP / SIM / Paspor 🇮🇩")
st.write("Gunakan kamera atau unggah gambar dokumen identitas.")

# Input gambar
input_type = st.radio("Pilih metode input:", ["Kamera", "Upload File"])

image = None
if input_type == "Kamera":
    image = st.camera_input("Ambil gambar dokumen")
else:
    image = st.file_uploader("Upload gambar dokumen", type=["jpg", "jpeg", "png"])

if image is not None:
    img = Image.open(image).convert("RGB")
    img_np = np.array(img)

    st.image(img_np, caption="📄 Gambar yang Diproses", use_column_width=True)

    st.write("🔍 Sedang memproses teks...")

    # OCR dengan EasyOCR
    reader = easyocr.Reader(['id', 'en'])
    results = reader.readtext(img_np)

    extracted_text = [text for (_, text, _) in results]

    st.subheader("📋 Teks Terdeteksi:")
    st.text("\n".join(extracted_text))

    # Ekstrak pola penting (misal NIK, Tanggal Lahir)
    nik = next((t for t in extracted_text if re.fullmatch(r"\d{16}", t)), None)
    tgl_lahir = next((t for t in extracted_text if re.search(r"\d{2}[-/ ]\d{2}[-/ ]\d{4}", t)), None)

    st.markdown(f"**NIK:** {nik or 'Tidak ditemukan'}")
    st.markdown(f"**Tanggal Lahir:** {tgl_lahir or 'Tidak ditemukan'}")
