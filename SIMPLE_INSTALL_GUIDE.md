# 🚀 Super Simple Installation Guide

## Method 1: Microsoft Store (Easiest)
1. **Press Windows Key + S**
2. **Type "Microsoft Store"** and open it
3. **Search for "Python 3.11"**
4. **Click "Install"** (it's free)
5. **Wait for installation to complete**

## Method 2: Direct Download
1. **Go to**: https://www.python.org/downloads/
2. **Click the big yellow "Download Python" button**
3. **Run the downloaded file**
4. **✅ IMPORTANT: Check "Add Python to PATH"**
5. **Click "Install Now"**

## After Python is Installed

### Quick Test:
1. **Press Windows Key + R**
2. **Type "cmd"** and press Enter
3. **Type**: `python --version`
4. **You should see**: `Python 3.11.x`

### Run Our System:
1. **Double-click**: `setup_and_run.bat` in your project folder
2. **OR open Command Prompt in your project folder and type**:
   ```
   pip install pandas numpy scikit-learn matplotlib plotly fastapi uvicorn
   python main_pipeline.py
   python web_interface.py
   ```

## If You Get Stuck:

### Option A: Use Our Demo (No Python Needed)
- **Double-click**: `run_demo.bat`
- **OR open**: `sample_output_demo.html` in your browser

### Option B: Manual Commands
```bash
# Navigate to your project folder
cd "C:\Users\rpaod\student_enrollment_prediction"

# Install packages one by one
pip install pandas
pip install numpy
pip install scikit-learn
pip install matplotlib
pip install plotly
pip install fastapi
pip install uvicorn

# Run the system
python main_pipeline.py
python web_interface.py
```

## What Each File Does:

- **`run_demo.bat`** → Shows you what the system looks like (no Python needed)
- **`setup_and_run.bat`** → Installs everything and runs the full system
- **`main_pipeline.py`** → Creates data and trains AI models
- **`web_interface.py`** → Starts the professional dashboard
- **`api_server.py`** → Runs the prediction API

## Troubleshooting:

**"Python not found"**
→ Restart your computer after installing Python

**"Permission denied"**
→ Right-click Command Prompt and "Run as Administrator"

**"Module not found"**
→ Run: `pip install --upgrade pip` then try again

**Still stuck?**
→ Just run the demo! It shows everything the system can do.