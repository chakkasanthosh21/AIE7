# 🚀 Quick Start Guide - AI Data Validation App

## Prerequisites

- Python 3.9+
- OpenAI API key
- UV package manager (recommended) or pip

## Installation

1. **Clone and navigate to the project:**
   ```bash
   cd data_validation_app
   ```

2. **Install dependencies:**
   ```bash
   uv sync
   # or with pip: pip install -r requirements.txt
   ```

3. **Set up environment variables:**
   ```bash
   cp env_template.txt .env
   # Edit .env and add your OpenAI API key
   export OPENAI_API_KEY="your-api-key-here"
   ```

## Running the App

### Option 1: Streamlit Web Interface (Recommended)
```bash
uv run streamlit run app/main.py
```
Open http://localhost:8501 in your browser

### Option 2: FastAPI Backend
```bash
uv run uvicorn app.api:app --reload
```
API available at http://localhost:8000

### Option 3: Command Line Demo
```bash
uv run python demo.py
```

## Docker Deployment

1. **Build and run with Docker Compose:**
   ```bash
   docker-compose up --build
   ```

2. **Or build manually:**
   ```bash
   docker build -t data-validation-app .
   docker run -p 8501:8501 -p 8000:8000 data-validation-app
   ```

## Usage

1. **Upload Data Files:**
   - Supported formats: CSV, JSON, Excel, Parquet
   - Multiple files can be uploaded simultaneously

2. **Run Validation:**
   - Click "Run Validation" to start AI-powered analysis
   - Review results in organized tabs

3. **View Results:**
   - Schema Analysis: Column mismatches and type conflicts
   - Quality Metrics: Completeness, consistency, uniqueness
   - Issues & Errors: Detailed problem descriptions
   - Recommendations: AI-generated improvement suggestions

## Sample Data

The app includes sample datasets for testing:
- `sample_users.csv` - Clean user data
- `sample_orders.csv` - Order information
- `inconsistent_users.csv` - Schema conflicts
- `low_quality_users.csv` - Data quality issues

## API Endpoints

- `GET /` - Health check
- `POST /api/validate` - Validate data sources
- `POST /api/validate/upload` - Validate uploaded files
- `GET /api/supported-formats` - List supported formats
- `GET /api/validation-metrics` - Available metrics

## Configuration

Edit `config/settings.py` or set environment variables:
- `OPENAI_MODEL` - LLM model to use
- `MAX_FILE_SIZE_MB` - Maximum file size
- `SUPPORTED_FORMATS` - File format support

## Troubleshooting

- **Import errors:** Ensure `uv sync` completed successfully
- **API key issues:** Check your `.env` file and environment variables
- **File upload errors:** Verify file format and size limits
- **Performance issues:** Consider using Docker for production deployment

## Next Steps

- Customize validation rules in `validation_engine.py`
- Add new data quality metrics
- Integrate with your existing data pipelines
- Set up automated validation workflows

## Support

For issues and questions:
1. Check the logs for error details
2. Verify your environment configuration
3. Test with sample data first
4. Review the validation engine code

Happy validating! 🔍✨
