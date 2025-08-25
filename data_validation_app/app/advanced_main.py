#!/usr/bin/env python3
"""Advanced Data Validation App with AIE7 Enhancements."""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import asyncio
import nest_asyncio
from typing import Dict, List, Any
import json
import io
import sys
import os

# Add the app directory to the path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import our enhanced components
from advanced_semantic_validator import AdvancedSemanticValidator
from advanced_ml_validator import AdvancedMLValidator
from intelligent_validation_agent import IntelligentValidationAgent

# Enable nested asyncio
nest_asyncio.apply()

# Page configuration
st.set_page_config(
    page_title="Advanced Data Validation App",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #667eea;
        margin: 0.5rem 0;
    }
    .enhancement-badge {
        background: linear-gradient(45deg, #ff6b6b, #4ecdc4);
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

def safe_json_serialize(obj):
    """Safely serialize objects to JSON, handling numpy types and other non-serializable objects."""
    import numpy as np
    import pandas as pd
    
    if isinstance(obj, np.integer):
        return int(obj)
    elif isinstance(obj, np.floating):
        return float(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, pd.Series):
        return obj.tolist()
    elif isinstance(obj, pd.DataFrame):
        return obj.to_dict('records')
    elif isinstance(obj, dict):
        return {str(k): safe_json_serialize(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [safe_json_serialize(item) for item in obj]
    elif hasattr(obj, 'dtype'):  # Handle other numpy-like objects
        return str(obj)
    else:
        return str(obj)

def main():
    # Header with AIE7 enhancements
    st.markdown("""
    <div class="main-header">
        <h1>🚀 Advanced Data Validation App</h1>
        <p>Powered by AIE7 Concepts: RAG + Vector DBs • ML + Statistics • Intelligent Agents</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar configuration
    st.sidebar.header("⚙️ Configuration")
    
    # API Key input
    openai_api_key = st.sidebar.text_input(
        "OpenAI API Key",
        type="password",
        help="Enter your OpenAI API key for AI-powered analysis"
    )
    
    guardrails_api_key = st.sidebar.text_input(
        "Guardrails API Key (Optional)",
        type="password",
        help="Enter your Guardrails API key for additional validation"
    )
    
    # Main content
    st.header("�� Upload Datasets")
    st.write("Select 2 datasets for comparison and validation:")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Dataset 1")
        dataset1_name = st.text_input("Dataset Name", "dataset_1", key="name1")
        dataset1_file = st.file_uploader(
            "Upload File",
            type=['csv', 'json', 'xlsx', 'parquet'],
            key="file1"
        )
    
    with col2:
        st.subheader("Dataset 2")
        dataset2_name = st.text_input("Dataset Name", "dataset_2", key="name2")
        dataset2_file = st.file_uploader(
            "Upload File",
            type=['csv', 'json', 'xlsx', 'parquet'],
            key="file2"
        )
    
    # Load datasets
    data_sources = {}
    if dataset1_file:
        try:
            if dataset1_file.name.endswith('.csv'):
                data_sources[dataset1_name] = pd.read_csv(dataset1_file)
            elif dataset1_file.name.endswith('.json'):
                data_sources[dataset1_name] = pd.read_json(dataset1_file)
            elif dataset1_file.name.endswith('.xlsx'):
                data_sources[dataset1_name] = pd.read_excel(dataset1_file)
            elif dataset1_file.name.endswith('.parquet'):
                data_sources[dataset1_name] = pd.read_parquet(dataset1_file)
            st.success(f"✅ Loaded {dataset1_name}: {data_sources[dataset1_name].shape}")
        except Exception as e:
            st.error(f"❌ Error loading {dataset1_name}: {str(e)}")
    
    if dataset2_file:
        try:
            if dataset2_file.name.endswith('.csv'):
                data_sources[dataset2_name] = pd.read_csv(dataset2_file)
            elif dataset2_file.name.endswith('.json'):
                data_sources[dataset2_name] = pd.read_json(dataset2_file)
            elif dataset2_file.name.endswith('.xlsx'):
                data_sources[dataset2_name] = pd.read_excel(dataset2_file)
            elif dataset2_file.name.endswith('.parquet'):
                data_sources[dataset2_name] = pd.read_parquet(dataset2_file)
            st.success(f"✅ Loaded {dataset2_name}: {data_sources[dataset2_name].shape}")
        except Exception as e:
            st.error(f"❌ Error loading {dataset2_name}: {str(e)}")
    
    # Validation configuration
    if data_sources:
        st.header("🔍 Validation Configuration")
        
        # Set enhancement flags to always enabled (removed toggles)
        enable_semantic = True
        enable_ml = True
        enable_agents = True
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            validation_type = st.selectbox(
                "Validation Type",
                ["Comprehensive", "Schema Only", "Quality Only", "Semantic Only", "ML Only"]
            )
        
        with col2:
            confidence_threshold = st.slider(
                "Confidence Threshold",
                min_value=0.5,
                max_value=0.99,
                value=0.8,
                step=0.01
            )
        
        with col3:
            business_context = st.text_area(
                "Business Context (Optional)",
                placeholder="Describe the business purpose and data requirements...",
                height=100
            )
        
        # Run validation workflow
        if st.button("🚀 Run Enhanced Validation", type="primary"):
            with st.spinner("Running advanced validation..."):
                try:
                    # Initialize validators
                    semantic_validator = None
                    ml_validator = None
                    intelligent_agent = None
                    
                    if enable_semantic:
                        semantic_validator = AdvancedSemanticValidator()
                    
                    if enable_ml:
                        ml_validator = AdvancedMLValidator()
                    
                    if enable_agents:
                        intelligent_agent = IntelligentValidationAgent(openai_api_key)
                    
                    results = {}
                    
                    # Basic validation
                    if enable_semantic and semantic_validator:
                        st.info("🔍 Running Advanced Semantic Analysis...")
                        semantic_results = semantic_validator.analyze_cross_dataset_semantics(data_sources)
                        results['semantic_analysis'] = semantic_results
                        
                        # Also run individual dataset semantic analysis
                        for name, dataset_df in data_sources.items():
                            individual_semantic = semantic_validator.analyze_column_semantics_advanced({name: dataset_df})
                            if 'semantic_analysis' not in results:
                                results['semantic_analysis'] = {}
                            results['semantic_analysis'][f'{name}_individual'] = individual_semantic
                    
                    if enable_ml and ml_validator:
                        st.info("🤖 Running Advanced ML Analysis...")
                        ml_results = {}
                        anomaly_summaries = {}
                        
                        for name, dataset_df in data_sources.items():
                            # Get detailed ML analysis
                            ml_analysis = ml_validator.analyze_data_quality_advanced({name: dataset_df})
                            ml_results[name] = ml_analysis
                            
                            # Get anomaly summary
                            anomaly_summary = ml_validator.get_anomaly_summary(dataset_df)
                            anomaly_summaries[name] = anomaly_summary
                        
                        results['ml_analysis'] = ml_results
                        results['anomaly_summaries'] = anomaly_summaries
                    
                    if enable_agents and intelligent_agent:
                        st.info("🧠 Initializing Intelligent Validation Agent...")
                        # Initialize agent with dataset context
                        agent_context = intelligent_agent.get_dataset_summary(data_sources)
                        results['agent_context'] = agent_context
                    
                    results['data_sources'] = {name: {'rows': len(dataset_df), 'columns': len(dataset_df.columns)} for name, dataset_df in data_sources.items()}
                    
                    st.success("✅ Validation completed successfully!")
                    
                    # Display results
                    display_enhanced_results(results, data_sources, intelligent_agent)
                    
                except Exception as e:
                    st.error(f"❌ Error during validation: {str(e)}")
                    st.exception(e)
                    results = None

def display_enhanced_results(results: Dict, data_sources: Dict, intelligent_agent):
    """Display enhanced validation results."""
    st.header("📊 Enhanced Validation Results")
    
    # Display results in tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Overview", 
        "🔍 Semantic Analysis", 
        "🤖 ML Analysis", 
        "🧠 AI Agent", 
        "📈 Visualizations"
    ])
    
    with tab1:
        st.header("📊 Validation Overview")
        if 'data_sources' in results:
            st.subheader("📁 Datasets Analyzed")
            for name, info in results['data_sources'].items():
                st.info(f"**{name}**: {info['rows']} rows, {info['columns']} columns")
    
    with tab2:
        st.header("🔍 Semantic Analysis Results")
        if 'semantic_analysis' in results:
            semantic_data = results['semantic_analysis']
            
            # Display cross-dataset analysis
            if any('_individual' not in key for key in semantic_data.keys()):
                st.subheader("🌐 Cross-Dataset Column Analysis")
                for col_name, col_analysis in semantic_data.items():
                    if '_individual' not in col_name:
                        st.write(f"**Column: {col_name}**")
                        
                        if 'datasets' in col_analysis:
                            # Show dataset comparison
                            col1, col2 = st.columns(2)
                            with col1:
                                st.write("**Dataset Information:**")
                                for dataset_name, dataset_info in col_analysis['datasets'].items():
                                    st.write(f"- {dataset_name}: {dataset_info['total_rows']} rows, {dataset_info['unique_count']} unique values")
                            
                            with col2:
                                st.write("**Comparison Results:**")
                                comparison = col_analysis.get('comparison', {})
                                
                                # Data type consistency
                                if 'data_type_consistency' in comparison:
                                    dt_consistency = comparison['data_type_consistency']
                                    if dt_consistency.get('status') == 'consistent':
                                        st.success(f"✅ Data types consistent: {dt_consistency.get('type')}")
                                    else:
                                        st.error(f"❌ Data types inconsistent: {dt_consistency.get('types')}")
                                
                                # Sample differences
                                if 'sample_differences' in comparison:
                                    sample_diff = comparison['sample_differences']
                                    if sample_diff.get('status') == 'differences_found':
                                        st.warning("⚠️ Sample differences found:")
                                        for diff in sample_diff.get('examples', [])[:2]:  # Show max 2 examples
                                            st.write(f"- {diff['datasets'][0]} vs {diff['datasets'][1]}:")
                                            if diff.get('unique_to_first'):
                                                st.write(f"  Unique to {diff['datasets'][0]}: {diff['unique_to_first']}")
                                            if diff.get('unique_to_second'):
                                                st.write(f"  Unique to {diff['datasets'][1]}: {diff['unique_to_second']}")
                                
                                # Recommendations
                                if 'recommendations' in comparison and comparison['recommendations']:
                                    st.write("**Recommendations:**")
                                    for rec in comparison['recommendations'][:3]:  # Show max 3 recommendations
                                        st.write(f"• {rec}")
                        
                        st.divider()
            
            # Display individual dataset analysis
            st.subheader("📋 Individual Dataset Analysis")
            for key, analysis in semantic_data.items():
                if '_individual' in key:
                    dataset_name = key.replace('_individual', '')
                    st.write(f"**Dataset: {dataset_name}**")
                    
                    if 'semantic_analysis' in analysis:
                        for col_name, col_info in analysis['semantic_analysis'].items():
                            if isinstance(col_info, dict) and 'semantic_type' in col_info:
                                st.write(f"- {col_name}: {col_info['semantic_type']}")
                    
                    st.divider()
        else:
            st.info("🔍 Enable Semantic Analysis to see results here")
    
    with tab3:
        st.header("🤖 ML Analysis Results")
        if 'ml_analysis' in results and 'anomaly_summaries' in results:
            ml_data = results['ml_analysis']
            anomaly_data = results['anomaly_summaries']
            
            # Display anomaly summaries
            st.subheader("🚨 Anomaly Summary")
            total_anomalies_all = 0
            
            for dataset_name, anomaly_summary in anomaly_data.items():
                st.write(f"**Dataset: {dataset_name}**")
                
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Total Anomalies", anomaly_summary['total_anomalies'])
                    st.metric("Columns with Anomalies", anomaly_summary['columns_with_anomalies'])
                
                with col2:
                    st.metric("Overall Anomaly Rate", f"{anomaly_summary['overall_anomaly_rate']:.2%}")
                    
                    # Anomaly types breakdown
                    anomaly_types = anomaly_summary['anomaly_types']
                    st.write("**Anomaly Types:**")
                    for anomaly_type, count in anomaly_types.items():
                        if count > 0:
                            st.write(f"- {anomaly_type.replace('_', ' ').title()}: {count}")
                
                total_anomalies_all += anomaly_summary['total_anomalies']
                
                # Show detailed anomalies for columns
                if anomaly_summary['anomaly_details']:
                    with st.expander(f"📋 Detailed Anomalies for {dataset_name}"):
                        for col_name, col_details in anomaly_summary['anomaly_details'].items():
                            st.write(f"**Column: {col_name}** ({col_details['total_anomalies']} total anomalies)")
                            
                            details = col_details['details']
                            for anomaly_type, info in details.items():
                                if info['count'] > 0:
                                    st.write(f"- {anomaly_type.replace('_', ' ').title()}: {info['count']} ({info['percentage']:.1%})")
                                    
                                    # Show sample indices/values
                                    if 'indices' in info and info['indices']:
                                        st.write(f"  Sample indices: {info['indices'][:5]}...")
                                    elif 'values' in info and info['values']:
                                        st.write(f"  Sample values: {info['values'][:5]}...")
                
                # Show recommendations
                if anomaly_summary['recommendations']:
                    st.write("**Recommendations:**")
                    for rec in anomaly_summary['recommendations'][:3]:  # Show max 3
                        st.write(f"• {rec}")
                
                st.divider()
            
            # Overall summary
            st.subheader("📊 Overall Summary")
            st.metric("Total Anomalies Across All Datasets", total_anomalies_all)
            
            if total_anomalies_all > 0:
                st.warning("⚠️ Anomalies detected across datasets. Review recommendations above.")
            else:
                st.success("✅ No anomalies detected across all datasets!")
                
        else:
            st.info("🤖 Enable ML Analysis to see results here")
    
    with tab4:
        st.header("🧠 AI Agent Chat")
        if 'agent_context' in results:
            st.info("🤖 AI Agent is ready to help! Ask questions about your datasets.")
            
            # Show suggested questions
            st.subheader("💡 Suggested Questions")
            suggested_questions = [
                "What are the main data quality issues in my datasets?",
                "Which columns have the most anomalies?",
                "Are there any schema inconsistencies between datasets?",
                "What recommendations do you have for improving data quality?",
                "Can you analyze the relationship between specific columns?",
                "What patterns do you see in the data?",
                "Are there any data type mismatches?",
                "What's the overall health score of my data?"
            ]
            
            # Create columns for questions
            cols = st.columns(2)
            for i, question in enumerate(suggested_questions):
                col_idx = i % 2
                with cols[col_idx]:
                    if st.button(question, key=f"q_{i}"):
                        st.session_state.user_question = question
            
            # Chat interface
            st.subheader("💬 Chat with AI Agent")
            
            # Initialize chat history
            if 'chat_history' not in st.session_state:
                st.session_state.chat_history = []
            
            # User input
            user_question = st.text_input("Ask a question about your data:", key="user_input")
            
            if st.button("Send", key="send_button") or 'user_question' in st.session_state:
                if user_question or st.session_state.get('user_question'):
                    question = user_question or st.session_state.user_question
                    st.session_state.user_question = None  # Clear the suggested question
                    
                    if question:
                        # Add user question to chat
                        st.session_state.chat_history.append({"role": "user", "content": question})
                        
                        # Get AI response
                        with st.spinner("🤖 AI Agent is thinking..."):
                            try:
                                ai_response = intelligent_agent.chat_with_agent(
                                    question, 
                                    st.session_state.chat_history
                                )
                                st.session_state.chat_history.append({"role": "assistant", "content": ai_response})
                            except Exception as e:
                                error_msg = f"Sorry, I encountered an error: {str(e)}"
                                st.session_state.chat_history.append({"role": "assistant", "content": error_msg})
            
            # Display chat history
            if st.session_state.chat_history:
                st.subheader("💬 Chat History")
                for message in st.session_state.chat_history:
                    if message["role"] == "user":
                        st.write(f"**You:** {message['content']}")
                    else:
                        st.write(f"**AI Agent:** {message['content']}")
                    st.divider()
            
            # Clear chat button
            if st.button("🗑️ Clear Chat History"):
                st.session_state.chat_history = []
                st.rerun()
                
        else:
            st.info("🧠 Enable AI Agent to chat about your datasets")
    
    with tab5:
        st.header("📈 Enhanced Visualizations")
        if 'ml_analysis' in results:
            st.subheader("📊 Data Quality Visualizations")
            
            # Create sample visualizations
            for dataset_name, ml_results in results['ml_analysis'].items():
                st.write(f"**Dataset: {dataset_name}**")
                
                # Example 1: Data completeness heatmap
                if 'data_quality' in ml_results and 'completeness' in ml_results['data_quality']:
                    completeness = ml_results['data_quality']['completeness']
                    if completeness:
                        st.write("**Data Completeness Heatmap:**")
                        
                        # Create a simple completeness visualization
                        import pandas as pd
                        import plotly.express as px
                        
                        # Sample data for visualization
                        sample_data = {
                            'Column': list(completeness.keys())[:10],  # Show first 10 columns
                            'Completeness %': [completeness[col] * 100 for col in list(completeness.keys())[:10]]
                        }
                        
                        df_viz = pd.DataFrame(sample_data)
                        fig = px.bar(df_viz, x='Column', y='Completeness %', 
                                   title=f"Data Completeness - {dataset_name}",
                                   color='Completeness %',
                                   color_continuous_scale='RdYlGn')
                        fig.update_layout(xaxis_tickangle=-45)
                        st.plotly_chart(fig, use_container_width=True)
                
                # Example 2: Anomaly distribution
                if 'anomaly_summaries' in results and dataset_name in results['anomaly_summaries']:
                    anomaly_summary = results['anomaly_summaries'][dataset_name]
                    if anomaly_summary['anomaly_details']:
                        st.write("**Anomaly Distribution:**")
                        
                        # Create anomaly type chart
                        anomaly_types = anomaly_summary['anomaly_types']
                        anomaly_data = {
                            'Anomaly Type': list(anomaly_types.keys()),
                            'Count': list(anomaly_types.values())
                        }
                        
                        df_anomaly = pd.DataFrame(anomaly_data)
                        fig2 = px.pie(df_anomaly, values='Count', names='Anomaly Type',
                                    title=f"Anomaly Types - {dataset_name}")
                        st.plotly_chart(fig2, use_container_width=True)
                
                # Example 3: Data type distribution
                if 'data_sources' in results and dataset_name in data_sources:
                    dataset_df = data_sources[dataset_name]
                    st.write("**Data Type Distribution:**")
                    
                    dtype_counts = dataset_df.dtypes.value_counts()
                    fig3 = px.pie(values=dtype_counts.values, names=dtype_counts.index,
                                title=f"Data Types - {dataset_name}")
                    st.plotly_chart(fig3, use_container_width=True)
                
                st.divider()
        else:
            st.info("📈 Run ML Analysis to see visualizations here")
            
            # Show example visualizations even without data
            st.subheader("💡 Example Visualizations You'll See:")
            st.write("• **Data Completeness Heatmap**: Shows missing data patterns across columns")
            st.write("• **Anomaly Distribution**: Pie chart of different anomaly types")
            st.write("• **Data Type Distribution**: Breakdown of column data types")
            st.write("• **Correlation Heatmaps**: Relationships between numerical columns")
            st.write("• **Outlier Scatter Plots**: Visual identification of anomalies")
            st.write("• **Distribution Histograms**: Data distribution patterns")
            st.write("• **Time Series Trends**: If temporal data is present")
            st.write("• **Categorical Value Counts**: For text/categorical columns")
    
    # Download results
    st.header("💾 Download Results")
    
    if results:
        try:
            # Convert results to JSON for download
            results_json = json.dumps(results, default=safe_json_serialize, indent=2)
            
            st.download_button(
                label="📥 Download Full Results (JSON)",
                data=results_json,
                file_name="validation_results.json",
                mime="application/json"
            )
            
            # Create summary report
            summary_report = create_summary_report(results, data_sources)
            st.download_button(
                label="📥 Download Summary Report (TXT)",
                data=summary_report,
                file_name="validation_summary.txt",
                mime="text/plain"
            )
            
        except Exception as e:
            st.error(f"❌ Error creating download files: {str(e)}")
            st.info("💡 You can still view the results in the app above")
            
            # Fallback: try to create a simplified summary
            try:
                summary_report = create_summary_report(results, data_sources)
                st.download_button(
                    label="📥 Download Summary Report (TXT) - Fallback",
                    data=summary_report,
                    file_name="validation_summary.txt",
                    mime="text/plain"
                )
            except Exception as e2:
                st.error(f"❌ Could not create summary report: {str(e2)}")

def create_summary_report(results: Dict, data_sources: Dict) -> str:
    """Create a human-readable summary report."""
    report = []
    report.append("=" * 60)
    report.append("ADVANCED DATA VALIDATION REPORT")
    report.append("=" * 60)
    report.append("")
    
    # Dataset overview
    report.append("DATASET OVERVIEW:")
    report.append("-" * 30)
    for name, dataset_df in data_sources.items():
        report.append(f"Dataset: {name}")
        report.append(f"  Shape: {dataset_df.shape}")
        report.append(f"  Columns: {list(dataset_df.columns)}")
        report.append("")
    
    # Results summary
    if 'semantic_analysis' in results:
        report.append("SEMANTIC ANALYSIS:")
        report.append("-" * 30)
        semantic_data = results['semantic_analysis']
        if 'semantic_relationships' in semantic_data:
            report.append(f"Semantic relationships found: {len(semantic_data['semantic_relationships'])}")
        if 'mapping_recommendations' in semantic_data:
            report.append(f"Mapping recommendations: {len(semantic_data['mapping_recommendations'])}")
        report.append("")
    
    if 'ml_analysis' in results:
        report.append("ML ANALYSIS:")
        report.append("-" * 30)
        for dataset_name, analysis in results['ml_analysis'].items():
            report.append(f"Dataset: {dataset_name}")
            report.append(f"  Quality Score: {analysis.get('quality_score', 0):.2%}")
            if 'anomalies' in analysis:
                total_anomalies = sum(
                    len(anom.get('consensus_outliers', {}).get('indices', []))
                    for anom in analysis['anomalies'].values()
                    if 'error' not in anom
                )
                report.append(f"  Total Anomalies: {total_anomalies}")
        report.append("")
    
    if 'agent_analysis' in results:
        report.append("AI AGENT ANALYSIS:")
        report.append("-" * 30)
        agent_data = results['agent_analysis']
        if 'tools_used' in agent_data:
            report.append(f"Tools used: {', '.join(agent_data['tools_used'])}")
        report.append("")
    
    report.append("=" * 60)
    report.append("Report generated by Advanced Data Validation App")
    report.append("Powered by AIE7 Concepts")
    
    return "\n".join(report)

if __name__ == "__main__":
    main()
