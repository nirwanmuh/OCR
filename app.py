import streamlit as st
from PIL import Image
import numpy as np
from paddleocr import PaddleOCR

# Inisialisasi model PaddleOCR (hanya sekali)
ocr_model = PaddleOCR(use_angle_cls=True, lang='ind')  # Menggunakan Bahasa Indonesia

# Fungsi untuk memuat dan mengubah file gambar menjadi array NumPy
def load_image(uploaded_file):
    image = Image.open(uploaded_file).convert("RGB")
    return np.array(image)

# Fungsi untuk ekstraksi teks dan data penting
def extract_text_fields(image_np):
    result = ocr_model.ocr(image_np, cls=True)
    lines = [line[1][0] for line in result[0]]  # Ambil teks dari hasil OCR

    full_text = "\n".join(lines)

    # Ekstrak informasi penting berdasarkan kata kunci
    fields = {
        "NIK": "-",
        "Nama": "-",
        "Tempat/Tanggal Lahir": "-",
        "Alamat": "-"
    }

    for line in lines:
        line_lower = line.lower()
        if "nik" in line_lower and fields["NIK"] == "-":
            fields["NIK"] = line
        elif "nama" in line_lower and fields["Nama"] == "-":
            fields["Nama"] = line
        elif "lahir" in line_lower and fields["Tempat/Tanggal Lahir"] == "-":
            fields["Tempat/Tanggal Lahir"] = line
        elif "alamat" in line_lower and fields["Alamat"] == "-":
            fields["Alamat"] = line

    return full_text, fields

# Klasifikasi jenis dokumen berdasarkan isi teks
def classify_doc(text):
    text_lower = text.lower()
    if "nik" in text_lower:
        return "KTP"
    elif "sim" in text_lower:
        return "SIM"
    elif "paspor" in text_lower or "passport" in text_lower:
        return "PASPOR"
    else:
        return "Tidak Diketahui"

# Konfigurasi halaman Streamlit
st.set_page_config(page_title="OCR Dokumen KTP, SIM, PASPOR", layout="wide")

st.title("📄 Pembaca KTP, SIM, dan PASPOR Otomatis")
st.markdown("Upload gambar dokumen, dan sistem akan mengekstrak data penting menggunakan AI (OCR).")

uploaded_file = st.file_uploader("📤 Upload gambar (PNG, JPG, JPEG)", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    st.image(uploaded_file, caption="Dokumen yang Diunggah", use_column_width=True)

    with st.spinner("🔍 Menganalisis dokumen..."):
        image_np = load_image(uploaded_file)
        full_text, fields = extract_text_fields(image_np)
        doc_type = classify_doc(full_text)

    st.success(f"📌 Jenis Dokumen: {doc_type}")

    st.subheader("📋 Data yang Terdeteksi:")
    for field, value in fields.items():
        st.text(f"{field}: {value}")

    st.subheader("📝 Teks Lengkap (OCR):")
    st.code(full_text)
