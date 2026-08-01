import re

from langchain_community.document_loaders import PyMuPDFLoader


def clean_text(text: str) -> str:

    text = text.replace("\n", " ")

    # Replace tabs with spaces
    text = text.replace("\t", " ")

    # Remove multiple spaces
    text = re.sub(r"[ ]{2,}", " ", text)

    # Remove excessive blank lines
    text = re.sub(r"\n{2,}", "\n", text)

    # Remove leading/trailing whitespace
    text = text.strip()

    return text


def load_pdf(file_path: str):
    loader = PyMuPDFLoader(file_path)
    documents = loader.load()

    # Clean every page
    for document in documents:
        document.page_content = clean_text(document.page_content)

    return documents