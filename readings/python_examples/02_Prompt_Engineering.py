#!/usr/bin/env python3
"""
🎯 Prompt Engineering Complete Guide
===================================

This file covers the art and science of crafting effective prompts to get the best 
possible responses from AI language models.

What you'll learn:
1. What is Prompt Engineering?
2. Basic Prompt Engineering Techniques
3. Advanced Techniques (Chain of Thought, Few-Shot Learning)
4. Prompt Templates and Best Practices
5. Interactive Prompt Builder
6. Prompt Evaluation Framework

Author: AI Learning Guide
Date: 2024
"""

import json
import time
import hashlib
import re
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from abc import ABC, abstractmethod

# =============================================================================
# SECTION 1: WHAT IS PROMPT ENGINEERING?
# =============================================================================

"""
Prompt Engineering is the art and science of crafting effective instructions (prompts) 
to get the best possible responses from AI language models. Think of it as learning 
to "speak AI" - you need to know how to ask questions in a way that the AI understands 
and can respond to effectively.

Why Prompt Engineering Matters:
- AI models are very literal and do exactly what you ask
- Vague instructions = vague responses
- Unclear context = confusing answers
- Missing details = incomplete results

Good prompt engineering helps you:
- Get more accurate and relevant responses
- Save time by getting the right answer the first time
- Control the style, tone, and format of responses
- Avoid common AI pitfalls and biases
"""

def print_prompt_engineering_overview():
    """Print an overview of Prompt Engineering"""
    print("🎯 Prompt Engineering Overview")
    print("=" * 50)
    
    concepts = {
        "Definition": "The art of writing instructions that get the best responses from AI models",
        "Purpose": "To communicate effectively with AI systems",
        "Key Principle": "Be specific, clear, and provide context",
        "Common Mistake": "Being too vague or unclear",
        "Best Practice": "Iterate and improve prompts based on responses"
    }
    
    for concept, description in concepts.items():
        print(f"📌 {concept}: {description}")
    
    print("\n💡 Think of prompt engineering as learning to ask questions in the right way!")

# =============================================================================
# SECTION 2: SIMPLE AI SIMULATOR
# =============================================================================

class SimpleAISimulator:
    """A simple AI simulator to demonstrate prompt engineering concepts"""
    
    def __init__(self):
        self.knowledge_base = {
            "python": "Python is a high-level programming language known for its simplicity and readability.",
            "ai": "Artificial Intelligence is technology that enables computers to perform human-like tasks.",
            "machine_learning": "Machine Learning is a subset of AI that allows systems to learn from data.",
            "data_science": "Data Science combines statistics, programming, and domain expertise to extract insights from data.",
            "deep_learning": "Deep Learning uses neural networks with multiple layers to learn complex patterns in data."
        }
        
        self.response_templates = {
            "explanation": "Here's a detailed explanation: {content}",
            "code_example": "Here's a code example:\n\n```python\n{code}\n```",
            "comparison": "Let me compare these concepts:\n\n{content}",
            "step_by_step": "Here's a step-by-step guide:\n\n{content}"
        }
    
    def generate_response(self, prompt: str) -> str:
        """Simulate AI response based on prompt quality"""
        prompt_lower = prompt.lower()
        
        # Check for specific topics
        for topic, info in self.knowledge_base.items():
            if topic in prompt_lower:
                if "explain" in prompt_lower or "what is" in prompt_lower:
                    return self.response_templates["explanation"].format(content=info)
                elif "code" in prompt_lower or "example" in prompt_lower:
                    code_example = f"# Example of {topic}\nprint('Hello, {topic.title()}!')\n\n# Basic usage\ndef {topic}_example():\n    return 'This is {topic} in action'"
                    return self.response_templates["code_example"].format(code=code_example)
                elif "compare" in prompt_lower or "difference" in prompt_lower:
                    return self.response_templates["comparison"].format(content=f"{info}\n\nThis differs from other concepts in its approach and application.")
                elif "step" in prompt_lower or "guide" in prompt_lower:
                    steps = f"1. Understand the basics\n2. Learn the fundamentals\n3. Practice with examples\n4. Apply to real projects"
                    return self.response_templates["step_by_step"].format(content=steps)
        
        # Check for greetings
        if any(word in prompt_lower for word in ["hello", "hi", "hey"]):
            return "Hello! How can I help you today?"
        
        # Check for help requests
        if "help" in prompt_lower:
            return "I can help you with Python, AI, machine learning, data science, and deep learning. Just ask me specific questions!"
        
        return "I'm not sure how to respond to that. Could you be more specific?"

# =============================================================================
# SECTION 3: BASIC PROMPT ENGINEERING TECHNIQUES
# =============================================================================

def demonstrate_basic_techniques():
    """Demonstrate basic prompt engineering techniques"""
    print("\n📝 Basic Prompt Engineering Techniques")
    print("=" * 45)
    
    ai_simulator = SimpleAISimulator()
    
    # 1. Be Specific and Clear
    print("\n1. Be Specific and Clear:")
    print("-" * 30)
    
    bad_prompts = [
        "Tell me about dogs",
        "Help me with my project",
        "Write something about AI"
    ]
    
    good_prompts = [
        "Write a 3-paragraph explanation of why golden retrievers make excellent family pets, focusing on their temperament, trainability, and health considerations.",
        "I'm building a Python web scraper for e-commerce sites. I need help with handling pagination and rate limiting. Can you provide code examples?",
        "Write a 500-word blog post about how AI is transforming small business operations in 2024, including 3 specific examples and actionable next steps."
    ]
    
    print("❌ Bad Prompt Examples:")
    for i, prompt in enumerate(bad_prompts, 1):
        print(f"  {i}. '{prompt}'")
        print(f"     Response: {ai_simulator.generate_response(prompt)}")
        print()
    
    print("✅ Good Prompt Examples:")
    for i, prompt in enumerate(good_prompts, 1):
        print(f"  {i}. '{prompt}'")
        print(f"     Response: {ai_simulator.generate_response(prompt)}")
        print()

def demonstrate_context_providing():
    """Demonstrate how to provide context in prompts"""
    print("\n2. Provide Context:")
    print("-" * 20)
    
    context_examples = [
        {
            "context": "You are a medical professional.",
            "prompt": "Please summarize the following patient symptoms in medical terminology, highlighting any concerning patterns.",
            "data": "Patient reports headache, fever, and fatigue for 3 days."
        },
        {
            "context": "You are an experienced software engineer with 10 years of experience.",
            "prompt": "Write a clear, technical explanation of how to implement a binary search algorithm, suitable for a junior developer.",
            "data": ""
        },
        {
            "context": "You are a business consultant specializing in startups.",
            "prompt": "Analyze this business idea and provide feedback on market potential, risks, and next steps.",
            "data": "Mobile app for connecting local farmers with consumers."
        }
    ]
    
    for i, example in enumerate(context_examples, 1):
        print(f"\nExample {i}:")
        print(f"Context: {example['context']}")
        print(f"Prompt: {example['prompt']}")
        if example['data']:
            print(f"Data: {example['data']}")
        print("-" * 40)

# =============================================================================
# SECTION 4: FEW-SHOT LEARNING
# =============================================================================

def demonstrate_few_shot_learning():
    """Demonstrate few-shot learning with examples"""
    print("\n3. Few-Shot Learning (Examples):")
    print("-" * 35)
    
    # Email response examples
    few_shot_prompt = """
Here are some examples of professional email responses:

Input: "Can we reschedule our meeting?"
Output: "Thank you for reaching out. I'd be happy to reschedule our meeting. Could you please let me know what times work best for you this week?"

Input: "The project deadline has been moved up"
Output: "I understand the deadline has been accelerated. Let me review our current progress and provide an updated timeline by end of day."

Now, please respond to this email in a similar professional tone:
Input: "Can you send me the quarterly report?"
Output:
"""
    
    print("📝 Few-Shot Learning Example:")
    print("=" * 35)
    print(few_shot_prompt)
    
    # Code review examples
    code_review_prompt = """
Here are examples of code review feedback:

Code: "def add(a, b): return a + b"
Feedback: "Good simple function. Consider adding type hints and docstring for better documentation."

Code: "for i in range(len(items)): print(items[i])"
Feedback: "Use enumerate() instead of range(len()) for better Pythonic code: 'for i, item in enumerate(items): print(item)'"

Now review this code:
Code: "def calculate_average(numbers): return sum(numbers) / len(numbers)"
Feedback:
"""
    
    print("\n🔍 Code Review Few-Shot Example:")
    print("=" * 35)
    print(code_review_prompt)

# =============================================================================
# SECTION 5: OUTPUT FORMAT SPECIFICATION
# =============================================================================

def demonstrate_output_formatting():
    """Demonstrate how to specify output formats"""
    print("\n4. Specify Output Format:")
    print("-" * 30)
    
    structured_prompts = [
        {
            "name": "Customer Feedback Analysis",
            "prompt": """
Analyze the following customer feedback and provide insights in this exact format:

**Positive Aspects:**
- [List 2-3 positive points]

**Areas for Improvement:**
- [List 2-3 areas to improve]

**Action Items:**
- [List 2-3 specific actions to take]

**Priority Level:** [High/Medium/Low]

Customer Feedback: [Insert feedback here]
"""
        },
        {
            "name": "Code Review",
            "prompt": """
Please review this Python function and provide feedback in this format:

**Code Quality:** [Score 1-10 with explanation]
**Potential Issues:** [List any bugs or problems]
**Suggestions:** [List 2-3 improvement suggestions]
**Security Concerns:** [Any security issues?]

Function:
[Insert code here]
"""
        },
        {
            "name": "Data Analysis Report",
            "prompt": """
Analyze this dataset and provide a report in this format:

**Dataset Overview:**
- Number of records: [count]
- Key columns: [list]
- Data quality: [assessment]

**Key Findings:**
1. [Finding 1]
2. [Finding 2]
3. [Finding 3]

**Recommendations:**
- [Recommendation 1]
- [Recommendation 2]

**Next Steps:**
[Action items]
"""
        }
    ]
    
    for example in structured_prompts:
        print(f"\n{example['name']}:")
        print(example['prompt'])
        print("-" * 40)

# =============================================================================
# SECTION 6: CHAIN OF THOUGHT (COT)
# =============================================================================

def demonstrate_chain_of_thought():
    """Demonstrate Chain of Thought reasoning"""
    print("\n5. Chain of Thought (CoT):")
    print("-" * 30)
    
    # Math problem example
    math_cot_prompt = """
Let's solve this math problem step by step:

Problem: If a store sells apples for $2 each and oranges for $3 each, and I buy 5 apples and 3 oranges, how much do I spend?

Let's break this down:
1. First, calculate the cost of apples
2. Then, calculate the cost of oranges  
3. Finally, add them together

Please show your work for each step.
"""
    
    print("🧮 Math Problem CoT Example:")
    print("=" * 35)
    print(math_cot_prompt)
    
    # Simulate CoT response
    cot_response = """
Let me solve this step by step:

1. Cost of apples:
   - 5 apples × $2 each = $10

2. Cost of oranges:
   - 3 oranges × $3 each = $9

3. Total cost:
   - $10 + $9 = $19

Answer: You spend $19 total.
"""
    
    print("\n🤖 AI Response:")
    print(cot_response)
    
    # Programming problem example
    programming_cot_prompt = """
Let's solve this programming problem step by step:

Problem: Write a function to find the longest word in a list of strings.

Let's break this down:
1. First, understand what we need to do
2. Then, think about the algorithm
3. Finally, write the code

Please show your reasoning for each step.
"""
    
    print("\n💻 Programming Problem CoT Example:")
    print("=" * 40)
    print(programming_cot_prompt)

# =============================================================================
# SECTION 7: PROMPT TEMPLATES
# =============================================================================

class PromptTemplates:
    """A collection of reusable prompt templates"""
    
    @staticmethod
    def code_review(language: str, code: str, focus_areas: List[str]) -> str:
        """Generate a code review prompt"""
        return f"""
Please review this {language} code for:
- {', '.join(focus_areas)}

Code:
{code}

Please provide specific suggestions with code examples where appropriate.
"""
    
    @staticmethod
    def content_creation(content_type: str, topic: str, target_audience: str, word_count: int) -> str:
        """Generate a content creation prompt"""
        return f"""
You are a professional content writer. Write a {word_count}-word {content_type} about "{topic}".

Target audience: {target_audience}

Requirements:
- Use a conversational, professional tone
- Include relevant examples and data
- End with actionable insights
- Include 3-4 subheadings to break up the content
"""
    
    @staticmethod
    def data_analysis(dataset_description: str, analysis_type: str) -> str:
        """Generate a data analysis prompt"""
        return f"""
You are a data analyst. Please analyze this dataset and provide insights:

Dataset: {dataset_description}
Analysis Type: {analysis_type}

Please provide:
1. Key findings (3-5 insights)
2. Data quality assessment
3. Recommendations for next steps
4. Suggested visualizations
"""
    
    @staticmethod
    def translation(text: str, source_language: str, target_language: str, style: str = "formal") -> str:
        """Generate a translation prompt"""
        return f"""
Please translate the following text from {source_language} to {target_language} in a {style} style:

Text: {text}

Please maintain the original meaning and tone while ensuring natural flow in the target language.
"""
    
    @staticmethod
    def summarization(text: str, summary_length: str = "medium", focus_areas: List[str] = None) -> str:
        """Generate a summarization prompt"""
        focus_text = ""
        if focus_areas:
            focus_text = f"\nFocus on: {', '.join(focus_areas)}"
        
        return f"""
Please provide a {summary_length} summary of the following text:{focus_text}

Text: {text}

Please include the key points and main ideas while maintaining clarity and coherence.
"""

def demonstrate_prompt_templates():
    """Demonstrate the use of prompt templates"""
    print("\n6. Prompt Templates:")
    print("=" * 25)
    
    templates = PromptTemplates()
    
    # Code review template
    code_review_prompt = templates.code_review(
        "Python",
        "def calculate_average(numbers):\n    return sum(numbers) / len(numbers)",
        ["code quality", "error handling", "performance"]
    )
    print("\n🔍 Code Review Template:")
    print(code_review_prompt)
    
    # Content creation template
    content_prompt = templates.content_creation(
        "blog post",
        "AI in Healthcare",
        "healthcare professionals",
        800
    )
    print("\n✍️ Content Creation Template:")
    print(content_prompt)
    
    # Data analysis template
    data_prompt = templates.data_analysis(
        "Customer satisfaction survey with 1000 responses",
        "sentiment analysis"
    )
    print("\n📊 Data Analysis Template:")
    print(data_prompt)

# =============================================================================
# SECTION 8: INTERACTIVE PROMPT BUILDER
# =============================================================================

@dataclass
class PromptBuilder:
    """Interactive prompt builder"""
    
    def build_prompt(self) -> str:
        """Build a prompt interactively"""
        print("\n🔧 Interactive Prompt Builder")
        print("=" * 35)
        
        # Get user input
        task = input("What task do you want the AI to perform? ")
        context = input("What context should the AI have? (e.g., 'You are a...') ")
        format_pref = input("Any specific output format? (e.g., 'Provide in bullet points') ")
        examples = input("Do you want to include examples? (y/n) ").lower() == 'y'
        length = input("How detailed should the response be? (brief/medium/detailed) ")
        
        # Build the prompt
        prompt_parts = []
        
        if context:
            prompt_parts.append(context)
        
        prompt_parts.append(f"Please {task}.")
        
        if format_pref:
            prompt_parts.append(f"{format_pref}.")
        
        if examples:
            prompt_parts.append("Please include relevant examples.")
        
        if length:
            prompt_parts.append(f"Provide a {length} response.")
        
        final_prompt = " ".join(prompt_parts)
        
        print(f"\n🎯 Your Generated Prompt:")
        print(f"\n{final_prompt}")
        
        return final_prompt

# =============================================================================
# SECTION 9: PROMPT EVALUATION FRAMEWORK
# =============================================================================

@dataclass
class PromptEvaluation:
    """Evaluate prompt quality"""
    specificity_score: float
    context_score: float
    format_score: float
    examples_score: float
    length_score: float
    overall_score: float
    feedback: Dict[str, str]

class PromptEvaluator:
    """Evaluate prompts based on multiple criteria"""
    
    def __init__(self):
        self.criteria = {
            "specificity": "Is the prompt specific and clear?",
            "context": "Does it provide sufficient context?",
            "format": "Does it specify the desired output format?",
            "examples": "Does it include relevant examples?",
            "length": "Is the prompt an appropriate length?"
        }
    
    def evaluate_prompt(self, prompt: str) -> PromptEvaluation:
        """Evaluate a prompt based on multiple criteria"""
        scores = {}
        feedback = {}
        
        # Specificity check
        word_count = len(prompt.split())
        specificity_score = min(10, word_count * 0.5)  # Simple heuristic
        scores["specificity"] = specificity_score
        feedback["specificity"] = "Good length" if specificity_score > 5 else "Consider adding more details"
        
        # Context check
        context_words = ["you are", "as a", "in the role of", "acting as"]
        has_context = any(word in prompt.lower() for word in context_words)
        scores["context"] = 10 if has_context else 3
        feedback["context"] = "Good context provided" if has_context else "Consider adding role/context"
        
        # Format check
        format_words = ["format", "structure", "list", "bullet", "paragraph"]
        has_format = any(word in prompt.lower() for word in format_words)
        scores["format"] = 10 if has_format else 5
        feedback["format"] = "Output format specified" if has_format else "Consider specifying output format"
        
        # Examples check
        example_words = ["example", "for instance", "such as", "like"]
        has_examples = any(word in prompt.lower() for word in example_words)
        scores["examples"] = 10 if has_examples else 5
        feedback["examples"] = "Examples included" if has_examples else "Consider adding examples"
        
        # Length check
        if word_count < 10:
            length_score = 3
            length_feedback = "Too short - add more details"
        elif word_count < 50:
            length_score = 7
            length_feedback = "Good length"
        else:
            length_score = 10
            length_feedback = "Comprehensive prompt"
        
        scores["length"] = length_score
        feedback["length"] = length_feedback
        
        # Overall score
        overall_score = sum(scores.values()) / len(scores)
        
        return PromptEvaluation(
            specificity_score=scores["specificity"],
            context_score=scores["context"],
            format_score=scores["format"],
            examples_score=scores["examples"],
            length_score=scores["length"],
            overall_score=overall_score,
            feedback=feedback
        )
    
    def display_evaluation(self, evaluation: PromptEvaluation):
        """Display evaluation results"""
        print(f"\n📊 Prompt Evaluation Results:")
        print(f"Overall Score: {evaluation.overall_score:.1f}/10")
        print(f"Word Count: {len(evaluation.feedback)}")
        
        criteria_scores = [
            ("Specificity", evaluation.specificity_score),
            ("Context", evaluation.context_score),
            ("Format", evaluation.format_score),
            ("Examples", evaluation.examples_score),
            ("Length", evaluation.length_score)
        ]
        
        for criterion, score in criteria_scores:
            print(f"  {criterion}: {score}/10 - {evaluation.feedback[criterion.lower()]}")

def demonstrate_prompt_evaluation():
    """Demonstrate prompt evaluation"""
    print("\n7. Prompt Evaluation:")
    print("=" * 25)
    
    evaluator = PromptEvaluator()
    
    test_prompts = [
        "Write about AI",  # Bad prompt
        "You are an AI expert. Write a 500-word blog post about the future of artificial intelligence, including 3 specific examples and actionable insights for business leaders. Format the response with clear headings and bullet points."  # Good prompt
    ]
    
    for i, prompt in enumerate(test_prompts, 1):
        print(f"\nPrompt {i}: {prompt[:50]}...")
        evaluation = evaluator.evaluate_prompt(prompt)
        evaluator.display_evaluation(evaluation)

# =============================================================================
# SECTION 10: PRACTICAL EXERCISES
# =============================================================================

def provide_practice_exercises():
    """Provide practice exercises for prompt engineering"""
    print("\n📝 Practice Exercises:")
    print("=" * 25)
    
    exercises = [
        {
            "task": "Create a social media post",
            "topic": "new product launch",
            "requirements": "Engaging, include call-to-action, 100 words max"
        },
        {
            "task": "Debug a coding error",
            "topic": "Python function not working",
            "requirements": "Include error message, explain the fix, provide corrected code"
        },
        {
            "task": "Analyze customer feedback",
            "topic": "restaurant reviews",
            "requirements": "Identify trends, provide actionable insights, format as report"
        },
        {
            "task": "Write a creative story",
            "topic": "robot finding friendship",
            "requirements": "150 words, include dialogue, happy ending"
        }
    ]
    
    for i, exercise in enumerate(exercises, 1):
        print(f"\nExercise {i}:")
        print(f"Task: {exercise['task']}")
        print(f"Topic: {exercise['topic']}")
        print(f"Requirements: {exercise['requirements']}")
        print("\nYour prompt should:")
        print("✅ Be specific about the task")
        print("✅ Include context and role")
        print("✅ Specify output format")
        print("✅ Include requirements")
        print("-" * 40)

# =============================================================================
# SECTION 11: PROMPT ENGINEERING BEST PRACTICES
# =============================================================================

def demonstrate_best_practices():
    """Demonstrate prompt engineering best practices"""
    print("\n💡 Prompt Engineering Best Practices:")
    print("=" * 40)
    
    best_practices = [
        {
            "practice": "Start Simple, Then Iterate",
            "description": "Begin with basic prompts and improve based on responses",
            "example": "Start with 'Explain AI' then refine to 'Explain AI to a 10-year-old in 3 sentences'"
        },
        {
            "practice": "Use Templates",
            "description": "Create reusable prompt templates for common tasks",
            "example": "Have templates for code review, content creation, data analysis"
        },
        {
            "practice": "Test with Different Models",
            "description": "Different AI models may respond differently to the same prompt",
            "example": "Test your prompts with ChatGPT, Claude, and other models"
        },
        {
            "practice": "Document Your Prompts",
            "description": "Keep a library of effective prompts for future use",
            "example": "Maintain a prompt database with notes on what works and what doesn't"
        },
        {
            "practice": "Consider the User Experience",
            "description": "Think about how the AI response will be used",
            "example": "Structure prompts to generate user-friendly outputs"
        }
    ]
    
    for i, practice in enumerate(best_practices, 1):
        print(f"\n{i}. {practice['practice']}:")
        print(f"   {practice['description']}")
        print(f"   Example: {practice['example']}")

# =============================================================================
# MAIN EXECUTION
# =============================================================================

def main():
    """Main function to run all prompt engineering demonstrations"""
    print("🎯 Prompt Engineering Complete Guide")
    print("=" * 50)
    print("This file contains comprehensive examples and explanations for Prompt Engineering.")
    print("Run individual functions to explore different concepts.\n")
    
    # Run all demonstrations
    print_prompt_engineering_overview()
    demonstrate_basic_techniques()
    demonstrate_context_providing()
    demonstrate_few_shot_learning()
    demonstrate_output_formatting()
    demonstrate_chain_of_thought()
    demonstrate_prompt_templates()
    demonstrate_prompt_evaluation()
    provide_practice_exercises()
    demonstrate_best_practices()
    
    print("\n🎉 Congratulations! You've completed the Prompt Engineering section!")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Practice the techniques shown above")
    print("2. Try the interactive prompt builder")
    print("3. Evaluate your own prompts")
    print("4. Build a prompt library")
    print("5. Explore the other Python files in this folder")
    
    print("\n💡 To use the interactive prompt builder, uncomment the line below:")
    print("# PromptBuilder().build_prompt()")

if __name__ == "__main__":
    main()
    
    # Uncomment the line below to use interactive prompt builder
    # PromptBuilder().build_prompt() 