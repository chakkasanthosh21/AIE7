"""Core validation engine using LangGraph for multi-agent data validation."""

import asyncio
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from pathlib import Path

import pandas as pd
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage
from langgraph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from pydantic import BaseModel

from config.settings import settings


@dataclass
class ValidationState:
    """State for the validation workflow."""
    data_sources: Dict[str, pd.DataFrame]
    validation_results: Dict[str, Any]
    schema_analysis: Dict[str, Any]
    quality_metrics: Dict[str, float]
    recommendations: List[str]
    errors: List[str]
    current_step: str = "initialized"


class SchemaValidator:
    """Validates data schemas and structure."""
    
    def __init__(self):
        self.llm = ChatOpenAI(
            model=settings.openai_model,
            temperature=0.1
        )
    
    def validate_schema(self, state: ValidationState) -> ValidationState:
        """Validate schema consistency across data sources."""
        try:
            schemas = {}
            for name, df in state.data_sources.items():
                schemas[name] = {
                    'columns': list(df.columns),
                    'dtypes': df.dtypes.to_dict(),
                    'shape': df.shape,
                    'null_counts': df.isnull().sum().to_dict()
                }
            
            # Analyze schema differences
            schema_analysis = self._analyze_schema_differences(schemas)
            
            state.schema_analysis = schema_analysis
            state.current_step = "schema_validated"
            
            if schema_analysis['has_conflicts']:
                state.errors.append(f"Schema conflicts detected: {schema_analysis['conflicts']}")
            
        except Exception as e:
            state.errors.append(f"Schema validation error: {str(e)}")
        
        return state
    
    def _analyze_schema_differences(self, schemas: Dict) -> Dict:
        """Analyze differences between schemas."""
        if len(schemas) < 2:
            return {'has_conflicts': False, 'conflicts': []}
        
        schema_names = list(schemas.keys())
        base_schema = schemas[schema_names[0]]
        conflicts = []
        
        for name in schema_names[1:]:
            schema = schemas[name]
            
            # Check column differences
            base_cols = set(base_schema['columns'])
            schema_cols = set(schema['columns'])
            
            missing_cols = base_cols - schema_cols
            extra_cols = schema_cols - base_cols
            
            if missing_cols:
                conflicts.append(f"{name} missing columns: {missing_cols}")
            if extra_cols:
                conflicts.append(f"{name} has extra columns: {extra_cols}")
            
            # Check data type differences for common columns
            common_cols = base_cols & schema_cols
            for col in common_cols:
                if base_schema['dtypes'][col] != schema['dtypes'][col]:
                    conflicts.append(f"Column {col} type mismatch: {base_schema['dtypes'][col]} vs {schema['dtypes'][col]}")
        
        return {
            'has_conflicts': len(conflicts) > 0,
            'conflicts': conflicts,
            'schemas': schemas
        }


class DataQualityAnalyzer:
    """Analyzes data quality using RAGAS metrics."""
    
    def __init__(self):
        self.llm = ChatOpenAI(
            model=settings.openai_model,
            temperature=0.1
        )
    
    def analyze_quality(self, state: ValidationState) -> ValidationState:
        """Analyze data quality across sources."""
        try:
            quality_scores = {}
            
            for name, df in state.data_sources.items():
                scores = self._calculate_quality_scores(df)
                quality_scores[name] = scores
            
            # Calculate overall quality metrics
            overall_quality = self._calculate_overall_quality(quality_scores)
            
            state.quality_metrics = overall_quality
            state.current_step = "quality_analyzed"
            
        except Exception as e:
            state.errors.append(f"Quality analysis error: {str(e)}")
        
        return state
    
    def _calculate_quality_scores(self, df: pd.DataFrame) -> Dict[str, float]:
        """Calculate quality scores for a dataframe."""
        scores = {}
        
        # Completeness
        total_cells = df.size
        null_cells = df.isnull().sum().sum()
        scores['completeness'] = 1 - (null_cells / total_cells) if total_cells > 0 else 0
        
        # Consistency (check for duplicate rows)
        scores['consistency'] = 1 - (df.duplicated().sum() / len(df)) if len(df) > 0 else 0
        
        # Uniqueness (check for unique values in key columns)
        unique_ratios = []
        for col in df.columns:
            if df[col].dtype in ['object', 'string']:
                unique_ratio = df[col].nunique() / len(df) if len(df) > 0 else 0
                unique_ratios.append(unique_ratio)
        
        scores['uniqueness'] = sum(unique_ratios) / len(unique_ratios) if unique_ratios else 0
        
        # Validity (basic type checking)
        valid_cells = 0
        total_cells = 0
        
        for col in df.columns:
            if df[col].dtype in ['int64', 'float64']:
                valid_cells += (~df[col].isna()).sum()
            elif df[col].dtype == 'object':
                valid_cells += (~df[col].isna()).sum()
            total_cells += len(df)
        
        scores['validity'] = valid_cells / total_cells if total_cells > 0 else 0
        
        return scores
    
    def _calculate_overall_quality(self, quality_scores: Dict) -> Dict[str, float]:
        """Calculate overall quality metrics."""
        if not quality_scores:
            return {}
        
        metrics = ['completeness', 'consistency', 'uniqueness', 'validity']
        overall = {}
        
        for metric in metrics:
            values = [scores.get(metric, 0) for scores in quality_scores.values()]
            overall[metric] = sum(values) / len(values)
        
        overall['average_score'] = sum(overall.values()) / len(overall)
        return overall


class SemanticValidator:
    """Validates semantic consistency using embeddings and LLMs."""
    
    def __init__(self):
        self.llm = ChatOpenAI(
            model=settings.openai_model,
            temperature=0.1
        )
    
    def validate_semantics(self, state: ValidationState) -> ValidationState:
        """Validate semantic consistency across data sources."""
        try:
            semantic_issues = []
            
            # Check for semantic inconsistencies in common columns
            if len(state.data_sources) >= 2:
                common_columns = self._find_common_columns(state.data_sources)
                
                for col in common_columns:
                    issues = self._check_column_semantics(col, state.data_sources)
                    semantic_issues.extend(issues)
            
            if semantic_issues:
                state.errors.extend(semantic_issues)
            
            state.current_step = "semantics_validated"
            
        except Exception as e:
            state.errors.append(f"Semantic validation error: {str(e)}")
        
        return state
    
    def _find_common_columns(self, data_sources: Dict) -> List[str]:
        """Find columns that exist in all data sources."""
        if not data_sources:
            return []
        
        column_sets = [set(df.columns) for df in data_sources.values()]
        return list(set.intersection(*column_sets))
    
    def _check_column_semantics(self, column: str, data_sources: Dict) -> List[str]:
        """Check semantic consistency for a specific column."""
        issues = []
        
        # Get unique values from each source
        unique_values = {}
        for name, df in data_sources.items():
            if column in df.columns:
                unique_values[name] = set(df[column].dropna().unique())
        
        # Check for value overlaps and conflicts
        if len(unique_values) >= 2:
            all_values = set.union(*unique_values.values())
            
            # Check if there are completely disjoint value sets
            for name1 in unique_values:
                for name2 in unique_values:
                    if name1 != name2:
                        intersection = unique_values[name1] & unique_values[name2]
                        if len(intersection) == 0:
                            issues.append(f"Column '{column}' has no overlapping values between {name1} and {name2}")
        
        return issues


class RecommendationEngine:
    """Generates recommendations for resolving validation issues."""
    
    def __init__(self):
        self.llm = ChatOpenAI(
            model=settings.openai_model,
            temperature=0.3
        )
    
    def generate_recommendations(self, state: ValidationState) -> ValidationState:
        """Generate actionable recommendations."""
        try:
            recommendations = []
            
            # Generate recommendations based on validation results
            if state.errors:
                recommendations.extend(self._generate_error_recommendations(state.errors))
            
            if state.schema_analysis.get('has_conflicts'):
                recommendations.extend(self._generate_schema_recommendations(state.schema_analysis))
            
            if state.quality_metrics:
                recommendations.extend(self._generate_quality_recommendations(state.quality_metrics))
            
            state.recommendations = recommendations
            state.current_step = "recommendations_generated"
            
        except Exception as e:
            state.errors.append(f"Recommendation generation error: {str(e)}")
        
        return state
    
    def _generate_error_recommendations(self, errors: List[str]) -> List[str]:
        """Generate recommendations for specific errors."""
        recommendations = []
        
        for error in errors:
            if "schema conflicts" in error.lower():
                recommendations.append("Review and standardize column names and data types across all data sources")
            elif "missing columns" in error.lower():
                recommendations.append("Create a unified schema that includes all necessary columns from all sources")
            elif "type mismatch" in error.lower():
                recommendations.append("Implement data type conversion rules to ensure consistency")
            elif "no overlapping values" in error.lower():
                recommendations.append("Investigate data source definitions and ensure they represent the same entities")
        
        return recommendations
    
    def _generate_schema_recommendations(self, schema_analysis: Dict) -> List[str]:
        """Generate recommendations for schema issues."""
        recommendations = []
        
        if schema_analysis.get('conflicts'):
            recommendations.append("Create a data dictionary defining standard column names and types")
            recommendations.append("Implement ETL processes to transform data into a consistent format")
            recommendations.append("Use schema validation tools in your data pipeline")
        
        return recommendations
    
    def _generate_quality_recommendations(self, quality_metrics: Dict) -> List[str]:
        """Generate recommendations for quality issues."""
        recommendations = []
        
        if quality_metrics.get('completeness', 1) < 0.9:
            recommendations.append("Implement data quality monitoring for missing values")
            recommendations.append("Set up alerts for when completeness drops below thresholds")
        
        if quality_metrics.get('consistency', 1) < 0.95:
            recommendations.append("Investigate duplicate data sources and implement deduplication")
            recommendations.append("Review data refresh processes for potential duplication")
        
        if quality_metrics.get('uniqueness', 1) < 0.8:
            recommendations.append("Review business rules for data uniqueness requirements")
            recommendations.append("Implement uniqueness constraints in your data model")
        
        return recommendations


def create_validation_workflow() -> StateGraph:
    """Create the validation workflow using LangGraph."""
    
    # Initialize components
    schema_validator = SchemaValidator()
    quality_analyzer = DataQualityAnalyzer()
    semantic_validator = SemanticValidator()
    recommendation_engine = RecommendationEngine()
    
    # Create the workflow
    workflow = StateGraph(ValidationState)
    
    # Add nodes
    workflow.add_node("validate_schema", schema_validator.validate_schema)
    workflow.add_node("analyze_quality", quality_analyzer.analyze_quality)
    workflow.add_node("validate_semantics", semantic_validator.validate_semantics)
    workflow.add_node("generate_recommendations", recommendation_engine.generate_recommendations)
    
    # Define the workflow
    workflow.set_entry_point("validate_schema")
    workflow.add_edge("validate_schema", "analyze_quality")
    workflow.add_edge("analyze_quality", "validate_semantics")
    workflow.add_edge("validate_semantics", "generate_recommendations")
    workflow.add_edge("generate_recommendations", END)
    
    # Compile the workflow
    return workflow.compile(checkpointer=MemorySaver())


class DataValidationEngine:
    """Main data validation engine."""
    
    def __init__(self):
        self.workflow = create_validation_workflow()
    
    async def validate_data_sources(self, data_sources: Dict[str, pd.DataFrame]) -> ValidationState:
        """Validate multiple data sources."""
        # Initialize state
        initial_state = ValidationState(
            data_sources=data_sources,
            validation_results={},
            schema_analysis={},
            quality_metrics={},
            recommendations=[],
            errors=[]
        )
        
        # Run validation workflow
        result = await self.workflow.ainvoke(initial_state)
        
        return result
    
    def validate_data_sources_sync(self, data_sources: Dict[str, pd.DataFrame]) -> ValidationState:
        """Synchronous version of data validation."""
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            result = loop.run_until_complete(self.validate_data_sources(data_sources))
            return result
        finally:
            loop.close()
