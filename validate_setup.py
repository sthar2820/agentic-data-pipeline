#!/usr/bin/env python3
"""
Validation script to verify the project structure and setup.
"""

import os
from pathlib import Path
import sys

def check_directory_structure():
    """Check if all required directories exist."""
    print("🔍 Checking directory structure...")
    
    required_dirs = [
        'agents/inspector',
        'agents/refiner',
        'agents/insight',
        'orchestrator',
        'ui',
        'configs',
        'tests/agents',
        'tests/orchestrator',
        'tests/ui',
        'data/raw',
        'data/processed',
        'data/artifacts',
        'logs',
        '.github/workflows'
    ]
    
    all_exist = True
    for dir_path in required_dirs:
        path = Path(dir_path)
        if path.exists():
            print(f"  ✅ {dir_path}")
        else:
            print(f"  ❌ {dir_path} (missing)")
            all_exist = False
    
    return all_exist

def check_required_files():
    """Check if all required files exist."""
    print("\n📄 Checking required files...")
    
    required_files = [
        'README.md',
        'requirements.txt',
        'main.py',
        '.gitignore',
        'setup.cfg',
        'LICENSE',
        'CONTRIBUTING.md',
        'agents/__init__.py',
        'agents/inspector/__init__.py',
        'agents/inspector/inspector_agent.py',
        'agents/refiner/__init__.py',
        'agents/refiner/refiner_agent.py',
        'agents/insight/__init__.py',
        'agents/insight/insight_agent.py',
        'orchestrator/__init__.py',
        'orchestrator/orchestrator.py',
        'ui/app.py',
        'configs/pipeline_config.yaml',
        '.github/workflows/ci.yml',
        'tests/conftest.py',
        'tests/agents/test_inspector.py',
        'tests/agents/test_refiner.py',
        'tests/agents/test_insight.py',
        'tests/orchestrator/test_orchestrator.py',
        'generate_sample_data.py'
    ]
    
    all_exist = True
    for file_path in required_files:
        path = Path(file_path)
        if path.exists():
            size = path.stat().st_size
            print(f"  ✅ {file_path} ({size} bytes)")
        else:
            print(f"  ❌ {file_path} (missing)")
            all_exist = False
    
    return all_exist

def check_sample_data():
    """Check if sample data exists."""
    print("\n📊 Checking sample data...")
    
    sample_file = Path('data/raw/sample_customer_data.csv')
    if sample_file.exists():
        size = sample_file.stat().st_size
        print(f"  ✅ sample_customer_data.csv ({size} bytes)")
        return True
    else:
        print(f"  ⚠️  sample_customer_data.csv (not generated yet)")
        print("     Run: python generate_sample_data.py")
        return False

def check_python_syntax():
    """Check if all Python files have valid syntax."""
    print("\n🐍 Checking Python syntax...")
    
    python_files = list(Path('.').rglob('*.py'))
    all_valid = True
    
    for py_file in python_files:
        # Skip virtual env and hidden directories
        if any(part.startswith('.') or part == 'venv' or part == '__pycache__' for part in py_file.parts):
            continue
        
        try:
            with open(py_file, 'r') as f:
                compile(f.read(), py_file, 'exec')
            print(f"  ✅ {py_file}")
        except SyntaxError as e:
            print(f"  ❌ {py_file}: {e}")
            all_valid = False
    
    return all_valid

def check_line_counts():
    """Check line counts for major components."""
    print("\n📏 Component sizes (lines of code)...")
    
    components = {
        'Inspector Agent': 'agents/inspector/inspector_agent.py',
        'Refiner Agent': 'agents/refiner/refiner_agent.py',
        'Insight Agent': 'agents/insight/insight_agent.py',
        'Orchestrator': 'orchestrator/orchestrator.py',
        'Streamlit UI': 'ui/app.py',
        'Main CLI': 'main.py'
    }
    
    for name, file_path in components.items():
        path = Path(file_path)
        if path.exists():
            with open(path, 'r') as f:
                lines = len(f.readlines())
            print(f"  {name:20s}: {lines:4d} lines")
    
    return True

def main():
    """Run all validation checks."""
    print("=" * 60)
    print("🔬 Agentic Data Pipeline - Validation Report")
    print("=" * 60)
    
    results = []
    
    results.append(("Directory Structure", check_directory_structure()))
    results.append(("Required Files", check_required_files()))
    results.append(("Sample Data", check_sample_data()))
    results.append(("Python Syntax", check_python_syntax()))
    results.append(("Component Sizes", check_line_counts()))
    
    print("\n" + "=" * 60)
    print("📋 Summary")
    print("=" * 60)
    
    all_passed = True
    for check_name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"  {status:10s} {check_name}")
        if not passed:
            all_passed = False
    
    print("=" * 60)
    
    if all_passed:
        print("\n🎉 All validation checks passed!")
        print("\n📌 Next steps:")
        print("  1. Install dependencies: pip install -r requirements.txt")
        print("  2. Run tests: pytest")
        print("  3. Try the CLI: python main.py --input data/raw/sample_customer_data.csv")
        print("  4. Try the UI: streamlit run ui/app.py")
        return 0
    else:
        print("\n⚠️  Some validation checks failed. Please review the output above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
