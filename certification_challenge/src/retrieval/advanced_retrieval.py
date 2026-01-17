"""
Advanced retrieval system for student loan assistant.
Implements multiple retrieval strategies with evaluation capabilities.
"""

import os
from typing import List, Dict, Any, Optional
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from langchain_community.retrievers import BM25Retriever
from langchain.retrievers.contextual_compression import ContextualCompressionRetriever
from langchain_cohere import CohereRerank
from langchain.retrievers.ensemble import EnsembleRetriever
from langchain_core.documents import Document
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams


class AdvancedRetrievalSystem:
    """Advanced retrieval system with multiple strategies."""
    
    def __init__(self, 
                 openai_api_key: Optional[str] = None,
                 cohere_api_key: Optional[str] = None):
        """
        Initialize the advanced retrieval system.
        
        Args:
            openai_api_key: OpenAI API key for embeddings
            cohere_api_key: Cohere API key for reranking
        """
        self.openai_api_key = openai_api_key or os.getenv("OPENAI_API_KEY")
        self.cohere_api_key = cohere_api_key or os.getenv("COHERE_API_KEY")
        
        # Initialize components
        self.embeddings = None
        self.vector_store = None
        self.vector_retriever = None
        self.bm25_retriever = None
        self.ensemble_retriever = None
        self.compression_retriever = None
        
        # Setup embeddings
        if self.openai_api_key:
            self.embeddings = OpenAIEmbeddings(
                model="text-embedding-3-small",
                openai_api_key=self.openai_api_key
            )
    
    def setup_vector_store(self, documents: List[Document], collection_name: str = "student_loans"):
        """Setup Qdrant vector store with documents."""
        if not self.embeddings:
            raise ValueError("OpenAI API key required for vector store setup")
        
        # Create Qdrant client
        client = QdrantClient(":memory:")
        
        # Create collection
        client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(size=1536, distance=Distance.COSINE)
        )
        
        # Create vector store
        self.vector_store = QdrantVectorStore(
            client=client,
            collection_name=collection_name,
            embeddings=self.embeddings
        )
        
        # Add documents
        if documents:
            self.vector_store.add_documents(documents)
        
        # Create retriever
        self.vector_retriever = self.vector_store.as_retriever(
            search_kwargs={"k": 5}
        )
    
    def setup_bm25_retriever(self, documents: List[Document]):
        """Setup BM25 retriever."""
        self.bm25_retriever = BM25Retriever.from_documents(documents)
        self.bm25_retriever.k = 5
    
    def setup_ensemble_retriever(self, k: int = 5):
        """Setup ensemble retriever combining vector and BM25."""
        if not self.vector_retriever or not self.bm25_retriever:
            raise ValueError("Both vector and BM25 retrievers must be set up first")
        
        self.ensemble_retriever = EnsembleRetriever(
            retrievers=[self.vector_retriever, self.bm25_retriever],
            weights=[0.7, 0.3]
        )
    
    def setup_compression_retriever(self, base_retriever, k: int = 5):
        """Setup contextual compression retriever with Cohere rerank."""
        if not self.cohere_api_key:
            print("Warning: Cohere API key not provided, skipping compression retriever")
            return
        
        try:
            compressor = CohereRerank(
                cohere_api_key=self.cohere_api_key,
                model="rerank-v3.5"
            )
            
            self.compression_retriever = ContextualCompressionRetriever(
                base_compressor=compressor,
                base_retriever=base_retriever
            )
        except Exception as e:
            print(f"Warning: Failed to setup compression retriever: {e}")
    
    def retrieve_vector(self, query: str, k: int = 5) -> List[Document]:
        """Retrieve documents using vector similarity."""
        if not self.vector_retriever:
            return []
        return self.vector_retriever.get_relevant_documents(query)
    
    def retrieve_bm25(self, query: str, k: int = 5) -> List[Document]:
        """Retrieve documents using BM25."""
        if not self.bm25_retriever:
            return []
        return self.bm25_retriever.get_relevant_documents(query)
    
    def retrieve_ensemble(self, query: str, k: int = 5) -> List[Document]:
        """Retrieve documents using ensemble method."""
        if not self.ensemble_retriever:
            return []
        return self.ensemble_retriever.get_relevant_documents(query)
    
    def retrieve_compression(self, query: str, k: int = 5) -> List[Document]:
        """Retrieve documents using contextual compression."""
        if not self.compression_retriever:
            return []
        return self.compression_retriever.get_relevant_documents(query)
    
    def compare_retrieval_methods(self, query: str) -> Dict[str, List[Document]]:
        """Compare all retrieval methods for a given query."""
        results = {}
        
        # Test each method
        methods = {
            "vector": self.vector_retriever,
            "bm25": self.bm25_retriever,
            "ensemble": self.ensemble_retriever,
            "compression": self.compression_retriever
        }
        
        for method_name, retriever in methods.items():
            if retriever:
                try:
                    docs = retriever.get_relevant_documents(query)
                    results[method_name] = docs
                except Exception as e:
                    results[method_name] = []
                    print(f"Error with {method_name}: {e}")
            else:
                results[method_name] = []
        
        return results
    
    def get_retrieval_summary(self) -> Dict[str, Any]:
        """Get summary of available retrieval methods."""
        return {
            "vector_available": self.vector_retriever is not None,
            "bm25_available": self.bm25_retriever is not None,
            "ensemble_available": self.ensemble_retriever is not None,
            "compression_available": self.compression_retriever is not None,
            "total_methods": sum([
                self.vector_retriever is not None,
                self.bm25_retriever is not None,
                self.ensemble_retriever is not None,
                self.compression_retriever is not None
            ])
        }


if __name__ == "__main__":
    # Example usage
    retrieval_system = AdvancedRetrievalSystem()
    print("Advanced retrieval system initialized")
    print(f"Status: {retrieval_system.get_retrieval_summary()}") 