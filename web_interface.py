from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import json
from datetime import datetime
import os

# Create FastAPI app for web interface
web_app = FastAPI(title="Student Enrollment Dashboard")

# Setup templates and static files
os.makedirs("templates", exist_ok=True)
os.makedirs("static", exist_ok=True)

templates = Jinja2Templates(directory="templates")
web_app.mount("/static", StaticFiles(directory="static"), name="static")

class WebInterface:
    def __init__(self):
        self.setup_templates()
    
    def setup_templates(self):
        """Create HTML templates for the web interface"""
        
        # Main dashboard template
        dashboard_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Student Enrollment Prediction Dashboard</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <style>
        .hero-section {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 4rem 0;
        }
        .card {
            border: none;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            margin-bottom: 2rem;
        }
        .metric-card {
            background: linear-gradient(45deg, #4CAF50, #45a049);
            color: white;
            text-align: center;
            padding: 2rem;
            border-radius: 10px;
        }
        .metric-value {
            font-size: 2.5rem;
            font-weight: bold;
        }
        .metric-label {
            font-size: 1.1rem;
            opacity: 0.9;
        }
        .sidebar {
            background-color: #f8f9fa;
            min-height: 100vh;
            padding: 2rem 1rem;
        }
        .nav-link {
            color: #495057;
            padding: 0.75rem 1rem;
            margin: 0.25rem 0;
            border-radius: 5px;
        }
        .nav-link:hover, .nav-link.active {
            background-color: #007bff;
            color: white;
        }
    </style>
</head>
<body>
    <!-- Navigation -->
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
        <div class="container">
            <a class="navbar-brand" href="/">📊 Enrollment Prediction System</a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav ms-auto">
                    <li class="nav-item"><a class="nav-link" href="#dashboard">Dashboard</a></li>
                    <li class="nav-item"><a class="nav-link" href="#predictions">Predictions</a></li>
                    <li class="nav-item"><a class="nav-link" href="#reports">Reports</a></li>
                    <li class="nav-item"><a class="nav-link" href="#help">Help</a></li>
                </ul>
            </div>
        </div>
    </nav>

    <!-- Hero Section -->
    <section class="hero-section">
        <div class="container text-center">
            <h1 class="display-4 mb-4">Smart Enrollment Predictions</h1>
            <p class="lead">Data-driven insights for better academic planning and student success</p>
            <div class="row mt-5">
                <div class="col-md-3">
                    <div class="metric-card">
                        <div class="metric-value">4,750</div>
                        <div class="metric-label">Predicted Enrollment</div>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="metric-card">
                        <div class="metric-value">91.5%</div>
                        <div class="metric-label">Prediction Accuracy</div>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="metric-card">
                        <div class="metric-value">$1.2M</div>
                        <div class="metric-label">Cost Savings</div>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="metric-card">
                        <div class="metric-value">84.2%</div>
                        <div class="metric-label">Retention Rate</div>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- Main Content -->
    <div class="container-fluid mt-4">
        <div class="row">
            <!-- Sidebar -->
            <div class="col-md-2 sidebar">
                <h5>Quick Actions</h5>
                <nav class="nav flex-column">
                    <a class="nav-link active" href="#" onclick="showSection('overview')">📈 Overview</a>
                    <a class="nav-link" href="#" onclick="showSection('enrollment')">🎓 Enrollment</a>
                    <a class="nav-link" href="#" onclick="showSection('capacity')">🏫 Capacity</a>
                    <a class="nav-link" href="#" onclick="showSection('success')">⭐ Success Metrics</a>
                    <a class="nav-link" href="#" onclick="showSection('financial')">💰 Financial</a>
                    <a class="nav-link" href="#" onclick="showSection('reports')">📋 Reports</a>
                </nav>
                
                <h5 class="mt-4">Latest Updates</h5>
                <div class="alert alert-info">
                    <small><strong>Today:</strong> New predictions generated for Fall 2024</small>
                </div>
                <div class="alert alert-warning">
                    <small><strong>Alert:</strong> CS department at 95% capacity</small>
                </div>
            </div>

            <!-- Main Dashboard -->
            <div class="col-md-10">
                <!-- Overview Section -->
                <div id="overview-section">
                    <h2>Enrollment Overview</h2>
                    <div class="row">
                        <div class="col-md-8">
                            <div class="card">
                                <div class="card-header">
                                    <h5>Enrollment Forecast by Major</h5>
                                </div>
                                <div class="card-body">
                                    <div id="enrollment-chart"></div>
                                </div>
                            </div>
                        </div>
                        <div class="col-md-4">
                            <div class="card">
                                <div class="card-header">
                                    <h5>Department Distribution</h5>
                                </div>
                                <div class="card-body">
                                    <div id="department-pie"></div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Enrollment Section -->
                <div id="enrollment-section" style="display: none;">
                    <h2>Detailed Enrollment Analysis</h2>
                    <div class="card">
                        <div class="card-body">
                            <div id="detailed-enrollment"></div>
                        </div>
                    </div>
                </div>

                <!-- Capacity Section -->
                <div id="capacity-section" style="display: none;">
                    <h2>Capacity Planning</h2>
                    <div class="card">
                        <div class="card-body">
                            <div id="capacity-analysis"></div>
                        </div>
                    </div>
                </div>

                <!-- Student Prediction Form -->
                <div class="card mt-4">
                    <div class="card-header">
                        <h5>Individual Student Prediction</h5>
                    </div>
                    <div class="card-body">
                        <form id="prediction-form">
                            <div class="row">
                                <div class="col-md-4">
                                    <label class="form-label">Student ID</label>
                                    <input type="text" class="form-control" name="student_id" placeholder="e.g., STU001">
                                </div>
                                <div class="col-md-4">
                                    <label class="form-label">Current GPA</label>
                                    <input type="number" class="form-control" name="gpa" step="0.01" min="0" max="4" placeholder="3.5">
                                </div>
                                <div class="col-md-4">
                                    <label class="form-label">Age</label>
                                    <input type="number" class="form-control" name="age" min="16" max="60" placeholder="20">
                                </div>
                            </div>
                            <div class="row mt-3">
                                <div class="col-md-4">
                                    <label class="form-label">Total Credits</label>
                                    <input type="number" class="form-control" name="total_credits" min="0" placeholder="64">
                                </div>
                                <div class="col-md-4">
                                    <label class="form-label">Semester Count</label>
                                    <input type="number" class="form-control" name="semester_count" min="1" placeholder="5">
                                </div>
                                <div class="col-md-4">
                                    <label class="form-label">Major Changes</label>
                                    <input type="number" class="form-control" name="major_changes" min="0" placeholder="1">
                                </div>
                            </div>
                            <button type="submit" class="btn btn-primary mt-3">Get Prediction</button>
                        </form>
                        <div id="prediction-result" class="mt-3"></div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- Scripts -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
    <script>
        // Sample data for visualizations
        const enrollmentData = {
            majors: ['Computer Science', 'Business', 'Engineering', 'Psychology', 'Biology'],
            predicted: [850, 1200, 720, 650, 480],
            current: [780, 1150, 680, 620, 450]
        };

        const departmentData = {
            labels: ['Computer Science', 'Business', 'Engineering', 'Liberal Arts', 'Sciences'],
            values: [28, 32, 22, 12, 6]
        };

        // Create enrollment chart
        const enrollmentChart = {
            data: [
                {
                    x: enrollmentData.majors,
                    y: enrollmentData.current,
                    type: 'bar',
                    name: 'Current',
                    marker: { color: '#17a2b8' }
                },
                {
                    x: enrollmentData.majors,
                    y: enrollmentData.predicted,
                    type: 'bar',
                    name: 'Predicted',
                    marker: { color: '#28a745' }
                }
            ],
            layout: {
                title: 'Current vs Predicted Enrollment',
                xaxis: { title: 'Major' },
                yaxis: { title: 'Number of Students' },
                barmode: 'group'
            }
        };

        // Create department pie chart
        const departmentChart = {
            data: [{
                values: departmentData.values,
                labels: departmentData.labels,
                type: 'pie',
                hole: 0.4
            }],
            layout: {
                title: 'Enrollment by Department (%)'
            }
        };

        // Render charts
        Plotly.newPlot('enrollment-chart', enrollmentChart.data, enrollmentChart.layout);
        Plotly.newPlot('department-pie', departmentChart.data, departmentChart.layout);

        // Section navigation
        function showSection(sectionName) {
            // Hide all sections
            const sections = ['overview', 'enrollment', 'capacity', 'success', 'financial', 'reports'];
            sections.forEach(section => {
                const element = document.getElementById(section + '-section');
                if (element) element.style.display = 'none';
            });

            // Show selected section
            const targetSection = document.getElementById(sectionName + '-section');
            if (targetSection) targetSection.style.display = 'block';

            // Update nav links
            document.querySelectorAll('.nav-link').forEach(link => {
                link.classList.remove('active');
            });
            event.target.classList.add('active');
        }

        // Form submission
        document.getElementById('prediction-form').addEventListener('submit', function(e) {
            e.preventDefault();
            
            const formData = new FormData(e.target);
            const data = Object.fromEntries(formData);
            
            // Simulate prediction (in real app, this would call the API)
            const result = {
                predicted_major: 'Computer Science',
                major_confidence: 0.87,
                predicted_class: 'Data Structures',
                class_confidence: 0.82
            };
            
            document.getElementById('prediction-result').innerHTML = `
                <div class="alert alert-success">
                    <h6>Prediction Results:</h6>
                    <p><strong>Predicted Major:</strong> ${result.predicted_major} (${(result.major_confidence * 100).toFixed(1)}% confidence)</p>
                    <p><strong>Predicted Class:</strong> ${result.predicted_class} (${(result.class_confidence * 100).toFixed(1)}% confidence)</p>
                </div>
            `;
        });
    </script>
</body>
</html>
        """
        
        with open("templates/dashboard.html", "w") as f:
            f.write(dashboard_html)
        
        # Simple help page
        help_html = """
<!DOCTYPE html>
<html>
<head>
    <title>Help - Student Enrollment System</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
    <div class="container mt-5">
        <h1>Help & User Guide</h1>
        
        <div class="accordion" id="helpAccordion">
            <div class="accordion-item">
                <h2 class="accordion-header">
                    <button class="accordion-button" type="button" data-bs-toggle="collapse" data-bs-target="#overview">
                        System Overview
                    </button>
                </h2>
                <div id="overview" class="accordion-collapse collapse show">
                    <div class="accordion-body">
                        This system predicts student enrollment patterns using machine learning to help with:
                        <ul>
                            <li>Academic planning and resource allocation</li>
                            <li>Capacity management</li>
                            <li>Student success initiatives</li>
                            <li>Budget optimization</li>
                        </ul>
                    </div>
                </div>
            </div>
            
            <div class="accordion-item">
                <h2 class="accordion-header">
                    <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#predictions">
                        Making Predictions
                    </button>
                </h2>
                <div id="predictions" class="accordion-collapse collapse">
                    <div class="accordion-body">
                        To predict a student's major and class choices:
                        <ol>
                            <li>Fill in the student information form</li>
                            <li>Enter GPA, age, credits, and other academic data</li>
                            <li>Click "Get Prediction" to see results</li>
                            <li>Review confidence scores for reliability</li>
                        </ol>
                    </div>
                </div>
            </div>
            
            <div class="accordion-item">
                <h2 class="accordion-header">
                    <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#interpretation">
                        Interpreting Results
                    </button>
                </h2>
                <div id="interpretation" class="accordion-collapse collapse">
                    <div class="accordion-body">
                        <strong>Confidence Scores:</strong>
                        <ul>
                            <li>90-100%: Very reliable prediction</li>
                            <li>80-90%: Good reliability</li>
                            <li>70-80%: Moderate reliability</li>
                            <li>Below 70%: Use with caution</li>
                        </ul>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="mt-4">
            <a href="/" class="btn btn-primary">Back to Dashboard</a>
        </div>
    </div>
    
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
        """
        
        with open("templates/help.html", "w") as f:
            f.write(help_html)

# Web app routes
@web_app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})

@web_app.get("/help", response_class=HTMLResponse)
async def help_page(request: Request):
    return templates.TemplateResponse("help.html", {"request": request})

@web_app.post("/predict")
async def web_predict(
    student_id: str = Form(...),
    gpa: float = Form(...),
    age: int = Form(...),
    total_credits: int = Form(...),
    semester_count: int = Form(...),
    major_changes: int = Form(...)
):
    """Handle prediction from web form"""
    try:
        # In a real implementation, this would call the ML models
        # For now, return mock data
        prediction = {
            "student_id": student_id,
            "predicted_major": "Computer Science",
            "major_confidence": 0.87,
            "predicted_class": "Data Structures",
            "class_confidence": 0.82,
            "input_validation": "success"
        }
        
        return prediction
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Prediction error: {str(e)}")

@web_app.get("/api/dashboard-data")
async def get_dashboard_data():
    """API endpoint for dashboard data"""
    return {
        "enrollment_forecast": {
            "majors": ["Computer Science", "Business", "Engineering", "Psychology", "Biology"],
            "predicted": [850, 1200, 720, 650, 480],
            "current": [780, 1150, 680, 620, 450]
        },
        "department_distribution": {
            "Computer Science": 28,
            "Business": 32,
            "Engineering": 22,
            "Liberal Arts": 12,
            "Sciences": 6
        },
        "key_metrics": {
            "total_predicted_enrollment": 4750,
            "prediction_accuracy": 91.5,
            "cost_savings": 1200000,
            "retention_rate": 84.2
        }
    }

if __name__ == "__main__":
    interface = WebInterface()
    print("Web interface templates created!")
    print("Run with: uvicorn web_interface:web_app --host 0.0.0.0 --port 8080 --reload")