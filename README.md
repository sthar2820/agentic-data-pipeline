# 🔬 Agentic Data Analytics Pipeline

An automated, intelligent data analytics pipeline powered by three specialized AI agents that work together to inspect, refine, and generate insights from your data.

[![CI Pipeline](https://github.com/sthar2820/agentic-data-pipeline/workflows/CI%20Pipeline/badge.svg)](https://github.com/sthar2820/agentic-data-pipeline/actions)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 📋 Overview

This pipeline uses a multi-agent architecture to automate the entire data analytics workflow:

1. **🔍 Inspector Agent** - Data profiling and quality validation
2. **🧹 Refiner Agent** - Data cleaning and transformation
3. **📊 Insight Agent** - Exploratory data analysis and visualization
4. **🎯 Orchestrator** - Coordinates all agents and manages the pipeline flow
5. **💻 Streamlit UI** - Interactive web interface for easy interaction

## ✨ Features

- ✅ **Automated Data Profiling** - Generate comprehensive data reports with ydata-profiling
- ✅ **Data Quality Validation** - Validate data using Great Expectations
- ✅ **Smart Data Cleaning** - Handle missing values, remove duplicates, unify categories
- ✅ **Advanced Transformations** - Fuzzy matching, imputation, normalization
- ✅ **Rich Visualizations** - Distribution plots, correlation heatmaps, categorical analysis
- ✅ **Interactive UI** - User-friendly Streamlit interface
- ✅ **Comprehensive Logging** - Track all operations with detailed metrics
- ✅ **Multiple File Formats** - Support for CSV, Excel, JSON, Parquet
- ✅ **CI/CD Ready** - GitHub Actions workflow included

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Streamlit UI / CLI                      │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
              ┌──────────────────────┐
              │    Orchestrator      │
              │  (Pipeline Manager)  │
              └──────────┬───────────┘
                         │
         ┌───────────────┼───────────────┐
         │               │               │
         ▼               ▼               ▼
┌────────────────┐ ┌────────────┐ ┌────────────┐
│   Inspector    │ │  Refiner   │ │  Insight   │
│     Agent      │ │   Agent    │ │   Agent    │
├────────────────┤ ├────────────┤ ├────────────┤
│ • Profiling    │ │ • Cleaning │ │ • EDA      │
│ • Validation   │ │ • Transform│ │ • Plots    │
│ • Quality      │ │ • Normalize│ │ • Stats    │
└────────────────┘ └────────────┘ └────────────┘
```

## 🚀 Quick Start

### Prerequisites

- Python 3.9 or higher
- pip package manager

### Installation

1. Clone the repository:
```bash
git clone https://github.com/sthar2820/agentic-data-pipeline.git
cd agentic-data-pipeline
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create necessary directories (already included):
```bash
# Directories are already created
data/
  ├── raw/          # Place your input data here
  ├── processed/    # Processed data will be saved here
  └── artifacts/    # Analysis artifacts (reports, plots, metrics)
logs/               # Pipeline logs
```

### Usage

#### Option 1: Command Line Interface (CLI)

```bash
# Basic usage
python main.py --input data/raw/your_data.csv

# With output path
python main.py --input data/raw/your_data.csv --output data/processed/output.csv

# With custom configuration
python main.py --input data/raw/your_data.csv --config configs/pipeline_config.yaml

# Verbose mode
python main.py --input data/raw/your_data.csv --verbose
```

#### Option 2: Streamlit Web UI

```bash
streamlit run ui/app.py
```

Then open your browser to `http://localhost:8501`

#### Option 3: Python API

```python
from orchestrator import PipelineOrchestrator

# Initialize orchestrator
orchestrator = PipelineOrchestrator(config_path='configs/pipeline_config.yaml')

# Run pipeline
results = orchestrator.run_pipeline(
    input_data='data/raw/your_data.csv',
    output_path='data/processed/output.csv',
    dataset_name='my_dataset'
)

# Check results
print(f"Status: {results['status']}")
print(f"Duration: {results['metrics']['duration_seconds']}s")
```

## 🔧 Configuration

Edit `configs/pipeline_config.yaml` to customize the pipeline:

```yaml
# Data paths
data_path: data
artifacts_path: data/artifacts
logs_path: logs

# Pipeline stages
pipeline:
  inspector:
    enabled: true
    profile: true
    validate: true
    
  refiner:
    enabled: true
    operations:
      - clean_column_names
      - handle_missing_values
      - remove_duplicates
    missing_strategy: smart
    
  insight:
    enabled: true
    generate_plots: true
```

## 📦 Agent Details

### 🔍 Inspector Agent

**Technologies:**
- `ydata-profiling` - Automated EDA and profiling
- `Great Expectations` - Data validation framework

**Capabilities:**
- Generate comprehensive data profile reports
- Validate data quality with custom expectations
- Detect missing values, duplicates, and anomalies
- Statistical analysis of all columns
- Data type inference and validation

### 🧹 Refiner Agent

**Technologies:**
- `pandas` - Core data manipulation
- `pyjanitor` - Data cleaning operations
- `rapidfuzz` - Fuzzy string matching
- `scikit-learn` - Imputation and normalization

**Capabilities:**
- Clean and standardize column names
- Handle missing values (multiple strategies)
- Remove duplicate records
- Unify similar categories using fuzzy matching
- Normalize numeric features
- Advanced imputation (KNN, median, mode)

### 📊 Insight Agent

**Technologies:**
- `matplotlib` - Static visualizations
- `seaborn` - Statistical plots
- `plotly` - Interactive visualizations

**Capabilities:**
- Generate distribution plots
- Create correlation heatmaps
- Analyze categorical variables
- Produce boxplots for outlier detection
- Interactive dashboards
- Summary statistics

## 🧪 Testing

Run the test suite:

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=agents --cov=orchestrator --cov-report=html

# Run specific test file
pytest tests/agents/test_inspector.py -v

# Run with verbose output
pytest -v
```

## 📊 Example Output

After running the pipeline, you'll find:

```
data/artifacts/
├── dataset_profile.html              # Interactive profile report
├── dataset_profile_stats.json        # Profile statistics
├── validation_results.json           # Data quality results
├── transformation_log.json           # Cleaning operations log
├── summary_statistics.json           # Statistical summary
├── distribution_plots.png            # Distribution visualizations
├── correlation_heatmap.png           # Correlation analysis
├── boxplots.png                      # Outlier detection
└── pipeline_metrics_dataset.json    # Pipeline execution metrics

logs/
└── pipeline_YYYYMMDD_HHMMSS.log     # Detailed execution logs
```

## 🛠️ Development

### Code Quality

```bash
# Format code
black agents/ orchestrator/ ui/ main.py

# Sort imports
isort agents/ orchestrator/ ui/ main.py

# Lint code
flake8 agents/ orchestrator/ ui/

# Type checking
mypy agents/ orchestrator/
```

### Project Structure

```
agentic-data-pipeline/
├── agents/                    # Agent modules
│   ├── inspector/            # Inspector agent
│   ├── refiner/              # Refiner agent
│   └── insight/              # Insight agent
├── orchestrator/             # Pipeline orchestrator
├── ui/                       # Streamlit UI
├── configs/                  # Configuration files
├── tests/                    # Test suite
│   ├── agents/              # Agent tests
│   ├── orchestrator/        # Orchestrator tests
│   └── conftest.py          # Test fixtures
├── data/                     # Data directories
│   ├── raw/                 # Input data
│   ├── processed/           # Output data
│   └── artifacts/           # Analysis artifacts
├── logs/                     # Log files
├── .github/workflows/        # CI/CD workflows
├── main.py                   # CLI entry point
├── requirements.txt          # Python dependencies
└── README.md                # This file
```

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [ydata-profiling](https://github.com/ydataai/ydata-profiling) for automated profiling
- [Great Expectations](https://greatexpectations.io/) for data validation
- [pyjanitor](https://github.com/pyjanitor-devs/pyjanitor) for data cleaning
- [Streamlit](https://streamlit.io/) for the web framework

## 📧 Contact

For questions or feedback, please open an issue on GitHub.

---

Made with ❤️ by the community
