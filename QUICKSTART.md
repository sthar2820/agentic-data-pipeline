# Quick Start Guide

This guide will help you get the Agentic Data Pipeline up and running quickly.

## Prerequisites

- Python 3.9 or higher
- pip package manager
- 2GB free disk space (for dependencies)

## Installation Steps

### 1. Clone the Repository

```bash
git clone https://github.com/sthar2820/agentic-data-pipeline.git
cd agentic-data-pipeline
```

### 2. Create Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate on Linux/Mac
source venv/bin/activate

# Activate on Windows
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

This will install all required packages including:
- Data processing: pandas, numpy
- Agent 1: ydata-profiling, great-expectations
- Agent 2: pyjanitor, rapidfuzz, scikit-learn
- Agent 3: matplotlib, seaborn, plotly
- UI: streamlit
- Utilities: loguru, pyyaml

**Note**: Installation may take 5-10 minutes depending on your internet connection.

### 4. Verify Installation

```bash
python validate_setup.py
```

You should see all checks pass with a green checkmark ✅.

## Quick Test

### Generate Sample Data

```bash
python generate_sample_data.py
```

This creates a sample customer dataset in `data/raw/sample_customer_data.csv`.

### Option 1: Run via Command Line

```bash
python main.py --input data/raw/sample_customer_data.csv
```

This will:
1. Profile the data (Inspector Agent)
2. Clean and transform it (Refiner Agent)
3. Generate visualizations (Insight Agent)
4. Save results to `data/artifacts/` and `data/processed/`

### Option 2: Run via Web UI

```bash
streamlit run ui/app.py
```

Then open your browser to `http://localhost:8501` and:
1. Upload your CSV file (or use the sample data)
2. Configure pipeline settings
3. Click "Run Pipeline"
4. View results and download processed data

## What Gets Generated

After running the pipeline, you'll find:

```
data/
├── artifacts/
│   ├── dataset_profile.html              # Interactive data report
│   ├── dataset_profile_stats.json        # Profile statistics
│   ├── validation_results.json           # Quality checks
│   ├── transformation_log.json           # Cleaning log
│   ├── summary_statistics.json           # Stats summary
│   ├── distribution_plots.png            # Visualizations
│   ├── correlation_heatmap.png           # Correlation plot
│   └── pipeline_metrics_dataset.json     # Execution metrics
├── processed/
│   └── sample_customer_data_processed.csv # Cleaned data
└── raw/
    └── sample_customer_data.csv          # Original data

logs/
└── pipeline_YYYYMMDD_HHMMSS.log         # Detailed logs
```

## Running Tests

```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=agents --cov=orchestrator --cov-report=html

# Run specific test
pytest tests/agents/test_inspector.py -v
```

## Common Issues

### Issue: ModuleNotFoundError

**Solution**: Make sure you've installed all dependencies:
```bash
pip install -r requirements.txt
```

### Issue: Permission Denied

**Solution**: On Linux/Mac, make scripts executable:
```bash
chmod +x main.py
```

### Issue: Port Already in Use (Streamlit)

**Solution**: Specify a different port:
```bash
streamlit run ui/app.py --server.port 8502
```

### Issue: Out of Memory

**Solution**: For large datasets, increase available memory or process in chunks.

## Configuration

Edit `configs/pipeline_config.yaml` to customize:

- Enable/disable specific agents
- Configure data paths
- Set cleaning strategies
- Adjust visualization settings

## Next Steps

1. **Explore the Code**: Check out the agent implementations in `agents/`
2. **Customize Agents**: Modify agent behavior for your use case
3. **Add Your Data**: Replace sample data with your own datasets
4. **Extend Pipeline**: Add new agents or operations
5. **Deploy**: Use the included CI/CD workflow for deployment

## Getting Help

- Read the [README.md](README.md) for detailed documentation
- Check [CONTRIBUTING.md](CONTRIBUTING.md) for development guidelines
- Open an issue on GitHub for bugs or questions

## Success Indicators

You'll know everything is working when:
- ✅ All validation checks pass
- ✅ Tests run successfully
- ✅ Pipeline processes sample data without errors
- ✅ Artifacts are generated in `data/artifacts/`
- ✅ Streamlit UI loads without errors

Happy analyzing! 🚀
