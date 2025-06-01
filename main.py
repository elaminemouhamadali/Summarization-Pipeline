# test_parser.py

from pathlib import Path
from src.parser import Parser

file_path = Path('data/raw/Mouhamad-Elamine-Resume.pdf')

# For basic flat text
parser_basic = Parser(use_unstructured=False)
flat_text = parser_basic.parse(file_path)
print("Flat Text (first 1000 chars):")
print(flat_text[:])

# For structured elements
parser_structured = Parser(use_unstructured=True)
structured_content = parser_structured.parse(file_path)
print("\nStructured Elements (first 5):")
for category, text in structured_content[:50]:
    print(f"[{category}]: {text[:100]}")
