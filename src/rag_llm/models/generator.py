
from typing import List, Dict, Any
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_ollama import ChatOllama
from langchain.schema import Document
from rag_llm.utils.config import load_config

class OllamaGenerator:
    def __init__(self):
        self.config = load_config()
        self.llm = self._init_llm()
        self.prompt_template = self._create_prompt()
        self.chain = self._build_chain()

    def _init_llm(self) -> ChatOllama:
        """
        Inisialisasi Ollama dengan config
        """
        return ChatOllama(
            model=self.config['ollama']['llm_model'],
            base_url=self.config['ollama']['base_url'],
            temperature=0.3,
            top_p=0.9,
            system="You are a helpful assistant specialized in fitness and nutrition."
            "always answer based on the provided context."
        )
    
    def _create_prompt(self) -> ChatPromptTemplate:
        """
        Buat template prompt yang terstruktur
        """

        return ChatPromptTemplate.from_template(
            """<|begin_of_text|>
            <|start_header_id|>system<|end_header_id|>
            You are an expert fitness coach. Answer the question using ONLY the provided context. 
            If unsure, say you don't know. Prioritize scientific evidence from context.
            
            Guidelines:
            - Use bullet points for lists
            - Highlight key terms in **bold**
            - Cite sources from metadata when possible<|eot_id|>
            
            <|start_header_id|>user<|end_header_id|>
            Context: {context}
            
            Question: {question}<|eot_id|>
            
            <|start_header_id|>assistant<|end_header_id|>
            Answer:"""
        )
    
    def _build_chain(self):
        """
        Build the RAG processing chain
        """
        return (
            {
                "context": RunnablePassthrough(),
                "question": RunnablePassthrough()
            }
            | self.prompt_template
            | self.llm
            | StrOutputParser()
        )
    
    def format_context(self, documents: List[Dict]) -> str:
        """
        Format retrieved doc ke context string
        """

        return "\n\n".join(
            f"Source: {doc.metadata.get('source', 'Unknown')}\n"
            f"Content: {doc.page_content}"
            for doc in documents
        )
    
    def generate(self, question: str, context: List[Document]) -> str:
        """
        Generate answer with source attribution
        """

        formatted_context = self.format_context(context)

        try:
            response = self.chain.invoke({
                "question": question,
                "context": formatted_context
            }
            )

            # Tambah sumber sitasi
            sources = {
                doc.metadat.get('source', 'Unknown') for doc in context
            }
            if sources:
                response += "\n\n**Sources:**\n- " + "\n- ".join(sources)

                return response
            
        except Exception as e:
            return f"Error generating response: {str(e)}"
        
