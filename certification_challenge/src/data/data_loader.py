"""
Data loader for student loan documents and complaints data.
Handles loading and preprocessing of federal loan documentation.
"""

import os
import pandas as pd
from typing import List, Dict, Any
from langchain_community.document_loaders import DirectoryLoader, PyMuPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import Document


class StudentLoanDataLoader:
    """Loader for student loan related documents and data."""
    
    def __init__(self, data_path: str = "../04_Production_RAG/data"):
        """
        Initialize the data loader.
        
        Args:
            data_path: Path to the data directory containing loan documents
        """
        self.data_path = data_path
        self.documents = []
        self.complaints_data = None
        self.test_data = None
        
    def load_pdf_documents(self) -> List[Document]:
        """
        Load PDF documents from the data directory.
        
        Returns:
            List of Document objects
        """
        loader = DirectoryLoader(
            self.data_path, 
            glob="*.pdf", 
            loader_cls=PyMuPDFLoader
        )
        self.documents = loader.load()
        print(f"Loaded {len(self.documents)} PDF documents")
        return self.documents
    
    def load_complaints_data(self) -> pd.DataFrame:
        """
        Load student loan complaints data.
        
        Returns:
            DataFrame containing complaints data
        """
        complaints_path = os.path.join(self.data_path, "complaints.csv")
        if os.path.exists(complaints_path):
            self.complaints_data = pd.read_csv(complaints_path)
            print(f"Loaded {len(self.complaints_data)} complaints")
        else:
            print("Complaints file not found")
        return self.complaints_data
    
    def load_test_data(self) -> pd.DataFrame:
        """
        Load test questions and evaluation data.
        
        Returns:
            DataFrame containing test data
        """
        test_path = os.path.join(self.data_path, "student_loan_rag_test_data.csv")
        if os.path.exists(test_path):
            self.test_data = pd.read_csv(test_path)
            print(f"Loaded {len(self.test_data)} test questions")
        else:
            print("Test data file not found")
        return self.test_data
    
    def split_documents(self, chunk_size: int = 1000, chunk_overlap: int = 200) -> List[Document]:
        """
        Split documents into chunks for processing.
        
        Args:
            chunk_size: Size of each chunk
            chunk_overlap: Overlap between chunks
            
        Returns:
            List of split documents
        """
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
        )
        
        split_docs = text_splitter.split_documents(self.documents)
        print(f"Split {len(self.documents)} documents into {len(split_docs)} chunks")
        return split_docs
    
    def get_document_summary(self) -> Dict[str, Any]:
        """
        Get a summary of loaded documents.
        
        Returns:
            Dictionary with document statistics
        """
        summary = {
            "total_documents": len(self.documents),
            "total_complaints": len(self.complaints_data) if self.complaints_data is not None else 0,
            "total_test_questions": len(self.test_data) if self.test_data is not None else 0,
            "document_sources": list(set([doc.metadata.get('source', 'unknown') for doc in self.documents]))
        }
        return summary
    
    def load_all_data(self) -> Dict[str, Any]:
        """
        Load all available data sources.
        
        Returns:
            Dictionary containing all loaded data
        """
        print("Loading student loan data...")
        
        # Load all data sources
        documents = self.load_pdf_documents()
        complaints = self.load_complaints_data()
        test_data = self.load_test_data()
        
        # Split documents for processing
        split_docs = self.split_documents()
        
        # Create empty DataFrames if files don't exist
        if complaints is None:
            complaints = pd.DataFrame()
        if test_data is None:
            test_data = pd.DataFrame()
        
        return {
            "documents": documents,
            "split_documents": split_docs,
            "complaints": complaints,
            "test_data": test_data,
            "summary": self.get_document_summary()
        }


if __name__ == "__main__":
    # Example usage
    loader = StudentLoanDataLoader()
    data = loader.load_all_data()
    print("Data loading complete!")
    print(f"Summary: {data['summary']}") 