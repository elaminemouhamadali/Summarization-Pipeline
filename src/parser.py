# src/parser.py

from pathlib import Path
from typing import List, Tuple, Union

try:
    from unstructured.partition.pdf import partition_pdf
    from unstructured.partition.docx import partition_docx
    from unstructured.documents.elements import Element
    UNSTRUCTURED_AVAILABLE = True
except ImportError:
    UNSTRUCTURED_AVAILABLE = False

import pymupdf  # PyMuPDF
import docx

class Parser:
    def __init__(self, use_unstructured: bool = False):
        if use_unstructured and not UNSTRUCTURED_AVAILABLE:
            raise ImportError("unstructured library not installed. Install it or set use_unstructured=False.")
        self.use_unstructured = use_unstructured

    def parse(self, file_path: Path) -> Union[str, List[Tuple[str, str]]]:
        ext = file_path.suffix.lower()
        if self.use_unstructured:
            if ext == ".pdf":
                return self._structured_parse_pdf(file_path)
            elif ext == ".docx":
                return self._structured_parse_docx(file_path)
            else:
                raise ValueError(f"Unsupported file type for structured parsing: {ext}")
        else:
            if ext == ".pdf":
                return self._basic_parse_pdf(file_path)
            elif ext == ".docx":
                return self._basic_parse_docx(file_path)
            else:
                raise ValueError(f"Unsupported file type for basic parsing: {ext}")

    def _basic_parse_pdf(self, file_path: Path) -> str:
        text = ""
        with pymupdf.open(file_path) as pdf:
            for page in pdf:
                text += page.get_text()
        return text

    def _basic_parse_docx(self, file_path: Path) -> str:
        doc = docx.Document(file_path)
        full_text = [para.text for para in doc.paragraphs]
        return '\n'.join(full_text)

    def _structured_parse_pdf(self, file_path: Path) -> List[Tuple[str, str]]:
        elements = partition_pdf(filename=file_path)
        return [(el.category, el.text) for el in elements]

    def _structured_parse_docx(self, file_path: Path) -> List[Tuple[str, str]]:
        elements = partition_docx(filename=file_path)
        return [(el.category, el.text) for el in elements]
