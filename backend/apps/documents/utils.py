import pymupdf4llm


def extract_text_from_pdf(file_path: str) -> str:
    return pymupdf4llm.to_markdown(file_path)
