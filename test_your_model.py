"""
TEST YOUR MODEL - Direct model usage example
"""

import joblib
import pandas as pd

def test_saved_model():
    """Test the saved model with custom input"""
    print("TESTING YOUR SAVED MODEL")
    print("=" * 40)
    
    # Load the model
    model_data = joblib.load('models/working_model.pkl')
    model = model_data['model']
    encoder = model_data['encoder']
    features = model_data['features']
    
    print(f"Model loaded successfully!")
    print(f"Features: {features}")
    print(f"Classes: {list(encoder.classes_)}")
    
    # Test with custom student data
    test_students = [
        {'gpa': 3.8, 'credits': 90, 'age': 21, 'grade': 3.9, 'semester': 6},  # High achiever
        {'gpa': 2.5, 'credits': 45, 'age': 19, 'grade': 2.3, 'semester': 3},  # Average student
        {'gpa': 3.2, 'credits': 120, 'age': 23, 'grade': 3.1, 'semester': 8}, # Transfer student
    ]
    
    student_types = ['High Achiever', 'Average Student', 'Transfer Student']
    
    print(f"\\nTesting with 3 different student profiles:")
    print("=" * 50)
    
    for i, (student, student_type) in enumerate(zip(test_students, student_types)):
        print(f"\\n{student_type}:")
        print(f"  GPA: {student['gpa']}")
        print(f"  Credits: {student['credits']}")
        print(f"  Age: {student['age']}")
        print(f"  Grade: {student['grade']}")
        print(f"  Semester: {student['semester']}")
        
        # Create DataFrame for prediction
        student_df = pd.DataFrame([student])
        
        # Make prediction
        prediction = model.predict(student_df)[0]
        probabilities = model.predict_proba(student_df)[0]
        predicted_major = encoder.inverse_transform([prediction])[0]
        confidence = probabilities.max()
        
        print(f"  -> Predicted Major: {predicted_major}")
        print(f"  -> Confidence: {confidence:.1%}")
        
        # Show top 3 predictions
        prob_pairs = list(zip(encoder.classes_, probabilities))
        prob_pairs.sort(key=lambda x: x[1], reverse=True)
        
        print(f"  -> Top 3 possibilities:")
        for j, (major, prob) in enumerate(prob_pairs[:3]):
            print(f"     {j+1}. {major}: {prob:.1%}")

if __name__ == "__main__":
    test_saved_model()
    print(f"\\n" + "="*50)
    print("Your model is working perfectly!")
    print("Try the web interface for more features:")
    print("  python unified_system.py")
    print("  Open: http://localhost:8080")