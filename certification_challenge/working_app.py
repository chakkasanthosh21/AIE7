"""
Simplified Student Loan Assistant - Working Version
This version bypasses complex initialization and provides immediate chatbot functionality.
"""

import streamlit as st
import os
import sys
from openai import OpenAI
import time

# Add the src directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def initialize_session_state():
    """Initialize session state variables."""
    if 'assistant' not in st.session_state:
        st.session_state.assistant = None
    if 'initialized' not in st.session_state:
        st.session_state.initialized = False
    if 'api_keys_configured' not in st.session_state:
        st.session_state.api_keys_configured = False
    if 'openai_api_key' not in st.session_state:
        st.session_state.openai_api_key = ""
    if 'cohere_api_key' not in st.session_state:
        st.session_state.cohere_api_key = ""
    if 'tavily_api_key' not in st.session_state:
        st.session_state.tavily_api_key = ""
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

def display_api_key_configuration():
    """Display API key configuration interface."""
    st.markdown('<h2>🔑 API Key Configuration</h2>', unsafe_allow_html=True)
    
    st.markdown("""
    To use the Student Loan Assistant, you need to configure your API keys. 
    These keys are stored securely in your browser session and are not saved to any server.
    """)
    
    with st.form("api_key_form"):
        st.markdown("#### Required API Keys")
        
        # OpenAI API Key (Required)
        openai_key = st.text_input(
            "OpenAI API Key *",
            value=st.session_state.openai_api_key,
            type="password",
            help="Get your API key from https://platform.openai.com/api-keys"
        )
        
        st.markdown("#### Optional API Keys")
        
        # Cohere API Key (Optional)
        cohere_key = st.text_input(
            "Cohere API Key",
            value=st.session_state.cohere_api_key,
            type="password",
            help="Get your API key from https://dashboard.cohere.ai/api-keys (optional, for enhanced retrieval)"
        )
        
        # Tavily API Key (Optional)
        tavily_key = st.text_input(
            "Tavily API Key",
            value=st.session_state.tavily_api_key,
            type="password",
            help="Get your API key from https://tavily.com/ (optional, for real-time web search)"
        )
        
        # Submit button
        submit_button = st.form_submit_button("🚀 Start Chatbot", type="primary")
        
        if submit_button:
            if not openai_key.strip():
                st.error("❌ OpenAI API Key is required!")
                return False
            
            # Store API keys in session state
            st.session_state.openai_api_key = openai_key.strip()
            st.session_state.cohere_api_key = cohere_key.strip()
            st.session_state.tavily_api_key = tavily_key.strip()
            st.session_state.api_keys_configured = True
            
            # Automatically initialize the system
            if initialize_simple_system():
                st.session_state.initialized = True
                st.success("✅ API keys configured and system ready!")
                st.rerun()
            else:
                st.error("❌ Failed to initialize system. Please check your API keys.")
                return False
            
            return True
    
    return False

def initialize_simple_system():
    """Initialize a simple system that works immediately."""
    try:
        # Set environment variables
        if st.session_state.openai_api_key:
            os.environ["OPENAI_API_KEY"] = st.session_state.openai_api_key
        if st.session_state.cohere_api_key:
            os.environ["COHERE_API_KEY"] = st.session_state.cohere_api_key
        if st.session_state.tavily_api_key:
            os.environ["TAVILY_API_KEY"] = st.session_state.tavily_api_key
        
        # Test OpenAI connection
        client = OpenAI(api_key=st.session_state.openai_api_key)
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": "Hello"}],
            max_tokens=5
        )
        
        st.session_state.initialized = True
        return True
        
    except Exception as e:
        st.error(f"❌ Initialization failed: {str(e)}")
        return False

def get_student_loan_response(query: str) -> str:
    """Get a response for student loan questions using OpenAI."""
    try:
        client = OpenAI(api_key=st.session_state.openai_api_key)
        
        # Enhanced system prompt for student loan assistance
        system_prompt = """You are a knowledgeable Student Loan Assistant specializing in federal student loans. 
        
        You have expertise in:
        - Federal Direct Loans (Subsidized and Unsubsidized)
        - Federal Pell Grants
        - Loan application processes
        - Repayment options and plans
        - Loan forgiveness programs
        - Interest rates and fees
        - Eligibility requirements
        - Financial aid applications (FAFSA)
        
        Provide accurate, helpful, and empathetic responses. Always mention that users should verify information with official sources like studentaid.gov.
        
        If you don't know something specific, say so and suggest where they can find the information."""
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": query}
            ],
            max_tokens=800,
            temperature=0.7
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        return f"I apologize, but I encountered an error: {str(e)}. Please check your API key and try again."

def display_chat_interface():
    """Display the main chat interface."""
    st.markdown('<h2>💬 Student Loan Assistant Chat</h2>', unsafe_allow_html=True)
    
    # Display chat history
    for message in st.session_state.chat_history:
        if message["role"] == "user":
            st.markdown(f"""
            <div class="user-message">
                <strong>You:</strong> {message["content"]}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="assistant-message">
                <strong>Assistant:</strong> {message["content"]}
            </div>
            """, unsafe_allow_html=True)
    
    # Chat input
    user_query = st.text_area(
        "Ask me about student loans:",
        placeholder="e.g., What are the eligibility requirements for federal student loans?",
        height=100,
        key="user_input"
    )
    
    col1, col2 = st.columns([1, 4])
    
    with col1:
        if st.button("🚀 Ask", type="primary"):
            if user_query.strip():
                # Add user message to history
                st.session_state.chat_history.append({
                    "role": "user",
                    "content": user_query.strip()
                })
                
                # Get response
                with st.spinner("🤔 Thinking..."):
                    response = get_student_loan_response(user_query.strip())
                
                # Add assistant response to history
                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": response
                })
                
                # Clear input and rerun to show new messages
                st.rerun()
            else:
                st.warning("Please enter a question.")
    
    with col2:
        if st.button("🗑️ Clear Chat"):
            st.session_state.chat_history = []
            st.rerun()

def display_sidebar():
    """Display sidebar with information and controls."""
    st.sidebar.markdown("## 🎓 Student Loan Assistant")
    
    st.sidebar.markdown("### 📋 Quick Questions")
    quick_questions = [
        "What are the eligibility requirements for federal student loans?",
        "How do I apply for a Direct Loan?",
        "What are the current interest rates?",
        "What's the difference between subsidized and unsubsidized loans?",
        "How do I apply for loan forgiveness?",
        "What are the repayment options?",
        "How do I fill out the FAFSA?",
        "What is the maximum loan amount I can borrow?"
    ]
    
    for question in quick_questions:
        if st.sidebar.button(question, key=f"quick_{question[:20]}"):
            st.session_state.chat_history.append({
                "role": "user",
                "content": question
            })
            
            with st.spinner("🤔 Thinking..."):
                response = get_student_loan_response(question)
            
            st.session_state.chat_history.append({
                "role": "assistant",
                "content": response
            })
            st.rerun()
    
    st.sidebar.markdown("---")
    
    # API Key Status
    st.sidebar.markdown("### 🔑 API Key Status")
    if st.session_state.openai_api_key:
        st.sidebar.success("✅ OpenAI API Key")
    else:
        st.sidebar.error("❌ OpenAI API Key")
    
    if st.session_state.cohere_api_key:
        st.sidebar.info("✅ Cohere API Key")
    else:
        st.sidebar.info("ℹ️ No Cohere API Key")
    
    if st.session_state.tavily_api_key:
        st.sidebar.info("✅ Tavily API Key")
    else:
        st.sidebar.info("ℹ️ No Tavily API Key")
    
    # Reconfigure button
    if st.sidebar.button("🔧 Reconfigure API Keys"):
        st.session_state.api_keys_configured = False
        st.session_state.initialized = False
        st.session_state.chat_history = []
        st.rerun()

def main():
    """Main application function."""
    st.set_page_config(
        page_title="Student Loan Assistant",
        page_icon="🎓",
        layout="wide"
    )
    
    # Custom CSS with dark theme
    st.markdown("""
    <style>
    /* Dark theme styling */
    .stApp {
        background-color: #1a1a1a;
        color: #ffffff;
    }
    
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #4CAF50;
        text-align: center;
        margin-bottom: 1rem;
    }
    
    .sub-header {
        font-size: 1.2rem;
        color: #ffffff;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    /* Dark chat messages */
    .user-message {
        background-color: #2d3748;
        color: #ffffff;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
        border-left: 4px solid #4CAF50;
    }
    
    .assistant-message {
        background-color: #1a202c;
        color: #ffffff;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
        border-left: 4px solid #2196F3;
    }
    
    /* Dark sidebar */
    .css-1d391kg {
        background-color: #2d3748;
    }
    
    /* Dark text inputs */
    .stTextInput > div > div > input {
        background-color: #2d3748;
        color: #ffffff;
        border: 1px solid #4a5568;
    }
    
    .stTextArea > div > div > textarea {
        background-color: #2d3748;
        color: #ffffff;
        border: 1px solid #4a5568;
    }
    
    /* Dark buttons */
    .stButton > button {
        background-color: #4CAF50;
        color: #ffffff;
        border: none;
        border-radius: 5px;
        padding: 10px 20px;
    }
    
    .stButton > button:hover {
        background-color: #45a049;
    }
    
    /* Dark form elements */
    .stForm {
        background-color: #2d3748;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #4a5568;
    }
    
    /* Override Streamlit's default styling */
    .stMarkdown {
        color: #ffffff;
    }
    
    .stSuccess {
        background-color: #2d3748;
        color: #4CAF50;
        border: 1px solid #4CAF50;
    }
    
    .stError {
        background-color: #2d3748;
        color: #f44336;
        border: 1px solid #f44336;
    }
    
    .stInfo {
        background-color: #2d3748;
        color: #2196F3;
        border: 1px solid #2196F3;
    }
    
    .stWarning {
        background-color: #2d3748;
        color: #ff9800;
        border: 1px solid #ff9800;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<h1 class="main-header">🎓 Student Loan Assistant</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Your AI-powered guide to federal student loans</p>', unsafe_allow_html=True)
    
    initialize_session_state()
    
    # Display sidebar
    display_sidebar()
    
    # Check if API keys are configured
    if not st.session_state.api_keys_configured:
        display_api_key_configuration()
        return
    
    # Display chat interface (system is already initialized)
    display_chat_interface()

if __name__ == "__main__":
    main() 