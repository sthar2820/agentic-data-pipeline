"""Tests for Refiner Agent."""

import pytest
import pandas as pd
from pathlib import Path
import sys
import numpy as np

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from agents.refiner import RefinerAgent


class TestRefinerAgent:
    """Test suite for Refiner Agent."""
    
    def test_initialization(self, test_config):
        """Test agent initialization."""
        agent = RefinerAgent(test_config)
        assert agent is not None
        assert agent.config == test_config
        assert agent.artifacts_path.exists()
    
    def test_clean_column_names(self, test_config):
        """Test column name cleaning."""
        agent = RefinerAgent(test_config)
        
        df = pd.DataFrame({
            'Column Name': [1, 2, 3],
            'Another Column!': [4, 5, 6],
            'UPPER CASE': [7, 8, 9]
        })
        
        df_cleaned = agent.clean_column_names(df)
        
        # Check that column names are cleaned
        assert 'column_name' in df_cleaned.columns or 'Column Name' != list(df_cleaned.columns)[0]
        assert len(agent.transformation_log) > 0
    
    def test_handle_missing_values_simple(self, sample_dataframe_with_issues, test_config):
        """Test simple missing value handling."""
        agent = RefinerAgent(test_config)
        
        df_clean = agent.handle_missing_values(sample_dataframe_with_issues, strategy='simple')
        
        # Check that missing values are reduced
        assert df_clean.isnull().sum().sum() <= sample_dataframe_with_issues.isnull().sum().sum()
    
    def test_handle_missing_values_drop(self, sample_dataframe_with_issues, test_config):
        """Test drop strategy for missing values."""
        agent = RefinerAgent(test_config)
        
        df_clean = agent.handle_missing_values(sample_dataframe_with_issues, strategy='drop')
        
        # Check that rows with missing values are dropped
        assert df_clean.isnull().sum().sum() == 0
        assert len(df_clean) < len(sample_dataframe_with_issues)
    
    def test_remove_duplicates(self, sample_dataframe, test_config):
        """Test duplicate removal."""
        agent = RefinerAgent(test_config)
        
        # Sample dataframe has duplicates
        df_dedup = agent.remove_duplicates(sample_dataframe)
        
        # Check that duplicates are removed
        assert df_dedup.duplicated().sum() == 0
        assert len(df_dedup) <= len(sample_dataframe)
    
    def test_normalize_numeric_columns(self, sample_dataframe, test_config):
        """Test numeric normalization."""
        agent = RefinerAgent(test_config)
        
        df_norm = agent.normalize_numeric_columns(sample_dataframe, method='standard')
        
        # Check that numeric columns are normalized
        numeric_cols = df_norm.select_dtypes(include=['number']).columns
        for col in numeric_cols:
            if col != 'id':  # Skip ID column
                # Normalized values should have mean close to 0 and std close to 1
                mean_val = df_norm[col].mean()
                std_val = df_norm[col].std()
                assert abs(mean_val) < 1e-10 or pd.isna(mean_val)  # Close to 0
                assert abs(std_val - 1.0) < 0.1 or pd.isna(std_val)  # Close to 1
    
    def test_run_complete_pipeline(self, sample_dataframe, test_config, tmp_path):
        """Test complete refiner pipeline."""
        test_config['artifacts_path'] = str(tmp_path)
        agent = RefinerAgent(test_config)
        
        df_refined, results = agent.run(sample_dataframe)
        
        assert results is not None
        assert results['status'] == 'success'
        assert 'operations_performed' in results
        assert len(results['operations_performed']) > 0
        assert results['rows_after'] > 0
        assert df_refined is not None
        assert len(df_refined) > 0
    
    def test_transformation_log(self, sample_dataframe, test_config):
        """Test that transformation log is maintained."""
        agent = RefinerAgent(test_config)
        
        df_refined, results = agent.run(sample_dataframe)
        
        assert 'transformation_log' in results
        assert len(results['transformation_log']) > 0
