"""Test utilities and fixtures for pytest."""

import pytest
import pandas as pd
import numpy as np
from pathlib import Path
import tempfile
import shutil


@pytest.fixture
def sample_dataframe():
    """Create a sample DataFrame for testing."""
    np.random.seed(42)
    
    data = {
        'id': range(1, 101),
        'name': [f'Person_{i}' for i in range(1, 101)],
        'age': np.random.randint(18, 80, 100),
        'salary': np.random.randint(30000, 150000, 100),
        'department': np.random.choice(['Sales', 'Engineering', 'Marketing', 'HR'], 100),
        'city': np.random.choice(['New York', 'San Francisco', 'Chicago', 'Boston'], 100),
    }
    
    df = pd.DataFrame(data)
    
    # Add some missing values
    df.loc[np.random.choice(df.index, 10), 'age'] = np.nan
    df.loc[np.random.choice(df.index, 5), 'salary'] = np.nan
    
    # Add some duplicates
    df = pd.concat([df, df.iloc[:5]], ignore_index=True)
    
    return df


@pytest.fixture
def sample_dataframe_with_issues():
    """Create a DataFrame with various data quality issues."""
    data = {
        'ID': [1, 2, 3, 4, 5, 5],  # Duplicate
        'Name ': ['Alice', 'Bob', None, 'David', 'Eve', 'Eve'],  # Space in column name, missing value
        'Age': [25, 30, 35, None, 45, 45],  # Missing value
        'Category': ['Cat A', 'Cat-A', 'Cat_A', 'Cat B', 'Cat B', 'Cat B'],  # Similar categories
        'Value': [100, 200, None, 400, 500, 500],  # Missing value
    }
    
    return pd.DataFrame(data)


@pytest.fixture
def temp_data_dir():
    """Create a temporary directory for test data."""
    temp_dir = tempfile.mkdtemp()
    yield Path(temp_dir)
    shutil.rmtree(temp_dir)


@pytest.fixture
def test_config():
    """Create a test configuration dictionary."""
    return {
        'data_path': 'data',
        'artifacts_path': 'data/artifacts',
        'logs_path': 'logs',
        'pipeline': {
            'inspector': {
                'enabled': True,
                'profile': True,
                'validate': True
            },
            'refiner': {
                'enabled': True,
                'operations': ['clean_column_names', 'handle_missing_values', 'remove_duplicates']
            },
            'insight': {
                'enabled': True,
                'generate_plots': True
            }
        }
    }


@pytest.fixture
def mock_csv_file(tmp_path, sample_dataframe):
    """Create a temporary CSV file for testing."""
    csv_path = tmp_path / "test_data.csv"
    sample_dataframe.to_csv(csv_path, index=False)
    return csv_path
