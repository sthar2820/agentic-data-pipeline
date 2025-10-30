"""
Insight Agent - EDA & Visualization

This agent performs exploratory data analysis and creates visualizations using:
- matplotlib for basic plots
- seaborn for statistical visualizations
- plotly for interactive plots
"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple
from loguru import logger
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json


class InsightAgent:
    """
    Agent responsible for exploratory data analysis and visualization.
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the Insight Agent.
        
        Args:
            config: Configuration dictionary containing paths and settings
        """
        self.config = config
        self.artifacts_path = Path(config.get('artifacts_path', 'data/artifacts'))
        self.artifacts_path.mkdir(parents=True, exist_ok=True)
        
        # Set style preferences
        sns.set_style("whitegrid")
        plt.rcParams['figure.figsize'] = (12, 8)
        
        self.insights = []
        logger.info("Insight Agent initialized")
    
    def generate_summary_statistics(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Generate comprehensive summary statistics.
        
        Args:
            df: Input DataFrame
            
        Returns:
            Dictionary containing summary statistics
        """
        logger.info("Generating summary statistics")
        
        try:
            stats = {
                'shape': {'rows': len(df), 'columns': len(df.columns)},
                'dtypes': df.dtypes.astype(str).to_dict(),
                'missing_values': df.isnull().sum().to_dict(),
                'numeric_summary': {},
                'categorical_summary': {}
            }
            
            # Numeric columns statistics
            numeric_cols = df.select_dtypes(include=['number']).columns
            if len(numeric_cols) > 0:
                numeric_stats = df[numeric_cols].describe().to_dict()
                for col in numeric_cols:
                    stats['numeric_summary'][col] = {
                        'mean': float(df[col].mean()),
                        'median': float(df[col].median()),
                        'std': float(df[col].std()),
                        'min': float(df[col].min()),
                        'max': float(df[col].max()),
                        'q25': float(df[col].quantile(0.25)),
                        'q75': float(df[col].quantile(0.75)),
                        'skewness': float(df[col].skew()),
                        'kurtosis': float(df[col].kurtosis())
                    }
            
            # Categorical columns statistics
            categorical_cols = df.select_dtypes(include=['object', 'category']).columns
            for col in categorical_cols:
                stats['categorical_summary'][col] = {
                    'unique_values': int(df[col].nunique()),
                    'most_common': str(df[col].mode()[0]) if len(df[col].mode()) > 0 else None,
                    'most_common_count': int(df[col].value_counts().iloc[0]) if len(df) > 0 else 0
                }
            
            # Save summary statistics
            stats_path = self.artifacts_path / "summary_statistics.json"
            with open(stats_path, 'w') as f:
                json.dump(stats, f, indent=2, default=str)
            
            self.insights.append({
                'type': 'summary_statistics',
                'path': str(stats_path)
            })
            
            logger.info("Summary statistics generated")
            return stats
            
        except Exception as e:
            logger.error(f"Error generating summary statistics: {str(e)}")
            raise
    
    def create_distribution_plots(self, df: pd.DataFrame) -> List[str]:
        """
        Create distribution plots for numeric columns.
        
        Args:
            df: Input DataFrame
            
        Returns:
            List of paths to saved plots
        """
        logger.info("Creating distribution plots")
        plot_paths = []
        
        try:
            numeric_cols = df.select_dtypes(include=['number']).columns
            
            if len(numeric_cols) == 0:
                logger.warning("No numeric columns for distribution plots")
                return plot_paths
            
            # Create histograms with KDE
            n_cols = min(len(numeric_cols), 3)
            n_rows = (len(numeric_cols) + n_cols - 1) // n_cols
            
            fig, axes = plt.subplots(n_rows, n_cols, figsize=(15, 5 * n_rows))
            axes = axes.flatten() if n_rows * n_cols > 1 else [axes]
            
            for idx, col in enumerate(numeric_cols):
                if idx < len(axes):
                    sns.histplot(df[col].dropna(), kde=True, ax=axes[idx])
                    axes[idx].set_title(f'Distribution of {col}')
                    axes[idx].set_xlabel(col)
                    axes[idx].set_ylabel('Frequency')
            
            # Hide empty subplots
            for idx in range(len(numeric_cols), len(axes)):
                axes[idx].set_visible(False)
            
            plt.tight_layout()
            dist_path = self.artifacts_path / "distribution_plots.png"
            plt.savefig(dist_path, dpi=300, bbox_inches='tight')
            plt.close()
            
            plot_paths.append(str(dist_path))
            self.insights.append({
                'type': 'distribution_plots',
                'path': str(dist_path)
            })
            
            logger.info(f"Distribution plots saved to {dist_path}")
            
            # Create interactive plotly version
            fig_plotly = make_subplots(
                rows=n_rows, cols=n_cols,
                subplot_titles=[col for col in numeric_cols]
            )
            
            for idx, col in enumerate(numeric_cols):
                row = idx // n_cols + 1
                col_pos = idx % n_cols + 1
                
                fig_plotly.add_trace(
                    go.Histogram(x=df[col].dropna(), name=col, showlegend=False),
                    row=row, col=col_pos
                )
            
            fig_plotly.update_layout(
                title_text="Distribution Plots",
                height=400 * n_rows,
                showlegend=False
            )
            
            plotly_path = self.artifacts_path / "distribution_plots_interactive.html"
            fig_plotly.write_html(plotly_path)
            plot_paths.append(str(plotly_path))
            
            logger.info(f"Interactive distribution plots saved to {plotly_path}")
            
            return plot_paths
            
        except Exception as e:
            logger.error(f"Error creating distribution plots: {str(e)}")
            raise
    
    def create_correlation_heatmap(self, df: pd.DataFrame) -> str:
        """
        Create a correlation heatmap for numeric columns.
        
        Args:
            df: Input DataFrame
            
        Returns:
            Path to saved plot
        """
        logger.info("Creating correlation heatmap")
        
        try:
            numeric_cols = df.select_dtypes(include=['number']).columns
            
            if len(numeric_cols) < 2:
                logger.warning("Need at least 2 numeric columns for correlation heatmap")
                return None
            
            # Calculate correlation matrix
            corr_matrix = df[numeric_cols].corr()
            
            # Create heatmap
            plt.figure(figsize=(12, 10))
            sns.heatmap(
                corr_matrix,
                annot=True,
                fmt='.2f',
                cmap='coolwarm',
                center=0,
                square=True,
                linewidths=1,
                cbar_kws={"shrink": 0.8}
            )
            plt.title('Correlation Heatmap', fontsize=16, pad=20)
            plt.tight_layout()
            
            heatmap_path = self.artifacts_path / "correlation_heatmap.png"
            plt.savefig(heatmap_path, dpi=300, bbox_inches='tight')
            plt.close()
            
            self.insights.append({
                'type': 'correlation_heatmap',
                'path': str(heatmap_path)
            })
            
            logger.info(f"Correlation heatmap saved to {heatmap_path}")
            
            # Create interactive plotly version
            fig_plotly = go.Figure(data=go.Heatmap(
                z=corr_matrix.values,
                x=corr_matrix.columns,
                y=corr_matrix.columns,
                colorscale='RdBu',
                zmid=0,
                text=corr_matrix.values,
                texttemplate='%{text:.2f}',
                textfont={"size": 10},
                colorbar=dict(title="Correlation")
            ))
            
            fig_plotly.update_layout(
                title='Correlation Heatmap',
                xaxis_title='Features',
                yaxis_title='Features',
                height=800,
                width=900
            )
            
            plotly_path = self.artifacts_path / "correlation_heatmap_interactive.html"
            fig_plotly.write_html(plotly_path)
            
            logger.info(f"Interactive correlation heatmap saved to {plotly_path}")
            
            return str(heatmap_path)
            
        except Exception as e:
            logger.error(f"Error creating correlation heatmap: {str(e)}")
            raise
    
    def create_categorical_plots(self, df: pd.DataFrame, max_categories: int = 10) -> List[str]:
        """
        Create bar plots for categorical columns.
        
        Args:
            df: Input DataFrame
            max_categories: Maximum number of categories to plot per column
            
        Returns:
            List of paths to saved plots
        """
        logger.info("Creating categorical plots")
        plot_paths = []
        
        try:
            categorical_cols = df.select_dtypes(include=['object', 'category']).columns
            
            if len(categorical_cols) == 0:
                logger.warning("No categorical columns for bar plots")
                return plot_paths
            
            for col in categorical_cols:
                value_counts = df[col].value_counts().head(max_categories)
                
                # Create bar plot
                plt.figure(figsize=(12, 6))
                sns.barplot(x=value_counts.values, y=value_counts.index, palette='viridis')
                plt.title(f'Top {max_categories} Categories in {col}', fontsize=14)
                plt.xlabel('Count')
                plt.ylabel(col)
                plt.tight_layout()
                
                plot_path = self.artifacts_path / f"categorical_{col}.png"
                plt.savefig(plot_path, dpi=300, bbox_inches='tight')
                plt.close()
                
                plot_paths.append(str(plot_path))
                self.insights.append({
                    'type': 'categorical_plot',
                    'column': col,
                    'path': str(plot_path)
                })
            
            logger.info(f"Created {len(categorical_cols)} categorical plots")
            return plot_paths
            
        except Exception as e:
            logger.error(f"Error creating categorical plots: {str(e)}")
            raise
    
    def create_boxplots(self, df: pd.DataFrame) -> str:
        """
        Create boxplots for numeric columns to identify outliers.
        
        Args:
            df: Input DataFrame
            
        Returns:
            Path to saved plot
        """
        logger.info("Creating boxplots")
        
        try:
            numeric_cols = df.select_dtypes(include=['number']).columns
            
            if len(numeric_cols) == 0:
                logger.warning("No numeric columns for boxplots")
                return None
            
            # Normalize data for better visualization
            df_normalized = df[numeric_cols].apply(lambda x: (x - x.mean()) / x.std())
            
            plt.figure(figsize=(14, 8))
            sns.boxplot(data=df_normalized, orient='h', palette='Set2')
            plt.title('Boxplots of Numeric Features (Normalized)', fontsize=16)
            plt.xlabel('Normalized Value')
            plt.tight_layout()
            
            boxplot_path = self.artifacts_path / "boxplots.png"
            plt.savefig(boxplot_path, dpi=300, bbox_inches='tight')
            plt.close()
            
            self.insights.append({
                'type': 'boxplots',
                'path': str(boxplot_path)
            })
            
            logger.info(f"Boxplots saved to {boxplot_path}")
            return str(boxplot_path)
            
        except Exception as e:
            logger.error(f"Error creating boxplots: {str(e)}")
            raise
    
    def run(self, df: pd.DataFrame, dataset_name: str = "dataset") -> Dict[str, Any]:
        """
        Run the complete insight generation pipeline.
        
        Args:
            df: Input DataFrame to analyze
            dataset_name: Name of the dataset
            
        Returns:
            Dictionary containing all analysis results
        """
        logger.info(f"Running Insight Agent on {dataset_name}")
        
        self.insights = []
        
        results = {
            'dataset_name': dataset_name,
            'summary_statistics': None,
            'visualizations': [],
            'insights': [],
            'status': 'success'
        }
        
        try:
            # Generate summary statistics
            results['summary_statistics'] = self.generate_summary_statistics(df)
            
            # Create visualizations
            dist_plots = self.create_distribution_plots(df)
            results['visualizations'].extend(dist_plots)
            
            corr_plot = self.create_correlation_heatmap(df)
            if corr_plot:
                results['visualizations'].append(corr_plot)
            
            cat_plots = self.create_categorical_plots(df)
            results['visualizations'].extend(cat_plots)
            
            box_plot = self.create_boxplots(df)
            if box_plot:
                results['visualizations'].append(box_plot)
            
            results['insights'] = self.insights
            
            # Save results summary
            summary_path = self.artifacts_path / "insight_summary.json"
            with open(summary_path, 'w') as f:
                json.dump({
                    'dataset_name': dataset_name,
                    'total_visualizations': len(results['visualizations']),
                    'insights': self.insights
                }, f, indent=2, default=str)
            
            logger.info(
                f"Insight Agent completed: {len(results['visualizations'])} visualizations created"
            )
            
        except Exception as e:
            logger.error(f"Insight Agent failed: {str(e)}")
            results['status'] = 'failed'
            results['error'] = str(e)
        
        return results
