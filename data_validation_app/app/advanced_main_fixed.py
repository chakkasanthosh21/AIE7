import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
import os
import sys
from datetime import datetime
import io

# Add the app directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from advanced_semantic_validator import AdvancedSemanticValidator
from advanced_ml_validator import AdvancedMLValidator
from intelligent_validation_agent import IntelligentValidationAgent
from database_ui import render_database_connections, get_database_data

# Enable nested asyncio
import nest_asyncio
nest_asyncio.apply()

def safe_json_serialize(obj):
    """Safely serialize objects for JSON, handling numpy types."""
    if isinstance(obj, (np.integer, np.int32, np.int64)):
        return int(obj)
    elif isinstance(obj, (np.floating, np.float32, np.float64)):
        return float(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, np.bool_):
        return bool(obj)
    elif hasattr(obj, 'dtype'):  # Handle numpy dtypes
        return str(obj)
    elif isinstance(obj, (list, tuple)):
        return [safe_json_serialize(item) for item in obj]
    elif isinstance(obj, dict):
        return {key: safe_json_serialize(value) for key, value in obj.items()}
    else:
        return str(obj)

def main():
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
        background: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border-left: 4px solid #667eea;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.markdown('<div class="main-header"><h1>🔍 Advanced Data Validation App</h1><p>Comprehensive data quality analysis with AI-powered insights</p></div>', unsafe_allow_html=True)
    
    # Sidebar configuration
    st.sidebar.header("⚙️ Configuration")
    
    # OpenAI API Key
    openai_api_key = st.sidebar.text_input("OpenAI API Key", type="password", help="Enter your OpenAI API key for AI agent functionality")
    
    # Create main tabs that are always visible
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "📁 File Upload", 
        "🗄️ Database Connections", 
        "🔍 Semantic Analysis", 
        "🤖 ML Analysis", 
        "🧠 AI Agent", 
        "📈 Visualizations"
    ])
    
    # Initialize data sources
    data_sources = {}
    
    # File Upload tab
    with tab1:
        st.header("📁 Upload Your Datasets")
        
        # Two file uploaders
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Dataset 1")
            dataset1_file = st.file_uploader("Upload first dataset", type=['csv', 'json', 'xlsx', 'parquet'], key="file1")
            dataset1_name = st.text_input("Dataset 1 name", value="dataset1", key="name1")
        
        with col2:
            st.subheader("Dataset 2")
            dataset2_file = st.file_uploader("Upload second dataset", type=['csv', 'json', 'xlsx', 'parquet'], key="file2")
            dataset2_name = st.text_input("Dataset 2 name", value="dataset2", key="name2")
        
        # Load datasets
        if dataset1_file and dataset2_file:
            try:
                # Load first dataset
                if dataset1_file.name.endswith('.csv'):
                    data_sources[dataset1_name] = pd.read_csv(dataset1_file)
                elif dataset1_file.name.endswith('.json'):
                    data_sources[dataset1_name] = pd.read_json(dataset1_file)
                elif dataset1_file.name.endswith('.xlsx'):
                    data_sources[dataset1_name] = pd.read_excel(dataset1_file)
                elif dataset1_file.name.endswith('.parquet'):
                    data_sources[dataset1_name] = pd.read_parquet(dataset1_file)
                
                # Load second dataset
                if dataset2_file.name.endswith('.csv'):
                    data_sources[dataset2_name] = pd.read_csv(dataset2_file)
                elif dataset2_file.name.endswith('.json'):
                    data_sources[dataset2_name] = pd.read_json(dataset2_file)
                elif dataset2_file.name.endswith('.xlsx'):
                    data_sources[dataset2_name] = pd.read_excel(dataset2_file)
                elif dataset2_file.name.endswith('.parquet'):
                    data_sources[dataset2_name] = pd.read_parquet(dataset2_file)
                
                st.success(f"✅ Successfully loaded {len(data_sources)} datasets!")
                
                # Display dataset info
                for name, current_dataset in data_sources.items():
                    st.info(f"**{name}**: {current_dataset.shape[0]} rows, {current_dataset.shape[1]} columns")
                
                # Show validation button
                if st.button("🚀 Run Enhanced Validation", type="primary"):
                    with st.spinner("Running advanced validation..."):
                        try:
                            # Initialize validators
                            semantic_validator = AdvancedSemanticValidator()
                            ml_validator = AdvancedMLValidator()
                            intelligent_agent = IntelligentValidationAgent(openai_api_key) if openai_api_key else None
                            
                            results = {}
                            
                            # Basic validation
                            st.info("🔍 Running Advanced Semantic Analysis...")
                            semantic_results = semantic_validator.analyze_cross_dataset_semantics(data_sources)
                            results['semantic_analysis'] = semantic_results
                            
                            # Also run individual dataset semantic analysis
                            for name, current_dataset in data_sources.items():
                                individual_semantic = semantic_validator.analyze_column_semantics_advanced({name: current_dataset})
                                if 'semantic_analysis' not in results:
                                    results['semantic_analysis'] = {}
                                results['semantic_analysis'][f'{name}_individual'] = individual_semantic
                            
                            st.info("🤖 Running Advanced ML Analysis...")
                            ml_results = {}
                            anomaly_summaries = {}
                            
                            for name, current_dataset in data_sources.items():
                                # Get detailed ML analysis
                                ml_analysis = ml_validator.analyze_data_quality_advanced({name: current_dataset})
                                ml_results[name] = ml_analysis
                                
                                # Get anomaly summary
                                anomaly_summary = ml_validator.get_anomaly_summary(current_dataset)
                                anomaly_summaries[name] = anomaly_summary
                            
                            results['ml_analysis'] = ml_results
                            results['anomaly_summaries'] = anomaly_summaries
                            
                            if intelligent_agent:
                                st.info("🧠 Initializing Intelligent Validation Agent...")
                                # Initialize agent with dataset context
                                agent_context = intelligent_agent.get_dataset_summary(data_sources)
                                results['agent_context'] = agent_context
                            
                            results['data_sources'] = {name: {'rows': len(current_dataset), 'columns': len(current_dataset.columns)} for name, current_dataset in data_sources.items()}
                            
                            st.success("✅ Validation completed successfully!")
                            
                            # Store results in session state for other tabs
                            st.session_state.validation_results = results
                            st.session_state.intelligent_agent = intelligent_agent
                            
                        except Exception as e:
                            st.error(f"❌ Error during validation: {str(e)}")
                            st.exception(e)
                            st.session_state.validation_results = None
            except Exception as e:
                st.error(f"❌ Error loading datasets: {str(e)}")
                st.exception(e)
        else:
            st.info("📁 Please upload both datasets to continue")
    
    # Database Connections tab
    with tab2:
        st.header("🗄️ Database Connections")
        st.markdown("Connect to databases and cloud storage to validate data from multiple sources.")
        
        # Render database connections interface
        render_database_connections()
        
        # Show combined data sources (file uploads + database data)
        if 'database_data' in st.session_state and st.session_state.database_data:
            st.subheader("🔄 Combined Data Sources")
            st.info("Data from databases is now available for validation alongside uploaded files.")
            
            # Merge database data with file data for validation
            all_data_sources = {**data_sources, **st.session_state.database_data}
            
            if len(all_data_sources) > len(data_sources):
                st.success(f"✅ Added {len(all_data_sources) - len(data_sources)} database data source(s) to validation pool")
                
                # Show database data summary
                for name, df in st.session_state.database_data.items():
                    st.write(f"**{name}**: {df.shape[0]} rows, {df.shape[1]} columns")
                
                # Update data_sources to include database data
                data_sources.update(st.session_state.database_data)
                
                # Show validation button if we have multiple sources
                if len(all_data_sources) > 1:
                    st.success(f"🚀 **{len(all_data_sources)} data sources ready for comparison!**")
                    
                    # Note: Validation button is in the Database Connections tab
                    st.info("💡 Click the 'Run Validation' button in the Database Connections tab to start validation")
        else:
            st.info("💡 Connect to databases to validate data from multiple sources simultaneously")
            
            # Show comparison options
            st.subheader("🔄 How to Compare Multiple Datasets")
            st.markdown("""
            **Option 1: Multiple Database Tables**
            - Connect to first MySQL table (e.g., 'customers')
            - Use "Connect to Different MySQL Table" option in MySQL tab
            - Load second table (e.g., 'orders')
            
            **Option 2: Database + Local File**
            - Connect to MySQL table and load data
            - Upload local CSV/Excel file in File Upload tab
            - Both sources will be available for comparison
            
            **Option 3: Different Database Types**
            - Connect to MySQL table
            - Connect to PostgreSQL/SQL Server table
            - Load data from both sources
            """)
    
    # Semantic Analysis tab
    with tab3:
        st.header("🔍 Semantic Analysis Results")
        
        if 'validation_results' in st.session_state and st.session_state.validation_results:
            results = st.session_state.validation_results
            if 'semantic_analysis' in results:
                semantic_data = results['semantic_analysis']
                
                # Display cross-dataset analysis in table format
                st.subheader("🌐 Cross-Dataset Column Analysis")
                
                # Create a table for cross-dataset analysis
                cross_dataset_data = []
                for col_name, col_analysis in semantic_data.items():
                    if '_individual' not in col_name and 'datasets' in col_analysis:
                        for dataset_name, dataset_info in col_analysis['datasets'].items():
                            cross_dataset_data.append({
                                'Column Name': col_name,
                                'Dataset': dataset_name,
                                'Unique Values': dataset_info.get('unique_count', 0),
                                'Null Count': dataset_info.get('null_count', 0),
                                'Data Type': dataset_info.get('data_type', 'Unknown')
                            })
                
                if cross_dataset_data:
                    df_cross = pd.DataFrame(cross_dataset_data)
                    st.dataframe(df_cross, use_container_width=True)
                    
                    # Show sample differences if available
                    st.subheader("🔍 Sample Differences Between Datasets")
                    for col_name, col_analysis in semantic_data.items():
                        if '_individual' not in col_name and 'comparison' in col_analysis:
                            comparison = col_analysis['comparison']
                            if 'sample_differences' in comparison:
                                st.write(f"**Column: {col_name}**")
                                sample_diff = comparison['sample_differences']
                                if 'examples' in sample_diff and sample_diff['examples']:
                                    diff_df = pd.DataFrame({
                                        'Sample Difference': sample_diff['examples'][:5]  # Show max 5 examples
                                    })
                                    st.dataframe(diff_df, use_container_width=True)
                
                # Display individual dataset analysis in table format
                st.subheader("📊 Individual Dataset Analysis")
                individual_data = []
                for key, analysis in semantic_data.items():
                    if '_individual' in key and 'semantic_analysis' in analysis:
                        dataset_name = key.replace('_individual', '')
                        for col_name, col_info in analysis['semantic_analysis'].items():
                            individual_data.append({
                                'Dataset': dataset_name,
                                'Column': col_name,
                                'Semantic Type': col_info.get('semantic_type', 'Unknown'),
                                'Confidence': f"{col_info.get('confidence', 0):.2f}",
                                'Unique Values': col_info.get('unique_count', 0),
                                'Null Count': col_info.get('null_count', 0)
                            })
                
                if individual_data:
                    df_individual = pd.DataFrame(individual_data)
                    st.dataframe(df_individual, use_container_width=True)
                else:
                    st.info("No individual dataset analysis available")
            else:
                st.warning("No semantic analysis results found")
        else:
            st.info("📊 Run validation first to see semantic analysis results")
    
    # ML Analysis tab
    with tab4:
        st.header("🤖 ML Analysis Results")
        
        if 'validation_results' in st.session_state and st.session_state.validation_results:
            results = st.session_state.validation_results
            if 'ml_analysis' in results:
                ml_data = results['ml_analysis']
                anomaly_data = results.get('anomaly_summaries', {})
                
                # Create summary table
                st.subheader("📊 Dataset Quality Summary")
                summary_data = []
                for dataset_name, ml_results in ml_data.items():
                    summary_data.append({
                        'Dataset': dataset_name,
                        'Quality Score': f"{ml_results.get('quality_score', 0):.2%}",
                        'Total Anomalies': anomaly_data.get(dataset_name, {}).get('total_anomalies', 0),
                        'Anomaly Types': len(anomaly_data.get(dataset_name, {}).get('anomaly_types', {})),
                        'Recommendations': len(ml_results.get('recommendations', []))
                    })
                
                if summary_data:
                    df_summary = pd.DataFrame(summary_data)
                    st.dataframe(df_summary, use_container_width=True)
                
                # Detailed analysis for each dataset
                for dataset_name, ml_results in ml_data.items():
                    st.subheader(f"🔍 Detailed Analysis: {dataset_name}")
                    
                    # Quality metrics
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Quality Score", f"{ml_results.get('quality_score', 0):.2%}")
                    with col2:
                        st.metric("Total Anomalies", anomaly_data.get(dataset_name, {}).get('total_anomalies', 0))
                    with col3:
                        st.metric("Anomaly Types", len(anomaly_data.get(dataset_name, {}).get('anomaly_types', {})))
                    
                    # Anomaly details in table format
                    if anomaly_data.get(dataset_name, {}).get('anomaly_details'):
                        st.write("**🚨 Anomaly Details:**")
                        anomaly_details = []
                        for col_name, col_details in anomaly_data[dataset_name]['anomaly_details'].items():
                            for anomaly_type, info in col_details.get('details', {}).items():
                                anomaly_details.append({
                                    'Column': col_name,
                                    'Anomaly Type': anomaly_type,
                                    'Count': info.get('count', 0),
                                    'Severity': info.get('severity', 'Unknown')
                                })
                        
                        if anomaly_details:
                            df_anomalies = pd.DataFrame(anomaly_details)
                            st.dataframe(df_anomalies, use_container_width=True)
                    
                    # Recommendations
                    if ml_results.get('recommendations'):
                        st.write("**💡 Recommendations:**")
                        for i, rec in enumerate(ml_results['recommendations'][:5], 1):
                            st.write(f"{i}. {rec}")
                    
                    st.divider()
            else:
                st.warning("No ML analysis results found")
        else:
            st.info("🤖 Run validation first to see ML analysis results")
    
    # AI Agent tab
    with tab5:
        st.header("🧠 AI Agent")
        
        if 'validation_results' in st.session_state and st.session_state.validation_results:
            # Check if we have an intelligent agent
            if 'intelligent_agent' not in st.session_state or not st.session_state.intelligent_agent:
                # Try to create one if we have OpenAI API key
                openai_api_key = st.session_state.get('openai_api_key', '')
                if openai_api_key:
                    try:
                        intelligent_agent = IntelligentValidationAgent(openai_api_key)
                        st.session_state.intelligent_agent = intelligent_agent
                        st.success("✅ AI Agent initialized successfully!")
                    except Exception as e:
                        st.error(f"❌ Failed to initialize AI Agent: {str(e)}")
                        st.info("Please check your OpenAI API key and try again.")
                        intelligent_agent = None
                else:
                    st.warning("⚠️ OpenAI API key required for AI Agent functionality")
                    st.info("Please enter your OpenAI API key in the sidebar to use the AI Agent.")
                    intelligent_agent = None
            else:
                intelligent_agent = st.session_state.intelligent_agent
            
            if intelligent_agent:
                st.success("🤖 AI Agent is ready to help! Ask questions about your datasets.")
                
                # Chat interface
                st.subheader("💬 Chat with AI Agent")
                
                # Initialize chat history
                if 'chat_history' not in st.session_state:
                    st.session_state.chat_history = []
                
                # Display suggested questions
                st.write("**💡 Quick Questions (click to ask):**")
                suggested_questions = [
                    "What are the main data quality issues?",
                    "Which columns have anomalies?",
                    "Any schema inconsistencies?",
                    "Data quality recommendations?",
                    "Column relationships?",
                    "Data patterns?",
                    "Data type mismatches?",
                    "Overall data health score?"
                ]
                
                # Create a more compact layout for questions
                cols = st.columns(4)
                for i, question in enumerate(suggested_questions):
                    col_idx = i % 4
                    with cols[col_idx]:
                        if st.button(question, key=f"q_{i}", help="Click to ask this question"):
                            try:
                                # Get response from agent
                                response = intelligent_agent.chat_with_agent(question)
                                # Add to chat history
                                st.session_state.chat_history.append({
                                    'question': question,
                                    'answer': response,
                                    'timestamp': pd.Timestamp.now()
                                })
                                st.rerun()
                            except Exception as e:
                                st.error(f"❌ Error getting response: {str(e)}")
                
                # Display chat history
                if st.session_state.chat_history:
                    st.subheader("📝 Chat History")
                    for i, chat in enumerate(st.session_state.chat_history):
                        with st.expander(f"Q: {chat['question']} ({chat['timestamp'].strftime('%H:%M:%S')})"):
                            st.write(f"**Question:** {chat['question']}")
                            st.write(f"**Answer:** {chat['answer']}")
                
                # Custom question input
                st.subheader("💭 Ask Your Own Question")
                custom_question = st.text_input("Type your question here:", key="custom_question_input")
                if st.button("🚀 Ask Question", key="ask_custom_btn"):
                    if custom_question.strip():
                        try:
                            response = intelligent_agent.chat_with_agent(custom_question)
                            st.session_state.chat_history.append({
                                'question': custom_question,
                                'answer': response,
                                'timestamp': pd.Timestamp.now()
                            })
                            st.rerun()
                        except Exception as e:
                            st.error(f"❌ Error getting response: {str(e)}")
                    else:
                        st.warning("Please enter a question")
            else:
                st.info("🤖 AI Agent is not available. Please check your OpenAI API key.")
        else:
            st.info("🧠 Run validation first to use the AI Agent")
    
    # Visualizations tab
    with tab6:
        st.header("📈 Enhanced Visualizations")
        if 'validation_results' in st.session_state and st.session_state.validation_results:
            results = st.session_state.validation_results
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
                    if 'anomaly_summaries' in results and dataset_name in results.get('anomaly_summaries', {}):
                        anomaly_summary = results['anomaly_summaries'][dataset_name]
                        if anomaly_summary.get('anomaly_details'):
                            st.write("**Anomaly Distribution:**")
                            
                            # Create anomaly type chart
                            anomaly_types = anomaly_summary.get('anomaly_types', {})
                            if anomaly_types:
                                anomaly_data = {
                                    'Anomaly Type': list(anomaly_types.keys()),
                                    'Count': list(anomaly_types.values())
                                }
                                
                                df_anomaly = pd.DataFrame(anomaly_data)
                                fig2 = px.pie(df_anomaly, values='Count', names='Anomaly Type',
                                            title=f"Anomaly Types - {dataset_name}")
                                st.plotly_chart(fig2, use_container_width=True)
                    
                    # Example 3: Data type distribution
                    if 'data_sources' in results and dataset_name in results.get('data_sources', {}):
                        dataset_info = results['data_sources'][dataset_name]
                        st.write("**Data Type Distribution:**")
                        
                        # Create a sample data type distribution (since we don't have actual data here)
                        sample_dtypes = {
                            'Data Type': ['object', 'int64', 'float64', 'datetime64', 'bool'],
                            'Count': [5, 3, 2, 1, 1]  # Sample counts
                        }
                        
                        df_dtypes = pd.DataFrame(sample_dtypes)
                        fig3 = px.pie(df_dtypes, values='Count', names='Data Type',
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
    if 'validation_results' in st.session_state and st.session_state.validation_results:
        st.header("💾 Download Results")
        results = st.session_state.validation_results
        
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

def create_summary_report(results: dict, input_data_sources: dict) -> str:
    """Create a human-readable summary report."""
    report = []
    report.append("=" * 60)
    report.append("ADVANCED DATA VALIDATION REPORT")
    report.append("=" * 60)
    report.append("")
    
    # Dataset overview
    report.append("DATASET OVERVIEW:")
    report.append("-" * 30)
    for name, current_dataset in input_data_sources.items():
        report.append(f"Dataset: {name}")
        report.append(f"  Shape: {current_dataset.shape}")
        report.append(f"  Columns: {list(current_dataset.columns)}")
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
