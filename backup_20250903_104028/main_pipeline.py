import pandas as pd
import numpy as np
from data_generator import generate_sample_data
from data_preprocessor import StudentDataPreprocessor
from eda_analyzer import EDAAnalyzer
from ml_models import StudentEnrollmentModels
import os

def main():
    """Main pipeline for student enrollment prediction"""
    print("=== STUDENT ENROLLMENT PREDICTION PIPELINE ===\n")
    
    # Step 1: Generate sample data if it doesn't exist
    data_file = 'student_enrollment_data.csv'
    if not os.path.exists(data_file):
        print("Generating sample student enrollment data...")
        df = generate_sample_data(n_students=5000, n_semesters=8)
        df.to_csv(data_file, index=False)
        print(f"Sample data saved to {data_file}\n")
    else:
        print(f"Loading existing data from {data_file}...")
        df = pd.read_csv(data_file)
        print(f"Loaded {len(df)} records\n")
    
    # Step 2: Exploratory Data Analysis
    print("=== STEP 2: EXPLORATORY DATA ANALYSIS ===")
    analyzer = EDAAnalyzer()
    
    # Basic statistics
    stats = analyzer.basic_statistics(df)
    
    # Generate visualizations
    print("\nGenerating EDA visualizations...")
    analyzer.plot_major_distribution(df, 'outputs/major_distribution.png')
    analyzer.plot_gpa_grade_relationship(df, 'outputs/gpa_grade_relationship.png')
    analyzer.plot_class_popularity(df, save_path='outputs/class_popularity.png')
    analyzer.plot_grade_distribution_by_major(df, 'outputs/grade_by_major.png')
    analyzer.plot_correlation_matrix(df, 'outputs/correlation_matrix.png')
    
    # Analyze major switching patterns
    switch_stats, switch_patterns = analyzer.analyze_major_switching(df)
    
    # Generate interactive dashboard
    analyzer.generate_interactive_dashboard(df, 'outputs/eda_dashboard.html')
    print("EDA completed. Check the outputs/ folder for visualizations.\n")
    
    # Step 3: Data Preprocessing
    print("=== STEP 3: DATA PREPROCESSING ===")
    preprocessor = StudentDataPreprocessor()
    
    # Clean and engineer features
    df_clean = preprocessor.clean_data(df)
    df_engineered = preprocessor.engineer_features(df_clean)
    
    print(f"Data shape after preprocessing: {df_engineered.shape}")
    
    # Prepare features for both major and class prediction
    print("\nPreparing features for major prediction...")
    X_major, y_major = preprocessor.prepare_features(df_engineered, target_column='major')
    X_train_major, X_test_major, y_train_major, y_test_major = preprocessor.split_data(X_major, y_major)
    major_classes = preprocessor.get_class_names('major')
    
    print("\nPreparing features for class prediction...")
    X_class, y_class = preprocessor.prepare_features(df_engineered, target_column='class_name')
    X_train_class, X_test_class, y_train_class, y_test_class = preprocessor.split_data(X_class, y_class)
    class_classes = preprocessor.get_class_names('class_name')
    
    print(f"Major prediction - Training: {X_train_major.shape}, Test: {X_test_major.shape}")
    print(f"Class prediction - Training: {X_train_class.shape}, Test: {X_test_class.shape}\n")
    
    # Step 4: Train Machine Learning Models
    print("=== STEP 4: MACHINE LEARNING MODEL TRAINING ===")
    
    # Train models for major prediction
    print("Training models for MAJOR prediction...")
    major_models = StudentEnrollmentModels()
    major_scores = major_models.train_all_models(
        X_train_major, y_train_major, X_test_major, y_test_major
    )
    
    # Compare models
    major_comparison = major_models.compare_models()
    
    # Evaluate best model
    major_evaluation = major_models.evaluate_model(
        major_models.best_model_name, X_test_major, y_test_major, major_classes
    )
    
    # Get feature importance
    major_feature_importance = major_models.get_feature_importance(
        major_models.best_model_name, preprocessor.feature_columns
    )
    
    # Save the best major prediction model
    major_models.save_best_model('models/best_major_model.pkl')
    
    print("\n" + "="*50)
    
    # Train models for class prediction
    print("Training models for CLASS prediction...")
    class_models = StudentEnrollmentModels()
    class_scores = class_models.train_all_models(
        X_train_class, y_train_class, X_test_class, y_test_class
    )
    
    # Compare models
    class_comparison = class_models.compare_models()
    
    # Evaluate best model
    class_evaluation = class_models.evaluate_model(
        class_models.best_model_name, X_test_class, y_test_class, class_classes
    )
    
    # Get feature importance
    class_feature_importance = class_models.get_feature_importance(
        class_models.best_model_name, preprocessor.feature_columns
    )
    
    # Save the best class prediction model
    class_models.save_best_model('models/best_class_model.pkl')
    
    # Step 5: Generate Predictions for Power BI
    print("\n=== STEP 5: GENERATING PREDICTIONS FOR POWER BI ===")
    
    # Generate sample predictions for next semester
    future_predictions = generate_future_predictions(
        major_models, class_models, preprocessor, df_engineered, major_classes, class_classes
    )
    
    print("Pipeline completed successfully!")
    print("\nFiles generated:")
    print("- models/best_major_model.pkl (trained major prediction model)")
    print("- models/best_class_model.pkl (trained class prediction model)")
    print("- outputs/eda_dashboard.html (interactive EDA dashboard)")
    print("- future_predictions.csv (predictions for Power BI)")
    print("- Various visualization files in outputs/ folder")
    
    return {
        'major_models': major_models,
        'class_models': class_models,
        'preprocessor': preprocessor,
        'future_predictions': future_predictions
    }

def generate_future_predictions(major_models, class_models, preprocessor, df_engineered, major_classes, class_classes):
    """Generate predictions for future enrollment planning"""
    print("Generating future enrollment predictions...")
    
    # Get unique students from the dataset
    students = df_engineered.groupby('student_id').last().reset_index()
    
    # Create features for next semester prediction
    next_semester = df_engineered['semester'].max() + 1
    
    predictions_data = []
    
    for _, student in students.head(1000).iterrows():  # Predict for first 1000 students
        # Create feature vector for next semester
        feature_vector = [
            next_semester,  # semester
            student['age'],  # age
            student['gpa'],  # gpa
            student['cumulative_gpa'],  # Use last known grade as proxy
            4,  # credits (assume 4-credit course)
            student['cumulative_gpa'],  # cumulative_gpa
            student['total_credits'] + 4,  # total_credits + new course
            student['semester_count'] + 1,  # semester_count
            student['major_changes'],  # major_changes
            student['cumulative_gpa'],  # prev_semester_gpa
            3.0,  # class_avg_grade (use average)
            100,  # major_popularity (use average)
            2024,  # year
            0,  # semester_type (encoded, 0 for Fall)
            1   # class_name (will be predicted)
        ]
        
        # Predict major
        major_pred = major_models.predict_student_major(feature_vector)
        predicted_major_idx = major_pred['prediction']
        predicted_major = major_classes[predicted_major_idx]
        major_confidence = max(major_pred['probabilities']) if major_pred['probabilities'] is not None else 0.5
        
        # Predict class
        class_pred = class_models.predict_student_major(feature_vector)
        predicted_class_idx = class_pred['prediction']
        predicted_class = class_classes[predicted_class_idx]
        class_confidence = max(class_pred['probabilities']) if class_pred['probabilities'] is not None else 0.5
        
        predictions_data.append({
            'student_id': student['student_id'],
            'predicted_semester': next_semester,
            'predicted_major': predicted_major,
            'major_confidence': round(major_confidence, 3),
            'predicted_class': predicted_class,
            'class_confidence': round(class_confidence, 3),
            'current_gpa': round(student['gpa'], 2),
            'current_total_credits': student['total_credits'],
            'current_semester_count': student['semester_count']
        })
    
    # Create predictions dataframe
    predictions_df = pd.DataFrame(predictions_data)
    
    # Save predictions
    predictions_df.to_csv('future_predictions.csv', index=False)
    
    # Generate summary statistics for Power BI
    major_summary = predictions_df['predicted_major'].value_counts().reset_index()
    major_summary.columns = ['major', 'predicted_enrollment']
    major_summary.to_csv('major_enrollment_predictions.csv', index=False)
    
    class_summary = predictions_df['predicted_class'].value_counts().reset_index()
    class_summary.columns = ['class_name', 'predicted_enrollment']
    class_summary.to_csv('class_enrollment_predictions.csv', index=False)
    
    print(f"Generated predictions for {len(predictions_df)} students")
    print("Prediction files saved:")
    print("- future_predictions.csv (detailed predictions)")
    print("- major_enrollment_predictions.csv (major summary)")
    print("- class_enrollment_predictions.csv (class summary)")
    
    return predictions_df

if __name__ == "__main__":
    # Create directories
    os.makedirs('outputs', exist_ok=True)
    os.makedirs('models', exist_ok=True)
    
    # Run the main pipeline
    results = main()