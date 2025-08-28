import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

def main():
    st.set_page_config(
        page_title="Simple Data Validation App",
        page_icon="🔍",
        layout="wide"
    )
    
    st.title("🔍 Simple Data Validation App")
    st.markdown("Upload your data and get instant validation insights")
    
    # File upload
    uploaded_file = st.file_uploader(
        "Choose a CSV file", 
        type=['csv'],
        help="Upload a CSV file to validate"
    )
    
    if uploaded_file is not None:
        try:
            # Load data
            df = pd.read_csv(uploaded_file)
            st.success(f"✅ Successfully loaded {len(df)} rows and {len(df.columns)} columns")
            
            # Show basic info
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Rows", len(df))
            with col2:
                st.metric("Total Columns", len(df.columns))
            with col3:
                st.metric("Missing Values", df.isnull().sum().sum())
            
            # Data preview
            st.subheader("📊 Data Preview")
            st.dataframe(df.head())
            
            # Basic validation
            st.subheader("🔍 Data Quality Analysis")
            
            # Missing data analysis
            missing_data = df.isnull().sum()
            if missing_data.sum() > 0:
                st.write("**Missing Data Analysis:**")
                fig = px.bar(
                    x=missing_data.index, 
                    y=missing_data.values,
                    title="Missing Values by Column"
                )
                st.plotly_chart(fig)
            else:
                st.success("✅ No missing data found!")
            
            # Data types
            st.write("**Data Types:**")
            dtype_df = pd.DataFrame({
                'Column': df.columns,
                'Data Type': df.dtypes.astype(str),
                'Unique Values': [df[col].nunique() for col in df.columns]
            })
            st.dataframe(dtype_df)
            
            # Numerical columns analysis
            numerical_cols = df.select_dtypes(include=[np.number]).columns
            if len(numerical_cols) > 0:
                st.subheader("📈 Numerical Data Analysis")
                
                # Outlier detection
                st.write("**Outlier Detection (using Isolation Forest):**")
                
                for col in numerical_cols[:3]:  # Limit to first 3 columns
                    col_data = df[col].dropna()
                    if len(col_data) > 10:
                        try:
                            # Prepare data for outlier detection
                            data_reshaped = col_data.values.reshape(-1, 1)
                            scaler = StandardScaler()
                            scaled_data = scaler.fit_transform(data_reshaped)
                            
                            # Detect outliers
                            iso_forest = IsolationForest(contamination=0.1, random_state=42)
                            outlier_labels = iso_forest.fit_predict(scaled_data)
                            outliers = col_data[outlier_labels == -1]
                            
                            if len(outliers) > 0:
                                st.warning(f"⚠️ **{col}**: {len(outliers)} outliers detected")
                                st.write(f"Outlier values: {outliers.head().tolist()}")
                            else:
                                st.success(f"✅ **{col}**: No outliers detected")
                        except Exception as e:
                            st.error(f"❌ Could not analyze {col}: {str(e)}")
                
                # Distribution plots
                if len(numerical_cols) > 0:
                    selected_col = st.selectbox("Select column for distribution plot:", numerical_cols)
                    if selected_col:
                        fig = px.histogram(df, x=selected_col, title=f"Distribution of {selected_col}")
                        st.plotly_chart(fig)
            
            # Summary statistics
            st.subheader("📋 Summary Statistics")
            st.dataframe(df.describe())
            
        except Exception as e:
            st.error(f"❌ Error loading file: {str(e)}")
            st.exception(e)
    
    else:
        st.info("👆 Please upload a CSV file to get started")
        
        # Sample data for demo
        if st.button("🎯 Try with Sample Data"):
            # Create sample data
            np.random.seed(42)
            sample_data = pd.DataFrame({
                'age': np.random.normal(35, 10, 1000),
                'salary': np.random.normal(50000, 15000, 1000),
                'experience': np.random.normal(8, 3, 1000),
                'department': np.random.choice(['IT', 'HR', 'Sales', 'Marketing'], 1000),
                'rating': np.random.uniform(1, 5, 1000)
            })
            
            # Add some missing values and outliers
            sample_data.loc[np.random.choice(1000, 50, replace=False), 'age'] = np.nan
            sample_data.loc[np.random.choice(1000, 20, replace=False), 'salary'] = 200000  # Outliers
            
            # Save sample data
            sample_data.to_csv('sample_data.csv', index=False)
            
            st.success("✅ Sample data created! Upload 'sample_data.csv' to see the app in action")
            st.dataframe(sample_data.head())

if __name__ == "__main__":
    main()
