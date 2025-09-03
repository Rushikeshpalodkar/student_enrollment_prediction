import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split

class StudentDataPreprocessor:
    def __init__(self):
        self.label_encoders = {}
        self.scaler = StandardScaler()
        self.feature_columns = []
        
    def load_data(self, filepath):
        """Load student enrollment data"""
        try:
            df = pd.read_csv(filepath)
            print(f"Loaded {len(df)} records from {filepath}")
            return df
        except Exception as e:
            print(f"Error loading data: {e}")
            return None
    
    def clean_data(self, df):
        """Clean and prepare the data"""
        # Remove duplicates
        df = df.drop_duplicates()
        
        # Handle missing values
        df = df.fillna({
            'gpa': df['gpa'].mean(),
            'age': df['age'].mean(),
            'grade': df['grade'].mean()
        })
        
        # Remove invalid records
        df = df[(df['gpa'] >= 0) & (df['gpa'] <= 4.0)]
        df = df[(df['grade'] >= 0) & (df['grade'] <= 4.0)]
        df = df[df['age'] >= 16]
        
        return df
    
    def engineer_features(self, df):
        """Create new features for better prediction"""
        # Sort by student and semester for sequential features
        df = df.sort_values(['student_id', 'semester'])
        
        # Calculate cumulative features per student
        df['cumulative_gpa'] = df.groupby('student_id')['grade'].expanding().mean().values
        df['total_credits'] = df.groupby('student_id')['credits'].cumsum()
        df['semester_count'] = df.groupby('student_id').cumcount() + 1
        
        # Create major stability features
        df['major_changes'] = df.groupby('student_id')['major'].apply(
            lambda x: (x != x.shift()).cumsum()
        ).values
        
        # Previous semester performance
        df['prev_semester_gpa'] = df.groupby('student_id')['grade'].shift(1)
        df['prev_semester_gpa'] = df['prev_semester_gpa'].fillna(df['gpa'])
        
        # Class difficulty (based on average grade for that class)
        class_difficulty = df.groupby('class_name')['grade'].mean()
        df['class_avg_grade'] = df['class_name'].map(class_difficulty)
        
        # Major popularity (number of students in each major)
        major_counts = df.groupby(['semester', 'major']).size().reset_index(name='major_popularity')
        df = df.merge(major_counts, on=['semester', 'major'], how='left')
        
        return df
    
    def prepare_features(self, df, target_column='major'):
        """Prepare features for ML models"""
        # Select relevant features
        feature_cols = [
            'semester', 'age', 'gpa', 'grade', 'credits',
            'cumulative_gpa', 'total_credits', 'semester_count',
            'major_changes', 'prev_semester_gpa', 'class_avg_grade',
            'major_popularity', 'year'
        ]
        
        # Categorical features to encode
        categorical_cols = ['semester_type', 'class_name']
        
        # Create feature matrix
        X = df[feature_cols + categorical_cols].copy()
        
        # Encode categorical variables
        for col in categorical_cols:
            if col not in self.label_encoders:
                self.label_encoders[col] = LabelEncoder()
                X[col] = self.label_encoders[col].fit_transform(X[col].astype(str))
            else:
                X[col] = self.label_encoders[col].transform(X[col].astype(str))
        
        # Encode target variable
        if target_column not in self.label_encoders:
            self.label_encoders[target_column] = LabelEncoder()
            y = self.label_encoders[target_column].fit_transform(df[target_column])
        else:
            y = self.label_encoders[target_column].transform(df[target_column])
        
        # Store feature columns
        self.feature_columns = X.columns.tolist()
        
        # Scale features
        X_scaled = self.scaler.fit_transform(X)
        X_scaled = pd.DataFrame(X_scaled, columns=X.columns, index=X.index)
        
        return X_scaled, y
    
    def split_data(self, X, y, test_size=0.2, random_state=42):
        """Split data into training and testing sets"""
        return train_test_split(X, y, test_size=test_size, random_state=random_state, stratify=y)
    
    def get_class_names(self, target_column='major'):
        """Get class names for the target variable"""
        if target_column in self.label_encoders:
            return self.label_encoders[target_column].classes_
        return None
    
    def inverse_transform_target(self, encoded_values, target_column='major'):
        """Convert encoded target values back to original labels"""
        if target_column in self.label_encoders:
            return self.label_encoders[target_column].inverse_transform(encoded_values)
        return encoded_values

if __name__ == "__main__":
    # Test the preprocessor
    preprocessor = StudentDataPreprocessor()
    
    # Load data
    df = preprocessor.load_data('student_enrollment_data.csv')
    if df is not None:
        print("Original data shape:", df.shape)
        
        # Clean data
        df_clean = preprocessor.clean_data(df)
        print("After cleaning:", df_clean.shape)
        
        # Engineer features
        df_engineered = preprocessor.engineer_features(df_clean)
        print("After feature engineering:", df_engineered.shape)
        
        # Prepare features
        X, y = preprocessor.prepare_features(df_engineered, target_column='major')
        print("Features shape:", X.shape)
        print("Target shape:", y.shape)
        
        # Split data
        X_train, X_test, y_train, y_test = preprocessor.split_data(X, y)
        print("Training set:", X_train.shape)
        print("Test set:", X_test.shape)
        
        print("Class names:", preprocessor.get_class_names('major'))