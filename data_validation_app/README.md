# 🔍 Comprehensive Data Validation App

A powerful data validation application that compares two datasets and performs comprehensive validation across 10 critical validation types. Built with Streamlit and incorporating concepts from LangChain, RAG, and evaluation frameworks.

## ✨ Features

### 🔍 **10 Comprehensive Validation Types**

1. **Row Count Validation** - Ensures source and target record counts match
2. **Column/Data Type Validation** - Verifies data type consistency across datasets
3. **Null/Not Null Validation** - Checks constraint violations and data integrity
4. **Primary Key / Unique Key Validation** - Detects duplicate or missing key records
5. **Data Completeness Validation** - Identifies potential data truncation risks
6. **Data Accuracy / Value Comparison** - Statistical comparison of numeric values
7. **Business Rule Validation** - Validates computed columns against business logic
8. **Data Format & Standardization** - Checks formatting consistency and mixed types
9. **Referential Integrity** - Validates foreign key relationships (planned)
10. **Performance & Accessibility** - Index and configuration validation (planned)

### 🚀 **Advanced Capabilities**

- **Dual File Upload**: Compare source vs target datasets
- **Interactive Visualizations**: Charts and metrics for validation results
- **Sample Data Generation**: Built-in test data with intentional validation issues
- **Comprehensive Reporting**: Detailed status, messages, and metrics for each validation
- **Real-time Processing**: Instant validation results with progress indicators

## 🛠️ Built With

- **Streamlit**: Modern web interface and data visualization
- **Pandas**: Advanced data manipulation and analysis
- **LangChain**: AI agent framework and LLM integration (planned)
- **Ragas**: Evaluation and testing framework (planned)
- **Plotly**: Interactive charts and dashboards
- **Scikit-learn**: Machine learning for outlier detection

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- OpenAI API key (optional, for future AI features)

### Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd data_validation_app
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the app**
   ```bash
   streamlit run app/main.py
   ```

4. **Open your browser**
   Navigate to `http://localhost:8501`

## 📊 How It Works

### **Step 1: Upload Datasets**
- Upload source dataset (original data)
- Upload target dataset (data to validate)
- Set custom names for each dataset

### **Step 2: Run Validation**
- Click "Run Comprehensive Validation"
- App automatically runs all 10 validation types
- Processes both datasets simultaneously

### **Step 3: Review Results**
- **Summary Dashboard**: Total validations, passed, failed, warnings
- **Detailed Results**: Expandable sections for each validation type
- **Status Indicators**: Color-coded PASS/FAIL/WARNING status
- **Actionable Messages**: Clear descriptions of issues found

## 🎯 Use Cases

- **Data Migration Validation**: Ensure data integrity during system migrations
- **ETL Pipeline Testing**: Validate data transformation processes
- **Data Quality Assurance**: Comprehensive quality checks for datasets
- **Compliance Validation**: Meet regulatory data quality requirements
- **Business Intelligence**: Validate data before reporting and analytics
- **Research Data Validation**: Academic and research data quality checks

## 📁 Project Structure

```
data_validation_app/
├── app/
│   └── main.py              # Main validation application
├── requirements.txt          # Python dependencies
├── .gitignore               # Git ignore rules
└── README.md                # This documentation
```

## 🔧 Configuration

### **Business Rules**
The app includes default business rules for common fields:
- **Age**: 0-120 range
- **Salary**: Minimum 0
- **Rating**: 1-5 range

Custom business rules can be configured in the code.

### **Validation Thresholds**
- **Data Accuracy**: 5% difference threshold for numeric comparisons
- **Primary Key Detection**: 90% uniqueness threshold for auto-detection
- **Format Issues**: High variance detection for string lengths

## 🚨 Troubleshooting

### **Common Issues**

1. **File Upload Errors**
   - Ensure files are valid CSV format
   - Check file size limits
   - Verify file encoding (UTF-8 recommended)

2. **Memory Issues**
   - Large datasets may require more RAM
   - Consider sampling for initial validation
   - Use chunked processing for very large files

3. **Validation Failures**
   - Review detailed error messages
   - Check data types and formats
   - Verify business rule configurations

### **Getting Help**

- Check the validation report for detailed status information
- Review error messages in the expandable sections
- Ensure all dependencies are properly installed
- Verify Python version compatibility (3.8+)

## 🔮 Future Enhancements

- **AI-Powered Validation**: LangChain integration for intelligent validation strategies
- **Referential Integrity**: Foreign key relationship validation
- **Performance Metrics**: Index and configuration validation
- **Custom Rules Engine**: User-defined business rule configuration
- **Batch Processing**: Handle multiple dataset pairs
- **Export Reports**: PDF and Excel report generation

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

---

**Professional Data Validation** - Built for enterprise-grade data quality assurance with comprehensive coverage of all critical validation types.
