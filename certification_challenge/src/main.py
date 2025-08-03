"""
Main system integration for Student Loan Assistant.
Brings together all components: data loading, retrieval, agents, and evaluation.
"""

import os
import sys
from typing import Dict, Any, List
import json

# Add the src directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from data.data_loader import StudentLoanDataLoader
from retrieval.advanced_retrieval import AdvancedRetrievalSystem
from agents.research_agent import ResearchAgent
from agents.response_agent import ResponseAgent
from agents.supervisor_agent import SupervisorAgent
from evaluation.metrics import StudentLoanEvaluator


class StudentLoanAssistant:
    """Main system class that integrates all components."""
    
    def __init__(self, 
                 openai_api_key: str = None,
                 cohere_api_key: str = None,
                 data_path: str = "../04_Production_RAG/data"):
        """
        Initialize the Student Loan Assistant system.
        
        Args:
            openai_api_key: OpenAI API key
            cohere_api_key: Cohere API key for reranking
            data_path: Path to data directory
        """
        self.openai_api_key = openai_api_key or os.getenv("OPENAI_API_KEY")
        self.cohere_api_key = cohere_api_key or os.getenv("COHERE_API_KEY")
        self.data_path = data_path
        
        # Initialize components
        self.data_loader = None
        self.retrieval_system = None
        self.research_agent = None
        self.response_agent = None
        self.supervisor_agent = None
        self.evaluator = None
        
        # System state
        self.is_initialized = False
        self.system_data = {}
        
    def initialize_system(self) -> Dict[str, Any]:
        """
        Initialize all system components.
        
        Returns:
            Initialization status and summary
        """
        print("🚀 Initializing Student Loan Assistant System...")
        
        try:
            # 1. Load data
            print("📚 Loading student loan data...")
            self.data_loader = StudentLoanDataLoader(self.data_path)
            data_results = self.data_loader.load_all_data()
            self.system_data = data_results
            
            # 2. Set up retrieval system
            print("🔍 Setting up retrieval system...")
            self.retrieval_system = AdvancedRetrievalSystem(
                openai_api_key=self.openai_api_key,
                cohere_api_key=self.cohere_api_key
            )
            
            # Initialize retrieval methods
            split_docs = data_results["split_documents"]
            self.retrieval_system.setup_vector_store(split_docs)
            self.retrieval_system.setup_bm25_retriever(split_docs)
            self.retrieval_system.setup_ensemble_retriever()
            
            # 3. Set up agents
            print("🤖 Setting up AI agents...")
            ensemble_retriever = self.retrieval_system.ensemble_retriever
            
            self.research_agent = ResearchAgent(ensemble_retriever)
            self.response_agent = ResponseAgent()
            self.supervisor_agent = SupervisorAgent(
                self.research_agent, 
                self.response_agent
            )
            
            # 4. Set up evaluator
            print("📊 Setting up evaluation system...")
            self.evaluator = StudentLoanEvaluator(self.openai_api_key)
            
            self.is_initialized = True
            
            initialization_summary = {
                "status": "success",
                "data_loaded": len(data_results["documents"]),
                "documents_chunked": len(data_results["split_documents"]),
                "complaints_loaded": len(data_results["complaints"]) if data_results["complaints"] is not None else 0,
                "test_questions": len(data_results["test_data"]) if data_results["test_data"] is not None else 0,
                "retrieval_methods": self.retrieval_system.get_retrieval_summary(),
                "agents_ready": True,
                "evaluator_ready": True
            }
            
            print("✅ System initialization complete!")
            return initialization_summary
            
        except Exception as e:
            print(f"❌ System initialization failed: {str(e)}")
            return {
                "status": "error",
                "error": str(e)
            }
            
    def process_student_query(self, query: str, student_context: str = "") -> Dict[str, Any]:
        """
        Process a student query through the complete system.
        
        Args:
            query: Student's question
            student_context: Additional context about the student
            
        Returns:
            Complete response with all metadata
        """
        if not self.is_initialized:
            return {"error": "System not initialized. Call initialize_system() first."}
            
        print(f"🎯 Processing query: {query}")
        
        try:
            # Process through the multi-agent workflow
            result = self.supervisor_agent.process_query(query, student_context)
            
            # Add system metadata
            result["system_metadata"] = {
                "query_processed": True,
                "timestamp": str(pd.Timestamp.now()),
                "system_version": "1.0.0"
            }
            
            return result
            
        except Exception as e:
            print(f"❌ Error processing query: {str(e)}")
            return {
                "error": str(e),
                "query": query,
                "final_response": "I apologize, but I encountered an error processing your query. Please try again or contact support."
            }
            
    def process_batch_queries(self, queries: List[str]) -> List[Dict[str, Any]]:
        """
        Process multiple queries in batch.
        
        Args:
            queries: List of student queries
            
        Returns:
            List of responses for each query
        """
        if not self.is_initialized:
            return [{"error": "System not initialized"} for _ in queries]
            
        print(f"📦 Processing batch of {len(queries)} queries...")
        
        results = self.supervisor_agent.process_batch_queries(queries)
        
        # Generate workflow report
        workflow_report = self.supervisor_agent.generate_workflow_report(results)
        
        return {
            "results": results,
            "workflow_report": workflow_report
        }
        
    def evaluate_system(self, test_queries: List[str] = None) -> Dict[str, Any]:
        """
        Evaluate the system performance.
        
        Args:
            test_queries: Optional list of test queries
            
        Returns:
            Comprehensive evaluation results
        """
        if not self.is_initialized:
            return {"error": "System not initialized"}
            
        print("🔍 Evaluating system performance...")
        
        # Use provided test queries or default ones
        if test_queries is None:
            test_queries = [
                "What are the eligibility requirements for federal student loans?",
                "How do I apply for a Direct Loan?",
                "What are the current interest rates for student loans?",
                "How do I repay my student loans?",
                "What happens if I can't make my loan payments?"
            ]
            
        # Process test queries
        batch_results = self.process_batch_queries(test_queries)
        responses = batch_results["results"]
        
        # Evaluate with custom metrics
        custom_evaluation = self.evaluator.evaluate_custom_metrics(test_queries, responses)
        
        # Combine all evaluation results
        all_evaluation_results = {
            "custom_metrics": custom_evaluation,
            "workflow_report": batch_results["workflow_report"]
        }
        
        # Generate comprehensive report
        evaluation_report = self.evaluator.generate_evaluation_report(all_evaluation_results)
        
        return evaluation_report
        
    def compare_retrieval_methods(self, query: str) -> Dict[str, Any]:
        """
        Compare different retrieval methods on a query.
        
        Args:
            query: Test query
            
        Returns:
            Comparison results
        """
        if not self.is_initialized:
            return {"error": "System not initialized"}
            
        print(f"🔍 Comparing retrieval methods for: {query}")
        
        comparison_results = self.retrieval_system.compare_retrieval_methods(query)
        
        # Analyze results
        analysis = {
            "query": query,
            "methods_compared": list(comparison_results.keys()),
            "document_counts": {
                method: len(docs) if isinstance(docs, list) else 0
                for method, docs in comparison_results.items()
            },
            "recommendation": self._recommend_retrieval_method(comparison_results)
        }
        
        return {
            "comparison_results": comparison_results,
            "analysis": analysis
        }
        
    def _recommend_retrieval_method(self, comparison_results: Dict[str, Any]) -> str:
        """Recommend the best retrieval method based on results."""
        valid_methods = {
            method: docs for method, docs in comparison_results.items()
            if isinstance(docs, list) and len(docs) > 0
        }
        
        if not valid_methods:
            return "No valid retrieval methods available"
            
        # Simple recommendation logic
        if "ensemble" in valid_methods:
            return "ensemble (combines vector and BM25 for best results)"
        elif "vector" in valid_methods:
            return "vector (semantic similarity)"
        elif "bm25" in valid_methods:
            return "bm25 (keyword-based)"
        else:
            return "compression (reranked results)"
            
    def get_system_status(self) -> Dict[str, Any]:
        """
        Get current system status and health.
        
        Returns:
            System status information
        """
        status = {
            "initialized": self.is_initialized,
            "components": {
                "data_loader": self.data_loader is not None,
                "retrieval_system": self.retrieval_system is not None,
                "research_agent": self.research_agent is not None,
                "response_agent": self.response_agent is not None,
                "supervisor_agent": self.supervisor_agent is not None,
                "evaluator": self.evaluator is not None
            }
        }
        
        if self.is_initialized:
            status["data_summary"] = self.system_data.get("summary", {})
            status["retrieval_status"] = self.retrieval_system.get_retrieval_summary()
            
        return status
        
    def save_system_state(self, filepath: str):
        """
        Save system state to file.
        
        Args:
            filepath: Path to save the state
        """
        state = {
            "system_status": self.get_system_status(),
            "data_summary": self.system_data.get("summary", {}),
            "timestamp": str(pd.Timestamp.now())
        }
        
        with open(filepath, 'w') as f:
            json.dump(state, f, indent=2)
            
        print(f"💾 System state saved to {filepath}")


def main():
    """Main function to demonstrate the system."""
    print("🎓 Student Loan Assistant - Certification Challenge")
    print("=" * 50)
    
    # Initialize the system
    assistant = StudentLoanAssistant()
    init_result = assistant.initialize_system()
    
    if init_result["status"] == "error":
        print(f"❌ Failed to initialize: {init_result['error']}")
        return
        
    print(f"✅ System initialized successfully!")
    print(f"📊 Data loaded: {init_result['data_loaded']} documents")
    
    # Example queries
    example_queries = [
        "What are the eligibility requirements for federal student loans?",
        "How do I apply for a Direct Loan?",
        "What are the current interest rates for student loans?"
    ]
    
    print("\n🧪 Testing system with example queries...")
    
    for i, query in enumerate(example_queries, 1):
        print(f"\n--- Query {i}: {query} ---")
        result = assistant.process_student_query(query)
        
        if "error" in result:
            print(f"❌ Error: {result['error']}")
        else:
            print(f"✅ Response generated successfully")
            print(f"📝 Response length: {len(result.get('final_response', ''))} characters")
            
    # Evaluate system
    print("\n📊 Evaluating system performance...")
    evaluation_results = assistant.evaluate_system()
    
    if "error" not in evaluation_results:
        summary = evaluation_results.get("evaluation_summary", {})
        print(f"📈 Overall Score: {summary.get('average_score', 0):.2f}")
        print(f"🎯 Passing Rate: {summary.get('passing_score', 0):.2%}")
        
    print("\n🎉 System demonstration complete!")


if __name__ == "__main__":
    import pandas as pd
    main() 