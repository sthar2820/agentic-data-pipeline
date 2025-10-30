"""Tests for Pipeline Orchestrator."""

import pytest
import pandas as pd
from pathlib import Path
import sys
import json

sys.path.insert(0, str(Path(__file__).parent.parent))

from orchestrator import PipelineOrchestrator


class TestPipelineOrchestrator:
    """Test suite for Pipeline Orchestrator."""
    
    def test_initialization(self):
        """Test orchestrator initialization."""
        orchestrator = PipelineOrchestrator()
        assert orchestrator is not None
        assert orchestrator.inspector is not None
        assert orchestrator.refiner is not None
        assert orchestrator.insight is not None
    
    def test_initialization_with_config(self, tmp_path):
        """Test orchestrator initialization with config."""
        config_path = tmp_path / "test_config.yaml"
        config_content = """
data_path: data
artifacts_path: data/artifacts
logs_path: logs
pipeline:
  inspector:
    enabled: true
  refiner:
    enabled: true
  insight:
    enabled: true
"""
        config_path.write_text(config_content)
        
        orchestrator = PipelineOrchestrator(str(config_path))
        assert orchestrator is not None
        assert orchestrator.config is not None
    
    def test_load_data_csv(self, mock_csv_file):
        """Test CSV data loading."""
        orchestrator = PipelineOrchestrator()
        df = orchestrator.load_data(str(mock_csv_file))
        
        assert df is not None
        assert len(df) > 0
        assert len(df.columns) > 0
    
    def test_save_data_csv(self, sample_dataframe, tmp_path):
        """Test CSV data saving."""
        orchestrator = PipelineOrchestrator()
        output_path = tmp_path / "output.csv"
        
        orchestrator.save_data(sample_dataframe, str(output_path))
        
        assert output_path.exists()
        
        # Verify saved data
        df_loaded = pd.read_csv(output_path)
        assert len(df_loaded) == len(sample_dataframe)
    
    def test_run_pipeline_with_dataframe(self, sample_dataframe, tmp_path):
        """Test running pipeline with DataFrame input."""
        orchestrator = PipelineOrchestrator()
        
        output_path = tmp_path / "processed.csv"
        results = orchestrator.run_pipeline(
            input_data=sample_dataframe,
            output_path=str(output_path),
            dataset_name="test"
        )
        
        assert results is not None
        assert results['status'] == 'success'
        assert 'metrics' in results
        assert output_path.exists()
    
    def test_run_pipeline_with_file(self, mock_csv_file, tmp_path):
        """Test running pipeline with file input."""
        orchestrator = PipelineOrchestrator()
        
        output_path = tmp_path / "processed.csv"
        results = orchestrator.run_pipeline(
            input_data=str(mock_csv_file),
            output_path=str(output_path),
            dataset_name="test"
        )
        
        assert results is not None
        assert results['status'] == 'success'
        assert 'metrics' in results
        assert output_path.exists()
    
    def test_pipeline_metrics(self, sample_dataframe):
        """Test pipeline metrics collection."""
        orchestrator = PipelineOrchestrator()
        
        results = orchestrator.run_pipeline(
            input_data=sample_dataframe,
            dataset_name="test"
        )
        
        assert 'metrics' in results
        metrics = results['metrics']
        
        assert 'start_time' in metrics
        assert 'end_time' in metrics
        assert 'duration_seconds' in metrics
        assert 'stages' in metrics
        assert len(metrics['stages']) > 0
    
    def test_get_metrics_summary(self, sample_dataframe):
        """Test metrics summary retrieval."""
        orchestrator = PipelineOrchestrator()
        
        orchestrator.run_pipeline(
            input_data=sample_dataframe,
            dataset_name="test"
        )
        
        summary = orchestrator.get_metrics_summary()
        
        assert summary is not None
        assert 'total_duration' in summary
        assert 'status' in summary
        assert 'stages' in summary
