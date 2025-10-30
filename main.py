#!/usr/bin/env python3
"""
Main CLI for Agentic Data Pipeline

Usage:
    python main.py --input data/raw/sample.csv --output data/processed/output.csv
    python main.py --input data/raw/sample.csv --config configs/pipeline_config.yaml
"""

import argparse
import sys
from pathlib import Path
from loguru import logger

from orchestrator import PipelineOrchestrator


def setup_logging(verbose: bool = False):
    """Configure logging."""
    logger.remove()  # Remove default handler
    
    level = "DEBUG" if verbose else "INFO"
    logger.add(
        sys.stderr,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <level>{message}</level>",
        level=level
    )


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Agentic Data Analytics Pipeline",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic usage
  python main.py --input data/raw/sample.csv

  # With output path
  python main.py --input data/raw/sample.csv --output data/processed/output.csv

  # With custom config
  python main.py --input data/raw/sample.csv --config configs/pipeline_config.yaml

  # Verbose mode
  python main.py --input data/raw/sample.csv --verbose
        """
    )
    
    parser.add_argument(
        '--input', '-i',
        type=str,
        required=True,
        help='Path to input data file (CSV, Excel, JSON, or Parquet)'
    )
    
    parser.add_argument(
        '--output', '-o',
        type=str,
        default=None,
        help='Path to save processed data (default: data/processed/<input_name>_processed.csv)'
    )
    
    parser.add_argument(
        '--config', '-c',
        type=str,
        default='configs/pipeline_config.yaml',
        help='Path to pipeline configuration file (default: configs/pipeline_config.yaml)'
    )
    
    parser.add_argument(
        '--name', '-n',
        type=str,
        default=None,
        help='Dataset name for reporting (default: derived from input filename)'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose logging'
    )
    
    args = parser.parse_args()
    
    # Setup logging
    setup_logging(args.verbose)
    
    # Validate input file
    input_path = Path(args.input)
    if not input_path.exists():
        logger.error(f"Input file not found: {input_path}")
        sys.exit(1)
    
    # Determine dataset name
    dataset_name = args.name or input_path.stem
    
    # Determine output path
    if args.output is None:
        output_path = f"data/processed/{dataset_name}_processed.csv"
    else:
        output_path = args.output
    
    # Check config file
    config_path = args.config
    if not Path(config_path).exists():
        logger.warning(f"Config file not found: {config_path}. Using default configuration.")
        config_path = None
    
    try:
        # Initialize orchestrator
        logger.info("Initializing Pipeline Orchestrator")
        orchestrator = PipelineOrchestrator(config_path)
        
        # Run pipeline
        logger.info(f"Processing dataset: {dataset_name}")
        logger.info(f"Input: {input_path}")
        logger.info(f"Output: {output_path}")
        
        results = orchestrator.run_pipeline(
            input_data=str(input_path),
            output_path=output_path,
            dataset_name=dataset_name
        )
        
        # Display results
        if results['status'] == 'success':
            logger.success("✅ Pipeline completed successfully!")
            
            metrics_summary = orchestrator.get_metrics_summary()
            logger.info(f"Total Duration: {metrics_summary['total_duration']:.2f} seconds")
            
            logger.info("Stage Summary:")
            for stage_name, stage_info in metrics_summary['stages'].items():
                logger.info(f"  {stage_name}: {stage_info['status']} ({stage_info['duration']:.2f}s)")
            
            logger.info(f"Processed data saved to: {output_path}")
            logger.info(f"Artifacts saved to: data/artifacts/")
            
            sys.exit(0)
        else:
            logger.error(f"❌ Pipeline failed: {results.get('error', 'Unknown error')}")
            sys.exit(1)
    
    except Exception as e:
        logger.exception(f"Fatal error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
