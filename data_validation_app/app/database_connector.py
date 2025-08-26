"""Database connector for multiple database types and cloud storage."""

import pandas as pd
import streamlit as st
from typing import Dict, List, Any, Optional, Union
import sqlalchemy as sa
from sqlalchemy import create_engine, text
import pymysql
import psycopg2
import pyodbc
from azure.storage.blob import BlobServiceClient
import io
import json
import os
from urllib.parse import quote_plus

class DatabaseConnector:
    """Connect to various databases and cloud storage for data validation."""
    
    def __init__(self):
        self.connections = {}
        self.connection_status = {}
    
    def connect_mysql(self, host: str, port: int, database: str, username: str, password: str) -> Dict:
        """Connect to MySQL database."""
        try:
            # Create connection string
            connection_string = f"mysql+pymysql://{username}:{password}@{host}:{port}/{database}"
            engine = create_engine(connection_string, echo=False)
            
            # Test connection
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            
            self.connections['mysql'] = engine
            self.connection_status['mysql'] = {'status': 'connected', 'database': database, 'host': host}
            
            return {
                'status': 'success',
                'message': f'Successfully connected to MySQL database: {database}',
                'connection_info': {'host': host, 'port': port, 'database': database}
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Failed to connect to MySQL: {str(e)}',
                'connection_info': None
            }
    
    def connect_postgresql(self, host: str, port: int, database: str, username: str, password: str) -> Dict:
        """Connect to PostgreSQL database."""
        try:
            # Create connection string
            connection_string = f"postgresql://{username}:{password}@{host}:{port}/{database}"
            engine = create_engine(connection_string, echo=False)
            
            # Test connection
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            
            self.connections['postgresql'] = engine
            self.connection_status['postgresql'] = {'status': 'connected', 'database': database, 'host': host}
            
            return {
                'status': 'success',
                'message': f'Successfully connected to PostgreSQL database: {database}',
                'connection_info': {'host': host, 'port': port, 'database': database}
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Failed to connect to PostgreSQL: {str(e)}',
                'connection_info': None
            }
    
    def connect_sqlserver(self, server: str, database: str, username: str, password: str, driver: str = "ODBC Driver 17 for SQL Server") -> Dict:
        """Connect to SQL Server database."""
        try:
            # Create connection string
            connection_string = f"mssql+pyodbc://{username}:{password}@{server}/{database}?driver={quote_plus(driver)}"
            engine = create_engine(connection_string, echo=False)
            
            # Test connection
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            
            self.connections['sqlserver'] = engine
            self.connection_status['sqlserver'] = {'status': 'connected', 'database': database, 'server': server}
            
            return {
                'status': 'success',
                'message': f'Successfully connected to SQL Server database: {database}',
                'connection_info': {'server': server, 'database': database, 'driver': driver}
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Failed to connect to SQL Server: {str(e)}',
                'connection_info': None
            }
    
    def connect_azure_blob(self, connection_string: str, container_name: str) -> Dict:
        """Connect to Azure Blob Storage."""
        try:
            # Create blob service client
            blob_service_client = BlobServiceClient.from_connection_string(connection_string)
            container_client = blob_service_client.get_container_client(container_name)
            
            # Test connection by listing blobs
            blobs = list(container_client.list_blobs(max_results=1))
            
            self.connections['azure_blob'] = {
                'service_client': blob_service_client,
                'container_client': container_client,
                'container_name': container_name
            }
            self.connection_status['azure_blob'] = {'status': 'connected', 'container': container_name}
            
            return {
                'status': 'success',
                'message': f'Successfully connected to Azure Blob Storage container: {container_name}',
                'connection_info': {'container': container_name}
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Failed to connect to Azure Blob Storage: {str(e)}',
                'connection_info': None
            }
    
    def get_mysql_tables(self) -> List[str]:
        """Get list of tables from MySQL database."""
        try:
            if 'mysql' not in self.connections:
                return []
            
            engine = self.connections['mysql']
            with engine.connect() as conn:
                result = conn.execute(text("SHOW TABLES"))
                tables = [row[0] for row in result.fetchall()]
            return tables
            
        except Exception as e:
            st.error(f"Error getting MySQL tables: {str(e)}")
            return []
    
    def get_postgresql_tables(self) -> List[str]:
        """Get list of tables from PostgreSQL database."""
        try:
            if 'postgresql' not in self.connections:
                return []
            
            engine = self.connections['postgresql']
            with engine.connect() as conn:
                result = conn.execute(text("""
                    SELECT table_name 
                    FROM information_schema.tables 
                    WHERE table_schema = 'public'
                """))
                tables = [row[0] for row in result.fetchall()]
            return tables
            
        except Exception as e:
            st.error(f"Error getting PostgreSQL tables: {str(e)}")
            return []
    
    def get_sqlserver_tables(self) -> List[str]:
        """Get list of tables from SQL Server database."""
        try:
            if 'sqlserver' not in self.connections:
                return []
            
            engine = self.connections['sqlserver']
            with engine.connect() as conn:
                result = conn.execute(text("""
                    SELECT table_name 
                    FROM information_schema.tables 
                    WHERE table_type = 'BASE TABLE'
                """))
                tables = [row[0] for row in result.fetchall()]
            return tables
            
        except Exception as e:
            st.error(f"Error getting SQL Server tables: {str(e)}")
            return []
    
    def get_azure_blob_files(self, file_extension: str = None) -> List[str]:
        """Get list of files from Azure Blob Storage."""
        try:
            if 'azure_blob' not in self.connections:
                return []
            
            container_client = self.connections['azure_blob']['container_client']
            blobs = list(container_client.list_blobs())
            
            if file_extension:
                files = [blob.name for blob in blobs if blob.name.endswith(file_extension)]
            else:
                files = [blob.name for blob in blobs]
            
            return files
            
        except Exception as e:
            st.error(f"Error getting Azure Blob files: {str(e)}")
            return []
    
    def load_mysql_table(self, table_name: str, limit: int = 1000) -> pd.DataFrame:
        """Load data from MySQL table."""
        try:
            if 'mysql' not in self.connections:
                return pd.DataFrame()
            
            engine = self.connections['mysql']
            query = f"SELECT * FROM {table_name} LIMIT {limit}"
            df = pd.read_sql(query, engine)
            return df
            
        except Exception as e:
            st.error(f"Error loading MySQL table {table_name}: {str(e)}")
            return pd.DataFrame()
    
    def load_postgresql_table(self, table_name: str, limit: int = 1000) -> pd.DataFrame:
        """Load data from PostgreSQL table."""
        try:
            if 'postgresql' not in self.connections:
                return pd.DataFrame()
            
            engine = self.connections['postgresql']
            query = f"SELECT * FROM {table_name} LIMIT {limit}"
            df = pd.read_sql(query, engine)
            return df
            
        except Exception as e:
            st.error(f"Error loading PostgreSQL table {table_name}: {str(e)}")
            return pd.DataFrame()
    
    def load_sqlserver_table(self, table_name: str, limit: int = 1000) -> pd.DataFrame:
        """Load data from SQL Server table."""
        try:
            if 'sqlserver' not in self.connections:
                return pd.DataFrame()
            
            engine = self.connections['sqlserver']
            query = f"SELECT TOP {limit} * FROM {table_name}"
            df = pd.read_sql(query, engine)
            return df
            
        except Exception as e:
            st.error(f"Error loading SQL Server table {table_name}: {str(e)}")
            return pd.DataFrame()
    
    def load_azure_blob_file(self, file_name: str) -> pd.DataFrame:
        """Load data from Azure Blob Storage file."""
        try:
            if 'azure_blob' not in self.connections:
                return pd.DataFrame()
            
            container_client = self.connections['azure_blob']['container_client']
            blob_client = container_client.get_blob_client(file_name)
            
            # Download blob content
            blob_data = blob_client.download_blob()
            content = blob_data.read()
            
            # Determine file type and load accordingly
            if file_name.endswith('.csv'):
                df = pd.read_csv(io.BytesIO(content))
            elif file_name.endswith('.json'):
                df = pd.read_json(io.BytesIO(content))
            elif file_name.endswith('.parquet'):
                df = pd.read_parquet(io.BytesIO(content))
            elif file_name.endswith('.xlsx') or file_name.endswith('.xls'):
                df = pd.read_excel(io.BytesIO(content))
            else:
                st.error(f"Unsupported file type: {file_name}")
                return pd.DataFrame()
            
            return df
            
        except Exception as e:
            st.error(f"Error loading Azure Blob file {file_name}: {str(e)}")
            return pd.DataFrame()
    
    def execute_custom_query(self, connection_type: str, query: str, limit: int = 1000) -> pd.DataFrame:
        """Execute custom SQL query on specified database."""
        try:
            if connection_type not in self.connections:
                st.error(f"No connection to {connection_type}")
                return pd.DataFrame()
            
            engine = self.connections[connection_type]
            
            # Add limit if not present
            if 'LIMIT' not in query.upper() and limit:
                if connection_type == 'sqlserver':
                    query = f"SELECT TOP {limit} * FROM ({query}) AS subquery"
                else:
                    query = f"{query} LIMIT {limit}"
            
            df = pd.read_sql(query, engine)
            return df
            
        except Exception as e:
            st.error(f"Error executing custom query: {str(e)}")
            return pd.DataFrame()
    
    def get_connection_summary(self) -> Dict:
        """Get summary of all active connections."""
        summary = {}
        for conn_type, status in self.connection_status.items():
            if status['status'] == 'connected':
                summary[conn_type] = status
        return summary
    
    def disconnect(self, connection_type: str) -> Dict:
        """Disconnect from specified database."""
        try:
            if connection_type in self.connections:
                if connection_type in ['mysql', 'postgresql', 'sqlserver']:
                    self.connections[connection_type].dispose()
                del self.connections[connection_type]
                del self.connection_status[connection_type]
                
                return {
                    'status': 'success',
                    'message': f'Successfully disconnected from {connection_type}'
                }
            else:
                return {
                    'status': 'error',
                    'message': f'No active connection to {connection_type}'
                }
                
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Error disconnecting from {connection_type}: {str(e)}'
            }
    
    def disconnect_all(self) -> Dict:
        """Disconnect from all databases."""
        try:
            for conn_type in list(self.connections.keys()):
                self.disconnect(conn_type)
            
            return {
                'status': 'success',
                'message': 'Successfully disconnected from all databases'
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Error disconnecting from all databases: {str(e)}'
            }
