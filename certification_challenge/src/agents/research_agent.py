"""
Research agent for student loan assistant.
Retrieves relevant information from loan documentation and web search.
"""

from typing import List, Dict, Any
from langchain_core.documents import Document
from langchain_core.messages import HumanMessage, AIMessage
from langchain_openai import ChatOpenAI
from .tavily_search_agent import TavilySearchAgent


class ResearchAgent:
    """Agent responsible for researching and retrieving loan information."""
    
    def __init__(self, retriever, llm_model: str = "gpt-4o-mini"):
        """
        Initialize the research agent.
        
        Args:
            retriever: Document retriever
            llm_model: LLM model to use
        """
        self.retriever = retriever
        self.llm = ChatOpenAI(model=llm_model)
        self.tavily_agent = TavilySearchAgent(llm_model=llm_model)
        
    def research_query(self, query: str, k: int = 5) -> Dict[str, Any]:
        """
        Research a query and retrieve relevant information.
        
        Args:
            query: Research query
            k: Number of documents to retrieve
            
        Returns:
            Dictionary with research results
        """
        # Retrieve relevant documents
        documents = self.retriever.get_relevant_documents(query)
        
        # Extract key information from documents
        context = self._extract_context(documents)
        
        # Check if web search is needed and enhance context
        enhanced_context = context
        web_search_results = None
        
        if self.tavily_agent.is_search_needed(query):
            enhanced_context = self.tavily_agent.enhance_context_with_search(context, query)
            web_search_results = self.tavily_agent.search_and_analyze(query)
        
        # Generate research summary
        summary = self._generate_summary(query, enhanced_context)
        
        return {
            "query": query,
            "documents": documents,
            "context": enhanced_context,
            "original_context": context,
            "summary": summary,
            "web_search_results": web_search_results,
            "sources": [doc.metadata.get('source', 'unknown') for doc in documents]
        }
        
    def _extract_context(self, documents: List[Document]) -> str:
        """
        Extract relevant context from documents.
        
        Args:
            documents: List of retrieved documents
            
        Returns:
            Extracted context as string
        """
        context_parts = []
        
        for i, doc in enumerate(documents):
            context_parts.append(f"Document {i+1}:\n{doc.page_content}\n")
            
        return "\n".join(context_parts)
        
    def _generate_summary(self, query: str, context: str) -> str:
        """
        Generate a summary of the research findings.
        
        Args:
            query: Original query
            context: Retrieved context
            
        Returns:
            Research summary
        """
        prompt = f"""
        You are a research assistant specializing in student loan policies.
        
        Query: {query}
        
        Context from loan documentation:
        {context}
        
        Please provide a comprehensive summary of the relevant information found in the context that addresses the query. 
        Focus on:
        1. Key policies and procedures
        2. Eligibility requirements
        3. Important deadlines and requirements
        4. Any specific details that directly answer the query
        
        Summary:
        """
        
        response = self.llm.invoke([HumanMessage(content=prompt)])
        return response.content
        
    def get_research_insights(self, query: str) -> Dict[str, Any]:
        """
        Get detailed research insights for a query.
        
        Args:
            query: Research query
            
        Returns:
            Dictionary with research insights
        """
        research_results = self.research_query(query)
        
        # Analyze the research results
        insights = {
            "key_findings": self._extract_key_findings(research_results["summary"]),
            "policy_implications": self._analyze_policy_implications(research_results["context"]),
            "action_items": self._identify_action_items(research_results["summary"]),
            "source_reliability": self._assess_source_reliability(research_results["sources"])
        }
        
        research_results["insights"] = insights
        return research_results
        
    def _extract_key_findings(self, summary: str) -> List[str]:
        """Extract key findings from research summary."""
        prompt = f"""
        Extract the key findings from this research summary:
        
        {summary}
        
        List the main points as bullet points:
        """
        
        response = self.llm.invoke([HumanMessage(content=prompt)])
        return response.content.split('\n')
        
    def _analyze_policy_implications(self, context: str) -> str:
        """Analyze policy implications of the research."""
        prompt = f"""
        Analyze the policy implications of this student loan information:
        
        {context}
        
        What are the key policy implications for students and administrators?
        """
        
        response = self.llm.invoke([HumanMessage(content=prompt)])
        return response.content
        
    def _identify_action_items(self, summary: str) -> List[str]:
        """Identify action items from research."""
        prompt = f"""
        Based on this research summary, identify specific action items:
        
        {summary}
        
        List actionable steps that should be taken:
        """
        
        response = self.llm.invoke([HumanMessage(content=prompt)])
        return response.content.split('\n')
        
    def _assess_source_reliability(self, sources: List[str]) -> Dict[str, str]:
        """Assess the reliability of information sources."""
        reliability_assessment = {}
        
        for source in sources:
            if "federal" in source.lower() or "direct" in source.lower():
                reliability_assessment[source] = "High - Official federal documentation"
            elif "complaints" in source.lower():
                reliability_assessment[source] = "Medium - User-reported issues"
            else:
                reliability_assessment[source] = "Standard - General documentation"
                
        return reliability_assessment


if __name__ == "__main__":
    # Example usage
    print("Research agent module loaded") 