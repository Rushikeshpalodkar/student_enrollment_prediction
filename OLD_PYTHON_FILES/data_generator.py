import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

def generate_sample_data(n_students=5000, n_semesters=8):
    """Generate realistic sample student enrollment data"""
    
    np.random.seed(42)
    random.seed(42)
    
    # Define possible majors and classes
    majors = [
        'Computer Science', 'Business Administration', 'Psychology', 'Biology',
        'Engineering', 'Mathematics', 'English', 'History', 'Economics', 'Art'
    ]
    
    classes = {
        'Computer Science': ['Intro to Programming', 'Data Structures', 'Algorithms', 'Database Systems', 'Software Engineering'],
        'Business Administration': ['Accounting', 'Marketing', 'Finance', 'Management', 'Business Statistics'],
        'Psychology': ['Intro to Psychology', 'Statistics', 'Research Methods', 'Cognitive Psychology', 'Social Psychology'],
        'Biology': ['General Biology', 'Organic Chemistry', 'Genetics', 'Microbiology', 'Ecology'],
        'Engineering': ['Calculus', 'Physics', 'Engineering Design', 'Thermodynamics', 'Materials Science'],
        'Mathematics': ['Calculus I', 'Calculus II', 'Linear Algebra', 'Statistics', 'Discrete Math'],
        'English': ['Composition', 'Literature', 'Creative Writing', 'Literary Analysis', 'Grammar'],
        'History': ['World History', 'American History', 'Research Methods', 'Historical Analysis', 'Modern History'],
        'Economics': ['Microeconomics', 'Macroeconomics', 'Statistics', 'Econometrics', 'International Economics'],
        'Art': ['Drawing', 'Painting', 'Sculpture', 'Art History', 'Digital Art']
    }
    
    # Generate student records
    students_data = []
    
    for student_id in range(1, n_students + 1):
        # Student demographics
        age = np.random.normal(20, 2)
        age = max(18, min(25, age))
        
        gpa = np.random.normal(3.0, 0.5)
        gpa = max(2.0, min(4.0, gpa))
        
        # Choose a primary major (students might change)
        primary_major = np.random.choice(majors)
        
        # Generate semester-by-semester data
        current_major = None
        major_change_probability = 0.1
        
        for semester in range(1, n_semesters + 1):
            # Determine if student changes major
            if semester == 1 or (current_major is None):
                current_major = primary_major
            elif np.random.random() < major_change_probability:
                current_major = np.random.choice(majors)
            
            # Number of classes per semester (typically 4-6)
            n_classes = np.random.randint(3, 7)
            
            # Select classes (mix of major-specific and general education)
            semester_classes = []
            
            # 60% major-specific classes, 40% from other majors
            major_classes = int(n_classes * 0.6)
            other_classes = n_classes - major_classes
            
            # Add major-specific classes
            if current_major in classes:
                available_major_classes = classes[current_major]
                selected_major_classes = np.random.choice(
                    available_major_classes, 
                    min(major_classes, len(available_major_classes)), 
                    replace=False
                )
                semester_classes.extend(selected_major_classes)
            
            # Add classes from other majors
            for _ in range(other_classes):
                other_major = np.random.choice([m for m in majors if m != current_major])
                if other_major in classes:
                    other_class = np.random.choice(classes[other_major])
                    semester_classes.append(other_class)
            
            # Create record for each class enrollment
            for class_name in semester_classes:
                grade = np.random.normal(gpa, 0.3)
                grade = max(0.0, min(4.0, grade))
                
                students_data.append({
                    'student_id': student_id,
                    'semester': semester,
                    'age': round(age, 1),
                    'gpa': round(gpa, 2),
                    'major': current_major,
                    'class_name': class_name,
                    'grade': round(grade, 2),
                    'credits': np.random.choice([3, 4]),
                    'year': 2020 + (semester - 1) // 2,
                    'semester_type': 'Fall' if semester % 2 == 1 else 'Spring'
                })
    
    df = pd.DataFrame(students_data)
    return df

if __name__ == "__main__":
    # Generate sample data
    df = generate_sample_data(5000, 8)
    df.to_csv('student_enrollment_data.csv', index=False)
    print(f"Generated {len(df)} enrollment records for {df['student_id'].nunique()} students")
    print(f"Data saved to student_enrollment_data.csv")
    print(f"\nData preview:")
    print(df.head(10))