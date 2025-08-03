"""
Supervisor agent for student loan assistant.
Orchestrates the multi-agent workflow and manages the overall process.
"""

from typing import Dict, Any, List
from langchain_core.messages import HumanMessage, AIMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolExecutor
from langchain_core.tools import tool
import json


class SupervisorAgent:
    """Supervisor agent that orchestrates the multi-agent workflow."""
    
    def __init__(self, research_agent, response_agent, llm_model: str = "gpt-4o-mini"):
        """
        Initialize the supervisor agent.
        
        Args:
            research_agent: Research agent instance
            response_agent: Response agent instance
            llm_model: LLM model to use
        """
        self.research_agent = research_agent
        self.response_agent = response_agent
        self.llm = ChatOpenAI(model=llm_model)
        
    def create_workflow_graph(self):
        """
        Create the LangGraph workflow for the multi-agent system.
        
        Returns:
            Compiled workflow graph
        """
        # Define the state structure
        from typing_extensions import TypedDict
        from langchain_core.documents import Document
        
        class AgentState(TypedDict):
            query: str
            research_results: Dict[str, Any]
            response: Dict[str, Any]
            final_response: str
            metadata: Dict[str, Any]
            
        # Define the workflow nodes
        def research_node(state: AgentState) -> AgentState:
            """Research node that retrieves relevant information."""
            query = state["query"]
            print(f"🔍 Researching: {query}")
            
            research_results = self.research_agent.get_research_insights(query)
            
            return {
                **state,
                "research_results": research_results
            }
            
        def response_node(state: AgentState) -> AgentState:
            """Response node that generates the final response."""
            query = state["query"]
            research_context = state["research_results"]["summary"]
            
            print(f"💬 Generating response for: {query}")
            
            response_data = self.response_agent.generate_response(query, research_context)
            
            return {
                **state,
                "response": response_data
            }
            
        def supervisor_node(state: AgentState) -> AgentState:
            """Supervisor node that reviews and finalizes the response."""
            query = state["query"]
            research_results = state["research_results"]
            response_data = state["response"]
            
            print(f"👨‍💼 Supervisor reviewing response for: {query}")
            
            # Review the response quality
            review_prompt = f"""
            As a supervisor, review this student loan response:
            
            Query: {query}
            Research Summary: {research_results.get('summary', '')}
            Generated Response: {response_data.get('response', '')}
            
            Please:
            1. Verify the response addresses the query accurately
            2. Check if all important information from research is included
            3. Ensure the tone is appropriate and empathetic
            4. Confirm the response provides clear next steps
            
            Provide a final, polished response that incorporates any necessary improvements:
            """
            
            review_response = self.llm.invoke([HumanMessage(content=review_prompt)])
            
            # Generate metadata
            metadata = {
                "query_type": self._classify_query_type(query),
                "complexity_level": self._assess_complexity(query),
                "research_sources": research_results.get('sources', []),
                "response_quality": response_data.get('quality_metrics', {}),
                "processing_time": "completed"
            }
            
            return {
                **state,
                "final_response": review_response.content,
                "metadata": metadata
            }
            
        # Create the workflow graph
        workflow = StateGraph(AgentState)
        
        # Add nodes
        workflow.add_node("research", research_node)
        workflow.add_node("response", response_node)
        workflow.add_node("supervisor", supervisor_node)
        
        # Add edges
        workflow.add_edge(START, "research")
        workflow.add_edge("research", "response")
        workflow.add_edge("response", "supervisor")
        workflow.add_edge("supervisor", END)
        
        return workflow.compile()
        
    def process_query(self, query: str, student_context: str = "") -> Dict[str, Any]:
        """
        Process a student query through the complete workflow.
        
        Args:
            query: Student's question
            student_context: Additional context about the student
            
        Returns:
            Complete response with all metadata
        """
        # Create the workflow
        workflow = self.create_workflow_graph()
        
        # Initialize state
        initial_state = {
            "query": query,
            "research_results": {},
            "response": {},
            "final_response": "",
            "metadata": {"student_context": student_context}
        }
        
        # Execute the workflow
        print(f"🚀 Starting workflow for query: {query}")
        result = workflow.invoke(initial_state)
        
        return result
        
    def process_batch_queries(self, queries: List[str]) -> List[Dict[str, Any]]:
        """
        Process multiple queries in batch.
        
        Args:
            queries: List of student queries
            
        Returns:
            List of responses for each query
        """
        results = []
        
        for i, query in enumerate(queries):
            print(f"Processing query {i+1}/{len(queries)}: {query}")
            try:
                result = self.process_query(query)
                results.append(result)
            except Exception as e:
                print(f"Error processing query '{query}': {str(e)}")
                results.append({
                    "query": query,
                    "error": str(e),
                    "final_response": "I apologize, but I encountered an error processing your query. Please try again or contact support."
                })
                
        return results
        
    def generate_workflow_report(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Generate a comprehensive report of the workflow execution.
        
        Args:
            results: List of workflow results
            
        Returns:
            Workflow execution report
        """
        total_queries = len(results)
        successful_queries = len([r for r in results if "error" not in r])
        failed_queries = total_queries - successful_queries
        
        # Analyze response quality
        quality_scores = []
        query_types = []
        complexity_levels = []
        
        for result in results:
            if "error" not in result:
                metadata = result.get("metadata", {})
                quality_metrics = metadata.get("response_quality", {})
                
                if quality_metrics:
                    avg_quality = sum(quality_metrics.values()) / len(quality_metrics)
                    quality_scores.append(avg_quality)
                    
                query_types.append(metadata.get("query_type", "unknown"))
                complexity_levels.append(metadata.get("complexity_level", "medium"))
                
        report = {
            "summary": {
                "total_queries": total_queries,
                "successful_queries": successful_queries,
                "failed_queries": failed_queries,
                "success_rate": successful_queries / total_queries if total_queries > 0 else 0
            },
            "quality_analysis": {
                "average_quality_score": sum(quality_scores) / len(quality_scores) if quality_scores else 0,
                "quality_distribution": {
                    "high": len([s for s in quality_scores if s >= 8]),
                    "medium": len([s for s in quality_scores if 6 <= s < 8]),
                    "low": len([s for s in quality_scores if s < 6])
                }
            },
            "query_analysis": {
                "query_types": self._count_occurrences(query_types),
                "complexity_distribution": self._count_occurrences(complexity_levels)
            },
            "recommendations": self._generate_recommendations(results)
        }
        
        return report
        
    def _classify_query_type(self, query: str) -> str:
        """Classify the type of query."""
        query_lower = query.lower()
        
        if any(word in query_lower for word in ["eligibility", "qualify", "eligible"]):
            return "eligibility"
        elif any(word in query_lower for word in ["application", "apply", "process"]):
            return "application"
        elif any(word in query_lower for word in ["payment", "repay", "due"]):
            return "payment"
        elif any(word in query_lower for word in ["deadline", "due date", "when"]):
            return "deadline"
        elif any(word in query_lower for word in ["amount", "how much", "limit"]):
            return "amount"
        else:
            return "general"
            
    def _assess_complexity(self, query: str) -> str:
        """Assess the complexity of the query."""
        query_lower = query.lower()
        
        # Count complexity indicators
        complexity_indicators = [
            "multiple", "several", "different", "various", "complex",
            "complicated", "detailed", "specific", "requirements"
        ]
        
        indicator_count = sum(1 for indicator in complexity_indicators if indicator in query_lower)
        
        if indicator_count >= 3:
            return "high"
        elif indicator_count >= 1:
            return "medium"
        else:
            return "low"
            
    def _count_occurrences(self, items: List[str]) -> Dict[str, int]:
        """Count occurrences of items in a list."""
        counts = {}
        for item in items:
            counts[item] = counts.get(item, 0) + 1
        return counts
        
    def _generate_recommendations(self, results: List[Dict[str, Any]]) -> List[str]:
        """Generate recommendations based on workflow results."""
        recommendations = []
        
        # Analyze success rate
        success_rate = len([r for r in results if "error" not in r]) / len(results)
        
        if success_rate < 0.9:
            recommendations.append("Consider improving error handling and retry mechanisms")
            
        # Analyze quality scores
        quality_scores = []
        for result in results:
            if "error" not in result:
                metadata = result.get("metadata", {})
                quality_metrics = metadata.get("response_quality", {})
                if quality_metrics:
                    avg_quality = sum(quality_metrics.values()) / len(quality_metrics)
                    quality_scores.append(avg_quality)
                    
        if quality_scores:
            avg_quality = sum(quality_scores) / len(quality_scores)
            if avg_quality < 7:
                recommendations.append("Consider improving response generation quality")
                
        # Analyze query types
        query_types = [r.get("metadata", {}).get("query_type", "unknown") for r in results if "error" not in r]
        type_counts = self._count_occurrences(query_types)
        
        if "general" in type_counts and type_counts["general"] > len(results) * 0.3:
            recommendations.append("Consider improving query classification for better routing")
            
        return recommendations


if __name__ == "__main__":
    # Example usage
    print("Supervisor agent module loaded") 