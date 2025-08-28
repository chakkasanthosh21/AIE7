# 🔍 Simple Data Validation App

A clean, working data validation application built with Streamlit that provides instant insights into your data quality.

## ✨ Features

- **File Upload**: Upload CSV files for validation
- **Data Quality Analysis**: Missing data detection and analysis
- **Outlier Detection**: Machine learning-based anomaly detection
- **Interactive Visualizations**: Charts and plots for data insights
- **Sample Data**: Built-in sample data for testing

## 🚀 Quick Start

### Installation

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the app**
   ```bash
   streamlit run app/main.py
   ```

3. **Open your browser**
   Navigate to `http://localhost:8501`

## 📊 What It Does

- **Data Overview**: Shows total rows, columns, and missing values
- **Missing Data Analysis**: Visualizes missing data patterns
- **Data Type Information**: Displays column types and unique value counts
- **Outlier Detection**: Uses Isolation Forest to find anomalies
- **Distribution Plots**: Interactive histograms for numerical columns
- **Summary Statistics**: Comprehensive statistical overview

## 🎯 Use Cases

- **Data Quality Assessment**: Quick validation of datasets
- **Data Exploration**: Understanding data structure and patterns
- **Anomaly Detection**: Finding unusual data points
- **Data Profiling**: Getting insights before analysis

## 🛠️ Built With

- **Streamlit**: Web interface
- **Pandas**: Data manipulation
- **Scikit-learn**: Machine learning (outlier detection)
- **Plotly**: Interactive visualizations

## 📁 Project Structure

```
data_validation_app/
├── app/
│   └── main.py              # Main application
├── requirements.txt          # Python dependencies
└── README.md                # This file
```

---

**Simple, Clean, Working** - This app focuses on core functionality without complexity.
