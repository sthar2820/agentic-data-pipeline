"""
Inspector Agent - Data Quality & Profiling

This agent performs comprehensive data quality checks and profiling using:
- ydata-profiling for automated EDA
- Great Expectations for data validation
"""

import pandas as pd
from pathlib import Path
from typing import Dict, Any, Optional
from loguru import logger
from ydata_profiling import ProfileReport
import great_expectations as ge
from great_expectations.core.batch import RuntimeBatchRequest
from great_expectations.data_context import FileDataContext
import json


class InspectorAgent:
    """
    Agent responsible for data inspection, profiling, and quality validation.
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the Inspector Agent.
        
        Args:
            config: Configuration dictionary containing paths and settings
        """
        self.config = config
        self.artifacts_path = Path(config.get('artifacts_path', 'data/artifacts'))
        self.artifacts_path.mkdir(parents=True, exist_ok=True)
        logger.info("Inspector Agent initialized")
    
    def profile_data(self, df: pd.DataFrame, dataset_name: str = "dataset") -> Dict[str, Any]:
        """
        Generate a comprehensive data profile using ydata-profiling.
        
        Args:
            df: Input DataFrame to profile
            dataset_name: Name of the dataset for reporting
            
        Returns:
            Dictionary containing profile statistics
        """
        logger.info(f"Generating profile for {dataset_name}")
        
        try:
            # Generate profile report
            profile = ProfileReport(
                df,
                title=f"{dataset_name} Profile Report",
                explorative=True,
                minimal=False
            )
            
            # Save HTML report
            report_path = self.artifacts_path / f"{dataset_name}_profile.html"
            profile.to_file(report_path)
            logger.info(f"Profile report saved to {report_path}")
            
            # Extract key statistics
            stats = {
                'n_rows': len(df),
                'n_columns': len(df.columns),
                'n_cells_missing': df.isnull().sum().sum(),
                'n_duplicates': df.duplicated().sum(),
                'memory_size': df.memory_usage(deep=True).sum(),
                'numeric_columns': list(df.select_dtypes(include=['number']).columns),
                'categorical_columns': list(df.select_dtypes(include=['object', 'category']).columns),
                'datetime_columns': list(df.select_dtypes(include=['datetime64']).columns),
            }
            
            # Save stats to JSON
            stats_path = self.artifacts_path / f"{dataset_name}_profile_stats.json"
            with open(stats_path, 'w') as f:
                json.dump(stats, f, indent=2, default=str)
            
            logger.info(f"Profile statistics: {stats['n_rows']} rows, {stats['n_columns']} columns")
            return stats
            
        except Exception as e:
            logger.error(f"Error generating profile: {str(e)}")
            raise
    
    def validate_data(self, df: pd.DataFrame, expectations: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Validate data quality using Great Expectations.
        
        Args:
            df: Input DataFrame to validate
            expectations: Optional custom expectations to apply
            
        Returns:
            Dictionary containing validation results
        """
        logger.info("Validating data quality")
        
        try:
            # Convert to Great Expectations DataFrame
            ge_df = ge.from_pandas(df)
            
            # Apply default expectations if none provided
            if expectations is None:
                expectations = self._get_default_expectations(df)
            
            # Run validations
            validation_results = {
                'total_expectations': 0,
                'successful_expectations': 0,
                'failed_expectations': 0,
                'success_percent': 0.0,
                'results': []
            }
            
            for expectation_name, expectation_args in expectations.items():
                try:
                    # Execute expectation
                    if hasattr(ge_df, expectation_name):
                        result = getattr(ge_df, expectation_name)(**expectation_args)
                        validation_results['total_expectations'] += 1
                        
                        if result.success:
                            validation_results['successful_expectations'] += 1
                        else:
                            validation_results['failed_expectations'] += 1
                        
                        validation_results['results'].append({
                            'expectation': expectation_name,
                            'success': result.success,
                            'args': expectation_args
                        })
                except Exception as e:
                    logger.warning(f"Expectation {expectation_name} failed: {str(e)}")
            
            # Calculate success percentage
            if validation_results['total_expectations'] > 0:
                validation_results['success_percent'] = (
                    validation_results['successful_expectations'] / 
                    validation_results['total_expectations'] * 100
                )
            
            # Save validation results
            results_path = self.artifacts_path / "validation_results.json"
            with open(results_path, 'w') as f:
                json.dump(validation_results, f, indent=2)
            
            logger.info(
                f"Validation complete: {validation_results['successful_expectations']}/"
                f"{validation_results['total_expectations']} passed "
                f"({validation_results['success_percent']:.1f}%)"
            )
            
            return validation_results
            
        except Exception as e:
            logger.error(f"Error validating data: {str(e)}")
            raise
    
    def _get_default_expectations(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Generate default expectations based on the DataFrame structure.
        
        Args:
            df: Input DataFrame
            
        Returns:
            Dictionary of expectation names and their arguments
        """
        expectations = {}
        
        # Expect table to exist and have rows
        expectations['expect_table_row_count_to_be_between'] = {
            'min_value': 1,
            'max_value': None
        }
        
        # Expect no completely null columns
        for col in df.columns:
            if df[col].notna().any():
                expectations[f'expect_column_values_to_not_be_null_{col}'] = {
                    'column': col
                }
        
        return expectations
    
    def run(self, df: pd.DataFrame, dataset_name: str = "dataset") -> Dict[str, Any]:
        """
        Run the complete inspection pipeline.
        
        Args:
            df: Input DataFrame to inspect
            dataset_name: Name of the dataset
            
        Returns:
            Dictionary containing all inspection results
        """
        logger.info(f"Running Inspector Agent on {dataset_name}")
        
        results = {
            'dataset_name': dataset_name,
            'profile': None,
            'validation': None,
            'status': 'success'
        }
        
        try:
            # Profile the data
            results['profile'] = self.profile_data(df, dataset_name)
            
            # Validate the data
            results['validation'] = self.validate_data(df)
            
            logger.info("Inspector Agent completed successfully")
            
        except Exception as e:
            logger.error(f"Inspector Agent failed: {str(e)}")
            results['status'] = 'failed'
            results['error'] = str(e)
        
        return results
