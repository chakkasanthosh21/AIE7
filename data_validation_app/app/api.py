"""FastAPI backend for the Data Validation App."""

from fastapi import FastAPI, File, UploadFile, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Dict, List, Any, Optional
import pandas as pd
import json
import io
from pathlib import Path

from validation_engine import DataValidationEngine, ValidationState
from config.settings import settings

# Initialize FastAPI app
app = FastAPI(
    title="AI Data Validation API",
    description="API for AI-powered data validation and quality analysis",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize validation engine
validation_engine = DataValidationEngine()


# Pydantic models for API requests/responses
class ValidationRequest(BaseModel):
    """Request model for validation."""
    data_sources: Dict[str, Any]
    validation_options: Optional[Dict[str, bool]] = None


class ValidationResponse(BaseModel):
    """Response model for validation results."""
    success: bool
    message: str
    results: Optional[ValidationState] = None
    errors: Optional[List[str]] = None


class HealthResponse(BaseModel):
    """Health check response."""
    status: str
    version: str
    timestamp: str


@app.get("/", response_model=HealthResponse)
async def root():
    """Root endpoint with health information."""
    return HealthResponse(
        status="healthy",
        version="1.0.0",
        timestamp=pd.Timestamp.now().isoformat()
    )


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return HealthResponse(
        status="healthy",
        version="1.0.0",
        timestamp=pd.Timestamp.now().isoformat()
    )


@app.post("/api/validate", response_model=ValidationResponse)
async def validate_data(request: ValidationRequest):
    """Validate multiple data sources."""
    try:
        # Convert data sources to DataFrames
        data_sources = {}
        for name, data in request.data_sources.items():
            if isinstance(data, list):
                # JSON data
                df = pd.DataFrame(data)
            elif isinstance(data, str):
                # CSV string
                df = pd.read_csv(io.StringIO(data))
            else:
                raise ValueError(f"Unsupported data format for {name}")
            
            data_sources[name] = df
        
        # Run validation
        validation_result = await validation_engine.validate_data_sources(data_sources)
        
        return ValidationResponse(
            success=True,
            message="Validation completed successfully",
            results=validation_result
        )
        
    except Exception as e:
        return ValidationResponse(
            success=False,
            message=f"Validation failed: {str(e)}",
            errors=[str(e)]
        )


@app.post("/api/validate/upload")
async def validate_uploaded_files(
    files: List[UploadFile] = File(...),
    validation_options: Optional[str] = None
):
    """Validate uploaded files."""
    try:
        if not files:
            raise HTTPException(status_code=400, detail="No files uploaded")
        
        # Parse validation options
        options = {}
        if validation_options:
            try:
                options = json.loads(validation_options)
            except json.JSONDecodeError:
                options = {}
        
        # Load data from files
        data_sources = {}
        for file in files:
            if file.filename:
                try:
                    content = await file.read()
                    
                    if file.filename.endswith('.csv'):
                        df = pd.read_csv(io.BytesIO(content))
                    elif file.filename.endswith('.json'):
                        df = pd.read_json(io.BytesIO(content))
                    elif file.filename.endswith(('.xlsx', '.xls')):
                        df = pd.read_excel(io.BytesIO(content))
                    elif file.filename.endswith('.parquet'):
                        df = pd.read_parquet(io.BytesIO(content))
                    else:
                        continue
                    
                    data_sources[file.filename] = df
                    
                except Exception as e:
                    raise HTTPException(
                        status_code=400, 
                        detail=f"Error processing {file.filename}: {str(e)}"
                    )
        
        if not data_sources:
            raise HTTPException(status_code=400, detail="No valid data files found")
        
        # Run validation
        validation_result = await validation_engine.validate_data_sources(data_sources)
        
        # Convert to serializable format
        result_dict = {
            "data_sources": {name: df.shape for name, df in data_sources.items()},
            "validation_results": validation_result.validation_results,
            "schema_analysis": validation_result.schema_analysis,
            "quality_metrics": validation_result.quality_metrics,
            "recommendations": validation_result.recommendations,
            "errors": validation_result.errors,
            "current_step": validation_result.current_step
        }
        
        return JSONResponse(content={
            "success": True,
            "message": "Validation completed successfully",
            "results": result_dict
        })
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@app.get("/api/supported-formats")
async def get_supported_formats():
    """Get list of supported file formats."""
    return {
        "supported_formats": settings.supported_formats,
        "max_file_size_mb": settings.max_file_size_mb
    }


@app.get("/api/validation-metrics")
async def get_validation_metrics():
    """Get available validation metrics."""
    return {
        "ragas_metrics": settings.ragas_metrics,
        "quality_metrics": ["completeness", "consistency", "uniqueness", "validity"]
    }


@app.post("/api/validate/schema")
async def validate_schema_only(request: ValidationRequest):
    """Validate only schema consistency."""
    try:
        # Convert data sources to DataFrames
        data_sources = {}
        for name, data in request.data_sources.items():
            if isinstance(data, list):
                df = pd.DataFrame(data)
            elif isinstance(data, str):
                df = pd.read_csv(io.StringIO(data))
            else:
                raise ValueError(f"Unsupported data format for {name}")
            
            data_sources[name] = df
        
        # Create validation state
        initial_state = ValidationState(
            data_sources=data_sources,
            validation_results={},
            schema_analysis={},
            quality_metrics={},
            recommendations=[],
            errors=[]
        )
        
        # Run only schema validation
        from validation_engine import SchemaValidator
        schema_validator = SchemaValidator()
        result = schema_validator.validate_schema(initial_state)
        
        return ValidationResponse(
            success=True,
            message="Schema validation completed",
            results=result
        )
        
    except Exception as e:
        return ValidationResponse(
            success=False,
            message=f"Schema validation failed: {str(e)}",
            errors=[str(e)]
        )


@app.post("/api/validate/quality")
async def validate_quality_only(request: ValidationRequest):
    """Validate only data quality."""
    try:
        # Convert data sources to DataFrames
        data_sources = {}
        for name, data in request.data_sources.items():
            if isinstance(data, list):
                df = pd.DataFrame(data)
            elif isinstance(data, str):
                df = pd.read_csv(io.StringIO(data))
            else:
                raise ValueError(f"Unsupported data format for {name}")
            
            data_sources[name] = df
        
        # Create validation state
        initial_state = ValidationState(
            data_sources=data_sources,
            validation_results={},
            schema_analysis={},
            quality_metrics={},
            recommendations=[],
            errors=[]
        )
        
        # Run only quality analysis
        from validation_engine import DataQualityAnalyzer
        quality_analyzer = DataQualityAnalyzer()
        result = quality_analyzer.analyze_quality(initial_state)
        
        return ValidationResponse(
            success=True,
            message="Quality analysis completed",
            results=result
        )
        
    except Exception as e:
        return ValidationResponse(
            success=False,
            message=f"Quality analysis failed: {str(e)}",
            errors=[str(e)]
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "api:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug
    )
