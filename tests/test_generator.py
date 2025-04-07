import pytest
from langchain.schema import Document
from rag_llm.models.generator import OllamaGenerator

def test_generation_with_context():
    generator = OllamaGenerator()
    test_docs = [
        Document(
            page_content="BCAAs help reduce muscle soreness and improve recovery",
            metadata={"source": "supplement_guide.pdf"}
        )
    ]

    response = generator.generate(
        question="What are BCAA benefits?",
        context=test_docs
    )

    assert "BCAAs" in response
    assert "supplement_guide.pdf" in response