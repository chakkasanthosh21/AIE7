"""
Advanced retrieval system for student loan assistant.
Implements multiple retrieval strategies with evaluation capabilities.
"""

import os
from typing import List, Dict, Any, Optional
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from langchain.retrievers import BM25Retriever
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
        Initialize the retrieval system.
        
        Args:
            openai_api_key: OpenAI API key for embeddings
            cohere_api_key: Cohere API key for reranking
        """
        self.openai_api_key = openai_api_key or os.getenv("OPENAI_API_KEY")
        self.cohere_api_key = cohere_api_key or os.getenv("COHERE_API_KEY")
        
        # Initialize components
        self.embeddings = OpenAIEmbeddings(
            model="text-embedding-3-small",
            openai_api_key=self.openai_api_key
        )
        
        self.vector_store = None
        self.bm25_retriever = None
        self.ensemble_retriever = None
        self.compression_retriever = None
        
    def setup_vector_store(self, documents: List[Document], collection_name: str = "student_loans"):
        """
        Set up Qdrant vector store with documents.
        
        Args:
            documents: List of documents to index
            collection_name: Name of the collection
        """
        # Initialize Qdrant client
        client = QdrantClient(":memory:")
        
        # Create collection
        client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(size=1536, distance=Distance.COSINE),
        )
        
        # Create vector store
        self.vector_store = QdrantVectorStore(
            client=client,
            collection_name=collection_name,
            embedding=self.embeddings,
        )
        
        # Add documents
        self.vector_store.add_documents(documents)
        print(f"Added {len(documents)} documents to vector store")
        
    def setup_bm25_retriever(self, documents: List[Document]):
        """
        Set up BM25 retriever.
        
        Args:
            documents: List of documents for BM25 indexing
        """
        self.bm25_retriever = BM25Retriever.from_documents(documents)
        print("BM25 retriever initialized")
        
    def setup_ensemble_retriever(self, k: int = 5):
        """
        Set up ensemble retriever combining vector and BM25.
        
        Args:
            k: Number of documents to retrieve
        """
        if not self.vector_store or not self.bm25_retriever:
            raise ValueError("Vector store and BM25 retriever must be initialized first")
            
        vector_retriever = self.vector_store.as_retriever(search_kwargs={"k": k})
        
        self.ensemble_retriever = EnsembleRetriever(
            retrievers=[vector_retriever, self.bm25_retriever],
            weights=[0.7, 0.3]
        )
        print("Ensemble retriever initialized")
        
    def setup_compression_retriever(self, base_retriever, k: int = 5):
        """
        Set up contextual compression retriever with reranking.
        
        Args:
            base_retriever: Base retriever to compress
            k: Number of documents to retrieve
        """
        if not self.cohere_api_key:
            print("Cohere API key not found, skipping compression retriever")
            return
            
        compressor = CohereRerank(model="rerank-v3.5")
        self.compression_retriever = ContextualCompressionRetriever(
            base_compressor=compressor,
            base_retriever=base_retriever,
            search_kwargs={"k": k}
        )
        print("Compression retriever initialized")
        
    def retrieve_vector(self, query: str, k: int = 5) -> List[Document]:
        """
        Retrieve documents using vector similarity.
        
        Args:
            query: Search query
            k: Number of documents to retrieve
            
        Returns:
            List of retrieved documents
        """
        if not self.vector_store:
            raise ValueError("Vector store not initialized")
            
        retriever = self.vector_store.as_retriever(search_kwargs={"k": k})
        return retriever.get_relevant_documents(query)
        
    def retrieve_bm25(self, query: str, k: int = 5) -> List[Document]:
        """
        Retrieve documents using BM25.
        
        Args:
            query: Search query
            k: Number of documents to retrieve
            
        Returns:
            List of retrieved documents
        """
        if not self.bm25_retriever:
            raise ValueError("BM25 retriever not initialized")
            
        return self.bm25_retriever.get_relevant_documents(query)
        
    def retrieve_ensemble(self, query: str, k: int = 5) -> List[Document]:
        """
        Retrieve documents using ensemble method.
        
        Args:
            query: Search query
            k: Number of documents to retrieve
            
        Returns:
            List of retrieved documents
        """
        if not self.ensemble_retriever:
            raise ValueError("Ensemble retriever not initialized")
            
        return self.ensemble_retriever.get_relevant_documents(query)
        
    def retrieve_compression(self, query: str, k: int = 5) -> List[Document]:
        """
        Retrieve documents using compression with reranking.
        
        Args:
            query: Search query
            k: Number of documents to retrieve
            
        Returns:
            List of retrieved documents
        """
        if not self.compression_retriever:
            raise ValueError("Compression retriever not initialized")
            
        return self.compression_retriever.get_relevant_documents(query)
        
    def compare_retrieval_methods(self, query: str, k: int = 5) -> Dict[str, List[Document]]:
        """
        Compare different retrieval methods on the same query.
        
        Args:
            query: Search query
            k: Number of documents to retrieve
            
        Returns:
            Dictionary with results from each method
        """
        results = {}
        
        try:
            results["vector"] = self.retrieve_vector(query, k)
        except Exception as e:
            results["vector"] = f"Error: {str(e)}"
            
        try:
            results["bm25"] = self.retrieve_bm25(query, k)
        except Exception as e:
            results["bm25"] = f"Error: {str(e)}"
            
        try:
            results["ensemble"] = self.retrieve_ensemble(query, k)
        except Exception as e:
            results["ensemble"] = f"Error: {str(e)}"
            
        try:
            results["compression"] = self.retrieve_compression(query, k)
        except Exception as e:
            results["compression"] = f"Error: {str(e)}"
            
        return results
        
    def get_retrieval_summary(self) -> Dict[str, Any]:
        """
        Get summary of available retrieval methods.
        
        Returns:
            Dictionary with retrieval method status
        """
        return {
            "vector_store": self.vector_store is not None,
            "bm25_retriever": self.bm25_retriever is not None,
            "ensemble_retriever": self.ensemble_retriever is not None,
            "compression_retriever": self.compression_retriever is not None,
            "cohere_available": bool(self.cohere_api_key)
        }


if __name__ == "__main__":
    # Example usage
    retrieval_system = AdvancedRetrievalSystem()
    print("Advanced retrieval system initialized")
    print(f"Status: {retrieval_system.get_retrieval_summary()}") 