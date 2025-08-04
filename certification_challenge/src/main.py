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

from .data.data_loader import StudentLoanDataLoader
from .retrieval.advanced_retrieval import AdvancedRetrievalSystem
from .agents.research_agent import ResearchAgent
from .agents.response_agent import ResponseAgent
from .agents.supervisor_agent import SupervisorAgent
from .evaluation.metrics import StudentLoanEvaluator


class StudentLoanAssistant:
    """Main system class that integrates all components."""
    
    def __init__(self, 
                 openai_api_key: str = None,
                 cohere_api_key: str = None,
                 tavily_api_key: str = None,
                 data_path: str = "../04_Production_RAG/data"):
        """
        Initialize the Student Loan Assistant system.
        
        Args:
            openai_api_key: OpenAI API key (optional, will use env var if not provided)
            cohere_api_key: Cohere API key (optional, for reranking)
            tavily_api_key: Tavily API key (optional, for web search)
            data_path: Path to the data directory
        """
        self.openai_api_key = openai_api_key
        self.cohere_api_key = cohere_api_key
        self.tavily_api_key = tavily_api_key
        self.data_path = data_path
        
        # Initialize components
        self.data_loader = None
        self.retrieval_system = None
        self.research_agent = None
        self.response_agent = None
        self.supervisor_agent = None
        self.evaluator = None
        
        # System state
        self.initialized = False
        self.data = {}
    
    def initialize_system(self) -> Dict[str, Any]:
        """Initialize all system components."""
        try:
            print(f"Initializing system with data path: {self.data_path}")
            
            # Load data
            self.data_loader = StudentLoanDataLoader(self.data_path)
            self.data = self.data_loader.load_all_data()
            
            print(f"Loaded {len(self.data.get('documents', []))} documents")
            
            # Initialize retrieval system
            self.retrieval_system = AdvancedRetrievalSystem(
                openai_api_key=self.openai_api_key,
                cohere_api_key=self.cohere_api_key
            )
            
            # Setup vector store and retrievers
            if self.data.get("documents"):
                print("Setting up vector store...")
                self.retrieval_system.setup_vector_store(self.data["documents"])
                print("Setting up BM25 retriever...")
                self.retrieval_system.setup_bm25_retriever(self.data["documents"])
                print("Setting up ensemble retriever...")
                self.retrieval_system.setup_ensemble_retriever()
                print("Setting up compression retriever...")
                self.retrieval_system.setup_compression_retriever(self.retrieval_system.vector_retriever)
            
            # Initialize agents
            print("Initializing agents...")
            self.research_agent = ResearchAgent(self.retrieval_system.ensemble_retriever)
            self.response_agent = ResponseAgent()
            self.supervisor_agent = SupervisorAgent(self.research_agent, self.response_agent)
            
            # Set up Tavily API key if provided
            if self.tavily_api_key:
                os.environ["TAVILY_API_KEY"] = self.tavily_api_key
            
            # Initialize evaluator
            print("Initializing evaluator...")
            self.evaluator = StudentLoanEvaluator(openai_api_key=self.openai_api_key)
            
            self.initialized = True
            print("System initialization complete!")
            
            return {
                "status": "success",
                "message": "System initialized successfully",
                "data_summary": {
                    "total_documents": len(self.data.get("documents", [])),
                    "total_complaints": len(self.data.get("complaints", [])),
                    "total_test_questions": len(self.data.get("test_data", []))
                }
            }
            
        except Exception as e:
            print(f"Error during initialization: {str(e)}")
            import traceback
            traceback.print_exc()
            return {
                "status": "error",
                "error": str(e),
                "message": "Failed to initialize system"
            }
    
    def process_student_query(self, query: str, student_context: str = "") -> Dict[str, Any]:
        """Process a student query through the multi-agent workflow."""
        if not self.initialized:
            return {"error": "System not initialized. Please call initialize_system() first."}
        
        try:
            # Process through supervisor agent
            result = self.supervisor_agent.process_query(query, student_context)
            
            return {
                "status": "success",
                "final_response": result.get("final_response", "No response generated."),
                "metadata": result.get("metadata", {}),
                "research_context": result.get("research_context", ""),
                "workflow_steps": result.get("workflow_steps", [])
            }
            
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "message": "Failed to process query"
            }
    
    def evaluate_system(self, test_queries: List[str] = None) -> Dict[str, Any]:
        """Evaluate the system performance."""
        if not self.initialized:
            return {"error": "System not initialized"}
        
        try:
            # Use test data if available, otherwise use provided queries
            if not test_queries and self.data.get("test_data"):
                test_queries = self.data["test_data"]["question"].tolist()[:10]  # Use first 10 questions
            
            if not test_queries:
                test_queries = [
                    "What are the eligibility requirements for federal student loans?",
                    "How do I apply for a Direct Loan?",
                    "What are the current interest rates for student loans?"
                ]
            
            # Process test queries
            responses = []
            for query in test_queries:
                result = self.process_student_query(query)
                if result.get("status") == "success":
                    responses.append(result)
            
            # Run evaluations
            evaluation_results = {}
            
            # Custom metrics evaluation
            if responses:
                custom_results = self.evaluator.evaluate_custom_metrics(test_queries, responses)
                evaluation_results["custom_metrics"] = custom_results
            
            # Generate evaluation summary
            summary = {
                "total_queries": len(test_queries),
                "successful_responses": len(responses),
                "success_rate": len(responses) / len(test_queries) if test_queries else 0
            }
            
            if evaluation_results.get("custom_metrics"):
                metrics = evaluation_results["custom_metrics"]
                summary["total_metrics"] = len(metrics)
                summary["average_score"] = sum(metrics.values()) / len(metrics) if metrics else 0
                summary["passing_score"] = sum(1 for score in metrics.values() if score >= 0.7) / len(metrics) if metrics else 0
            
            evaluation_results["evaluation_summary"] = summary
            
            return evaluation_results
            
        except Exception as e:
            return {"error": f"Evaluation failed: {str(e)}"}
    
    def compare_retrieval_methods(self, query: str) -> Dict[str, Any]:
        """Compare different retrieval methods for a given query."""
        if not self.initialized:
            return {"error": "System not initialized"}
        
        try:
            comparison_results = {}
            
            # Test different retrieval methods
            methods = {
                "vector": self.retrieval_system.vector_retriever,
                "bm25": self.retrieval_system.bm25_retriever,
                "ensemble": self.retrieval_system.ensemble_retriever,
                "compression": self.retrieval_system.compression_retriever
            }
            
            for method_name, retriever in methods.items():
                if retriever:
                    try:
                        docs = retriever.get_relevant_documents(query)
                        comparison_results[method_name] = docs
                    except Exception as e:
                        comparison_results[method_name] = f"Error: {str(e)}"
            
            # Analyze results
            analysis = {
                "document_counts": {
                    method: len(docs) if isinstance(docs, list) else 0
                    for method, docs in comparison_results.items()
                },
                "recommendation": "ensemble" if "ensemble" in comparison_results else "vector"
            }
            
            return {
                "comparison_results": comparison_results,
                "analysis": analysis
            }
            
        except Exception as e:
            return {"error": f"Comparison failed: {str(e)}"}
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get the current system status."""
        status = {
            "initialized": self.initialized,
            "components": {
                "data_loader": self.data_loader is not None,
                "retrieval_system": self.retrieval_system is not None,
                "research_agent": self.research_agent is not None,
                "response_agent": self.response_agent is not None,
                "supervisor_agent": self.supervisor_agent is not None,
                "evaluator": self.evaluator is not None
            }
        }
        
        if self.initialized and self.data:
            status["data_summary"] = {
                "total_documents": len(self.data.get("documents", [])),
                "total_complaints": len(self.data.get("complaints", [])),
                "total_test_questions": len(self.data.get("test_data", []))
            }
        
        return status
    
    def save_system_state(self, filepath: str):
        """Save system state to a file."""
        state = {
            "initialized": self.initialized,
            "data_summary": self.get_system_status().get("data_summary", {}),
            "timestamp": str(datetime.now())
        }
        
        with open(filepath, 'w') as f:
            json.dump(state, f, indent=2)


def main():
    """Main function for demonstration."""
    print("🎓 Student Loan Assistant - Initialization")
    print("=" * 50)
    
    # Initialize the system
    assistant = StudentLoanAssistant()
    result = assistant.initialize_system()
    
    if result["status"] == "success":
        print("✅ System initialized successfully!")
        print(f"📄 Loaded {result['data_summary']['total_documents']} documents")
        print(f"📝 Loaded {result['data_summary']['total_complaints']} complaints")
        print(f"❓ Loaded {result['data_summary']['total_test_questions']} test questions")
        
        # Test a query
        print("\n🧪 Testing with a sample query...")
        test_result = assistant.process_student_query("What are the eligibility requirements for federal student loans?")
        
        if test_result.get("status") == "success":
            print("✅ Query processed successfully!")
            print(f"📝 Response: {test_result['final_response'][:200]}...")
        else:
            print(f"❌ Query failed: {test_result.get('error')}")
        
        # Show system status
        print("\n📊 System Status:")
        status = assistant.get_system_status()
        for component, ready in status["components"].items():
            icon = "✅" if ready else "❌"
            print(f"   {icon} {component}")
    
    else:
        print(f"❌ Initialization failed: {result.get('error')}")


if __name__ == "__main__":
    from datetime import datetime
    main() 