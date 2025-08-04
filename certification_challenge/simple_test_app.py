"""
Simple test app to debug initialization issues.
"""

import streamlit as st
import os
import sys

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
        submit_button = st.form_submit_button("🚀 Configure and Initialize System", type="primary")
        
        if submit_button:
            if not openai_key.strip():
                st.error("❌ OpenAI API Key is required!")
                return False
            
            # Store API keys in session state
            st.session_state.openai_api_key = openai_key.strip()
            st.session_state.cohere_api_key = cohere_key.strip()
            st.session_state.tavily_api_key = tavily_key.strip()
            st.session_state.api_keys_configured = True
            
            st.success("✅ API keys configured successfully!")
            st.info("🔄 Initializing system with your API keys...")
            return True
    
    return False

def simple_initialize_system():
    """Simple system initialization that skips complex data loading."""
    try:
        st.write("🔍 Step 1: Setting up environment variables...")
        if st.session_state.openai_api_key:
            os.environ["OPENAI_API_KEY"] = st.session_state.openai_api_key
        if st.session_state.cohere_api_key:
            os.environ["COHERE_API_KEY"] = st.session_state.cohere_api_key
        if st.session_state.tavily_api_key:
            os.environ["TAVILY_API_KEY"] = st.session_state.tavily_api_key
        
        st.write("✅ Environment variables set successfully!")
        
        st.write("🔍 Step 2: Testing OpenAI connection...")
        try:
            from openai import OpenAI
            client = OpenAI(api_key=st.session_state.openai_api_key)
            # Simple test call
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": "Hello"}],
                max_tokens=5
            )
            st.write("✅ OpenAI connection successful!")
        except Exception as e:
            st.error(f"❌ OpenAI connection failed: {str(e)}")
            return False
        
        st.write("🔍 Step 3: Testing data path...")
        data_path = "../04_Production_RAG/data"
        if os.path.exists(data_path):
            st.write(f"✅ Data path exists: {data_path}")
            files = os.listdir(data_path)
            st.write(f"📁 Found {len(files)} files: {files}")
        else:
            st.error(f"❌ Data path not found: {data_path}")
            return False
        
        st.write("🔍 Step 4: Testing basic imports...")
        try:
            import pandas as pd
            import numpy as np
            st.write("✅ Basic imports successful!")
        except Exception as e:
            st.error(f"❌ Basic imports failed: {str(e)}")
            return False
        
        st.write("🔍 Step 5: Testing LangChain imports...")
        try:
            from langchain_openai import ChatOpenAI
            from langchain_core.messages import HumanMessage
            st.write("✅ LangChain imports successful!")
        except Exception as e:
            st.error(f"❌ LangChain imports failed: {str(e)}")
            return False
        
        st.success("🎉 System initialization completed successfully!")
        st.session_state.initialized = True
        return True
        
    except Exception as e:
        st.error(f"❌ Initialization failed: {str(e)}")
        import traceback
        st.code(traceback.format_exc())
        return False

def main():
    """Main application function."""
    st.set_page_config(
        page_title="Student Loan Assistant - Debug",
        page_icon="🎓",
        layout="wide"
    )
    
    st.markdown('<h1>🎓 Student Loan Assistant - Debug Mode</h1>', unsafe_allow_html=True)
    
    initialize_session_state()
    
    # Check if API keys are configured
    if not st.session_state.api_keys_configured:
        display_api_key_configuration()
        return
    
    # Initialize system if not already done
    if not st.session_state.initialized:
        if simple_initialize_system():
            st.rerun()
        else:
            st.stop()
    
    # Main interface
    st.success("✅ System is ready!")
    st.markdown("### 💬 Chat Interface")
    
    user_query = st.text_area(
        "Enter your question:",
        placeholder="e.g., What are the eligibility requirements for federal student loans?",
        height=100
    )
    
    if st.button("🚀 Ask Question"):
        if user_query.strip():
            st.info("This is a debug version. The full system would process your query here.")
            st.write(f"**Your question:** {user_query}")
            st.write("**Response:** This is a test response. The full system would provide a detailed answer based on the student loan documentation.")
        else:
            st.warning("Please enter a question.")

if __name__ == "__main__":
    main() 