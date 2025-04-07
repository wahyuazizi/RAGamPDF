"""
    Embeddings dan retrieval
"""

import os
from typing import List, Optional
from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.schema import Document
from rag_llm.utils.config import load_config

class FAISSRetriever:
    """
        Class untuk embedding dan retrieval
    """

    def __init__(self, embedding_model: str = "nomic-embed-text"):
        self.config = load_config()
        self.embedding_model = OllamaEmbeddings(
            model=embedding_model,
            base_url=self.config['ollama']['base_url']
        )
        self.vector_store : Optional[FAISS] = None

    def create_index(self, documents: List[Document]):
        """
        Mmembuat index dari dokumen
        """

        if not documents:
            raise ValueError("Tidak ada value yang diberikan")
        
        self.vector_store = FAISS.from_documents(
            documents=documents,
            embedding=self.embedding_model
        )

        return self.vector_store
    
    def save_index(self, index_name: str="index"):
        """
        Menyimpan index ke dalam file
        """

        if not self.vector_store:
            raise ValueError("Index belum dibuat")
        
        save_path = os.path.join(self.config['data_paths']['processed'], index_name)

        self.vector_store.save_local(save_path)

    def load_index(self, index_name: str="index"):
        """
        Memuat index dari folder data/processed
        """

        load_path = os.path.join(self.config['data_paths']['processed'], index_name)

        if not os.path.exists(load_path):
            raise ValueError(f"Index {index_name} tidak ditemukan")
        
        self.vector_store = FAISS.load_local(
            folder_path=load_path,
            embeddings=self.embedding_model,
            allow_dangerous_deserialization=True
        )

        return self.vector_store
    
    def get_retriever(self, search_type: str="mmr", k: int=5):
        """
        membuat retriever untuk RAG pipeline
        """

        if not self.vector_store:
            raise ValueError("Index belum dibuat")
        
        return self.vector_store.as_retriever(
            search_type=search_type,
            search_kwargs={
                "k": k,
                "fetch_k": k * 20,
                "lambda_mult": 1
                           }
        )
    



