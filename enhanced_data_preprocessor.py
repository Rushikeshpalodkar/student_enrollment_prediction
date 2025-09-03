import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, StandardScaler, RobustScaler
from sklearn.model_selection import train_test_split
from sklearn.feature_selection import SelectKBest, f_classif, mutual_info_classif
from sklearn.impute import KNNImputer
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

class EnhancedStudentDataPreprocessor:
    def __init__(self):
        self.label_encoders = {}
        self.scaler = RobustScaler()  # More robust to outliers than StandardScaler
        self.feature_columns = []
        self.feature_names = []
        self.class_names = []
        self.data_quality_report = {}
        self.outlier_indices = []
        
    def load_and_validate_data(self, filepath):
        """Enhanced data loading with validation"""
        try:
            df = pd.read_csv(filepath)
            print(f"[OK] Loaded {len(df)} records from {filepath}")
            
            # Basic data validation
            self.validate_data_structure(df)
            
            return df
        except Exception as e:
            print(f"[ERROR] Error loading data: {e}")
            return None
    
    def validate_data_structure(self, df):
        """Validate the structure and quality of the dataset"""
        print("\n[VALIDATION] DATA VALIDATION REPORT")
        print("=" * 40)
        
        validation_report = {
            'total_records': len(df),
            'total_features': len(df.columns),
            'missing_values': df.isnull().sum().sum(),
            'duplicate_records': df.duplicated().sum(),
            'numeric_features': len(df.select_dtypes(include=[np.number]).columns),
            'categorical_features': len(df.select_dtypes(include=[object]).columns)
        }
        
        print(f"Total Records: {validation_report['total_records']:,}")
        print(f"Total Features: {validation_report['total_features']}")
        print(f"Missing Values: {validation_report['missing_values']:,}")
        print(f"Duplicate Records: {validation_report['duplicate_records']:,}")
        print(f"Numeric Features: {validation_report['numeric_features']}")
        print(f"Categorical Features: {validation_report['categorical_features']}")
        
        # Check for potential issues
        issues = []
        if validation_report['missing_values'] > 0:
            issues.append(f"[WARNING] Found {validation_report['missing_values']} missing values")
        if validation_report['duplicate_records'] > 0:
            issues.append(f"[WARNING] Found {validation_report['duplicate_records']} duplicate records")
        
        if issues:
            print("\nData Quality Issues:")
            for issue in issues:
                print(f"  {issue}")
        else:
            print("\n[OK] No major data quality issues detected")
        
        self.data_quality_report = validation_report
        return validation_report
    
    def advanced_outlier_detection(self, df, method='isolation_forest'):
        """Advanced outlier detection using multiple methods"""
        print(f"\n[OUTLIERS] OUTLIER DETECTION using {method}")
        print("=" * 40)
        
        numeric_columns = df.select_dtypes(include=[np.number]).columns.tolist()
        numeric_df = df[numeric_columns]
        
        if method == 'isolation_forest':
            from sklearn.ensemble import IsolationForest
            detector = IsolationForest(contamination=0.1, random_state=42)
            outlier_labels = detector.fit_predict(numeric_df.fillna(numeric_df.mean()))
            outlier_indices = df.index[outlier_labels == -1].tolist()
            
        elif method == 'z_score':
            # Z-score method (absolute z-score > 3)
            z_scores = np.abs(stats.zscore(numeric_df.fillna(numeric_df.mean())))
            outlier_mask = (z_scores > 3).any(axis=1)
            outlier_indices = df.index[outlier_mask].tolist()
            
        elif method == 'iqr':
            # Interquartile Range method
            outlier_indices = []
            for column in numeric_columns:
                Q1 = df[column].quantile(0.25)
                Q3 = df[column].quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - 1.5 * IQR
                upper_bound = Q3 + 1.5 * IQR
                column_outliers = df.index[(df[column] < lower_bound) | (df[column] > upper_bound)].tolist()
                outlier_indices.extend(column_outliers)
            outlier_indices = list(set(outlier_indices))  # Remove duplicates
        
        print(f"Found {len(outlier_indices)} outliers ({len(outlier_indices)/len(df)*100:.2f}% of data)")
        
        # Store outlier indices for later analysis
        self.outlier_indices = outlier_indices
        
        # Create outlier visualization
        self.visualize_outliers(df, outlier_indices, numeric_columns)
        
        return outlier_indices
    
    def visualize_outliers(self, df, outlier_indices, numeric_columns):
        """Create visualizations for outlier analysis"""
        if len(numeric_columns) > 4:
            numeric_columns = numeric_columns[:4]  # Limit to first 4 for visualization
        
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        axes = axes.ravel()
        
        for i, column in enumerate(numeric_columns):
            if i < len(axes):
                # Box plot with outliers highlighted
                normal_data = df.loc[~df.index.isin(outlier_indices), column]
                outlier_data = df.loc[df.index.isin(outlier_indices), column]
                
                axes[i].boxplot(normal_data.dropna(), patch_artist=True, 
                               boxprops=dict(facecolor='lightblue'))
                if len(outlier_data) > 0:
                    axes[i].scatter([1] * len(outlier_data), outlier_data, 
                                   color='red', alpha=0.6, s=30)
                axes[i].set_title(f'{column} - Outliers in Red')
                axes[i].set_ylabel(column)
        
        plt.tight_layout()
        plt.savefig('outputs/outlier_analysis.png', dpi=300, bbox_inches='tight')
        plt.show()
    
    def advanced_missing_value_handling(self, df, strategy='knn'):
        """Advanced missing value imputation"""
        print(f"\n[MISSING] MISSING VALUE HANDLING using {strategy}")
        print("=" * 40)
        
        missing_info = df.isnull().sum()
        missing_features = missing_info[missing_info > 0]
        
        if len(missing_features) == 0:
            print("[OK] No missing values found")
            return df
        
        print("Missing values by feature:")
        for feature, count in missing_features.items():
            percentage = (count / len(df)) * 100
            print(f"  {feature}: {count} ({percentage:.1f}%)")
        
        df_imputed = df.copy()
        
        if strategy == 'knn':
            # KNN Imputation for numeric columns
            numeric_columns = df.select_dtypes(include=[np.number]).columns.tolist()
            if len(numeric_columns) > 0:
                knn_imputer = KNNImputer(n_neighbors=5)
                df_imputed[numeric_columns] = knn_imputer.fit_transform(df[numeric_columns])
            
            # Mode imputation for categorical columns
            categorical_columns = df.select_dtypes(include=[object]).columns.tolist()
            for col in categorical_columns:
                if df[col].isnull().sum() > 0:
                    mode_value = df[col].mode()[0] if len(df[col].mode()) > 0 else 'Unknown'
                    df_imputed[col] = df[col].fillna(mode_value)
        
        elif strategy == 'advanced':
            # Advanced strategy based on feature type and distribution
            for col in missing_features.index:
                if df[col].dtype in ['int64', 'float64']:
                    # For numeric: use median if skewed, mean if normal
                    if abs(df[col].skew()) > 1:  # Skewed data
                        fill_value = df[col].median()
                    else:  # Normal distribution
                        fill_value = df[col].mean()
                    df_imputed[col] = df[col].fillna(fill_value)
                else:
                    # For categorical: use mode or create 'Unknown' category
                    mode_value = df[col].mode()[0] if len(df[col].mode()) > 0 else 'Unknown'
                    df_imputed[col] = df[col].fillna(mode_value)
        
        print(f"[OK] Imputation completed. Missing values reduced to: {df_imputed.isnull().sum().sum()}")
        return df_imputed
    
    def advanced_feature_engineering(self, df):
        """Enhanced feature engineering with sophisticated derived features"""
        print("\n[FEATURES] ADVANCED FEATURE ENGINEERING")
        print("=" * 40)
        
        df_enhanced = df.copy()
        new_features = []
        
        # Ensure data is sorted for time-based features
        if 'student_id' in df.columns and 'semester' in df.columns:
            df_enhanced = df_enhanced.sort_values(['student_id', 'semester'])
        
        # 1. Academic Performance Features
        if 'gpa' in df.columns:
            # GPA categories
            df_enhanced['gpa_category'] = pd.cut(df_enhanced['gpa'], 
                                                bins=[0, 2.0, 2.5, 3.0, 3.5, 4.0],
                                                labels=['Poor', 'Below Avg', 'Average', 'Good', 'Excellent'])
            new_features.append('gpa_category')
            
            # GPA trend (if multiple records per student)
            if 'student_id' in df.columns:
                df_enhanced['gpa_trend'] = df_enhanced.groupby('student_id')['gpa'].pct_change()
                df_enhanced['gpa_improvement'] = (df_enhanced['gpa_trend'] > 0).astype(int)
                new_features.extend(['gpa_trend', 'gpa_improvement'])
        
        # 2. Credit and Course Load Features
        if 'credits' in df.columns:
            df_enhanced['credit_load_category'] = pd.cut(df_enhanced['credits'],
                                                        bins=[0, 6, 12, 18, 24],
                                                        labels=['Part-time', 'Half-time', 'Full-time', 'Overload'])
            
            if 'student_id' in df.columns:
                df_enhanced['total_credits'] = df_enhanced.groupby('student_id')['credits'].cumsum()
                df_enhanced['avg_credits_per_semester'] = df_enhanced.groupby('student_id')['credits'].expanding().mean().values
                new_features.extend(['credit_load_category', 'total_credits', 'avg_credits_per_semester'])
        
        # 3. Semester and Time-based Features
        if 'semester' in df.columns:
            # Convert semester to string if it's not already
            df_enhanced['semester'] = df_enhanced['semester'].astype(str)
            
            # Extract numeric part from semester
            try:
                df_enhanced['semester_numeric'] = df_enhanced['semester'].str.extract('(\d+)').astype(float)
            except:
                # If extraction fails, just use the semester as is (if it's already numeric)
                df_enhanced['semester_numeric'] = pd.to_numeric(df_enhanced['semester'], errors='coerce')
            
            df_enhanced['is_fall_semester'] = df_enhanced['semester'].str.contains('Fall', case=False, na=False).astype(int)
            df_enhanced['is_spring_semester'] = df_enhanced['semester'].str.contains('Spring', case=False, na=False).astype(int)
            new_features.extend(['semester_numeric', 'is_fall_semester', 'is_spring_semester'])
            
            if 'student_id' in df.columns:
                df_enhanced['semester_count'] = df_enhanced.groupby('student_id').cumcount() + 1
                new_features.append('semester_count')
        
        # 4. Major Stability and Change Patterns
        if 'major' in df.columns and 'student_id' in df.columns:
            # Count major changes
            major_changes = df_enhanced.groupby('student_id')['major'].apply(
                lambda x: (x != x.shift()).sum() - 1
            ).fillna(0)
            df_enhanced['major_changes'] = df_enhanced['student_id'].map(major_changes)
            
            # Major stability (same major for how many semesters)
            df_enhanced['major_stability'] = df_enhanced.groupby(['student_id', 'major']).cumcount() + 1
            new_features.extend(['major_changes', 'major_stability'])
        
        # 5. Grade Performance Features
        if 'grade' in df.columns:
            # Grade categories
            df_enhanced['grade_letter'] = pd.cut(df_enhanced['grade'],
                                               bins=[0, 1.0, 1.67, 2.33, 2.67, 3.0, 3.33, 3.67, 4.0],
                                               labels=['F', 'D', 'D+', 'C', 'C+', 'B', 'B+', 'A'])
            
            if 'student_id' in df.columns:
                # Grade trend
                df_enhanced['grade_trend'] = df_enhanced.groupby('student_id')['grade'].pct_change()
                df_enhanced['consistent_performance'] = df_enhanced.groupby('student_id')['grade'].rolling(3, min_periods=1).std().values
                new_features.extend(['grade_letter', 'grade_trend', 'consistent_performance'])
        
        # 6. Age and Demographic Features
        if 'age' in df.columns:
            df_enhanced['age_category'] = pd.cut(df_enhanced['age'],
                                               bins=[0, 18, 22, 25, 30, 100],
                                               labels=['Traditional', 'Young Adult', 'Adult', 'Mature', 'Senior'])
            new_features.append('age_category')
        
        # 7. Interaction Features (for highly correlated features)
        if 'gpa' in df.columns and 'credits' in df.columns:
            df_enhanced['gpa_credits_interaction'] = df_enhanced['gpa'] * df_enhanced['credits']
            new_features.append('gpa_credits_interaction')
        
        # 8. Statistical Features per Student
        if 'student_id' in df.columns and 'grade' in df.columns:
            # Rolling statistics
            df_enhanced['grade_rolling_mean'] = df_enhanced.groupby('student_id')['grade'].rolling(3, min_periods=1).mean().values
            df_enhanced['grade_rolling_std'] = df_enhanced.groupby('student_id')['grade'].rolling(3, min_periods=1).std().values
            new_features.extend(['grade_rolling_mean', 'grade_rolling_std'])
        
        print(f"[OK] Created {len(new_features)} new features:")
        for feature in new_features[:10]:  # Show first 10
            print(f"  - {feature}")
        if len(new_features) > 10:
            print(f"  ... and {len(new_features) - 10} more features")
        
        return df_enhanced, new_features
    
    def intelligent_feature_selection(self, X, y, method='mutual_info', k=50):
        """Intelligent feature selection using multiple methods"""
        print(f"\n[SELECTION] FEATURE SELECTION using {method}")
        print("=" * 40)
        
        print(f"Original features: {X.shape[1]}")
        
        if method == 'mutual_info':
            # Mutual Information based selection
            selector = SelectKBest(score_func=mutual_info_classif, k=min(k, X.shape[1]))
        elif method == 'f_classif':
            # F-statistic based selection
            selector = SelectKBest(score_func=f_classif, k=min(k, X.shape[1]))
        else:
            print("Unknown method, using mutual_info")
            selector = SelectKBest(score_func=mutual_info_classif, k=min(k, X.shape[1]))
        
        X_selected = selector.fit_transform(X, y)
        selected_features = selector.get_support(indices=True)
        
        print(f"Selected features: {X_selected.shape[1]}")
        print(f"Feature reduction: {((X.shape[1] - X_selected.shape[1]) / X.shape[1] * 100):.1f}%")
        
        # Get feature scores
        feature_scores = pd.DataFrame({
            'feature_idx': range(len(selector.scores_)),
            'feature_name': self.feature_names if self.feature_names else [f'feature_{i}' for i in range(X.shape[1])],
            'score': selector.scores_,
            'selected': selector.get_support()
        }).sort_values('score', ascending=False)
        
        print(f"\nTop 10 selected features:")
        for idx, row in feature_scores[feature_scores['selected']].head(10).iterrows():
            print(f"  {row['feature_name']}: {row['score']:.4f}")
        
        return X_selected, selected_features, feature_scores
    
    def comprehensive_data_preprocessing(self, df, target_column, test_size=0.2, handle_outliers=True):
        """Complete preprocessing pipeline"""
        print("\n[PREPROCESSING] COMPREHENSIVE DATA PREPROCESSING PIPELINE")
        print("=" * 60)
        
        # 1. Data Validation
        self.validate_data_structure(df)
        
        # 2. Handle missing values
        df_clean = self.advanced_missing_value_handling(df)
        
        # 3. Outlier detection and handling
        if handle_outliers:
            outlier_indices = self.advanced_outlier_detection(df_clean)
            print(f"\nOutlier handling: Found {len(outlier_indices)} outliers")
            
            # Option to remove outliers (you can modify this logic)
            if len(outlier_indices) > 0:
                print("Removing outliers from dataset...")
                df_clean = df_clean.drop(index=outlier_indices)
                print(f"Dataset size after outlier removal: {len(df_clean)}")
        
        # 4. Feature Engineering
        df_enhanced, new_features = self.advanced_feature_engineering(df_clean)
        
        # 5. Prepare features and target
        if target_column not in df_enhanced.columns:
            raise ValueError(f"Target column '{target_column}' not found in dataset")
        
        # Separate features and target
        X = df_enhanced.drop(columns=[target_column])
        y = df_enhanced[target_column]
        
        # 6. Handle categorical variables
        X_processed = self.encode_categorical_features(X)
        
        # 7. Store feature names and class names
        self.feature_names = list(X_processed.columns)
        self.class_names = sorted(y.unique().astype(str))
        
        # 8. Feature selection
        if X_processed.shape[1] > 50:  # Only if we have many features
            X_selected, selected_idx, feature_scores = self.intelligent_feature_selection(
                X_processed, y, k=50
            )
            self.feature_names = [self.feature_names[i] for i in selected_idx]
            X_processed = pd.DataFrame(X_selected, columns=self.feature_names)
        
        # 9. Train-test split
        X_train, X_test, y_train, y_test = train_test_split(
            X_processed, y, test_size=test_size, random_state=42, stratify=y
        )
        
        # 10. Scale features
        X_train_scaled = pd.DataFrame(
            self.scaler.fit_transform(X_train),
            columns=X_train.columns,
            index=X_train.index
        )
        X_test_scaled = pd.DataFrame(
            self.scaler.transform(X_test),
            columns=X_test.columns,
            index=X_test.index
        )
        
        print("\n[OK] PREPROCESSING COMPLETED")
        print(f"Final dataset shape: {X_train_scaled.shape[0] + X_test_scaled.shape[0]} rows, {X_train_scaled.shape[1]} features")
        print(f"Training set: {X_train_scaled.shape[0]} samples")
        print(f"Testing set: {X_test_scaled.shape[0]} samples")
        print(f"Number of classes: {len(self.class_names)}")
        
        return X_train_scaled, X_test_scaled, y_train, y_test
    
    def encode_categorical_features(self, X):
        """Enhanced categorical feature encoding"""
        X_encoded = X.copy()
        
        categorical_columns = X.select_dtypes(include=['object', 'category']).columns
        
        if len(categorical_columns) > 0:
            print(f"Encoding {len(categorical_columns)} categorical features...")
            
            for col in categorical_columns:
                # Use label encoding for ordinal and binary features
                if col not in self.label_encoders:
                    self.label_encoders[col] = LabelEncoder()
                    X_encoded[col] = self.label_encoders[col].fit_transform(X[col].astype(str))
                else:
                    X_encoded[col] = self.label_encoders[col].transform(X[col].astype(str))
        
        # Ensure all columns are numeric
        X_encoded = X_encoded.select_dtypes(include=[np.number])
        
        return X_encoded
    
    def generate_data_quality_report(self, df):
        """Generate comprehensive data quality report"""
        print("\n📊 COMPREHENSIVE DATA QUALITY REPORT")
        print("=" * 50)
        
        # Basic statistics
        print("DATASET OVERVIEW:")
        print(f"Shape: {df.shape}")
        print(f"Memory usage: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
        
        # Missing values analysis
        missing_df = df.isnull().sum()
        missing_df = missing_df[missing_df > 0].sort_values(ascending=False)
        
        if len(missing_df) > 0:
            print(f"\nMISSING VALUES:")
            for col, count in missing_df.items():
                print(f"  {col}: {count} ({count/len(df)*100:.1f}%)")
        else:
            print(f"\n[OK] NO MISSING VALUES")
        
        # Data types
        print(f"\nDATA TYPES:")
        type_counts = df.dtypes.value_counts()
        for dtype, count in type_counts.items():
            print(f"  {dtype}: {count} columns")
        
        # Duplicates
        duplicates = df.duplicated().sum()
        print(f"\nDUPLICATE RECORDS: {duplicates} ({duplicates/len(df)*100:.1f}%)")
        
        # Numeric column statistics
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) > 0:
            print(f"\nNUMERIC FEATURES SUMMARY:")
            desc = df[numeric_cols].describe()
            print(desc.round(3))
        
        return {
            'shape': df.shape,
            'missing_values': missing_df.to_dict(),
            'data_types': type_counts.to_dict(),
            'duplicates': duplicates,
            'numeric_summary': df[numeric_cols].describe().to_dict() if len(numeric_cols) > 0 else {}
        }

if __name__ == "__main__":
    print("[LOADED] Enhanced Data Preprocessor loaded successfully!")
    print("Features include:")
    print("  * Advanced outlier detection (Isolation Forest, Z-score, IQR)")
    print("  * Intelligent missing value handling (KNN imputation)")
    print("  * Sophisticated feature engineering")
    print("  * Intelligent feature selection")
    print("  * Comprehensive data quality reporting")
    print("  * Robust scaling for outlier resilience")