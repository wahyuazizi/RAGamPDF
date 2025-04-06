import os
from langchain_community.document_loaders import PyMuPDFLoader

class PDFLoader(PyMuPDFLoader):
    """
    Load PDF menggunakan PyMuPDFLoader dari Langchain community.
    """
    def __init__(self, file_path: str):
        """
        Inisialisasi PDFLoader dengan path file PDF.
        
        Args:
            file_path (str): path ke file PDF yang akan dimuat.
        """
        super().__init__(file_path)
        self.file_path = file_path
    
    def cari_data(self):
        """
        melakukan traversal ke seluruh direktori dan subdirektori yang ada di dalam folder data

        Returns:
            list: berisi path lengkap ke semua file PDF di dalam folder data dan subfoldernya.
        """
        list_pdfs = []
        for root, dirs, files in os.walk('data'):
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
        list_pdfs = self.cari_data()
        for pdf in list_pdfs:
            loader = PyMuPDFLoader(pdf)
            pages = loader.load()
            list_docs.extend(pages)

        return list_docs