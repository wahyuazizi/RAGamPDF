from rag_llm.core import RAGPipeline

pipeline = RAGPipeline().process_documents()
response = pipeline.query("Apa manfaat BCAA untuk fitness?")
print(response)