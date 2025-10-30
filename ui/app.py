"""
Streamlit UI for Data Analytics Pipeline

Interactive web interface for:
- Uploading datasets
- Running the analytics pipeline
- Viewing analysis results and visualizations
- Downloading processed data
"""

import streamlit as st
import pandas as pd
import sys
from pathlib import Path
import json
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from orchestrator import PipelineOrchestrator
from agents import InsightAgent


# Page configuration
st.set_page_config(
    page_title="Agentic Data Pipeline",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)


def load_css():
    """Apply custom CSS styling."""
    st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .agent-card {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .metric-card {
        background-color: #e8f4f8;
        padding: 1rem;
        border-radius: 5px;
        text-align: center;
    }
    .success-box {
        background-color: #d4edda;
        border-left: 5px solid #28a745;
        padding: 1rem;
        margin: 1rem 0;
    }
    .error-box {
        background-color: #f8d7da;
        border-left: 5px solid #dc3545;
        padding: 1rem;
        margin: 1rem 0;
    }
    </style>
    """, unsafe_allow_html=True)


def main():
    """Main Streamlit application."""
    
    load_css()
    
    # Header
    st.markdown('<h1 class="main-header">🔬 Agentic Data Analytics Pipeline</h1>', unsafe_allow_html=True)
    st.markdown("---")
    
    # Sidebar
    with st.sidebar:
        st.image("https://via.placeholder.com/300x100/1f77b4/ffffff?text=Data+Pipeline", use_column_width=True)
        st.title("Navigation")
        
        page = st.radio(
            "Select a page:",
            ["Home", "Upload & Process", "View Results", "About"]
        )
        
        st.markdown("---")
        st.markdown("### Pipeline Stages")
        st.markdown("1. 🔍 **Inspector** - Data Profiling")
        st.markdown("2. 🧹 **Refiner** - Data Cleaning")
        st.markdown("3. 📊 **Insight** - Visualization")
    
    # Main content based on page selection
    if page == "Home":
        show_home_page()
    elif page == "Upload & Process":
        show_upload_page()
    elif page == "View Results":
        show_results_page()
    elif page == "About":
        show_about_page()


def show_home_page():
    """Display the home page."""
    
    st.header("Welcome to the Agentic Data Analytics Pipeline")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('<div class="agent-card">', unsafe_allow_html=True)
        st.markdown("### 🔍 Inspector Agent")
        st.markdown("""
        **Data Quality & Profiling**
        - Automated data profiling
        - Quality validation
        - Statistical analysis
        - Missing data detection
        """)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="agent-card">', unsafe_allow_html=True)
        st.markdown("### 🧹 Refiner Agent")
        st.markdown("""
        **Data Cleaning & Transformation**
        - Missing value imputation
        - Duplicate removal
        - Category unification
        - Data normalization
        """)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="agent-card">', unsafe_allow_html=True)
        st.markdown("### 📊 Insight Agent")
        st.markdown("""
        **EDA & Visualization**
        - Distribution analysis
        - Correlation heatmaps
        - Category plots
        - Interactive dashboards
        """)
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.header("Getting Started")
    st.markdown("""
    1. Navigate to **Upload & Process** to upload your dataset
    2. Configure pipeline settings
    3. Run the analytics pipeline
    4. View results and visualizations
    5. Download processed data
    """)
    
    st.info("💡 **Tip**: Supported formats: CSV, Excel, JSON, Parquet")


def show_upload_page():
    """Display the upload and processing page."""
    
    st.header("📤 Upload & Process Data")
    
    # File upload
    uploaded_file = st.file_uploader(
        "Upload your dataset",
        type=['csv', 'xlsx', 'xls', 'json', 'parquet'],
        help="Supported formats: CSV, Excel, JSON, Parquet"
    )
    
    if uploaded_file is not None:
        # Save uploaded file temporarily
        temp_path = Path("data/raw") / uploaded_file.name
        temp_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(temp_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        st.success(f"✅ File uploaded: {uploaded_file.name}")
        
        # Load and preview data
        try:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(temp_path)
            elif uploaded_file.name.endswith(('.xlsx', '.xls')):
                df = pd.read_excel(temp_path)
            elif uploaded_file.name.endswith('.json'):
                df = pd.read_json(temp_path)
            elif uploaded_file.name.endswith('.parquet'):
                df = pd.read_parquet(temp_path)
            
            # Data preview
            st.subheader("Data Preview")
            st.dataframe(df.head(10), use_container_width=True)
            
            # Data info
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Rows", len(df))
            with col2:
                st.metric("Columns", len(df.columns))
            with col3:
                st.metric("Missing Values", df.isnull().sum().sum())
            with col4:
                st.metric("Duplicates", df.duplicated().sum())
            
            st.markdown("---")
            
            # Pipeline configuration
            st.subheader("⚙️ Pipeline Configuration")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Enable Agents:**")
                enable_inspector = st.checkbox("🔍 Inspector Agent", value=True)
                enable_refiner = st.checkbox("🧹 Refiner Agent", value=True)
                enable_insight = st.checkbox("📊 Insight Agent", value=True)
            
            with col2:
                st.markdown("**Refiner Options:**")
                clean_names = st.checkbox("Clean column names", value=True)
                handle_missing = st.checkbox("Handle missing values", value=True)
                remove_dups = st.checkbox("Remove duplicates", value=True)
            
            dataset_name = st.text_input("Dataset Name", value=uploaded_file.name.split('.')[0])
            
            # Run pipeline button
            if st.button("🚀 Run Pipeline", type="primary", use_container_width=True):
                with st.spinner("Running pipeline... This may take a few minutes."):
                    try:
                        # Initialize orchestrator
                        config = {
                            'data_path': 'data',
                            'artifacts_path': 'data/artifacts',
                            'logs_path': 'logs',
                            'pipeline': {
                                'inspector': {'enabled': enable_inspector},
                                'refiner': {
                                    'enabled': enable_refiner,
                                    'operations': []
                                },
                                'insight': {'enabled': enable_insight}
                            }
                        }
                        
                        if clean_names:
                            config['pipeline']['refiner']['operations'].append('clean_column_names')
                        if handle_missing:
                            config['pipeline']['refiner']['operations'].append('handle_missing_values')
                        if remove_dups:
                            config['pipeline']['refiner']['operations'].append('remove_duplicates')
                        
                        # Create temporary config file
                        config_path = Path("data/artifacts/temp_config.json")
                        with open(config_path, 'w') as f:
                            json.dump(config, f)
                        
                        orchestrator = PipelineOrchestrator(str(config_path))
                        
                        # Run pipeline
                        output_path = f"data/processed/{dataset_name}_processed.csv"
                        results = orchestrator.run_pipeline(
                            str(temp_path),
                            output_path=output_path,
                            dataset_name=dataset_name
                        )
                        
                        if results['status'] == 'success':
                            st.markdown('<div class="success-box">', unsafe_allow_html=True)
                            st.success("✅ Pipeline completed successfully!")
                            st.markdown('</div>', unsafe_allow_html=True)
                            
                            # Show metrics
                            metrics = results['metrics']
                            st.subheader("Pipeline Metrics")
                            
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                st.metric("Total Duration", f"{metrics['duration_seconds']:.2f}s")
                            with col2:
                                st.metric("Stages Completed", len(metrics['stages']))
                            with col3:
                                st.metric("Status", metrics['status'].upper())
                            
                            # Stage breakdown
                            st.subheader("Stage Breakdown")
                            for stage in metrics['stages']:
                                with st.expander(f"**{stage['stage'].title()}** - {stage['status']}"):
                                    st.write(f"Duration: {stage['duration_seconds']:.2f} seconds")
                                    if 'results' in stage:
                                        st.json(stage['results'])
                            
                            # Download button
                            if Path(output_path).exists():
                                with open(output_path, 'rb') as f:
                                    st.download_button(
                                        label="📥 Download Processed Data",
                                        data=f,
                                        file_name=f"{dataset_name}_processed.csv",
                                        mime="text/csv",
                                        use_container_width=True
                                    )
                        
                        else:
                            st.markdown('<div class="error-box">', unsafe_allow_html=True)
                            st.error(f"❌ Pipeline failed: {results.get('error', 'Unknown error')}")
                            st.markdown('</div>', unsafe_allow_html=True)
                    
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")
        
        except Exception as e:
            st.error(f"❌ Error loading file: {str(e)}")


def show_results_page():
    """Display the results and visualizations page."""
    
    st.header("📊 View Results")
    
    artifacts_path = Path("data/artifacts")
    
    if not artifacts_path.exists() or not list(artifacts_path.glob("*")):
        st.info("No results available yet. Please upload and process a dataset first.")
        return
    
    # List available result files
    st.subheader("Available Artifacts")
    
    # Profile reports
    profile_reports = list(artifacts_path.glob("*_profile.html"))
    if profile_reports:
        st.markdown("### 📋 Profile Reports")
        for report in profile_reports:
            st.markdown(f"- [{report.name}]({report})")
    
    # Visualizations
    viz_files = list(artifacts_path.glob("*.png")) + list(artifacts_path.glob("*.html"))
    viz_files = [f for f in viz_files if '_profile' not in f.name]
    
    if viz_files:
        st.markdown("### 📈 Visualizations")
        
        # Display images
        image_files = [f for f in viz_files if f.suffix == '.png']
        for img_file in image_files:
            with st.expander(f"📊 {img_file.stem.replace('_', ' ').title()}"):
                st.image(str(img_file), use_column_width=True)
    
    # JSON results
    json_files = list(artifacts_path.glob("*.json"))
    if json_files:
        st.markdown("### 📄 Analysis Results")
        
        for json_file in json_files:
            with st.expander(f"📝 {json_file.stem.replace('_', ' ').title()}"):
                try:
                    with open(json_file, 'r') as f:
                        data = json.load(f)
                    st.json(data)
                except:
                    st.error("Could not load file")


def show_about_page():
    """Display the about page."""
    
    st.header("About This Pipeline")
    
    st.markdown("""
    ## 🔬 Agentic Data Analytics Pipeline
    
    This is an automated data analytics pipeline powered by three specialized AI agents:
    
    ### Architecture
    
    The pipeline consists of:
    - **3 Agents**: Inspector, Refiner, Insight
    - **1 Orchestrator**: Coordinates agent execution
    - **Streamlit UI**: Interactive web interface
    
    ### Technologies Used
    
    #### Agent 1: Inspector
    - `ydata-profiling` - Automated data profiling
    - `Great Expectations` - Data quality validation
    
    #### Agent 2: Refiner
    - `pandas` - Core data manipulation
    - `pyjanitor` - Data cleaning operations
    - `rapidfuzz` - Fuzzy matching for deduplication
    - `scikit-learn` - Imputation and normalization
    
    #### Agent 3: Insight
    - `matplotlib` - Static visualizations
    - `seaborn` - Statistical plots
    - `plotly` - Interactive visualizations
    
    #### Infrastructure
    - `streamlit` - Web UI framework
    - `loguru` - Advanced logging
    - `pytest` - Testing framework
    
    ### Features
    
    ✅ Automated data profiling and quality checks  
    ✅ Smart data cleaning and transformation  
    ✅ Comprehensive EDA and visualizations  
    ✅ Interactive web interface  
    ✅ Detailed logging and metrics  
    ✅ Support for multiple file formats  
    
    ### License
    
    MIT License - Feel free to use and modify!
    
    ---
    
    Made with ❤️ using Python and Streamlit
    """)


if __name__ == "__main__":
    main()
