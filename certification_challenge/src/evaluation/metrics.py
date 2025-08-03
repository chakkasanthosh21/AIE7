"""
Evaluation metrics for student loan assistant.
Uses RAGAS and custom metrics to evaluate system performance.
"""

import os
from typing import List, Dict, Any, Optional
import pandas as pd
from ragas import evaluate, RunConfig
from ragas.metrics import (
    LLMContextRecall, 
    Faithfulness, 
    FactualCorrectness, 
    ResponseRelevancy, 
    ContextEntityRecall, 
    NoiseSensitivity
)
from ragas.llms import LangchainLLMWrapper
from langchain_openai import ChatOpenAI
from langsmith.evaluation import LangChainStringEvaluator, evaluate as langsmith_evaluate
import json


class StudentLoanEvaluator:
    """Evaluator for student loan assistant using RAGAS and custom metrics."""
    
    def __init__(self, openai_api_key: Optional[str] = None):
        """
        Initialize the evaluator.
        
        Args:
            openai_api_key: OpenAI API key for evaluation
        """
        self.openai_api_key = openai_api_key or os.getenv("OPENAI_API_KEY")
        
        # Initialize evaluation LLM
        self.eval_llm = LangchainLLMWrapper(
            ChatOpenAI(model="gpt-4o-mini", openai_api_key=self.openai_api_key)
        )
        
        # Initialize RAGAS metrics
        self.ragas_metrics = [
            LLMContextRecall(),
            Faithfulness(),
            FactualCorrectness(),
            ResponseRelevancy(),
            ContextEntityRecall(),
            NoiseSensitivity()
        ]
        
    def evaluate_with_ragas(self, dataset, run_config: Optional[RunConfig] = None) -> Dict[str, Any]:
        """
        Evaluate the system using RAGAS metrics.
        
        Args:
            dataset: RAGAS dataset for evaluation
            run_config: RAGAS run configuration
            
        Returns:
            Evaluation results
        """
        if run_config is None:
            run_config = RunConfig(timeout=360)
            
        print("🔍 Evaluating with RAGAS metrics...")
        
        try:
            results = evaluate(
                dataset=dataset,
                metrics=self.ragas_metrics,
                llm=self.eval_llm,
                run_config=run_config
            )
            
            return {
                "ragas_results": results,
                "metrics_summary": self._summarize_ragas_results(results)
            }
            
        except Exception as e:
            print(f"Error in RAGAS evaluation: {str(e)}")
            return {"error": str(e)}
            
    def evaluate_with_langsmith(self, dataset_name: str, rag_function) -> Dict[str, Any]:
        """
        Evaluate the system using LangSmith.
        
        Args:
            dataset_name: Name of the LangSmith dataset
            rag_function: RAG function to evaluate
            
        Returns:
            LangSmith evaluation results
        """
        print("🔍 Evaluating with LangSmith...")
        
        try:
            # Define custom evaluators
            qa_evaluator = LangChainStringEvaluator("qa", config={"llm": self.eval_llm})
            
            helpfulness_evaluator = LangChainStringEvaluator(
                "labeled_criteria",
                config={
                    "criteria": {
                        "helpfulness": "Is this response helpful to the student's query about student loans?"
                    },
                    "llm": self.eval_llm
                }
            )
            
            empathy_evaluator = LangChainStringEvaluator(
                "criteria",
                config={
                    "criteria": {
                        "empathy": "Does this response show empathy and understanding of the student's situation?"
                    },
                    "llm": self.eval_llm
                }
            )
            
            # Run evaluation
            results = langsmith_evaluate(
                rag_function,
                data=dataset_name,
                evaluators=[qa_evaluator, helpfulness_evaluator, empathy_evaluator],
                experiment_prefix="Student Loan Assistant Evaluation"
            )
            
            return {
                "langsmith_results": results,
                "evaluators_used": ["qa", "helpfulness", "empathy"]
            }
            
        except Exception as e:
            print(f"Error in LangSmith evaluation: {str(e)}")
            return {"error": str(e)}
            
    def evaluate_custom_metrics(self, test_queries: List[str], responses: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Evaluate using custom metrics specific to student loan assistance.
        
        Args:
            test_queries: List of test queries
            responses: List of system responses
            
        Returns:
            Custom evaluation results
        """
        print("🔍 Evaluating with custom metrics...")
        
        custom_metrics = {
            "accuracy": self._evaluate_accuracy(test_queries, responses),
            "completeness": self._evaluate_completeness(test_queries, responses),
            "empathy": self._evaluate_empathy(responses),
            "actionability": self._evaluate_actionability(responses),
            "compliance": self._evaluate_compliance(responses)
        }
        
        return {
            "custom_metrics": custom_metrics,
            "overall_score": sum(custom_metrics.values()) / len(custom_metrics)
        }
        
    def _summarize_ragas_results(self, results) -> Dict[str, float]:
        """Summarize RAGAS evaluation results."""
        summary = {}
        
        for metric_name, metric_value in results.items():
            if hasattr(metric_value, 'score'):
                summary[metric_name] = metric_value.score
            else:
                summary[metric_name] = metric_value
                
        return summary
        
    def _evaluate_accuracy(self, queries: List[str], responses: List[Dict[str, Any]]) -> float:
        """Evaluate response accuracy."""
        accuracy_scores = []
        
        for query, response in zip(queries, responses):
            if "error" in response:
                accuracy_scores.append(0.0)
                continue
                
            # Check if response contains relevant loan information
            response_text = response.get("final_response", response.get("response", ""))
            
            loan_keywords = [
                "loan", "federal", "direct", "subsidized", "unsubsidized",
                "eligibility", "application", "payment", "deadline", "requirement"
            ]
            
            keyword_matches = sum(1 for keyword in loan_keywords if keyword.lower() in response_text.lower())
            accuracy_score = min(keyword_matches / len(loan_keywords), 1.0)
            accuracy_scores.append(accuracy_score)
            
        return sum(accuracy_scores) / len(accuracy_scores) if accuracy_scores else 0.0
        
    def _evaluate_completeness(self, queries: List[str], responses: List[Dict[str, Any]]) -> float:
        """Evaluate response completeness."""
        completeness_scores = []
        
        for query, response in zip(queries, responses):
            if "error" in response:
                completeness_scores.append(0.0)
                continue
                
            response_text = response.get("final_response", response.get("response", ""))
            
            # Check for completeness indicators
            completeness_indicators = [
                "step", "process", "next", "deadline", "contact", "website",
                "requirement", "document", "form", "submit"
            ]
            
            indicator_matches = sum(1 for indicator in completeness_indicators if indicator.lower() in response_text.lower())
            completeness_score = min(indicator_matches / len(completeness_indicators), 1.0)
            completeness_scores.append(completeness_score)
            
        return sum(completeness_scores) / len(completeness_scores) if completeness_scores else 0.0
        
    def _evaluate_empathy(self, responses: List[Dict[str, Any]]) -> float:
        """Evaluate response empathy."""
        empathy_scores = []
        
        for response in responses:
            if "error" in response:
                empathy_scores.append(0.0)
                continue
                
            response_text = response.get("final_response", response.get("response", ""))
            
            # Check for empathy indicators
            empathy_indicators = [
                "understand", "concern", "stress", "difficult", "challenging",
                "support", "help", "assist", "guide", "encourage", "feel"
            ]
            
            indicator_matches = sum(1 for indicator in empathy_indicators if indicator.lower() in response_text.lower())
            empathy_score = min(indicator_matches / len(empathy_indicators), 1.0)
            empathy_scores.append(empathy_score)
            
        return sum(empathy_scores) / len(empathy_scores) if empathy_scores else 0.0
        
    def _evaluate_actionability(self, responses: List[Dict[str, Any]]) -> float:
        """Evaluate response actionability."""
        actionability_scores = []
        
        for response in responses:
            if "error" in response:
                actionability_scores.append(0.0)
                continue
                
            response_text = response.get("final_response", response.get("response", ""))
            
            # Check for actionability indicators
            action_indicators = [
                "visit", "call", "submit", "apply", "complete", "fill out",
                "contact", "deadline", "due date", "next step", "action"
            ]
            
            indicator_matches = sum(1 for indicator in action_indicators if indicator.lower() in response_text.lower())
            actionability_score = min(indicator_matches / len(action_indicators), 1.0)
            actionability_scores.append(actionability_score)
            
        return sum(actionability_scores) / len(actionability_scores) if actionability_scores else 0.0
        
    def _evaluate_compliance(self, responses: List[Dict[str, Any]]) -> float:
        """Evaluate response compliance with federal guidelines."""
        compliance_scores = []
        
        for response in responses:
            if "error" in response:
                compliance_scores.append(0.0)
                continue
                
            response_text = response.get("final_response", response.get("response", ""))
            
            # Check for compliance indicators
            compliance_indicators = [
                "federal", "government", "official", "policy", "regulation",
                "requirement", "eligibility", "deadline", "documentation"
            ]
            
            # Check for disclaimers
            disclaimer_indicators = [
                "consult", "advisor", "official", "verify", "confirm"
            ]
            
            compliance_matches = sum(1 for indicator in compliance_indicators if indicator.lower() in response_text.lower())
            disclaimer_matches = sum(1 for indicator in disclaimer_indicators if indicator.lower() in response_text.lower())
            
            compliance_score = min((compliance_matches + disclaimer_matches) / (len(compliance_indicators) + len(disclaimer_indicators)), 1.0)
            compliance_scores.append(compliance_score)
            
        return sum(compliance_scores) / len(compliance_scores) if compliance_scores else 0.0
        
    def generate_evaluation_report(self, all_results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate a comprehensive evaluation report.
        
        Args:
            all_results: Dictionary containing all evaluation results
            
        Returns:
            Comprehensive evaluation report
        """
        report = {
            "evaluation_summary": {
                "total_metrics": 0,
                "average_score": 0.0,
                "passing_score": 0.0
            },
            "detailed_results": all_results,
            "recommendations": []
        }
        
        # Calculate overall metrics
        scores = []
        
        # RAGAS scores
        if "ragas_results" in all_results and "metrics_summary" in all_results["ragas_results"]:
            ragas_scores = all_results["ragas_results"]["metrics_summary"].values()
            scores.extend(ragas_scores)
            
        # Custom scores
        if "custom_metrics" in all_results:
            custom_scores = all_results["custom_metrics"].values()
            scores.extend(custom_scores)
            
        if scores:
            report["evaluation_summary"]["total_metrics"] = len(scores)
            report["evaluation_summary"]["average_score"] = sum(scores) / len(scores)
            report["evaluation_summary"]["passing_score"] = sum(1 for score in scores if score >= 0.7) / len(scores)
            
        # Generate recommendations
        report["recommendations"] = self._generate_evaluation_recommendations(all_results)
        
        return report
        
    def _generate_evaluation_recommendations(self, results: Dict[str, Any]) -> List[str]:
        """Generate recommendations based on evaluation results."""
        recommendations = []
        
        # Check RAGAS results
        if "ragas_results" in results and "metrics_summary" in results["ragas_results"]:
            ragas_scores = results["ragas_results"]["metrics_summary"]
            
            if ragas_scores.get("faithfulness", 1.0) < 0.8:
                recommendations.append("Improve response faithfulness to source documents")
                
            if ragas_scores.get("response_relevancy", 1.0) < 0.8:
                recommendations.append("Enhance response relevance to user queries")
                
        # Check custom metrics
        if "custom_metrics" in results:
            custom_scores = results["custom_metrics"]
            
            if custom_scores.get("empathy", 1.0) < 0.7:
                recommendations.append("Increase empathetic tone in responses")
                
            if custom_scores.get("actionability", 1.0) < 0.7:
                recommendations.append("Provide more actionable guidance")
                
            if custom_scores.get("compliance", 1.0) < 0.8:
                recommendations.append("Strengthen compliance with federal guidelines")
                
        return recommendations


if __name__ == "__main__":
    # Example usage
    evaluator = StudentLoanEvaluator()
    print("Student loan evaluator initialized") 