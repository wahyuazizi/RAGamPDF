
from rag_llm.data.loader import PDFLoader
from rag_llm.data.splitter import PDFChunker
from rag_llm.models.retriever import FAISSRetriever
from rag_llm.models.generator import OllamaGenerator
from rag_llm.utils.config import load_config

class RAGPipeline:
    def __init__(self, config: dict):
        self.config = config
        self.loader = PDFLoader(self.config['data_paths']['raw'])
        self.splitter = PDFChunker()
        self.retriever = FAISSRetriever()
        self.generator = OllamaGenerator(
            model_name=self.config['model']
        )

    def process_documents(self):
        # Load PDF
        raw_docs = self.loader.load_data()

        # Chunk dokumen
        chunks = self.splitter.split_documents(raw_docs)

        # Buat vector store
        self.retriever.create_index(chunks)
        self.retriever.save_index()

        return self
    
    def query(self, question: str):
        return self.generator.generate(
            question=question,
            context=self.retriever.get_retriever().invoke(question)
        )