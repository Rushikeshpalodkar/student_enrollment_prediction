import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, VotingClassifier, StackingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.metrics import (classification_report, confusion_matrix, accuracy_score, 
                            precision_score, recall_score, f1_score, roc_auc_score)
from sklearn.model_selection import cross_val_score, RandomizedSearchCV, StratifiedKFold
from sklearn.utils.class_weight import compute_class_weight
import xgboost as xgb
import lightgbm as lgb
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings('ignore')

class EnhancedStudentEnrollmentModels:
    def __init__(self):
        self.base_models = {
            'random_forest': RandomForestClassifier(random_state=42, n_jobs=-1),
            'gradient_boosting': GradientBoostingClassifier(random_state=42),
            'xgboost': xgb.XGBClassifier(random_state=42, n_jobs=-1, eval_metric='logloss'),
            'lightgbm': lgb.LGBMClassifier(random_state=42, n_jobs=-1, verbose=-1),
            'logistic_regression': LogisticRegression(random_state=42, max_iter=2000),
            'svm': SVC(random_state=42, probability=True)
        }
        self.trained_models = {}
        self.model_metrics = {}
        self.best_model = None
        self.best_model_name = None
        self.class_weights = None
        self.feature_names = None
        self.class_names = None
        
    def calculate_class_weights(self, y):
        """Calculate class weights to handle imbalanced data"""
        unique_classes = np.unique(y)
        weights = compute_class_weight('balanced', classes=unique_classes, y=y)
        weight_dict = dict(zip(unique_classes, weights))
        self.class_weights = weight_dict
        print(f"Calculated class weights: {weight_dict}")
        return weight_dict
    
    def get_hyperparameter_grids(self, class_weight=None):
        """Get optimized hyperparameter grids for RandomizedSearchCV"""
        return {
            'random_forest': {
                'n_estimators': [100, 200, 300, 500],
                'max_depth': [10, 15, 20, 25, None],
                'min_samples_split': [2, 5, 10, 15],
                'min_samples_leaf': [1, 2, 4, 8],
                'max_features': ['sqrt', 'log2', None],
                'class_weight': ['balanced', class_weight, None],
                'bootstrap': [True, False]
            },
            'xgboost': {
                'n_estimators': [100, 200, 300, 500],
                'max_depth': [3, 5, 6, 8, 10],
                'learning_rate': [0.01, 0.05, 0.1, 0.15, 0.2],
                'subsample': [0.7, 0.8, 0.9, 1.0],
                'colsample_bytree': [0.7, 0.8, 0.9, 1.0],
                'reg_alpha': [0, 0.1, 0.5, 1.0],
                'reg_lambda': [0, 0.1, 0.5, 1.0]
            },
            'lightgbm': {
                'n_estimators': [100, 200, 300, 500],
                'max_depth': [3, 5, 6, 8, 10],
                'learning_rate': [0.01, 0.05, 0.1, 0.15, 0.2],
                'num_leaves': [20, 31, 50, 75, 100],
                'subsample': [0.7, 0.8, 0.9, 1.0],
                'colsample_bytree': [0.7, 0.8, 0.9, 1.0],
                'reg_alpha': [0, 0.1, 0.5, 1.0],
                'reg_lambda': [0, 0.1, 0.5, 1.0],
                'class_weight': ['balanced', None]
            },
            'gradient_boosting': {
                'n_estimators': [100, 200, 300],
                'max_depth': [3, 5, 6, 8],
                'learning_rate': [0.01, 0.05, 0.1, 0.15, 0.2],
                'subsample': [0.7, 0.8, 0.9, 1.0],
                'min_samples_split': [2, 5, 10],
                'min_samples_leaf': [1, 2, 4]
            },
            'logistic_regression': {
                'C': [0.1, 0.5, 1.0, 2.0, 5.0, 10.0],
                'penalty': ['l1', 'l2', 'elasticnet'],
                'solver': ['liblinear', 'saga'],
                'class_weight': ['balanced', class_weight, None],
                'max_iter': [1000, 2000, 3000]
            },
            'svm': {
                'C': [0.1, 1, 10, 100],
                'kernel': ['rbf', 'poly', 'sigmoid'],
                'gamma': ['scale', 'auto', 0.001, 0.01, 0.1, 1],
                'class_weight': ['balanced', class_weight, None]
            }
        }
    
    def train_and_optimize_models(self, X_train, y_train, X_test, y_test, 
                                 feature_names=None, class_names=None):
        """Train all models with hyperparameter optimization"""
        self.feature_names = feature_names
        self.class_names = class_names
        
        print("=== ENHANCED MODEL TRAINING WITH OPTIMIZATION ===")
        
        # Calculate class weights
        class_weight = self.calculate_class_weights(y_train)
        param_grids = self.get_hyperparameter_grids(class_weight)
        
        # Stratified K-Fold for better cross-validation
        cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
        
        for name, model in self.base_models.items():
            print(f"\n[TRAIN] Training and optimizing {name}...")
            
            try:
                # Hyperparameter optimization with RandomizedSearchCV
                if name in param_grids:
                    print(f"   Performing hyperparameter optimization...")
                    search = RandomizedSearchCV(
                        model, 
                        param_grids[name],
                        n_iter=20,  # Reduced for reasonable training time
                        cv=cv,
                        scoring='f1_weighted',  # Use F1 for imbalanced data
                        n_jobs=-1,
                        random_state=42,
                        verbose=0
                    )
                    search.fit(X_train, y_train)
                    optimized_model = search.best_estimator_
                    print(f"   Best parameters: {search.best_params_}")
                    print(f"   Best CV F1 score: {search.best_score_:.4f}")
                else:
                    # Use default model if no param grid defined
                    optimized_model = model
                    optimized_model.fit(X_train, y_train)
                
                # Store the optimized model
                self.trained_models[name] = optimized_model
                
                # Comprehensive evaluation
                metrics = self.evaluate_model_comprehensive(
                    optimized_model, X_test, y_test, name
                )
                self.model_metrics[name] = metrics
                
                print(f"   [OK] {name} completed - F1 Score: {metrics['f1_weighted']:.4f}")
                
            except Exception as e:
                print(f"   [ERROR] Error training {name}: {e}")
                continue
        
        # Find best model based on F1 score
        best_f1_score = 0
        for name, metrics in self.model_metrics.items():
            if metrics['f1_weighted'] > best_f1_score:
                best_f1_score = metrics['f1_weighted']
                self.best_model_name = name
                self.best_model = self.trained_models[name]
        
        print(f"\n[BEST] Best model: {self.best_model_name} with F1 score: {best_f1_score:.4f}")
        
        # Create stacking ensemble
        self.create_stacking_ensemble(X_train, y_train, X_test, y_test)
        
        return self.model_metrics
    
    def create_stacking_ensemble(self, X_train, y_train, X_test, y_test):
        """Create a stacking ensemble of the best performing models"""
        print("\n🔄 Creating stacking ensemble...")
        
        # Select top 3 models based on F1 score
        sorted_models = sorted(self.model_metrics.items(), 
                             key=lambda x: x[1]['f1_weighted'], reverse=True)
        top_models = [(name, self.trained_models[name]) for name, _ in sorted_models[:3]]
        
        print(f"   Using top models: {[name for name, _ in top_models]}")
        
        # Create stacking classifier
        stacking_classifier = StackingClassifier(
            estimators=top_models,
            final_estimator=LogisticRegression(random_state=42, max_iter=2000),
            cv=3,
            n_jobs=-1
        )
        
        # Train stacking ensemble
        stacking_classifier.fit(X_train, y_train)
        self.trained_models['stacking_ensemble'] = stacking_classifier
        
        # Evaluate stacking ensemble
        metrics = self.evaluate_model_comprehensive(
            stacking_classifier, X_test, y_test, 'stacking_ensemble'
        )
        self.model_metrics['stacking_ensemble'] = metrics
        
        # Update best model if stacking is better
        if metrics['f1_weighted'] > self.model_metrics[self.best_model_name]['f1_weighted']:
            self.best_model_name = 'stacking_ensemble'
            self.best_model = stacking_classifier
            print(f"   [NEW BEST] Stacking ensemble is the new best model!")
        
        print(f"   [OK] Stacking ensemble F1 score: {metrics['f1_weighted']:.4f}")
    
    def evaluate_model_comprehensive(self, model, X_test, y_test, model_name):
        """Comprehensive model evaluation with multiple metrics"""
        y_pred = model.predict(X_test)
        y_pred_proba = model.predict_proba(X_test) if hasattr(model, 'predict_proba') else None
        
        # Calculate all metrics
        metrics = {
            'accuracy': accuracy_score(y_test, y_pred),
            'precision_macro': precision_score(y_test, y_pred, average='macro', zero_division=0),
            'recall_macro': recall_score(y_test, y_pred, average='macro', zero_division=0),
            'f1_macro': f1_score(y_test, y_pred, average='macro', zero_division=0),
            'precision_weighted': precision_score(y_test, y_pred, average='weighted', zero_division=0),
            'recall_weighted': recall_score(y_test, y_pred, average='weighted', zero_division=0),
            'f1_weighted': f1_score(y_test, y_pred, average='weighted', zero_division=0),
            'predictions': y_pred,
            'probabilities': y_pred_proba
        }
        
        # Add AUC if probabilities available and binary/multiclass
        if y_pred_proba is not None:
            try:
                if len(np.unique(y_test)) == 2:
                    metrics['auc'] = roc_auc_score(y_test, y_pred_proba[:, 1])
                else:
                    metrics['auc'] = roc_auc_score(y_test, y_pred_proba, multi_class='ovr', average='weighted')
            except:
                metrics['auc'] = None
        
        return metrics
    
    def generate_detailed_evaluation_report(self, model_name, X_test, y_test, save_plots=True):
        """Generate a comprehensive evaluation report for a model"""
        if model_name not in self.trained_models:
            print(f"Model {model_name} not found.")
            return None
        
        model = self.trained_models[model_name]
        metrics = self.model_metrics[model_name]
        y_pred = metrics['predictions']
        
        print(f"\n[REPORT] DETAILED EVALUATION REPORT: {model_name.upper()}")
        print("=" * 60)
        
        # Performance Metrics
        print(f"Accuracy:           {metrics['accuracy']:.4f}")
        print(f"Precision (macro):  {metrics['precision_macro']:.4f}")
        print(f"Recall (macro):     {metrics['recall_macro']:.4f}")
        print(f"F1 Score (macro):   {metrics['f1_macro']:.4f}")
        print(f"F1 Score (weighted): {metrics['f1_weighted']:.4f}")
        if metrics.get('auc'):
            print(f"AUC Score:          {metrics['auc']:.4f}")
        
        # Classification Report
        print(f"\n📈 CLASSIFICATION REPORT:")
        print(classification_report(y_test, y_pred, 
                                   target_names=self.class_names if self.class_names else None))
        
        # Confusion Matrix Visualization
        if save_plots:
            self.plot_enhanced_confusion_matrix(y_test, y_pred, model_name)
            
        # Feature Importance (if available)
        if hasattr(model, 'feature_importances_') and self.feature_names is not None:
            self.plot_feature_importance_interactive(model, model_name)
        
        return {
            'metrics': metrics,
            'classification_report': classification_report(y_test, y_pred, output_dict=True),
            'confusion_matrix': confusion_matrix(y_test, y_pred)
        }
    
    def plot_enhanced_confusion_matrix(self, y_test, y_pred, model_name):
        """Create an enhanced confusion matrix with percentages"""
        cm = confusion_matrix(y_test, y_pred)
        cm_percent = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis] * 100
        
        # Create interactive plotly heatmap
        labels = self.class_names if self.class_names else [f'Class {i}' for i in range(len(cm))]
        
        fig = go.Figure(data=go.Heatmap(
            z=cm_percent,
            x=labels,
            y=labels,
            colorscale='Blues',
            text=[[f'{cm[i][j]}<br>({cm_percent[i][j]:.1f}%)' 
                   for j in range(len(cm[0]))] for i in range(len(cm))],
            texttemplate="%{text}",
            textfont={"size": 10},
            hoverongaps=False
        ))
        
        fig.update_layout(
            title=f'Confusion Matrix - {model_name}',
            xaxis_title='Predicted Class',
            yaxis_title='True Class',
            width=600,
            height=500
        )
        
        fig.write_html(f'outputs/confusion_matrix_{model_name}.html')
        fig.show()
    
    def plot_feature_importance_interactive(self, model, model_name, top_n=15):
        """Create interactive feature importance plot"""
        if hasattr(model, 'feature_importances_'):
            importances = model.feature_importances_
        elif hasattr(model, 'coef_'):
            importances = np.abs(model.coef_[0]) if len(model.coef_.shape) > 1 else np.abs(model.coef_)
        else:
            print(f"Model {model_name} doesn't support feature importance")
            return None
        
        # Create feature importance dataframe
        feature_imp = pd.DataFrame({
            'feature': self.feature_names,
            'importance': importances
        }).sort_values('importance', ascending=False).head(top_n)
        
        # Create interactive bar plot
        fig = go.Figure(data=[
            go.Bar(x=feature_imp['importance'], 
                   y=feature_imp['feature'],
                   orientation='h',
                   marker_color='rgba(55, 128, 191, 0.7)',
                   text=feature_imp['importance'].round(4),
                   textposition='auto')
        ])
        
        fig.update_layout(
            title=f'Top {top_n} Feature Importances - {model_name}',
            xaxis_title='Importance Score',
            yaxis_title='Features',
            yaxis={'categoryorder': 'total ascending'},
            width=800,
            height=600
        )
        
        fig.write_html(f'outputs/feature_importance_{model_name}.html')
        fig.show()
        
        return feature_imp
    
    def predict_with_confidence(self, student_features, model_name=None):
        """Enhanced prediction with confidence scores and explanations"""
        if model_name is None:
            model_name = self.best_model_name
        
        if model_name not in self.trained_models:
            return {'error': f"Model {model_name} not found"}
        
        model = self.trained_models[model_name]
        
        # Make prediction
        prediction = model.predict([student_features])[0]
        probabilities = model.predict_proba([student_features])[0] if hasattr(model, 'predict_proba') else None
        
        # Calculate confidence
        if probabilities is not None:
            confidence = float(np.max(probabilities))
            prediction_proba = {
                class_name: float(prob) 
                for class_name, prob in zip(self.class_names or range(len(probabilities)), probabilities)
            }
        else:
            confidence = 0.5
            prediction_proba = {}
        
        # Get feature importance for explanation (if available)
        explanation = self.get_prediction_explanation(model, student_features, model_name)
        
        return {
            'prediction': prediction,
            'confidence': confidence,
            'prediction_probabilities': prediction_proba,
            'model_used': model_name,
            'explanation': explanation,
            'confidence_level': self.get_confidence_level(confidence)
        }
    
    def get_prediction_explanation(self, model, student_features, model_name):
        """Generate explanation for the prediction"""
        try:
            if hasattr(model, 'feature_importances_') and self.feature_names is not None:
                importances = model.feature_importances_
                
                # Get top 5 most important features for this prediction
                feature_contributions = []
                for i, (feature, importance, value) in enumerate(
                    zip(self.feature_names, importances, student_features)
                ):
                    contribution_score = importance * abs(value) if value != 0 else 0
                    feature_contributions.append({
                        'feature': feature,
                        'importance': float(importance),
                        'value': float(value),
                        'contribution': float(contribution_score)
                    })
                
                # Sort by contribution and return top 5
                feature_contributions = sorted(
                    feature_contributions, 
                    key=lambda x: x['contribution'], 
                    reverse=True
                )[:5]
                
                return {
                    'top_features': feature_contributions,
                    'explanation_text': f"Top factors influencing this prediction based on {model_name} model"
                }
        except Exception as e:
            print(f"Error generating explanation: {e}")
        
        return {'explanation_text': 'Feature explanation not available for this model'}
    
    def get_confidence_level(self, confidence):
        """Convert confidence score to categorical level"""
        if confidence >= 0.9:
            return 'Very High'
        elif confidence >= 0.8:
            return 'High'
        elif confidence >= 0.7:
            return 'Moderate'
        elif confidence >= 0.6:
            return 'Low'
        else:
            return 'Very Low'
    
    def create_model_comparison_dashboard(self):
        """Create an interactive dashboard comparing all models"""
        if not self.model_metrics:
            print("No models trained yet.")
            return None
        
        # Prepare data for comparison
        models = []
        metrics_data = {
            'accuracy': [],
            'f1_weighted': [],
            'precision_weighted': [],
            'recall_weighted': []
        }
        
        for name, metrics in self.model_metrics.items():
            models.append(name)
            for metric in metrics_data.keys():
                metrics_data[metric].append(metrics.get(metric, 0))
        
        # Create subplots
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Accuracy', 'F1 Score (Weighted)', 'Precision (Weighted)', 'Recall (Weighted)'),
            specs=[[{"type": "bar"}, {"type": "bar"}],
                   [{"type": "bar"}, {"type": "bar"}]]
        )
        
        colors = px.colors.qualitative.Set3[:len(models)]
        
        # Add traces for each metric
        fig.add_trace(
            go.Bar(x=models, y=metrics_data['accuracy'], name='Accuracy',
                   marker_color=colors, showlegend=False),
            row=1, col=1
        )
        
        fig.add_trace(
            go.Bar(x=models, y=metrics_data['f1_weighted'], name='F1 Score',
                   marker_color=colors, showlegend=False),
            row=1, col=2
        )
        
        fig.add_trace(
            go.Bar(x=models, y=metrics_data['precision_weighted'], name='Precision',
                   marker_color=colors, showlegend=False),
            row=2, col=1
        )
        
        fig.add_trace(
            go.Bar(x=models, y=metrics_data['recall_weighted'], name='Recall',
                   marker_color=colors, showlegend=False),
            row=2, col=2
        )
        
        # Update layout
        fig.update_layout(
            title_text="Model Performance Comparison Dashboard",
            showlegend=False,
            width=1000,
            height=700
        )
        
        # Update y-axes to start from 0
        fig.update_yaxes(range=[0, 1])
        
        fig.write_html('outputs/model_comparison_dashboard.html')
        fig.show()
        
        return fig
    
    def save_enhanced_model(self, filepath='models/enhanced_student_model.pkl'):
        """Save the best trained model with all metadata"""
        if self.best_model is None:
            print("No best model to save.")
            return False
        
        # Create models directory if it doesn't exist
        import os
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        try:
            model_data = {
                'model': self.best_model,
                'model_name': self.best_model_name,
                'model_metrics': self.model_metrics,
                'all_trained_models': self.trained_models,
                'class_weights': self.class_weights,
                'feature_names': self.feature_names,
                'class_names': self.class_names
            }
            
            joblib.dump(model_data, filepath)
            print(f"[OK] Enhanced model saved to {filepath}")
            return True
        except Exception as e:
            print(f"[ERROR] Error saving model: {e}")
            return False
    
    def load_enhanced_model(self, filepath='models/enhanced_student_model.pkl'):
        """Load a saved enhanced model"""
        try:
            model_data = joblib.load(filepath)
            self.best_model = model_data['model']
            self.best_model_name = model_data['model_name']
            self.model_metrics = model_data.get('model_metrics', {})
            self.trained_models = model_data.get('all_trained_models', {})
            self.class_weights = model_data.get('class_weights', None)
            self.feature_names = model_data.get('feature_names', None)
            self.class_names = model_data.get('class_names', None)
            
            print(f"[OK] Enhanced model loaded from {filepath}")
            print(f"   Best model: {self.best_model_name}")
            if self.best_model_name in self.model_metrics:
                metrics = self.model_metrics[self.best_model_name]
                print(f"   F1 Score: {metrics.get('f1_weighted', 'N/A'):.4f}")
            return True
        except Exception as e:
            print(f"[ERROR] Error loading model: {e}")
            return False

if __name__ == "__main__":
    print("[LOADED] Enhanced ML Models module loaded successfully!")
    print("This module includes:")
    print("  * Advanced hyperparameter optimization")
    print("  * Class weighting for imbalanced data") 
    print("  * Stacking ensemble methods")
    print("  * Comprehensive evaluation metrics")
    print("  * Interactive visualizations")
    print("  * Explainable AI features")