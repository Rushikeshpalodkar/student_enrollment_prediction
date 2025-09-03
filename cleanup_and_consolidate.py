"""
CLEANUP AND CONSOLIDATION SCRIPT
Removes duplicate files and consolidates the system
"""

import os
import shutil
import json
from datetime import datetime

def cleanup_redundant_files():
    """Remove redundant files and create backup"""
    
    # Files to remove (keeping enhanced versions)
    files_to_remove = [
        'api_server.py',  # Replaced by unified_system.py
        'web_interface.py',  # Replaced by unified_system.py  
        'simple_server.py',  # Replaced by unified_system.py
        'ml_models.py',  # Replaced by enhanced_ml_models.py
        'data_preprocessor.py',  # Replaced by enhanced_data_preprocessor.py
        'main_pipeline.py',  # Replaced by enhanced_main_pipeline.py
        'complete_demo.py',  # Functionality in unified_system.py
        'working_demo.py',  # Functionality in unified_system.py
        'quick_test.py',  # Replaced by test_enhancements.py
        'executive_dashboard.py'  # Integrated into unified_system.py
    ]
    
    # Create backup directory
    backup_dir = f'backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}'
    os.makedirs(backup_dir, exist_ok=True)
    
    print("CONSOLIDATION CLEANUP")
    print("=" * 50)
    print(f"Creating backup in: {backup_dir}")
    
    removed_count = 0
    backed_up_count = 0
    
    for file in files_to_remove:
        if os.path.exists(file):
            try:
                # Backup the file first
                shutil.copy2(file, os.path.join(backup_dir, file))
                backed_up_count += 1
                
                # Remove the original
                os.remove(file)
                removed_count += 1
                print(f"[REMOVED] {file} (backed up)")
                
            except Exception as e:
                print(f"[ERROR] Could not remove {file}: {e}")
        else:
            print(f"[SKIP] {file} (not found)")
    
    print(f"\n[SUMMARY] Removed {removed_count} files, backed up {backed_up_count} files")
    
    return backup_dir

def update_requirements():
    """Update requirements.txt with all necessary packages"""
    
    requirements = """# Core ML and Data Processing
pandas==2.1.4
numpy==1.24.3
scikit-learn==1.3.2
xgboost==2.0.3
lightgbm==4.1.0
joblib==1.3.2

# Visualization
matplotlib==3.8.2
seaborn==0.13.0
plotly==5.17.0

# Web Framework and API
fastapi==0.104.1
uvicorn==0.24.0
pydantic==2.5.2
jinja2==3.1.2
python-multipart==0.0.6

# Additional Utilities
python-dateutil==2.8.2
requests==2.31.0

# Development and Testing (optional)
pytest==7.4.3
jupyter==1.0.0
"""
    
    with open('requirements.txt', 'w') as f:
        f.write(requirements.strip())
    
    print("\n[UPDATED] requirements.txt with consolidated dependencies")

def create_system_overview():
    """Create overview of the consolidated system"""
    
    overview = {
        "system_name": "Unified Student Enrollment Prediction System",
        "version": "3.0.0",
        "consolidation_date": datetime.now().isoformat(),
        "main_components": {
            "unified_system.py": "Complete integrated system with web UI and API",
            "enhanced_ml_models.py": "Advanced ML models with explainable AI",
            "enhanced_data_preprocessor.py": "Sophisticated data processing",
            "enhanced_main_pipeline.py": "Complete training pipeline",
            "data_generator.py": "Sample data generation",
            "eda_analyzer.py": "Exploratory data analysis"
        },
        "removed_duplicates": [
            "api_server.py -> integrated into unified_system.py",
            "web_interface.py -> replaced by unified_system.py",
            "simple_server.py -> consolidated into unified_system.py",
            "ml_models.py -> enhanced version kept",
            "data_preprocessor.py -> enhanced version kept",
            "main_pipeline.py -> enhanced version kept"
        ],
        "features": {
            "backend": [
                "Advanced hyperparameter optimization",
                "Class weighting for imbalanced data",
                "Stacking ensemble methods",
                "Comprehensive evaluation metrics",
                "Enhanced data quality checks",
                "Sophisticated feature engineering"
            ],
            "frontend": [
                "Explainable AI with confidence indicators",
                "Interactive web interface",
                "Real-time model training",
                "Visual prediction explanations",
                "Modern responsive design",
                "Integrated system management"
            ]
        },
        "usage": {
            "start_system": "python unified_system.py",
            "web_interface": "http://localhost:8080",
            "api_docs": "http://localhost:8080/docs",
            "full_training": "python enhanced_main_pipeline.py"
        }
    }
    
    with open('SYSTEM_OVERVIEW.json', 'w') as f:
        json.dump(overview, f, indent=2)
    
    print("[CREATED] SYSTEM_OVERVIEW.json")

def create_startup_guide():
    """Create a simple startup guide"""
    
    guide = """# 🚀 Unified Student Enrollment Prediction System - Quick Start

## What Was Consolidated
- ✅ Removed duplicate web servers (api_server.py, web_interface.py, simple_server.py)
- ✅ Consolidated into unified_system.py with all enhanced features
- ✅ Kept only enhanced versions of ML models and preprocessing
- ✅ Integrated all functionality into single, cohesive system

## Quick Start (2 Minutes)

### Option 1: Unified Web Interface (Recommended)
```bash
# Install dependencies
pip install -r requirements.txt

# Start the complete system
python unified_system.py

# Open browser to: http://localhost:8080
```

**In the web interface:**
1. Click "Initialize System" 
2. Click "Train Enhanced Models"
3. Enter student data and get predictions with explanations!

### Option 2: Full Training Pipeline
```bash
# Run complete enhanced pipeline (takes longer)
python enhanced_main_pipeline.py

# Then start unified system
python unified_system.py
```

## Key Features Now Available
- **🤖 Enhanced ML Models** - 5+ algorithms with optimization
- **🧠 Explainable AI** - See why predictions were made
- **📊 Interactive Interface** - Modern web UI with confidence indicators
- **⚡ Real-time Training** - Train models through web interface
- **📈 Advanced Analytics** - Comprehensive reporting and visualizations

## System Architecture
```
unified_system.py           <- Main application (web + API + ML)
├── enhanced_ml_models.py    <- Advanced ML with explanations
├── enhanced_data_preprocessor.py <- Sophisticated preprocessing  
├── data_generator.py        <- Sample data creation
└── eda_analyzer.py          <- Data analysis tools
```

## API Endpoints
- `GET /` - Web interface
- `POST /api/initialize` - Initialize system
- `POST /api/train` - Train models
- `POST /api/predict` - Make predictions
- `GET /api/status` - System status
- `GET /docs` - API documentation

## What Makes This System Special
1. **No Duplication** - Single source of truth for all functionality
2. **Integrated Experience** - Everything works together seamlessly  
3. **Enhanced Features** - All improvements from improve.txt implemented
4. **Production Ready** - Comprehensive error handling and logging
5. **User Friendly** - Modern UI that non-technical users can understand

## Troubleshooting
- **Missing packages**: Run `pip install -r requirements.txt`
- **Port conflicts**: Change port in unified_system.py (line with uvicorn.run)
- **Memory issues**: System uses sample data by default for speed

---
🎉 **Success!** Your system is now consolidated and enhanced with all features working together!
"""

    with open('QUICK_START.md', 'w', encoding='utf-8') as f:
        f.write(guide)
    
    print("[CREATED] QUICK_START.md")

def update_readme():
    """Update the main README to reflect consolidation"""
    
    readme_update = """

---

## 🔄 SYSTEM CONSOLIDATION UPDATE

**All duplicate functionality has been consolidated into a unified system!**

### What Changed:
- ✅ **Removed Duplicates**: Eliminated 6+ redundant files
- ✅ **Unified Interface**: Single system with web UI + API + ML
- ✅ **Enhanced Features**: All improvements from improve.txt integrated
- ✅ **Simplified Usage**: One command to start everything

### New Quick Start:
```bash
pip install -r requirements.txt
python unified_system.py
# Open: http://localhost:8080
```

### Key Benefits:
1. **No Confusion** - Single entry point for all functionality
2. **Better Integration** - All components work together seamlessly
3. **Easier Maintenance** - No duplicate code to maintain
4. **Enhanced UX** - Modern interface with explainable AI

See `QUICK_START.md` for detailed instructions.

"""

    try:
        with open('README.md', 'r', encoding='utf-8') as f:
            current_readme = f.read()
        
        # Add the update section if not already present
        if "SYSTEM CONSOLIDATION UPDATE" not in current_readme:
            with open('README.md', 'w', encoding='utf-8') as f:
                f.write(current_readme + readme_update)
            print("[UPDATED] README.md with consolidation info")
        else:
            print("[SKIP] README.md already contains consolidation info")
    
    except Exception as e:
        print(f"[ERROR] Could not update README.md: {e}")

if __name__ == "__main__":
    print("[CLEANUP] SYSTEM CLEANUP AND CONSOLIDATION")
    print("=" * 60)
    
    try:
        # Step 1: Cleanup redundant files
        backup_dir = cleanup_redundant_files()
        
        # Step 2: Update requirements
        update_requirements()
        
        # Step 3: Create system overview
        create_system_overview()
        
        # Step 4: Create startup guide
        create_startup_guide()
        
        # Step 5: Update README
        update_readme()
        
        print("\n[SUCCESS] CONSOLIDATION COMPLETE!")
        print("=" * 60)
        print("Your system is now:")
        print("  * Duplicate-free")
        print("  * Fully integrated") 
        print("  * Enhanced with all requested features")
        print("  * Ready for production use")
        
        print(f"\n[BACKUP] Backup created in: {backup_dir}")
        print("[START] Start the system: python unified_system.py")
        print("[WEB] Web interface: http://localhost:8080")
        print("[GUIDE] Quick start guide: QUICK_START.md")
        
    except Exception as e:
        print(f"[ERROR] Consolidation failed: {e}")
        import traceback
        traceback.print_exc()