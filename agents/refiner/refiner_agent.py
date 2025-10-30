"""
Refiner Agent - Data Cleaning & Transformation

This agent performs data cleaning and transformation using:
- pandas for core data manipulation
- pyjanitor for cleaning operations
- rapidfuzz for fuzzy matching and deduplication
- sklearn for imputation and normalization
"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple
from loguru import logger
import janitor
from rapidfuzz import fuzz, process
from sklearn.impute import SimpleImputer, KNNImputer
from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler
import json


class RefinerAgent:
    """
    Agent responsible for data cleaning, transformation, and refinement.
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the Refiner Agent.
        
        Args:
            config: Configuration dictionary containing paths and settings
        """
        self.config = config
        self.artifacts_path = Path(config.get('artifacts_path', 'data/artifacts'))
        self.artifacts_path.mkdir(parents=True, exist_ok=True)
        self.transformation_log = []
        logger.info("Refiner Agent initialized")
    
    def clean_column_names(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Clean and standardize column names using pyjanitor.
        
        Args:
            df: Input DataFrame
            
        Returns:
            DataFrame with cleaned column names
        """
        logger.info("Cleaning column names")
        
        try:
            df_cleaned = df.clean_names()
            self.transformation_log.append({
                'operation': 'clean_column_names',
                'columns_before': list(df.columns),
                'columns_after': list(df_cleaned.columns)
            })
            logger.info(f"Column names cleaned: {len(df.columns)} columns standardized")
            return df_cleaned
        except Exception as e:
            logger.error(f"Error cleaning column names: {str(e)}")
            raise
    
    def handle_missing_values(
        self, 
        df: pd.DataFrame, 
        strategy: str = 'smart',
        numeric_strategy: str = 'median',
        categorical_strategy: str = 'most_frequent'
    ) -> pd.DataFrame:
        """
        Handle missing values using various imputation strategies.
        
        Args:
            df: Input DataFrame
            strategy: Overall strategy ('smart', 'simple', 'knn', 'drop')
            numeric_strategy: Strategy for numeric columns ('mean', 'median', 'most_frequent')
            categorical_strategy: Strategy for categorical columns ('most_frequent', 'constant')
            
        Returns:
            DataFrame with missing values handled
        """
        logger.info(f"Handling missing values with strategy: {strategy}")
        
        try:
            df_clean = df.copy()
            missing_before = df.isnull().sum().sum()
            
            if strategy == 'drop':
                # Drop rows with any missing values
                df_clean = df_clean.dropna()
                self.transformation_log.append({
                    'operation': 'handle_missing_values',
                    'strategy': 'drop',
                    'rows_dropped': len(df) - len(df_clean)
                })
            
            elif strategy == 'simple':
                # Simple imputation for numeric columns
                numeric_cols = df_clean.select_dtypes(include=['number']).columns
                if len(numeric_cols) > 0:
                    imputer = SimpleImputer(strategy=numeric_strategy)
                    df_clean[numeric_cols] = imputer.fit_transform(df_clean[numeric_cols])
                
                # Simple imputation for categorical columns
                categorical_cols = df_clean.select_dtypes(include=['object', 'category']).columns
                if len(categorical_cols) > 0:
                    imputer = SimpleImputer(strategy=categorical_strategy)
                    df_clean[categorical_cols] = imputer.fit_transform(df_clean[categorical_cols])
                
                self.transformation_log.append({
                    'operation': 'handle_missing_values',
                    'strategy': 'simple',
                    'numeric_strategy': numeric_strategy,
                    'categorical_strategy': categorical_strategy
                })
            
            elif strategy == 'knn':
                # KNN imputation for numeric columns
                numeric_cols = df_clean.select_dtypes(include=['number']).columns
                if len(numeric_cols) > 0:
                    imputer = KNNImputer(n_neighbors=5)
                    df_clean[numeric_cols] = imputer.fit_transform(df_clean[numeric_cols])
                
                # Most frequent for categorical
                categorical_cols = df_clean.select_dtypes(include=['object', 'category']).columns
                if len(categorical_cols) > 0:
                    imputer = SimpleImputer(strategy='most_frequent')
                    df_clean[categorical_cols] = imputer.fit_transform(df_clean[categorical_cols])
                
                self.transformation_log.append({
                    'operation': 'handle_missing_values',
                    'strategy': 'knn'
                })
            
            elif strategy == 'smart':
                # Smart strategy: choose based on missing percentage
                for col in df_clean.columns:
                    missing_pct = df_clean[col].isnull().sum() / len(df_clean) * 100
                    
                    if missing_pct > 50:
                        # Drop columns with >50% missing
                        df_clean = df_clean.drop(columns=[col])
                    elif missing_pct > 0:
                        # Impute based on data type
                        if df_clean[col].dtype in ['int64', 'float64']:
                            df_clean[col].fillna(df_clean[col].median(), inplace=True)
                        else:
                            df_clean[col].fillna(df_clean[col].mode()[0] if len(df_clean[col].mode()) > 0 else 'Unknown', inplace=True)
                
                self.transformation_log.append({
                    'operation': 'handle_missing_values',
                    'strategy': 'smart'
                })
            
            missing_after = df_clean.isnull().sum().sum()
            logger.info(f"Missing values: {missing_before} → {missing_after}")
            
            return df_clean
            
        except Exception as e:
            logger.error(f"Error handling missing values: {str(e)}")
            raise
    
    def remove_duplicates(self, df: pd.DataFrame, subset: Optional[List[str]] = None) -> pd.DataFrame:
        """
        Remove duplicate rows from the DataFrame.
        
        Args:
            df: Input DataFrame
            subset: Optional list of columns to consider for duplicates
            
        Returns:
            DataFrame with duplicates removed
        """
        logger.info("Removing duplicates")
        
        try:
            duplicates_before = df.duplicated(subset=subset).sum()
            df_dedup = df.drop_duplicates(subset=subset, keep='first')
            duplicates_removed = len(df) - len(df_dedup)
            
            self.transformation_log.append({
                'operation': 'remove_duplicates',
                'duplicates_removed': duplicates_removed,
                'subset': subset
            })
            
            logger.info(f"Duplicates removed: {duplicates_removed}")
            return df_dedup
            
        except Exception as e:
            logger.error(f"Error removing duplicates: {str(e)}")
            raise
    
    def unify_categories(
        self, 
        df: pd.DataFrame, 
        column: str, 
        similarity_threshold: float = 80.0
    ) -> pd.DataFrame:
        """
        Unify similar category values using fuzzy matching.
        
        Args:
            df: Input DataFrame
            column: Column name to unify
            similarity_threshold: Minimum similarity score (0-100) to consider a match
            
        Returns:
            DataFrame with unified categories
        """
        logger.info(f"Unifying categories in column: {column}")
        
        try:
            if column not in df.columns:
                logger.warning(f"Column {column} not found, skipping")
                return df
            
            df_unified = df.copy()
            unique_values = df_unified[column].dropna().unique()
            
            # Create mapping of similar values
            value_mapping = {}
            processed = set()
            
            for value in unique_values:
                if value in processed:
                    continue
                
                # Find similar values
                matches = process.extract(
                    str(value), 
                    [str(v) for v in unique_values],
                    scorer=fuzz.ratio,
                    limit=None
                )
                
                # Group similar values
                similar_group = [match[0] for match in matches if match[1] >= similarity_threshold]
                
                if len(similar_group) > 1:
                    # Use the most common value as the canonical form
                    canonical = max(similar_group, key=lambda x: (df_unified[column] == x).sum())
                    for similar_value in similar_group:
                        value_mapping[similar_value] = canonical
                        processed.add(similar_value)
            
            # Apply mapping
            if value_mapping:
                df_unified[column] = df_unified[column].replace(value_mapping)
                
                self.transformation_log.append({
                    'operation': 'unify_categories',
                    'column': column,
                    'unified_count': len(value_mapping),
                    'threshold': similarity_threshold
                })
                
                logger.info(f"Unified {len(value_mapping)} category values in {column}")
            else:
                logger.info(f"No categories needed unification in {column}")
            
            return df_unified
            
        except Exception as e:
            logger.error(f"Error unifying categories: {str(e)}")
            raise
    
    def normalize_numeric_columns(
        self, 
        df: pd.DataFrame, 
        method: str = 'standard',
        columns: Optional[List[str]] = None
    ) -> pd.DataFrame:
        """
        Normalize numeric columns using various scaling methods.
        
        Args:
            df: Input DataFrame
            method: Normalization method ('standard', 'minmax', 'robust')
            columns: Optional list of specific columns to normalize
            
        Returns:
            DataFrame with normalized numeric columns
        """
        logger.info(f"Normalizing numeric columns with method: {method}")
        
        try:
            df_normalized = df.copy()
            
            # Select numeric columns
            if columns is None:
                numeric_cols = df_normalized.select_dtypes(include=['number']).columns.tolist()
            else:
                numeric_cols = [col for col in columns if col in df_normalized.columns]
            
            if len(numeric_cols) == 0:
                logger.warning("No numeric columns to normalize")
                return df_normalized
            
            # Apply scaling
            if method == 'standard':
                scaler = StandardScaler()
            elif method == 'minmax':
                scaler = MinMaxScaler()
            elif method == 'robust':
                scaler = RobustScaler()
            else:
                raise ValueError(f"Unknown normalization method: {method}")
            
            df_normalized[numeric_cols] = scaler.fit_transform(df_normalized[numeric_cols])
            
            self.transformation_log.append({
                'operation': 'normalize_numeric_columns',
                'method': method,
                'columns': numeric_cols
            })
            
            logger.info(f"Normalized {len(numeric_cols)} numeric columns")
            return df_normalized
            
        except Exception as e:
            logger.error(f"Error normalizing columns: {str(e)}")
            raise
    
    def run(self, df: pd.DataFrame, operations: Optional[List[str]] = None) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        """
        Run the complete refinement pipeline.
        
        Args:
            df: Input DataFrame to refine
            operations: Optional list of operations to perform (default: all)
            
        Returns:
            Tuple of (refined DataFrame, results dictionary)
        """
        logger.info("Running Refiner Agent")
        
        self.transformation_log = []
        df_refined = df.copy()
        
        # Default operations
        if operations is None:
            operations = [
                'clean_column_names',
                'handle_missing_values',
                'remove_duplicates'
            ]
        
        results = {
            'operations_performed': [],
            'rows_before': len(df),
            'rows_after': 0,
            'columns_before': len(df.columns),
            'columns_after': 0,
            'status': 'success'
        }
        
        try:
            # Execute operations
            if 'clean_column_names' in operations:
                df_refined = self.clean_column_names(df_refined)
                results['operations_performed'].append('clean_column_names')
            
            if 'handle_missing_values' in operations:
                df_refined = self.handle_missing_values(df_refined, strategy='smart')
                results['operations_performed'].append('handle_missing_values')
            
            if 'remove_duplicates' in operations:
                df_refined = self.remove_duplicates(df_refined)
                results['operations_performed'].append('remove_duplicates')
            
            if 'normalize' in operations:
                df_refined = self.normalize_numeric_columns(df_refined)
                results['operations_performed'].append('normalize')
            
            # Update results
            results['rows_after'] = len(df_refined)
            results['columns_after'] = len(df_refined.columns)
            results['transformation_log'] = self.transformation_log
            
            # Save transformation log
            log_path = self.artifacts_path / "transformation_log.json"
            with open(log_path, 'w') as f:
                json.dump(self.transformation_log, f, indent=2)
            
            logger.info(
                f"Refiner Agent completed: {results['rows_before']} → {results['rows_after']} rows, "
                f"{results['columns_before']} → {results['columns_after']} columns"
            )
            
        except Exception as e:
            logger.error(f"Refiner Agent failed: {str(e)}")
            results['status'] = 'failed'
            results['error'] = str(e)
        
        return df_refined, results
