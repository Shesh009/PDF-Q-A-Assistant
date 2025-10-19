import PyPDF2
import re

class PDFParser:
    def __init__(self, pdf_file):
        self.pdf_file = pdf_file

    def is_english(self, text):
        return re.sub(r"[^a-zA-Z0-9\s.,;:!?\'\"()\[\]\-]", '', text)

    def extract_text(self):
        pdf_reader = PyPDF2.PdfReader(self.pdf_file)
        extracted_text = ""

        for page in pdf_reader.pages:
            text = page.extract_text()
            if text:
                cleaned_text = self.is_english(text)
                extracted_text += cleaned_text + "\n"
        
        return extracted_text.strip()
