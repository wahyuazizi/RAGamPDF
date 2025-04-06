
from src.rag_llm.data.splitter import PDFChunker
from langchain.schema import Document
#Test untuk memastikan metode load_data memuat konten dari semua file PDF.

def test_split_text():
    """
    Test untuk memastikan metode split_text membagi teks menjadi potongan-potongan kecil.
    """
    
    # Setup PDFChunker
    chunker = PDFChunker(chunk_size=1000,
                         chunk_overlap=300)
    
    # Teks dummy untuk pengujian
    dummy_text = "Ini cuma teks dummy untuk testing. " * 100

    # Panggil metode split_text
    chunks = chunker.split_text(dummy_text)

    # Pastikan jumlah potongan yang dihasilkan sesuai dengan ekspektasi
    assert len(chunks) > 0
    
    # Pastikan setiap potongan memiliki panjang yang sesuai
    assert all(isinstance(chunk, str) for chunk in chunks)

def test_split_document():
    """
    Test untuk memastikan metode split_text membagi teks menjadi potongan-potongan kecil.
    """
    
    # Setup PDFChunker
    chunker = PDFChunker(chunk_size=30,
                         chunk_overlap=10)
    
    # Teks dummy untuk pengujian
    docs = [
    Document(page_content="Ini adalah halaman 1...", metadata={"source": "doc1.pdf"}),
    Document(page_content="Ini adalah halaman 2...", metadata={"source": "doc2.pdf"}),
]

    # Panggil metode split_text
    chunks = chunker.split_documents(docs)

    # Pastikan jumlah potongan yang dihasilkan sesuai dengan ekspektasi
    assert len(chunks) > 0
    # Pastikan setiap potongan memiliki panjang yang sesuai
    for chunk in chunks:
        assert len(chunk.page_content) <= chunker.chunk_size
        assert len(chunk.page_content) >= (chunker.chunk_size - chunker.chunk_overlap)
