"""
Pipeline Orchestrator

Coordinates the execution of all agents in the data analytics pipeline:
1. Inspector Agent - Data profiling and validation
2. Refiner Agent - Data cleaning and transformation  
3. Insight Agent - EDA and visualization

Logs all metrics and artifacts throughout the pipeline execution.
"""

import pandas as pd
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime
from loguru import logger
import json
import yaml

from agents import InspectorAgent, RefinerAgent, InsightAgent


class PipelineOrchestrator:
    """
    Orchestrates the complete data analytics pipeline.
    """
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize the Pipeline Orchestrator.
        
        Args:
            config_path: Path to configuration file (YAML or JSON)
        """
        # Load configuration
        if config_path and Path(config_path).exists():
            self.config = self._load_config(config_path)
        else:
            self.config = self._get_default_config()
        
        # Setup paths
        self.data_path = Path(self.config.get('data_path', 'data'))
        self.artifacts_path = Path(self.config.get('artifacts_path', 'data/artifacts'))
        self.logs_path = Path(self.config.get('logs_path', 'logs'))
        
        # Create directories
        self.artifacts_path.mkdir(parents=True, exist_ok=True)
        self.logs_path.mkdir(parents=True, exist_ok=True)
        
        # Setup logging
        log_file = self.logs_path / f"pipeline_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        logger.add(log_file, rotation="10 MB", retention="30 days", level="INFO")
        
        # Initialize agents
        agent_config = {
            'artifacts_path': str(self.artifacts_path),
            'logs_path': str(self.logs_path)
        }
        
        self.inspector = InspectorAgent(agent_config)
        self.refiner = RefinerAgent(agent_config)
        self.insight = InsightAgent(agent_config)
        
        # Pipeline state
        self.pipeline_metrics = {
            'start_time': None,
            'end_time': None,
            'duration_seconds': None,
            'stages': []
        }
        
        logger.info("Pipeline Orchestrator initialized")
    
    def _load_config(self, config_path: str) -> Dict[str, Any]:
        """Load configuration from file."""
        config_path = Path(config_path)
        
        if config_path.suffix in ['.yaml', '.yml']:
            with open(config_path, 'r') as f:
                return yaml.safe_load(f)
        elif config_path.suffix == '.json':
            with open(config_path, 'r') as f:
                return json.load(f)
        else:
            raise ValueError(f"Unsupported config format: {config_path.suffix}")
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Get default configuration."""
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
                    'operations': [
                        'clean_column_names',
                        'handle_missing_values',
                        'remove_duplicates'
                    ]
                },
                'insight': {
                    'enabled': True,
                    'generate_plots': True
                }
            }
        }
    
    def load_data(self, file_path: str, **kwargs) -> pd.DataFrame:
        """
        Load data from file.
        
        Args:
            file_path: Path to data file
            **kwargs: Additional arguments for pandas read functions
            
        Returns:
            Loaded DataFrame
        """
        logger.info(f"Loading data from {file_path}")
        
        file_path = Path(file_path)
        
        if not file_path.exists():
            raise FileNotFoundError(f"Data file not found: {file_path}")
        
        # Determine file type and load
        if file_path.suffix == '.csv':
            df = pd.read_csv(file_path, **kwargs)
        elif file_path.suffix in ['.xlsx', '.xls']:
            df = pd.read_excel(file_path, **kwargs)
        elif file_path.suffix == '.json':
            df = pd.read_json(file_path, **kwargs)
        elif file_path.suffix == '.parquet':
            df = pd.read_parquet(file_path, **kwargs)
        else:
            raise ValueError(f"Unsupported file format: {file_path.suffix}")
        
        logger.info(f"Loaded data: {len(df)} rows, {len(df.columns)} columns")
        return df
    
    def save_data(self, df: pd.DataFrame, file_path: str, **kwargs):
        """
        Save DataFrame to file.
        
        Args:
            df: DataFrame to save
            file_path: Output file path
            **kwargs: Additional arguments for pandas write functions
        """
        logger.info(f"Saving data to {file_path}")
        
        file_path = Path(file_path)
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Save based on extension
        if file_path.suffix == '.csv':
            df.to_csv(file_path, index=False, **kwargs)
        elif file_path.suffix in ['.xlsx', '.xls']:
            df.to_excel(file_path, index=False, **kwargs)
        elif file_path.suffix == '.json':
            df.to_json(file_path, **kwargs)
        elif file_path.suffix == '.parquet':
            df.to_parquet(file_path, index=False, **kwargs)
        else:
            raise ValueError(f"Unsupported file format: {file_path.suffix}")
        
        logger.info(f"Data saved: {len(df)} rows, {len(df.columns)} columns")
    
    def run_pipeline(
        self, 
        input_data: str, 
        output_path: Optional[str] = None,
        dataset_name: str = "dataset"
    ) -> Dict[str, Any]:
        """
        Run the complete data analytics pipeline.
        
        Args:
            input_data: Path to input data file or DataFrame
            output_path: Optional path to save processed data
            dataset_name: Name of the dataset for reporting
            
        Returns:
            Dictionary containing pipeline results and metrics
        """
        logger.info("=" * 80)
        logger.info(f"Starting Pipeline for {dataset_name}")
        logger.info("=" * 80)
        
        self.pipeline_metrics['start_time'] = datetime.now().isoformat()
        
        try:
            # Stage 1: Load Data
            stage_start = datetime.now()
            if isinstance(input_data, str):
                df = self.load_data(input_data)
            elif isinstance(input_data, pd.DataFrame):
                df = input_data.copy()
            else:
                raise ValueError("input_data must be a file path or DataFrame")
            
            self.pipeline_metrics['stages'].append({
                'stage': 'load_data',
                'status': 'success',
                'duration_seconds': (datetime.now() - stage_start).total_seconds()
            })
            
            # Stage 2: Inspector Agent
            if self.config['pipeline']['inspector']['enabled']:
                stage_start = datetime.now()
                logger.info("\n" + "=" * 80)
                logger.info("Stage 1: Inspector Agent - Data Profiling & Validation")
                logger.info("=" * 80)
                
                inspector_results = self.inspector.run(df, dataset_name)
                
                self.pipeline_metrics['stages'].append({
                    'stage': 'inspector',
                    'status': inspector_results['status'],
                    'duration_seconds': (datetime.now() - stage_start).total_seconds(),
                    'results': inspector_results
                })
                
                logger.info(f"Inspector Agent: {inspector_results['status']}")
            
            # Stage 3: Refiner Agent
            if self.config['pipeline']['refiner']['enabled']:
                stage_start = datetime.now()
                logger.info("\n" + "=" * 80)
                logger.info("Stage 2: Refiner Agent - Data Cleaning & Transformation")
                logger.info("=" * 80)
                
                operations = self.config['pipeline']['refiner'].get('operations')
                df_refined, refiner_results = self.refiner.run(df, operations)
                
                self.pipeline_metrics['stages'].append({
                    'stage': 'refiner',
                    'status': refiner_results['status'],
                    'duration_seconds': (datetime.now() - stage_start).total_seconds(),
                    'results': refiner_results
                })
                
                logger.info(f"Refiner Agent: {refiner_results['status']}")
                
                # Use refined data for next stage
                df = df_refined
            
            # Stage 4: Insight Agent
            if self.config['pipeline']['insight']['enabled']:
                stage_start = datetime.now()
                logger.info("\n" + "=" * 80)
                logger.info("Stage 3: Insight Agent - EDA & Visualization")
                logger.info("=" * 80)
                
                insight_results = self.insight.run(df, dataset_name)
                
                self.pipeline_metrics['stages'].append({
                    'stage': 'insight',
                    'status': insight_results['status'],
                    'duration_seconds': (datetime.now() - stage_start).total_seconds(),
                    'results': insight_results
                })
                
                logger.info(f"Insight Agent: {insight_results['status']}")
            
            # Stage 5: Save Processed Data
            if output_path:
                stage_start = datetime.now()
                self.save_data(df, output_path)
                
                self.pipeline_metrics['stages'].append({
                    'stage': 'save_data',
                    'status': 'success',
                    'duration_seconds': (datetime.now() - stage_start).total_seconds(),
                    'output_path': output_path
                })
            
            # Finalize metrics
            self.pipeline_metrics['end_time'] = datetime.now().isoformat()
            self.pipeline_metrics['duration_seconds'] = (
                datetime.fromisoformat(self.pipeline_metrics['end_time']) -
                datetime.fromisoformat(self.pipeline_metrics['start_time'])
            ).total_seconds()
            self.pipeline_metrics['status'] = 'success'
            
            # Save metrics
            metrics_path = self.artifacts_path / f"pipeline_metrics_{dataset_name}.json"
            with open(metrics_path, 'w') as f:
                json.dump(self.pipeline_metrics, f, indent=2, default=str)
            
            logger.info("\n" + "=" * 80)
            logger.info("Pipeline Completed Successfully")
            logger.info(f"Total Duration: {self.pipeline_metrics['duration_seconds']:.2f} seconds")
            logger.info(f"Metrics saved to: {metrics_path}")
            logger.info("=" * 80)
            
            return {
                'status': 'success',
                'metrics': self.pipeline_metrics,
                'processed_data': df
            }
            
        except Exception as e:
            logger.error(f"Pipeline failed: {str(e)}")
            
            self.pipeline_metrics['end_time'] = datetime.now().isoformat()
            self.pipeline_metrics['status'] = 'failed'
            self.pipeline_metrics['error'] = str(e)
            
            return {
                'status': 'failed',
                'error': str(e),
                'metrics': self.pipeline_metrics
            }
    
    def get_metrics_summary(self) -> Dict[str, Any]:
        """
        Get a summary of pipeline metrics.
        
        Returns:
            Dictionary containing metrics summary
        """
        summary = {
            'total_duration': self.pipeline_metrics.get('duration_seconds'),
            'status': self.pipeline_metrics.get('status'),
            'stages': {}
        }
        
        for stage in self.pipeline_metrics.get('stages', []):
            summary['stages'][stage['stage']] = {
                'status': stage['status'],
                'duration': stage['duration_seconds']
            }
        
        return summary
