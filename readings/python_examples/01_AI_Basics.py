#!/usr/bin/env python3
"""
🤖 AI Learning Path - Basics
============================

This file covers the fundamental concepts of AI Engineering with detailed explanations
and working Python code examples.

What you'll learn:
1. What is AI Engineering?
2. Basic Python for AI
3. Your first AI application
4. Core AI concepts
5. Setting up your environment

Author: AI Learning Guide
Date: 2024
"""

import sys
import platform
import json
import time
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from abc import ABC, abstractmethod

# =============================================================================
# SECTION 1: WHAT IS AI ENGINEERING?
# =============================================================================

"""
AI Engineering is the practice of building, deploying, and maintaining AI applications 
in real-world environments. Think of it as the bridge between AI research and practical 
applications that people actually use.

Key Areas:
- Prompt Engineering: Teaching AI models how to respond effectively
- RAG (Retrieval Augmented Generation): Making AI smarter with external knowledge
- Agents: Creating AI that can take actions and make decisions
- Fine-tuning: Customizing AI models for specific tasks
- Production Deployment: Making AI applications reliable and scalable
"""

def print_ai_engineering_overview():
    """Print an overview of AI Engineering"""
    print("🎯 AI Engineering Overview")
    print("=" * 50)
    
    areas = {
        "Prompt Engineering": "Teaching AI models how to respond effectively",
        "RAG Systems": "Making AI smarter by giving it access to knowledge",
        "AI Agents": "Creating AI that can take actions and make decisions",
        "Fine-tuning": "Customizing AI models for specific tasks",
        "Production Deployment": "Making AI applications reliable and scalable"
    }
    
    for area, description in areas.items():
        print(f"📌 {area}: {description}")
    
    print("\n💡 Think of AI Engineering as building the bridge between AI research and real-world applications!")

# =============================================================================
# SECTION 2: ENVIRONMENT SETUP AND CHECK
# =============================================================================

def check_environment():
    """Check if your Python environment is ready for AI development"""
    print("\n🔧 Environment Check")
    print("=" * 30)
    
    # Check Python version
    print(f"🐍 Python version: {sys.version}")
    print(f"🖥️  Platform: {platform.system()} {platform.release()}")
    print(f"🏗️  Architecture: {platform.machine()}")
    
    # Check required libraries
    required_libraries = [
        "numpy", "pandas", "requests", "json", "time", "typing"
    ]
    
    print("\n📦 Checking required libraries:")
    for lib in required_libraries:
        try:
            __import__(lib)
            print(f"  ✅ {lib} - Available")
        except ImportError:
            print(f"  ❌ {lib} - Not installed")
    
    # Check optional libraries
    optional_libraries = [
        "openai", "langchain", "transformers", "torch", "tensorflow"
    ]
    
    print("\n📚 Optional AI libraries:")
    for lib in optional_libraries:
        try:
            __import__(lib)
            print(f"  ✅ {lib} - Available")
        except ImportError:
            print(f"  ⚠️  {lib} - Not installed (optional)")
    
    print("\n💡 If you see ❌ marks, install missing libraries with: pip install library_name")

# =============================================================================
# SECTION 3: BASIC PYTHON FOR AI
# =============================================================================

def demonstrate_python_basics():
    """Demonstrate essential Python concepts for AI development"""
    print("\n🐍 Python Basics for AI")
    print("=" * 30)
    
    # 1. Variables and Data Types
    print("\n1. Variables and Data Types:")
    text = "Hello, AI World!"  # String
    number = 42                 # Integer
    decimal = 3.14             # Float
    is_ai_cool = True          # Boolean
    ai_list = ["GPT", "Claude", "Llama"]  # List
    ai_dict = {"OpenAI": "GPT-4", "Anthropic": "Claude"}  # Dictionary
    
    print(f"Text: {text} (type: {type(text)})")
    print(f"Number: {number} (type: {type(number)})")
    print(f"Decimal: {decimal} (type: {type(decimal)})")
    print(f"Boolean: {is_ai_cool} (type: {type(is_ai_cool)})")
    print(f"List: {ai_list} (type: {type(ai_list)})")
    print(f"Dictionary: {ai_dict} (type: {type(ai_dict)})")
    
    # 2. Functions
    print("\n2. Functions:")
    
    def greet_ai(name: str) -> str:
        """A simple function to greet an AI"""
        return f"Hello, {name}! Welcome to AI Engineering!"
    
    def calculate_ai_score(accuracy: float, speed: float, cost: float) -> float:
        """Calculate a score for an AI model"""
        return (accuracy * 0.5) + (speed * 0.3) + (cost * 0.2)
    
    # Test the functions
    print(greet_ai("ChatGPT"))
    print(f"AI Score: {calculate_ai_score(0.9, 0.8, 0.7):.2f}")
    
    # 3. Working with Lists and Dictionaries
    print("\n3. Working with Lists and Dictionaries:")
    
    # AI Models list
    ai_models = [
        {"name": "GPT-4", "company": "OpenAI", "type": "Language Model"},
        {"name": "Claude", "company": "Anthropic", "type": "Language Model"},
        {"name": "Llama", "company": "Meta", "type": "Language Model"},
        {"name": "DALL-E", "company": "OpenAI", "type": "Image Generation"}
    ]
    
    # Filter models by type
    language_models = [model for model in ai_models if model["type"] == "Language Model"]
    print(f"Language Models: {[model['name'] for model in language_models]}")
    
    # Group by company
    companies = {}
    for model in ai_models:
        company = model["company"]
        if company not in companies:
            companies[company] = []
        companies[company].append(model["name"])
    
    print(f"\nModels by Company:")
    for company, models in companies.items():
        print(f"  {company}: {', '.join(models)}")

# =============================================================================
# SECTION 4: WORKING WITH APIs
# =============================================================================

def demonstrate_api_usage():
    """Demonstrate how to work with APIs (essential for AI development)"""
    print("\n🌐 Working with APIs")
    print("=" * 25)
    
    # Simulate API response
    def simulate_api_call(url: str, params: Optional[Dict] = None) -> Dict:
        """Simulate an API call for demonstration"""
        print(f"Making request to: {url}")
        if params:
            print(f"Parameters: {params}")
        
        # Simulate response
        response = {
            "status": "success",
            "data": {
                "message": "This is a simulated API response",
                "timestamp": "2024-01-01T12:00:00Z"
            }
        }
        
        return response
    
    # Example: Weather API simulation
    def get_weather_data(city: str) -> Dict:
        """Example function to get weather data (simulated)"""
        weather_data = {
            "city": city,
            "temperature": 22,
            "condition": "sunny",
            "humidity": 65
        }
        return weather_data
    
    # Test the functions
    weather = get_weather_data("San Francisco")
    print(f"Weather in {weather['city']}: {weather['temperature']}°C, {weather['condition']}")
    
    api_response = simulate_api_call("https://api.example.com/data", {"query": "AI"})
    print(f"\nAPI Response: {json.dumps(api_response, indent=2)}")

# =============================================================================
# SECTION 5: CORE AI CONCEPTS
# =============================================================================

def demonstrate_ai_concepts():
    """Demonstrate core AI concepts with simple implementations"""
    print("\n🧠 Core AI Concepts")
    print("=" * 25)
    
    # 1. Large Language Models (LLMs)
    print("\n1. Large Language Models (LLMs):")
    print("   - AI systems trained on massive amounts of text data")
    print("   - Can understand and generate human-like text")
    print("   - Examples: ChatGPT, Claude, GPT-4")
    
    # Simulate LLM behavior
    def simple_llm_response(prompt: str) -> str:
        """Simulate a simple LLM response"""
        responses = {
            "hello": "Hello! How can I help you today?",
            "what is ai": "AI (Artificial Intelligence) is technology that enables computers to perform tasks that typically require human intelligence.",
            "how are you": "I'm functioning well, thank you for asking! How can I assist you?"
        }
        
        prompt_lower = prompt.lower()
        for key, response in responses.items():
            if key in prompt_lower:
                return response
        
        return "I'm not sure how to respond to that. Could you rephrase your question?"
    
    # Test the simple LLM
    test_prompts = ["Hello", "What is AI?", "How are you?", "Tell me a joke"]
    for prompt in test_prompts:
        response = simple_llm_response(prompt)
        print(f"\nUser: {prompt}")
        print(f"AI: {response}")
    
    # 2. Prompt Engineering
    print("\n2. Prompt Engineering:")
    print("   - The art of writing instructions for AI models")
    print("   - Getting the best responses by asking the right way")
    
    def demonstrate_prompt_engineering():
        """Show the difference between good and bad prompts"""
        
        # Bad prompt example
        bad_prompt = "Tell me about dogs"
        
        # Good prompt example
        good_prompt = "Write a 3-paragraph explanation of why golden retrievers make excellent family pets, focusing on their temperament, trainability, and health considerations."
        
        print("\nBad Prompt:")
        print(f"  '{bad_prompt}'")
        print("  Problems: Too vague, no specific requirements")
        
        print("\nGood Prompt:")
        print(f"  '{good_prompt}'")
        print("  Benefits: Specific, clear requirements, focused topic")
        
        return bad_prompt, good_prompt
    
    bad, good = demonstrate_prompt_engineering()
    
    # 3. Embeddings
    print("\n3. Embeddings:")
    print("   - Mathematical representations of text that capture meaning")
    print("   - Allow computers to understand relationships between words")
    
    # Simple embedding simulation
    def create_simple_embedding(text: str) -> List[float]:
        """Create a simple numerical representation of text"""
        # This is a very simplified embedding - real embeddings are much more complex
        words = text.lower().split()
        embedding = [0.0] * 10  # 10-dimensional vector
        
        for i, word in enumerate(words):
            # Simple hash-based embedding
            hash_val = hash(word) % 10
            embedding[hash_val] += 1
        
        return embedding
    
    def calculate_similarity(embedding1: List[float], embedding2: List[float]) -> float:
        """Calculate similarity between two embeddings"""
        import math
        dot_product = sum(a * b for a, b in zip(embedding1, embedding2))
        norm1 = math.sqrt(sum(a * a for a in embedding1))
        norm2 = math.sqrt(sum(b * b for b in embedding2))
        return dot_product / (norm1 * norm2) if norm1 * norm2 != 0 else 0
    
    # Test embeddings
    text1 = "machine learning"
    text2 = "artificial intelligence"
    text3 = "cooking recipes"
    
    emb1 = create_simple_embedding(text1)
    emb2 = create_simple_embedding(text2)
    emb3 = create_simple_embedding(text3)
    
    print(f"\nEmbedding for '{text1}': {emb1}")
    print(f"Embedding for '{text2}': {emb2}")
    print(f"Embedding for '{text3}': {emb3}")
    
    similarity_12 = calculate_similarity(emb1, emb2)
    similarity_13 = calculate_similarity(emb1, emb3)
    
    print(f"\nSimilarity between '{text1}' and '{text2}': {similarity_12:.3f}")
    print(f"Similarity between '{text1}' and '{text3}': {similarity_13:.3f}")

# =============================================================================
# SECTION 6: YOUR FIRST AI APPLICATION
# =============================================================================

@dataclass
class ChatMessage:
    """Represents a chat message"""
    role: str  # 'user' or 'assistant'
    content: str
    timestamp: str

class SimpleAIChatbot:
    """A simple AI chatbot implementation"""
    
    def __init__(self):
        self.conversation_history: List[ChatMessage] = []
        self.personality = "helpful and friendly"
        
        # Simple knowledge base
        self.knowledge_base = {
            "ai": "Artificial Intelligence (AI) is technology that enables computers to perform tasks that typically require human intelligence.",
            "machine learning": "Machine Learning is a subset of AI that allows computers to learn and improve from experience without being explicitly programmed.",
            "python": "Python is a popular programming language for AI and machine learning due to its simplicity and rich ecosystem of libraries.",
            "chatbot": "A chatbot is a computer program designed to simulate conversation with human users, especially over the internet."
        }
    
    def generate_response(self, user_input: str) -> str:
        """Generate a response based on user input"""
        user_input_lower = user_input.lower()
        
        # Check for greetings
        if any(word in user_input_lower for word in ["hello", "hi", "hey"]):
            return "Hello! I'm your AI assistant. How can I help you learn about AI today?"
        
        # Check for questions about AI topics
        for topic, explanation in self.knowledge_base.items():
            if topic in user_input_lower:
                return f"{explanation}"
        
        # Check for help requests
        if "help" in user_input_lower:
            return "I can help you learn about AI, machine learning, Python, and chatbots. Just ask me questions!"
        
        # Default response
        return "I'm not sure about that. Try asking me about AI, machine learning, Python, or chatbots!"
    
    def chat(self, user_input: str) -> str:
        """Process a chat message and return response"""
        # Add to conversation history
        self.conversation_history.append(ChatMessage("user", user_input, time.strftime("%H:%M:%S")))
        
        # Generate response
        response = self.generate_response(user_input)
        
        # Add response to history
        self.conversation_history.append(ChatMessage("assistant", response, time.strftime("%H:%M:%S")))
        
        return response
    
    def get_conversation_summary(self) -> str:
        """Get a summary of the conversation"""
        return f"Conversation has {len(self.conversation_history)} messages"
    
    def display_conversation_history(self):
        """Display the full conversation history"""
        print("\n📜 Conversation History:")
        print("-" * 30)
        for message in self.conversation_history:
            emoji = "👤" if message.role == "user" else "🤖"
            print(f"{emoji} {message.role.title()}: {message.content}")

def demonstrate_chatbot():
    """Demonstrate the AI chatbot"""
    print("\n🤖 Building Your First AI Chatbot")
    print("=" * 40)
    
    # Create and test the chatbot
    chatbot = SimpleAIChatbot()
    
    # Test conversation
    test_messages = [
        "Hello!",
        "What is AI?",
        "Tell me about machine learning",
        "How can you help me?",
        "What's the weather like?"
    ]
    
    print("\n🤖 Chatbot Conversation:")
    print("-" * 30)
    
    for message in test_messages:
        print(f"\n👤 You: {message}")
        response = chatbot.chat(message)
        print(f"🤖 AI: {response}")
    
    print(f"\n📊 {chatbot.get_conversation_summary()}")
    
    # Display conversation history
    chatbot.display_conversation_history()
    
    return chatbot

# =============================================================================
# SECTION 7: INTERACTIVE CHAT INTERFACE
# =============================================================================

def interactive_chat():
    """Run an interactive chat session"""
    print("\n🎯 Interactive Chat Session")
    print("Type 'quit' to exit")
    print("-" * 30)
    
    chatbot = SimpleAIChatbot()
    
    while True:
        try:
            user_input = input("\n👤 You: ")
            
            if user_input.lower() in ['quit', 'exit', 'bye']:
                print("🤖 AI: Goodbye! Thanks for chatting with me!")
                break
            
            response = chatbot.chat(user_input)
            print(f"🤖 AI: {response}")
            
        except KeyboardInterrupt:
            print("\n\n🤖 AI: Goodbye! Thanks for chatting with me!")
            break
        except EOFError:
            print("\n\n🤖 AI: Goodbye! Thanks for chatting with me!")
            break

# =============================================================================
# SECTION 8: LEARNING PROGRESS TRACKER
# =============================================================================

@dataclass
class LearningTopic:
    """Represents a learning topic"""
    name: str
    completed: bool
    progress: int
    notes: List[str]

@dataclass
class Project:
    """Represents a learning project"""
    name: str
    description: str
    status: str  # 'planned', 'in_progress', 'completed'
    date_added: str

class AILearningTracker:
    """Track your AI learning progress"""
    
    def __init__(self):
        self.topics = {
            "python_basics": LearningTopic("Python Basics", False, 0, []),
            "prompt_engineering": LearningTopic("Prompt Engineering", False, 0, []),
            "rag_systems": LearningTopic("RAG Systems", False, 0, []),
            "ai_agents": LearningTopic("AI Agents", False, 0, []),
            "fine_tuning": LearningTopic("Fine-tuning", False, 0, []),
            "deployment": LearningTopic("Production Deployment", False, 0, [])
        }
        
        self.projects: List[Project] = []
        self.notes: List[Dict] = []
    
    def update_progress(self, topic: str, progress_percentage: int):
        """Update progress for a specific topic"""
        if topic in self.topics:
            self.topics[topic].progress = min(100, max(0, progress_percentage))
            if self.topics[topic].progress >= 100:
                self.topics[topic].completed = True
            print(f"✅ Updated {self.topics[topic].name} progress to {self.topics[topic].progress}%")
        else:
            print(f"❌ Topic '{topic}' not found")
    
    def add_project(self, name: str, description: str, status: str = "planned"):
        """Add a new project"""
        project = Project(name, description, status, time.strftime("%Y-%m-%d"))
        self.projects.append(project)
        print(f"📁 Added project: {name}")
    
    def add_note(self, topic: str, note: str):
        """Add a learning note"""
        self.notes.append({"topic": topic, "note": note, "date": time.strftime("%Y-%m-%d")})
        print(f"📝 Added note for {topic}")
    
    def get_overall_progress(self) -> float:
        """Calculate overall learning progress"""
        total_progress = sum(topic.progress for topic in self.topics.values())
        return total_progress / len(self.topics)
    
    def display_progress(self):
        """Display current learning progress"""
        print("\n📊 Your AI Learning Progress")
        print("=" * 40)
        
        for topic_id, topic in self.topics.items():
            status = "✅" if topic.completed else "🔄"
            progress_bar = "█" * (topic.progress // 10) + "░" * (10 - topic.progress // 10)
            print(f"{status} {topic.name}: {progress_bar} {topic.progress}%")
        
        overall = self.get_overall_progress()
        print(f"\n🎯 Overall Progress: {overall:.1f}%")
        
        if self.projects:
            print(f"\n📁 Projects ({len(self.projects)}):")
            for project in self.projects:
                status_emoji = {"planned": "📋", "in_progress": "🔄", "completed": "✅"}
                print(f"  {status_emoji.get(project.status, '📋')} {project.name} ({project.status})")

def demonstrate_learning_tracker():
    """Demonstrate the learning tracker"""
    print("\n📈 Learning Progress Tracker")
    print("=" * 35)
    
    # Create and test the tracker
    tracker = AILearningTracker()
    
    # Update some progress
    tracker.update_progress("python_basics", 80)
    tracker.update_progress("prompt_engineering", 60)
    tracker.update_progress("rag_systems", 20)
    
    # Add some projects
    tracker.add_project("AI Chatbot", "Build a simple chatbot using Python", "completed")
    tracker.add_project("Document Q&A System", "Create a RAG system for document search", "in_progress")
    tracker.add_project("AI Agent", "Build an autonomous AI agent", "planned")
    
    # Add some notes
    tracker.add_note("prompt_engineering", "Being specific and clear is key to good prompts")
    tracker.add_note("rag_systems", "Embeddings help find similar documents")
    
    # Display progress
    tracker.display_progress()
    
    return tracker

# =============================================================================
# MAIN EXECUTION
# =============================================================================

def main():
    """Main function to run all demonstrations"""
    print("🚀 AI Learning Path - Complete Guide")
    print("=" * 50)
    print("This file contains comprehensive examples and explanations for AI Engineering.")
    print("Run individual functions to explore different concepts.\n")
    
    # Run all demonstrations
    print_ai_engineering_overview()
    check_environment()
    demonstrate_python_basics()
    demonstrate_api_usage()
    demonstrate_ai_concepts()
    demonstrate_chatbot()
    demonstrate_learning_tracker()
    
    print("\n🎉 Congratulations! You've completed the AI Basics section!")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Practice the code examples above")
    print("2. Try the interactive chat (uncomment interactive_chat() below)")
    print("3. Explore the other Python files in this folder")
    print("4. Build your own AI projects!")
    
    print("\n💡 To start an interactive chat session, uncomment the line below:")
    print("# interactive_chat()")

if __name__ == "__main__":
    main()
    
    # Uncomment the line below to start interactive chat
    # interactive_chat() 