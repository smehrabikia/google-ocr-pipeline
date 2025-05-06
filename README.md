# Google OCR Pipeline with Resume & Recovery

This project uses **Google Cloud Vision API** to perform OCR on PDFs and images (including Persian + English mixed content), and outputs `.txt`, `.docx`, and `.json` with RTL/LTR-aware formatting.

## 🔧 Features

- PDF to image conversion using `pdf2image`
- OCR using Google Vision API
- Proper directionality (RTL/LTR) handling for Persian-English mix
- Smart resume support (avoids reprocessing)
- Error logging to `errors.txt`
- DOCX output with B Nazanin font

## 🚀 How to Use

```bash
python pipeline.py \
  --input_dir data/input \
  --service_account credentials/your-service-account.json \
  --save_docx --save_txt --save_json \
  --dpi 300 \
  --detection_type DOCUMENT_TEXT_DETECTION
```

## 📂 Project Structure
google_ocr_pipeline/
├── pipeline.py # Main runner script
├── pdf_to_images_and_text.py # PDF to images + OCR per page
├── ocr_helper.py # OCR & formatting logic
├── requirements.txt # Python dependencies
├── .gitignore # Files/folders to exclude from Git
├── README.md # This documentation
├── credentials/ # Your Google API key (NOT in Git)
├── data/input/ # Source PDFs/images
├── output/ # Processed output (optional)
└── errors.txt # Error log

 Requires Python 3.8+

Installation
pip install -r requirements.txt


License
MIT License – free for personal and commercial use.
