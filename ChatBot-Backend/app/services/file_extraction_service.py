import tempfile
import os

import fitz
from docx import Document
import pandas as pd


class FileTextExtractionService:

    @staticmethod
    def extract(file_bytes: bytes, filename: str) -> str:
        if not filename or "." not in filename:
            raise ValueError("Invalid file name")

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

            cleaned = FileTextExtractionService._clean(text)

            if not cleaned:
                raise ValueError("No readable text found in file")

            return cleaned

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
        return "\n".join(p.text for p in doc.paragraphs if p.text.strip())

    @staticmethod
    def _extract_excel(path: str) -> str:
        sheets = pd.read_excel(path, sheet_name=None)
        parts = []

        for sheet, df in sheets.items():
            df = df.fillna("")

            for _, row in df.iterrows():
                sentence = " | ".join(
                    f"{col.replace('_', ' ')}: {row[col]}"
                    for col in df.columns
                )
                parts.append(f"Sheet {sheet} record — {sentence}.")

        return "\n".join(parts)

    @staticmethod
    def _clean(text: str) -> str:
        return " ".join(line.strip() for line in text.splitlines() if line.strip())