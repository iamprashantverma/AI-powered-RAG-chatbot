import tempfile
import os

import fitz
from docx import Document
import pandas as pd


class FileTextExtractionService:

    @staticmethod
    def extract(file_bytes: bytes, filename: str) -> str:
        suffix = filename.split(".")[-1].lower()

        tmp = tempfile.NamedTemporaryFile(delete=False, suffix="." + suffix)
        try:
            tmp.write(file_bytes)
            tmp.close()

            if suffix == "pdf":
                text = FileTextExtractionService._extract_pdf(tmp.name)
            elif suffix == "docx":
                text = FileTextExtractionService._extract_docx(tmp.name)
            elif suffix in ("xlsx", "xls"):
                text = FileTextExtractionService._extract_excel(tmp.name)
            else:
                raise ValueError("Only PDF, DOCX, and Excel files are supported")

            if not text.strip():
                raise ValueError("No readable text found in file")

            return FileTextExtractionService._clean(text)

        finally:
            os.unlink(tmp.name)

    @staticmethod
    def _extract_pdf(path: str) -> str:
        text = ""
        with fitz.open(path) as doc:
            for page in doc:
                text += page.get_text()
        return text

    @staticmethod
    def _extract_docx(path: str) -> str:
        doc = Document(path)
        return "\n".join(p.text for p in doc.paragraphs if p.text)

    @staticmethod
    def _extract_excel(path: str) -> str:
        sheets = pd.read_excel(path, sheet_name=None)
        text = ""
        for sheet, df in sheets.items():
            text += df.fillna("").to_string(index=False)
        return text

    @staticmethod
    def _clean(text: str) -> str:
        return " ".join(line.strip() for line in text.splitlines() if line.strip())