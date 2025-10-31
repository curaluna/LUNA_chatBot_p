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
    return docs


def chunk_documents(docs: List[Document]) -> List[Document]:
    """Chunk documents into smaller pieces."""
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
    )
    return text_splitter.split_documents(docs)


chunked_documents = chunk_documents(load_pdf(PDF_DIR))
