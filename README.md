 __     ____   ___   ___  ___   ____ 
 \ \   / /_ | / _ \ / _ \|__ \ / __ \
  \ \_/ / | || | | | | | |  ) | |  | |
   \   /  | || | | | | | | / /| |  | |
    | |   | || |_| | |_| |/ /_| |__| |
    |_|   |_(_)___/ \___//____|\____/ 

             ID-ICR
Indonesian Document Intelligent Character Recognition


[ Project Overview ]
-------------------------------------------------------------------------------
ID-ICR is a tool for extracting information from Indonesian identity documents.
Currently, it supports OCR-based parsing of KTP (Indonesian national ID cards).
In the future, ID-ICR aims to expand into a full-fledged ICR (Intelligent 
Character Recognition) solution for various Indonesian documents like NPWP, 
driver’s licenses (SIM), invoices, and more.

[ Current Features ]
-------------------------------------------------------------------------------
1. FastAPI endpoint for uploading KTP images and receiving extracted data in JSON.
2. Image preprocessing (OpenCV + Tesseract) to enhance OCR accuracy.
3. Regex-based parsing for key KTP fields (NIK, Nama, Tempat/Tgl Lahir, etc.).
4. Ready to integrate with classification logic for multi-document support.

[ Roadmap ]
-------------------------------------------------------------------------------
1. Document Type Classification 
   - Use ML or rule-based approaches to distinguish KTP, NPWP, etc.
2. Expand Field Extraction 
   - Add specialized parsers for NPWP, SIM, official letters, and more.
3. Validation & Checks 
   - Validate field formats (e.g., 16-digit NIK, 15-digit NPWP).
4. User-Friendly Front-End 
   - Implement a web or mobile interface for direct uploads & quick scanning.

[ How to Use ]
-------------------------------------------------------------------------------
1. Clone or download this repository.
2. Install required Python packages from `requirements.txt`.
3. Run `uvicorn main:app --reload` to start the FastAPI server.
4. Send a POST request to `/extract` with a file upload of a KTP image.
5. Receive a JSON response containing the extracted fields.

[ Contributing ]
-------------------------------------------------------------------------------
1. Fork the repo and create a new branch for your feature or fix.
2. Implement and test your changes.
3. Submit a Pull Request describing your work.

[ License ]
-------------------------------------------------------------------------------
This project is licensed under the MIT License (or your chosen license). 
Please see the LICENSE file for details.

===============================================================================
     Thank you for your interest in ID-ICR!
       Let's build the future of Indonesian Document ICR together.
===============================================================================
