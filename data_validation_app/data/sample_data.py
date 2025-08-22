"""Sample data files for testing the validation app."""

import pandas as pd
import json
from pathlib import Path

# Create data directory if it doesn't exist
Path("data_validation_app/data").mkdir(parents=True, exist_ok=True)


def create_sample_users_data():
    """Create sample users dataset."""
    users_data = {
        "id": [1, 2, 3, 4, 5],
        "name": ["Alice Johnson", "Bob Smith", "Charlie Brown", "Diana Prince", "Eve Wilson"],
        "email": ["alice@example.com", "bob@example.com", "charlie@example.com", "diana@example.com", "eve@example.com"],
        "age": [25, 30, 35, 28, 32],
        "department": ["Engineering", "Marketing", "Sales", "Engineering", "HR"],
        "salary": [75000, 65000, 70000, 80000, 60000],
        "hire_date": ["2023-01-15", "2022-06-20", "2021-12-10", "2023-03-01", "2022-09-15"]
    }
    
    df = pd.DataFrame(users_data)
    df.to_csv("data_validation_app/data/sample_users.csv", index=False)
    df.to_json("data_validation_app/data/sample_users.json", orient="records", indent=2)
    
    return df


def create_sample_orders_data():
    """Create sample orders dataset."""
    orders_data = {
        "order_id": [101, 102, 103, 104, 105, 106],
        "user_id": [1, 2, 1, 3, 4, 2],
        "product_name": ["Laptop", "Mouse", "Keyboard", "Monitor", "Headphones", "Webcam"],
        "quantity": [1, 2, 1, 1, 1, 1],
        "unit_price": [1200.00, 25.50, 75.00, 300.00, 150.00, 80.00],
        "total_amount": [1200.00, 51.00, 75.00, 300.00, 150.00, 80.00],
        "order_date": ["2024-01-15", "2024-01-16", "2024-01-17", "2024-01-18", "2024-01-19", "2024-01-20"],
        "status": ["completed", "pending", "completed", "shipped", "completed", "pending"]
    }
    
    df = pd.DataFrame(orders_data)
    df.to_csv("data_validation_app/data/sample_orders.csv", index=False)
    df.to_json("data_validation_app/data/sample_orders.json", orient="records", indent=2)
    
    return df


def create_sample_products_data():
    """Create sample products dataset."""
    products_data = {
        "product_id": [1, 2, 3, 4, 5, 6, 7],
        "product_name": ["Laptop", "Mouse", "Keyboard", "Monitor", "Headphones", "Webcam", "Tablet"],
        "category": ["Electronics", "Accessories", "Accessories", "Electronics", "Accessories", "Accessories", "Electronics"],
        "brand": ["TechCorp", "TechCorp", "TechCorp", "TechCorp", "AudioTech", "TechCorp", "TechCorp"],
        "price": [1200.00, 25.50, 75.00, 300.00, 150.00, 80.00, 500.00],
        "stock_quantity": [50, 200, 100, 75, 80, 60, 40],
        "supplier_id": [1, 1, 1, 1, 2, 1, 1],
        "created_at": ["2023-01-01", "2023-01-01", "2023-01-01", "2023-01-01", "2023-01-01", "2023-01-01", "2023-01-01"]
    }
    
    df = pd.DataFrame(products_data)
    df.to_csv("data_validation_app/data/sample_products.csv", index=False)
    df.to_json("data_validation_app/data/sample_products.json", orient="records", indent=2)
    
    return df


def create_inconsistent_users_data():
    """Create users dataset with inconsistencies for testing validation."""
    users_data = {
        "user_id": [1, 2, 3, 4, 5],  # Different column name
        "full_name": ["Alice Johnson", "Bob Smith", "Charlie Brown", "Diana Prince", "Eve Wilson"],  # Different column name
        "email_address": ["alice@example.com", "bob@example.com", "charlie@example.com", "diana@example.com", "eve@example.com"],  # Different column name
        "user_age": [25, 30, 35, 28, 32],  # Different column name
        "dept": ["Engineering", "Marketing", "Sales", "Engineering", "HR"],  # Different column name
        "annual_salary": [75000, 65000, 70000, 80000, 60000],  # Different column name
        "employment_date": ["2023-01-15", "2022-06-20", "2021-12-10", "2023-03-01", "2022-09-15"]  # Different column name
    }
    
    df = pd.DataFrame(users_data)
    df.to_csv("data_validation_app/data/inconsistent_users.csv", index=False)
    
    return df


def create_low_quality_data():
    """Create dataset with quality issues for testing."""
    users_data = {
        "id": [1, 2, 3, 4, 5, 6, 7, 8],
        "name": ["Alice Johnson", "Bob Smith", None, "Diana Prince", "Eve Wilson", "Frank Miller", None, "Grace Lee"],
        "email": ["alice@example.com", "bob@example.com", "charlie@example.com", None, "eve@example.com", "frank@example.com", "george@example.com", None],
        "age": [25, 30, 35, 28, 32, None, 40, 29],
        "department": ["Engineering", "Marketing", "Sales", "Engineering", "HR", "Sales", "Marketing", "Engineering"],
        "salary": [75000, 65000, 70000, 80000, 60000, 72000, 68000, 75000],
        "hire_date": ["2023-01-15", "2022-06-20", "2021-12-10", "2023-03-01", "2022-09-15", "2022-11-01", "2023-02-15", "2022-08-10"]
    }
    
    df = pd.DataFrame(users_data)
    df.to_csv("data_validation_app/data/low_quality_users.csv", index=False)
    
    return df


def create_all_sample_data():
    """Create all sample data files."""
    print("Creating sample data files...")
    
    users_df = create_sample_users_data()
    orders_df = create_sample_orders_data()
    products_df = create_sample_products_data()
    inconsistent_users_df = create_inconsistent_users_data()
    low_quality_users_df = create_low_quality_data()
    
    print("✅ Sample data files created successfully!")
    print(f"📁 Users: {users_df.shape}")
    print(f"📁 Orders: {orders_df.shape}")
    print(f"📁 Products: {products_df.shape}")
    print(f"📁 Inconsistent Users: {inconsistent_users_df.shape}")
    print(f"📁 Low Quality Users: {low_quality_users_df.shape}")
    
    return {
        "users": users_df,
        "orders": orders_df,
        "products": products_df,
        "inconsistent_users": inconsistent_users_df,
        "low_quality_users": low_quality_users_df
    }


if __name__ == "__main__":
    create_all_sample_data()
