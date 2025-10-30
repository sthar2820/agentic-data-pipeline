# Pipeline Flow Diagram

## 🔄 Complete Data Analytics Pipeline Flow

```
┌────────────────────────────────────────────────────────────────────┐
│                         USER INTERFACES                             │
├────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌──────────────────┐              ┌──────────────────┐           │
│  │   CLI Interface  │              │  Streamlit Web   │           │
│  │    (main.py)     │              │   UI (app.py)    │           │
│  └────────┬─────────┘              └────────┬─────────┘           │
│           │                                  │                      │
│           └──────────────┬───────────────────┘                      │
└───────────────────────────┼────────────────────────────────────────┘
                            │
                            ▼
┌────────────────────────────────────────────────────────────────────┐
│                       ORCHESTRATOR                                  │
│                  (orchestrator/orchestrator.py)                     │
├────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  • Loads data from various formats (CSV, Excel, JSON, Parquet)    │
│  • Coordinates agent execution                                     │
│  • Manages pipeline state and metrics                              │
│  • Saves processed data and artifacts                              │
│                                                                     │
└────────────────────────────────────────────────────────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
        ▼                   ▼                   ▼
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│   AGENT 1    │    │   AGENT 2    │    │   AGENT 3    │
│  Inspector   │───▶│   Refiner    │───▶│   Insight    │
│              │    │              │    │              │
├──────────────┤    ├──────────────┤    ├──────────────┤
│              │    │              │    │              │
│ Data         │    │ Data         │    │ Data         │
│ Profiling:   │    │ Cleaning:    │    │ Analysis:    │
│              │    │              │    │              │
│ • ydata-     │    │ • pandas     │    │ • matplotlib │
│   profiling  │    │ • pyjanitor  │    │ • seaborn    │
│ • Great      │    │ • rapidfuzz  │    │ • plotly     │
│   Expectations│   │ • sklearn    │    │              │
│              │    │              │    │              │
│ Outputs:     │    │ Operations:  │    │ Generates:   │
│ • Profile    │    │ • Clean      │    │ • Stats      │
│   reports    │    │   columns    │    │ • Plots      │
│ • Quality    │    │ • Handle     │    │ • Heatmaps   │
│   metrics    │    │   missing    │    │ • Reports    │
│ • Stats      │    │ • Remove     │    │              │
│   JSON       │    │   duplicates │    │              │
│              │    │ • Normalize  │    │              │
└──────────────┘    └──────────────┘    └──────────────┘
        │                   │                   │
        └───────────────────┼───────────────────┘
                            │
                            ▼
┌────────────────────────────────────────────────────────────────────┐
│                         OUTPUTS                                     │
├────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  data/artifacts/                                                   │
│  ├── dataset_profile.html          # Interactive profile report   │
│  ├── dataset_profile_stats.json    # Profile statistics           │
│  ├── validation_results.json       # Data quality results         │
│  ├── transformation_log.json       # Cleaning operations log      │
│  ├── summary_statistics.json       # Statistical summary          │
│  ├── distribution_plots.png        # Distribution visualizations  │
│  ├── correlation_heatmap.png       # Correlation analysis         │
│  ├── boxplots.png                  # Outlier detection            │
│  └── pipeline_metrics.json         # Pipeline execution metrics   │
│                                                                     │
│  data/processed/                                                   │
│  └── dataset_processed.csv         # Cleaned data                 │
│                                                                     │
│  logs/                                                             │
│  └── pipeline_YYYYMMDD_HHMMSS.log # Detailed execution logs       │
│                                                                     │
└────────────────────────────────────────────────────────────────────┘
```

## 📊 Data Flow Example

### Input:
```
Raw CSV with 500 rows, 13 columns
- Missing values: 100 cells
- Duplicates: 9 rows
- Inconsistent categories: 15%
```

### After Inspector Agent:
```
✓ Profile report generated
✓ 10 quality checks performed
✓ 8/10 quality checks passed
✓ Issues identified and documented
```

### After Refiner Agent:
```
✓ Column names standardized
✓ Missing values handled (smart imputation)
✓ Duplicates removed (9 rows)
✓ Categories unified (fuzzy matching)
✓ Result: 491 clean rows
```

### After Insight Agent:
```
✓ 5 distribution plots created
✓ Correlation heatmap generated
✓ 3 categorical plots produced
✓ Boxplots for outlier detection
✓ Summary statistics computed
```

## 🔄 Pipeline Execution Flow

1. **Initialization**
   - Load configuration
   - Initialize agents
   - Setup logging

2. **Data Loading**
   - Read input file
   - Validate format
   - Create DataFrame

3. **Agent Execution**
   - Run Inspector → profile + validate
   - Run Refiner → clean + transform
   - Run Insight → analyze + visualize

4. **Output Generation**
   - Save processed data
   - Export artifacts
   - Generate metrics
   - Write logs

5. **Completion**
   - Display summary
   - Return results
   - Clean up resources

## ⚙️ Configuration Options

```yaml
pipeline:
  inspector:
    enabled: true      # Run profiling
    profile: true      # Generate HTML report
    validate: true     # Run quality checks
    
  refiner:
    enabled: true      # Run cleaning
    operations:
      - clean_column_names
      - handle_missing_values
      - remove_duplicates
    missing_strategy: smart
    
  insight:
    enabled: true      # Run analysis
    generate_plots: true
    max_categories: 10
```

## 🎯 Key Features

### Modularity
- Each agent is independent
- Easy to add new agents
- Flexible pipeline configuration

### Observability
- Comprehensive logging
- Metrics tracking
- Artifact management

### Extensibility
- Plugin architecture
- Custom expectations
- Configurable operations

### Usability
- CLI for automation
- Web UI for exploration
- Clear documentation

---

**Pipeline Status**: ✅ Production Ready
**Total Processing Time**: ~30-60 seconds for 500 rows
**Supported Formats**: CSV, Excel, JSON, Parquet
**Output Formats**: CSV, JSON, PNG, HTML
