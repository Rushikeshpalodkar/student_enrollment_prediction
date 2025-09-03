import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.model_selection import cross_val_score, GridSearchCV
import xgboost as xgb
import lightgbm as lgb
import joblib
import matplotlib.pyplot as plt
import seaborn as sns

class StudentEnrollmentModels:
    def __init__(self):
        self.models = {
            'random_forest': RandomForestClassifier(n_estimators=100, random_state=42),
            'gradient_boosting': GradientBoostingClassifier(n_estimators=100, random_state=42),
            'xgboost': xgb.XGBClassifier(n_estimators=100, random_state=42),
            'lightgbm': lgb.LGBMClassifier(n_estimators=100, random_state=42, verbose=-1),
            'logistic_regression': LogisticRegression(random_state=42, max_iter=1000),
            'svm': SVC(random_state=42, probability=True)
        }
        self.trained_models = {}
        self.model_scores = {}
        self.best_model = None
        self.best_model_name = None
        
    def train_all_models(self, X_train, y_train, X_test, y_test):
        """Train all models and evaluate their performance"""
        print("Training multiple ML models...")
        
        for name, model in self.models.items():
            print(f"\nTraining {name}...")
            
            try:
                # Train the model
                model.fit(X_train, y_train)
                
                # Make predictions
                y_pred = model.predict(X_test)
                y_pred_proba = model.predict_proba(X_test) if hasattr(model, 'predict_proba') else None
                
                # Calculate accuracy
                accuracy = accuracy_score(y_test, y_pred)
                
                # Cross-validation score
                cv_scores = cross_val_score(model, X_train, y_train, cv=5)
                cv_mean = cv_scores.mean()
                cv_std = cv_scores.std()
                
                # Store results
                self.trained_models[name] = model
                self.model_scores[name] = {
                    'accuracy': accuracy,
                    'cv_mean': cv_mean,
                    'cv_std': cv_std,
                    'predictions': y_pred,
                    'probabilities': y_pred_proba
                }
                
                print(f"{name} - Accuracy: {accuracy:.4f}, CV Score: {cv_mean:.4f} (+/- {cv_std * 2:.4f})")
                
            except Exception as e:
                print(f"Error training {name}: {e}")
                continue
        
        # Find best model
        best_cv_score = 0
        for name, scores in self.model_scores.items():
            if scores['cv_mean'] > best_cv_score:
                best_cv_score = scores['cv_mean']
                self.best_model_name = name
                self.best_model = self.trained_models[name]
        
        print(f"\nBest model: {self.best_model_name} with CV score: {best_cv_score:.4f}")
        
        return self.model_scores
    
    def optimize_best_model(self, X_train, y_train, X_test, y_test):
        """Optimize hyperparameters for the best performing model"""
        if self.best_model_name is None:
            print("No best model found. Run train_all_models first.")
            return None
        
        print(f"\nOptimizing hyperparameters for {self.best_model_name}...")
        
        # Define parameter grids for different models
        param_grids = {
            'random_forest': {
                'n_estimators': [100, 200, 300],
                'max_depth': [10, 20, None],
                'min_samples_split': [2, 5, 10],
                'min_samples_leaf': [1, 2, 4]
            },
            'xgboost': {
                'n_estimators': [100, 200, 300],
                'max_depth': [3, 6, 9],
                'learning_rate': [0.01, 0.1, 0.2],
                'subsample': [0.8, 0.9, 1.0]
            },
            'lightgbm': {
                'n_estimators': [100, 200, 300],
                'max_depth': [3, 6, 9],
                'learning_rate': [0.01, 0.1, 0.2],
                'num_leaves': [31, 50, 100]
            },
            'gradient_boosting': {
                'n_estimators': [100, 200],
                'max_depth': [3, 6, 9],
                'learning_rate': [0.01, 0.1, 0.2]
            }
        }
        
        if self.best_model_name in param_grids:
            param_grid = param_grids[self.best_model_name]
            
            # Perform grid search
            grid_search = GridSearchCV(
                self.models[self.best_model_name],
                param_grid,
                cv=3,  # Reduced for faster execution
                scoring='accuracy',
                n_jobs=-1,
                verbose=1
            )
            
            grid_search.fit(X_train, y_train)
            
            # Update best model
            self.best_model = grid_search.best_estimator_
            self.trained_models[f'{self.best_model_name}_optimized'] = self.best_model
            
            # Evaluate optimized model
            y_pred = self.best_model.predict(X_test)
            accuracy = accuracy_score(y_test, y_pred)
            
            print(f"Best parameters: {grid_search.best_params_}")
            print(f"Optimized model accuracy: {accuracy:.4f}")
            
            return grid_search.best_params_
        else:
            print(f"No optimization parameters defined for {self.best_model_name}")
            return None
    
    def evaluate_model(self, model_name, X_test, y_test, class_names=None):
        """Generate detailed evaluation for a specific model"""
        if model_name not in self.trained_models:
            print(f"Model {model_name} not found.")
            return None
        
        model = self.trained_models[model_name]
        y_pred = model.predict(X_test)
        
        # Classification report
        print(f"\n=== {model_name.upper()} EVALUATION ===")
        print("Classification Report:")
        print(classification_report(y_test, y_pred, target_names=class_names))
        
        # Confusion Matrix
        cm = confusion_matrix(y_test, y_pred)
        
        plt.figure(figsize=(12, 8))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                   xticklabels=class_names, yticklabels=class_names)
        plt.title(f'Confusion Matrix - {model_name}')
        plt.xlabel('Predicted')
        plt.ylabel('Actual')
        plt.tight_layout()
        plt.savefig(f'confusion_matrix_{model_name}.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        return {
            'classification_report': classification_report(y_test, y_pred, target_names=class_names, output_dict=True),
            'confusion_matrix': cm,
            'accuracy': accuracy_score(y_test, y_pred)
        }
    
    def get_feature_importance(self, model_name, feature_names, top_n=15):
        """Get and plot feature importance for tree-based models"""
        if model_name not in self.trained_models:
            print(f"Model {model_name} not found.")
            return None
        
        model = self.trained_models[model_name]
        
        # Check if model has feature importance
        if hasattr(model, 'feature_importances_'):
            importances = model.feature_importances_
            
            # Create feature importance dataframe
            feature_imp = pd.DataFrame({
                'feature': feature_names,
                'importance': importances
            }).sort_values('importance', ascending=False)
            
            # Plot top features
            plt.figure(figsize=(10, 8))
            top_features = feature_imp.head(top_n)
            plt.barh(range(len(top_features)), top_features['importance'])
            plt.yticks(range(len(top_features)), top_features['feature'])
            plt.xlabel('Feature Importance')
            plt.title(f'Top {top_n} Feature Importances - {model_name}')
            plt.gca().invert_yaxis()
            plt.tight_layout()
            plt.savefig(f'feature_importance_{model_name}.png', dpi=300, bbox_inches='tight')
            plt.show()
            
            return feature_imp
        else:
            print(f"Model {model_name} does not have feature importance.")
            return None
    
    def predict_student_major(self, student_features, model_name=None):
        """Predict major for a new student"""
        if model_name is None:
            model_name = self.best_model_name
        
        if model_name not in self.trained_models:
            print(f"Model {model_name} not found.")
            return None
        
        model = self.trained_models[model_name]
        
        # Make prediction
        prediction = model.predict([student_features])[0]
        probabilities = model.predict_proba([student_features])[0] if hasattr(model, 'predict_proba') else None
        
        return {
            'prediction': prediction,
            'probabilities': probabilities,
            'model_used': model_name
        }
    
    def save_best_model(self, filepath='best_student_model.pkl'):
        """Save the best trained model"""
        if self.best_model is None:
            print("No best model to save.")
            return False
        
        try:
            joblib.dump({
                'model': self.best_model,
                'model_name': self.best_model_name,
                'model_scores': self.model_scores
            }, filepath)
            print(f"Best model saved to {filepath}")
            return True
        except Exception as e:
            print(f"Error saving model: {e}")
            return False
    
    def load_model(self, filepath='best_student_model.pkl'):
        """Load a saved model"""
        try:
            loaded_data = joblib.load(filepath)
            self.best_model = loaded_data['model']
            self.best_model_name = loaded_data['model_name']
            self.model_scores = loaded_data.get('model_scores', {})
            self.trained_models[self.best_model_name] = self.best_model
            print(f"Model loaded from {filepath}")
            return True
        except Exception as e:
            print(f"Error loading model: {e}")
            return False
    
    def compare_models(self):
        """Compare performance of all trained models"""
        if not self.model_scores:
            print("No models trained yet.")
            return None
        
        # Create comparison dataframe
        comparison_data = []
        for name, scores in self.model_scores.items():
            comparison_data.append({
                'Model': name,
                'Accuracy': scores['accuracy'],
                'CV Mean': scores['cv_mean'],
                'CV Std': scores['cv_std']
            })
        
        comparison_df = pd.DataFrame(comparison_data)
        comparison_df = comparison_df.sort_values('CV Mean', ascending=False)
        
        print("\n=== MODEL COMPARISON ===")
        print(comparison_df.to_string(index=False))
        
        # Plot comparison
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        # Accuracy comparison
        ax1.bar(comparison_df['Model'], comparison_df['Accuracy'])
        ax1.set_title('Model Accuracy Comparison')
        ax1.set_xlabel('Model')
        ax1.set_ylabel('Accuracy')
        ax1.tick_params(axis='x', rotation=45)
        
        # CV Score comparison with error bars
        ax2.bar(comparison_df['Model'], comparison_df['CV Mean'], 
                yerr=comparison_df['CV Std'], capsize=5)
        ax2.set_title('Cross-Validation Score Comparison')
        ax2.set_xlabel('Model')
        ax2.set_ylabel('CV Score')
        ax2.tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        plt.savefig('model_comparison.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        return comparison_df

if __name__ == "__main__":
    # This would be run as part of the main training pipeline
    print("ML Models module loaded successfully.")
    print("Use this module with the data preprocessor to train models.")