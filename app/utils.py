import cv2
import pytesseract
from PIL import Image
import numpy as np
import re

def process_image(image: Image.Image, debug: bool = False):
    """
    Preprocessing for better OCR accuracy:
      1) Convert to grayscale
      2) Resize (2x)
      3) Gaussian blur
      4) Adaptive threshold
    If debug=True, saves an intermediate 'processed_image_debug.jpg'.
    """
    # Convert PIL Image to OpenCV BGR format
    img = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    
    # Grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Resize the image (scaling by 2x). Increase if text is very small.
    resized = cv2.resize(gray, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    
    # Gaussian blur to reduce noise
    blurred = cv2.GaussianBlur(resized, (5, 5), 0)
    
    # Adaptive threshold (black & white)
    thresh = cv2.adaptiveThreshold(
        blurred,
        255,
        cv2.ADAPTIVE_THRESH_MEAN_C,
        cv2.THRESH_BINARY,
        15, 10
    )
    
    # Optional morphological closing (if needed)
    # kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2,2))
    # thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

    if debug:
        cv2.imwrite("processed_image_debug.jpg", thresh)
    
    return thresh

def extract_text(image, debug: bool = False) -> str:
    """
    Extract text from the thresholded image using Tesseract OCR.
    debug=True will print the raw OCR text.
    """
    custom_config = r'--oem 3 --psm 6'  # LSTM engine, uniform text block
    text = pytesseract.image_to_string(image, lang="ind", config=custom_config)
    
    if debug:
        print("=== Extracted OCR Text ===")
        print(text)
        print("=========================")
    
    return text

def unify_spaced_dates(line: str, debug: bool = False) -> str:
    """
    Convert spaced dates like '18 02 1986' to '18-02-1986' so regex can match them.
    Also attempts to handle partial splits like '1 22 02-2017'.
    """
    original_line = line
    
    # 1) Convert 'DD MM YYYY' => 'DD-MM-YYYY'
    line = re.sub(r'(\d{2})\s+(\d{2})\s+(\d{4})', r'\1-\2-\3', line)

    # 2) If we have partial patterns like '1 22 02-2017', remove leading digit
    #    e.g., '1 22 02-2017' => '22-02-2017' if we suspect the '1' is OCR noise.
    match_partial = re.search(r'\b(\d)\s+(\d{2})-(\d{2}-\d{4})\b', line)
    if match_partial:
        corrected = match_partial.group(2) + '-' + match_partial.group(3)
        start, end = match_partial.span()
        line = line[:start] + corrected + line[end:]
    
    if debug and line != original_line:
        print("=== unify_spaced_dates changed ===")
        print(f"Before: {original_line}")
        print(f"After:  {line}")
        print("==================================")

    return line

def clean_text(text: str, debug: bool = False) -> dict:
    """
    Cleans OCR text, unifies spaced dates, and extracts key KTP fields.
    Returns a dictionary of extracted data.
    """
    # Step 1: Basic cleanup
    text = re.sub(r'[“”‘’`"–—]+', ' ', text)  # fancy quotes/dashes -> space
    text = re.sub(r'[._/\-\\]+', ' ', text)   # . / \ - -> space
    text = re.sub(r'\s+', ' ', text).strip()  # multiple spaces -> single space
    
    # Step 2: Some common OCR mistake fixes (22-02:2017 => 22-02-2017)
    text = re.sub(r'(\d):(\d)', r'\1-\2', text)
    
    # Step 3: Single-line format
    cleaned_line = ' '.join(text.split())
    
    # Step 4: Unify spaced dates (if you have '18 02 1986')
    cleaned_line = unify_spaced_dates(cleaned_line, debug=debug)

    if debug:
        print("=== Final Cleaned Line ===")
        print(cleaned_line)
        print("=========================")

    # Prepare placeholders
    data = {
        'NIK': '',
        'Nama': '',
        'Tempat/Tgl Lahir': '',
        'Jenis Kelamin': '',
        'Gol. Darah': '',
        'Alamat': '',
        'RT/RW': '',
        'Kel/Desa': '',
        'Kecamatan': '',
        'Agama': '',
        'Status Perkawinan': '',
        'Pekerjaan': '',
        'Kewarganegaraan': '',
        'Berlaku Hingga': ''
    }

    # Step 5: Regex extraction
    # -----------------------------------------------------
    
    # NIK
    match = re.search(r'\bnik\s*:?\s*(\d{16})', cleaned_line, re.IGNORECASE)
    if match:
        data['NIK'] = match.group(1)
    else:
        match = re.search(r'\b(\d{16})\b', cleaned_line)
        if match:
            data['NIK'] = match.group(1)

    # Nama
    match = re.search(r'(?:nama\s*:?\s*)([A-Z\s]+)', cleaned_line, re.IGNORECASE)
    if match:
        data['Nama'] = match.group(1).strip()

    # Tempat/Tgl Lahir
    pattern_tempat = (
        r'(?:tempat\s*[^\s]*\s*lahir\s*:?\s*)'
        r'([A-Za-z]+,\s*\d{2}-\d{2}-\d{4})'
    )
    match = re.search(pattern_tempat, cleaned_line, re.IGNORECASE)
    if match:
        data['Tempat/Tgl Lahir'] = match.group(1).strip()
    else:
        # fallback: just capture "City, dd-mm-yyyy" if keywords are missing
        match2 = re.search(r'([A-Za-z]+,\s*\d{2}-\d{2}-\d{4})', cleaned_line)
        if match2:
            data['Tempat/Tgl Lahir'] = match2.group(1).strip()

    # Jenis Kelamin
    match = re.search(r'(?:jenis\s*kelamin\s*:?\s*)([A-Za-z]+)', cleaned_line, re.IGNORECASE)
    if match:
        data['Jenis Kelamin'] = match.group(1).strip()

    # Gol. Darah
    match = re.search(r'(?:gol\s*\.?\s*darah\s*:?\s*)([ABOab]{1,2})', cleaned_line, re.IGNORECASE)
    if match:
        data['Gol. Darah'] = match.group(1).upper()

    # Alamat
    match = re.search(r'(?:alamat\s*:?\s*)([A-Za-z0-9\s]+)', cleaned_line, re.IGNORECASE)
    if match:
        data['Alamat'] = match.group(1).strip()[:60]

    # RT/RW
    pattern_rtrw = (
        r'(?:rt\s*/?\s*rw|rturw)\s*:?\s*'
        r'([0-9]{1,3}\s*[/-]\s*[0-9]{1,3})'
    )
    match = re.search(pattern_rtrw, cleaned_line, re.IGNORECASE)
    if match:
        # unify e.g. "007 008" => "007/008"
        rt_rw = re.sub(r'\s*[/-]\s*', '/', match.group(1))
        data['RT/RW'] = rt_rw

    # Kel/Desa
    match = re.search(r'(?:kel[^\s]*desa\s*:?\s*)([A-Za-z]+)', cleaned_line, re.IGNORECASE)
    if match:
        data['Kel/Desa'] = match.group(1).strip()

    # Kecamatan
    match = re.search(r'(?:kecamatan\s*:?\s*)([A-Za-z]+)', cleaned_line, re.IGNORECASE)
    if match:
        data['Kecamatan'] = match.group(1).strip()

    # Agama
    match = re.search(r'agama\s*:?\s*[^\n]{0,20}([A-Za-z]+)', cleaned_line, re.IGNORECASE)
    if match:
        data['Agama'] = match.group(1).strip()

    # Status Perkawinan
    match = re.search(r'(?:status\s*perkawinan\s*:?\s*)([A-Za-z]+)', cleaned_line, re.IGNORECASE)
    if match:
        data['Status Perkawinan'] = match.group(1).strip()

    # Pekerjaan
    match = re.search(r'(?:pekerjaan\s*[^\w]*)([A-Za-z\s]+)', cleaned_line, re.IGNORECASE)
    if match:
        data['Pekerjaan'] = match.group(1).strip()[:30]

    # Kewarganegaraan
    match = re.search(r'(?:kewarganegaraan\s*:?\s*)([A-Za-z]+)', cleaned_line, re.IGNORECASE)
    if match:
        data['Kewarganegaraan'] = match.group(1).strip()

    # Berlaku Hingga
    pattern_berlaku = (
        r'berlaku\s*[^\w]*\s*hingga\s*[^\w]*\s*'
        r'(\d{1,2}[\s-]\d{2}[\s-]\d{4})'
    )
    match = re.search(pattern_berlaku, cleaned_line, re.IGNORECASE)
    if match:
        # e.g. "22 02 2017" or "22-02-2017" or "1 22 02-2017"
        raw_end_date = match.group(1).strip()
        normalized_date = re.sub(r'(\d{1,2})[\s-](\d{2})[\s-](\d{4})', r'\1-\2-\3', raw_end_date)
        data['Berlaku Hingga'] = normalized_date
    else:
        # fallback: any standalone dd-mm-yyyy (that isn't the same as Tempat/Tgl Lahir)
        match2 = re.search(r'\d{2}-\d{2}-\d{4}', cleaned_line)
        if match2:
            candidate_date = match2.group(0)
            if candidate_date != data['Tempat/Tgl Lahir']:
                data['Berlaku Hingga'] = candidate_date

    if debug:
        print("=== Extracted Fields ===")
        for k, v in data.items():
            print(f"{k}: {v}")
        print("========================")

    return data