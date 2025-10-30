#!/usr/bin/env python3
"""
Agentic Data Pipeline - Main Entry Point

A clean, minimal pipeline with three AI agents:
- Inspector: Data profiling and validation
- Refiner: Data cleaning and transformation
- Insight: Analysis and visualization
"""

import argparse
from pathlib import Path
from loguru import logger


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Agentic Data Pipeline",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        '--input', '-i',
        type=str,
        required=True,
        help='Path to input CSV file'
    )
    
    parser.add_argument(
        '--output', '-o',
        type=str,
        help='Path to save processed data (optional)'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose logging'
    )
    
    args = parser.parse_args()
    
    # Setup logging
    logger.remove()
    level = "DEBUG" if args.verbose else "INFO"
    logger.add(
        lambda msg: print(msg, end=""),
        format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | {message}",
        level=level,
        colorize=True
    )
    
    # Validate input
    input_path = Path(args.input)
    if not input_path.exists():
        logger.error(f"Input file not found: {input_path}")
        return
    
    logger.info(f"🚀 Starting pipeline for: {input_path.name}")
    logger.info(f"📊 Dataset: {input_path.stem}")
    
    # TODO: Implement pipeline orchestration
    logger.warning("⚠️  Pipeline not yet implemented - building from scratch...")
    
    logger.info("✅ Ready to build!")


if __name__ == "__main__":
    main()
