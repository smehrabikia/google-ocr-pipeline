# pipeline.py

import os
from pathlib import Path
import argparse
from pdf_to_images_and_text import PDFProcessor

def main():
    parser = argparse.ArgumentParser(
        description="Full PDF to OCR pipeline with skip, error handling, and customizable outputs."
    )
    parser.add_argument("--input_dir", required=True, help="Input directory containing PDFs and images.")
    parser.add_argument("--service_account", required=True, help="Path to Google Cloud Service Account JSON.")
    parser.add_argument("--poppler_path", default=None, help="Path to poppler binaries (Windows only).")
    parser.add_argument("--save_txt", action="store_true", help="Save extracted text as .txt file.")
    parser.add_argument("--save_json", action="store_true", help="Save raw Vision API response as .json file.")
    parser.add_argument("--save_docx", action="store_true", help="Save OCR result as .docx file (Word document).")
    parser.add_argument("--dpi", type=int, default=300, help="DPI (Dots Per Inch) for PDF to image conversion. Recommended: 300.")
    parser.add_argument("--detection_type", default="TEXT_DETECTION", choices=["TEXT_DETECTION", "DOCUMENT_TEXT_DETECTION"], help="Vision API detection type: TEXT_DETECTION or DOCUMENT_TEXT_DETECTION.")
    
    args = parser.parse_args()

    input_dir = Path(args.input_dir)
    service_account = args.service_account
    poppler_path = args.poppler_path

    processor = PDFProcessor(
        service_account_path=service_account,
        poppler_path=poppler_path,
        save_txt=args.save_txt,
        save_json=args.save_json,
        save_docx=args.save_docx,
        dpi=args.dpi,
        detection_type=args.detection_type
    )

    pdf_files = list(input_dir.rglob("*.pdf"))
    total = len(pdf_files)
    print(f"🔵 Found {total} PDFs.")

    errors_file = open("errors.txt", "a", encoding="utf-8")

    for idx, pdf_path in enumerate(pdf_files, start=1):
        print(f"🔵 Processing {idx} of {total}: {pdf_path}")
        try:
            processor.process_pdf(pdf_path, input_dir)
        except Exception as e:
            print(f"❌ Error: {e}")
            errors_file.write(str(pdf_path) + "\n")
            continue

    errors_file.close()
    print("✅ All PDFs processed successfully.")

if __name__ == "__main__":
    main()
