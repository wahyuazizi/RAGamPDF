import pytest
from langchain.schema import Document
from rag_llm.models.retriever import FAISSRetriever

def test_index_creation():
    retriever = FAISSRetriever()
    test_docs = [Document(page_content="test content")]
    index = retriever.create_index(test_docs)

    assert index.index.ntotal == 1