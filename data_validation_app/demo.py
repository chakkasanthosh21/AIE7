#!/usr/bin/env python3
"""
Demo script for the AI-Powered Data Validation App.
This script demonstrates the core functionality without requiring the web interface.
"""

import pandas as pd
import asyncio
from pathlib import Path
import sys

# Add the app directory to the Python path
sys.path.append(str(Path(__file__).parent))

from app.validation_engine import DataValidationEngine
from data.sample_data import create_all_sample_data


def run_demo():
    """Run a comprehensive demo of the validation app."""
    
    print("🚀 AI-Powered Data Validation App Demo")
    print("=" * 50)
    
    # Step 1: Create sample data
    print("\n📊 Step 1: Creating sample data...")
    sample_data = create_all_sample_data()
    
    # Step 2: Initialize validation engine
    print("\n🤖 Step 2: Initializing AI validation engine...")
    validation_engine = DataValidationEngine()
    
    # Step 3: Run validation scenarios
    print("\n🔍 Step 3: Running validation scenarios...")
    
    # Scenario 1: Consistent data sources
    print("\n--- Scenario 1: Consistent Data Sources ---")
    consistent_sources = {
        "users": sample_data["users"],
        "orders": sample_data["orders"],
        "products": sample_data["products"]
    }
    
    print("Validating consistent data sources...")
    result1 = validation_engine.validate_data_sources_sync(consistent_sources)
    display_validation_results("Consistent Data Sources", result1)
    
    # Scenario 2: Inconsistent schemas
    print("\n--- Scenario 2: Inconsistent Schemas ---")
    inconsistent_sources = {
        "users": sample_data["users"],
        "inconsistent_users": sample_data["inconsistent_users"]
    }
    
    print("Validating inconsistent schemas...")
    result2 = validation_engine.validate_data_sources_sync(inconsistent_sources)
    display_validation_results("Inconsistent Schemas", result2)
    
    # Scenario 3: Low quality data
    print("\n--- Scenario 3: Low Quality Data ---")
    quality_sources = {
        "users": sample_data["users"],
        "low_quality_users": sample_data["low_quality_users"]
    }
    
    print("Validating data quality...")
    result3 = validation_engine.validate_data_sources_sync(quality_sources)
    display_validation_results("Data Quality Analysis", result3)
    
    # Summary
    print("\n" + "=" * 50)
    print("🎯 Demo Summary")
    print("=" * 50)
    print(f"✅ Total scenarios tested: 3")
    print(f"🔍 Schema conflicts detected: {sum(1 for r in [result1, result2, result3] if r.schema_analysis.get('has_conflicts', False))}")
    print(f"⚠️ Quality issues found: {sum(len(r.errors) for r in [result1, result2, result3])}")
    print(f"💡 Total recommendations: {sum(len(r.recommendations) for r in [result1, result2, result3])}")
    
    print("\n🚀 Demo completed! The app is ready for production use.")
    print("💡 Try running 'uv run streamlit run app/main.py' to start the web interface.")


def display_validation_results(scenario_name: str, result):
    """Display validation results in a formatted way."""
    
    print(f"\n📊 Results for: {scenario_name}")
    print("-" * 40)
    
    # Schema analysis
    if result.schema_analysis:
        schema = result.schema_analysis
        if schema.get('has_conflicts'):
            print(f"❌ Schema conflicts: {len(schema.get('conflicts', []))}")
            for conflict in schema.get('conflicts', [])[:3]:  # Show first 3
                print(f"   - {conflict}")
        else:
            print("✅ No schema conflicts detected")
    
    # Quality metrics
    if result.quality_metrics:
        quality = result.quality_metrics
        print(f"📈 Quality metrics:")
        print(f"   - Completeness: {quality.get('completeness', 0):.1%}")
        print(f"   - Consistency: {quality.get('consistency', 0):.1%}")
        print(f"   - Uniqueness: {quality.get('uniqueness', 0):.1%}")
        print(f"   - Validity: {quality.get('validity', 0):.1%}")
        print(f"   - Overall: {quality.get('average_score', 0):.1%}")
    
    # Errors
    if result.errors:
        print(f"⚠️ Issues found: {len(result.errors)}")
        for error in result.errors[:3]:  # Show first 3
            print(f"   - {error}")
    
    # Recommendations
    if result.recommendations:
        print(f"💡 Recommendations: {len(result.recommendations)}")
        for rec in result.recommendations[:3]:  # Show first 3
            print(f"   - {rec}")


def run_async_demo():
    """Run the demo using async validation."""
    
    async def async_validation():
        print("🚀 Running async validation demo...")
        
        # Create sample data
        sample_data = create_all_sample_data()
        
        # Initialize engine
        validation_engine = DataValidationEngine()
        
        # Run validation
        consistent_sources = {
            "users": sample_data["users"],
            "orders": sample_data["orders"]
        }
        
        result = await validation_engine.validate_data_sources(consistent_sources)
        display_validation_results("Async Validation", result)
    
    # Run async demo
    asyncio.run(async_validation())


if __name__ == "__main__":
    try:
        # Check if OpenAI API key is set
        import os
        if not os.getenv("OPENAI_API_KEY"):
            print("⚠️  Warning: OPENAI_API_KEY not set. Some features may not work.")
            print("💡 Set your OpenAI API key: export OPENAI_API_KEY='your-key-here'")
        
        # Run the demo
        run_demo()
        
        # Optionally run async demo
        print("\n" + "=" * 50)
        print("🔄 Running async validation demo...")
        run_async_demo()
        
    except KeyboardInterrupt:
        print("\n\n⏹️  Demo interrupted by user")
    except Exception as e:
        print(f"\n❌ Error running demo: {str(e)}")
        print("💡 Make sure all dependencies are installed: uv sync")
