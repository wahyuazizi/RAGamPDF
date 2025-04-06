import os
from langchain_community.document_loaders import PyMuPDFLoader

class PDFLoader:
    """
    Kelas PDFLoader untuk memuat dan memproses file PDF dari direktori tertentu.
    """
    def __init__(self, base_dir: str = "data"):
        """
        Inisialisasi PDFLoader dengan direktori dasar.        
        Args:
            base_dir (str): direktori dasar tempat file PDF berada. Defaultnya adalah "data".
        """
        self.base_dir = base_dir
    
    def cari_data(self):
        """
        melakukan traversal ke seluruh direktori dan subdirektori yang ada di dalam folder data

        Returns:
            list: berisi path lengkap ke semua file PDF di dalam folder data dan subfoldernya.
        """
        list_pdfs = []
        for root, _, files in os.walk(self.base_dir):
            for file in files:
                if file.endswith('.pdf'):
                    list_pdfs.append(os.path.join(root, file))

        return list_pdfs
    
    def load_data(self):
        """
        muat dan proses file PDF dengan library PyMuPDF (pymupdf).

        Returns:
            list: berisi konten semua halaman dari seluruh file PDF yang ditemukan.
        """

        list_docs = []
        # list_pdfs = self.cari_data()
        for pdf in self.cari_data():
            loader = PyMuPDFLoader(pdf)
            pages = loader.load()
            list_docs.extend(pages)
            
        return list_docs