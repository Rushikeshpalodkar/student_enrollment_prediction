from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, validator
import pandas as pd
import numpy as np
import joblib
from typing import List, Dict, Any, Optional
import uvicorn
import logging
import traceback
from datetime import datetime
import os

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('api.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Student Enrollment Prediction API",
    description="Advanced API for predicting student major and class enrollment with comprehensive error handling",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variables to store loaded models
major_model = None
class_model = None
preprocessor = None
major_classes = None
class_classes = None

# Enhanced Pydantic models with validation
class StudentFeatures(BaseModel):
    semester: int
    age: float
    gpa: float
    grade: float
    credits: int
    cumulative_gpa: float
    total_credits: int
    semester_count: int
    major_changes: int
    prev_semester_gpa: float
    class_avg_grade: float
    major_popularity: int
    year: int
    semester_type: str
    class_name: str
    
    @validator('age')
    def validate_age(cls, v):
        if not 16 <= v <= 60:
            raise ValueError('Age must be between 16 and 60')
        return v
    
    @validator('gpa', 'cumulative_gpa', 'prev_semester_gpa', 'grade', 'class_avg_grade')
    def validate_gpa(cls, v):
        if not 0.0 <= v <= 4.0:
            raise ValueError('GPA values must be between 0.0 and 4.0')
        return v
    
    @validator('semester', 'credits', 'total_credits', 'semester_count', 'major_changes', 'major_popularity')
    def validate_positive_integers(cls, v):
        if v < 0:
            raise ValueError('Value must be non-negative')
        return v

class PredictionResponse(BaseModel):
    student_id: str
    predicted_major: str
    major_confidence: float
    predicted_class: str
    class_confidence: float
    model_version: str
    prediction_timestamp: str
    data_quality_score: Optional[float] = None
    warnings: Optional[List[str]] = None

class BatchPredictionRequest(BaseModel):
    students: List[Dict[str, Any]]

class EnrollmentSummaryResponse(BaseModel):
    major_predictions: Dict[str, int]
    class_predictions: Dict[str, int]
    total_students: int

@app.on_event("startup")
async def load_models():
    """Load trained models on startup with comprehensive error handling"""
    global major_model, class_model, preprocessor, major_classes, class_classes
    
    try:
        logger.info("Starting model loading process...")
        
        # Check if model files exist
        model_files = ['models/best_major_model.pkl', 'models/best_class_model.pkl']
        for file_path in model_files:
            if not os.path.exists(file_path):
                logger.warning(f"Model file not found: {file_path}")
                logger.info("Please run main_pipeline.py first to train models")
                return
        
        # Load major prediction model
        logger.info("Loading major prediction model...")
        major_model_data = joblib.load('models/best_major_model.pkl')
        major_model = major_model_data['model']
        
        # Load class prediction model
        logger.info("Loading class prediction model...")
        class_model_data = joblib.load('models/best_class_model.pkl')
        class_model = class_model_data['model']
        
        # Load preprocessor
        logger.info("Initializing data preprocessor...")
        from data_preprocessor import StudentDataPreprocessor
        preprocessor = StudentDataPreprocessor()
        
        # Load sample data to fit the preprocessor
        if os.path.exists('student_enrollment_data.csv'):
            logger.info("Loading training data for preprocessor...")
            df = pd.read_csv('student_enrollment_data.csv')
            df_clean = preprocessor.clean_data(df)
            df_engineered = preprocessor.engineer_features(df_clean)
            
            # Fit preprocessor
            X_major, y_major = preprocessor.prepare_features(df_engineered, target_column='major')
            X_class, y_class = preprocessor.prepare_features(df_engineered, target_column='class_name')
            
            # Get class names
            major_classes = preprocessor.get_class_names('major')
            class_classes = preprocessor.get_class_names('class_name')
            
            logger.info("Models loaded successfully!")
        else:
            logger.warning("Training data not found. Run main_pipeline.py to generate data and train models.")
        
    except FileNotFoundError as e:
        logger.error(f"Model file not found: {e}")
        logger.info("Please run main_pipeline.py first to train models")
    except Exception as e:
        logger.error(f"Error loading models: {e}")
        logger.error(traceback.format_exc())
        raise e

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Student Enrollment Prediction API",
        "version": "1.0.0",
        "status": "running"
    }

def assess_data_quality(student_data: Dict[str, Any]) -> tuple[float, List[str]]:
    """Assess the quality of input data and return score and warnings"""
    warnings = []
    quality_score = 1.0
    
    # Check for missing or default values
    if student_data.get('gpa', 0) == 0:
        warnings.append("GPA is 0 - may affect prediction accuracy")
        quality_score -= 0.1
    
    if student_data.get('age', 0) < 18 or student_data.get('age', 0) > 25:
        warnings.append("Student age is outside typical range")
        quality_score -= 0.05
    
    if student_data.get('major_changes', 0) > 2:
        warnings.append("High number of major changes may indicate uncertainty")
        quality_score -= 0.05
    
    if student_data.get('total_credits', 0) > 150:
        warnings.append("High credit count - student may be near graduation")
        quality_score -= 0.05
    
    return max(0.0, quality_score), warnings

@app.get("/health")
async def health_check():
    """Enhanced health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "models_loaded": {
            "major_model": major_model is not None,
            "class_model": class_model is not None,
            "preprocessor": preprocessor is not None
        },
        "api_version": "2.0.0",
        "endpoints_available": ["/predict/student", "/predict/batch", "/enrollment/summary", "/models/info"]
    }

@app.post("/predict/student", response_model=PredictionResponse)
async def predict_student_enrollment(student_data: Dict[str, Any]):
    """Enhanced prediction endpoint with validation and error handling"""
    # Check if models are loaded
    if major_model is None or class_model is None:
        logger.error("Prediction attempted but models not loaded")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, 
            detail="Models not loaded. Please contact administrator."
        )
    
    try:
        logger.info(f"Processing prediction for student: {student_data.get('student_id', 'unknown')}")
        
        # Assess data quality
        quality_score, warnings = assess_data_quality(student_data)
        
        # Log low quality data
        if quality_score < 0.8:
            logger.warning(f"Low quality data detected for student {student_data.get('student_id')}: {warnings}")
        
        # Extract features with defaults and validation
        try:
            feature_vector = [
                student_data.get('semester', 1),
                max(16, min(60, student_data.get('age', 20))),  # Clamp age
                max(0.0, min(4.0, student_data.get('gpa', 3.0))),  # Clamp GPA
                max(0.0, min(4.0, student_data.get('grade', 3.0))),
                max(1, student_data.get('credits', 4)),
                max(0.0, min(4.0, student_data.get('cumulative_gpa', 3.0))),
                max(0, student_data.get('total_credits', 12)),
                max(1, student_data.get('semester_count', 1)),
                max(0, student_data.get('major_changes', 0)),
                max(0.0, min(4.0, student_data.get('prev_semester_gpa', 3.0))),
                max(0.0, min(4.0, student_data.get('class_avg_grade', 3.0))),
                max(1, student_data.get('major_popularity', 100)),
                student_data.get('year', 2024),
                0,  # semester_type encoded
                1   # class_name encoded (placeholder)
            ]
        except (ValueError, TypeError) as e:
            logger.error(f"Feature extraction error: {e}")
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Invalid input data format: {str(e)}"
            )
        
        # Make predictions with error handling
        try:
            # Predict major
            major_pred = major_model.predict([feature_vector])[0]
            major_proba = major_model.predict_proba([feature_vector])[0]
            predicted_major = major_classes[major_pred] if major_classes is not None else "Unknown"
            major_confidence = float(max(major_proba))
            
            # Predict class
            class_pred = class_model.predict([feature_vector])[0]
            class_proba = class_model.predict_proba([feature_vector])[0]
            predicted_class = class_classes[class_pred] if class_classes is not None else "Unknown"
            class_confidence = float(max(class_proba))
            
        except Exception as pred_error:
            logger.error(f"Model prediction error: {pred_error}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Model prediction failed. Please try again or contact support."
            )
        
        # Create response
        response = PredictionResponse(
            student_id=student_data.get('student_id', 'unknown'),
            predicted_major=predicted_major,
            major_confidence=round(major_confidence, 3),
            predicted_class=predicted_class,
            class_confidence=round(class_confidence, 3),
            model_version="2.0.0",
            prediction_timestamp=datetime.now().isoformat(),
            data_quality_score=round(quality_score, 3),
            warnings=warnings if warnings else None
        )
        
        logger.info(f"Prediction completed for student {response.student_id}")
        return response
        
    except HTTPException:
        raise  # Re-raise HTTP exceptions
    except Exception as e:
        logger.error(f"Unexpected error in prediction: {e}")
        logger.error(traceback.format_exc())
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred. Please contact support."
        )

@app.post("/predict/batch")
async def predict_batch_enrollment(request: BatchPredictionRequest):
    """Predict enrollments for multiple students"""
    if major_model is None or class_model is None:
        raise HTTPException(status_code=500, detail="Models not loaded")
    
    try:
        predictions = []
        
        for student_data in request.students:
            # Create feature vector
            feature_vector = [
                student_data.get('semester', 1),
                student_data.get('age', 20),
                student_data.get('gpa', 3.0),
                student_data.get('grade', 3.0),
                student_data.get('credits', 4),
                student_data.get('cumulative_gpa', 3.0),
                student_data.get('total_credits', 12),
                student_data.get('semester_count', 1),
                student_data.get('major_changes', 0),
                student_data.get('prev_semester_gpa', 3.0),
                student_data.get('class_avg_grade', 3.0),
                student_data.get('major_popularity', 100),
                student_data.get('year', 2024),
                0,  # semester_type encoded
                1   # class_name encoded
            ]
            
            # Predict major
            major_pred = major_model.predict([feature_vector])[0]
            major_proba = major_model.predict_proba([feature_vector])[0]
            predicted_major = major_classes[major_pred]
            major_confidence = float(max(major_proba))
            
            # Predict class
            class_pred = class_model.predict([feature_vector])[0]
            class_proba = class_model.predict_proba([feature_vector])[0]
            predicted_class = class_classes[class_pred]
            class_confidence = float(max(class_proba))
            
            predictions.append({
                'student_id': student_data.get('student_id', 'unknown'),
                'predicted_major': predicted_major,
                'major_confidence': round(major_confidence, 3),
                'predicted_class': predicted_class,
                'class_confidence': round(class_confidence, 3)
            })
        
        return {"predictions": predictions}
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Batch prediction error: {str(e)}")

@app.get("/enrollment/summary", response_model=EnrollmentSummaryResponse)
async def get_enrollment_summary():
    """Get enrollment summary from pre-generated predictions"""
    try:
        # Load pre-generated predictions
        major_summary = pd.read_csv('major_enrollment_predictions.csv')
        class_summary = pd.read_csv('class_enrollment_predictions.csv')
        
        major_predictions = dict(zip(major_summary['major'], major_summary['predicted_enrollment']))
        class_predictions = dict(zip(class_summary['class_name'], class_summary['predicted_enrollment']))
        
        total_students = major_summary['predicted_enrollment'].sum()
        
        return EnrollmentSummaryResponse(
            major_predictions=major_predictions,
            class_predictions=class_predictions,
            total_students=int(total_students)
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading enrollment summary: {str(e)}")

@app.get("/models/info")
async def get_model_info():
    """Get information about loaded models"""
    if major_model is None or class_model is None:
        raise HTTPException(status_code=500, detail="Models not loaded")
    
    return {
        "major_model": {
            "type": type(major_model).__name__,
            "classes": major_classes.tolist() if major_classes is not None else []
        },
        "class_model": {
            "type": type(class_model).__name__,
            "classes": class_classes.tolist() if class_classes is not None else []
        },
        "features": preprocessor.feature_columns if preprocessor else []
    }

@app.get("/sample/student")
async def get_sample_student_data():
    """Get sample student data for testing API"""
    return {
        "student_id": "sample_001",
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
        "year": 2024,
        "semester_type": "Fall",
        "class_name": "Data Structures"
    }

if __name__ == "__main__":
    uvicorn.run(
        "api_server:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )