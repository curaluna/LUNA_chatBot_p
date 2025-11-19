from pathlib import Path
from typing import List
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document


PDF_DIR = Path(__file__).resolve().parents[4] / "data" / "pdfs"

CHUNK_SIZE = 800
CHUNK_OVERLAP = 150


def load_pdf(file_path: Path) -> List[Document]:
    """Load a PDF file and return its pages as a list of Document objects."""
    docs: List[Document] = []
    for pdf_file in file_path.glob("*.pdf"):
        loader = PyPDFLoader(str(pdf_file))
        docs.extend(loader.load_and_split())

    for d in docs:
        if d.metadata["source"] != "":
            d.metadata["title"] = d.metadata["source"].rsplit("/", 1)[-1]
            print(
                f"Source: \033[33m{d.metadata['source']}\033[0m  converted to Title: \033[32m{d.metadata['title']}\033[0m ",
            )
            d.metadata["source"] = ""
            print("removed \033[31msource\033[0m from metadata", end="\n\n")
        else:
            raise Exception(
                "\033[31mThere is likely a file with no source provided in its metadata. Check the PyPdfLoader in document_loader.py\033[0m "
            )
    return docs


def chunk_documents(docs: List[Document]) -> List[Document]:
    """Chunk documents into smaller pieces."""
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
    )
    return text_splitter.split_documents(docs)


def get_chunked_documents():
    return chunk_documents(load_pdf(PDF_DIR))
