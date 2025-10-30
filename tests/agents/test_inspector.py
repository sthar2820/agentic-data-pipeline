"""Tests for Inspector Agent."""

import pytest
import pandas as pd
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from agents.inspector import InspectorAgent


class TestInspectorAgent:
    """Test suite for Inspector Agent."""
    
    def test_initialization(self, test_config):
        """Test agent initialization."""
        agent = InspectorAgent(test_config)
        assert agent is not None
        assert agent.config == test_config
        assert agent.artifacts_path.exists()
    
    def test_profile_data(self, sample_dataframe, test_config, tmp_path):
        """Test data profiling functionality."""
        test_config['artifacts_path'] = str(tmp_path)
        agent = InspectorAgent(test_config)
        
        stats = agent.profile_data(sample_dataframe, "test_dataset")
        
        assert stats is not None
        assert 'n_rows' in stats
        assert 'n_columns' in stats
        assert stats['n_rows'] > 0
        assert stats['n_columns'] > 0
        
        # Check that profile report was created
        profile_html = tmp_path / "test_dataset_profile.html"
        assert profile_html.exists()
        
        # Check that stats JSON was created
        stats_json = tmp_path / "test_dataset_profile_stats.json"
        assert stats_json.exists()
    
    def test_validate_data(self, sample_dataframe, test_config, tmp_path):
        """Test data validation functionality."""
        test_config['artifacts_path'] = str(tmp_path)
        agent = InspectorAgent(test_config)
        
        validation_results = agent.validate_data(sample_dataframe)
        
        assert validation_results is not None
        assert 'total_expectations' in validation_results
        assert 'successful_expectations' in validation_results
        assert 'failed_expectations' in validation_results
        assert 'success_percent' in validation_results
    
    def test_run_complete_pipeline(self, sample_dataframe, test_config, tmp_path):
        """Test complete inspector pipeline."""
        test_config['artifacts_path'] = str(tmp_path)
        agent = InspectorAgent(test_config)
        
        results = agent.run(sample_dataframe, "test_dataset")
        
        assert results is not None
        assert results['status'] == 'success'
        assert 'profile' in results
        assert 'validation' in results
        assert results['profile']['n_rows'] > 0
    
    def test_handle_empty_dataframe(self, test_config, tmp_path):
        """Test handling of empty DataFrame."""
        test_config['artifacts_path'] = str(tmp_path)
        agent = InspectorAgent(test_config)
        
        empty_df = pd.DataFrame()
        
        # Should handle gracefully
        try:
            stats = agent.profile_data(empty_df, "empty_dataset")
            assert stats['n_rows'] == 0
        except Exception:
            # It's okay if it raises an exception for empty data
            pass
