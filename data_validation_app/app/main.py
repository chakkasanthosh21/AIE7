"""Main Streamlit application for the Data Validation App."""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import tempfile
import os
from typing import Dict, List
import json

from validation_engine import DataValidationEngine
from config.settings import settings


# Page configuration
st.set_page_config(
    page_title="AI Data Validation App",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .error-card {
        background-color: #ffe6e6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #ff4444;
    }
    .success-card {
        background-color: #e6ffe6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #44ff44;
    }
</style>
""", unsafe_allow_html=True)


def main():
    """Main application function."""
    
    # Header
    st.markdown('<h1 class="main-header">🔍 AI-Powered Data Validation App</h1>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.header("📁 Data Sources")
        
        # File upload section
        st.subheader("Upload Data Files")
        
        uploaded_files = {}
        supported_formats = settings.supported_formats
        
        for format_type in supported_formats:
            files = st.file_uploader(
                f"Upload {format_type.upper()} files",
                type=[format_type],
                accept_multiple_files=True,
                key=f"uploader_{format_type}"
            )
            
            if files:
                for i, file in enumerate(files):
                    key = f"{file.name}_{i}"
                    uploaded_files[key] = file
        
        # Manual data entry
        st.subheader("Or Enter Data Manually")
        manual_data = st.text_area(
            "Paste JSON data:",
            height=100,
            help="Enter data in JSON format"
        )
        
        if manual_data:
            try:
                data = json.loads(manual_data)
                if isinstance(data, list):
                    df = pd.DataFrame(data)
                    uploaded_files["manual_data"] = df
                st.success("Manual data loaded successfully!")
            except Exception as e:
                st.error(f"Error parsing JSON: {str(e)}")
        
        # Validation settings
        st.subheader("⚙️ Validation Settings")
        
        enable_schema_validation = st.checkbox("Schema Validation", value=True)
        enable_quality_analysis = st.checkbox("Quality Analysis", value=True)
        enable_semantic_validation = st.checkbox("Semantic Validation", value=True)
        
        # Run validation button
        if st.button("🚀 Run Validation", type="primary", use_container_width=True):
            st.session_state.run_validation = True
    
    # Main content area
    if 'run_validation' not in st.session_state:
        st.session_state.run_validation = False
    
    if st.session_state.run_validation and uploaded_files:
        run_validation_workflow(uploaded_files)
    elif not uploaded_files:
        show_welcome_message()
    else:
        show_upload_instructions()


def show_welcome_message():
    """Display welcome message and app description."""
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
        ## 🎯 Welcome to AI-Powered Data Validation!
        
        This application helps you validate multiple data sources for:
        
        - **Schema Consistency** - Detect column mismatches and type conflicts
        - **Data Quality** - Analyze completeness, consistency, and validity
        - **Semantic Validation** - Identify semantic inconsistencies across sources
        - **Intelligent Recommendations** - Get AI-powered suggestions for improvements
        
        ### 🚀 How to Use:
        1. **Upload your data files** using the sidebar (CSV, JSON, Excel, Parquet)
        2. **Configure validation settings** as needed
        3. **Click "Run Validation"** to start the analysis
        4. **Review results** and implement recommendations
        
        ### 💡 Supported Formats:
        - CSV files
        - JSON files  
        - Excel files (xlsx, xls)
        - Parquet files
        
        Start by uploading your data files in the sidebar! 📁
        """)
        
        # Show sample data structure
        with st.expander("📊 Sample Data Structure"):
            sample_data = {
                "users": pd.DataFrame({
                    "id": [1, 2, 3],
                    "name": ["Alice", "Bob", "Charlie"],
                    "email": ["alice@example.com", "bob@example.com", "charlie@example.com"],
                    "age": [25, 30, 35]
                }),
                "orders": pd.DataFrame({
                    "order_id": [101, 102, 103],
                    "user_id": [1, 2, 1],
                    "amount": [100.50, 75.25, 200.00],
                    "status": ["completed", "pending", "completed"]
                })
            }
            
            st.write("**Sample Users Dataset:**")
            st.dataframe(sample_data["users"])
            
            st.write("**Sample Orders Dataset:**")
            st.dataframe(sample_data["orders"])
            
            st.info("""
            **Validation Example:** 
            The app would detect that `users.id` and `orders.user_id` are related columns 
            and validate referential integrity between these datasets.
            """)


def show_upload_instructions():
    """Show instructions for uploading data."""
    st.info("📁 Please upload your data files using the sidebar to begin validation.")


def run_validation_workflow(uploaded_files: Dict):
    """Run the validation workflow."""
    
    st.header("🔍 Running Data Validation...")
    
    # Progress bar
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    try:
        # Step 1: Load data
        status_text.text("📥 Loading data files...")
        progress_bar.progress(25)
        
        data_sources = load_data_sources(uploaded_files)
        
        if not data_sources:
            st.error("❌ No valid data sources found. Please check your file uploads.")
            return
        
        # Step 2: Initialize validation engine
        status_text.text("🤖 Initializing AI validation engine...")
        progress_bar.progress(50)
        
        validation_engine = DataValidationEngine()
        
        # Step 3: Run validation
        status_text.text("🔍 Running validation analysis...")
        progress_bar.progress(75)
        
        with st.spinner("Running AI-powered validation..."):
            validation_result = validation_engine.validate_data_sources_sync(data_sources)
        
        # Step 4: Display results
        status_text.text("✅ Validation complete! Displaying results...")
        progress_bar.progress(100)
        
        display_validation_results(validation_result, data_sources)
        
    except Exception as e:
        st.error(f"❌ Error during validation: {str(e)}")
        st.exception(e)


def load_data_sources(uploaded_files: Dict) -> Dict[str, pd.DataFrame]:
    """Load data from uploaded files."""
    
    data_sources = {}
    
    for key, file in uploaded_files.items():
        try:
            if isinstance(file, pd.DataFrame):
                # Manual data entry
                data_sources[key] = file
            else:
                # File upload
                if file.name.endswith('.csv'):
                    df = pd.read_csv(file)
                elif file.name.endswith('.json'):
                    df = pd.read_json(file)
                elif file.name.endswith(('.xlsx', '.xls')):
                    df = pd.read_excel(file)
                elif file.name.endswith('.parquet'):
                    df = pd.read_parquet(file)
                else:
                    continue
                
                data_sources[key] = df
                
        except Exception as e:
            st.warning(f"⚠️ Could not load {file.name}: {str(e)}")
            continue
    
    return data_sources


def display_validation_results(validation_result, data_sources: Dict[str, pd.DataFrame]):
    """Display validation results in an organized way."""
    
    st.header("📊 Validation Results")
    
    # Overview metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Data Sources", len(data_sources))
    
    with col2:
        error_count = len(validation_result.errors)
        st.metric("Issues Found", error_count, delta=f"{error_count} issues")
    
    with col3:
        avg_quality = validation_result.quality_metrics.get('average_score', 0)
        st.metric("Overall Quality", f"{avg_quality:.1%}")
    
    with col4:
        rec_count = len(validation_result.recommendations)
        st.metric("Recommendations", rec_count)
    
    # Tabs for different result sections
    tab1, tab2, tab3, tab4 = st.tabs([
        "🔍 Schema Analysis", 
        "📈 Quality Metrics", 
        "⚠️ Issues & Errors", 
        "💡 Recommendations"
    ])
    
    with tab1:
        display_schema_analysis(validation_result.schema_analysis)
    
    with tab2:
        display_quality_metrics(validation_result.quality_metrics, data_sources)
    
    with tab3:
        display_issues_and_errors(validation_result.errors)
    
    with tab4:
        display_recommendations(validation_result.recommendations)
    
    # Data preview
    with st.expander("📋 Data Preview"):
        for name, df in data_sources.items():
            st.subheader(f"📁 {name}")
            st.dataframe(df.head(), use_container_width=True)
            st.write(f"Shape: {df.shape}")


def display_schema_analysis(schema_analysis: Dict):
    """Display schema analysis results."""
    
    if not schema_analysis:
        st.info("No schema analysis available.")
        return
    
    if schema_analysis.get('has_conflicts'):
        st.error("❌ Schema conflicts detected!")
        
        for conflict in schema_analysis.get('conflicts', []):
            st.markdown(f"- **{conflict}**")
        
        # Show detailed schema comparison
        if 'schemas' in schema_analysis:
            st.subheader("📊 Schema Comparison")
            
            schemas = schema_analysis['schemas']
            comparison_data = []
            
            for name, schema in schemas.items():
                comparison_data.append({
                    'Source': name,
                    'Columns': len(schema['columns']),
                    'Rows': schema['shape'][0],
                    'Null Values': sum(schema['null_counts'].values())
                })
            
            comparison_df = pd.DataFrame(comparison_data)
            st.dataframe(comparison_df, use_container_width=True)
    else:
        st.success("✅ No schema conflicts detected!")
        
        if 'schemas' in schema_analysis:
            st.subheader("📊 Schema Summary")
            schemas = schema_analysis['schemas']
            
            for name, schema in schemas.items():
                with st.expander(f"📁 {name}"):
                    st.write(f"**Columns:** {len(schema['columns'])}")
                    st.write(f"**Rows:** {schema['shape'][0]}")
                    st.write(f"**Data Types:**")
                    for col, dtype in schema['dtypes'].items():
                        st.write(f"  - {col}: {dtype}")


def display_quality_metrics(quality_metrics: Dict, data_sources: Dict):
    """Display quality metrics with visualizations."""
    
    if not quality_metrics:
        st.info("No quality metrics available.")
        return
    
    # Overall quality score
    overall_score = quality_metrics.get('average_score', 0)
    
    if overall_score >= 0.8:
        st.success(f"🎯 Overall Quality Score: {overall_score:.1%}")
    elif overall_score >= 0.6:
        st.warning(f"⚠️ Overall Quality Score: {overall_score:.1%}")
    else:
        st.error(f"❌ Overall Quality Score: {overall_score:.1%}")
    
    # Quality breakdown
    metrics = ['completeness', 'consistency', 'uniqueness', 'validity']
    values = [quality_metrics.get(metric, 0) for metric in metrics]
    
    # Create radar chart
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=metrics,
        fill='toself',
        name='Quality Metrics',
        line_color='#1f77b4'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 1]
            )),
        showlegend=False,
        title="Data Quality Radar Chart"
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Detailed metrics
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Quality Breakdown")
        for metric in metrics:
            value = quality_metrics.get(metric, 0)
            st.metric(metric.title(), f"{value:.1%}")
    
    with col2:
        st.subheader("💡 Quality Insights")
        if overall_score >= 0.9:
            st.success("Excellent data quality! Your datasets are well-maintained.")
        elif overall_score >= 0.7:
            st.info("Good data quality with room for improvement.")
        else:
            st.warning("Data quality needs attention. Review the recommendations.")


def display_issues_and_errors(errors: List[str]):
    """Display validation issues and errors."""
    
    if not errors:
        st.success("✅ No validation issues found!")
        return
    
    st.error(f"❌ Found {len(errors)} validation issues:")
    
    for i, error in enumerate(errors, 1):
        st.markdown(f"**{i}.** {error}")
    
    # Categorize errors
    error_categories = {
        'Schema': [e for e in errors if 'schema' in e.lower()],
        'Quality': [e for e in errors if any(word in e.lower() for word in ['quality', 'completeness', 'consistency'])],
        'Semantic': [e for e in errors if 'semantic' in e.lower()],
        'Other': [e for e in errors if not any(word in e.lower() for word in ['schema', 'quality', 'completeness', 'consistency', 'semantic'])]
    }
    
    st.subheader("📊 Error Categories")
    
    for category, category_errors in error_categories.items():
        if category_errors:
            with st.expander(f"{category} ({len(category_errors)} issues)"):
                for error in category_errors:
                    st.markdown(f"- {error}")


def display_recommendations(recommendations: List[str]):
    """Display AI-generated recommendations."""
    
    if not recommendations:
        st.info("No recommendations available.")
        return
    
    st.success(f"💡 Generated {len(recommendations)} recommendations:")
    
    for i, rec in enumerate(recommendations, 1):
        st.markdown(f"**{i}.** {rec}")
    
    # Action items
    st.subheader("🚀 Next Steps")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Immediate Actions:**
        - Review all validation issues
        - Prioritize critical problems
        - Implement schema standardization
        """)
    
    with col2:
        st.markdown("""
        **Long-term Improvements:**
        - Set up automated validation
        - Create data quality dashboards
        - Establish data governance processes
        """)
    
    # Export results
    if st.button("📥 Export Validation Report"):
        export_validation_report(recommendations)


def export_validation_report(recommendations: List[str]):
    """Export validation results to a file."""
    
    report_content = f"""
# Data Validation Report

## Summary
Generated on: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}

## Recommendations
{chr(10).join([f"{i+1}. {rec}" for i, rec in enumerate(recommendations)])}

## Next Steps
1. Review all validation issues
2. Implement recommended fixes
3. Set up ongoing monitoring
4. Establish data quality processes
    """
    
    # Create download button
    st.download_button(
        label="📥 Download Report",
        data=report_content,
        file_name="validation_report.md",
        mime="text/markdown"
    )


if __name__ == "__main__":
    main()
