from pathlib import Path
from typing import List
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document

try:
    from src.app.paths import PDF_DIR
except ImportError:
    PDF_DIR = Path(__file__).resolve().parents[3] / "data" / "pdfs"

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
        separators=["\n\n", "\n", " ", ""]
    )
    return text_splitter.split_documents(docs)

if __name__ == "__main__":
    print(f"Loading PDFs from {PDF_DIR}")
    raw_docs = load_pdf(PDF_DIR)
    print(f"Loaded {len(raw_docs)} documents.")
    chunked_docs = chunk_documents(raw_docs)
    print(f"Chunked into {len(chunked_docs)} documents.")

    # Print a sample chunk for verification
    for i, d in enumerate(chunked_docs[:2], start=1):
        src = d.metadata.get("source", "unbekannt")
        page = d.metadata.get("page", "?")
        preview = d.page_content.replace("\n", " ")[:220]
        print(f"\nChunk {i} — Quelle: {src}, Seite: {page}\n{preview} ...")