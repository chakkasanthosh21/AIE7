#!/usr/bin/env python3
"""
🔍 RAG (Retrieval Augmented Generation) Complete Guide
=====================================================

This file covers RAG systems - how to make AI smarter by giving it access to 
external knowledge sources.

What you'll learn:
1. What is RAG and why it matters?
2. Core components of RAG systems
3. Building a simple RAG system
4. Advanced RAG techniques
5. Real-world applications
6. Evaluation and optimization

Author: AI Learning Guide
Date: 2024
"""

import json
import time
import math
import hashlib
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from abc import ABC, abstractmethod

# =============================================================================
# SECTION 1: WHAT IS RAG?
# =============================================================================

"""
RAG (Retrieval Augmented Generation) is a technique that combines the power of 
large language models with external knowledge sources to provide more accurate, 
up-to-date, and factual responses.

The Problem RAG Solves:
- Knowledge Cutoff: Models are trained on data up to a certain date
- Hallucination: Models can make up information that sounds plausible but is false
- No Access to Current Information: Can't access real-time data
- Limited Domain Knowledge: May not have expertise in specific areas

RAG Solution:
- Real-time Information: Access to current, up-to-date data
- Factual Accuracy: Ground responses in actual documents
- Domain Expertise: Can be specialized for any field
- Transparency: Can cite sources and show where information comes from

How RAG Works:
1. User Question → 2. Document Retrieval → 3. Context Assembly → 4. LLM Generation → 5. Response
"""

def print_rag_overview():
    """Print an overview of RAG systems"""
    print("🔍 RAG (Retrieval Augmented Generation) Overview")
    print("=" * 55)
    
    concepts = {
        "Definition": "Combines LLMs with external knowledge sources",
        "Problem Solved": "AI models lack current/domain-specific knowledge",
        "Key Benefit": "More accurate, factual, and up-to-date responses",
        "Core Process": "Retrieve → Augment → Generate",
        "Main Components": "Document Store, Embeddings, Vector DB, LLM"
    }
    
    for concept, description in concepts.items():
        print(f"📌 {concept}: {description}")
    
    print("\n💡 Think of RAG as giving an AI assistant access to a library!")

# =============================================================================
# SECTION 2: CORE COMPONENTS OF RAG
# =============================================================================

@dataclass
class Document:
    """Represents a document in the knowledge base"""
    id: str
    content: str
    metadata: Dict[str, Any]
    embedding: Optional[List[float]] = None

@dataclass
class SearchResult:
    """Represents a search result"""
    document: Document
    similarity_score: float
    rank: int

class SimpleEmbeddingGenerator:
    """Simple embedding generator for demonstration"""
    
    def __init__(self, dimension: int = 10):
        self.dimension = dimension
    
    def generate_embedding(self, text: str) -> List[float]:
        """Generate a simple embedding for text"""
        # This is a very simplified embedding - real embeddings are much more complex
        words = text.lower().split()
        embedding = [0.0] * self.dimension
        
        for word in words:
            # Simple hash-based embedding
            hash_val = hash(word) % self.dimension
            embedding[hash_val] += 1
        
        # Normalize
        norm = math.sqrt(sum(x * x for x in embedding))
        if norm > 0:
            embedding = [x / norm for x in embedding]
        
        return embedding
    
    def similarity(self, embedding1: List[float], embedding2: List[float]) -> float:
        """Calculate cosine similarity between two embeddings"""
        dot_product = sum(a * b for a, b in zip(embedding1, embedding2))
        return dot_product  # Already normalized, so this is cosine similarity

class SimpleVectorStore:
    """Simple in-memory vector store"""
    
    def __init__(self, embedding_generator: SimpleEmbeddingGenerator):
        self.embedding_generator = embedding_generator
        self.documents: List[Document] = []
        self.embeddings: List[List[float]] = []
    
    def add_document(self, document: Document):
        """Add a document to the vector store"""
        # Generate embedding if not provided
        if document.embedding is None:
            document.embedding = self.embedding_generator.generate_embedding(document.content)
        
        self.documents.append(document)
        self.embeddings.append(document.embedding)
    
    def search(self, query: str, top_k: int = 3) -> List[SearchResult]:
        """Search for similar documents"""
        query_embedding = self.embedding_generator.generate_embedding(query)
        
        # Calculate similarities
        similarities = []
        for i, doc_embedding in enumerate(self.embeddings):
            similarity = self.embedding_generator.similarity(query_embedding, doc_embedding)
            similarities.append((similarity, i))
        
        # Sort by similarity (descending)
        similarities.sort(reverse=True)
        
        # Return top-k results
        results = []
        for rank, (similarity, doc_index) in enumerate(similarities[:top_k]):
            result = SearchResult(
                document=self.documents[doc_index],
                similarity_score=similarity,
                rank=rank + 1
            )
            results.append(result)
        
        return results
    
    def get_document_count(self) -> int:
        """Get the number of documents in the store"""
        return len(self.documents)

def demonstrate_rag_components():
    """Demonstrate the core components of RAG"""
    print("\n🔧 Core Components of RAG")
    print("=" * 35)
    
    # Create embedding generator
    embedding_gen = SimpleEmbeddingGenerator(dimension=10)
    
    # Create vector store
    vector_store = SimpleVectorStore(embedding_gen)
    
    # Add some sample documents
    sample_documents = [
        Document(
            id="doc1",
            content="Python is a high-level programming language known for its simplicity and readability.",
            metadata={"source": "python_guide", "topic": "programming"}
        ),
        Document(
            id="doc2",
            content="Machine Learning is a subset of AI that allows computers to learn from data.",
            metadata={"source": "ai_guide", "topic": "machine_learning"}
        ),
        Document(
            id="doc3",
            content="Data Science combines statistics, programming, and domain expertise to extract insights.",
            metadata={"source": "data_science_guide", "topic": "data_science"}
        ),
        Document(
            id="doc4",
            content="Deep Learning uses neural networks with multiple layers to learn complex patterns.",
            metadata={"source": "deep_learning_guide", "topic": "deep_learning"}
        )
    ]
    
    # Add documents to vector store
    for doc in sample_documents:
        vector_store.add_document(doc)
    
    print(f"📚 Added {vector_store.get_document_count()} documents to vector store")
    
    # Test search
    test_queries = [
        "What is Python?",
        "How does machine learning work?",
        "Tell me about data science",
        "What is deep learning?"
    ]
    
    print("\n🔍 Testing Document Retrieval:")
    print("-" * 35)
    
    for query in test_queries:
        print(f"\nQuery: '{query}'")
        results = vector_store.search(query, top_k=2)
        
        for result in results:
            print(f"  Rank {result.rank}: {result.document.content[:50]}... (similarity: {result.similarity_score:.3f})")
    
    return vector_store

# =============================================================================
# SECTION 3: BUILDING A SIMPLE RAG SYSTEM
# =============================================================================

class SimpleRAGSystem:
    """A simple RAG system implementation"""
    
    def __init__(self, vector_store: SimpleVectorStore):
        self.vector_store = vector_store
        self.llm_simulator = SimpleLLMSimulator()
    
    def retrieve_documents(self, query: str, top_k: int = 3) -> List[Document]:
        """Retrieve relevant documents for a query"""
        search_results = self.vector_store.search(query, top_k)
        return [result.document for result in search_results]
    
    def create_context(self, documents: List[Document]) -> str:
        """Create context from retrieved documents"""
        context_parts = []
        for i, doc in enumerate(documents, 1):
            context_parts.append(f"Document {i}:\n{doc.content}\n")
        return "\n".join(context_parts)
    
    def generate_response(self, query: str, context: str) -> str:
        """Generate response using LLM with context"""
        prompt = f"""
Based on the following information, answer the question.

Information:
{context}

Question: {query}

Answer:
"""
        return self.llm_simulator.generate_response(prompt)
    
    def rag_pipeline(self, query: str) -> Tuple[str, List[Document]]:
        """Run the complete RAG pipeline"""
        # Step 1: Retrieve relevant documents
        documents = self.retrieve_documents(query)
        
        # Step 2: Create context
        context = self.create_context(documents)
        
        # Step 3: Generate response
        response = self.generate_response(query, context)
        
        return response, documents

class SimpleLLMSimulator:
    """Simple LLM simulator for demonstration"""
    
    def __init__(self):
        self.knowledge_base = {
            "python": "Python is a high-level programming language known for its simplicity and readability.",
            "machine learning": "Machine Learning is a subset of AI that allows computers to learn from data.",
            "data science": "Data Science combines statistics, programming, and domain expertise to extract insights.",
            "deep learning": "Deep Learning uses neural networks with multiple layers to learn complex patterns."
        }
    
    def generate_response(self, prompt: str) -> str:
        """Generate a response based on the prompt"""
        prompt_lower = prompt.lower()
        
        # Check if the prompt contains context
        if "information:" in prompt_lower and "question:" in prompt_lower:
            # Extract question from prompt
            question_start = prompt_lower.find("question:")
            if question_start != -1:
                question = prompt[question_start:].split("\n")[0].replace("Question:", "").strip()
                
                # Generate response based on question
                for topic, info in self.knowledge_base.items():
                    if topic in question.lower():
                        return f"Based on the provided information: {info}"
                
                return "Based on the provided information, I can help answer your question. Please provide more specific details."
        
        # Fallback response
        return "I'm here to help! Please ask me a specific question."

def demonstrate_simple_rag():
    """Demonstrate a simple RAG system"""
    print("\n🤖 Building a Simple RAG System")
    print("=" * 40)
    
    # Create vector store with sample data
    embedding_gen = SimpleEmbeddingGenerator()
    vector_store = SimpleVectorStore(embedding_gen)
    
    # Add sample documents
    documents = [
        Document(
            id="doc1",
            content="Python is a high-level programming language known for its simplicity and readability. It's widely used in AI and data science.",
            metadata={"source": "python_guide", "topic": "programming"}
        ),
        Document(
            id="doc2",
            content="Machine Learning is a subset of AI that allows computers to learn from data without being explicitly programmed.",
            metadata={"source": "ai_guide", "topic": "machine_learning"}
        ),
        Document(
            id="doc3",
            content="Data Science combines statistics, programming, and domain expertise to extract insights from data.",
            metadata={"source": "data_science_guide", "topic": "data_science"}
        )
    ]
    
    for doc in documents:
        vector_store.add_document(doc)
    
    # Create RAG system
    rag_system = SimpleRAGSystem(vector_store)
    
    # Test the RAG pipeline
    test_questions = [
        "What is Python?",
        "How does machine learning work?",
        "What is data science?",
        "What are the benefits of Python?"
    ]
    
    print("\n🔍 RAG Pipeline Test:")
    print("-" * 25)
    
    for question in test_questions:
        print(f"\nQuestion: {question}")
        
        # Run RAG pipeline
        response, retrieved_docs = rag_system.rag_pipeline(question)
        
        print(f"Response: {response}")
        print(f"Retrieved {len(retrieved_docs)} documents")
        
        for i, doc in enumerate(retrieved_docs, 1):
            print(f"  Doc {i}: {doc.content[:50]}...")
    
    return rag_system

# =============================================================================
# SECTION 4: ADVANCED RAG TECHNIQUES
# =============================================================================

class AdvancedRAGSystem(SimpleRAGSystem):
    """Advanced RAG system with additional features"""
    
    def __init__(self, vector_store: SimpleVectorStore):
        super().__init__(vector_store)
        self.query_history = []
        self.response_cache = {}
    
    def query_expansion(self, query: str) -> List[str]:
        """Expand query with related terms"""
        # Simple query expansion - in practice, you'd use more sophisticated methods
        expansions = [query]
        
        # Add variations
        if "what is" in query.lower():
            expansions.append(query.replace("what is", "explain"))
            expansions.append(query.replace("what is", "define"))
        
        if "how" in query.lower():
            expansions.append(query.replace("how", "what are the steps to"))
        
        return expansions
    
    def rerank_results(self, query: str, search_results: List[SearchResult]) -> List[SearchResult]:
        """Rerank search results based on relevance"""
        # Simple reranking - in practice, you'd use more sophisticated methods
        reranked = []
        
        for result in search_results:
            # Boost score if query terms appear in document
            query_terms = query.lower().split()
            doc_content = result.document.content.lower()
            
            term_matches = sum(1 for term in query_terms if term in doc_content)
            boosted_score = result.similarity_score + (term_matches * 0.1)
            
            reranked.append(SearchResult(
                document=result.document,
                similarity_score=boosted_score,
                rank=result.rank
            ))
        
        # Sort by boosted score
        reranked.sort(key=lambda x: x.similarity_score, reverse=True)
        
        # Update ranks
        for i, result in enumerate(reranked):
            result.rank = i + 1
        
        return reranked
    
    def multi_step_retrieval(self, query: str) -> List[Document]:
        """Multi-step retrieval process"""
        # Step 1: Initial retrieval
        initial_results = self.vector_store.search(query, top_k=5)
        
        # Step 2: Rerank results
        reranked_results = self.rerank_results(query, initial_results)
        
        # Step 3: Extract key terms from top results for additional search
        top_docs = [result.document for result in reranked_results[:2]]
        key_terms = self.extract_key_terms(top_docs)
        
        # Step 4: Additional retrieval with key terms
        additional_docs = []
        for term in key_terms[:3]:  # Use top 3 terms
            term_results = self.vector_store.search(term, top_k=2)
            additional_docs.extend([result.document for result in term_results])
        
        # Combine and deduplicate
        all_docs = top_docs + additional_docs
        unique_docs = []
        seen_ids = set()
        
        for doc in all_docs:
            if doc.id not in seen_ids:
                unique_docs.append(doc)
                seen_ids.add(doc.id)
        
        return unique_docs[:5]  # Return top 5 unique documents
    
    def extract_key_terms(self, documents: List[Document]) -> List[str]:
        """Extract key terms from documents"""
        # Simple key term extraction - in practice, you'd use NLP techniques
        all_text = " ".join([doc.content for doc in documents])
        words = all_text.lower().split()
        
        # Filter out common words
        common_words = {"the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for", "of", "with", "by"}
        key_terms = [word for word in words if word not in common_words and len(word) > 3]
        
        # Count frequency
        term_counts = {}
        for term in key_terms:
            term_counts[term] = term_counts.get(term, 0) + 1
        
        # Return most frequent terms
        sorted_terms = sorted(term_counts.items(), key=lambda x: x[1], reverse=True)
        return [term for term, count in sorted_terms[:5]]
    
    def advanced_rag_pipeline(self, query: str) -> Tuple[str, List[Document], Dict[str, Any]]:
        """Advanced RAG pipeline with multiple steps"""
        # Track query
        self.query_history.append({"query": query, "timestamp": time.time()})
        
        # Check cache
        cache_key = hashlib.md5(query.encode()).hexdigest()
        if cache_key in self.response_cache:
            cached = self.response_cache[cache_key]
            return cached["response"], cached["documents"], {"cached": True}
        
        # Multi-step retrieval
        documents = self.multi_step_retrieval(query)
        
        # Create context
        context = self.create_context(documents)
        
        # Generate response
        response = self.generate_response(query, context)
        
        # Cache result
        self.response_cache[cache_key] = {
            "response": response,
            "documents": documents,
            "timestamp": time.time()
        }
        
        metadata = {
            "documents_retrieved": len(documents),
            "cache_hit": False,
            "processing_time": time.time()
        }
        
        return response, documents, metadata

def demonstrate_advanced_rag():
    """Demonstrate advanced RAG techniques"""
    print("\n🚀 Advanced RAG Techniques")
    print("=" * 35)
    
    # Create vector store with more data
    embedding_gen = SimpleEmbeddingGenerator()
    vector_store = SimpleVectorStore(embedding_gen)
    
    # Add more comprehensive documents
    advanced_documents = [
        Document(
            id="doc1",
            content="Python is a high-level programming language known for its simplicity and readability. It's widely used in AI, data science, and web development.",
            metadata={"source": "python_guide", "topic": "programming"}
        ),
        Document(
            id="doc2",
            content="Machine Learning is a subset of AI that allows computers to learn from data without being explicitly programmed. It includes supervised, unsupervised, and reinforcement learning.",
            metadata={"source": "ai_guide", "topic": "machine_learning"}
        ),
        Document(
            id="doc3",
            content="Data Science combines statistics, programming, and domain expertise to extract insights from data. It involves data cleaning, analysis, and visualization.",
            metadata={"source": "data_science_guide", "topic": "data_science"}
        ),
        Document(
            id="doc4",
            content="Deep Learning uses neural networks with multiple layers to learn complex patterns in data. It's particularly effective for image recognition and natural language processing.",
            metadata={"source": "deep_learning_guide", "topic": "deep_learning"}
        ),
        Document(
            id="doc5",
            content="Natural Language Processing (NLP) is a branch of AI that helps computers understand and process human language. It's used in chatbots, translation, and text analysis.",
            metadata={"source": "nlp_guide", "topic": "nlp"}
        )
    ]
    
    for doc in advanced_documents:
        vector_store.add_document(doc)
    
    # Create advanced RAG system
    advanced_rag = AdvancedRAGSystem(vector_store)
    
    # Test advanced features
    test_queries = [
        "What is Python and how is it used in AI?",
        "Explain machine learning and its types",
        "How does data science work with programming?"
    ]
    
    print("\n🔍 Advanced RAG Pipeline Test:")
    print("-" * 35)
    
    for query in test_queries:
        print(f"\nQuery: {query}")
        
        # Test query expansion
        expansions = advanced_rag.query_expansion(query)
        print(f"Query expansions: {expractions}")
        
        # Test advanced pipeline
        response, documents, metadata = advanced_rag.advanced_rag_pipeline(query)
        
        print(f"Response: {response}")
        print(f"Retrieved {metadata['documents_retrieved']} documents")
        print(f"Cache hit: {metadata.get('cached', False)}")
        
        for i, doc in enumerate(documents, 1):
            print(f"  Doc {i}: {doc.content[:60]}...")
    
    return advanced_rag

# =============================================================================
# SECTION 5: RAG EVALUATION
# =============================================================================

@dataclass
class RAGEvaluation:
    """Evaluation results for RAG system"""
    retrieval_accuracy: float
    response_relevance: float
    factual_accuracy: float
    response_time: float
    overall_score: float

class RAGEvaluator:
    """Evaluate RAG system performance"""
    
    def __init__(self):
        self.test_questions = [
            "What is Python?",
            "How does machine learning work?",
            "What is data science?",
            "Explain deep learning",
            "What is natural language processing?"
        ]
        
        self.expected_keywords = {
            "What is Python?": ["programming", "language", "simplicity"],
            "How does machine learning work?": ["learn", "data", "algorithm"],
            "What is data science?": ["statistics", "programming", "insights"],
            "Explain deep learning": ["neural", "networks", "layers"],
            "What is natural language processing?": ["language", "text", "understanding"]
        }
    
    def evaluate_retrieval_accuracy(self, query: str, retrieved_docs: List[Document]) -> float:
        """Evaluate if relevant documents were retrieved"""
        expected_keywords = self.expected_keywords.get(query, [])
        
        if not retrieved_docs:
            return 0.0
        
        # Check if retrieved documents contain expected keywords
        relevant_docs = 0
        for doc in retrieved_docs:
            doc_content = doc.content.lower()
            keyword_matches = sum(1 for keyword in expected_keywords if keyword in doc_content)
            if keyword_matches > 0:
                relevant_docs += 1
        
        return relevant_docs / len(retrieved_docs)
    
    def evaluate_response_relevance(self, query: str, response: str) -> float:
        """Evaluate if response is relevant to query"""
        expected_keywords = self.expected_keywords.get(query, [])
        
        if not response:
            return 0.0
        
        response_lower = response.lower()
        keyword_matches = sum(1 for keyword in expected_keywords if keyword in response_lower)
        
        return min(1.0, keyword_matches / len(expected_keywords)) if expected_keywords else 0.0
    
    def evaluate_factual_accuracy(self, response: str) -> float:
        """Evaluate factual accuracy (simplified)"""
        # In practice, this would require human evaluation or fact-checking
        # For demonstration, we'll use a simple heuristic
        factual_indicators = ["based on", "according to", "research shows", "studies indicate"]
        response_lower = response.lower()
        
        factual_indicators_found = sum(1 for indicator in factual_indicators if indicator in response_lower)
        return min(1.0, factual_indicators_found / len(factual_indicators))
    
    def evaluate_rag_system(self, rag_system: SimpleRAGSystem) -> RAGEvaluation:
        """Evaluate a RAG system"""
        total_retrieval_accuracy = 0.0
        total_response_relevance = 0.0
        total_factual_accuracy = 0.0
        total_response_time = 0.0
        
        for query in self.test_questions:
            start_time = time.time()
            
            # Run RAG pipeline
            response, documents = rag_system.rag_pipeline(query)
            
            end_time = time.time()
            response_time = end_time - start_time
            
            # Evaluate metrics
            retrieval_accuracy = self.evaluate_retrieval_accuracy(query, documents)
            response_relevance = self.evaluate_response_relevance(query, response)
            factual_accuracy = self.evaluate_factual_accuracy(response)
            
            total_retrieval_accuracy += retrieval_accuracy
            total_response_relevance += response_relevance
            total_factual_accuracy += factual_accuracy
            total_response_time += response_time
        
        # Calculate averages
        num_queries = len(self.test_questions)
        avg_retrieval_accuracy = total_retrieval_accuracy / num_queries
        avg_response_relevance = total_response_relevance / num_queries
        avg_factual_accuracy = total_factual_accuracy / num_queries
        avg_response_time = total_response_time / num_queries
        
        # Calculate overall score
        overall_score = (avg_retrieval_accuracy + avg_response_relevance + avg_factual_accuracy) / 3
        
        return RAGEvaluation(
            retrieval_accuracy=avg_retrieval_accuracy,
            response_relevance=avg_response_relevance,
            factual_accuracy=avg_factual_accuracy,
            response_time=avg_response_time,
            overall_score=overall_score
        )
    
    def display_evaluation(self, evaluation: RAGEvaluation):
        """Display evaluation results"""
        print("\n📊 RAG System Evaluation Results:")
        print("=" * 40)
        print(f"Retrieval Accuracy: {evaluation.retrieval_accuracy:.3f}")
        print(f"Response Relevance: {evaluation.response_relevance:.3f}")
        print(f"Factual Accuracy: {evaluation.factual_accuracy:.3f}")
        print(f"Average Response Time: {evaluation.response_time:.3f}s")
        print(f"Overall Score: {evaluation.overall_score:.3f}")
        
        # Provide recommendations
        print("\n💡 Recommendations:")
        if evaluation.retrieval_accuracy < 0.7:
            print("  - Improve document retrieval by adding more relevant documents")
        if evaluation.response_relevance < 0.7:
            print("  - Improve response generation by refining prompts")
        if evaluation.factual_accuracy < 0.7:
            print("  - Add fact-checking mechanisms to responses")
        if evaluation.response_time > 2.0:
            print("  - Optimize system performance for faster responses")

def demonstrate_rag_evaluation():
    """Demonstrate RAG system evaluation"""
    print("\n📈 RAG System Evaluation")
    print("=" * 30)
    
    # Create and populate vector store
    embedding_gen = SimpleEmbeddingGenerator()
    vector_store = SimpleVectorStore(embedding_gen)
    
    # Add evaluation documents
    eval_documents = [
        Document(
            id="doc1",
            content="Python is a high-level programming language known for its simplicity and readability.",
            metadata={"source": "python_guide", "topic": "programming"}
        ),
        Document(
            id="doc2",
            content="Machine Learning is a subset of AI that allows computers to learn from data.",
            metadata={"source": "ai_guide", "topic": "machine_learning"}
        ),
        Document(
            id="doc3",
            content="Data Science combines statistics, programming, and domain expertise to extract insights.",
            metadata={"source": "data_science_guide", "topic": "data_science"}
        )
    ]
    
    for doc in eval_documents:
        vector_store.add_document(doc)
    
    # Create RAG system
    rag_system = SimpleRAGSystem(vector_store)
    
    # Create evaluator
    evaluator = RAGEvaluator()
    
    # Evaluate system
    evaluation = evaluator.evaluate_rag_system(rag_system)
    
    # Display results
    evaluator.display_evaluation(evaluation)
    
    return evaluation

# =============================================================================
# SECTION 6: REAL-WORLD RAG APPLICATIONS
# =============================================================================

def demonstrate_real_world_applications():
    """Demonstrate real-world RAG applications"""
    print("\n🌍 Real-World RAG Applications")
    print("=" * 35)
    
    applications = [
        {
            "name": "Customer Support Chatbot",
            "description": "Answer customer questions using company documentation",
            "benefits": ["24/7 availability", "Consistent responses", "Reduced wait times"],
            "implementation": "Use company FAQs, manuals, and policies as knowledge base"
        },
        {
            "name": "Research Assistant",
            "description": "Help researchers find and synthesize information from papers",
            "benefits": ["Access to vast knowledge", "Citation tracking", "Time savings"],
            "implementation": "Index academic papers, research databases, and publications"
        },
        {
            "name": "Legal Document Analysis",
            "description": "Search through legal documents and case law",
            "benefits": ["Precise retrieval", "Source attribution", "Legal compliance"],
            "implementation": "Index legal documents, case law, and regulations"
        },
        {
            "name": "Medical Information System",
            "description": "Provide medical information based on latest research",
            "benefits": ["Up-to-date information", "Evidence-based responses", "Patient education"],
            "implementation": "Index medical literature, clinical guidelines, and research papers"
        },
        {
            "name": "Educational Platform",
            "description": "Create AI tutors with access to course materials",
            "benefits": ["Personalized learning", "Comprehensive knowledge", "24/7 availability"],
            "implementation": "Index textbooks, course materials, and educational resources"
        }
    ]
    
    for i, app in enumerate(applications, 1):
        print(f"\n{i}. {app['name']}:")
        print(f"   Description: {app['description']}")
        print(f"   Benefits: {', '.join(app['benefits'])}")
        print(f"   Implementation: {app['implementation']}")
        print("-" * 50)

# =============================================================================
# SECTION 7: BUILDING YOUR OWN RAG SYSTEM
# =============================================================================

class RAGSystemBuilder:
    """Helper class to build custom RAG systems"""
    
    def __init__(self):
        self.embedding_generator = SimpleEmbeddingGenerator()
        self.vector_store = SimpleVectorStore(self.embedding_generator)
        self.rag_system = None
    
    def add_documents_from_text(self, documents_text: List[str], metadata: List[Dict] = None):
        """Add documents from text"""
        if metadata is None:
            metadata = [{"source": f"doc_{i}"} for i in range(len(documents_text))]
        
        for i, (text, meta) in enumerate(zip(documents_text, metadata)):
            doc = Document(
                id=f"doc_{i}",
                content=text,
                metadata=meta
            )
            self.vector_store.add_document(doc)
    
    def build_simple_rag(self) -> SimpleRAGSystem:
        """Build a simple RAG system"""
        self.rag_system = SimpleRAGSystem(self.vector_store)
        return self.rag_system
    
    def build_advanced_rag(self) -> AdvancedRAGSystem:
        """Build an advanced RAG system"""
        self.rag_system = AdvancedRAGSystem(self.vector_store)
        return self.rag_system
    
    def test_system(self, test_questions: List[str]):
        """Test the built RAG system"""
        if self.rag_system is None:
            print("Please build a RAG system first!")
            return
        
        print(f"\n🧪 Testing RAG System with {len(test_questions)} questions:")
        print("-" * 50)
        
        for question in test_questions:
            print(f"\nQuestion: {question}")
            
            if isinstance(self.rag_system, AdvancedRAGSystem):
                response, documents, metadata = self.rag_system.advanced_rag_pipeline(question)
                print(f"Response: {response}")
                print(f"Documents retrieved: {len(documents)}")
                print(f"Cache hit: {metadata.get('cached', False)}")
            else:
                response, documents = self.rag_system.rag_pipeline(question)
                print(f"Response: {response}")
                print(f"Documents retrieved: {len(documents)}")

def demonstrate_rag_builder():
    """Demonstrate building a custom RAG system"""
    print("\n🔨 Building Your Own RAG System")
    print("=" * 35)
    
    # Create RAG builder
    builder = RAGSystemBuilder()
    
    # Add sample documents
    sample_documents = [
        "Python is a versatile programming language used in web development, data science, and AI.",
        "Machine learning algorithms can be supervised, unsupervised, or reinforcement learning.",
        "Data science involves collecting, cleaning, analyzing, and visualizing data to extract insights.",
        "Deep learning uses neural networks with multiple layers to solve complex problems.",
        "Natural language processing helps computers understand and generate human language."
    ]
    
    metadata = [
        {"topic": "programming", "difficulty": "beginner"},
        {"topic": "machine_learning", "difficulty": "intermediate"},
        {"topic": "data_science", "difficulty": "intermediate"},
        {"topic": "deep_learning", "difficulty": "advanced"},
        {"topic": "nlp", "difficulty": "intermediate"}
    ]
    
    builder.add_documents_from_text(sample_documents, metadata)
    
    # Build advanced RAG system
    rag_system = builder.build_advanced_rag()
    
    # Test the system
    test_questions = [
        "What is Python used for?",
        "How does machine learning work?",
        "What is data science?",
        "Explain deep learning"
    ]
    
    builder.test_system(test_questions)
    
    return builder

# =============================================================================
# MAIN EXECUTION
# =============================================================================

def main():
    """Main function to run all RAG demonstrations"""
    print("🔍 RAG (Retrieval Augmented Generation) Complete Guide")
    print("=" * 60)
    print("This file contains comprehensive examples and explanations for RAG systems.")
    print("Run individual functions to explore different concepts.\n")
    
    # Run all demonstrations
    print_rag_overview()
    demonstrate_rag_components()
    demonstrate_simple_rag()
    demonstrate_advanced_rag()
    demonstrate_rag_evaluation()
    demonstrate_real_world_applications()
    demonstrate_rag_builder()
    
    print("\n🎉 Congratulations! You've completed the RAG Systems section!")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Practice building RAG systems with your own data")
    print("2. Experiment with different embedding methods")
    print("3. Try advanced techniques like query expansion")
    print("4. Evaluate and optimize your RAG system")
    print("5. Explore the other Python files in this folder")
    
    print("\n💡 To build your own RAG system, use the RAGSystemBuilder class!")

if __name__ == "__main__":
    main() 