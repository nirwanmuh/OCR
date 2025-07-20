import cv2
import numpy as np
from paddleocr import PaddleOCR

ocr_model = PaddleOCR(use_angle_cls=True, lang='ind')

def load_image(uploaded_file):
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    image = cv2.imdecode(file_bytes, 1)
    return image

def preprocess_image(image):
    # Convert to grayscale & threshold
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return gray

def extract_text_fields(image):
    result = ocr_model.ocr(image, cls=True)
    lines = [line[1][0] for line in result[0]]
    text = "\n".join(lines)

    fields = {
        "NIK": None,
        "Nama": None,
        "Tempat/Tanggal Lahir": None,
        "Alamat": None
    }

    for line in lines:
        if "nik" in line.lower():
            fields["NIK"] = line
        elif "nama" in line.lower():
            fields["Nama"] = line
        elif "lahir" in line.lower():
            fields["Tempat/Tanggal Lahir"] = line
        elif "alamat" in line.lower():
            fields["Alamat"] = line

    return text, fields

def classify_doc(text):
    if "nik" in text.lower():
        return "KTP"
    elif "sim" in text.lower():
        return "SIM"
    elif "paspor" in text.lower() or "passport" in text.lower():
        return "PASPOR"
    else:
        return "Tidak Diketahui"
