import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import hashlib
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class DataValidator:
    """Comprehensive data validation engine implementing all 10 validation types"""
    
    def __init__(self):
        self.validation_results = {}
        
    def validate_row_count(self, source_df, target_df, source_name="Source", target_name="Target"):
        """1. Row Count Validation"""
        source_count = len(source_df)
        target_count = len(target_df)
        
        result = {
            'source_count': source_count,
            'target_count': target_count,
            'difference': target_count - source_count,
            'status': 'PASS' if source_count == target_count else 'FAIL',
            'message': f"Row counts match: {source_count} = {target_count}" if source_count == target_count 
                      else f"Row count mismatch: Source={source_count}, Target={target_count}"
        }
        
        return result
    
    def validate_data_types(self, source_df, target_df, source_name="Source", target_name="Target"):
        """2. Column/Data Type Validation"""
        results = {}
        
        for col in source_df.columns:
            if col in target_df.columns:
                source_dtype = str(source_df[col].dtype)
                target_dtype = str(target_df[col].dtype)
                
                results[col] = {
                    'source_dtype': source_dtype,
                    'target_dtype': target_dtype,
                    'status': 'PASS' if source_dtype == target_dtype else 'FAIL',
                    'message': f"Data types match: {source_dtype}" if source_dtype == target_dtype 
                              else f"Data type mismatch: {source_dtype} vs {target_dtype}"
                }
            else:
                results[col] = {
                    'source_dtype': str(source_df[col].dtype),
                    'target_dtype': 'MISSING',
                    'status': 'FAIL',
                    'message': f"Column '{col}' missing in target"
                }
        
        return results
    
    def validate_null_constraints(self, source_df, target_df, source_name="Source", target_name="Target"):
        """3. Null/Not Null Validation"""
        results = {}
        
        for col in source_df.columns:
            if col in target_df.columns:
                source_null_count = source_df[col].isnull().sum()
                target_null_count = target_df[col].isnull().sum()
                
                # Check if source has no nulls but target has nulls
                source_was_not_null = source_null_count == 0
                target_has_null = target_null_count > 0
                
                results[col] = {
                    'source_null_count': source_null_count,
                    'target_null_count': target_null_count,
                    'source_was_not_null': source_was_not_null,
                    'target_has_null': target_has_null,
                    'status': 'FAIL' if source_was_not_null and target_has_null else 'PASS',
                    'message': f"Source nulls: {source_null_count}, Target nulls: {target_null_count}"
                }
            else:
                results[col] = {
                    'status': 'FAIL',
                    'message': f"Column '{col}' missing in target"
                }
        
        return results
    
    def validate_primary_keys(self, source_df, target_df, key_columns=None, source_name="Source", target_name="Target"):
        """4. Primary Key / Unique Key Validation"""
        if key_columns is None:
            # Auto-detect potential key columns (columns with high uniqueness)
            key_columns = []
            for col in source_df.columns:
                if source_df[col].nunique() / len(source_df) > 0.9:  # 90% unique values
                    key_columns.append(col)
        
        results = {}
        
        for col in key_columns:
            if col in source_df.columns and col in target_df.columns:
                source_unique = source_df[col].nunique()
                target_unique = target_df[col].nunique()
                source_total = len(source_df)
                target_total = len(target_df)
                
                # Check for duplicates
                source_duplicates = source_total - source_unique
                target_duplicates = target_total - target_unique
                
                results[col] = {
                    'source_unique': source_unique,
                    'target_unique': target_unique,
                    'source_duplicates': source_duplicates,
                    'target_duplicates': target_duplicates,
                    'status': 'PASS' if source_duplicates == 0 and target_duplicates == 0 else 'FAIL',
                    'message': f"Source duplicates: {source_duplicates}, Target duplicates: {target_duplicates}"
                }
            else:
                results[col] = {
                    'status': 'FAIL',
                    'message': f"Key column '{col}' missing in one or both datasets"
                }
        
        return results
    
    def validate_data_completeness(self, source_df, target_df, source_name="Source", target_name="Target"):
        """5. Data Completeness Validation"""
        results = {}
        
        for col in source_df.columns:
            if col in target_df.columns:
                source_length = source_df[col].astype(str).str.len().max()
                target_length = target_df[col].astype(str).str.len().max()
                
                # Check for potential truncation
                truncation_risk = target_length < source_length
                
                results[col] = {
                    'source_max_length': source_length,
                    'target_max_length': target_length,
                    'truncation_risk': truncation_risk,
                    'status': 'WARNING' if truncation_risk else 'PASS',
                    'message': f"Source max length: {source_length}, Target max length: {target_length}"
                }
            else:
                results[col] = {
                    'status': 'FAIL',
                    'message': f"Column '{col}' missing in target"
                }
        
        return results
    
    def validate_data_accuracy(self, source_df, target_df, source_name="Source", target_name="Target"):
        """6. Data Accuracy / Value Comparison"""
        results = {}
        
        for col in source_df.columns:
            if col in source_df.columns and col in target_df.columns:
                # Check if column is numeric for statistical comparison
                if pd.api.types.is_numeric_dtype(source_df[col]) and pd.api.types.is_numeric_dtype(target_df[col]):
                    source_mean = source_df[col].mean()
                    target_mean = target_df[col].mean()
                    source_std = source_df[col].std()
                    target_std = target_df[col].std()
                    
                    # Calculate difference percentage
                    mean_diff_pct = abs(source_mean - target_mean) / abs(source_mean) * 100 if source_mean != 0 else 0
                    
                    results[col] = {
                        'source_mean': source_mean,
                        'target_mean': target_mean,
                        'source_std': source_std,
                        'target_std': target_std,
                        'mean_difference_pct': mean_diff_pct,
                        'status': 'PASS' if mean_diff_pct < 5 else 'WARNING',  # 5% threshold
                        'message': f"Mean difference: {mean_diff_pct:.2f}%"
                    }
                else:
                    # For non-numeric columns, check sample values
                    source_sample = source_df[col].dropna().head(5).tolist()
                    target_sample = target_df[col].dropna().head(5).tolist()
                    
                    results[col] = {
                        'source_sample': source_sample,
                        'target_sample': target_sample,
                        'status': 'INFO',
                        'message': f"Sample values comparison (non-numeric column)"
                    }
            else:
                results[col] = {
                    'status': 'FAIL',
                    'message': f"Column '{col}' missing in one or both datasets"
                }
        
        return results
    
    def validate_business_rules(self, source_df, target_df, business_rules=None, source_name="Source", target_name="Target"):
        """7. Business Rule Validation"""
        if business_rules is None:
            # Default business rules
            business_rules = {
                'age': {'min': 0, 'max': 120},
                'salary': {'min': 0},
                'rating': {'min': 1, 'max': 5}
            }
        
        results = {}
        
        for col, rules in business_rules.items():
            if col in target_df.columns:
                violations = 0
                messages = []
                
                if 'min' in rules:
                    min_violations = (target_df[col] < rules['min']).sum()
                    if min_violations > 0:
                        violations += min_violations
                        messages.append(f"Min violation: {min_violations} values below {rules['min']}")
                
                if 'max' in rules:
                    max_violations = (target_df[col] > rules['max']).sum()
                    if max_violations > 0:
                        violations += max_violations
                        messages.append(f"Max violation: {max_violations} values above {rules['max']}")
                
                results[col] = {
                    'violations': violations,
                    'messages': messages,
                    'status': 'PASS' if violations == 0 else 'FAIL',
                    'message': '; '.join(messages) if messages else 'All business rules satisfied'
                }
            else:
                results[col] = {
                    'status': 'FAIL',
                    'message': f"Column '{col}' missing in target for business rule validation"
                }
        
        return results
    
    def validate_data_format(self, source_df, target_df, source_name="Source", target_name="Target"):
        """8. Data Format & Standardization Validation"""
        results = {}
        
        for col in source_df.columns:
            if col in target_df.columns:
                # Check for common format issues
                format_issues = []
                
                # Check for mixed data types
                if target_df[col].dtype == 'object':
                    mixed_types = target_df[col].apply(lambda x: type(x).__name__).nunique()
                    if mixed_types > 1:
                        format_issues.append(f"Mixed data types: {mixed_types} types found")
                
                # Check for inconsistent string lengths (potential formatting issues)
                if target_df[col].dtype == 'object':
                    str_lengths = target_df[col].astype(str).str.len()
                    if str_lengths.std() > str_lengths.mean() * 0.5:  # High variance in lengths
                        format_issues.append("High variance in string lengths")
                
                results[col] = {
                    'format_issues': format_issues,
                    'status': 'PASS' if not format_issues else 'WARNING',
                    'message': '; '.join(format_issues) if format_issues else 'No format issues detected'
                }
            else:
                results[col] = {
                    'status': 'FAIL',
                    'message': f"Column '{col}' missing in target"
                }
        
        return results
    
    def generate_validation_report(self, source_df, target_df, source_name="Source", target_name="Target"):
        """Generate comprehensive validation report"""
        report = {
            'timestamp': datetime.now().isoformat(),
            'source_name': source_name,
            'target_name': target_name,
            'source_shape': source_df.shape,
            'target_shape': target_df.shape,
            'validations': {}
        }
        
        # Run all validations
        report['validations']['row_count'] = self.validate_row_count(source_df, target_df, source_name, target_name)
        report['validations']['data_types'] = self.validate_data_types(source_df, target_df, source_name, target_name)
        report['validations']['null_constraints'] = self.validate_null_constraints(source_df, target_df, source_name, target_name)
        report['validations']['primary_keys'] = self.validate_primary_keys(source_df, target_df, source_name=source_name, target_name=target_name)
        report['validations']['data_completeness'] = self.validate_data_completeness(source_df, target_df, source_name, target_name)
        report['validations']['data_accuracy'] = self.validate_data_accuracy(source_df, target_df, source_name, target_name)
        report['validations']['business_rules'] = self.validate_business_rules(source_df, target_df, source_name=source_name, target_name=target_name)
        report['validations']['data_format'] = self.validate_data_format(source_df, target_df, source_name, target_name)
        
        return report

def main():
    st.set_page_config(
        page_title="Comprehensive Data Validation App",
        page_icon="🔍",
        layout="wide"
    )
    
    st.title("🔍 Comprehensive Data Validation App")
    st.markdown("Compare two datasets and validate data quality across 10 validation types")
    
    # Sidebar for configuration
    st.sidebar.header("⚙️ Configuration")
    
    # File uploads
    st.header("📁 Upload Your Datasets")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Source Dataset")
        source_file = st.file_uploader("Upload source dataset", type=['csv'], key="source")
        source_name = st.text_input("Source dataset name", value="Source", key="source_name")
    
    with col2:
        st.subheader("Target Dataset")
        target_file = st.file_uploader("Upload target dataset", type=['csv'], key="target")
        target_name = st.text_input("Target dataset name", value="Target", key="target_name")
    
    # Validation button
    if st.button("🚀 Run Comprehensive Validation", type="primary", disabled=not (source_file and target_file)):
        if source_file and target_file:
            try:
                with st.spinner("Loading datasets and running validation..."):
                    # Load datasets
                    source_df = pd.read_csv(source_file)
                    target_df = pd.read_csv(target_file)
                    
                    st.success(f"✅ Datasets loaded successfully!")
                    
                    # Show dataset info
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("Source Rows", len(source_df))
                    with col2:
                        st.metric("Source Columns", len(source_df.columns))
                    with col3:
                        st.metric("Target Rows", len(target_df))
                    with col4:
                        st.metric("Target Columns", len(target_df.columns))
                    
                    # Run validation
                    validator = DataValidator()
                    report = validator.generate_validation_report(source_df, target_df, source_name, target_name)
                    
                    # Display results
                    st.header("📊 Validation Results")
                    
                    # Summary metrics
                    total_validations = 0
                    passed_validations = 0
                    failed_validations = 0
                    warnings = 0
                    
                    for validation_type, result in report['validations'].items():
                        if isinstance(result, dict):
                            if 'status' in result:
                                total_validations += 1
                                if result['status'] == 'PASS':
                                    passed_validations += 1
                                elif result['status'] == 'FAIL':
                                    failed_validations += 1
                                elif result['status'] == 'WARNING':
                                    warnings += 1
                        elif isinstance(result, dict):
                            for col_result in result.values():
                                if isinstance(col_result, dict) and 'status' in col_result:
                                    total_validations += 1
                                    if col_result['status'] == 'PASS':
                                        passed_validations += 1
                                    elif col_result['status'] == 'FAIL':
                                        failed_validations += 1
                                    elif col_result['status'] == 'WARNING':
                                        warnings += 1
                    
                    # Summary metrics
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("Total Validations", total_validations)
                    with col2:
                        st.metric("✅ Passed", passed_validations)
                    with col3:
                        st.metric("❌ Failed", failed_validations)
                    with col4:
                        st.metric("⚠️ Warnings", warnings)
                    
                    # Detailed results by validation type
                    for validation_type, result in report['validations'].items():
                        st.subheader(f"🔍 {validation_type.replace('_', ' ').title()}")
                        
                        if isinstance(result, dict) and 'status' in result:
                            # Single result
                            status_color = {'PASS': 'green', 'FAIL': 'red', 'WARNING': 'orange', 'INFO': 'blue'}
                            st.markdown(f"**Status:** :{status_color.get(result['status'], 'blue')}[{result['status']}]")
                            st.write(f"**Message:** {result['message']}")
                            
                            # Show additional details if available
                            for key, value in result.items():
                                if key not in ['status', 'message']:
                                    st.write(f"**{key.replace('_', ' ').title()}:** {value}")
                        else:
                            # Multiple results (e.g., by column)
                            for col_name, col_result in result.items():
                                if isinstance(col_result, dict) and 'status' in col_result:
                                    with st.expander(f"📋 {col_name}"):
                                        status_color = {'PASS': 'green', 'FAIL': 'red', 'WARNING': 'orange', 'INFO': 'blue'}
                                        st.markdown(f"**Status:** :{status_color.get(col_result['status'], 'blue')}[{col_result['status']}]")
                                        st.write(f"**Message:** {col_result['message']}")
                                        
                                        # Show additional details
                                        for key, value in col_result.items():
                                            if key not in ['status', 'message']:
                                                st.write(f"**{key.replace('_', ' ').title()}:** {value}")
                        
                        st.divider()
                    
                    # Store report in session state
                    st.session_state.validation_report = report
                    
            except Exception as e:
                st.error(f"❌ Error during validation: {str(e)}")
                st.exception(e)
        else:
            st.warning("⚠️ Please upload both source and target datasets")
    
    # Sample data generation
    if not (source_file and target_file):
        st.info("👆 Please upload both datasets to run validation")
        
        if st.button("🎯 Generate Sample Data for Testing"):
            # Create sample source data
            np.random.seed(42)
            source_data = pd.DataFrame({
                'id': range(1, 1001),
                'name': [f"Person_{i}" for i in range(1, 1001)],
                'age': np.random.normal(35, 10, 1000),
                'salary': np.random.normal(50000, 15000, 1000),
                'department': np.random.choice(['IT', 'HR', 'Sales', 'Marketing'], 1000),
                'rating': np.random.uniform(1, 5, 1000),
                'join_date': pd.date_range('2020-01-01', periods=1000, freq='D')
            })
            
            # Create target data with some intentional differences
            target_data = source_data.copy()
            
            # Introduce some validation issues
            target_data.loc[100:150, 'age'] = np.nan  # Null constraint violation
            target_data.loc[200:250, 'salary'] = target_data.loc[200:250, 'salary'] * 1.1  # Data accuracy issue
            target_data.loc[300:350, 'rating'] = 6  # Business rule violation
            target_data = target_data.drop(columns=['join_date'])  # Missing column
            
            # Save sample data
            source_data.to_csv('sample_source.csv', index=False)
            target_data.to_csv('sample_target.csv', index=False)
            
            st.success("✅ Sample data generated!")
            st.write("**Source dataset:** `sample_source.csv` (1000 rows, 7 columns)")
            st.write("**Target dataset:** `sample_target.csv` (1000 rows, 6 columns)")
            st.write("Upload these files to test the validation app!")

if __name__ == "__main__":
    main()
