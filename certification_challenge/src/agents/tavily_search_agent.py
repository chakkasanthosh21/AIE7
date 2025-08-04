"""
Tavily Search Agent for student loan assistant.
Performs real-time web searches to enhance responses with current information.
"""

import os
from typing import List, Dict, Any, Optional
from langchain_core.messages import HumanMessage, AIMessage
from langchain_openai import ChatOpenAI
from langchain_community.tools import TavilySearchResults
from langchain_core.tools import tool


class TavilySearchAgent:
    """Agent responsible for performing real-time web searches using Tavily."""
    
    def __init__(self, llm_model: str = "gpt-4o-mini"):
        """
        Initialize the Tavily search agent.
        
        Args:
            llm_model: LLM model to use for processing search results
        """
        self.llm = ChatOpenAI(model=llm_model)
        self.tavily_api_key = os.getenv("TAVILY_API_KEY")
        
        if not self.tavily_api_key:
            print("Warning: TAVILY_API_KEY not found. Web search functionality will be disabled.")
            self.search_tool = None
        else:
            self.search_tool = TavilySearchResults(max_results=5)
        
    def search_and_analyze(self, query: str, search_depth: str = "moderate") -> Dict[str, Any]:
        """
        Perform web search and analyze results for student loan queries.
        
        Args:
            query: Search query
            search_depth: Search depth ("basic", "moderate", "advanced")
            
        Returns:
            Dictionary with search results and analysis
        """
        if not self.search_tool:
            return {
                "query": query,
                "search_results": [],
                "analysis": "Web search disabled - TAVILY_API_KEY not configured",
                "current_info": "",
                "recommendations": []
            }
        
        try:
            # Perform web search
            search_results = self.search_tool.invoke({
                "query": f"student loan {query} current information 2024",
                "search_depth": search_depth
            })
            
            # Analyze search results
            analysis = self._analyze_search_results(query, search_results)
            
            # Extract current information
            current_info = self._extract_current_information(search_results)
            
            # Generate recommendations
            recommendations = self._generate_recommendations(query, search_results)
            
            return {
                "query": query,
                "search_results": search_results,
                "analysis": analysis,
                "current_info": current_info,
                "recommendations": recommendations,
                "sources": [result.get('url', 'unknown') for result in search_results]
            }
            
        except Exception as e:
            return {
                "query": query,
                "search_results": [],
                "analysis": f"Search failed: {str(e)}",
                "current_info": "",
                "recommendations": []
            }
    
    def _analyze_search_results(self, query: str, search_results: List[Dict]) -> str:
        """
        Analyze search results for relevance and accuracy.
        
        Args:
            query: Original query
            search_results: List of search results
            
        Returns:
            Analysis of search results
        """
        if not search_results:
            return "No search results found."
        
        # Prepare search results for analysis
        results_text = "\n\n".join([
            f"Title: {result.get('title', 'No title')}\n"
            f"Content: {result.get('content', 'No content')}\n"
            f"URL: {result.get('url', 'No URL')}"
            for result in search_results
        ])
        
        prompt = f"""
        You are a student loan expert analyzing web search results.
        
        Original Query: {query}
        
        Search Results:
        {results_text}
        
        Please analyze these search results and provide:
        1. Relevance to the student loan query
        2. Accuracy of the information
        3. Timeliness of the data
        4. Credibility of the sources
        
        Focus on identifying the most reliable and current information about student loans.
        """
        
        response = self.llm.invoke([HumanMessage(content=prompt)])
        return response.content
    
    def _extract_current_information(self, search_results: List[Dict]) -> str:
        """
        Extract current and relevant information from search results.
        
        Args:
            search_results: List of search results
            
        Returns:
            Extracted current information
        """
        if not search_results:
            return "No current information available."
        
        # Filter for recent and relevant results
        relevant_results = []
        for result in search_results:
            content = result.get('content', '')
            title = result.get('title', '')
            
            # Check for current year mentions and student loan relevance
            if any(year in content.lower() for year in ['2024', '2023', 'current', 'latest']):
                if any(term in content.lower() for term in ['student loan', 'federal loan', 'direct loan', 'pell grant']):
                    relevant_results.append(result)
        
        if not relevant_results:
            return "No current student loan information found in search results."
        
        # Extract key information from relevant results
        current_info_parts = []
        for result in relevant_results[:3]:  # Limit to top 3 results
            current_info_parts.append(f"Source: {result.get('title', 'Unknown')}\n{result.get('content', '')}")
        
        return "\n\n".join(current_info_parts)
    
    def _generate_recommendations(self, query: str, search_results: List[Dict]) -> List[str]:
        """
        Generate recommendations based on search results.
        
        Args:
            query: Original query
            search_results: List of search results
            
        Returns:
            List of recommendations
        """
        if not search_results:
            return ["No recommendations available due to lack of search results."]
        
        # Prepare search results for recommendation generation
        results_summary = "\n".join([
            f"- {result.get('title', 'No title')}: {result.get('content', 'No content')[:200]}..."
            for result in search_results[:3]
        ])
        
        prompt = f"""
        Based on these web search results about student loans, generate actionable recommendations:
        
        Query: {query}
        
        Search Results Summary:
        {results_summary}
        
        Provide 3-5 specific, actionable recommendations that students or administrators can follow.
        Focus on practical steps and current best practices.
        """
        
        response = self.llm.invoke([HumanMessage(content=prompt)])
        return [rec.strip() for rec in response.content.split('\n') if rec.strip()]
    
    def enhance_context_with_search(self, original_context: str, query: str) -> str:
        """
        Enhance original context with current web search information.
        
        Args:
            original_context: Original context from documentation
            query: User query
            
        Returns:
            Enhanced context with current information
        """
        search_results = self.search_and_analyze(query)
        
        if not search_results.get("current_info") or "disabled" in search_results.get("current_info", ""):
            return original_context
        
        enhanced_context = f"""
{original_context}

=== CURRENT INFORMATION FROM WEB SEARCH ===
{search_results.get("current_info", "")}

=== RECOMMENDATIONS ===
{chr(10).join(search_results.get("recommendations", []))}
        """
        
        return enhanced_context.strip()
    
    def is_search_needed(self, query: str) -> bool:
        """
        Determine if web search is needed for the query.
        
        Args:
            query: User query
            
        Returns:
            True if search is recommended
        """
        search_keywords = [
            'current', 'latest', '2024', '2023', 'recent', 'update', 'new',
            'interest rate', 'deadline', 'application', 'deadline',
            'forgiveness', 'repayment', 'consolidation'
        ]
        
        query_lower = query.lower()
        return any(keyword in query_lower for keyword in search_keywords)


if __name__ == "__main__":
    # Example usage
    print("Tavily search agent module loaded") 