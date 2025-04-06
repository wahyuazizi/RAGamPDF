"""
Test untuk PDFLoader
"""
import os
from io import BytesIO
import pytest
from reportlab.pdfgen import canvas
from src.rag_llm.data.loader import PDFLoader

def generate_pdf_content(text: str) -> bytes:
    """Generate PDF bytes dengan konten teks sederhana."""
    buffer = BytesIO()
    c = canvas.Canvas(buffer)
    c.drawString(100, 750, text)  # Tambahkan teks ke PDF
    c.save()
    buffer.seek(0)
    return buffer.getvalue()


@pytest.fixture
def setup_test_dir(tmp_path):
    """
    Fixture untuk menyiapkan direktori sementara dengan file PDF dummy.
    Menggunakan pytest untuk membuat direktori sementara.
    Args:
        tmp_path (Path): direktori sementara yang dibuat oleh pytest.
    Returns:
        str: path ke direktori sementara yang berisi file PDF dummy.
    
    """
    # Buat temp directory untuk file PDF
    test_dir = tmp_path / "data"
    test_dir.mkdir(parents=True, exist_ok=True)

    # Buat file PDF dummy
    (test_dir / "test.pdf").write_bytes(generate_pdf_content("Test PDF content"))
    
    # Buat subfolder dengan file PDF dummy
    subfolder = test_dir / "subfolder"
    subfolder.mkdir(parents=True, exist_ok=True)

    (subfolder / "test2.pdf").write_bytes(generate_pdf_content("Test PDF content in subfolder"))

    return str(test_dir)

def test_cari_data(setup_test_dir):
    """
    Test untuk memastikan metode cari_data menemukan semua file PDF di dalam folder data dan subfoldernya.
    """
    # Setup test directory

    data_dir = setup_test_dir
    loader = PDFLoader(data_dir)

    # Panggil metode cari_data
    pdf_paths = loader.cari_data()

    # Pastikan semua file PDF ditemukan
    expected_files = [
        os.path.join(data_dir, "test.pdf"),
        os.path.join(data_dir, "subfolder", "test2.pdf")
    ]

    assert sorted(pdf_paths) == sorted(expected_files)

def test_load_data(setup_test_dir):
    """
    Test untuk memastikan metode load_data memuat konten dari semua file PDF yang ditemukan.
    """
    # Setup test directory
    data_dir = setup_test_dir
    loader = PDFLoader(data_dir)

    # Panggil metode load_data
    docs = loader.load_data()

    # Pastikan konten dari file PDF dimuat
    assert len(docs) == 2

    # Verifikasi konten teks
    assert "Test PDF content" in docs[0].page_content
    assert "Test PDF content in subfolder" in docs[1].page_content

def test_load_data_empty_dir(tmp_path):
    # Buat temp dir tanpa file PDf
    empty_dir = tmp_path / "empty_data"
    empty_dir.mkdir(parents=True, exist_ok=True)

    loader = PDFLoader(empty_dir)
    
    # Panggil metode cari data
    pdfs_found = loader.cari_data()
    assert pdfs_found == []

    # Panggil metode load_data
    docs = loader.load_data()
    assert docs == []

