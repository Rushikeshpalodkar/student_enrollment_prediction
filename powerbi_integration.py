import pandas as pd
import numpy as np
import requests
import json
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

class PowerBIDataGenerator:
    def __init__(self, api_base_url="http://localhost:8000"):
        self.api_base_url = api_base_url
        
    def generate_powerbi_datasets(self):
        """Generate all datasets needed for Power BI visualizations"""
        print("Generating Power BI datasets...")
        
        # Generate different types of prediction data
        self.generate_enrollment_forecast()
        self.generate_major_trends()
        self.generate_class_capacity_planning()
        self.generate_student_success_metrics()
        self.generate_resource_allocation_data()
        
        print("All Power BI datasets generated successfully!")
    
    def generate_enrollment_forecast(self):
        """Generate enrollment forecast data for next 4 semesters"""
        print("Generating enrollment forecast data...")
        
        # Base enrollment numbers (you would get these from your API)
        majors = ['Computer Science', 'Business Administration', 'Psychology', 'Biology',
                 'Engineering', 'Mathematics', 'English', 'History', 'Economics', 'Art']
        
        forecast_data = []
        current_date = datetime.now()
        
        # Generate forecast for next 4 semesters
        for semester_ahead in range(1, 5):
            forecast_date = current_date + timedelta(days=semester_ahead * 120)  # ~4 months per semester
            semester_type = "Fall" if forecast_date.month >= 8 else "Spring" if forecast_date.month >= 1 else "Summer"
            
            for major in majors:
                # Simulate different growth/decline trends for different majors
                if major in ['Computer Science', 'Engineering']:
                    base_enrollment = np.random.normal(200, 30)
                    growth_rate = 1.05  # 5% growth
                elif major in ['Business Administration', 'Psychology']:
                    base_enrollment = np.random.normal(180, 25)
                    growth_rate = 1.02  # 2% growth
                else:
                    base_enrollment = np.random.normal(120, 20)
                    growth_rate = 0.98  # 2% decline
                
                predicted_enrollment = int(base_enrollment * (growth_rate ** semester_ahead))
                predicted_enrollment = max(50, predicted_enrollment)  # Minimum 50 students
                
                forecast_data.append({
                    'semester': f"{forecast_date.year} {semester_type}",
                    'year': forecast_date.year,
                    'semester_type': semester_type,
                    'major': major,
                    'predicted_enrollment': predicted_enrollment,
                    'confidence_level': round(np.random.uniform(0.75, 0.95), 2),
                    'forecast_date': forecast_date.strftime('%Y-%m-%d'),
                    'semesters_ahead': semester_ahead
                })
        
        forecast_df = pd.DataFrame(forecast_data)
        forecast_df.to_csv('powerbi_enrollment_forecast.csv', index=False)
        print(f"Saved enrollment forecast: {len(forecast_df)} records")
    
    def generate_major_trends(self):
        """Generate historical and predicted major popularity trends"""
        print("Generating major trends data...")
        
        majors = ['Computer Science', 'Business Administration', 'Psychology', 'Biology',
                 'Engineering', 'Mathematics', 'English', 'History', 'Economics', 'Art']
        
        trends_data = []
        
        # Historical data (2020-2024)
        for year in range(2020, 2025):
            for semester_type in ['Fall', 'Spring']:
                for major in majors:
                    # Simulate trends - CS and Engineering growing, others stable or declining
                    if major == 'Computer Science':
                        base = 150
                        trend = (year - 2020) * 15  # Strong growth
                    elif major == 'Engineering':
                        base = 130
                        trend = (year - 2020) * 8   # Moderate growth
                    elif major in ['Business Administration', 'Psychology']:
                        base = 140
                        trend = (year - 2020) * 2   # Slight growth
                    else:
                        base = 100
                        trend = -(year - 2020) * 3  # Slight decline
                    
                    enrollment = base + trend + np.random.normal(0, 10)
                    enrollment = max(30, int(enrollment))
                    
                    trends_data.append({
                        'year': year,
                        'semester': f"{year} {semester_type}",
                        'semester_type': semester_type,
                        'major': major,
                        'enrollment': enrollment,
                        'is_predicted': False,
                        'growth_rate': round(trend / base * 100, 1) if base > 0 else 0
                    })
        
        # Future predictions (2025-2026)
        for year in range(2025, 2027):
            for semester_type in ['Fall', 'Spring']:
                for major in majors:
                    # Continue trends with some uncertainty
                    if major == 'Computer Science':
                        base = 150 + (year - 2020) * 15
                        uncertainty = 0.15
                    elif major == 'Engineering':
                        base = 130 + (year - 2020) * 8
                        uncertainty = 0.12
                    else:
                        base = max(50, 100 - (year - 2020) * 3)
                        uncertainty = 0.10
                    
                    enrollment = int(base * (1 + np.random.normal(0, uncertainty)))
                    enrollment = max(30, enrollment)
                    
                    trends_data.append({
                        'year': year,
                        'semester': f"{year} {semester_type}",
                        'semester_type': semester_type,
                        'major': major,
                        'enrollment': enrollment,
                        'is_predicted': True,
                        'growth_rate': round(np.random.normal(5, 10), 1)
                    })
        
        trends_df = pd.DataFrame(trends_data)
        trends_df.to_csv('powerbi_major_trends.csv', index=False)
        print(f"Saved major trends: {len(trends_df)} records")
    
    def generate_class_capacity_planning(self):
        """Generate class capacity and demand predictions"""
        print("Generating class capacity planning data...")
        
        classes = [
            'Intro to Programming', 'Data Structures', 'Algorithms', 'Database Systems',
            'Accounting', 'Marketing', 'Finance', 'Statistics', 'Calculus I',
            'Organic Chemistry', 'Physics', 'Psychology', 'Literature', 'History'
        ]
        
        capacity_data = []
        
        for class_name in classes:
            # Current capacity
            current_capacity = np.random.randint(25, 50)
            
            # Predicted demand for next semester
            if class_name in ['Intro to Programming', 'Data Structures', 'Statistics']:
                demand_multiplier = np.random.uniform(1.2, 1.8)  # High demand
            elif class_name in ['Accounting', 'Marketing', 'Psychology']:
                demand_multiplier = np.random.uniform(1.0, 1.3)  # Moderate demand
            else:
                demand_multiplier = np.random.uniform(0.7, 1.1)  # Lower demand
            
            predicted_demand = int(current_capacity * demand_multiplier)
            
            # Calculate metrics
            utilization_rate = min(100, (predicted_demand / current_capacity) * 100)
            capacity_shortage = max(0, predicted_demand - current_capacity)
            recommended_sections = max(1, np.ceil(predicted_demand / 25))  # 25 students per section
            
            capacity_data.append({
                'class_name': class_name,
                'current_capacity': current_capacity,
                'predicted_demand': predicted_demand,
                'utilization_rate': round(utilization_rate, 1),
                'capacity_shortage': capacity_shortage,
                'recommended_sections': int(recommended_sections),
                'priority_level': 'High' if capacity_shortage > 10 else 'Medium' if capacity_shortage > 0 else 'Low',
                'estimated_cost': int(recommended_sections * 5000),  # $5000 per section
                'department': self.get_department(class_name)
            })
        
        capacity_df = pd.DataFrame(capacity_data)
        capacity_df.to_csv('powerbi_class_capacity.csv', index=False)
        print(f"Saved class capacity data: {len(capacity_df)} records")
    
    def generate_student_success_metrics(self):
        """Generate student success and retention predictions"""
        print("Generating student success metrics...")
        
        majors = ['Computer Science', 'Business Administration', 'Psychology', 'Biology',
                 'Engineering', 'Mathematics', 'English', 'History', 'Economics', 'Art']
        
        success_data = []
        
        for major in majors:
            # Simulate different success rates by major
            if major in ['Mathematics', 'Engineering', 'Computer Science']:
                base_retention = 0.75  # Lower retention due to difficulty
                base_gpa = 2.9
            elif major in ['Business Administration', 'Psychology']:
                base_retention = 0.85  # Higher retention
                base_gpa = 3.2
            else:
                base_retention = 0.80  # Average retention
                base_gpa = 3.1
            
            # Add some variation
            retention_rate = base_retention + np.random.normal(0, 0.05)
            retention_rate = max(0.6, min(0.95, retention_rate))
            
            avg_gpa = base_gpa + np.random.normal(0, 0.15)
            avg_gpa = max(2.0, min(4.0, avg_gpa))
            
            # Calculate other metrics
            graduation_rate = retention_rate * 0.85  # 85% of retained students graduate
            employment_rate = 0.75 + (avg_gpa - 2.0) * 0.1  # GPA correlates with employment
            
            success_data.append({
                'major': major,
                'retention_rate': round(retention_rate * 100, 1),
                'graduation_rate': round(graduation_rate * 100, 1),
                'average_gpa': round(avg_gpa, 2),
                'employment_rate': round(employment_rate * 100, 1),
                'predicted_dropouts': int(100 * (1 - retention_rate)),
                'at_risk_students': int(150 * 0.15),  # 15% at risk
                'support_needed': 'High' if retention_rate < 0.75 else 'Medium' if retention_rate < 0.85 else 'Low'
            })
        
        success_df = pd.DataFrame(success_data)
        success_df.to_csv('powerbi_student_success.csv', index=False)
        print(f"Saved student success metrics: {len(success_df)} records")
    
    def generate_resource_allocation_data(self):
        """Generate resource allocation recommendations"""
        print("Generating resource allocation data...")
        
        departments = ['Computer Science', 'Business', 'Liberal Arts', 'Sciences', 'Engineering']
        
        resource_data = []
        
        for dept in departments:
            # Budget allocation based on enrollment predictions
            if dept in ['Computer Science', 'Engineering']:
                base_budget = 500000
                growth_factor = 1.15
            elif dept == 'Business':
                base_budget = 400000
                growth_factor = 1.05
            else:
                base_budget = 300000
                growth_factor = 0.98
            
            recommended_budget = int(base_budget * growth_factor)
            faculty_needed = np.random.randint(8, 15)
            classroom_hours = np.random.randint(200, 400)
            
            resource_data.append({
                'department': dept,
                'current_budget': base_budget,
                'recommended_budget': recommended_budget,
                'budget_change': recommended_budget - base_budget,
                'budget_change_percent': round(((recommended_budget - base_budget) / base_budget) * 100, 1),
                'faculty_needed': faculty_needed,
                'classroom_hours_needed': classroom_hours,
                'equipment_cost': np.random.randint(50000, 150000),
                'priority_score': np.random.randint(1, 10)
            })
        
        resource_df = pd.DataFrame(resource_data)
        resource_df.to_csv('powerbi_resource_allocation.csv', index=False)
        print(f"Saved resource allocation data: {len(resource_df)} records")
    
    def get_department(self, class_name):
        """Map class names to departments"""
        mapping = {
            'Intro to Programming': 'Computer Science',
            'Data Structures': 'Computer Science',
            'Algorithms': 'Computer Science',
            'Database Systems': 'Computer Science',
            'Accounting': 'Business',
            'Marketing': 'Business',
            'Finance': 'Business',
            'Statistics': 'Mathematics',
            'Calculus I': 'Mathematics',
            'Organic Chemistry': 'Sciences',
            'Physics': 'Sciences',
            'Psychology': 'Liberal Arts',
            'Literature': 'Liberal Arts',
            'History': 'Liberal Arts'
        }
        return mapping.get(class_name, 'General')
    
    def create_powerbi_dashboard_template(self):
        """Create a sample Power BI dashboard template with visualizations"""
        print("Creating Power BI dashboard template...")
        
        # Load generated data
        try:
            enrollment_forecast = pd.read_csv('powerbi_enrollment_forecast.csv')
            major_trends = pd.read_csv('powerbi_major_trends.csv')
            class_capacity = pd.read_csv('powerbi_class_capacity.csv')
            student_success = pd.read_csv('powerbi_student_success.csv')
            resource_allocation = pd.read_csv('powerbi_resource_allocation.csv')
        except FileNotFoundError:
            print("Generate datasets first before creating dashboard template")
            return
        
        # Create sample visualizations
        fig = make_subplots(
            rows=3, cols=2,
            subplot_titles=[
                'Enrollment Forecast by Major',
                'Class Capacity vs Demand',
                'Student Success Metrics',
                'Resource Allocation by Department',
                'Major Trends Over Time',
                'Department Budget Requirements'
            ],
            specs=[[{"type": "bar"}, {"type": "scatter"}],
                   [{"type": "bar"}, {"type": "pie"}],
                   [{"type": "scatter"}, {"type": "bar"}]]
        )
        
        # 1. Enrollment Forecast
        forecast_summary = enrollment_forecast.groupby('major')['predicted_enrollment'].sum()
        fig.add_trace(
            go.Bar(x=forecast_summary.index, y=forecast_summary.values, name="Enrollment Forecast"),
            row=1, col=1
        )
        
        # 2. Class Capacity vs Demand
        fig.add_trace(
            go.Scatter(
                x=class_capacity['current_capacity'],
                y=class_capacity['predicted_demand'],
                mode='markers',
                text=class_capacity['class_name'],
                name="Capacity vs Demand"
            ),
            row=1, col=2
        )
        
        # 3. Student Success Metrics
        fig.add_trace(
            go.Bar(x=student_success['major'], y=student_success['retention_rate'], name="Retention Rate"),
            row=2, col=1
        )
        
        # 4. Resource Allocation
        fig.add_trace(
            go.Pie(labels=resource_allocation['department'], values=resource_allocation['recommended_budget'], name="Budget Allocation"),
            row=2, col=2
        )
        
        # 5. Major Trends
        trends_summary = major_trends[major_trends['major'] == 'Computer Science']
        fig.add_trace(
            go.Scatter(x=trends_summary['year'], y=trends_summary['enrollment'], mode='lines+markers', name="CS Trend"),
            row=3, col=1
        )
        
        # 6. Department Budget Requirements
        fig.add_trace(
            go.Bar(x=resource_allocation['department'], y=resource_allocation['budget_change'], name="Budget Change"),
            row=3, col=2
        )
        
        fig.update_layout(height=1200, showlegend=True, title_text="Student Enrollment Prediction Dashboard")
        fig.write_html('powerbi_dashboard_template.html')
        print("Dashboard template saved as powerbi_dashboard_template.html")
    
    def generate_powerbi_connection_guide(self):
        """Generate a guide for connecting to Power BI"""
        guide = """
# Power BI Integration Guide

## Data Sources
The following CSV files have been generated for Power BI import:

1. **powerbi_enrollment_forecast.csv** - Enrollment predictions for next 4 semesters
2. **powerbi_major_trends.csv** - Historical and predicted major popularity trends
3. **powerbi_class_capacity.csv** - Class capacity planning and demand predictions
4. **powerbi_student_success.csv** - Student success and retention metrics
5. **powerbi_resource_allocation.csv** - Resource allocation recommendations

## API Endpoints
For real-time data, connect to these API endpoints:

- Base URL: http://localhost:8000
- Health Check: GET /health
- Single Prediction: POST /predict/student
- Batch Predictions: POST /predict/batch
- Enrollment Summary: GET /enrollment/summary

## Recommended Power BI Visualizations

### Page 1: Enrollment Dashboard
- **Card Visuals**: Total predicted enrollment, number of majors, confidence score
- **Bar Chart**: Enrollment by major (horizontal)
- **Line Chart**: Enrollment trends over time
- **Map Visual**: Enrollment by department/building

### Page 2: Capacity Planning
- **Scatter Plot**: Current capacity vs predicted demand
- **Table**: Class capacity details with priority levels
- **Gauge Chart**: Utilization rates
- **Clustered Bar Chart**: Recommended vs current sections

### Page 3: Success Metrics
- **KPI Visuals**: Retention rate, graduation rate, employment rate
- **Funnel Chart**: Student progression through major
- **Heat Map**: GPA by major and semester
- **Donut Chart**: At-risk student distribution

### Page 4: Resource Allocation
- **Waterfall Chart**: Budget changes by department
- **Tree Map**: Faculty allocation
- **Stacked Bar**: Equipment and operational costs
- **Matrix**: Resource priorities

## Data Refresh Strategy
1. **Static Data**: Import CSV files for historical analysis
2. **Real-time Data**: Connect to API endpoints for live predictions
3. **Scheduled Refresh**: Set up daily refresh for batch predictions
4. **Manual Refresh**: Use for ad-hoc analysis

## Power BI Desktop Steps
1. Open Power BI Desktop
2. Get Data → Text/CSV
3. Import all generated CSV files
4. Create relationships between tables
5. Build visualizations as recommended above
6. Publish to Power BI Service

## DAX Measures Examples
```dax
Total Predicted Enrollment = SUM(EnrollmentForecast[predicted_enrollment])
Average Confidence = AVERAGE(EnrollmentForecast[confidence_level])
Capacity Utilization = DIVIDE(SUM(ClassCapacity[predicted_demand]), SUM(ClassCapacity[current_capacity]))
At Risk Percentage = DIVIDE(SUM(StudentSuccess[at_risk_students]), SUM(StudentSuccess[predicted_dropouts]) + SUM(StudentSuccess[at_risk_students]))
```
"""
        
        with open('powerbi_integration_guide.md', 'w') as f:
            f.write(guide)
        
        print("Power BI integration guide saved as powerbi_integration_guide.md")

if __name__ == "__main__":
    # Generate all Power BI datasets and templates
    generator = PowerBIDataGenerator()
    
    # Generate all datasets
    generator.generate_powerbi_datasets()
    
    # Create dashboard template
    generator.create_powerbi_dashboard_template()
    
    # Generate integration guide
    generator.generate_powerbi_connection_guide()
    
    print("\n=== POWER BI INTEGRATION COMPLETE ===")
    print("Files generated:")
    print("- powerbi_enrollment_forecast.csv")
    print("- powerbi_major_trends.csv") 
    print("- powerbi_class_capacity.csv")
    print("- powerbi_student_success.csv")
    print("- powerbi_resource_allocation.csv")
    print("- powerbi_dashboard_template.html")
    print("- powerbi_integration_guide.md")