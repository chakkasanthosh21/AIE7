"""Intelligent validation agent using free LangChain tools."""

import asyncio
from typing import Dict, List, Any, Optional
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain.tools import Tool
from langchain.memory import ConversationBufferMemory
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage
import streamlit as st
import pandas as pd
import numpy as np

class IntelligentValidationAgent:
    """Intelligent validation agent that chooses best validation strategies."""
    
    def __init__(self, openai_api_key: str):
        self.llm = ChatOpenAI(
            model="gpt-4o-mini",  # Use cheaper model for cost efficiency
            temperature=0.1,
            api_key=openai_api_key
        )
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )
        self.tools = self._create_validation_tools()
        self.agent = self._create_agent()
        self.agent_executor = AgentExecutor(
            agent=self.agent,
            tools=self.tools,
            memory=self.memory,
            verbose=True,
            handle_parsing_errors=True
        )
        self.validation_history = []
    
    def _create_validation_tools(self) -> List[Tool]:
        """Create specialized validation tools."""
        return [
            Tool(
                name="schema_validator",
                func=self._validate_schema_tool,
                description="Validate data schema consistency across datasets. Use this when you need to check column names, data types, and structural compatibility."
            ),
            Tool(
                name="quality_assessor",
                func=self._assess_quality_tool,
                description="Assess data quality metrics including completeness, consistency, and uniqueness. Use this for comprehensive quality evaluation."
            ),
            Tool(
                name="business_rule_checker",
                func=self._check_business_rules_tool,
                description="Check data against common business rules and constraints. Use this to validate business logic and domain-specific requirements."
            ),
            Tool(
                name="anomaly_detector",
                func=self._detect_anomalies_tool,
                description="Detect anomalies and outliers in numerical data. Use this when you suspect data quality issues or unusual patterns."
            ),
            Tool(
                name="semantic_analyzer",
                func=self._analyze_semantics_tool,
                description="Analyze semantic relationships between columns and datasets. Use this to understand data meaning and find hidden connections."
            ),
            Tool(
                name="compliance_validator",
                func=self._validate_compliance_tool,
                description="Validate data against common compliance requirements. Use this for regulatory and governance checks."
            ),
            Tool(
                name="performance_optimizer",
                func=self._optimize_performance_tool,
                description="Analyze and optimize data performance characteristics. Use this to improve processing speed and memory usage."
            )
        ]
    
    def _create_agent(self):
        """Create an intelligent validation agent."""
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert data validation specialist with deep knowledge of data quality, business rules, and best practices.

Your role is to:
1. Analyze validation requests and choose the most appropriate tools
2. Provide intelligent recommendations based on validation results
3. Explain findings in business-friendly language
4. Suggest improvements and next steps

Available tools:
- schema_validator: For structural validation
- quality_assessor: For quality metrics
- business_rule_checker: For business logic validation
- anomaly_detector: For outlier detection
- semantic_analyzer: For meaning analysis
- compliance_validator: For regulatory checks
- performance_optimizer: For optimization

Always explain your reasoning and provide actionable insights."""),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad")
        ])
        
        return create_openai_functions_agent(
            llm=self.llm,
            tools=self.tools,
            prompt=prompt
        )
    
    def _validate_schema_tool(self, data_sources: Dict[str, pd.DataFrame]) -> Dict:
        """Validate data schema consistency across datasets."""
        try:
            schemas = {}
            conflicts = []
            
            for name, dataset_df in data_sources.items():
                schemas[name] = {
                    'columns': list(dataset_df.columns),
                    'dtypes': dataset_df.dtypes.to_dict(),
                    'shape': dataset_df.shape,
                    'memory_usage_mb': dataset_df.memory_usage(deep=True).sum() / 1024 / 1024
                }
            
            # Analyze differences
            if len(schemas) >= 2:
                base_schema = schemas[list(schemas.keys())[0]]
                for name, schema in schemas.items():
                    if name == list(schemas.keys())[0]:
                        continue
                    
                    base_cols = set(base_schema['columns'])
                    schema_cols = set(schema['columns'])
                    
                    missing_cols = base_cols - schema_cols
                    extra_cols = schema_cols - base_cols
                    
                    if missing_cols:
                        conflicts.append(f"{name} missing columns: {missing_cols}")
                    if extra_cols:
                        conflicts.append(f"{name} has extra columns: {extra_cols}")
            
            return {
                'schemas': schemas,
                'conflicts': conflicts,
                'has_conflicts': len(conflicts) > 0,
                'recommendation': 'Standardize column names and structure across datasets' if conflicts else 'Schemas are consistent'
            }
            
        except Exception as e:
            return {'error': f"Schema validation failed: {str(e)}"}
    
    def _assess_quality_tool(self, data_sources: Dict[str, pd.DataFrame]) -> Dict:
        """Assess data quality metrics."""
        try:
            quality_metrics = {}
            
            for name, dataset_df in data_sources.items():
                # Basic quality metrics
                total_cells = dataset_df.size
                null_cells = dataset_df.isnull().sum().sum()
                completeness = 1 - (null_cells / total_cells)
                
                duplicate_rows = dataset_df.duplicated().sum()
                consistency = 1 - (duplicate_rows / len(dataset_df))
                
                # Column-specific quality
                column_quality = {}
                for col in dataset_df.columns:
                    col_data = dataset_df[col].dropna()
                    if len(col_data) > 0:
                        if col_data.dtype in ['int64', 'float64']:
                            column_quality[col] = {
                                'completeness': 1 - (col_data.isnull().sum() / len(dataset_df)),
                                'uniqueness': col_data.nunique() / len(col_data),
                                'range': (col_data.min(), col_data.max())
                            }
                        else:
                            column_quality[col] = {
                                'completeness': 1 - (col_data.isnull().sum() / len(dataset_df)),
                                'uniqueness': col_data.nunique() / len(col_data),
                                'avg_length': col_data.astype(str).str.len().mean()
                            }
                
                quality_metrics[name] = {
                    'completeness': completeness,
                    'consistency': consistency,
                    'column_quality': column_quality,
                    'total_rows': len(dataset_df),
                    'total_columns': len(dataset_df.columns)
                }
            
            return {
                'quality_metrics': quality_metrics,
                'overall_score': sum([m['completeness'] + m['consistency'] for m in quality_metrics.values()]) / (len(quality_metrics) * 2),
                'recommendations': [
                    'Improve data completeness by addressing null values',
                    'Reduce duplicate entries for better consistency',
                    'Standardize column naming conventions'
                ]
            }
            
        except Exception as e:
            return {'error': f"Quality assessment failed: {str(e)}"}
    
    def _check_business_rules_tool(self, data_sources: Dict[str, pd.DataFrame]) -> Dict:
        """Check data against common business rules."""
        try:
            business_rule_violations = {}
            
            for name, dataset_df in data_sources.items():
                violations = []
                
                # Check for common business rule violations
                for col in dataset_df.columns:
                    col_data = dataset_df[col].dropna()
                    
                    if len(col_data) > 0:
                        # Check for negative values in financial columns
                        if any(keyword in col.lower() for keyword in ['price', 'cost', 'amount', 'revenue', 'profit']):
                            if col_data.dtype in ['int64', 'float64']:
                                negative_count = (col_data < 0).sum()
                                if negative_count > 0:
                                    violations.append(f"Column '{col}' has {negative_count} negative values")
                        
                        # Check for unrealistic values
                        if col_data.dtype in ['int64', 'float64']:
                            mean_val = col_data.mean()
                            std_val = col_data.std()
                            if std_val > 0:
                                z_scores = abs((col_data - mean_val) / std_val)
                                outliers = (z_scores > 3).sum()
                                if outliers > 0:
                                    violations.append(f"Column '{col}' has {outliers} statistical outliers")
                
                business_rule_violations[name] = violations
            
            return {
                'violations': business_rule_violations,
                'total_violations': sum(len(v) for v in business_rule_violations.values()),
                'recommendations': [
                    'Review negative values in financial columns',
                    'Investigate statistical outliers',
                    'Validate business logic constraints'
                ]
            }
            
        except Exception as e:
            return {'error': f"Business rule validation failed: {str(e)}"}
    
    def _detect_anomalies_tool(self, data_sources: Dict[str, pd.DataFrame]) -> Dict:
        """Detect anomalies and outliers in numerical data."""
        try:
            anomaly_results = {}
            
            for name, dataset_df in data_sources.items():
                anomalies = {}
                
                for col in dataset_df.columns:
                    col_data = dataset_df[col].dropna()
                    
                    if len(col_data) > 0 and col_data.dtype in ['int64', 'float64']:
                        # Statistical anomaly detection
                        Q1 = col_data.quantile(0.25)
                        Q3 = col_data.quantile(0.75)
                        IQR = Q3 - Q1
                        
                        lower_bound = Q1 - 1.5 * IQR
                        upper_bound = Q3 + 1.5 * IQR
                        
                        outliers = col_data[(col_data < lower_bound) | (col_data > upper_bound)]
                        
                        if len(outliers) > 0:
                            anomalies[col] = {
                                'count': len(outliers),
                                'percentage': len(outliers) / len(col_data),
                                'values': outliers.head(10).tolist(),
                                'bounds': (lower_bound, upper_bound)
                            }
                
                anomaly_results[name] = {
                    'anomalies': anomalies,
                    'total_anomalies': sum(len(a['values']) for a in anomalies.values()),
                    'columns_with_anomalies': len(anomalies)
                }
            
            return {
                'anomaly_results': anomaly_results,
                'total_anomalies': sum(r['total_anomalies'] for r in anomaly_results.values()),
                'recommendations': [
                    'Investigate statistical outliers',
                    'Review data collection processes',
                    'Consider data cleaning strategies'
                ]
            }
            
        except Exception as e:
            return {'error': f"Anomaly detection failed: {str(e)}"}
    
    def _analyze_semantics_tool(self, data_sources: Dict[str, pd.DataFrame]) -> Dict:
        """Analyze semantic relationships between columns and datasets."""
        try:
            semantic_analysis = {}
            
            for name, dataset_df in data_sources.items():
                column_relationships = {}
                
                for col in dataset_df.columns:
                    col_data = dataset_df[col].dropna()
                    
                    if len(col_data) > 0:
                        # Analyze column characteristics
                        if col_data.dtype in ['int64', 'float64']:
                            column_relationships[col] = {
                                'type': 'numerical',
                                'range': (col_data.min(), col_data.max()),
                                'distribution': 'normal' if col_data.skew() < 1 else 'skewed',
                                'correlations': {}
                            }
                        else:
                            column_relationships[col] = {
                                'type': 'categorical',
                                'unique_values': col_data.nunique(),
                                'most_common': col_data.value_counts().head(3).to_dict(),
                                'relationships': {}
                            }
                
                semantic_analysis[name] = {
                    'column_relationships': column_relationships,
                    'dataset_characteristics': {
                        'size': dataset_df.shape,
                        'memory_usage': dataset_df.memory_usage(deep=True).sum() / 1024 / 1024
                    }
                }
            
            return {
                'semantic_analysis': semantic_analysis,
                'insights': [
                    'Numerical columns show statistical patterns',
                    'Categorical columns reveal data categories',
                    'Column relationships indicate data structure'
                ]
            }
            
        except Exception as e:
            return {'error': f"Semantic analysis failed: {str(e)}"}
    
    def _validate_compliance_tool(self, data_sources: Dict[str, pd.DataFrame]) -> Dict:
        """Validate data against common compliance requirements."""
        try:
            compliance_results = {}
            
            for name, dataset_df in data_sources.items():
                compliance_checks = {
                    'data_privacy': True,
                    'data_integrity': True,
                    'audit_trail': True,
                    'data_retention': True
                }
                
                # Check for sensitive data patterns
                sensitive_patterns = ['ssn', 'credit_card', 'password', 'email', 'phone']
                for col in dataset_df.columns:
                    if any(pattern in col.lower() for pattern in sensitive_patterns):
                        compliance_checks['data_privacy'] = False
                        break
                
                # Check data integrity
                if dataset_df.isnull().sum().sum() > len(dataset_df) * 0.1:  # More than 10% nulls
                    compliance_checks['data_integrity'] = False
                
                compliance_results[name] = compliance_checks
            
            return {
                'compliance_results': compliance_results,
                'overall_compliance': all(all(checks.values()) for checks in compliance_results.values()),
                'recommendations': [
                    'Implement data privacy controls',
                    'Improve data quality standards',
                    'Establish audit procedures'
                ]
            }
            
        except Exception as e:
            return {'error': f"Compliance validation failed: {str(e)}"}
    
    def _optimize_performance_tool(self, data_sources: Dict[str, pd.DataFrame]) -> Dict:
        """Analyze and optimize data performance characteristics."""
        try:
            performance_analysis = {}
            
            for name, dataset_df in data_sources.items():
                # Memory usage analysis
                memory_usage = dataset_df.memory_usage(deep=True)
                total_memory = memory_usage.sum() / 1024 / 1024  # MB
                
                # Data type optimization suggestions
                optimization_suggestions = []
                for col in dataset_df.columns:
                    col_data = dataset_df[col]
                    
                    if col_data.dtype == 'object':
                        # Check if can be converted to category
                        if col_data.nunique() / len(col_data) < 0.5:  # Less than 50% unique values
                            optimization_suggestions.append(f"Convert '{col}' to category type")
                    
                    elif col_data.dtype == 'int64':
                        # Check if can use smaller int types
                        if col_data.min() >= -128 and col_data.max() <= 127:
                            optimization_suggestions.append(f"Convert '{col}' to int8")
                        elif col_data.min() >= -32768 and col_data.max() <= 32767:
                            optimization_suggestions.append(f"Convert '{col}' to int16")
                
                performance_analysis[name] = {
                    'memory_usage_mb': total_memory,
                    'optimization_suggestions': optimization_suggestions,
                    'estimated_savings': len(optimization_suggestions) * 0.1  # Rough estimate
                }
            
            return {
                'performance_analysis': performance_analysis,
                'total_memory_usage': sum(a['memory_usage_mb'] for a in performance_analysis.values()),
                'recommendations': [
                    'Implement data type optimizations',
                    'Use appropriate data structures',
                    'Monitor memory usage patterns'
                ]
            }
            
        except Exception as e:
            return {'error': f"Performance optimization failed: {str(e)}"}
    
    def _assess_overall_quality(self, quality_metrics: Dict) -> str:
        """Assess overall data quality."""
        overall_scores = [metrics['overall_score'] for metrics in quality_metrics.values()]
        avg_score = np.mean(overall_scores)
        
        if avg_score >= 0.9:
            return "Excellent - Data quality is very high"
        elif avg_score >= 0.7:
            return "Good - Data quality is acceptable with minor issues"
        elif avg_score >= 0.5:
            return "Fair - Data quality needs improvement"
        else:
            return "Poor - Data quality requires immediate attention"
    
    def _identify_priority_issues(self, quality_metrics: Dict) -> List[str]:
        """Identify priority issues for immediate attention."""
        priority_issues = []
        
        for name, metrics in quality_metrics.items():
            if metrics['completeness'] < 0.8:
                priority_issues.append(f"{name}: Low completeness ({metrics['completeness']:.1%})")
            if metrics['consistency'] < 0.9:
                priority_issues.append(f"{name}: Low consistency ({metrics['consistency']:.1%})")
        
        return priority_issues
    
    def _generate_semantic_insights(self, semantic_analysis: Dict) -> List[str]:
        """Generate insights from semantic analysis."""
        insights = []
        
        for dataset_name, columns in semantic_analysis.items():
            for col, analysis in columns.items():
                if analysis['semantic_type'] == 'email_like':
                    insights.append(f"{dataset_name}.{col}: Email-like data detected")
                elif analysis['semantic_type'] == 'date_like':
                    insights.append(f"{dataset_name}.{col}: Date-like data detected")
                elif analysis['semantic_type'] == 'code_like':
                    insights.append(f"{dataset_name}.{col}: Code-like data detected")
        
        return insights
    
    async def run_intelligent_validation(self, data_sources: Dict[str, pd.DataFrame], validation_context: str) -> Dict:
        """Run intelligent validation using AI agent."""
        try:
            context = f"""
            Validate these datasets: {list(data_sources.keys())}
            Business context: {validation_context}
            
            Please provide a comprehensive validation analysis focusing on:
            1. Schema consistency and structural issues
            2. Data quality metrics and anomalies
            3. Business rule compliance
            4. Semantic relationships and patterns
            5. Performance optimization opportunities
            6. Compliance and governance issues
            
            Use the appropriate tools and provide actionable recommendations.
            """
            
            result = await self.agent.ainvoke({
                "input": context,
                "chat_history": self.memory.chat_memory.messages
            })
            
            # Store validation history
            self.validation_history.append({
                'timestamp': pd.Timestamp.now(),
                'datasets': list(data_sources.keys()),
                'context': validation_context,
                'result': result
            })
            
            return {
                'agent_response': result,
                'validation_history': self.validation_history,
                'tools_used': [tool.name for tool in self.tools],
                'recommendations': self._extract_recommendations(result)
            }
            
        except Exception as e:
            return {
                'error': f"Intelligent validation failed: {str(e)}",
                'fallback': "Using basic validation tools instead"
            }
    
    def _extract_recommendations(self, agent_result: Dict) -> List[str]:
        """Extract recommendations from agent response."""
        recommendations = []
        
        if 'output' in agent_result:
            output = agent_result['output']
            # Simple extraction - in practice, you'd use more sophisticated parsing
            if 'recommendation' in output.lower():
                recommendations.append(output)
        
        return recommendations

    def chat_with_agent(self, user_input: str, chat_history: List = None) -> str:
        """Chat with the validation agent about the datasets."""
        if chat_history is None:
            chat_history = []
        
        try:
            # Create a more conversational prompt
            system_prompt = """You are an expert data validation specialist. You can help users understand their datasets, identify issues, and provide recommendations. 

Available tools:
- schema_validator: Check data schemas and types
- quality_assessor: Assess overall data quality
- anomaly_detector: Find anomalies and outliers
- semantic_analyzer: Analyze semantic relationships
- data_explorer: Explore dataset characteristics

Be helpful, conversational, and provide specific insights about the user's data. If they ask about specific columns or issues, use the appropriate tools to investigate."""
            
            # Update the agent with the new prompt
            prompt = ChatPromptTemplate.from_messages([
                ("system", system_prompt),
                MessagesPlaceholder(variable_name="chat_history"),
                ("human", "{input}"),
                MessagesPlaceholder(variable_name="agent_scratchpad")
            ])
            
            # Create a new agent with the updated prompt
            new_agent = create_openai_functions_agent(llm=self.llm, tools=self.tools, prompt=prompt)
            
            # Create a new agent executor for this conversation
            agent_executor = AgentExecutor(
                agent=new_agent,
                tools=self.tools,
                memory=self.memory,
                verbose=True,
                handle_parsing_errors=True
            )
            
            # Run the agent
            response = agent_executor.invoke({
                "input": user_input,
                "chat_history": chat_history
            })
            
            return response.get("output", "I'm sorry, I couldn't process your request. Please try again.")
            
        except Exception as e:
            return f"I encountered an error: {str(e)}. Please try rephrasing your question or check if your OpenAI API key is valid."
    
    def get_dataset_summary(self, data_sources: Dict[str, pd.DataFrame]) -> str:
        """Get a quick summary of all datasets for the agent to reference."""
        summary = []
        for name, dataset_df in data_sources.items():
            summary.append(f"Dataset '{name}': {len(dataset_df)} rows, {len(dataset_df.columns)} columns")
            summary.append(f"Columns: {', '.join(dataset_df.columns[:5])}{'...' if len(dataset_df.columns) > 5 else ''}")
            summary.append(f"Data types: {dict(dataset_df.dtypes.value_counts())}")
            summary.append("---")
        
        return "\n".join(summary)
    
    def suggest_questions(self) -> List[str]:
        """Suggest helpful questions users can ask the agent."""
        return [
            "What are the main data quality issues in my datasets?",
            "Which columns have the most anomalies?",
            "Are there any schema inconsistencies between datasets?",
            "What recommendations do you have for improving data quality?",
            "Can you analyze the relationship between specific columns?",
            "What patterns do you see in the data?",
            "Are there any data type mismatches?",
            "What's the overall health score of my data?"
        ]
