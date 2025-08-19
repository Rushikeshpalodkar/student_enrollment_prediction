@echo off
echo ========================================
echo Student Enrollment Prediction System
echo Professional Setup Script
echo ========================================
echo.

echo Step 1: Checking Python installation...
python --version
if %errorlevel% neq 0 (
    echo.
    echo ERROR: Python is not installed or not in PATH
    echo.
    echo Please install Python from: https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation
    echo.
    echo After installing Python, run this script again.
    pause
    exit /b 1
)

echo.
echo Step 2: Installing required packages...
echo This may take a few minutes...
pip install pandas numpy scikit-learn matplotlib seaborn plotly fastapi uvicorn pydantic

echo.
echo Step 3: Creating necessary directories...
if not exist "models" mkdir models
if not exist "outputs" mkdir outputs
if not exist "templates" mkdir templates
if not exist "static" mkdir static

echo.
echo Step 4: Running the main pipeline...
echo This will generate sample data and train ML models...
python main_pipeline.py

echo.
echo Step 5: Starting the web interface...
echo The dashboard will be available at: http://localhost:8080
echo Press Ctrl+C to stop the server
echo.
python web_interface.py

pause