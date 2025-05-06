# pdf_to_images_and_text.py

import os
from pathlib import Path
from pdf2image import convert_from_path
from ocr_helper import OCRHelper

class PDFProcessor:
    def __init__(self, service_account_path, poppler_path=None, save_txt=True, save_json=True, save_docx=True, dpi=300, detection_type="TEXT_DETECTION"):
        self.poppler_path = poppler_path
        self.save_txt = save_txt
        self.save_json = save_json
        self.save_docx = save_docx
        self.dpi = dpi
        self.detection_type = detection_type
        self.ocr_helper = OCRHelper(service_account_path, detection_type=detection_type)

    def process_pdf(self, pdf_path, output_root):
        relative_path = pdf_path.relative_to(output_root)
        folder_name = relative_path.parent / pdf_path.stem
        output_folder = output_root / folder_name
        output_folder.mkdir(parents=True, exist_ok=True)

        ok_file = output_folder / "ok.txt"
        if ok_file.exists():
            print(f"⏩ Already processed: {pdf_path}")
            return

        try:
            # Step 1: Convert PDF to images if not already done
            image_files = sorted(output_folder.glob("page_*.jpg"))
            if not image_files:
                print(f"🖼 Converting PDF to images: {pdf_path}")
                images = convert_from_path(str(pdf_path), dpi=self.dpi, poppler_path=self.poppler_path)
                for idx, image in enumerate(images):
                    image_path = output_folder / f"page_{idx+1:03d}.jpg"
                    image.save(image_path, 'JPEG')
                image_files = sorted(output_folder.glob("page_*.jpg"))

            if not image_files:
                raise Exception("No images found or conversion failed.")

            # Step 2: OCR only missing outputs
            success_count = 0
            for image_path in image_files:
                base = image_path.with_suffix('')
                txt_ok = base.with_suffix('.txt').exists() if self.save_txt else True
                json_ok = base.with_suffix('.json').exists() if self.save_json else True
                docx_ok = base.with_suffix('.docx').exists() if self.save_docx else True

                if txt_ok and json_ok and docx_ok:
                    continue  # already processed

                print(f"🔍 OCR: {image_path.name}")
                self.ocr_helper.ocr_image(
                    str(image_path),
                    save_txt=self.save_txt,
                    save_json=self.save_json,
                    save_docx=self.save_docx
                )
                success_count += 1

            if success_count == 0:
                print(f"✅ All pages already OCRed for: {pdf_path}")
            else:
                print(f"✅ OCR completed for {success_count} new pages in: {pdf_path}")

            # Step 3: If all pages have output, mark as completed
            if all(
                (img.with_suffix('.txt').exists() if self.save_txt else True) and
                (img.with_suffix('.json').exists() if self.save_json else True) and
                (img.with_suffix('.docx').exists() if self.save_docx else True)
                for img in image_files
            ):
                ok_file.write_text("done")
                print(f"📌 Marked as complete: {pdf_path}")

        except Exception as e:
            raise Exception(f"Error processing {pdf_path}: {e}")
