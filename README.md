# Student Enrollment Prediction System

A comprehensive machine learning system for predicting student major and class enrollment using historical data, with Power BI integration for visualization and decision-making.

## Overview

This system provides:
- **Data Generation**: Realistic sample student enrollment data
- **Machine Learning Models**: Multiple algorithms for predicting student majors and class choices
- **API Service**: RESTful API for real-time predictions
- **Power BI Integration**: Ready-to-use datasets and visualizations
- **Analytics Dashboard**: Interactive data exploration tools

## Features

### 🎯 Predictive Analytics
- **Major Prediction**: Predict which major a student will choose
- **Class Enrollment**: Forecast class demand and enrollment
- **Trend Analysis**: Identify enrollment patterns over time
- **Success Metrics**: Predict retention and graduation rates

### 🔍 Data Analysis
- **Exploratory Data Analysis**: Comprehensive data visualization
- **Feature Engineering**: Advanced feature creation and selection
- **Model Comparison**: Multiple ML algorithms comparison
- **Performance Metrics**: Detailed model evaluation

### 🚀 API & Integration
- **REST API**: Real-time prediction endpoints
- **Batch Processing**: Handle multiple student predictions
- **Power BI Ready**: Pre-formatted datasets for business intelligence
- **Scalable Architecture**: Designed for production deployment

## Installation

### Prerequisites
- Python 3.8+
- pip package manager

### Setup
1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd student_enrollment_prediction
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the main pipeline**
   ```bash
   python main_pipeline.py
   ```

## Quick Start

### 1. Generate Sample Data and Train Models
```bash
python main_pipeline.py
```
This will:
- Generate realistic student enrollment data
- Perform exploratory data analysis
- Train multiple ML models
- Save the best performing models
- Generate prediction datasets

### 2. Start the API Server
```bash
python api_server.py
```
The API will be available at `http://localhost:8000`

### 3. Generate Power BI Datasets
```bash
python powerbi_integration.py
```
This creates all necessary files for Power BI integration.

## Project Structure

```
student_enrollment_prediction/
├── data_generator.py          # Generate realistic sample data
├── data_preprocessor.py       # Data cleaning and feature engineering
├── eda_analyzer.py           # Exploratory data analysis
├── ml_models.py              # Machine learning model training
├── api_server.py             # FastAPI web service
├── powerbi_integration.py    # Power BI dataset generation
├── main_pipeline.py          # Main execution pipeline
├── requirements.txt          # Python dependencies
├── models/                   # Saved ML models
├── outputs/                  # Analysis outputs and visualizations
└── README.md                # This file
```

## API Endpoints

### Health Check
```
GET /health
```

### Single Student Prediction
```
POST /predict/student
Content-Type: application/json

{
  "student_id": "12345",
  "semester": 5,
  "age": 20.5,
  "gpa": 3.2,
  "grade": 3.4,
  "credits": 4,
  "cumulative_gpa": 3.15,
  "total_credits": 64,
  "semester_count": 5,
  "major_changes": 1,
  "prev_semester_gpa": 3.1,
  "class_avg_grade": 3.0,
  "major_popularity": 150,
  "year": 2024
}
```

### Batch Predictions
```
POST /predict/batch
Content-Type: application/json

{
  "students": [
    { /* student data */ },
    { /* student data */ }
  ]
}
```

### Enrollment Summary
```
GET /enrollment/summary
```

## Power BI Integration

### Generated Datasets
1. **powerbi_enrollment_forecast.csv** - Future enrollment predictions
2. **powerbi_major_trends.csv** - Historical and predicted trends
3. **powerbi_class_capacity.csv** - Capacity planning data
4. **powerbi_student_success.csv** - Success and retention metrics
5. **powerbi_resource_allocation.csv** - Resource planning recommendations

### Integration Steps
1. Open Power BI Desktop
2. Import the generated CSV files using "Get Data" → "Text/CSV"
3. Create relationships between tables if needed
4. Use the recommended visualizations from `powerbi_integration_guide.md`
5. Publish to Power BI Service for sharing

### Recommended Visualizations
- **Enrollment Dashboard**: Cards, bar charts, line charts
- **Capacity Planning**: Scatter plots, tables, gauge charts
- **Success Metrics**: KPIs, funnel charts, heat maps
- **Resource Allocation**: Waterfall charts, tree maps, matrices

## Machine Learning Models

The system trains and compares multiple algorithms:

### Algorithms Used
- **Random Forest**: Ensemble method, good baseline performance
- **Gradient Boosting**: Strong performance on structured data
- **XGBoost**: Advanced gradient boosting with optimization
- **LightGBM**: Fast and efficient gradient boosting
- **Logistic Regression**: Linear baseline model
- **Support Vector Machine**: Non-linear classification

### Model Selection
- Cross-validation for robust evaluation
- Automatic hyperparameter tuning for best model
- Feature importance analysis
- Comprehensive performance metrics

### Features Used
- Student demographics (age, GPA)
- Academic history (cumulative GPA, credits, grades)
- Enrollment patterns (semester count, major changes)
- Course information (class difficulty, popularity)
- Temporal features (year, semester type)

## Data Features

### Student Features
- **Demographics**: Age, GPA, academic standing
- **Academic History**: Cumulative GPA, total credits, semester count
- **Behavioral**: Major changes, previous performance
- **Contextual**: Class difficulty, major popularity, time factors

### Engineered Features
- **Cumulative GPA**: Running average of student performance
- **Major Stability**: Number of major changes
- **Performance Trends**: Previous semester GPA trends
- **Course Difficulty**: Average grade for each class
- **Popularity Metrics**: Enrollment numbers by major/class

## Performance Metrics

### Model Evaluation
- **Accuracy**: Overall prediction correctness
- **Precision & Recall**: Class-specific performance
- **F1-Score**: Balanced performance metric
- **Confusion Matrix**: Detailed classification results
- **Cross-Validation**: Robust performance estimation

### Business Metrics
- **Enrollment Accuracy**: How well predictions match actual enrollment
- **Capacity Planning**: Efficiency of resource allocation
- **Success Prediction**: Retention and graduation forecasting
- **Trend Identification**: Pattern recognition accuracy

## Customization

### Using Your Own Data
1. Replace the sample data generation with your actual data
2. Ensure your data has similar columns or modify the preprocessing
3. Retrain the models with your data
4. Update the API endpoints if needed

### Adding New Features
1. Modify `data_preprocessor.py` to include new features
2. Update the feature engineering pipeline
3. Retrain models with new features
4. Update API request/response models

### Custom Models
1. Add new model classes to `ml_models.py`
2. Include them in the model comparison
3. Update the evaluation metrics if needed

## Deployment

### Local Development
```bash
# Start API server
python api_server.py

# Access API documentation
# Open browser to http://localhost:8000/docs
```

### Production Deployment
1. **Docker**: Create Dockerfile for containerization
2. **Cloud Services**: Deploy to AWS, Azure, or Google Cloud
3. **Load Balancing**: Use multiple API instances for scale
4. **Database**: Replace CSV files with proper database
5. **Monitoring**: Add logging and performance monitoring

## Troubleshooting

### Common Issues
1. **Module Import Errors**: Ensure all dependencies are installed
2. **File Not Found**: Run `main_pipeline.py` first to generate data
3. **Model Loading**: Check if model files exist in `models/` directory
4. **API Errors**: Verify the API server is running and accessible

### Performance Optimization
1. **Data Size**: Use data sampling for large datasets
2. **Model Training**: Use subset of models for faster training
3. **Feature Selection**: Remove less important features
4. **Caching**: Implement prediction caching for repeated requests

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For questions or issues:
1. Check the troubleshooting section
2. Review the API documentation at `/docs`
3. Create an issue in the repository
4. Contact the development team

## Future Enhancements

### Planned Features
- **Real-time Data Integration**: Connect to live student information systems
- **Advanced Analytics**: Student success predictions, early warning systems
- **Mobile App**: Student-facing mobile application
- **Advanced Visualizations**: 3D visualizations, interactive dashboards
- **A/B Testing**: Model performance comparison in production

### Research Opportunities
- **Deep Learning**: Neural network models for complex patterns
- **Natural Language Processing**: Analysis of course descriptions and reviews
- **Time Series Analysis**: Advanced temporal modeling
- **Ensemble Methods**: Combining multiple prediction approaches
- **Causal Inference**: Understanding factors that influence student choices