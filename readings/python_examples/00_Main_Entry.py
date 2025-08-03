#!/usr/bin/env python3
"""
🎓 AI Learning Path - Main Entry Point
======================================

Welcome to the comprehensive AI learning materials! This file serves as the main
entry point to explore all the AI concepts covered in this repository.

What you'll find:
1. AI Basics - Fundamental concepts and Python for AI
2. Prompt Engineering - Crafting effective AI prompts
3. RAG Systems - Retrieval Augmented Generation
4. AI Agents - Autonomous AI systems
5. Fine-tuning - Adapting pre-trained models
6. Production Deployment - Deploying AI applications

Author: AI Learning Guide
Date: 2024
"""

import sys
import os
from typing import Dict, List, Any

# =============================================================================
# LEARNING PATH OVERVIEW
# =============================================================================

LEARNING_MODULES = {
    "01_AI_Basics": {
        "title": "AI Basics",
        "description": "Fundamental concepts of AI Engineering with Python examples",
        "topics": [
            "What is AI Engineering?",
            "Basic Python for AI",
            "Your first AI application",
            "Core AI concepts",
            "Environment setup"
        ],
        "difficulty": "Beginner",
        "estimated_time": "2-3 hours"
    },
    "02_Prompt_Engineering": {
        "title": "Prompt Engineering",
        "description": "The art and science of crafting effective prompts for AI models",
        "topics": [
            "Basic prompt engineering techniques",
            "Advanced techniques (Chain of Thought, Few-Shot)",
            "Prompt templates and best practices",
            "Interactive prompt builder",
            "Prompt evaluation framework"
        ],
        "difficulty": "Beginner to Intermediate",
        "estimated_time": "3-4 hours"
    },
    "03_RAG_Systems": {
        "title": "RAG Systems",
        "description": "Retrieval Augmented Generation - making AI smarter with external knowledge",
        "topics": [
            "Core components of RAG",
            "Building simple RAG systems",
            "Advanced RAG techniques",
            "Real-world applications",
            "Evaluation and optimization"
        ],
        "difficulty": "Intermediate",
        "estimated_time": "4-5 hours"
    },
    "04_AI_Agents": {
        "title": "AI Agents",
        "description": "Autonomous AI systems that can perceive, think, and act",
        "topics": [
            "Types of AI agents",
            "Building simple agents",
            "Multi-agent systems",
            "Agent communication",
            "Real-world applications"
        ],
        "difficulty": "Intermediate",
        "estimated_time": "4-5 hours"
    },
    "05_Fine_Tuning": {
        "title": "Fine-tuning AI Models",
        "description": "Adapting pre-trained models to specific tasks and domains",
        "topics": [
            "Types of fine-tuning",
            "Data preparation",
            "Training strategies",
            "Evaluation and optimization",
            "Real-world applications"
        ],
        "difficulty": "Intermediate to Advanced",
        "estimated_time": "5-6 hours"
    },
    "06_Production_Deployment": {
        "title": "Production Deployment",
        "description": "Deploying AI applications to production environments",
        "topics": [
            "Deployment strategies",
            "Containerization with Docker",
            "Monitoring and scaling",
            "Best practices",
            "Production pipeline"
        ],
        "difficulty": "Intermediate to Advanced",
        "estimated_time": "4-5 hours"
    }
}

def print_welcome_message():
    """Print welcome message and overview"""
    print("🎓 Welcome to AI Learning Path!")
    print("=" * 50)
    print("This repository contains comprehensive learning materials for AI Engineering.")
    print("Each module includes detailed explanations, working code examples, and practical exercises.")
    print("\n💡 Start with AI Basics if you're new to AI, or jump to any topic that interests you!")

def print_learning_path():
    """Print the complete learning path"""
    print("\n📚 Complete Learning Path")
    print("=" * 30)
    
    for module_id, module_info in LEARNING_MODULES.items():
        print(f"\n{module_id}: {module_info['title']}")
        print(f"   Difficulty: {module_info['difficulty']}")
        print(f"   Time: {module_info['estimated_time']}")
        print(f"   Description: {module_info['description']}")
        print(f"   Topics: {', '.join(module_info['topics'][:3])}...")

def print_module_details(module_id: str):
    """Print detailed information about a specific module"""
    if module_id not in LEARNING_MODULES:
        print(f"❌ Module '{module_id}' not found!")
        return
    
    module = LEARNING_MODULES[module_id]
    print(f"\n📖 {module['title']} - Detailed Overview")
    print("=" * 50)
    print(f"Difficulty: {module['difficulty']}")
    print(f"Estimated Time: {module['estimated_time']}")
    print(f"Description: {module['description']}")
    
    print(f"\n🎯 Topics Covered:")
    for i, topic in enumerate(module['topics'], 1):
        print(f"   {i}. {topic}")
    
    print(f"\n💡 To explore this module, run: python {module_id}.py")

def print_learning_recommendations():
    """Print learning recommendations based on experience level"""
    print("\n🎯 Learning Recommendations")
    print("=" * 30)
    
    print("\n🚀 For Beginners:")
    print("   1. Start with '01_AI_Basics'")
    print("   2. Then try '02_Prompt_Engineering'")
    print("   3. Practice with simple projects")
    
    print("\n📈 For Intermediate Learners:")
    print("   1. Review '01_AI_Basics' quickly")
    print("   2. Focus on '03_RAG_Systems' and '04_AI_Agents'")
    print("   3. Experiment with '05_Fine_Tuning'")
    
    print("\n🏆 For Advanced Learners:")
    print("   1. Skip to '05_Fine_Tuning' and '06_Production_Deployment'")
    print("   2. Build complex multi-agent systems")
    print("   3. Deploy your own AI applications")

def print_practical_projects():
    """Print suggested practical projects"""
    print("\n🔨 Practical Projects to Build")
    print("=" * 30)
    
    projects = [
        {
            "name": "AI Chatbot",
            "description": "Build a chatbot using prompt engineering and RAG",
            "modules": ["01_AI_Basics", "02_Prompt_Engineering", "03_RAG_Systems"],
            "difficulty": "Beginner"
        },
        {
            "name": "Document Q&A System",
            "description": "Create a system that answers questions from documents",
            "modules": ["03_RAG_Systems", "04_AI_Agents"],
            "difficulty": "Intermediate"
        },
        {
            "name": "Multi-Agent Assistant",
            "description": "Build a system with multiple specialized agents",
            "modules": ["04_AI_Agents", "05_Fine_Tuning"],
            "difficulty": "Intermediate"
        },
        {
            "name": "Fine-tuned Domain Expert",
            "description": "Fine-tune a model for a specific domain",
            "modules": ["05_Fine_Tuning", "06_Production_Deployment"],
            "difficulty": "Advanced"
        },
        {
            "name": "Production AI API",
            "description": "Deploy an AI application to production",
            "modules": ["06_Production_Deployment"],
            "difficulty": "Advanced"
        }
    ]
    
    for i, project in enumerate(projects, 1):
        print(f"\n{i}. {project['name']} ({project['difficulty']})")
        print(f"   Description: {project['description']}")
        print(f"   Required Modules: {', '.join(project['modules'])}")

def print_resources():
    """Print additional learning resources"""
    print("\n📚 Additional Resources")
    print("=" * 25)
    
    resources = [
        {
            "type": "Books",
            "items": [
                "Hands-On Machine Learning by Aurélien Géron",
                "Deep Learning by Ian Goodfellow",
                "Natural Language Processing with Python by Steven Bird"
            ]
        },
        {
            "type": "Online Courses",
            "items": [
                "Coursera: Machine Learning by Andrew Ng",
                "edX: Introduction to Artificial Intelligence",
                "Fast.ai: Practical Deep Learning"
            ]
        },
        {
            "type": "Tools and Libraries",
            "items": [
                "OpenAI API and GPT models",
                "Hugging Face Transformers",
                "LangChain for building AI applications",
                "Streamlit for web applications"
            ]
        },
        {
            "type": "Communities",
            "items": [
                "AI/ML subreddits",
                "Stack Overflow",
                "GitHub AI repositories",
                "AI conferences and meetups"
            ]
        }
    ]
    
    for resource in resources:
        print(f"\n{resource['type']}:")
        for item in resource['items']:
            print(f"   • {item}")

def interactive_menu():
    """Provide an interactive menu for navigation"""
    print("\n🎮 Interactive Learning Menu")
    print("=" * 30)
    
    while True:
        print("\nOptions:")
        print("1. View learning path")
        print("2. Get module details")
        print("3. Learning recommendations")
        print("4. Practical projects")
        print("5. Additional resources")
        print("6. Exit")
        
        try:
            choice = input("\nEnter your choice (1-6): ").strip()
            
            if choice == "1":
                print_learning_path()
            elif choice == "2":
                print("\nAvailable modules:")
                for module_id in LEARNING_MODULES.keys():
                    print(f"   {module_id}")
                module_id = input("Enter module ID: ").strip()
                print_module_details(module_id)
            elif choice == "3":
                print_learning_recommendations()
            elif choice == "4":
                print_practical_projects()
            elif choice == "5":
                print_resources()
            elif choice == "6":
                print("\n🎉 Happy learning! Good luck with your AI journey!")
                break
            else:
                print("❌ Invalid choice. Please enter a number between 1-6.")
                
        except KeyboardInterrupt:
            print("\n\n🎉 Happy learning! Good luck with your AI journey!")
            break
        except EOFError:
            print("\n\n🎉 Happy learning! Good luck with your AI journey!")
            break

def main():
    """Main function"""
    print_welcome_message()
    print_learning_path()
    print_learning_recommendations()
    print_practical_projects()
    print_resources()
    
    print("\n" + "="*60)
    print("🎯 Ready to start your AI learning journey?")
    print("="*60)
    
    # Check if user wants interactive menu
    try:
        response = input("\nWould you like to use the interactive menu? (y/n): ").strip().lower()
        if response in ['y', 'yes']:
            interactive_menu()
        else:
            print("\n💡 To explore specific modules, run:")
            for module_id in LEARNING_MODULES.keys():
                print(f"   python {module_id}.py")
            print("\n🎉 Happy learning! Good luck with your AI journey!")
    except (KeyboardInterrupt, EOFError):
        print("\n\n🎉 Happy learning! Good luck with your AI journey!")

if __name__ == "__main__":
    main() 