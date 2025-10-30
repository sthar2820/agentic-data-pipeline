"""Tests for Insight Agent."""

import pytest
import pandas as pd
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from agents.insight import InsightAgent


class TestInsightAgent:
    """Test suite for Insight Agent."""
    
    def test_initialization(self, test_config):
        """Test agent initialization."""
        agent = InsightAgent(test_config)
        assert agent is not None
        assert agent.config == test_config
        assert agent.artifacts_path.exists()
    
    def test_generate_summary_statistics(self, sample_dataframe, test_config, tmp_path):
        """Test summary statistics generation."""
        test_config['artifacts_path'] = str(tmp_path)
        agent = InsightAgent(test_config)
        
        stats = agent.generate_summary_statistics(sample_dataframe)
        
        assert stats is not None
        assert 'shape' in stats
        assert 'dtypes' in stats
        assert 'numeric_summary' in stats
        assert 'categorical_summary' in stats
        
        # Check JSON file was created
        stats_json = tmp_path / "summary_statistics.json"
        assert stats_json.exists()
    
    def test_create_distribution_plots(self, sample_dataframe, test_config, tmp_path):
        """Test distribution plot creation."""
        test_config['artifacts_path'] = str(tmp_path)
        agent = InsightAgent(test_config)
        
        plot_paths = agent.create_distribution_plots(sample_dataframe)
        
        assert plot_paths is not None
        assert len(plot_paths) > 0
        
        # Check that plot files were created
        for path in plot_paths:
            assert Path(path).exists()
    
    def test_create_correlation_heatmap(self, sample_dataframe, test_config, tmp_path):
        """Test correlation heatmap creation."""
        test_config['artifacts_path'] = str(tmp_path)
        agent = InsightAgent(test_config)
        
        heatmap_path = agent.create_correlation_heatmap(sample_dataframe)
        
        assert heatmap_path is not None
        assert Path(heatmap_path).exists()
    
    def test_create_categorical_plots(self, sample_dataframe, test_config, tmp_path):
        """Test categorical plot creation."""
        test_config['artifacts_path'] = str(tmp_path)
        agent = InsightAgent(test_config)
        
        plot_paths = agent.create_categorical_plots(sample_dataframe)
        
        # Should create plots for categorical columns
        assert isinstance(plot_paths, list)
        
        if len(plot_paths) > 0:
            for path in plot_paths:
                assert Path(path).exists()
    
    def test_create_boxplots(self, sample_dataframe, test_config, tmp_path):
        """Test boxplot creation."""
        test_config['artifacts_path'] = str(tmp_path)
        agent = InsightAgent(test_config)
        
        boxplot_path = agent.create_boxplots(sample_dataframe)
        
        assert boxplot_path is not None
        assert Path(boxplot_path).exists()
    
    def test_run_complete_pipeline(self, sample_dataframe, test_config, tmp_path):
        """Test complete insight pipeline."""
        test_config['artifacts_path'] = str(tmp_path)
        agent = InsightAgent(test_config)
        
        results = agent.run(sample_dataframe, "test_dataset")
        
        assert results is not None
        assert results['status'] == 'success'
        assert 'summary_statistics' in results
        assert 'visualizations' in results
        assert len(results['visualizations']) > 0
    
    def test_handle_dataframe_no_numerics(self, test_config, tmp_path):
        """Test handling DataFrame with no numeric columns."""
        test_config['artifacts_path'] = str(tmp_path)
        agent = InsightAgent(test_config)
        
        df = pd.DataFrame({
            'name': ['Alice', 'Bob', 'Charlie'],
            'city': ['NYC', 'LA', 'SF']
        })
        
        # Should handle gracefully
        stats = agent.generate_summary_statistics(df)
        assert stats is not None
        assert len(stats['numeric_summary']) == 0
        assert len(stats['categorical_summary']) > 0
