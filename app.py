import streamlit as st
import easyocr
import numpy as np
from PIL import Image
import cv2

# Inisialisasi model EasyOCR (Bahasa Indonesia dan Inggris)
reader = easyocr.Reader(['id', 'en'])

st.set_page_config(page_title="OCR KTP/SIM/Paspor", layout="wide")
st.title("📷 OCR Pembaca KTP, SIM, dan Paspor")

# Pilihan input
input_mode = st.radio("Pilih metode input:", ["Upload Gambar", "Kamera Langsung"])

image = None

if input_mode == "Upload Gambar":
    uploaded_file = st.file_uploader("Unggah gambar dokumen", type=["jpg", "jpeg", "png"])
    if uploaded_file:
        image = Image.open(uploaded_file).convert("RGB")

elif input_mode == "Kamera Langsung":
    picture = st.camera_input("Ambil gambar dokumen")
    if picture:
        image = Image.open(picture).convert("RGB")

# Proses OCR jika gambar tersedia
if image:
    st.image(image, caption="Gambar Diterima", use_column_width=True)
    st.info("🔍 Memproses gambar dengan OCR...")

    # Ubah gambar ke numpy array
    image_np = np.array(image)

    # Gunakan EasyOCR
    results = reader.readtext(image_np)

    st.subheader("📄 Hasil Teks Terdeteksi")
    if not results:
        st.warning("❌ Tidak ada teks terdeteksi.")
    else:
        for (bbox, text, conf) in results:
            st.markdown(f"- **{text}** _(kepercayaan: {conf:.2f})_")

        # (Optional) Simpan hasil ke TXT
        with st.expander("📥 Unduh hasil OCR"):
            ocr_text = "\n".join([text for (_, text, _) in results])
            st.download_button("Unduh sebagai .txt", ocr_text, file_name="hasil_ocr.txt")

