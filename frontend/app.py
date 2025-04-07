
import streamlit as st
from rag_llm.core import RAGPipeline
import time
import os
from rag_llm.utils.config import load_config

# Konfigurasi tampilan
st.set_page_config(
    page_title="RAGamPDF - DocumentAI with RAG",
    page_icon="📚",
    layout="centered"
)

def init_session_state():
    """
    Inisialisasi state session
    """
    if 'pipeline' not in st.session_state:
        st.session_state.pipeline = None
    if 'processed' not in st.session_state:
        st.session_state.processed = False

def sidebar_config():
    """Sidebar untuk konfigurasi"""

    with st.sidebar:
        st.header("System Configuration")

        # Model selection
        model_options = ["llama3.2:1b"]
        selected_model = st.selectbox(
            "LLM Model",
            model_options,
            index=0
        )

        with st.expander("Advanced Settings"):
            chunk_size = st.slider("Chunk Size", 256, 2048, 1024)
            chunk_overlap = st.slider("Chunk Overlap", 0, 512, 64)
            # search_depth = st.slider("Search Depth", 1, 10, 3)

    return{
        "model": selected_model,
        "chunk_size": chunk_size,
        "chunk_overlap": chunk_overlap,
        "search_depth": search_depth
    }

def document_upload(full_config):
    """Komponen upload dan processing dokumen"""
    st.header("📤 Document Processing")

    uploaded_files = st.file_uploader(
        "Upload PDF docs",
        type=["pdf"],
        accept_multiple_files=True
    )

    if uploaded_files:
        # Simpan file ke folder data/raw
        raw_dir = "data/raw"
        os.makedirs(raw_dir, exist_ok=True)

        for file in uploaded_files:
            file_path = os.path.join(raw_dir, file.name)
            with open(file_path, 'wb') as f:
                f.write(file.getbuffer())

        # Tombol processing
        if st.button("🚀 Process Documents"):
            with st.spinner("Processing documents..."):
                start_time = time.time()

                try:
                    # Inisialisasi pipeline
                    st.session_state.pipeline = RAGPipeline(full_config)
                    st.session_state.pipeline.process_documents()

                    # Update status
                    st.session_state.processed = True
                    processing_time = time.time() - start_time

                    st.success(f"✅ Processed {len(uploaded_files)} documents in {processing_time:.2f} seconds")
                    st.balloons()
                except Exception as e:
                    st.error(f"❌ Error processing documents: {str(e)}")

def qa_interface():
    """Interface tanya jawab"""
    st.header("❓ Tanya dokumenmu")

    question = st.text_input(
        "Masukkan pertanyaan:",
        placeholder="...",
        disabled=not st.session_state.processed
    )

    if question and st.session_state.processed:
        with st.spinner("Analyzing documents..."):
            try:
                # Get answer
                answer = st.session_state.pipeline.query(question)

                # Tampilkan jawaban
                st.subheader("📝 Answer")
                st.markdown(f"```\n{answer}\n```")

                # # Tampilkan resource
                # with st.expander("🔍 View Sources"):
                #     st.write("Relevant socument exceprts:")
            except Exception as e:
                st.error(f"❌ Error processing documents: {str(e)}")

def main():
    """Main app layout"""

    init_session_state()

    st.title("📚 RAGamPDF")
    st.markdown("**AI Powered Document Analysis**")

    # Sidebar config
    config = sidebar_config()
    full_config = {
        **load_config(),
        **config
    }

    # Inisialisasi pipeline dengna config
    if st.session_state.pipeline is None:
        st.session_state.pipeline = RAGPipeline(full_config)

    # Main content
    document_upload(full_config)
    qa_interface()

if __name__=="__main__":
    main()