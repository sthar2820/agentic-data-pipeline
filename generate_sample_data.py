"""
Generate sample dataset for testing the pipeline.
"""

import pandas as pd
import numpy as np
from pathlib import Path

# Set random seed for reproducibility
np.random.seed(42)

# Generate sample data
n_rows = 500

data = {
    'customer_id': range(1, n_rows + 1),
    'customer_name': [f'Customer_{i}' for i in range(1, n_rows + 1)],
    'age': np.random.randint(18, 80, n_rows),
    'annual_income': np.random.randint(20000, 200000, n_rows),
    'credit_score': np.random.randint(300, 850, n_rows),
    'account_balance': np.random.uniform(0, 100000, n_rows).round(2),
    'num_products': np.random.randint(1, 5, n_rows),
    'region': np.random.choice(['North', 'South', 'East', 'West', 'Central'], n_rows),
    'customer_segment': np.random.choice(['Premium', 'Standard', 'Basic'], n_rows, p=[0.2, 0.5, 0.3]),
    'account_type': np.random.choice(['Savings', 'Checking', 'Investment'], n_rows),
    'is_active': np.random.choice([True, False], n_rows, p=[0.8, 0.2]),
    'join_date': pd.date_range(start='2020-01-01', end='2024-01-01', periods=n_rows),
    'last_transaction_date': pd.date_range(start='2023-01-01', end='2024-10-30', periods=n_rows),
}

df = pd.DataFrame(data)

# Introduce some data quality issues

# 1. Add missing values (5-10% per column)
for col in ['age', 'annual_income', 'credit_score', 'account_balance']:
    missing_idx = np.random.choice(df.index, size=int(len(df) * 0.05), replace=False)
    df.loc[missing_idx, col] = np.nan

# 2. Add some duplicate rows
duplicate_rows = df.sample(n=10).copy()
df = pd.concat([df, duplicate_rows], ignore_index=True)

# 3. Add some similar category variations (typos/inconsistencies)
region_variations = {
    'North': ['North', 'north', 'N', 'Northern'],
    'South': ['South', 'south', 'S', 'Southern'],
    'East': ['East', 'east', 'E', 'Eastern'],
    'West': ['West', 'west', 'W', 'Western'],
    'Central': ['Central', 'central', 'C']
}

for idx in range(len(df)):
    if np.random.random() < 0.1:  # 10% chance of variation
        original = df.loc[idx, 'region']
        if original in region_variations:
            df.loc[idx, 'region'] = np.random.choice(region_variations[original])

# 4. Add some outliers
outlier_idx = np.random.choice(df.index, size=5, replace=False)
df.loc[outlier_idx, 'annual_income'] = np.random.randint(500000, 1000000, 5)

# Save to CSV
output_dir = Path('data/raw')
output_dir.mkdir(parents=True, exist_ok=True)

output_path = output_dir / 'sample_customer_data.csv'
df.to_csv(output_path, index=False)

print(f"✅ Sample dataset created: {output_path}")
print(f"   - {len(df)} rows")
print(f"   - {len(df.columns)} columns")
print(f"   - {df.isnull().sum().sum()} missing values")
print(f"   - {df.duplicated().sum()} duplicate rows")
print("\nYou can now run the pipeline with:")
print(f"   python main.py --input {output_path}")
print("   or")
print("   streamlit run ui/app.py")
