"""
Student Loan Assistant - Web UI
Streamlit application for interacting with the AI-powered student loan assistant.
"""

import streamlit as st
import sys
import os
import time
import json
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# Add the src directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.main import StudentLoanAssistant


def initialize_session_state():
    """Initialize session state variables."""
    if 'assistant' not in st.session_state:
        st.session_state.assistant = None
    if 'initialized' not in st.session_state:
        st.session_state.initialized = False
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'evaluation_results' not in st.session_state:
        st.session_state.evaluation_results = None


def setup_page():
    """Configure the Streamlit page."""
    st.set_page_config(
        page_title="Student Loan Assistant",
        page_icon="🎓",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Custom CSS for better styling
    st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #2c3e50;
        margin-bottom: 1rem;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .user-message {
        background-color: #e3f2fd;
        border-left: 4px solid #2196f3;
    }
    .assistant-message {
        background-color: #f3e5f5;
        border-left: 4px solid #9c27b0;
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #dee2e6;
    }
    </style>
    """, unsafe_allow_html=True)


def initialize_system():
    """Initialize the Student Loan Assistant system."""
    if not st.session_state.initialized:
        with st.spinner("🚀 Initializing Student Loan Assistant..."):
            try:
                assistant = StudentLoanAssistant()
                init_result = assistant.initialize_system()
                
                if init_result["status"] == "success":
                    st.session_state.assistant = assistant
                    st.session_state.initialized = True
                    st.success("✅ System initialized successfully!")
                    return True
                else:
                    st.error(f"❌ Initialization failed: {init_result.get('error', 'Unknown error')}")
                    return False
            except Exception as e:
                st.error(f"❌ Error during initialization: {str(e)}")
                return False
    return True


def display_header():
    """Display the main header."""
    st.markdown('<h1 class="main-header">🎓 Student Loan Assistant</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; font-size: 1.2rem; color: #666;">AI-Powered Guidance for Federal Student Loans</p>', unsafe_allow_html=True)


def display_sidebar():
    """Display the sidebar with system information and controls."""
    with st.sidebar:
        st.markdown("## 🔧 System Controls")
        
        # System Status
        if st.session_state.initialized:
            st.success("✅ System Ready")
            
            # System Info
            status = st.session_state.assistant.get_system_status()
            st.markdown("### 📊 System Status")
            
            for component, ready in status["components"].items():
                icon = "✅" if ready else "❌"
                st.write(f"{icon} {component.replace('_', ' ').title()}")
            
            if "data_summary" in status:
                st.markdown("### 📚 Data Summary")
                summary = status["data_summary"]
                st.write(f"📄 Documents: {summary.get('total_documents', 0)}")
                st.write(f"📝 Complaints: {summary.get('total_complaints', 0)}")
                st.write(f"❓ Test Questions: {summary.get('total_test_questions', 0)}")
        else:
            st.warning("⚠️ System Not Initialized")
        
        st.markdown("---")
        
        # Quick Actions
        st.markdown("### ⚡ Quick Actions")
        
        if st.button("🔄 Reinitialize System"):
            st.session_state.initialized = False
            st.session_state.assistant = None
            st.rerun()
        
        if st.button("📊 Run Evaluation"):
            if st.session_state.initialized:
                run_evaluation()
        
        if st.button("🗑️ Clear Chat History"):
            st.session_state.chat_history = []
            st.rerun()
        
        st.markdown("---")
        
        # Example Queries
        st.markdown("### 💡 Example Queries")
        example_queries = [
            "What are the eligibility requirements for federal student loans?",
            "How do I apply for a Direct Loan?",
            "What are the current interest rates for student loans?",
            "How do I repay my student loans?",
            "What happens if I can't make my loan payments?",
            "What is the difference between subsidized and unsubsidized loans?",
            "How do I consolidate my student loans?",
            "What are the loan forgiveness options?"
        ]
        
        for query in example_queries:
            if st.button(query, key=f"example_{hash(query)}"):
                st.session_state.example_query = query
                st.rerun()


def display_chat_interface():
    """Display the main chat interface."""
    st.markdown('<h2 class="sub-header">💬 Ask Your Student Loan Questions</h2>', unsafe_allow_html=True)
    
    # Chat input
    col1, col2 = st.columns([4, 1])
    
    with col1:
        user_query = st.text_area(
            "Enter your question:",
            placeholder="e.g., What are the eligibility requirements for federal student loans?",
            height=100,
            key="user_input"
        )
    
    with col2:
        st.write("")  # Spacing
        st.write("")  # Spacing
        submit_button = st.button("🚀 Ask Assistant", type="primary")
    
    # Handle example query
    if hasattr(st.session_state, 'example_query'):
        user_query = st.session_state.example_query
        del st.session_state.example_query
        submit_button = True
    
    # Process query
    if submit_button and user_query.strip():
        process_user_query(user_query.strip())


def process_user_query(query: str):
    """Process a user query and display the response."""
    if not st.session_state.initialized:
        st.error("❌ System not initialized. Please wait for initialization to complete.")
        return
    
    # Add user message to chat history
    st.session_state.chat_history.append({
        "role": "user",
        "content": query,
        "timestamp": datetime.now()
    })
    
    # Process with assistant
    with st.spinner("🤖 Processing your question..."):
        try:
            result = st.session_state.assistant.process_student_query(query)
            
            if "error" in result:
                response_text = f"I apologize, but I encountered an error: {result['error']}"
                metadata = {}
            else:
                response_text = result.get("final_response", "No response generated.")
                metadata = result.get("metadata", {})
            
            # Add assistant response to chat history
            st.session_state.chat_history.append({
                "role": "assistant",
                "content": response_text,
                "metadata": metadata,
                "timestamp": datetime.now()
            })
            
        except Exception as e:
            error_response = f"I apologize, but I encountered an error processing your query: {str(e)}"
            st.session_state.chat_history.append({
                "role": "assistant",
                "content": error_response,
                "timestamp": datetime.now()
            })
    
    # Rerun to display updated chat
    st.rerun()


def display_chat_history():
    """Display the chat history."""
    if not st.session_state.chat_history:
        return
    
    st.markdown('<h3 class="sub-header">💭 Conversation History</h3>', unsafe_allow_html=True)
    
    for i, message in enumerate(st.session_state.chat_history):
        if message["role"] == "user":
            st.markdown(f"""
            <div class="chat-message user-message">
                <strong>👤 You:</strong><br>
                {message["content"]}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="chat-message assistant-message">
                <strong>🤖 Assistant:</strong><br>
                {message["content"]}
            </div>
            """, unsafe_allow_html=True)
            
            # Display metadata if available
            if "metadata" in message and message["metadata"]:
                with st.expander("📊 Response Details"):
                    metadata = message["metadata"]
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Query Type", metadata.get("query_type", "Unknown"))
                    with col2:
                        st.metric("Complexity", metadata.get("complexity_level", "Unknown"))
                    with col3:
                        st.metric("Sources", len(metadata.get("research_sources", [])))
                    
                    # Display quality metrics if available
                    if "response_quality" in metadata:
                        st.markdown("#### Quality Metrics")
                        quality = metadata["response_quality"]
                        if isinstance(quality, dict):
                            for metric, score in quality.items():
                                st.progress(score / 10 if score <= 10 else score / 100)
                                st.write(f"{metric.title()}: {score:.1f}")


def run_evaluation():
    """Run system evaluation and display results."""
    if not st.session_state.initialized:
        st.error("❌ System not initialized")
        return
    
    with st.spinner("📊 Running system evaluation..."):
        try:
            evaluation_results = st.session_state.assistant.evaluate_system()
            st.session_state.evaluation_results = evaluation_results
            st.success("✅ Evaluation completed!")
        except Exception as e:
            st.error(f"❌ Evaluation failed: {str(e)}")


def display_evaluation_results():
    """Display evaluation results."""
    if not st.session_state.evaluation_results:
        return
    
    st.markdown('<h2 class="sub-header">📊 System Evaluation Results</h2>', unsafe_allow_html=True)
    
    results = st.session_state.evaluation_results
    
    if "error" in results:
        st.error(f"❌ Evaluation Error: {results['error']}")
        return
    
    # Summary metrics
    summary = results.get("evaluation_summary", {})
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Metrics", summary.get("total_metrics", 0))
    
    with col2:
        avg_score = summary.get("average_score", 0)
        st.metric("Average Score", f"{avg_score:.2f}")
    
    with col3:
        passing_rate = summary.get("passing_score", 0)
        st.metric("Passing Rate", f"{passing_rate:.1%}")
    
    with col4:
        status = "✅ Excellent" if avg_score >= 0.85 else "⚠️ Good" if avg_score >= 0.7 else "❌ Needs Improvement"
        st.metric("Overall Status", status)
    
    # Detailed results
    with st.expander("📈 Detailed Evaluation Results"):
        if "custom_metrics" in results:
            custom_metrics = results["custom_metrics"]
            
            # Create metrics visualization
            metrics_data = []
            for metric, score in custom_metrics.items():
                metrics_data.append({"Metric": metric.title(), "Score": score})
            
            if metrics_data:
                df = pd.DataFrame(metrics_data)
                fig = px.bar(df, x="Metric", y="Score", 
                           title="Custom Metrics Performance",
                           color="Score",
                           color_continuous_scale="RdYlGn")
                st.plotly_chart(fig, use_container_width=True)
        
        # Workflow report
        if "workflow_report" in results:
            workflow = results["workflow_report"]
            
            st.markdown("#### Workflow Analysis")
            
            col1, col2 = st.columns(2)
            with col1:
                st.write("**Query Analysis:**")
                if "query_analysis" in workflow:
                    query_types = workflow["query_analysis"].get("query_types", {})
                    for query_type, count in query_types.items():
                        st.write(f"- {query_type}: {count}")
            
            with col2:
                st.write("**Quality Distribution:**")
                if "quality_analysis" in workflow:
                    quality_dist = workflow["quality_analysis"].get("quality_distribution", {})
                    for level, count in quality_dist.items():
                        st.write(f"- {level.title()}: {count}")
        
        # Recommendations
        if "recommendations" in results:
            st.markdown("#### Recommendations")
            for rec in results["recommendations"]:
                st.write(f"• {rec}")


def display_retrieval_comparison():
    """Display retrieval method comparison."""
    if not st.session_state.initialized:
        return
    
    st.markdown('<h2 class="sub-header">🔍 Retrieval Method Comparison</h2>', unsafe_allow_html=True)
    
    comparison_query = st.text_input(
        "Enter a query to compare retrieval methods:",
        placeholder="e.g., student loan eligibility requirements"
    )
    
    if st.button("🔍 Compare Methods") and comparison_query:
        with st.spinner("Comparing retrieval methods..."):
            try:
                comparison_results = st.session_state.assistant.compare_retrieval_methods(comparison_query)
                
                if "error" not in comparison_results:
                    analysis = comparison_results.get("analysis", {})
                    
                    # Display comparison
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown("#### Document Counts")
                        doc_counts = analysis.get("document_counts", {})
                        for method, count in doc_counts.items():
                            st.write(f"- {method.title()}: {count} documents")
                    
                    with col2:
                        st.markdown("#### Recommendation")
                        st.info(analysis.get("recommendation", "No recommendation available"))
                    
                    # Display detailed results
                    with st.expander("📄 Detailed Retrieval Results"):
                        results = comparison_results.get("comparison_results", {})
                        for method, docs in results.items():
                            if isinstance(docs, list):
                                st.markdown(f"**{method.title()} Results:**")
                                for i, doc in enumerate(docs[:3]):  # Show first 3 docs
                                    st.write(f"{i+1}. {doc.page_content[:200]}...")
                                st.write("---")
                
            except Exception as e:
                st.error(f"❌ Comparison failed: {str(e)}")


def main():
    """Main application function."""
    setup_page()
    initialize_session_state()
    
    # Initialize system
    if not st.session_state.initialized:
        if initialize_system():
            st.rerun()
        else:
            st.stop()
    
    # Display header
    display_header()
    
    # Display sidebar
    display_sidebar()
    
    # Main content area
    tab1, tab2, tab3 = st.tabs(["💬 Chat", "📊 Evaluation", "🔍 Retrieval Comparison"])
    
    with tab1:
        display_chat_interface()
        display_chat_history()
    
    with tab2:
        display_evaluation_results()
    
    with tab3:
        display_retrieval_comparison()


if __name__ == "__main__":
    main() 