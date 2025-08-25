"""Intelligent validation agent using free LangChain tools."""

import asyncio
from typing import Dict, List, Any, Optional
from langchain.agents import Tool, AgentExecutor, create_openai_functions_agent
from langchain.tools import tool
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
    
    @tool
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
    
    @tool
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
                    'overall_score': (completeness + consistency) / 2
                }
            
            return {
                'quality_metrics': quality_metrics,
                'overall_assessment': self._assess_overall_quality(quality_metrics),
                'priority_issues': self._identify_priority_issues(quality_metrics)
            }
            
        except Exception as e:
            return {'error': f"Quality assessment failed: {str(e)}"}
    
    @tool
    def _check_business_rules_tool(self, data_sources: Dict[str, pd.DataFrame]) -> Dict:
        """Check data against common business rules."""
        try:
            business_rule_violations = {}
            
            for name, dataset_df in data_sources.items():
                violations = []
                
                for col in dataset_df.columns:
                    col_data = dataset_df[col].dropna()
                    
                    if len(col_data) > 0:
                        # Common business rules
                        if col.lower() in ['age', 'age_group']:
                            if col_data.dtype in ['int64', 'float64']:
                                if (col_data < 0).any() or (col_data > 120).any():
                                    violations.append(f"Column {col}: Age values outside reasonable range (0-120)")
                        
                        elif col.lower() in ['email', 'email_address']:
                            # Basic email format check
                            email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
                            invalid_emails = col_data[~col_data.astype(str).str.match(email_pattern, na=False)]
                            if len(invalid_emails) > 0:
                                violations.append(f"Column {col}: {len(invalid_emails)} invalid email formats")
                        
                        elif col.lower() in ['phone', 'phone_number']:
                            # Basic phone format check
                            phone_pattern = r'^[\+]?[1-9][\d]{0,15}$'
                            invalid_phones = col_data[~col_data.astype(str).str.match(phone_pattern, na=False)]
                            if len(invalid_phones) > 0:
                                violations.append(f"Column {col}: {len(invalid_phones)} invalid phone formats")
                        
                        elif col.lower() in ['date', 'created_date', 'updated_date']:
                            # Date format check
                            try:
                                pd.to_datetime(col_data)
                            except:
                                violations.append(f"Column {col}: Invalid date formats detected")
                
                business_rule_violations[name] = violations
            
            return {
                'violations': business_rule_violations,
                'total_violations': sum(len(v) for v in business_rule_violations.values()),
                'recommendation': 'Implement data validation rules and business logic checks'
            }
            
        except Exception as e:
            return {'error': f"Business rule checking failed: {str(e)}"}
    
    @tool
    def _detect_anomalies_tool(self, data_sources: Dict[str, pd.DataFrame]) -> Dict:
        """Detect anomalies and outliers in numerical data."""
        try:
            anomaly_report = {}
            
            for name, dataset_df in data_sources.items():
                anomalies = {}
                
                for col in dataset_df.select_dtypes(include=[np.number]).columns:
                    col_data = dataset_df[col].dropna()
                    
                    if len(col_data) > 10:
                        # Statistical outlier detection
                        Q1 = col_data.quantile(0.25)
                        Q3 = col_data.quantile(0.75)
                        IQR = Q3 - Q1
                        
                        lower_bound = Q1 - 1.5 * IQR
                        upper_bound = Q3 + 1.5 * IQR
                        
                        outliers = col_data[(col_data < lower_bound) | (col_data > upper_bound)]
                        
                        if len(outliers) > 0:
                            anomalies[col] = {
                                'outlier_count': len(outliers),
                                'outlier_percentage': len(outliers) / len(col_data),
                                'outlier_values': outliers.head(10).tolist(),
                                'bounds': (lower_bound, upper_bound),
                                'severity': 'high' if len(outliers) / len(col_data) > 0.1 else 'medium'
                            }
                
                anomaly_report[name] = anomalies
            
            return {
                'anomalies': anomaly_report,
                'total_anomalies': sum(len(a) for a in anomaly_report.values()),
                'recommendation': 'Investigate outlier patterns and review data collection processes'
            }
            
        except Exception as e:
            return {'error': f"Anomaly detection failed: {str(e)}"}
    
    @tool
    def _analyze_semantics_tool(self, data_sources: Dict[str, pd.DataFrame]) -> Dict:
        """Analyze semantic relationships between columns and datasets."""
        try:
            semantic_analysis = {}
            
            for name, dataset_df in data_sources.items():
                column_insights = {}
                
                for col in dataset_df.columns:
                    col_data = dataset_df[col].dropna()
                    
                    if len(col_data) > 0:
                        # Semantic analysis
                        if col_data.dtype in ['int64', 'float64']:
                            # Numerical column analysis
                            if col_data.min() >= 0 and col_data.max() <= 100:
                                semantic_type = "percentage_like"
                            elif col_data.min() >= 1900 and col_data.max() <= 2100:
                                semantic_type = "year_like"
                            elif col_data.min() >= 1 and col_data.max() <= 31:
                                semantic_type = "day_like"
                            else:
                                semantic_type = "numeric"
                        else:
                            # Text column analysis
                            sample_values = col_data.head(10).astype(str)
                            if sample_values.str.contains('@').any():
                                semantic_type = "email_like"
                            elif sample_values.str.contains(r'\d{4}-\d{2}-\d{2}').any():
                                semantic_type = "date_like"
                            elif sample_values.str.len().mean() < 3:
                                semantic_type = "code_like"
                            else:
                                semantic_type = "text"
                        
                        column_insights[col] = {
                            'semantic_type': semantic_type,
                            'unique_values': col_data.nunique(),
                            'most_common': col_data.value_counts().head(3).to_dict()
                        }
                
                semantic_analysis[name] = column_insights
            
            return {
                'semantic_analysis': semantic_analysis,
                'insights': self._generate_semantic_insights(semantic_analysis)
            }
            
        except Exception as e:
            return {'error': f"Semantic analysis failed: {str(e)}"}
    
    @tool
    def _validate_compliance_tool(self, data_sources: Dict[str, pd.DataFrame]) -> Dict:
        """Validate data against common compliance requirements."""
        try:
            compliance_report = {}
            
            for name, dataset_df in data_sources.items():
                compliance_issues = []
                
                # GDPR-like compliance checks
                for col in dataset_df.columns:
                    col_lower = col.lower()
                    
                    # PII detection
                    if any(keyword in col_lower for keyword in ['ssn', 'social_security', 'passport', 'id_number']):
                        compliance_issues.append(f"Column {col}: Potential PII data detected")
                    
                    # Sensitive data
                    if any(keyword in col_lower for keyword in ['password', 'credit_card', 'bank_account']):
                        compliance_issues.append(f"Column {col}: Sensitive data detected")
                
                # Data retention check
                if 'created_date' in dataset_df.columns or 'updated_date' in dataset_df.columns:
                    date_col = 'created_date' if 'created_date' in dataset_df.columns else 'updated_date'
                    if dataset_df[date_col].dtype == 'object':
                        try:
                            dates = pd.to_datetime(dataset_df[date_col])
                            if (dates < pd.Timestamp('2010-01-01')).any():
                                compliance_issues.append(f"Column {date_col}: Data older than 10 years detected")
                        except:
                            compliance_issues.append(f"Column {date_col}: Invalid date formats")
                
                compliance_report[name] = compliance_issues
            
            return {
                'compliance_issues': compliance_report,
                'total_issues': sum(len(i) for i in compliance_report.values()),
                'recommendation': 'Review data governance policies and implement compliance controls'
            }
            
        except Exception as e:
            return {'error': f"Compliance validation failed: {str(e)}"}
    
    @tool
    def _optimize_performance_tool(self, data_sources: Dict[str, pd.DataFrame]) -> Dict:
        """Analyze and optimize data performance characteristics."""
        try:
            performance_report = {}
            
            for name, dataset_df in data_sources.items():
                optimizations = []
                
                # Memory usage analysis
                current_memory = dataset_df.memory_usage(deep=True).sum() / 1024 / 1024  # MB
                
                # Data type optimization opportunities
                for col in dataset_df.columns:
                    col_data = dataset_df[col].dropna()
                    
                    if col_data.dtype == 'object':
                        # Check if can be converted to category
                        if col_data.nunique() / len(col_data) < 0.5:
                            optimizations.append(f"Column {col}: Convert to category type (saves memory)")
                    
                    elif col_data.dtype == 'int64':
                        # Check if can use smaller integer types
                        if col_data.min() >= -128 and col_data.max() <= 127:
                            optimizations.append(f"Column {col}: Convert to int8 (saves memory)")
                        elif col_data.min() >= -32768 and col_data.max() <= 32767:
                            optimizations.append(f"Column {col}: Convert to int16 (saves memory)")
                
                # Row optimization
                if dataset_df.duplicated().sum() > 0:
                    optimizations.append(f"Remove {dataset_df.duplicated().sum()} duplicate rows")
                
                performance_report[name] = {
                    'current_memory_mb': current_memory,
                    'optimizations': optimizations,
                    'potential_savings': len(optimizations) * 0.1  # Estimate 10% savings per optimization
                }
            
            return {
                'performance_analysis': performance_report,
                'total_optimizations': sum(len(p['optimizations']) for p in performance_report.values()),
                'recommendation': 'Implement suggested optimizations to improve performance'
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
            
            self.agent = create_openai_functions_agent(llm=self.llm, tools=self.tools, prompt=prompt)
            
            # Run the agent
            response = self.agent_executor.invoke({
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
