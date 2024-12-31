# ID-ICR

**ID-ICR (Indonesian Document Intelligent Character Recognition)** is a project designed to extract information from Indonesian identity documents. The current focus is on **OCR-based KTP (Indonesian national ID card) parsing**, with plans to expand into a broader ICR solution for various Indonesian documents like NPWP, SIM, and more.

## Project Features

- **FastAPI Endpoint**:
  - Upload KTP images and receive extracted data in **JSON** format.
- **Image Preprocessing**:
  - Leverages OpenCV and Tesseract for improved OCR accuracy on scanned or low-quality images.
- **Field Extraction**:
  - Regex-based parsing tailored for KTP fields such as NIK, Nama, Alamat, Tempat/Tgl Lahir, etc.
- **Extensibility**:
  - Ready to support new document types and implement classification logic for multi-document support.

---

## Roadmap

1. **Document Classification**:
   - Introduce ML-based or heuristic-based document type detection (e.g., KTP vs. NPWP).
2. **Field-Level Parsing for Additional Documents**:
   - Add parsing logic for NPWP, SIM, and other common Indonesian documents.
3. **Validation and Verification**:
   - Include validation logic for field formats (e.g., 16-digit NIK, 15-digit NPWP patterns).
4. **User-Friendly Frontend**:
   - Develop a simple web or mobile interface for direct uploads and real-time scanning.

---

## How to Use

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/id-icr.git
   cd id-icr
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Start the FastAPI server:
   ```bash
   uvicorn main:app --reload
   ```
4. Use the `/extract` endpoint:
   - Upload a KTP image via a POST request.
   - Receive extracted data in JSON format.

---

## Contributing

We welcome contributions! Follow these steps:

1. **Fork** the repository and create a new branch for your feature or fix.
2. Implement and test your changes.
3. Submit a **Pull Request** with a detailed explanation of your work.

---

## License

This project is licensed under the **MIT License**. See the `LICENSE` file for details.

---

### Join Us!

Help us expand **ID-ICR** into a full-featured platform for **Indonesian Document Intelligent Character Recognition**. Together, we can enable smarter and faster document processing for Indonesia!