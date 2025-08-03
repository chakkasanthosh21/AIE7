"""
Response agent for student loan assistant.
Generates helpful and empathetic responses to student queries.
"""

from typing import Dict, Any, List
from langchain_core.messages import HumanMessage, AIMessage
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate


class ResponseAgent:
    """Agent responsible for generating helpful responses to student queries."""
    
    def __init__(self, llm_model: str = "gpt-4o-mini"):
        """
        Initialize the response agent.
        
        Args:
            llm_model: LLM model to use
        """
        self.llm = ChatOpenAI(model=llm_model)
        
        # Define response templates
        self.response_template = ChatPromptTemplate.from_template("""
        You are a helpful and empathetic student loan advisor. Your role is to provide clear, 
        accurate, and supportive guidance to students and their families about federal student loans.
        
        Research Context:
        {research_context}
        
        Student Query:
        {student_query}
        
        Please provide a comprehensive response that:
        1. Directly addresses the student's question
        2. Uses the research context to provide accurate information
        3. Shows empathy and understanding of their situation
        4. Provides clear next steps or action items
        5. Maintains a supportive and encouraging tone
        
        Response:
        """)
        
        self.follow_up_template = ChatPromptTemplate.from_template("""
        Based on the student's query and your response, suggest 2-3 follow-up questions 
        that might be helpful for them to consider:
        
        Original Query: {student_query}
        Your Response: {response}
        
        Follow-up questions:
        """)
        
    def generate_response(self, student_query: str, research_context: str) -> Dict[str, Any]:
        """
        Generate a helpful response to a student query.
        
        Args:
            student_query: The student's question
            research_context: Research findings and context
            
        Returns:
            Dictionary with response and metadata
        """
        # Generate main response
        response_messages = self.response_template.format_messages(
            research_context=research_context,
            student_query=student_query
        )
        
        response = self.llm.invoke(response_messages)
        
        # Generate follow-up questions
        follow_up_messages = self.follow_up_template.format_messages(
            student_query=student_query,
            response=response.content
        )
        
        follow_up_response = self.llm.invoke(follow_up_messages)
        
        # Analyze response quality
        quality_metrics = self._analyze_response_quality(response.content, student_query)
        
        return {
            "query": student_query,
            "response": response.content,
            "follow_up_questions": self._extract_follow_up_questions(follow_up_response.content),
            "quality_metrics": quality_metrics,
            "response_length": len(response.content),
            "tone_analysis": self._analyze_tone(response.content)
        }
        
    def generate_empathetic_response(self, student_query: str, research_context: str, 
                                   student_context: str = "") -> Dict[str, Any]:
        """
        Generate an empathetic response considering student context.
        
        Args:
            student_query: The student's question
            research_context: Research findings
            student_context: Additional context about the student's situation
            
        Returns:
            Dictionary with empathetic response
        """
        empathetic_prompt = f"""
        You are a compassionate student loan advisor who understands the stress and 
        confusion that can come with navigating student loans.
        
        Student Context: {student_context}
        Student Query: {student_query}
        Research Information: {research_context}
        
        Please provide a response that:
        1. Acknowledges the student's feelings and concerns
        2. Provides clear, accurate information
        3. Offers practical guidance and next steps
        4. Maintains a warm, supportive tone
        5. Shows understanding of their unique situation
        
        Response:
        """
        
        response = self.llm.invoke([HumanMessage(content=empathetic_prompt)])
        
        return {
            "query": student_query,
            "response": response.content,
            "student_context": student_context,
            "empathy_score": self._calculate_empathy_score(response.content),
            "clarity_score": self._calculate_clarity_score(response.content)
        }
        
    def generate_action_plan(self, student_query: str, research_context: str) -> Dict[str, Any]:
        """
        Generate a structured action plan for the student.
        
        Args:
            student_query: The student's question
            research_context: Research findings
            
        Returns:
            Dictionary with action plan
        """
        action_plan_prompt = f"""
        Based on the student's query and the research context, create a structured action plan.
        
        Student Query: {student_query}
        Research Context: {research_context}
        
        Please create an action plan that includes:
        1. Immediate next steps (next 1-2 weeks)
        2. Medium-term actions (next 1-3 months)
        3. Important deadlines to remember
        4. Resources and contacts they should use
        5. Potential challenges and how to address them
        
        Format as a clear, step-by-step plan:
        """
        
        response = self.llm.invoke([HumanMessage(content=action_plan_prompt)])
        
        return {
            "query": student_query,
            "action_plan": response.content,
            "priority_level": self._assess_priority_level(student_query),
            "estimated_timeline": self._estimate_timeline(student_query)
        }
        
    def _extract_follow_up_questions(self, follow_up_text: str) -> List[str]:
        """Extract follow-up questions from the response."""
        lines = follow_up_text.split('\n')
        questions = []
        
        for line in lines:
            line = line.strip()
            if line and ('?' in line or line.startswith(('1.', '2.', '3.', '-'))):
                questions.append(line)
                
        return questions[:3]  # Return max 3 questions
        
    def _analyze_response_quality(self, response: str, query: str) -> Dict[str, float]:
        """Analyze the quality of the response."""
        quality_prompt = f"""
        Analyze the quality of this response to a student loan query:
        
        Query: {query}
        Response: {response}
        
        Rate the following aspects on a scale of 1-10:
        1. Accuracy (how well it addresses the query)
        2. Completeness (how comprehensive the response is)
        3. Clarity (how easy it is to understand)
        4. Helpfulness (how useful the information is)
        5. Empathy (how understanding and supportive the tone is)
        
        Provide scores as: Accuracy: X, Completeness: Y, etc.
        """
        
        quality_response = self.llm.invoke([HumanMessage(content=quality_prompt)])
        
        # Parse scores (simplified parsing)
        scores = {}
        for line in quality_response.content.split('\n'):
            if ':' in line:
                key, value = line.split(':', 1)
                try:
                    scores[key.strip()] = float(value.strip())
                except:
                    pass
                    
        return scores
        
    def _analyze_tone(self, response: str) -> Dict[str, str]:
        """Analyze the tone of the response."""
        tone_prompt = f"""
        Analyze the tone of this response:
        
        {response}
        
        Identify the tone characteristics:
        """
        
        tone_response = self.llm.invoke([HumanMessage(content=tone_prompt)])
        
        return {
            "tone_description": tone_response.content,
            "is_empathetic": "empathetic" in tone_response.content.lower(),
            "is_professional": "professional" in tone_response.content.lower(),
            "is_encouraging": "encouraging" in tone_response.content.lower()
        }
        
    def _calculate_empathy_score(self, response: str) -> float:
        """Calculate empathy score of the response."""
        empathy_indicators = [
            "understand", "concern", "stress", "difficult", "challenging",
            "support", "help", "assist", "guide", "encourage"
        ]
        
        score = 0
        for indicator in empathy_indicators:
            if indicator in response.lower():
                score += 1
                
        return min(score / len(empathy_indicators) * 10, 10)
        
    def _calculate_clarity_score(self, response: str) -> float:
        """Calculate clarity score of the response."""
        clarity_indicators = [
            "first", "second", "next", "then", "finally",
            "step", "process", "procedure", "deadline", "requirement"
        ]
        
        score = 0
        for indicator in clarity_indicators:
            if indicator in response.lower():
                score += 1
                
        return min(score / len(clarity_indicators) * 10, 10)
        
    def _assess_priority_level(self, query: str) -> str:
        """Assess the priority level of the query."""
        high_priority_keywords = ["deadline", "urgent", "immediate", "payment", "default"]
        medium_priority_keywords = ["application", "process", "requirement", "eligibility"]
        
        query_lower = query.lower()
        
        if any(keyword in query_lower for keyword in high_priority_keywords):
            return "High"
        elif any(keyword in query_lower for keyword in medium_priority_keywords):
            return "Medium"
        else:
            return "Low"
            
    def _estimate_timeline(self, query: str) -> str:
        """Estimate timeline for addressing the query."""
        query_lower = query.lower()
        
        if "deadline" in query_lower or "urgent" in query_lower:
            return "Immediate (1-2 days)"
        elif "application" in query_lower or "process" in query_lower:
            return "Short-term (1-2 weeks)"
        else:
            return "Medium-term (1-3 months)"


if __name__ == "__main__":
    # Example usage
    print("Response agent module loaded") 