import streamlit as st
import easyocr
import numpy as np
from PIL import Image
import re

st.set_page_config(page_title="OCR KTP/SIM/Paspor", layout="centered")

st.title("📷 OCR KTP / SIM / Paspor 🇮🇩")

# --- Sidebar ---
st.sidebar.header("🛠️ Pilih Metode Input")
st.sidebar.write("Gunakan kamera atau unggah gambar dokumen identitas.")

input_method = None
col1, col2 = st.sidebar.columns(2)
with col1:
    if st.button("📸 Kamera"):
        input_method = "Kamera"
with col2:
    if st.button("📁 Upload"):
        input_method = "Upload"

image = None
if input_method == "Kamera":
    image = st.camera_input("Ambil gambar dokumen")
elif input_method == "Upload":
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
