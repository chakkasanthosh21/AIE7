"""
Comprehensive RAG System Evaluation using RAGAS.
Evaluates the actual Student Loan Assistant against golden test data.
"""

import os
import sys
import pandas as pd
import time
from typing import List, Dict, Any
import json

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from golden_test_dataset import GoldenTestDataSet
from src.main import StudentLoanAssistant
from src.evaluation.metrics import StudentLoanEvaluator


class RAGSystemEvaluator:
    """Evaluates the complete RAG system using golden test data."""
    
    def __init__(self, openai_api_key: str, cohere_api_key: str = None, tavily_api_key: str = None):
        """
        Initialize the evaluator.
        
        Args:
            openai_api_key: OpenAI API key
            cohere_api_key: Cohere API key (optional)
            tavily_api_key: Tavily API key (optional)
        """
        self.openai_api_key = openai_api_key
        self.cohere_api_key = cohere_api_key
        self.tavily_api_key = tavily_api_key
        
        # Initialize the RAG system
        print("🔧 Initializing RAG System...")
        self.rag_system = StudentLoanAssistant(
            openai_api_key=openai_api_key,
            cohere_api_key=cohere_api_key,
            tavily_api_key=tavily_api_key
        )
        
        # Initialize system
        self.rag_system.initialize_system()
        
        # Initialize evaluator
        self.evaluator = StudentLoanEvaluator(openai_api_key=openai_api_key)
        
        # Load golden test data
        self.test_data = GoldenTestDataSet()
        
    def run_system_evaluation(self) -> Dict[str, Any]:
        """Run comprehensive evaluation of the RAG system."""
        print("🚀 Starting RAG System Evaluation...")
        
        # Get test queries
        test_queries = self.test_data.test_queries
        ground_truth_answers = self.test_data.ground_truth_answers
        
        print(f"📝 Testing {len(test_queries)} queries...")
        
        # Process queries through the system
        system_responses = []
        processing_times = []
        
        for i, query in enumerate(test_queries):
            print(f"Processing query {i+1}/{len(test_queries)}: {query[:50]}...")
            
            start_time = time.time()
            
            try:
                # Process query through the RAG system
                response = self.rag_system.process_student_query(query)
                processing_time = time.time() - start_time
                
                system_responses.append(response)
                processing_times.append(processing_time)
                
                print(f"✅ Query {i+1} processed in {processing_time:.2f}s")
                
            except Exception as e:
                print(f"❌ Error processing query {i+1}: {str(e)}")
                system_responses.append({"error": str(e)})
                processing_times.append(0)
        
        # Extract response texts
        response_texts = []
        for response in system_responses:
            if "error" in response:
                response_texts.append("Error occurred during processing")
            else:
                response_texts.append(response.get("final_response", "No response generated"))
        
        # Run RAGAS evaluation
        print("🔍 Running RAGAS Evaluation...")
        ragas_results = self._run_ragas_evaluation(test_queries, response_texts, ground_truth_answers)
        
        # Run custom evaluation
        print("🔍 Running Custom Evaluation...")
        custom_results = self.evaluator.evaluate_custom_metrics(test_queries, system_responses)
        
        # Compile comprehensive results
        evaluation_results = {
            "ragas_results": ragas_results,
            "custom_metrics": custom_results,
            "performance_metrics": {
                "average_processing_time": sum(processing_times) / len(processing_times),
                "total_queries": len(test_queries),
                "successful_queries": len([r for r in system_responses if "error" not in r]),
                "failed_queries": len([r for r in system_responses if "error" in r])
            },
            "detailed_responses": {
                "queries": test_queries,
                "system_responses": response_texts,
                "ground_truth": ground_truth_answers,
                "processing_times": processing_times
            }
        }
        
        return evaluation_results
    
    def _run_ragas_evaluation(self, queries: List[str], responses: List[str], ground_truth: List[str]) -> Dict[str, Any]:
        """Run RAGAS evaluation on the system responses."""
        try:
            from datasets import Dataset
            from ragas import evaluate
            from ragas.metrics import faithfulness, ResponseRelevancy, ContextPrecision, ContextRecall
            
            # Create dataset for RAGAS
            dataset_dict = {
                "question": queries,
                "answer": responses,
                "ground_truth": ground_truth,
                "contexts": self.test_data.contexts
            }
            
            ragas_dataset = Dataset.from_dict(dataset_dict)
            
            # Run evaluation
            results = evaluate(
                ragas_dataset,
                metrics=[
                    faithfulness,
                    ResponseRelevancy(),
                    ContextPrecision(),
                    ContextRecall()
                ]
            )
            
            return {
                "faithfulness": float(results['faithfulness']),
                "response_relevancy": float(results['ResponseRelevancy']),
                "context_precision": float(results['ContextPrecision']),
                "context_recall": float(results['ContextRecall'])
            }
            
        except Exception as e:
            print(f"❌ RAGAS evaluation failed: {str(e)}")
            return {
                "faithfulness": 0.0,
                "response_relevancy": 0.0,
                "context_precision": 0.0,
                "context_recall": 0.0,
                "error": str(e)
            }
    
    def generate_evaluation_report(self, results: Dict[str, Any]) -> str:
        """Generate a comprehensive evaluation report."""
        report = []
        report.append("=" * 60)
        report.append("🎓 STUDENT LOAN ASSISTANT - RAG SYSTEM EVALUATION")
        report.append("=" * 60)
        report.append("")
        
        # Performance Summary
        report.append("📊 PERFORMANCE SUMMARY")
        report.append("-" * 30)
        perf = results["performance_metrics"]
        report.append(f"Total Queries: {perf['total_queries']}")
        report.append(f"Successful Queries: {perf['successful_queries']}")
        report.append(f"Failed Queries: {perf['failed_queries']}")
        report.append(f"Success Rate: {(perf['successful_queries']/perf['total_queries'])*100:.1f}%")
        report.append(f"Average Processing Time: {perf['average_processing_time']:.2f}s")
        report.append("")
        
        # RAGAS Results
        report.append("🔍 RAGAS EVALUATION RESULTS")
        report.append("-" * 30)
        ragas = results["ragas_results"]
        
        if "error" not in ragas:
            report.append(f"Faithfulness: {ragas['faithfulness']:.3f}")
            report.append(f"Response Relevancy: {ragas['response_relevancy']:.3f}")
            report.append(f"Context Precision: {ragas['context_precision']:.3f}")
            report.append(f"Context Recall: {ragas['context_recall']:.3f}")
            
            # Calculate average RAGAS score
            ragas_scores = [ragas['faithfulness'], ragas['response_relevancy'], 
                           ragas['context_precision'], ragas['context_recall']]
            avg_ragas = sum(ragas_scores) / len(ragas_scores)
            report.append(f"Average RAGAS Score: {avg_ragas:.3f}")
        else:
            report.append(f"RAGAS Evaluation Failed: {ragas['error']}")
        report.append("")
        
        # Custom Metrics
        report.append("🎯 CUSTOM EVALUATION METRICS")
        report.append("-" * 30)
        custom = results["custom_metrics"]
        report.append(f"Accuracy: {custom['accuracy']:.3f}")
        report.append(f"Completeness: {custom['completeness']:.3f}")
        report.append(f"Empathy: {custom['empathy']:.3f}")
        report.append(f"Actionability: {custom['actionability']:.3f}")
        report.append(f"Compliance: {custom['compliance']:.3f}")
        report.append(f"Overall Custom Score: {custom['overall_score']:.3f}")
        report.append("")
        
        # Overall Assessment
        report.append("📋 OVERALL ASSESSMENT")
        report.append("-" * 30)
        
        if "error" not in ragas:
            avg_ragas = sum([ragas['faithfulness'], ragas['response_relevancy'], 
                           ragas['context_precision'], ragas['context_recall']]) / 4
        else:
            avg_ragas = 0.0
            
        avg_custom = custom['overall_score']
        success_rate = perf['successful_queries'] / perf['total_queries']
        
        # Calculate overall score
        overall_score = (avg_ragas + avg_custom + success_rate) / 3
        
        report.append(f"Overall System Score: {overall_score:.3f}")
        
        if overall_score >= 0.8:
            report.append("✅ EXCELLENT - System is highly effective")
        elif overall_score >= 0.7:
            report.append("✅ GOOD - System is effective with minor improvements needed")
        elif overall_score >= 0.6:
            report.append("⚠️  FAIR - Significant improvements recommended")
        else:
            report.append("❌ POOR - Major improvements required")
        
        report.append("")
        
        # Recommendations
        report.append("🎯 RECOMMENDATIONS")
        report.append("-" * 30)
        
        if "error" not in ragas:
            if ragas['faithfulness'] < 0.8:
                report.append("- Improve response faithfulness to source documents")
            if ragas['response_relevancy'] < 0.8:
                report.append("- Enhance response relevance to user queries")
            if ragas['context_precision'] < 0.8:
                report.append("- Improve context retrieval precision")
            if ragas['context_recall'] < 0.8:
                report.append("- Enhance context retrieval recall")
        
        if custom['empathy'] < 0.7:
            report.append("- Increase empathetic tone in responses")
        if custom['actionability'] < 0.7:
            report.append("- Provide more actionable guidance")
        if custom['compliance'] < 0.8:
            report.append("- Strengthen compliance with federal guidelines")
        
        if success_rate < 0.9:
            report.append("- Improve system reliability and error handling")
        
        report.append("")
        report.append("=" * 60)
        
        return "\n".join(report)
    
    def save_evaluation_results(self, results: Dict[str, Any], filename: str = "evaluation_results.json"):
        """Save evaluation results to JSON file."""
        with open(filename, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"✅ Evaluation results saved to {filename}")
    
    def create_results_table(self, results: Dict[str, Any]) -> pd.DataFrame:
        """Create a results table for analysis."""
        ragas = results["ragas_results"]
        custom = results["custom_metrics"]
        
        if "error" not in ragas:
            data = {
                "Metric": [
                    "Faithfulness", "Response Relevancy", "Context Precision", "Context Recall",
                    "Accuracy", "Completeness", "Empathy", "Actionability", "Compliance"
                ],
                "Score": [
                    ragas['faithfulness'], ragas['response_relevancy'], 
                    ragas['context_precision'], ragas['context_recall'],
                    custom['accuracy'], custom['completeness'], custom['empathy'],
                    custom['actionability'], custom['compliance']
                ],
                "Category": [
                    "RAGAS", "RAGAS", "RAGAS", "RAGAS",
                    "Custom", "Custom", "Custom", "Custom", "Custom"
                ]
            }
        else:
            data = {
                "Metric": [
                    "Accuracy", "Completeness", "Empathy", "Actionability", "Compliance"
                ],
                "Score": [
                    custom['accuracy'], custom['completeness'], custom['empathy'],
                    custom['actionability'], custom['compliance']
                ],
                "Category": [
                    "Custom", "Custom", "Custom", "Custom", "Custom"
                ]
            }
        
        return pd.DataFrame(data)


def main():
    """Main evaluation function."""
    print("🎓 Student Loan Assistant - RAG System Evaluation")
    print("=" * 60)
    
    # Get API keys from environment or user input
    openai_api_key = os.getenv("OPENAI_API_KEY")
    cohere_api_key = os.getenv("COHERE_API_KEY")
    tavily_api_key = os.getenv("TAVILY_API_KEY")
    
    if not openai_api_key:
        print("❌ OpenAI API key not found. Please set OPENAI_API_KEY environment variable.")
        return
    
    # Initialize evaluator
    evaluator = RAGSystemEvaluator(
        openai_api_key=openai_api_key,
        cohere_api_key=cohere_api_key,
        tavily_api_key=tavily_api_key
    )
    
    # Run evaluation
    results = evaluator.run_system_evaluation()
    
    # Generate and display report
    report = evaluator.generate_evaluation_report(results)
    print(report)
    
    # Save results
    evaluator.save_evaluation_results(results)
    
    # Create and save results table
    results_table = evaluator.create_results_table(results)
    results_table.to_csv("evaluation_results_table.csv", index=False)
    print("✅ Results table saved to evaluation_results_table.csv")
    
    # Display results table
    print("\n📊 EVALUATION RESULTS TABLE:")
    print("=" * 50)
    print(results_table.to_string(index=False))
    print("=" * 50)


if __name__ == "__main__":
    main() 