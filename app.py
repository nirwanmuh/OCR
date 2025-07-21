import streamlit as st
import easyocr
import numpy as np
from PIL import Image
from spellchecker import SpellChecker  # Untuk koreksi kata
import io

# Inisialisasi OCR dan SpellChecker
reader = easyocr.Reader(['id', 'en'])  # Bahasa Indonesia + Inggris
spell = SpellChecker(language=None)  # Kita masukkan kosa kata manual
spell.word_frequency.load_text_file('indonesian_words.txt')  # File berisi kata2 baku Indo

# Fungsi koreksi kata
def auto_correct_text(text):
    corrected = []
    for word in text.split():
        if word.lower() in spell:
            corrected.append(word)
        else:
            corrected.append(spell.correction(word) or word)
    return " ".join(corrected)

# UI di Streamlit
st.sidebar.title("OCR Dokumen Identitas")
input_mode = st.sidebar.radio("Pilih metode input:", ["Kamera", "Upload File"])

if input_mode == "Kamera":
    uploaded_file = st.camera_input("Ambil foto dokumen:")
else:
    uploaded_file = st.file_uploader("Upload gambar dokumen (JPEG/PNG)", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Gambar diambil", use_column_width=True)

    with st.spinner("Sedang mengenali teks..."):
        result = reader.readtext(np.array(image), detail=0, paragraph=True)
        original_text = "\n".join(result)
        corrected_text = auto_correct_text(original_text)

        st.subheader("📄 Teks Asli (OCR):")
        st.text_area("Teks dari gambar:", value=original_text, height=200)

        st.subheader("🛠️ Setelah Koreksi Otomatis:")
        st.text_area("Teks setelah koreksi:", value=corrected_text, height=200)
