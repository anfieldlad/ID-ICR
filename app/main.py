from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from PIL import Image

# Import the utilities from your 'utils.py'
from app.utils import process_image, extract_text, clean_text
# or, if you want to use the single wrapper:
# from app.utils import extract_ktp_data

app = FastAPI()

@app.post("/extract")
async def extract_data(file: UploadFile = File(...)):
    try:
        # 1. Load the image via PIL
        image = Image.open(file.file)
        
        # 2. Preprocess the image (adaptive threshold, etc.)
        processed_image = process_image(image, debug=False)
        
        # 3. Extract text via Tesseract
        extracted_text = extract_text(processed_image, debug=False)
        print("=== OCR Extracted Text ===")
        print(extracted_text)
        print("=========================")

        # 4. Clean & parse the text for KTP fields
        structured_data = clean_text(extracted_text, debug=False)
        
        return JSONResponse(
            content={"status": "Success", "data": structured_data},
            status_code=200
        )

    except Exception as e:
        return JSONResponse(
            content={"status": "Error", "message": str(e)},
            status_code=500
        )
