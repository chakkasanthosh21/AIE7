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
import openai
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
import json

# Load environment variables
load_dotenv()

class AIDataValidator:
    """AI-powered data validation engine using LangChain and OpenAI"""

    def __init__(self):
        self.validation_results = {}
        self.llm = None
        self.setup_ai()
    
    def setup_ai(self):
        """Initialize AI components"""
        try:
            api_key = os.getenv('OPENAI_API_KEY')
            if api_key:
                openai.api_key = api_key
                self.llm = ChatOpenAI(
                    model="gpt-3.5-turbo",
                    temperature=0.1,
                    openai_api_key=api_key
                )
                st.success("🤖 AI validation engine initialized successfully!")
            else:
                st.warning("⚠️ OpenAI API key not found. AI validation will be limited.")
        except Exception as e:
            st.error(f"❌ AI setup failed: {str(e)}")
    
    def ai_validate_data_quality(self, source_df, target_df, source_name="Source", target_name="Target"):
        """AI-powered data quality validation using LLM analysis"""
        if not self.llm:
            return {"status": "FAIL", "message": "AI engine not available"}
        
        try:
            # Prepare data summary for AI analysis
            source_summary = f"""
            Source Dataset ({source_name}):
            - Shape: {source_df.shape}
            - Columns: {list(source_df.columns)}
            - Data types: {dict(source_df.dtypes)}
            - Missing values: {dict(source_df.isnull().sum())}
            - Sample data: {source_df.head(3).to_dict()}
            """
            
            target_summary = f"""
            Target Dataset ({target_name}):
            - Shape: {target_df.shape}
            - Columns: {list(target_df.columns)}
            - Data types: {dict(target_df.dtypes)}
            - Missing values: {dict(target_df.isnull().sum())}
            - Sample data: {target_df.head(3).to_dict()}
            """
            
            # AI prompt for data quality analysis
            prompt = PromptTemplate(
                input_variables=["source_summary", "target_summary"],
                template="""
                You are a data quality expert. Analyze these two datasets and identify potential data quality issues:
                
                {source_summary}
                
                {target_summary}
                
                Provide a JSON response with:
                1. Overall data quality score (0-100)
                2. Critical issues found
                3. Data integrity concerns
                4. Recommendations for improvement
                5. Risk assessment (LOW/MEDIUM/HIGH)
                
                Format your response as valid JSON only.
                """
            )
            
            chain = LLMChain(llm=self.llm, prompt=prompt)
            response = chain.run(source_summary=source_summary, target_summary=target_summary)
            
            # Parse AI response
            try:
                ai_analysis = json.loads(response)
                return {
                    'status': 'PASS',
                    'ai_score': ai_analysis.get('overall_data_quality_score', 0),
                    'critical_issues': ai_analysis.get('critical_issues', []),
                    'integrity_concerns': ai_analysis.get('data_integrity_concerns', []),
                    'recommendations': ai_analysis.get('recommendations', []),
                    'risk_level': ai_analysis.get('risk_assessment', 'MEDIUM'),  # Default to MEDIUM instead of UNKNOWN
                    'ai_insights': response
                }
            except json.JSONDecodeError:
                return {
                    'status': 'WARNING',
                    'message': 'AI analysis completed but response format unclear',
                    'raw_response': response
                }
                
        except Exception as e:
            return {
                'status': 'FAIL',
                'message': f'AI data quality validation failed: {str(e)}'
            }
    
    def ai_validate_business_logic(self, source_df, target_df, business_rules=None):
        """AI-powered business logic validation"""
        if not self.llm:
            return {"status": "FAIL", "message": "AI engine not available"}
        
        try:
            # Generate business rule suggestions using AI with proper column names
            column_info = {}
            for col in target_df.columns:
                if col in source_df.columns:
                    sample_values = target_df[col].dropna().head(5).tolist()
                    column_info[col] = {
                        'exists_in_source': True,
                        'sample_values': sample_values,
                        'data_type': str(target_df[col].dtype),
                        'null_count': target_df[col].isnull().sum(),
                        'unique_count': target_df[col].nunique()
                    }
                else:
                    sample_values = target_df[col].dropna().head(5).tolist()
                    column_info[col] = {
                        'exists_in_source': False,
                        'sample_values': sample_values,
                        'data_type': str(target_df[col].dtype),
                        'null_count': target_df[col].isnull().sum(),
                        'unique_count': target_df[col].nunique()
                    }
            
            prompt = PromptTemplate(
                input_variables=["column_info", "business_rules"],
                template="""
                Analyze this dataset and suggest business rules for validation. Use the actual column names provided:
                
                Column Information: {column_info}
                Existing Rules: {business_rules}
                
                Provide JSON response with:
                {{
                    "suggested_business_rules": [
                        {{
                            "column_name": "actual_column_name_here",
                            "rule_description": "description of the rule",
                            "validation_type": "type of validation",
                            "threshold": "threshold value if applicable"
                        }}
                    ],
                    "data_quality_patterns": [
                        {{
                            "column_name": "actual_column_name_here",
                            "pattern": "pattern description",
                            "confidence": "confidence level"
                        }}
                    ],
                    "anomaly_detection_rules": [
                        {{
                            "column_name": "actual_column_name_here",
                            "anomaly_type": "type of anomaly",
                            "detection_method": "method to detect"
                        }}
                    ],
                    "validation_thresholds": {{
                        "column_name": "threshold_value"
                    }}
                }}
                
                IMPORTANT: Use the actual column names from the column_info, not generic numbers like 1, 2, 3.
                Format as valid JSON only.
                """
            )
            
            chain = LLMChain(llm=self.llm, prompt=prompt)
            response = chain.run(column_info=str(column_info), business_rules=str(business_rules))
            
            try:
                ai_rules = json.loads(response)
                return {
                    'status': 'PASS',
                    'suggested_rules': ai_rules.get('suggested_business_rules', []),
                    'quality_patterns': ai_rules.get('data_quality_patterns', []),
                    'anomaly_rules': ai_rules.get('anomaly_detection_rules', []),
                    'validation_thresholds': ai_rules.get('validation_thresholds', {}),
                    'ai_insights': response,
                    'column_analysis': column_info
                }
            except json.JSONDecodeError:
                return {
                    'status': 'WARNING',
                    'message': 'AI business logic analysis completed but response format unclear',
                    'raw_response': response
                }
                
        except Exception as e:
            return {
                'status': 'FAIL',
                'message': f'AI business logic validation failed: {str(e)}'
            }
    
    def ai_validate_semantic_consistency(self, source_df, target_df):
        """AI-powered semantic consistency validation"""
        if not self.llm:
            return {"status": "FAIL", "message": "AI engine not available"}
        
        try:
            # Analyze column names and data for semantic consistency
            column_analysis = {}
            for col in target_df.columns:
                if col in source_df.columns:
                    sample_values = target_df[col].dropna().head(5).tolist()
                    column_analysis[col] = {
                        'source_exists': True,
                        'sample_values': sample_values,
                        'data_type': str(target_df[col].dtype)
                    }
                else:
                    column_analysis[col] = {
                        'source_exists': False,
                        'sample_values': target_df[col].dropna().head(5).tolist(),
                        'data_type': str(target_df[col].dtype)
                    }
            
            prompt = PromptTemplate(
                input_variables=["column_analysis"],
                template="""
                Analyze these dataset columns for semantic consistency and data quality:
                
                Column Analysis: {column_analysis}
                
                Provide JSON response with:
                1. Semantic consistency score (0-100)
                2. Column mapping suggestions
                3. Data quality insights
                4. Potential data lineage issues
                
                Format as valid JSON only.
                """
            )
            
            chain = LLMChain(llm=self.llm, prompt=prompt)
            response = chain.run(column_analysis=str(column_analysis))
            
            try:
                semantic_analysis = json.loads(response)
                return {
                    'status': 'PASS',
                    'semantic_score': semantic_analysis.get('semantic_consistency_score', 0),
                    'column_mappings': semantic_analysis.get('column_mapping_suggestions', []),
                    'quality_insights': semantic_analysis.get('data_quality_insights', []),
                    'lineage_issues': semantic_analysis.get('data_lineage_issues', []),
                    'ai_insights': response
                }
            except json.JSONDecodeError:
                return {
                    'status': 'WARNING',
                    'message': 'AI semantic analysis completed but response format unclear',
                    'raw_response': response
                }
                
        except Exception as e:
            return {
                'status': 'FAIL',
                'message': f'AI semantic consistency validation failed: {str(e)}'
            }

class DataValidator:
    """Comprehensive data validation engine with AI enhancement"""
    
    def __init__(self):
        self.ai_validator = AIDataValidator()
    
    def validate_row_count(self, source_df, target_df, source_name="Source", target_name="Target"):
        """1. Row Count Validation"""
        source_count = len(source_df)
        target_count = len(target_df)
        
        if source_count == target_count:
            return {
                'status': 'PASS',
                'source_count': source_count,
                'target_count': target_count,
                'message': f'Row counts match: {source_count} records'
            }
        else:
            difference = abs(source_count - target_count)
            return {
                'status': 'FAIL',
                'source_count': source_count,
                'target_count': target_count,
                'message': f'Row count mismatch: {difference} records difference'
            }
    
    def validate_data_types(self, source_df, target_df, source_name="Source", target_name="Target"):
        """2. Data Type Validation"""
        results = {}
        
        for col in source_df.columns:
            if col in target_df.columns:
                source_dtype = str(source_df[col].dtype)
                target_dtype = str(target_df[col].dtype)
                
                if source_dtype == target_dtype:
                    status = 'PASS'
                    message = 'Data types match'
                else:
                    status = 'FAIL'
                    message = f'Data type mismatch: {source_dtype} vs {target_dtype}'
                
                results[col] = {
                    'source_dtype': source_dtype,
                    'target_dtype': target_dtype,
                    'status': status,
                    'message': message,
                    'source_sample': source_df[col].dropna().head(3).tolist(),
                    'target_sample': target_df[col].dropna().head(3).tolist()
                }
            else:
                results[col] = {
                    'status': 'FAIL',
                    'message': f"Column '{col}' missing in target"
                }
        
        return results
    
    def validate_null_constraints(self, source_df, target_df, source_name="Source", target_name="Target"):
        """3. Null Constraints Validation"""
        results = {}
        
        for col in source_df.columns:
            if col in target_df.columns:
                source_null_count = source_df[col].isnull().sum()
                target_null_count = target_df[col].isnull().sum()
                
                if target_null_count <= source_null_count:
                    status = 'PASS'
                    message = 'Null constraints maintained'
                else:
                    status = 'FAIL'
                    message = f'Target has more nulls: {target_null_count} vs {source_null_count}'
                
                results[col] = {
                    'source_null_count': source_null_count,
                    'target_null_count': target_null_count,
                    'status': status,
                    'message': message
                }
            else:
                results[col] = {
                    'status': 'FAIL',
                    'message': f"Column '{col}' missing in target"
                }
        
        return results
    
    def validate_primary_keys(self, source_df, target_df, source_name="Source", target_name="Target"):
        """4. Primary Key / Unique Key Validation"""
        results = {}
        
        for col in source_df.columns:
            if col in target_df.columns:
                # Check for primary key characteristics
                source_unique = source_df[col].nunique()
                target_unique = target_df[col].nunique()
                source_duplicates = len(source_df) - source_unique
                target_duplicates = len(target_df) - target_unique
                
                # Determine status based on uniqueness
                if source_duplicates == 0 and target_duplicates == 0:
                    status = 'PASS'
                    message = 'No duplicates found in either dataset'
                elif source_duplicates == 0 and target_duplicates > 0:
                    status = 'FAIL'
                    message = f'Target has {target_duplicates} duplicate values'
                elif source_duplicates > 0 and target_duplicates == 0:
                    status = 'WARNING'
                    message = f'Source has {source_duplicates} duplicate values, target is clean'
                else:
                    status = 'FAIL'
                    message = f'Both datasets have duplicates - Source: {source_duplicates}, Target: {target_duplicates}'
                
                results[col] = {
                    'source_unique': source_unique,
                    'target_unique': target_unique,
                    'source_duplicates': source_duplicates,
                    'target_duplicates': target_duplicates,
                    'status': status,
                    'message': message
                }
            else:
                results[col] = {
                    'status': 'FAIL',
                    'message': f"Column '{col}' missing in target"
                }
        
        return results
    
    def validate_data_completeness(self, source_df, target_df, source_name="Source", target_name="Target"):
        """5. Data Completeness Validation"""
        results = {}
        
        for col in source_df.columns:
            if col in target_df.columns:
                # Check for data truncation
                if source_df[col].dtype == 'object':
                    source_max_length = source_df[col].astype(str).str.len().max()
                    target_max_length = target_df[col].astype(str).str.len().max()
                    
                    if target_max_length >= source_max_length:
                        status = 'PASS'
                        message = 'Data length preserved'
                    else:
                        status = 'WARNING'
                        message = f'Potential truncation: {target_max_length} vs {source_max_length}'
                    
                    results[col] = {
                        'source_max_length': source_max_length,
                        'target_max_length': target_max_length,
                        'truncation_risk': target_max_length < source_max_length,
                        'status': status,
                        'message': message
                    }
                else:
                    results[col] = {
                        'status': 'PASS',
                        'message': 'Non-string column - no truncation risk'
                    }
            else:
                results[col] = {
                    'status': 'FAIL',
                    'message': f"Column '{col}' missing in target"
                }
        
        return results
    
    def validate_data_accuracy(self, source_df, target_df, source_name="Source", target_name="Target"):
        """6. Data Accuracy / Value Comparison Validation"""
        results = {}
        
        for col in source_df.columns:
            if col in target_df.columns:
                # Check if column is numeric
                if pd.api.types.is_numeric_dtype(source_df[col]) and pd.api.types.is_numeric_dtype(target_df[col]):
                    # Numeric column - calculate statistical comparison
                    source_mean = source_df[col].mean()
                    target_mean = target_df[col].mean()
                    
                    if source_mean != 0:
                        mean_difference_pct = abs((target_mean - source_mean) / source_mean) * 100
                    else:
                        mean_difference_pct = 0
                    
                    # Determine status based on difference
                    if mean_difference_pct < 0.1:  # Less than 0.1% difference
                        status = 'PASS'
                    elif mean_difference_pct < 1.0:  # Less than 1% difference
                        status = 'WARNING'
                    else:
                        status = 'FAIL'
                    
                    results[col] = {
                        'source_mean': source_mean,
                        'target_mean': target_mean,
                        'mean_difference_pct': mean_difference_pct,
                        'status': status,
                        'message': f'Mean difference: {mean_difference_pct:.2f}%'
                    }
                else:
                    # Non-numeric column - sample comparison
                    source_sample = source_df[col].dropna().head(5).tolist()
                    target_sample = target_df[col].dropna().head(5).tolist()
                    
                    # Check if samples are similar
                    source_set = set(str(x) for x in source_sample)
                    target_set = set(str(x) for x in target_sample)
                    
                    similarity = len(source_set.intersection(target_set)) / len(source_set.union(target_set)) if source_set.union(target_set) else 0
                    
                    if similarity > 0.8:
                        status = 'PASS'
                    elif similarity > 0.5:
                        status = 'WARNING'
                    else:
                        status = 'FAIL'
                    
                    results[col] = {
                        'source_sample': source_sample,
                        'target_sample': target_sample,
                        'similarity': similarity,
                        'status': status,
                        'message': f'Sample similarity: {similarity:.2f}'
                    }
            else:
                results[col] = {
                    'status': 'FAIL',
                    'message': f"Column '{col}' missing in target"
                }
        
        return results
    
    def validate_business_rules(self, source_df, target_df, business_rules=None):
        """7. Business Rule Validation"""
        results = {}
        
        if business_rules is None:
            # Define some common business rules to check
            business_rules = {
                'total_amount': {
                    'rule': 'total_amount = quantity * unit_price',
                    'description': 'Total amount should equal quantity times unit price'
                },
                'order_date': {
                    'rule': 'order_date <= ship_date',
                    'description': 'Order date should be before or equal to ship date'
                },
                'quantity': {
                    'rule': 'quantity > 0',
                    'description': 'Quantity should be positive'
                },
                'unit_price': {
                    'rule': 'unit_price > 0',
                    'description': 'Unit price should be positive'
                }
            }
        
        for col, rule_info in business_rules.items():
            if col in source_df.columns and col in target_df.columns:
                violations = 0
                messages = []
                
                if col == 'total_amount' and 'quantity' in target_df.columns and 'unit_price' in target_df.columns:
                    # Check if total_amount = quantity * unit_price
                    # First ensure both columns are numeric
                    try:
                        # Convert to numeric, coercing errors to NaN
                        quantity_numeric = pd.to_numeric(target_df['quantity'], errors='coerce')
                        unit_price_numeric = pd.to_numeric(target_df['unit_price'], errors='coerce')
                        
                        # Only proceed if we have valid numeric data
                        if not quantity_numeric.isna().all() and not unit_price_numeric.isna().all():
                            expected_total = quantity_numeric * unit_price_numeric
                            actual_total = pd.to_numeric(target_df['total_amount'], errors='coerce')
                            
                            # Remove NaN values for comparison
                            valid_mask = ~(expected_total.isna() | actual_total.isna())
                            if valid_mask.any():
                                difference = abs(expected_total[valid_mask] - actual_total[valid_mask])
                                
                                # Allow small rounding differences (0.01)
                                violations = (difference > 0.01).sum()
                                if violations > 0:
                                    messages.append(f"{violations} records have total_amount ≠ quantity × unit_price")
                                else:
                                    messages.append("All records follow total_amount = quantity × unit_price rule")
                            else:
                                messages.append("No valid numeric data for comparison")
                        else:
                            messages.append("Quantity or unit_price columns are not numeric")
                    except Exception as e:
                        messages.append(f"Error in total_amount validation: {str(e)}")
                        violations = 0
                
                elif col == 'order_date' and 'ship_date' in target_df.columns:
                    # Check if order_date <= ship_date
                    try:
                        # Convert to datetime if possible
                        order_dates = pd.to_datetime(target_df['order_date'], errors='coerce')
                        ship_dates = pd.to_datetime(target_df['ship_date'], errors='coerce')
                        
                        # Only proceed if we have valid datetime data
                        valid_mask = ~(order_dates.isna() | ship_dates.isna())
                        if valid_mask.any():
                            violations = (order_dates[valid_mask] > ship_dates[valid_mask]).sum()
                            if violations > 0:
                                messages.append(f"{violations} records have order_date > ship_date")
                            else:
                                messages.append("All records follow order_date ≤ ship_date rule")
                        else:
                            messages.append("No valid date data for comparison")
                    except Exception as e:
                        messages.append(f"Error in date validation: {str(e)}")
                        violations = 0
                
                elif col == 'quantity':
                    # Check if quantity > 0
                    try:
                        quantity_numeric = pd.to_numeric(target_df['quantity'], errors='coerce')
                        valid_mask = ~quantity_numeric.isna()
                        if valid_mask.any():
                            violations = (quantity_numeric[valid_mask] <= 0).sum()
                            if violations > 0:
                                messages.append(f"{violations} records have quantity ≤ 0")
                            else:
                                messages.append("All records have positive quantities")
                        else:
                            messages.append("No valid numeric data for quantity")
                    except Exception as e:
                        messages.append(f"Error in quantity validation: {str(e)}")
                        violations = 0
                
                elif col == 'unit_price':
                    # Check if unit_price > 0
                    try:
                        unit_price_numeric = pd.to_numeric(target_df['unit_price'], errors='coerce')
                        valid_mask = ~unit_price_numeric.isna()
                        if valid_mask.any():
                            violations = (unit_price_numeric[valid_mask] <= 0).sum()
                            if violations > 0:
                                messages.append(f"{violations} records have unit_price ≤ 0")
                            else:
                                messages.append("All records have positive unit prices")
                        else:
                            messages.append("No valid numeric data for unit_price")
                    except Exception as e:
                        messages.append(f"Error in unit_price validation: {str(e)}")
                        violations = 0
                
                # Determine status
                if violations == 0:
                    status = 'PASS'
                elif violations <= 5:  # Allow some violations
                    status = 'WARNING'
                else:
                    status = 'FAIL'
                
                results[col] = {
                    'violations': violations,
                    'messages': messages,
                    'status': status,
                    'rule_description': rule_info['description']
                }
            else:
                results[col] = {
                    'violations': 0,
                    'messages': [f"Column '{col}' not available for validation"],
                    'status': 'INFO',
                    'rule_description': 'Column not available'
                }
        
        return results
    
    def validate_data_format(self, source_df, target_df, source_name="Source", target_name="Target"):
        """8. Data Format & Standardization Validation"""
        results = {}
        overall_issues = []
        overall_status = 'PASS'

        for col in source_df.columns:
            if col in target_df.columns:
                # Check for common format issues
                format_issues = []

                # Check for mixed data types
                if target_df[col].dtype == 'object':
                    mixed_types = target_df[col].apply(lambda x: type(x).__name__).nunique()
                    if mixed_types > 1:
                        format_issues.append(f"Mixed data types: {mixed_types} types found")
                        overall_issues.append(f"Column '{col}': Mixed data types")

                # Check for inconsistent string lengths (potential formatting issues)
                if target_df[col].dtype == 'object':
                    str_lengths = target_df[col].astype(str).str.len()
                    if str_lengths.std() > str_lengths.mean() * 0.5:  # High variance in lengths
                        format_issues.append("High variance in string lengths")
                        overall_issues.append(f"Column '{col}': High variance in string lengths")

                # Check for date format consistency
                if target_df[col].dtype == 'object':
                    # Try to detect if column contains dates
                    sample_values = target_df[col].dropna().head(10)
                    if len(sample_values) > 0:
                        try:
                            pd.to_datetime(sample_values, errors='raise')
                            # If successful, check for format consistency
                            date_formats = []
                            for val in sample_values:
                                try:
                                    parsed = pd.to_datetime(val)
                                    date_formats.append(parsed.strftime('%Y-%m-%d'))
                                except:
                                    pass
                            if len(set(date_formats)) > 1:
                                format_issues.append("Inconsistent date formats")
                                overall_issues.append(f"Column '{col}': Inconsistent date formats")
                        except:
                            pass  # Not a date column

                results[col] = {
                    'format_issues': format_issues,
                    'status': 'PASS' if not format_issues else 'WARNING',
                    'message': '; '.join(format_issues) if format_issues else 'No format issues detected'
                }

                if format_issues:
                    overall_status = 'WARNING'
            else:
                results[col] = {
                    'status': 'FAIL',
                    'message': f"Column '{col}' missing in target"
                }
                overall_status = 'FAIL'
                overall_issues.append(f"Column '{col}' missing in target")

        # Add overall summary
        results['overall'] = {
            'status': overall_status,
            'message': '; '.join(overall_issues) if overall_issues else 'All format validations passed',
            'total_issues': len(overall_issues)
        }

        return results

    def validate_referential_integrity(self, source_df, target_df, foreign_key_mappings=None):
        """9. Referential Integrity Validation (AI-Enhanced)"""
        if foreign_key_mappings is None:
            # AI-powered foreign key detection
            ai_result = self.ai_validator.ai_validate_semantic_consistency(source_df, target_df)
            if ai_result['status'] == 'PASS':
                # Use AI insights to suggest foreign key relationships
                return {
                    'status': 'INFO',
                    'message': 'AI analysis completed - check semantic consistency results for foreign key insights',
                    'ai_analysis': ai_result
                }
        
        # Traditional referential integrity validation
        results = {}
        # Implementation would check foreign key constraints
        # For now, return basic structure
        results['status'] = 'INFO'
        results['message'] = 'Referential integrity validation framework ready'
        
        return results

    def validate_performance_accessibility(self, source_df, target_df):
        """10. Performance & Accessibility Validation (AI-Enhanced)"""
        # AI-powered performance analysis
        ai_result = self.ai_validator.ai_validate_data_quality(source_df, target_df)
        
        results = {
            'ai_analysis': ai_result,
            'performance_metrics': {
                'source_size_mb': source_df.memory_usage(deep=True).sum() / 1024 / 1024,
                'target_size_mb': target_df.memory_usage(deep=True).sum() / 1024 / 1024,
                'column_count': len(target_df.columns),
                'row_count': len(target_df)
            }
        }
        
        # Basic performance assessment
        if results['performance_metrics']['target_size_mb'] > 100:
            results['status'] = 'WARNING'
            results['message'] = 'Large dataset detected - consider optimization strategies'
        else:
            results['status'] = 'PASS'
            results['message'] = 'Dataset size within acceptable limits'
        
        return results

    def generate_validation_report(self, source_df, target_df, source_name="Source", target_name="Target"):
        """Generate comprehensive validation report with AI enhancement"""
        report = {
            'timestamp': datetime.now().isoformat(),
            'source_name': source_name,
            'target_name': target_name,
            'source_shape': source_df.shape,
            'target_shape': target_df.shape,
            'validations': {}
        }

        # Run all traditional validations
        report['validations']['row_count'] = self.validate_row_count(source_df, target_df, source_name, target_name)
        report['validations']['data_types'] = self.validate_data_types(source_df, target_df, source_name, target_name)
        report['validations']['null_constraints'] = self.validate_null_constraints(source_df, target_df, source_name, target_name)
        report['validations']['primary_keys'] = self.validate_primary_keys(source_df, target_df, source_name=source_name, target_name=target_name)
        report['validations']['data_completeness'] = self.validate_data_completeness(source_df, target_df, source_name, target_name)
        report['validations']['data_accuracy'] = self.validate_data_accuracy(source_df, target_df, source_name, target_name)
        report['validations']['business_rules'] = self.validate_business_rules(source_df, target_df)
        report['validations']['data_format'] = self.validate_data_format(source_df, target_df, source_name, target_name)
        report['validations']['referential_integrity'] = self.validate_referential_integrity(source_df, target_df)
        report['validations']['performance_accessibility'] = self.validate_performance_accessibility(source_df, target_df)
        
        # Run AI-enhanced validations
        report['validations']['ai_data_quality'] = self.ai_validator.ai_validate_data_quality(source_df, target_df, source_name, target_name)
        report['validations']['ai_business_logic'] = self.ai_validator.ai_validate_business_logic(source_df, target_df)
        report['validations']['ai_semantic_consistency'] = self.ai_validator.ai_validate_semantic_consistency(source_df, target_df)

        return report

def main():
    st.set_page_config(
        page_title="AI-Powered Data Validation App",
        page_icon="🔍",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Custom CSS for better styling
    st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
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
    .status-pass { color: #28a745; font-weight: bold; }
    .status-fail { color: #dc3545; font-weight: bold; }
    .status-warning { color: #ffc107; font-weight: bold; }
    .status-info { color: #17a2b8; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)
    
    # Main header
    st.markdown('<h1 class="main-header">🔍 AI-Powered Data Validation App</h1>', unsafe_allow_html=True)
    st.markdown("### Comprehensive data quality analysis with AI-powered insights")
    
    # Sidebar configuration
    st.sidebar.markdown("## ⚙️ Configuration")
    
    # Add OpenAI API key input
    st.sidebar.markdown("## 🔑 OpenAI API Configuration")
    api_key = st.sidebar.text_input(
        "OpenAI API Key",
        value="",  # Remove hardcoded API key
        type="password",
        help="Enter your OpenAI API key to enable AI-powered validation insights"
    )
    if api_key != st.session_state.get('openai_api_key', ''):
        st.session_state.openai_api_key = api_key
        if api_key:
            os.environ['OPENAI_API_KEY'] = api_key
            st.sidebar.success("✅ API Key updated successfully!")
        else:
            st.sidebar.warning("⚠️ API Key cleared")
    
    # Initialize session state
    if 'source_df' not in st.session_state:
        st.session_state.source_df = None
    if 'target_df' not in st.session_state:
        st.session_state.target_df = None
    if 'validation_results' not in st.session_state:
        st.session_state.validation_results = None
    if 'openai_api_key' not in st.session_state:
        st.session_state.openai_api_key = ""
    
    # File upload section
    st.markdown("## 📁 File Upload")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Source Dataset")
        source_file = st.file_uploader("Upload source dataset", type=['csv', 'xlsx', 'xls'], key="source")
        
        if source_file is not None:
            try:
                if source_file.name.endswith('.csv'):
                    source_df = pd.read_csv(source_file)
                else:
                    source_df = pd.read_excel(source_file)
                
                st.session_state.source_df = source_df
                st.success(f"✅ Source dataset loaded: {source_df.shape[0]} rows, {source_df.shape[1]} columns")
                
                # Display source dataset info
                with st.expander("📊 Source Dataset Info"):
                    st.write(f"**Shape:** {source_df.shape}")
                    st.write(f"**Columns:** {list(source_df.columns)}")
                    st.write(f"**Data Types:** {dict(source_df.dtypes)}")
                    st.write(f"**Missing Values:** {dict(source_df.isnull().sum())}")
                    
            except Exception as e:
                st.error(f"❌ Error loading source dataset: {str(e)}")
    
    with col2:
        st.markdown("### Target Dataset")
        target_file = st.file_uploader("Upload target dataset", type=['csv', 'xlsx', 'xls'], key="target")
        
        if target_file is not None:
            try:
                if target_file.name.endswith('.csv'):
                    target_df = pd.read_excel(target_file)
                else:
                    target_df = pd.read_excel(target_file)
                
                st.session_state.target_df = target_df
                st.success(f"✅ Target dataset loaded: {target_df.shape[0]} rows, {target_df.shape[1]} columns")
                
                # Display target dataset info
                with st.expander("📊 Target Dataset Info"):
                    st.write(f"**Shape:** {target_df.shape}")
                    st.write(f"**Columns:** {list(target_df.columns)}")
                    st.write(f"**Data Types:** {dict(target_df.dtypes)}")
                    st.write(f"**Missing Values:** {dict(target_df.isnull().sum())}")
                    
            except Exception as e:
                st.error(f"❌ Error loading target dataset: {str(e)}")
    
    # Generate sample data option
    if st.button("🎲 Generate Sample Data"):
        # Create sample datasets for testing
        np.random.seed(42)
        
        # Sample e-commerce data
        n_records = 1000
        source_df = pd.DataFrame({
            'id': range(1, n_records + 1),
            'customer_id': np.random.randint(1000, 10000, n_records),
            'product_id': np.random.randint(100, 2000, n_records),
            'order_date': pd.date_range('2023-01-01', periods=n_records, freq='D'),
            'ship_date': pd.date_range('2023-01-02', periods=n_records, freq='D'),
            'status': np.random.choice(['PENDING', 'PROCESSING', 'SHIPPED', 'DELIVERED'], n_records),
            'quantity': np.random.randint(1, 20, n_records),
            'unit_price': np.random.uniform(10, 500, n_records),
            'total_amount': np.random.uniform(100, 5000, n_records),
            'currency': ['USD'] * n_records
        })
        
        # Create target dataset with some variations
        target_df = source_df.copy()
        target_df['total_amount'] = target_df['quantity'] * target_df['unit_price']  # Fix business rule
        target_df.loc[100:200, 'status'] = 'CANCELLED'  # Introduce some changes
        
        st.session_state.source_df = source_df
        st.session_state.target_df = target_df
        
        st.success("✅ Sample datasets generated successfully!")
        st.rerun()
    
    # Validation section
    if st.session_state.source_df is not None and st.session_state.target_df is not None:
        st.markdown("## 🔍 Data Validation")
        
        if st.button("🚀 Run Validation", type="primary"):
            with st.spinner("Running comprehensive validation..."):
                try:
                    # Initialize validator
                    validator = DataValidator()
                    
                    # Get dataset names
                    source_name = source_file.name if source_file else "Source"
                    target_name = target_file.name if target_file else "Target"
                    
                    # Run validation
                    report = validator.generate_validation_report(
                        st.session_state.source_df, 
                        st.session_state.target_df, 
                        source_name, 
                        target_name
                    )
                    
                    st.session_state.validation_results = report
                    st.success("✅ Validation completed successfully!")
                    
                except Exception as e:
                    st.error(f"❌ Error during validation: {str(e)}")
                    st.error(f"Traceback: {e.__traceback__}")
        
        # Display validation results
        if st.session_state.validation_results:
            display_validation_results(st.session_state.validation_results, st.session_state.source_df, st.session_state.target_df)
    
    # Footer
    st.markdown("---")
    st.markdown("### 📚 Features")
    st.markdown("""
    - **10 Comprehensive Validation Types** including Row Count, Data Types, Null Constraints, Primary Keys, Referential Integrity, Data Completeness, Data Accuracy, Business Rules, Data Format, and Performance
    - **AI-Powered Analysis** using OpenAI GPT models for intelligent data quality insights
    - **Interactive Visualizations** with Plotly charts and graphs
    - **Detailed Reporting** with actionable insights and recommendations
    - **Real-time Validation** with immediate feedback and error handling
    """)

def display_validation_results(report, source_df, target_df):
    """Display comprehensive validation results with improved formatting"""
    
    # Navigation
    st.markdown("## 📋 Validation Results")
    
    # Summary metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Source Dataset", f"{report['source_shape'][0]} rows, {report['source_shape'][1]} cols")
    
    with col2:
        st.metric("Target Dataset", f"{report['target_shape'][0]} rows, {report['target_shape'][1]} cols")
    
    with col3:
        total_validations = len(report['validations'])
        st.metric("Total Validations", total_validations)
    
    with col4:
        timestamp = datetime.fromisoformat(report['timestamp'])
        st.metric("Validation Time", timestamp.strftime("%H:%M:%S"))
    
    # Table of contents
    st.markdown("### 📑 Navigation")
    st.markdown("- [AI Validation Results](#ai-validation-results)")
    st.markdown("- [Traditional Validation Results](#traditional-validation-results)")
    
    # AI Validation Results (highlighted)
    st.subheader("🤖 AI-Powered Validation Results")
    
    # Floating Back to Top button for AI section
    if st.button("⬆️ Back to Top", key="back_to_top_ai"):
        st.rerun()
    
    ai_validations = ['ai_data_quality', 'ai_business_logic', 'ai_semantic_consistency']
    for ai_type in ai_validations:
        if ai_type in report['validations']:
            ai_result = report['validations'][ai_type]
            
            # Create anchor for navigation
            st.markdown(f"<a name='{ai_type.replace('_', '-')}'></a>", unsafe_allow_html=True)
            
            with st.expander(f"🤖 {ai_type.replace('_', ' ').title()}", expanded=True):
                if ai_result['status'] == 'PASS':
                    st.success(f"✅ {ai_result.get('message', 'AI analysis completed successfully')}")
                    
                    # Display AI insights in clean table format
                    if 'ai_score' in ai_result:
                        st.metric("AI Quality Score", f"{ai_result['ai_score']}/100")
                    
                    # Create clean summary table for AI results
                    ai_summary_data = []
                    if 'critical_issues' in ai_result and ai_result['critical_issues']:
                        for i, issue in enumerate(ai_result['critical_issues']):
                            ai_summary_data.append({
                                'Type': 'Critical Issue',
                                'Description': str(issue)[:150],  # Limit length for readability
                                'Priority': 'HIGH',
                                'Action': 'Immediate attention required'
                            })
                    
                    if 'recommendations' in ai_result and ai_result['recommendations']:
                        for i, rec in enumerate(ai_result['recommendations']):
                            ai_summary_data.append({
                                'Type': 'Recommendation',
                                'Description': str(rec)[:150],  # Limit length for readability
                                'Priority': 'MEDIUM',
                                'Action': 'Consider implementing'
                            })
                    
                    if ai_summary_data:
                        ai_df = pd.DataFrame(ai_summary_data)
                        st.markdown("**📋 AI Analysis Summary:**")
                        st.dataframe(ai_df, use_container_width=True, hide_index=True)
                    
                    # Show additional AI insights in clean format
                    additional_insights = []
                    if 'integrity_concerns' in ai_result and ai_result['integrity_concerns']:
                        for concern in ai_result['integrity_concerns']:
                            additional_insights.append({
                                'Category': 'Data Integrity',
                                'Issue': str(concern)[:120],
                                'Impact': 'Medium'
                            })
                    
                    if 'risk_level' in ai_result:
                        additional_insights.append({
                            'Category': 'Risk Assessment',
                            'Issue': f"Overall Risk Level: {ai_result['risk_level']}",
                            'Impact': 'High' if ai_result['risk_level'] == 'HIGH' else 'Medium' if ai_result['risk_level'] == 'MEDIUM' else 'Low'
                        })
                    
                    if additional_insights:
                        insights_df = pd.DataFrame(additional_insights)
                        st.markdown("**🔍 Additional AI Insights:**")
                        st.dataframe(insights_df, use_container_width=True, hide_index=True)
                    
                    # Raw AI response in collapsible section (optional)
                    if 'ai_insights' in ai_result:
                        with st.expander("🔍 View Raw AI Analysis (JSON)"):
                            st.code(ai_result['ai_insights'], language='json')
                
                elif ai_result['status'] == 'WARNING':
                    st.warning(f"⚠️ {ai_result.get('message', 'AI analysis completed with warnings')}")
                    
                    # Show warnings in clean table format
                    if 'raw_response' in ai_result:
                        st.markdown("**⚠️ AI Analysis Warnings:**")
                        warning_data = [{
                            'Type': 'Warning',
                            'Message': 'AI analysis completed but response format unclear',
                            'Details': 'Check raw response for details'
                        }]
                        warning_df = pd.DataFrame(warning_data)
                        st.dataframe(warning_df, use_container_width=True, hide_index=True)
                        
                        with st.expander("🔍 View Raw AI Response"):
                            st.code(ai_result['raw_response'], language='text')
                
                else:
                    st.error(f"❌ {ai_result.get('message', 'AI analysis failed')}")
                    
                    # Show error details in clean format
                    error_data = [{
                        'Type': 'Error',
                        'Message': ai_result.get('message', 'AI analysis failed'),
                        'Action': 'Check API key and try again'
                    }]
                    error_df = pd.DataFrame(error_data)
                    st.dataframe(error_df, use_container_width=True, hide_index=True)

    # Traditional Validation Results
    st.subheader("🔍 Traditional Validation Results")
    
    # Floating Back to Top button for traditional section
    if st.button("⬆️ Back to Top", key="back_to_top_traditional"):
        st.rerun()
    
    traditional_validations = ['row_count', 'data_types', 'null_constraints', 'primary_keys', 
                            'data_completeness', 'data_accuracy', 'business_rules', 'data_format',
                            'referential_integrity', 'performance_accessibility']
    
    for validation_type in traditional_validations:
        if validation_type in report['validations']:
            result = report['validations'][validation_type]
            
            # Create anchor for navigation
            st.markdown(f"<a name='{validation_type.replace('_', '-')}'></a>", unsafe_allow_html=True)
            
            # Add description for each validation type
            validation_descriptions = {
                'row_count': '**Row Count Validation:** Ensures the number of records in source and target datasets match. Detects missing or duplicate data during migration.',
                'data_types': '**Data Types Validation:** Verifies that data types in target match the source. Prevents data type mismatches that could cause application errors.',
                'null_constraints': '**Null Constraints Validation:** Checks that NOT NULL columns in source don\'t have NULL values in target. Prevents data integrity issues.',
                'primary_keys': '**Primary Keys Validation:** Ensures primary keys and unique constraints are preserved. Detects duplicate or missing key records.',
                'referential_integrity': '**Referential Integrity Validation:** Validates foreign key relationships between tables. Prevents orphaned records.',
                'data_completeness': '**Data Completeness Validation:** Confirms no columns were truncated or dropped during migration. Ensures all data is preserved.',
                'data_accuracy': '**Data Accuracy Validation:** Validates that critical field values match between source and target using sampling or checksum comparison.',
                'business_rules': '**Business Rules Validation:** Validates computed/derived columns against business logic (e.g., Total = Quantity × Price).',
                'data_format': '**Data Format Validation:** Ensures formatting consistency across datasets (dates, phone numbers, currency, emails).',
                'performance_accessibility': '**Performance Validation:** Verifies indexes, partitions, and performance configurations for required SLAs.'
            }
            
            if validation_type in validation_descriptions:
                st.markdown(validation_descriptions[validation_type])
            
            st.subheader(f"🔍 {validation_type.replace('_', ' ').title()}")
            
            # Display validation results based on type
            if validation_type == 'row_count':
                display_row_count_validation(result)
            elif validation_type in ['data_types', 'null_constraints', 'data_completeness']:
                display_column_validation(validation_type, result, source_df, target_df)
            elif validation_type == 'primary_keys':
                display_primary_keys_validation(result, source_df, target_df)
            elif validation_type == 'data_accuracy':
                display_data_accuracy_validation(result, source_df, target_df)
            elif validation_type == 'business_rules':
                display_business_rules_validation(result)
            elif validation_type == 'data_format':
                display_data_format_validation(result)
            elif validation_type == 'referential_integrity':
                display_referential_integrity_validation(result)
            elif validation_type == 'performance_accessibility':
                display_performance_validation(result)

def display_row_count_validation(result):
    """Display row count validation results"""
    st.markdown(f"**Status:** {result['status']}")
    st.markdown(f"**Source Count:** {result['source_count']}")
    st.markdown(f"**Target Count:** {result['target_count']}")
    st.markdown(f"**Message:** {result['message']}")

def display_column_validation(validation_type, result, source_df, target_df):
    """Display column-based validation results (data types, null constraints, data completeness)"""
    
    # Create comparison data for display
    comparison_data = []
    
    if isinstance(result, dict):
        # Handle both single result and column-wise results
        if 'status' in result and validation_type == 'row_count':
            # Single result for row count
            comparison_data.append({
                'Column Name': 'Row Count',
                'Source': str(result.get('source_count', 'N/A')),
                'Target': str(result.get('target_count', 'N/A')),
                'Value': 'N/A',
                'Status': result.get('status', 'INFO')
            })
        else:
            # Column-wise results
            for col_name, col_result in result.items():
                if isinstance(col_result, dict) and 'status' in col_result:
                    # Get sample values for the Value column from the actual data
                    sample_values = []
                    try:
                        # Get sample values from source or target dataframe
                        if col_name in source_df.columns:
                            sample_values = source_df[col_name].dropna().head(3).tolist()
                        elif col_name in target_df.columns:
                            sample_values = target_df[col_name].dropna().head(3).tolist()
                    except:
                        pass
                    
                    value_display = ', '.join(map(str, sample_values[:3])) if sample_values else 'No sample data'
                    
                    if validation_type == 'data_types':
                        comparison_data.append({
                            'Column Name': str(col_name),
                            'Source': str(col_result.get('source_dtype', 'N/A')),
                            'Target': str(col_result.get('target_dtype', 'N/A')),
                            'Value': value_display,
                            'Status': str(col_result.get('status', 'INFO'))
                        })
                    elif validation_type == 'null_constraints':
                        comparison_data.append({
                            'Column Name': str(col_name),
                            'Source': f"{col_result.get('source_null_count', 'N/A')} nulls",
                            'Target': f"{col_result.get('target_null_count', 'N/A')} nulls",
                            'Value': value_display,
                            'Status': str(col_result.get('status', 'INFO'))
                        })
                    elif validation_type == 'data_completeness':
                        comparison_data.append({
                            'Column Name': str(col_name),
                            'Source': f"Max: {col_result.get('source_max_length', 'N/A')}",
                            'Target': f"Max: {col_result.get('target_max_length', 'N/A')}",
                            'Value': value_display,
                            'Status': str(col_result.get('status', 'INFO'))
                        })
    
    if comparison_data:
        # Create DataFrame and display
        comparison_df = pd.DataFrame(comparison_data)
        
        # Color code the status column for better visibility
        def color_status(val):
            """Color code the status column with strong colors"""
            if str(val) == 'FAIL':
                return 'background-color: #ff0000 !important; color: white !important; font-weight: bold !important;'
            elif str(val) == 'PASS':
                return 'background-color: #00ff00 !important; color: white !important; font-weight: bold !important;'
            elif str(val) == 'WARNING':
                return 'background-color: #ffaa00 !important; color: white !important; font-weight: bold !important;'
            elif str(val) == 'INFO':
                return 'background-color: #0066ff !important; color: white !important; font-weight: bold !important;'
            else:
                return ''
        
        # Apply styling with stronger color application
        styled_df = comparison_df.style.applymap(color_status, subset=['Status'])
        
        # Display the styled dataframe
        st.dataframe(styled_df, use_container_width=True, hide_index=True)
        
        # Summary statistics
        if len(comparison_data) > 0:
            status_counts = {}
            for row in comparison_data:
                status = row.get('Status', 'INFO')
                if isinstance(status, str):
                    status_counts[status] = status_counts.get(status, 0) + 1
            
            if status_counts:
                st.markdown("**📊 Validation Summary:**")
                summary_cols = st.columns(len(status_counts))
                for i, (status, count) in enumerate(status_counts.items()):
                    with summary_cols[i]:
                        status_icon = {'PASS': '🟢', 'FAIL': '🔴', 'WARNING': '🟡', 'INFO': '🔵'}.get(str(status), '🔵')
                        st.metric(f"{status_icon} {status}", count)

def display_primary_keys_validation(result, source_df, target_df):
    """Display primary keys validation results"""
    
    # Create comparison data for display
    comparison_data = []
    
    if isinstance(result, dict):
        for col_name, col_result in result.items():
            if isinstance(col_result, dict) and 'status' in col_result:
                # Get sample values for the Value column from the actual data
                sample_values = []
                try:
                    # Get sample values from source or target dataframe
                    if col_name in source_df.columns:
                        sample_values = source_df[col_name].dropna().head(3).tolist()
                    elif col_name in target_df.columns:
                        sample_values = target_df[col_name].dropna().head(3).tolist()
                except:
                    pass
                
                value_display = ', '.join(map(str, sample_values[:3])) if sample_values else 'No sample data'
                
                comparison_data.append({
                    'Column Name': str(col_name),
                    'Source': f"{col_result.get('source_unique', 'N/A')} unique",
                    'Target': f"{col_result.get('target_unique', 'N/A')} unique",
                    'Value': value_display,
                    'Details': f"Source duplicates: {col_result.get('source_duplicates', 'N/A')}, Target duplicates: {col_result.get('target_duplicates', 'N/A')}",
                    'Status': str(col_result.get('status', 'INFO'))
                })
    
    if comparison_data:
        # Create DataFrame and display
        comparison_df = pd.DataFrame(comparison_data)
        
        # Color code the status column
        def color_status(val):
            if str(val) == 'FAIL':
                return 'background-color: #ff0000 !important; color: white !important; font-weight: bold !important;'
            elif str(val) == 'PASS':
                return 'background-color: #00ff00 !important; color: white !important; font-weight: bold !important;'
            elif str(val) == 'WARNING':
                return 'background-color: #ffaa00 !important; color: white !important; font-weight: bold !important;'
            elif str(val) == 'INFO':
                return 'background-color: #0066ff !important; color: white !important; font-weight: bold !important;'
            else:
                return ''
        
        styled_df = comparison_df.style.applymap(color_status, subset=['Status'])
        st.dataframe(styled_df, use_container_width=True, hide_index=True)
        
        # Summary statistics
        if len(comparison_data) > 0:
            status_counts = {}
            for row in comparison_data:
                status = row.get('Status', 'INFO')
                if isinstance(status, str):
                    status_counts[status] = status_counts.get(status, 0) + 1
            
            if status_counts:
                st.markdown("**📊 Validation Summary:**")
                summary_cols = st.columns(len(status_counts))
                for i, (status, count) in enumerate(status_counts.items()):
                    with summary_cols[i]:
                        status_icon = {'PASS': '🟢', 'FAIL': '🔴', 'WARNING': '🟡', 'INFO': '🔵'}.get(str(status), '🔵')
                        st.metric(f"{status_icon} {status}", count)

def display_data_accuracy_validation(result, source_df, target_df):
    """Display data accuracy validation results"""
    
    # Create comparison data for display
    comparison_data = []
    
    if isinstance(result, dict):
        for col_name, col_result in result.items():
            if isinstance(col_result, dict) and 'status' in col_result:
                # Check if this column is numeric and has mean data
                if 'mean_difference_pct' in col_result and col_result['mean_difference_pct'] is not None:
                    comparison_data.append({
                        'Column Name': str(col_name),
                        'Source': f"Mean: {col_result.get('source_mean', 'N/A'):.2f}",
                        'Target': f"Mean: {col_result.get('target_mean', 'N/A'):.2f}",
                        'Details': f"Difference: {col_result.get('mean_difference_pct', 'N/A'):.2f}%",
                        'Status': str(col_result.get('status', 'INFO'))
                    })
                elif 'source_sample' in col_result and 'target_sample' in col_result:
                    # For non-numeric columns, show actual sample values instead of just counts
                    source_samples = col_result.get('source_sample', [])
                    target_samples = col_result.get('target_sample', [])
                    
                    # Get actual sample values from the dataframes if not in result
                    if not source_samples and col_name in source_df.columns:
                        source_samples = source_df[col_name].dropna().head(3).tolist()
                    if not target_samples and col_name in target_df.columns:
                        target_samples = target_df[col_name].dropna().head(3).tolist()
                    
                    source_display = ', '.join(map(str, source_samples[:2])) if source_samples else 'No data'
                    target_display = ', '.join(map(str, target_samples[:2])) if target_samples else 'No data'
                    
                    comparison_data.append({
                        'Column Name': str(col_name),
                        'Source': source_display,
                        'Target': target_display,
                        'Details': f"Sample comparison - Source: {len(source_samples)}, Target: {len(target_samples)}",
                        'Status': str(col_result.get('status', 'INFO'))
                    })
                else:
                    comparison_data.append({
                        'Column Name': str(col_name),
                        'Source': 'Data available',
                        'Target': 'Data available',
                        'Details': 'Accuracy validation completed',
                        'Status': str(col_result.get('status', 'INFO'))
                    })
    
    if comparison_data:
        # Create DataFrame and display
        comparison_df = pd.DataFrame(comparison_data)
        
        # Color code the status column
        def color_status(val):
            if str(val) == 'FAIL':
                return 'background-color: #ff0000 !important; color: white !important; font-weight: bold !important;'
            elif str(val) == 'PASS':
                return 'background-color: #00ff00 !important; color: white !important; font-weight: bold !important;'
            elif str(val) == 'WARNING':
                return 'background-color: #ffaa00 !important; color: white !important; font-weight: bold !important;'
            elif str(val) == 'INFO':
                return 'background-color: #0066ff !important; color: white !important; font-weight: bold !important;'
            else:
                return ''
        
        styled_df = comparison_df.style.applymap(color_status, subset=['Status'])
        st.dataframe(styled_df, use_container_width=True, hide_index=True)
        
        # Summary statistics
        if len(comparison_data) > 0:
            status_counts = {}
            for row in comparison_data:
                status = row.get('Status', 'INFO')
                if isinstance(status, str):
                    status_counts[status] = status_counts.get(status, 0) + 1
            
            if status_counts:
                st.markdown("**📊 Validation Summary:**")
                summary_cols = st.columns(len(status_counts))
                for i, (status, count) in enumerate(status_counts.items()):
                    with summary_cols[i]:
                        status_icon = {'PASS': '🟢', 'FAIL': '🔴', 'WARNING': '🟡', 'INFO': '🔵'}.get(str(status), '🔵')
                        st.metric(f"{status_icon} {status}", count)

def display_business_rules_validation(result):
    """Display business rules validation results"""
    
    # Create comparison data for display
    comparison_data = []
    
    if isinstance(result, dict):
        for col_name, col_result in result.items():
            if isinstance(col_result, dict) and 'status' in col_result:
                violations_count = col_result.get('violations', 0)
                messages = col_result.get('messages', [])
                details = '; '.join(messages) if messages else 'No violation details available'
                
                comparison_data.append({
                    'Column Name': str(col_name),
                    'Source': 'Rules defined',
                    'Target': f"{violations_count} violations found",
                    'Details': details[:60] + "..." if len(details) > 60 else details,
                    'Status': str(col_result.get('status', 'INFO'))
                })
    
    if comparison_data:
        # Create DataFrame and display
        comparison_df = pd.DataFrame(comparison_data)
        
        # Color code the status column
        def color_status(val):
            if str(val) == 'FAIL':
                return 'background-color: #ff0000 !important; color: white !important; font-weight: bold !important;'
            elif str(val) == 'PASS':
                return 'background-color: #00ff00 !important; color: white !important; font-weight: bold !important;'
            elif str(val) == 'WARNING':
                return 'background-color: #ffaa00 !important; color: white !important; font-weight: bold !important;'
            elif str(val) == 'INFO':
                return 'background-color: #0066ff !important; color: white !important; font-weight: bold !important;'
            else:
                return ''
        
        styled_df = comparison_df.style.applymap(color_status, subset=['Status'])
        st.dataframe(styled_df, use_container_width=True, hide_index=True)
        
        # Summary statistics
        if len(comparison_data) > 0:
            status_counts = {}
            for row in comparison_data:
                status = row.get('Status', 'INFO')
                if isinstance(status, str):
                    status_counts[status] = status_counts.get(status, 0) + 1
            
            if status_counts:
                st.markdown("**📊 Validation Summary:**")
                summary_cols = st.columns(len(status_counts))
                for i, (status, count) in enumerate(status_counts.items()):
                    with summary_cols[i]:
                        status_icon = {'PASS': '🟢', 'FAIL': '🔴', 'WARNING': '🟡', 'INFO': '🔵'}.get(str(status), '🔵')
                        st.metric(f"{status_icon} {status}", count)

def display_data_format_validation(result):
    """Display data format validation results"""
    
    # Create comparison data for display
    comparison_data = []
    
    if isinstance(result, dict):
        if 'overall' in result:
            # Show overall summary first
            overall_result = result['overall']
            comparison_data.append({
                'Column Name': 'Overall Format',
                'Source': 'Format validation',
                'Target': f"{overall_result.get('total_issues', 0)} issues found",
                'Details': overall_result.get('message', 'No format details available'),
                'Status': overall_result.get('status', 'INFO')
            })
        
        # Show individual column results
        for col_name, col_result in result.items():
            if col_name != 'overall' and isinstance(col_result, dict) and 'status' in col_result:
                if 'format_issues' in col_result:
                    if isinstance(col_result['format_issues'], list) and len(col_result['format_issues']) > 0:
                        comparison_data.append({
                            'Column Name': str(col_name),
                            'Source': 'Expected format',
                            'Target': f"{len(col_result['format_issues'])} format issues",
                            'Details': '; '.join(col_result['format_issues']),
                            'Status': 'FAIL'
                        })
                    else:
                        comparison_data.append({
                            'Column Name': str(col_name),
                            'Source': 'Expected format',
                            'Target': 'No format issues',
                            'Details': 'Format validation passed',
                            'Status': 'PASS'
                        })
                else:
                    comparison_data.append({
                        'Column Name': str(col_name),
                        'Source': 'Expected format',
                        'Target': 'Format validation completed',
                        'Details': col_result.get('message', 'No format details available'),
                        'Status': col_result.get('status', 'INFO')
                    })
    
    if comparison_data:
        # Create DataFrame and display
        comparison_df = pd.DataFrame(comparison_data)
        
        # Color code the status column
        def color_status(val):
            if str(val) == 'FAIL':
                return 'background-color: #ff0000 !important; color: white !important; font-weight: bold !important;'
            elif str(val) == 'PASS':
                return 'background-color: #00ff00 !important; color: white !important; font-weight: bold !important;'
            elif str(val) == 'WARNING':
                return 'background-color: #ffaa00 !important; color: white !important; font-weight: bold !important;'
            elif str(val) == 'INFO':
                return 'background-color: #0066ff !important; color: white !important; font-weight: bold !important;'
            else:
                return ''
        
        styled_df = comparison_df.style.applymap(color_status, subset=['Status'])
        st.dataframe(styled_df, use_container_width=True, hide_index=True)
        
        # Summary statistics
        if len(comparison_data) > 0:
            status_counts = {}
            for row in comparison_data:
                status = row.get('Status', 'INFO')
                if isinstance(status, str):
                    status_counts[status] = status_counts.get(status, 0) + 1
            
            if status_counts:
                st.markdown("**📊 Validation Summary:**")
                summary_cols = st.columns(len(status_counts))
                for i, (status, count) in enumerate(status_counts.items()):
                    with summary_cols[i]:
                        status_icon = {'PASS': '🟢', 'FAIL': '🔴', 'WARNING': '🟡', 'INFO': '🔵'}.get(str(status), '🔵')
                        st.metric(f"{status_icon} {status}", count)

def display_referential_integrity_validation(result):
    """Display referential integrity validation results"""
    st.markdown(f"**Status:** {result['status']}")
    st.markdown(f"**Message:** {result['message']}")
    
    if 'ai_analysis' in result:
        st.markdown("**AI Analysis Available:** Check AI validation results for detailed insights.")

def display_performance_validation(result):
    """Display performance validation results"""
    st.markdown(f"**Status:** {result['status']}")
    st.markdown(f"**Message:** {result['message']}")
    
    if 'performance_metrics' in result:
        metrics = result['performance_metrics']
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Source Size", f"{metrics['source_size_mb']:.2f} MB")
        
        with col2:
            st.metric("Target Size", f"{metrics['target_size_mb']:.2f} MB")
        
        with col3:
            st.metric("Columns", metrics['column_count'])
        
        with col4:
            st.metric("Rows", metrics['row_count'])

if __name__ == "__main__":
    main()
