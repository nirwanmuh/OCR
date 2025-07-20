import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase
import av
import cv2
import pytesseract
from PIL import Image
import numpy as np
import re

st.set_page_config(page_title="OCR KTP/SIM/Paspor", layout="centered")
st.title("\U0001F4F8 OCR dari Kamera & Upload Gambar")

st.sidebar.header("\U0001F4E4 Pilih Input")
input_type = st.sidebar.radio("Input dari:", ["Kamera", "Upload Gambar"])

image_to_ocr = None  # Global holder for image

if input_type == "Upload Gambar":
    uploaded_file = st.file_uploader("Upload gambar dokumen", type=['jpg', 'jpeg', 'png'])
    if uploaded_file:
        image = Image.open(uploaded_file).convert("RGB")
        st.image(image, caption="Dokumen yang diunggah", use_column_width=True)
        image_to_ocr = np.array(image)

else:
    class VideoTransformer(VideoTransformerBase):
        def transform(self, frame: av.VideoFrame) -> np.ndarray:
            img = frame.to_ndarray(format="bgr24")
            self.last_frame = img
            return cv2.putText(img.copy(), "Tekan tombol OCR setelah ini!", (10, 30),
                               cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    ctx = webrtc_streamer(
        key="ocr-camera",
        video_transformer_factory=VideoTransformer,
        media_stream_constraints={"video": True, "audio": False},
        async_transform=True,
    )

    if ctx.video_transformer:
        if st.button("\U0001F4F8 Ambil Gambar dari Kamera"):
            frame = ctx.video_transformer.last_frame
            if frame is not None:
                st.image(frame, caption="Gambar dari kamera", use_column_width=True)
                image_to_ocr = frame

# Jalankan OCR jika gambar tersedia
if image_to_ocr is not None:
    st.subheader("\U0001F4CB Hasil OCR")
    with st.spinner("\U0001F50D Sedang membaca teks..."):
        text = pytesseract.image_to_string(image_to_ocr, lang='ind')  # Bisa juga 'eng'
    st.text_area("\U0001F4DD Teks Terbaca:", text, height=300)

    # Ekstraksi otomatis (opsional)
    st.subheader("\U0001F4CC Ekstraksi Otomatis")
    nik = re.search(r'\d{16}', text)
    nama = re.search(r'Nama\s*[:\-]?\s*(.*)', text, re.IGNORECASE)
    ttl = re.search(r'Tempat.*Tgl.*Lahir\s*[:\-]?\s*(.*)', text, re.IGNORECASE)

    st.write("**NIK:**", nik.group() if nik else "Tidak ditemukan")
    st.write("**Nama:**", nama.group(1).strip() if nama else "Tidak ditemukan")
    st.write("**Tempat/Tgl Lahir:**", ttl.group(1).strip() if ttl else "Tidak ditemukan")
