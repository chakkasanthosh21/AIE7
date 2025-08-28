# 🤖 AI-Powered Data Validation App

A comprehensive data validation application that combines traditional statistical validation with **AI-powered intelligent analysis** using LangChain and OpenAI.

## 🚀 Features

### **AI-Powered Validation (NEW!)**
- **🤖 Intelligent Data Quality Analysis**: AI-driven assessment of data quality with scoring
- **🧠 Business Logic Validation**: AI-generated business rules and validation strategies
- **🔍 Semantic Consistency Analysis**: AI-powered column mapping and data lineage insights
- **📊 Risk Assessment**: AI-generated risk levels and recommendations

### **Traditional Validation (10 Types)**
1. **Row Count Validation** - Ensure record counts match between source and target
2. **Column/Data Type Validation** - Verify data type consistency across datasets
3. **Null/Not Null Validation** - Check constraint violations and data integrity
4. **Primary Key / Unique Key Validation** - Detect duplicate and missing key records
5. **Data Completeness Validation** - Identify truncation risks and missing data
6. **Data Accuracy / Value Comparison** - Statistical comparison of numerical values
7. **Business Rule Validation** - Enforce domain-specific validation rules
8. **Data Format & Standardization** - Detect formatting inconsistencies
9. **Referential Integrity Validation** - AI-enhanced foreign key relationship analysis
10. **Performance & Accessibility Validation** - AI-powered performance assessment

## 🛠️ Installation

1. **Clone the repository**:
   ```bash
   git clone <your-repo-url>
   cd data_validation_app
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up AI validation** (Optional but recommended):
   ```bash
   # Create .env file
   echo "OPENAI_API_KEY=your-actual-api-key-here" > .env
   
   # Get your API key from: https://platform.openai.com/api-keys
   ```

## 🚀 Usage

### **Start the App**:
```bash
streamlit run app/main.py
```

### **Access the App**:
- **Local URL**: `http://localhost:8501`
- **Network URL**: Available for other devices on your network

### **Using AI Validation**:
1. **Upload two CSV files** (source and target datasets)
2. **Set your OpenAI API key** in the `.env` file
3. **Click "Run AI-Powered Validation"**
4. **View AI insights** in the highlighted sections

## 🤖 AI Validation Features

### **Data Quality Analysis**
- Overall quality score (0-100)
- Critical issues identification
- Data integrity concerns
- Risk assessment (LOW/MEDIUM/HIGH)
- AI-generated recommendations

### **Business Logic Intelligence**
- Automated business rule suggestions
- Data quality pattern detection
- Anomaly detection rules
- Validation threshold optimization

### **Semantic Consistency**
- Column mapping suggestions
- Data lineage analysis
- Quality insights generation
- Consistency scoring

## 📊 Sample Data

The app includes a **"Generate Sample Data"** button that creates:
- `sample_source.csv` (1000 rows, 7 columns)
- `sample_target.csv` (1000 rows, 6 columns) with intentional validation issues

Perfect for testing AI validation capabilities!

## 🔧 Configuration

### **Environment Variables**:
```bash
OPENAI_API_KEY=your-openai-api-key-here
OPENAI_MODEL=gpt-3.5-turbo          # Optional
OPENAI_TEMPERATURE=0.1               # Optional
```

### **AI Model Settings**:
- **Default Model**: GPT-3.5-turbo
- **Temperature**: 0.1 (for consistent results)
- **Response Format**: Structured JSON for parsing

## 🏗️ Architecture

### **Core Components**:
- **`DataValidator`**: Traditional validation engine
- **`AIDataValidator`**: AI-powered validation using LangChain
- **Streamlit UI**: Interactive web interface
- **OpenAI Integration**: GPT models for intelligent analysis

### **Validation Flow**:
1. **Data Loading** → CSV parsing and validation
2. **Traditional Validation** → Statistical and rule-based checks
3. **AI Validation** → LLM-powered intelligent analysis
4. **Results Display** → Interactive reports with AI insights

## 🎯 Use Cases

- **Data Migration Validation**: Ensure data integrity during system migrations
- **ETL Pipeline Testing**: Validate data transformation processes
- **Data Quality Assessment**: AI-powered quality scoring and recommendations
- **Compliance Checking**: Automated business rule validation
- **Data Lineage Analysis**: AI-enhanced relationship mapping

## 🔮 Future Enhancements

- **Ragas Integration**: Advanced evaluation framework
- **Custom AI Models**: Support for other LLM providers
- **Batch Processing**: Handle multiple dataset comparisons
- **Real-time Monitoring**: Continuous validation pipelines
- **Advanced Visualizations**: Interactive AI insights dashboard

## 📝 Requirements

- Python 3.8+
- Streamlit 1.28+
- OpenAI API key (for AI validation)
- See `requirements.txt` for full dependency list

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Implement your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

**🚀 Ready to validate your data with AI intelligence? Start the app and experience the future of data validation!**
