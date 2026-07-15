"""resume_text_extractor.py
Extract plain text from a resume PDF or DOCX file and save it to a temporary
.text file.

Usage:
    python resume_text_extractor.py /path/to/resume.pdf
    python resume_text_extractor.py /path/to/resume.docx

The script prints the path of the generated .txt file to stdout.
"""

import argparse
import os
import re
import sys
import tempfile
import zipfile
import xml.etree.ElementTree as ET


def _extract_text_from_docx(file_path: str) -> str:
    """Extract text from a DOCX file using only the standard library."""
    try:
        with zipfile.ZipFile(file_path) as docx_zip:
            with docx_zip.open('word/document.xml') as xml_file:
                tree = ET.parse(xml_file)
                root = tree.getroot()
                # Word namespace handling
                namespaces = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
                texts = [node.text
                         for node in root.iterfind('.//w:t', namespaces)
                         if node.text]
                return '\n'.join(texts)
    except Exception as e:
        raise RuntimeError(f"Failed to extract DOCX text: {e}") from e


def _extract_text_from_pdf(file_path: str) -> str:
    """Very naive PDF text extractor: pulls printable strings from the binary."""
    try:
        with open(file_path, 'rb') as f:
            data = f.read().decode('latin-1', errors='ignore')
        # Find sequences of printable characters (length >= 5)
        printable_strings = re.findall(r'[ -~]{5,}', data)
        return '\n'.join(printable_strings)
    except Exception as e:
        raise RuntimeError(f"Failed to extract PDF text: {e}") from e


def extract_text(file_path: str) -> str:
    """Dispatch to the appropriate extractor based on file extension."""
    _, ext = os.path.splitext(file_path.lower())
    if ext == '.docx':
        return _extract_text_from_docx(file_path)
    elif ext == '.pdf':
        return _extract_text_from_pdf(file_path)
    else:
        raise ValueError(f"Unsupported file extension '{ext}'. Only .pdf and .docx are allowed.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Extract text from a resume PDF/DOCX.")
    parser.add_argument('resume_path', help='Path to the PDF or DOCX resume file')
    args = parser.parse_args()

    try:
        text = extract_text(args.resume_path)
    except Exception as err:
        print(f"Error: {err}", file=sys.stderr)
        sys.exit(1)

    try:
        with tempfile.NamedTemporaryFile('w', delete=False, suffix='.txt', encoding='utf-8') as tmp_file:
            tmp_file.write(text)
            temp_path = tmp_file.name
        print(f"Extracted text saved to: {temp_path}")
    except Exception as err:
        print(f"Failed to write temporary file: {err}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()