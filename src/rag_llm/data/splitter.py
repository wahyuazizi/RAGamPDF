"""
    Chunking dan Splitting
"""
from typing import List
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.schema import Document

class PDFChunker:
    """
    kelas PDFChuncker untuk membagi teks menjadi potongan-potongan kecil.
    """
    def __init__(self, chunk_size: int = 512, chunk_overlap: int = 64):
        """
        Inisialisasi PDFChunker dengan ukuran chunk dan overlap.
        
        Args:
            chunk_size (int): ukuran chunk dalam karakter. Defaultnya adalah 1000.)
            chunk_overlap (int): ukuran overlap antara chunk dalam karakter. Defaultnya adalah 300.
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def split_text(self, docs: str) -> List[str]:
        """
        Membagi teks menjadi potongan-potongan kecil dengan ukuran dan overlap yang ditentukan.
        
        Args:
            text (str): teks yang akan dibagi.
        Returns:
            list: daftar potongan teks yang telah dibagi.
        """
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
        )

        # Split teks menjadi potongan-potongan kecil
        chunks = text_splitter.split_text(docs)
        return chunks
    
    def split_documents(self, docs: List[Document]) -> List[Document]:
        """
        Split dokumen menjadi potongan-potongan kecil dengan ukuran dan overlap yang ditentukan.
        """
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
        )

        #  Split dokumen menjadi potongan-potongan kecil
        chunks = text_splitter.split_documents(docs)
        return chunks