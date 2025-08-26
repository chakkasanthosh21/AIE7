"""Database connection UI components for Streamlit."""

import streamlit as st
import pandas as pd
from typing import Dict, List, Any
from database_connector import DatabaseConnector
from advanced_semantic_validator import AdvancedSemanticValidator
from advanced_ml_validator import AdvancedMLValidator

def render_database_connections():
    """Render database connection interface."""
    
    # Initialize database connector in session state
    if 'db_connector' not in st.session_state:
        st.session_state.db_connector = DatabaseConnector()
    
    db_connector = st.session_state.db_connector
    
    st.header("🗄️ Database Connections")
    st.markdown("Connect to various databases and cloud storage for data validation.")
    
    # Add comparison section
    st.subheader("🔄 Data Source Comparison")
    st.info("Connect to multiple databases/datasets to compare and validate them together")
    
    # Instructions for multiple connections
    st.markdown("""
    **How to compare multiple datasets:**
    1. **Connect to first database** (e.g., MySQL table 'customers')
    2. **Connect to second database** (e.g., PostgreSQL table 'users') 
    3. **Load data** from both tables
    4. **Run Enhanced Validation** to compare them
    """)
    
    # Show current data sources
    if 'database_data' in st.session_state and st.session_state.database_data:
        st.write("**Current Data Sources:**")
        for source_name, df in st.session_state.database_data.items():
            st.write(f"- {source_name}: {len(df)} rows, {len(df.columns)} columns")
        
        if len(st.session_state.database_data) > 1:
            st.success("✅ Multiple data sources loaded! You can now run validation to compare them.")
            
            # Add Run Enhanced Validation button for multiple sources
            if st.button("🚀 Run Enhanced Validation on Multiple Sources", key="multi_source_validation"):
                st.session_state.run_multi_validation = True
                st.rerun()
    
    # Create tabs for different connection types
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🐬 MySQL", "🐘 PostgreSQL", "🪟 SQL Server", "☁️ Azure Blob", "📊 Active Connections"
    ])
    
    with tab1:
        render_mysql_connection(db_connector)
    
    with tab2:
        render_postgresql_connection(db_connector)
    
    with tab3:
        render_sqlserver_connection(db_connector)
    
    with tab4:
        render_azure_blob_connection(db_connector)
    
    with tab5:
        render_active_connections(db_connector)

def render_mysql_connection(db_connector: DatabaseConnector):
    """Render MySQL connection interface."""
    st.subheader("MySQL Database Connection")
    
    # Connection form
    with st.form("mysql_connection"):
        col1, col2 = st.columns(2)
        
        with col1:
            mysql_host = st.text_input("Host", value="localhost", key="mysql_host")
            mysql_port = st.number_input("Port", value=3306, min_value=1, max_value=65535, key="mysql_port")
            mysql_database = st.text_input("Database Name", key="mysql_database")
            mysql_table = st.text_input("Table Name", key="mysql_table", help="Enter the specific table name you want to connect to")
        
        with col2:
            mysql_username = st.text_input("Username", key="mysql_username")
            mysql_password = st.text_input("Password", type="password", key="mysql_password")
            mysql_limit = st.number_input("Row Limit", value=1000, min_value=100, max_value=10000, key="mysql_limit")
        
        connect_clicked = st.form_submit_button("🔌 Connect to MySQL")
        
        if connect_clicked:
            if all([mysql_host, mysql_database, mysql_username, mysql_password, mysql_table]):
                with st.spinner("Connecting to MySQL..."):
                    result = db_connector.connect_mysql(
                        host=mysql_host,
                        port=mysql_port,
                        database=mysql_database,
                        username=mysql_username,
                        password=mysql_password
                    )
                
                if result['status'] == 'success':
                    st.success(result['message'])
                    st.session_state.mysql_connected = True
                    st.session_state.mysql_connection_info = {
                        'host': mysql_host,
                        'port': mysql_port,
                        'database': mysql_database,
                        'table': mysql_table
                    }
                    
                    # Automatically load the table data after successful connection
                    with st.spinner(f"Auto-loading table: {mysql_table}"):
                        df = db_connector.load_mysql_table(mysql_table, mysql_limit)
                        if not df.empty:
                            # Initialize database_data if it doesn't exist
                            if 'database_data' not in st.session_state:
                                st.session_state.database_data = {}
                            
                            # Add to existing database data
                            st.session_state.database_data[f"MySQL_{mysql_table}"] = df
                            st.success(f"✅ **Auto-loaded {len(df)} rows from MySQL table: {mysql_table}**")
                            st.dataframe(df.head())
                        else:
                            st.error("Failed to auto-load table data. Please use 'Load Table Data' button.")
                else:
                    st.error(result['message'])
            else:
                st.error("Please fill in all required fields including table name.")
    
    # All other elements must be outside the form
    if 'mysql' in db_connector.connections:
        st.subheader("📋 Table Information")
        table_name = st.session_state.get('mysql_connection_info', {}).get('table', 'Unknown')
        st.info(f"**Connected to table:** {table_name}")
        
        # Show available tables button
        if st.button("📊 Show Available Tables", key="mysql_show_tables_btn"):
            tables = db_connector.get_mysql_tables()
            if tables:
                st.write("**Available Tables in Database:**")
                for table in tables:
                    st.write(f"- {table}")
            else:
                st.info("No tables found or unable to retrieve table list.")
        
        # Load table data button
        if st.button("📥 Load Table Data", key="mysql_load_btn"):
            table_name = st.session_state.get('mysql_connection_info', {}).get('table')
            if table_name:
                with st.spinner(f"Loading table: {table_name}"):
                    df = db_connector.load_mysql_table(table_name, mysql_limit)
                    if not df.empty:
                        # Initialize database_data if it doesn't exist
                        if 'database_data' not in st.session_state:
                            st.session_state.database_data = {}
                        
                        # Add to existing database data (don't overwrite)
                        st.session_state.database_data[f"MySQL_{table_name}"] = df
                        
                        st.success(f"✅ Loaded {len(df)} rows from MySQL table: {table_name}")
                        st.dataframe(df.head())
                    else:
                        st.error("Failed to load table data.")
            else:
                st.error("No table name specified.")
        
        # Add "Connect Another Dataset" section
        st.subheader("🔄 Connect Another Dataset for Comparison")
        st.info("Connect to a different data source to compare with this MySQL table")
        
        # Show current status
        if 'database_data' in st.session_state and st.session_state.database_data:
            mysql_datasets = [k for k in st.session_state.database_data.keys() if k.startswith('MySQL_')]
            if mysql_datasets:
                st.success(f"✅ **MySQL table loaded:** {', '.join(mysql_datasets)}")
            else:
                st.warning("⚠️ **MySQL table not loaded yet.** Click 'Load Table Data' button above.")
        else:
            st.warning("⚠️ **No datasets loaded yet.** Connect to MySQL and load table data first.")
        
        # Dropdown to select data source type
        source_type = st.selectbox(
            "Select Data Source Type:",
            ["MySQL Table", "PostgreSQL Table", "SQL Server Table", "Local File Upload"],
            key="source_type_select"
        )
        
        if source_type == "MySQL Table":
            # Connect to another MySQL table
            col1, col2 = st.columns(2)
            with col1:
                mysql_table2 = st.text_input("Table Name", key="mysql_table2", help="Enter a different table name")
                mysql_limit2 = st.number_input("Row Limit", value=1000, min_value=100, max_value=10000, key="mysql_limit2")
            
            if st.button("🔌 Connect to Second Table", key="mysql_connect_table2"):
                if mysql_table2:
                    with st.spinner(f"Loading second table: {mysql_table2}"):
                        df2 = db_connector.load_mysql_table(mysql_table2, mysql_limit2)
                        if not df2.empty:
                            # Add to existing database data
                            if 'database_data' not in st.session_state:
                                st.session_state.database_data = {}
                            st.session_state.database_data[f"MySQL_{mysql_table2}"] = df2
                            st.success(f"✅ Loaded {len(df2)} rows from second table: {mysql_table2}")
                            st.dataframe(df2.head())
                        else:
                            st.error("Failed to load second table data.")
                else:
                    st.error("Please enter a table name.")
        
        elif source_type == "PostgreSQL Table":
            st.info("Go to the 'PostgreSQL' tab to connect to a PostgreSQL table")
        
        elif source_type == "SQL Server Table":
            st.info("Go to the 'SQL Server' tab to connect to a SQL Server table")
        
        elif source_type == "Local File Upload":
            st.info("Upload a CSV/Excel file to compare with the MySQL table")
            
            # File upload interface
            uploaded_file = st.file_uploader(
                "Choose a file", 
                type=['csv', 'xlsx', 'xls'], 
                key="mysql_comparison_file"
            )
            
            if uploaded_file is not None:
                try:
                    if uploaded_file.name.endswith('.csv'):
                        df = pd.read_csv(uploaded_file)
                    else:
                        df = pd.read_excel(uploaded_file)
                    
                    st.success(f"✅ File uploaded successfully: {uploaded_file.name}")
                    st.write(f"**File Data:** {len(df)} rows, {len(df.columns)} columns")
                    st.dataframe(df.head())
                    
                    # Add to database data for comparison
                    if 'database_data' not in st.session_state:
                        st.session_state.database_data = {}
                    st.session_state.database_data[f"File_{uploaded_file.name}"] = df
                    
                except Exception as e:
                    st.error(f"Error reading file: {str(e)}")
        
        # Show current datasets
        st.subheader("📊 Current Datasets for Comparison")
        
        # Debug info
        st.write(f"**Debug:** database_data keys: {list(st.session_state.get('database_data', {}).keys())}")
        st.write(f"**Debug:** Total datasets: {len(st.session_state.get('database_data', {}))}")
        
        if 'database_data' in st.session_state and st.session_state.database_data:
            for source_name, df in st.session_state.database_data.items():
                st.write(f"- **{source_name}**: {len(df)} rows, {len(df.columns)} columns")
            
            if len(st.session_state.database_data) > 1:
                st.success("🎯 Multiple datasets loaded! You can now run validation to compare them.")
                
                # Simple validation button
                if st.button("🚀 Run Validation", key="run_validation_btn", type="primary"):
                    # Actually run the validation
                    with st.spinner("Running validation..."):
                        try:
                            # Run all validation types
                            semantic_validator = AdvancedSemanticValidator()
                            ml_validator = AdvancedMLValidator()
                            
                            # Get validation results
                            semantic_results = semantic_validator.analyze_column_semantics_advanced(st.session_state.database_data)
                            ml_results = ml_validator.analyze_data_quality_advanced(st.session_state.database_data)
                            
                            # Store results in session state for the tabs
                            st.session_state.validation_results = {
                                'semantic_analysis': semantic_results,
                                'ml_analysis': ml_results
                            }
                            
                            st.success("✅ Validation completed! Check the Semantic Analysis, ML Analysis, AI Agent, and Visualization tabs for results.")
                            
                        except Exception as e:
                            st.error(f"❌ Validation failed: {str(e)}")
                            st.write("**Debug Info:**")
                            st.write(f"- Datasets: {list(st.session_state.database_data.keys())}")
                            st.write(f"- Dataset shapes: {[(k, v.shape) for k, v in st.session_state.database_data.items()]}")
            else:
                st.info("💡 Load both the MySQL table and upload a file to enable comparison")
                
                # Show what's needed
                if len(st.session_state.get('database_data', {})) == 1:
                    st.warning("⚠️ You have 1 dataset. You need 2 datasets to compare!")
                    st.write("**What you have:**")
                    for source_name, df in st.session_state.database_data.items():
                        st.write(f"- {source_name}")
                    st.write("**What you need:** Upload a file or connect to another table")
        else:
            st.info("💡 No datasets loaded yet. Connect to MySQL table and upload a file to compare.")
        
        # Custom query section
        st.subheader("🔍 Custom SQL Query")
        custom_query = st.text_area("Enter your SQL query:", key="mysql_custom_query")
        
        if st.button("🚀 Execute Query", key="mysql_execute_btn"):
            if custom_query.strip():
                with st.spinner("Executing query..."):
                    df = db_connector.execute_custom_query('mysql', custom_query, mysql_limit)
                    if not df.empty:
                        st.session_state.database_data = {
                            f"MySQL_Custom_Query": df
                        }
                        st.success(f"✅ Query executed successfully. Loaded {len(df)} rows.")
                        st.dataframe(df.head())
                    else:
                        st.error("Query returned no results or failed.")
            else:
                st.error("Please enter a SQL query.")

def render_postgresql_connection(db_connector: DatabaseConnector):
    """Render PostgreSQL connection interface."""
    st.subheader("PostgreSQL Database Connection")
    
    with st.form("postgresql_connection"):
        col1, col2 = st.columns(2)
        
        with col1:
            pg_host = st.text_input("Host", value="localhost", key="pg_host")
            pg_port = st.number_input("Port", value=5432, min_value=1, max_value=65535, key="pg_port")
            pg_database = st.text_input("Database Name", key="pg_database")
            pg_table = st.text_input("Table Name", key="pg_table", help="Enter the specific table name you want to connect to")
        
        with col2:
            pg_username = st.text_input("Username", key="pg_username")
            pg_password = st.text_input("Password", type="password", key="pg_password")
            pg_limit = st.number_input("Row Limit", value=1000, min_value=100, max_value=10000, key="pg_limit")
        
        connect_clicked = st.form_submit_button("🔌 Connect to PostgreSQL")
        
        if connect_clicked:
            if all([pg_host, pg_database, pg_username, pg_password, pg_table]):
                with st.spinner("Connecting to PostgreSQL..."):
                    result = db_connector.connect_postgresql(
                        host=pg_host,
                        port=pg_port,
                        database=pg_database,
                        username=pg_username,
                        password=pg_password
                    )
                
                if result['status'] == 'success':
                    st.success(result['message'])
                    st.session_state.postgresql_connected = True
                    st.session_state.postgresql_table = pg_table
                else:
                    st.error(result['message'])
            else:
                st.error("Please fill in all required fields including table name.")
    
    # Show table info if connected
    if 'postgresql' in db_connector.connections:
        st.subheader("📋 Table Information")
        st.info(f"**Connected to table:** {st.session_state.get('postgresql_table', 'Unknown')}")
        
        # Show available tables button
        if st.button("📊 Show Available Tables", key="pg_show_tables_btn"):
            tables = db_connector.get_postgresql_tables()
            if tables:
                st.write("**Available Tables in Database:**")
                for table in tables:
                    st.write(f"- {table}")
            else:
                st.info("No tables found or unable to retrieve table list.")
        
        # Load table data button
        if st.button("📥 Load Table Data", key="pg_load_btn"):
            table_name = st.session_state.get('postgresql_table')
            if table_name:
                with st.spinner(f"Loading table: {table_name}"):
                    df = db_connector.load_postgresql_table(table_name, pg_limit)
                    if not df.empty:
                        st.session_state.database_data = {
                            f"PostgreSQL_{table_name}": df
                        }
                        st.success(f"✅ Loaded {len(df)} rows from PostgreSQL table: {table_name}")
                        st.dataframe(df.head())
                    else:
                        st.error("Failed to load table data.")
            else:
                st.error("No table name specified.")
        
        # Custom query section
        st.subheader("🔍 Custom SQL Query")
        custom_query = st.text_area("Enter your SQL query:", key="pg_custom_query")
        
        if st.button("🚀 Execute Query", key="pg_execute_btn"):
            if custom_query.strip():
                with st.spinner("Executing query..."):
                    df = db_connector.execute_custom_query('postgresql', custom_query, pg_limit)
                    if not df.empty:
                        st.session_state.database_data = {
                            f"PostgreSQL_Custom_Query": df
                        }
                        st.success(f"✅ Query executed successfully. Loaded {len(df)} rows.")
                        st.dataframe(df.head())
                    else:
                        st.error("Query returned no results or failed.")
            else:
                st.error("Please enter a SQL query.")

def render_sqlserver_connection(db_connector: DatabaseConnector):
    """Render SQL Server connection interface."""
    st.subheader("SQL Server Database Connection")
    
    with st.form("sqlserver_connection"):
        col1, col2 = st.columns(2)
        
        with col1:
            sql_server = st.text_input("Server", value="localhost", key="sql_server")
            sql_database = st.text_input("Database Name", key="sql_database")
            sql_table = st.text_input("Table Name", key="sql_table", help="Enter the specific table name you want to connect to")
            sql_driver = st.selectbox("Driver", [
                "ODBC Driver 17 for SQL Server",
                "ODBC Driver 18 for SQL Server",
                "SQL Server Native Client 11.0"
            ], key="sql_driver")
        
        with col2:
            sql_username = st.text_input("Username", key="sql_username")
            sql_password = st.text_input("Password", type="password", key="sql_password")
            sql_limit = st.number_input("Row Limit", value=1000, min_value=100, max_value=10000, key="sql_limit")
        
        connect_clicked = st.form_submit_button("🔌 Connect to SQL Server")
        
        if connect_clicked:
            if all([sql_server, sql_database, sql_username, sql_password, sql_table]):
                with st.spinner("Connecting to SQL Server..."):
                    result = db_connector.connect_sqlserver(
                        server=sql_server,
                        database=sql_database,
                        username=sql_username,
                        password=sql_password,
                        driver=sql_driver
                    )
                
                if result['status'] == 'success':
                    st.success(result['message'])
                    st.session_state.sqlserver_connected = True
                    st.session_state.sqlserver_table = sql_table
                else:
                    st.error(result['message'])
            else:
                st.error("Please fill in all required fields including table name.")
    
    # Show table info if connected
    if 'sqlserver' in db_connector.connections:
        st.subheader("📋 Table Information")
        st.info(f"**Connected to table:** {st.session_state.get('sqlserver_table', 'Unknown')}")
        
        # Show available tables button
        if st.button("📊 Show Available Tables", key="sql_show_tables_btn"):
            tables = db_connector.get_sqlserver_tables()
            if tables:
                st.write("**Available Tables in Database:**")
                for table in tables:
                    st.write(f"- {table}")
            else:
                st.info("No tables found or unable to retrieve table list.")
        
        # Load table data button
        if st.button("📥 Load Table Data", key="sql_load_btn"):
            table_name = st.session_state.get('sqlserver_table')
            if table_name:
                with st.spinner(f"Loading table: {table_name}"):
                    df = db_connector.load_sqlserver_table(table_name, sql_limit)
                    if not df.empty:
                        st.session_state.database_data = {
                            f"SQLServer_{table_name}": df
                        }
                        st.success(f"✅ Loaded {len(df)} rows from SQL Server table: {table_name}")
                        st.dataframe(df.head())
                    else:
                        st.error("Failed to load table data.")
            else:
                st.error("No table name specified.")
        
        # Custom query section
        st.subheader("🔍 Custom SQL Query")
        custom_query = st.text_area("Enter your SQL query:", key="sql_custom_query")
        
        if st.button("🚀 Execute Query", key="sql_execute_btn"):
            if custom_query.strip():
                with st.spinner("Executing query..."):
                    df = db_connector.execute_custom_query('sqlserver', custom_query, sql_limit)
                    if not df.empty:
                        st.session_state.database_data = {
                            f"SQLServer_Custom_Query": df
                        }
                        st.success(f"✅ Query executed successfully. Loaded {len(df)} rows.")
                        st.dataframe(df.head())
                    else:
                        st.error("Query returned no results or failed.")
            else:
                st.error("Please enter a SQL query.")

def render_azure_blob_connection(db_connector: DatabaseConnector):
    """Render Azure Blob Storage connection interface."""
    st.subheader("Azure Blob Storage Connection")
    
    with st.form("azure_blob_connection"):
        azure_connection_string = st.text_input(
            "Connection String", 
            type="password", 
            key="azure_connection_string",
            help="Azure Storage Account connection string"
        )
        azure_container = st.text_input("Container Name", key="azure_container")
        azure_file_extension = st.selectbox(
            "File Type Filter", 
            ["All Files", ".csv", ".json", ".parquet", ".xlsx", ".xls"],
            key="azure_file_extension"
        )
        
        connect_clicked = st.form_submit_button("🔌 Connect to Azure Blob")
        
        if connect_clicked:
            if azure_connection_string and azure_container:
                with st.spinner("Connecting to Azure Blob Storage..."):
                    result = db_connector.connect_azure_blob(
                        connection_string=azure_connection_string,
                        container_name=azure_container
                    )
                
                if result['status'] == 'success':
                    st.success(result['message'])
                    st.session_state.azure_blob_connected = True
                else:
                    st.error(result['message'])
            else:
                st.error("Please provide connection string and container name.")
    
    # Show files if connected
    if 'azure_blob' in db_connector.connections:
        st.subheader("📁 Available Files")
        
        # Get file extension filter
        file_ext = None
        if azure_file_extension != "All Files":
            file_ext = azure_file_extension
        
        files = db_connector.get_azure_blob_files(file_ext)
        
        if files:
            selected_file = st.selectbox("Select a file to load:", files, key="azure_file_select")
            
            if st.button("📥 Load File Data", key="azure_load_btn"):
                with st.spinner(f"Loading file: {selected_file}"):
                    df = db_connector.load_azure_blob_file(selected_file)
                    if not df.empty:
                        st.session_state.database_data = {
                            f"AzureBlob_{selected_file}": df
                        }
                        st.success(f"✅ Loaded {len(df)} rows from Azure Blob file: {selected_file}")
                        st.dataframe(df.head())
                    else:
                        st.error("Failed to load file data.")
        else:
            st.info("No files found or unable to retrieve file list.")

def render_active_connections(db_connector: DatabaseConnector):
    """Render active connections management."""
    st.subheader("🔗 Active Connections")
    
    connections = db_connector.get_connection_summary()
    
    if connections:
        st.success(f"✅ {len(connections)} active connection(s)")
        
        for conn_type, details in connections.items():
            with st.expander(f"{conn_type.upper()} Connection Details"):
                st.json(details)
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button(f"❌ Disconnect {conn_type}", key=f"disconnect_{conn_type}"):
                        result = db_connector.disconnect(conn_type)
                        if result['status'] == 'success':
                            st.success(result['message'])
                            st.rerun()
                        else:
                            st.error(result['message'])
                
                with col2:
                    if conn_type in ['mysql', 'postgresql', 'sqlserver']:
                        if st.button(f"📊 Show Schema", key=f"schema_{conn_type}"):
                            if conn_type == 'mysql':
                                tables = db_connector.get_mysql_tables()
                            elif conn_type == 'postgresql':
                                tables = db_connector.get_postgresql_tables()
                            else:  # sqlserver
                                tables = db_connector.get_sqlserver_tables()
                            
                            if tables:
                                st.write("**Available Tables:**")
                                for table in tables:
                                    st.write(f"- {table}")
                            else:
                                st.info("No tables found.")
        
        # Disconnect all button
        if st.button("❌ Disconnect All", type="secondary"):
            result = db_connector.disconnect_all()
            if result['status'] == 'success':
                st.success(result['message'])
                st.rerun()
            else:
                st.error(result['message'])
    
    else:
        st.info("No active database connections.")
        st.markdown("""
        **To get started:**
        1. Go to any database tab above
        2. Enter your connection details
        3. Click connect to establish a connection
        4. Load tables/files for validation
        """)
    
    # Show loaded data summary
    if 'database_data' in st.session_state:
        st.subheader("📊 Loaded Data Summary")
        data_summary = {}
        
        for name, df in st.session_state.database_data.items():
            data_summary[name] = {
                'rows': len(df),
                'columns': len(df.columns),
                'memory_usage_mb': df.memory_usage(deep=True).sum() / 1024 / 1024
            }
        
        st.json(data_summary)
        
        # Option to clear loaded data
        if st.button("🗑️ Clear All Loaded Data"):
            del st.session_state.database_data
            st.success("All loaded data cleared.")
            st.rerun()

def get_database_data() -> Dict[str, pd.DataFrame]:
    """Get all loaded database data for validation."""
    return st.session_state.get('database_data', {})
