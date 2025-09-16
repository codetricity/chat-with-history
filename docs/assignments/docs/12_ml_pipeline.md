---
theme: gaia
_class: lead
paginate: true
backgroundColor: #fff
backgroundImage: url('https://marp.app/assets/hero-background.svg')
---

![bg left:40% 80%](https://oppkey.com/static/logo.jpg)

# **Machine Learning Pipeline Assignment**
## End-to-End ML for Data Processing

**Build comprehensive ML pipelines for data analysis and insights**

---

# Assignment Overview

## What You'll Build

A comprehensive machine learning pipeline system that:
- **Data preprocessing** - Clean, transform, and prepare data for ML
- **Feature engineering** - Create meaningful features from raw data
- **Model training** - Train multiple ML models for different tasks
- **Model evaluation** - Comprehensive evaluation and validation
- **Model deployment** - Serve models via API endpoints
- **Monitoring** - Track model performance and data drift

---

# Problem Statement

## ML Pipeline Challenges

Real-world ML applications face several challenges:
- **Data quality** - Raw data is often messy and incomplete
- **Feature engineering** - Creating meaningful features from raw data
- **Model selection** - Choosing the right algorithm for the task
- **Evaluation** - Properly evaluating model performance
- **Deployment** - Serving models in production environments
- **Monitoring** - Tracking model performance over time

---

# Your Solution

## End-to-End ML Pipeline

Create a comprehensive ML pipeline that addresses these challenges:

1. **Data Pipeline** - Automated data processing and validation
2. **Feature Engineering** - Automated feature creation and selection
3. **Model Training** - Automated model training and hyperparameter tuning
4. **Model Evaluation** - Comprehensive evaluation and validation
5. **Model Deployment** - API endpoints for model serving
6. **Monitoring** - Real-time monitoring and alerting

---

# Technical Requirements

## Tech Stack

- **Python 3.8+** with type hints
- **Pandas & NumPy** - Data manipulation
- **Scikit-learn** - Machine learning algorithms
- **XGBoost** - Gradient boosting
- **TensorFlow/PyTorch** - Deep learning
- **MLflow** - Model management and tracking
- **FastAPI** - Model serving API
- **Docker** - Containerization

---

# Project Structure

## Recommended Architecture

```
ml_pipeline/
├── src/
│   ├── data/
│   │   ├── ingestion.py
│   │   ├── preprocessing.py
│   │   └── validation.py
│   ├── features/
│   │   ├── engineering.py
│   │   ├── selection.py
│   │   └── transformation.py
│   ├── models/
│   │   ├── training.py
│   │   ├── evaluation.py
│   │   └── deployment.py
│   ├── pipelines/
│   │   ├── training_pipeline.py
│   │   ├── inference_pipeline.py
│   │   └── monitoring_pipeline.py
│   └── api/
│       ├── endpoints.py
│       └── middleware.py
├── config/
│   ├── model_config.yaml
│   └── pipeline_config.yaml
├── models/
│   ├── trained_models/
│   └── model_artifacts/
├── data/
│   ├── raw/
│   ├── processed/
│   └── features/
└── tests/
    ├── test_data.py
    └── test_models.py
```

---

# Core Components

## 1. Data Preprocessing

```python
# src/data/preprocessing.py
import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional
from sklearn.preprocessing import StandardScaler, LabelEncoder, OneHotEncoder
from sklearn.impute import SimpleImputer, KNNImputer
from sklearn.feature_selection import SelectKBest, f_classif
import logging

class DataPreprocessor:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.scalers = {}
        self.encoders = {}
        self.imputers = {}
        self.logger = logging.getLogger(__name__)
    
    def preprocess(self, data: pd.DataFrame, 
                  target_column: Optional[str] = None) -> pd.DataFrame:
        """Main preprocessing pipeline"""
        self.logger.info("Starting data preprocessing")
        
        # Create a copy to avoid modifying original data
        processed_data = data.copy()
        
        # Handle missing values
        processed_data = self._handle_missing_values(processed_data)
        
        # Handle outliers
        processed_data = self._handle_outliers(processed_data)
        
        # Encode categorical variables
        processed_data = self._encode_categorical(processed_data)
        
        # Scale numerical variables
        processed_data = self._scale_numerical(processed_data)
        
        # Feature selection
        if target_column and target_column in processed_data.columns:
            processed_data = self._select_features(processed_data, target_column)
        
        self.logger.info("Data preprocessing completed")
        return processed_data
    
    def _handle_missing_values(self, data: pd.DataFrame) -> pd.DataFrame:
        """Handle missing values in the dataset"""
        self.logger.info("Handling missing values")
        
        for column in data.columns:
            if data[column].isnull().any():
                missing_count = data[column].isnull().sum()
                missing_percent = (missing_count / len(data)) * 100
                
                self.logger.info(f"Column {column}: {missing_count} missing values ({missing_percent:.2f}%)")
                
                if missing_percent > 50:
                    # Drop columns with more than 50% missing values
                    data = data.drop(columns=[column])
                    self.logger.info(f"Dropped column {column} due to high missing value percentage")
                elif data[column].dtype in ['object', 'category']:
                    # Use mode for categorical variables
                    mode_value = data[column].mode()[0] if not data[column].mode().empty else 'Unknown'
                    data[column] = data[column].fillna(mode_value)
                else:
                    # Use KNN imputation for numerical variables
                    if column not in self.imputers:
                        self.imputers[column] = KNNImputer(n_neighbors=5)
                        data[column] = self.imputers[column].fit_transform(data[[column]]).flatten()
                    else:
                        data[column] = self.imputers[column].transform(data[[column]]).flatten()
        
        return data
    
    def _handle_outliers(self, data: pd.DataFrame) -> pd.DataFrame:
        """Handle outliers using IQR method"""
        self.logger.info("Handling outliers")
        
        for column in data.select_dtypes(include=[np.number]).columns:
            Q1 = data[column].quantile(0.25)
            Q3 = data[column].quantile(0.75)
            IQR = Q3 - Q1
            
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            
            outliers = (data[column] < lower_bound) | (data[column] > upper_bound)
            outlier_count = outliers.sum()
            
            if outlier_count > 0:
                self.logger.info(f"Column {column}: {outlier_count} outliers detected")
                
                # Cap outliers instead of removing them
                data[column] = np.where(data[column] < lower_bound, lower_bound, data[column])
                data[column] = np.where(data[column] > upper_bound, upper_bound, data[column])
        
        return data
    
    def _encode_categorical(self, data: pd.DataFrame) -> pd.DataFrame:
        """Encode categorical variables"""
        self.logger.info("Encoding categorical variables")
        
        for column in data.select_dtypes(include=['object', 'category']).columns:
            unique_values = data[column].nunique()
            
            if unique_values <= 10:
                # Use label encoding for low cardinality
                if column not in self.encoders:
                    self.encoders[column] = LabelEncoder()
                    data[column] = self.encoders[column].fit_transform(data[column])
                else:
                    data[column] = self.encoders[column].transform(data[column])
            else:
                # Use one-hot encoding for high cardinality
                if column not in self.encoders:
                    self.encoders[column] = OneHotEncoder(sparse_output=False, handle_unknown='ignore')
                    encoded_data = self.encoders[column].fit_transform(data[[column]])
                    encoded_df = pd.DataFrame(encoded_data, columns=[f"{column}_{i}" for i in range(encoded_data.shape[1])])
                    data = pd.concat([data.drop(columns=[column]), encoded_df], axis=1)
                else:
                    encoded_data = self.encoders[column].transform(data[[column]])
                    encoded_df = pd.DataFrame(encoded_data, columns=[f"{column}_{i}" for i in range(encoded_data.shape[1])])
                    data = pd.concat([data.drop(columns=[column]), encoded_df], axis=1)
        
        return data
    
    def _scale_numerical(self, data: pd.DataFrame) -> pd.DataFrame:
        """Scale numerical variables"""
        self.logger.info("Scaling numerical variables")
        
        numerical_columns = data.select_dtypes(include=[np.number]).columns
        
        for column in numerical_columns:
            if column not in self.scalers:
                self.scalers[column] = StandardScaler()
                data[column] = self.scalers[column].fit_transform(data[[column]]).flatten()
            else:
                data[column] = self.scalers[column].transform(data[[column]]).flatten()
        
        return data
    
    def _select_features(self, data: pd.DataFrame, target_column: str) -> pd.DataFrame:
        """Select the most important features"""
        self.logger.info("Selecting features")
        
        X = data.drop(columns=[target_column])
        y = data[target_column]
        
        # Select top k features
        k = min(50, X.shape[1])  # Select top 50 features or all if less than 50
        selector = SelectKBest(score_func=f_classif, k=k)
        X_selected = selector.fit_transform(X, y)
        
        # Get selected feature names
        selected_features = X.columns[selector.get_support()].tolist()
        
        # Create new dataframe with selected features
        selected_data = pd.DataFrame(X_selected, columns=selected_features)
        selected_data[target_column] = y
        
        self.logger.info(f"Selected {len(selected_features)} features out of {X.shape[1]}")
        
        return selected_data
```

---

# Core Components

## 2. Feature Engineering

```python
# src/features/engineering.py
import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
import re
from datetime import datetime

class FeatureEngineer:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.vectorizers = {}
        self.pca_models = {}
        self.cluster_models = {}
    
    def engineer_features(self, data: pd.DataFrame, 
                         target_column: Optional[str] = None) -> pd.DataFrame:
        """Main feature engineering pipeline"""
        print("Starting feature engineering")
        
        # Create a copy to avoid modifying original data
        engineered_data = data.copy()
        
        # Text features
        engineered_data = self._create_text_features(engineered_data)
        
        # Temporal features
        engineered_data = self._create_temporal_features(engineered_data)
        
        # Numerical features
        engineered_data = self._create_numerical_features(engineered_data)
        
        # Categorical features
        engineered_data = self._create_categorical_features(engineered_data)
        
        # Interaction features
        engineered_data = self._create_interaction_features(engineered_data)
        
        # Dimensionality reduction
        if target_column and target_column in engineered_data.columns:
            engineered_data = self._apply_dimensionality_reduction(engineered_data, target_column)
        
        print("Feature engineering completed")
        return engineered_data
    
    def _create_text_features(self, data: pd.DataFrame) -> pd.DataFrame:
        """Create features from text columns"""
        text_columns = data.select_dtypes(include=['object']).columns
        
        for column in text_columns:
            if data[column].dtype == 'object':
                # Basic text features
                data[f'{column}_length'] = data[column].astype(str).str.len()
                data[f'{column}_word_count'] = data[column].astype(str).str.split().str.len()
                data[f'{column}_char_count'] = data[column].astype(str).str.replace(' ', '').str.len()
                
                # TF-IDF features
                if column not in self.vectorizers:
                    self.vectorizers[column] = TfidfVectorizer(max_features=100, stop_words='english')
                    tfidf_matrix = self.vectorizers[column].fit_transform(data[column].astype(str))
                else:
                    tfidf_matrix = self.vectorizers[column].transform(data[column].astype(str])
                
                # Add TF-IDF features
                tfidf_df = pd.DataFrame(tfidf_matrix.toarray(), 
                                      columns=[f'{column}_tfidf_{i}' for i in range(tfidf_matrix.shape[1])])
                data = pd.concat([data, tfidf_df], axis=1)
        
        return data
    
    def _create_temporal_features(self, data: pd.DataFrame) -> pd.DataFrame:
        """Create features from temporal columns"""
        temporal_columns = data.select_dtypes(include=['datetime64']).columns
        
        for column in temporal_columns:
            if data[column].dtype == 'datetime64[ns]':
                # Extract temporal components
                data[f'{column}_year'] = data[column].dt.year
                data[f'{column}_month'] = data[column].dt.month
                data[f'{column}_day'] = data[column].dt.day
                data[f'{column}_weekday'] = data[column].dt.weekday
                data[f'{column}_hour'] = data[column].dt.hour
                
                # Calculate time differences
                if len(data) > 1:
                    data[f'{column}_days_since_first'] = (data[column] - data[column].min()).dt.days
                    data[f'{column}_days_since_last'] = (data[column].max() - data[column]).dt.days
                
                # Cyclical encoding
                data[f'{column}_month_sin'] = np.sin(2 * np.pi * data[column].dt.month / 12)
                data[f'{column}_month_cos'] = np.cos(2 * np.pi * data[column].dt.month / 12)
                data[f'{column}_day_sin'] = np.sin(2 * np.pi * data[column].dt.day / 31)
                data[f'{column}_day_cos'] = np.cos(2 * np.pi * data[column].dt.day / 31)
        
        return data
    
    def _create_numerical_features(self, data: pd.DataFrame) -> pd.DataFrame:
        """Create features from numerical columns"""
        numerical_columns = data.select_dtypes(include=[np.number]).columns
        
        for column in numerical_columns:
            # Statistical features
            data[f'{column}_log'] = np.log1p(data[column])
            data[f'{column}_sqrt'] = np.sqrt(data[column])
            data[f'{column}_square'] = data[column] ** 2
            
            # Rolling statistics
            if len(data) > 10:
                data[f'{column}_rolling_mean_5'] = data[column].rolling(window=5).mean()
                data[f'{column}_rolling_std_5'] = data[column].rolling(window=5).std()
                data[f'{column}_rolling_mean_10'] = data[column].rolling(window=10).mean()
                data[f'{column}_rolling_std_10'] = data[column].rolling(window=10).std()
            
            # Percentile features
            data[f'{column}_percentile_25'] = data[column].quantile(0.25)
            data[f'{column}_percentile_75'] = data[column].quantile(0.75)
            data[f'{column}_iqr'] = data[f'{column}_percentile_75'] - data[f'{column}_percentile_25']
        
        return data
    
    def _create_categorical_features(self, data: pd.DataFrame) -> pd.DataFrame:
        """Create features from categorical columns"""
        categorical_columns = data.select_dtypes(include=['object', 'category']).columns
        
        for column in categorical_columns:
            # Frequency encoding
            freq_map = data[column].value_counts().to_dict()
            data[f'{column}_freq'] = data[column].map(freq_map)
            
            # Target encoding (if target column is available)
            if 'target' in data.columns:
                target_mean = data.groupby(column)['target'].mean()
                data[f'{column}_target_mean'] = data[column].map(target_mean)
        
        return data
    
    def _create_interaction_features(self, data: pd.DataFrame) -> pd.DataFrame:
        """Create interaction features between columns"""
        numerical_columns = data.select_dtypes(include=[np.number]).columns
        
        # Create pairwise interactions for top numerical columns
        top_columns = numerical_columns[:5]  # Limit to top 5 columns to avoid explosion
        
        for i, col1 in enumerate(top_columns):
            for col2 in top_columns[i+1:]:
                # Multiplication
                data[f'{col1}_x_{col2}'] = data[col1] * data[col2]
                
                # Division (avoid division by zero)
                data[f'{col1}_div_{col2}'] = np.where(data[col2] != 0, data[col1] / data[col2], 0)
                
                # Addition
                data[f'{col1}_plus_{col2}'] = data[col1] + data[col2]
                
                # Subtraction
                data[f'{col1}_minus_{col2}'] = data[col1] - data[col2]
        
        return data
    
    def _apply_dimensionality_reduction(self, data: pd.DataFrame, target_column: str) -> pd.DataFrame:
        """Apply dimensionality reduction techniques"""
        X = data.drop(columns=[target_column])
        y = data[target_column]
        
        # PCA
        if X.shape[1] > 50:
            n_components = min(50, X.shape[1])
            pca = PCA(n_components=n_components)
            X_pca = pca.fit_transform(X)
            
            # Create PCA features
            pca_df = pd.DataFrame(X_pca, columns=[f'pca_{i}' for i in range(n_components)])
            data = pd.concat([data, pca_df], axis=1)
        
        # Clustering
        if X.shape[1] > 10:
            n_clusters = min(10, X.shape[0] // 10)
            if n_clusters > 1:
                kmeans = KMeans(n_clusters=n_clusters, random_state=42)
                clusters = kmeans.fit_predict(X)
                data['cluster'] = clusters
        
        return data
```

---

# Core Components

## 3. Model Training

```python
# src/models/training.py
import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional, Tuple
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score
import xgboost as xgb
import joblib
import mlflow
import mlflow.sklearn
from datetime import datetime

class ModelTrainer:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.models = {}
        self.best_model = None
        self.best_score = 0
        self.training_history = []
    
    def train_models(self, X: pd.DataFrame, y: pd.Series, 
                    test_size: float = 0.2) -> Dict[str, Any]:
        """Train multiple models and select the best one"""
        print("Starting model training")
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=42, stratify=y
        )
        
        # Define models to train
        models = {
            'logistic_regression': LogisticRegression(random_state=42),
            'random_forest': RandomForestClassifier(random_state=42),
            'gradient_boosting': GradientBoostingClassifier(random_state=42),
            'svm': SVC(random_state=42, probability=True),
            'xgboost': xgb.XGBClassifier(random_state=42)
        }
        
        # Train and evaluate each model
        results = {}
        for name, model in models.items():
            print(f"Training {name}...")
            
            # Train model
            model.fit(X_train, y_train)
            
            # Evaluate model
            train_score = model.score(X_train, y_train)
            test_score = model.score(X_test, y_test)
            
            # Cross-validation score
            cv_scores = cross_val_score(model, X_train, y_train, cv=5)
            
            # Predictions
            y_pred = model.predict(X_test)
            y_pred_proba = model.predict_proba(X_test)[:, 1] if hasattr(model, 'predict_proba') else None
            
            # Calculate metrics
            auc_score = roc_auc_score(y_test, y_pred_proba) if y_pred_proba is not None else 0
            
            # Store results
            results[name] = {
                'model': model,
                'train_score': train_score,
                'test_score': test_score,
                'cv_mean': cv_scores.mean(),
                'cv_std': cv_scores.std(),
                'auc_score': auc_score,
                'predictions': y_pred,
                'probabilities': y_pred_proba
            }
            
            # Update best model
            if test_score > self.best_score:
                self.best_score = test_score
                self.best_model = model
                self.best_model_name = name
            
            print(f"{name} - Test Score: {test_score:.4f}, CV Score: {cv_scores.mean():.4f} (+/- {cv_scores.std() * 2:.4f})")
        
        # Hyperparameter tuning for best model
        if self.best_model_name in ['random_forest', 'gradient_boosting', 'xgboost']:
            print(f"Performing hyperparameter tuning for {self.best_model_name}...")
            tuned_model = self._hyperparameter_tuning(
                self.best_model_name, X_train, y_train, X_test, y_test
            )
            if tuned_model is not None:
                results[f'{self.best_model_name}_tuned'] = tuned_model
                self.best_model = tuned_model['model']
                self.best_model_name = f'{self.best_model_name}_tuned'
        
        # Log to MLflow
        self._log_to_mlflow(results, X_test, y_test)
        
        print(f"Best model: {self.best_model_name} with score: {self.best_score:.4f}")
        return results
    
    def _hyperparameter_tuning(self, model_name: str, X_train: pd.DataFrame, 
                              y_train: pd.Series, X_test: pd.DataFrame, 
                              y_test: pd.Series) -> Optional[Dict[str, Any]]:
        """Perform hyperparameter tuning for the best model"""
        param_grids = {
            'random_forest': {
                'n_estimators': [100, 200, 300],
                'max_depth': [10, 20, None],
                'min_samples_split': [2, 5, 10],
                'min_samples_leaf': [1, 2, 4]
            },
            'gradient_boosting': {
                'n_estimators': [100, 200, 300],
                'learning_rate': [0.01, 0.1, 0.2],
                'max_depth': [3, 5, 7],
                'subsample': [0.8, 0.9, 1.0]
            },
            'xgboost': {
                'n_estimators': [100, 200, 300],
                'learning_rate': [0.01, 0.1, 0.2],
                'max_depth': [3, 5, 7],
                'subsample': [0.8, 0.9, 1.0]
            }
        }
        
        if model_name not in param_grids:
            return None
        
        # Get base model
        base_models = {
            'random_forest': RandomForestClassifier(random_state=42),
            'gradient_boosting': GradientBoostingClassifier(random_state=42),
            'xgboost': xgb.XGBClassifier(random_state=42)
        }
        
        base_model = base_models[model_name]
        param_grid = param_grids[model_name]
        
        # Grid search
        grid_search = GridSearchCV(
            base_model, param_grid, cv=5, scoring='accuracy', n_jobs=-1
        )
        grid_search.fit(X_train, y_train)
        
        # Get best model
        best_model = grid_search.best_estimator_
        best_params = grid_search.best_params_
        best_score = grid_search.best_score_
        
        # Evaluate on test set
        test_score = best_model.score(X_test, y_test)
        y_pred = best_model.predict(X_test)
        y_pred_proba = best_model.predict_proba(X_test)[:, 1]
        auc_score = roc_auc_score(y_test, y_pred_proba)
        
        return {
            'model': best_model,
            'best_params': best_params,
            'best_score': best_score,
            'test_score': test_score,
            'auc_score': auc_score,
            'predictions': y_pred,
            'probabilities': y_pred_proba
        }
    
    def _log_to_mlflow(self, results: Dict[str, Any], X_test: pd.DataFrame, 
                      y_test: pd.Series) -> None:
        """Log training results to MLflow"""
        with mlflow.start_run():
            # Log parameters
            mlflow.log_param("test_size", 0.2)
            mlflow.log_param("random_state", 42)
            
            # Log metrics for each model
            for name, result in results.items():
                mlflow.log_metric(f"{name}_test_score", result['test_score'])
                mlflow.log_metric(f"{name}_auc_score", result['auc_score'])
            
            # Log best model
            if self.best_model is not None:
                mlflow.sklearn.log_model(self.best_model, "model")
                
                # Log model performance
                y_pred = self.best_model.predict(X_test)
                y_pred_proba = self.best_model.predict_proba(X_test)[:, 1]
                
                # Classification report
                report = classification_report(y_test, y_pred, output_dict=True)
                for metric, value in report.items():
                    if isinstance(value, dict):
                        for sub_metric, sub_value in value.items():
                            mlflow.log_metric(f"{metric}_{sub_metric}", sub_value)
                    else:
                        mlflow.log_metric(metric, value)
    
    def save_model(self, filepath: str) -> None:
        """Save the best model to disk"""
        if self.best_model is not None:
            joblib.dump(self.best_model, filepath)
            print(f"Model saved to {filepath}")
        else:
            print("No model to save")
    
    def load_model(self, filepath: str) -> None:
        """Load a model from disk"""
        self.best_model = joblib.load(filepath)
        print(f"Model loaded from {filepath}")
```

---

# Core Components

## 4. Model Deployment

```python
# src/api/endpoints.py
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
import pandas as pd
import numpy as np
import joblib
import logging

# Initialize FastAPI app
app = FastAPI(title="ML Pipeline API", version="1.0.0")

# Global model storage
models = {}
model_metadata = {}

class PredictionRequest(BaseModel):
    features: Dict[str, Any]
    model_name: Optional[str] = None

class PredictionResponse(BaseModel):
    prediction: Any
    probability: Optional[float] = None
    model_name: str
    confidence: Optional[float] = None

class ModelInfo(BaseModel):
    name: str
    accuracy: float
    auc_score: float
    features: List[str]
    created_at: str

@app.on_event("startup")
async def startup_event():
    """Load models on startup"""
    # Load pre-trained models
    # This would typically load from a model registry or file system
    pass

@app.post("/predict", response_model=PredictionResponse)
async def predict(request: PredictionRequest):
    """Make a prediction using the specified model"""
    try:
        # Get model name
        model_name = request.model_name or "best_model"
        
        if model_name not in models:
            raise HTTPException(status_code=404, detail=f"Model {model_name} not found")
        
        model = models[model_name]
        
        # Convert features to DataFrame
        features_df = pd.DataFrame([request.features])
        
        # Make prediction
        prediction = model.predict(features_df)[0]
        
        # Get probability if available
        probability = None
        if hasattr(model, 'predict_proba'):
            proba = model.predict_proba(features_df)[0]
            probability = float(max(proba))
        
        # Calculate confidence
        confidence = probability if probability else 0.5
        
        return PredictionResponse(
            prediction=prediction,
            probability=probability,
            model_name=model_name,
            confidence=confidence
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/predict_batch", response_model=List[PredictionResponse])
async def predict_batch(requests: List[PredictionRequest]):
    """Make predictions for multiple samples"""
    try:
        results = []
        
        for request in requests:
            # Get model name
            model_name = request.model_name or "best_model"
            
            if model_name not in models:
                raise HTTPException(status_code=404, detail=f"Model {model_name} not found")
            
            model = models[model_name]
            
            # Convert features to DataFrame
            features_df = pd.DataFrame([request.features])
            
            # Make prediction
            prediction = model.predict(features_df)[0]
            
            # Get probability if available
            probability = None
            if hasattr(model, 'predict_proba'):
                proba = model.predict_proba(features_df)[0]
                probability = float(max(proba))
            
            # Calculate confidence
            confidence = probability if probability else 0.5
            
            results.append(PredictionResponse(
                prediction=prediction,
                probability=probability,
                model_name=model_name,
                confidence=confidence
            ))
        
        return results
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/models", response_model=List[ModelInfo])
async def list_models():
    """List all available models"""
    model_list = []
    
    for name, model in models.items():
        if name in model_metadata:
            metadata = model_metadata[name]
            model_list.append(ModelInfo(
                name=name,
                accuracy=metadata.get('accuracy', 0.0),
                auc_score=metadata.get('auc_score', 0.0),
                features=metadata.get('features', []),
                created_at=metadata.get('created_at', '')
            ))
    
    return model_list

@app.get("/models/{model_name}", response_model=ModelInfo)
async def get_model_info(model_name: str):
    """Get information about a specific model"""
    if model_name not in models:
        raise HTTPException(status_code=404, detail=f"Model {model_name} not found")
    
    if model_name not in model_metadata:
        raise HTTPException(status_code=404, detail=f"Metadata for model {model_name} not found")
    
    metadata = model_metadata[model_name]
    return ModelInfo(
        name=model_name,
        accuracy=metadata.get('accuracy', 0.0),
        auc_score=metadata.get('auc_score', 0.0),
        features=metadata.get('features', []),
        created_at=metadata.get('created_at', '')
    )

@app.post("/models/{model_name}/load")
async def load_model(model_name: str, filepath: str):
    """Load a model from disk"""
    try:
        model = joblib.load(filepath)
        models[model_name] = model
        
        # Load metadata if available
        metadata_file = filepath.replace('.pkl', '_metadata.json')
        if os.path.exists(metadata_file):
            import json
            with open(metadata_file, 'r') as f:
                model_metadata[model_name] = json.load(f)
        
        return {"message": f"Model {model_name} loaded successfully"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "models_loaded": len(models)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

---

# Success Criteria

## Must-Have Features

- [ ] **Data Preprocessing** - Automated data cleaning and transformation
- [ ] **Feature Engineering** - Automated feature creation and selection
- [ ] **Model Training** - Multiple ML algorithms with hyperparameter tuning
- [ ] **Model Evaluation** - Comprehensive evaluation and validation
- [ ] **Model Deployment** - API endpoints for model serving
- [ ] **Model Management** - Model versioning and tracking
- [ ] **Monitoring** - Model performance monitoring
- [ ] **Documentation** - Comprehensive documentation and examples

---

# Bonus Challenges

## Advanced Features

- [ ] **AutoML** - Automated model selection and hyperparameter tuning
- [ ] **Model Ensembling** - Combine multiple models for better performance
- [ ] **Online Learning** - Update models with new data
- [ ] **A/B Testing** - Compare different models in production
- [ ] **Model Explainability** - Explain model predictions
- [ ] **Data Drift Detection** - Detect when data distribution changes
- [ ] **Model Retraining** - Automated model retraining pipeline
- [ ] **Real-time Monitoring** - Real-time model performance monitoring

---

# Getting Started

## Setup Instructions

1. **Set up environment** - Install required packages and dependencies
2. **Prepare data** - Clean and prepare your dataset
3. **Implement preprocessing** - Build data preprocessing pipeline
4. **Create features** - Implement feature engineering
5. **Train models** - Train multiple ML models
6. **Evaluate performance** - Compare model performance
7. **Deploy models** - Create API endpoints for model serving
8. **Monitor performance** - Set up monitoring and alerting

---

# Dependencies

## requirements.txt

```txt
pandas>=2.0.0
numpy>=1.24.0
scikit-learn>=1.3.0
xgboost>=1.7.0
tensorflow>=2.13.0
mlflow>=2.5.0
fastapi>=0.100.0
uvicorn>=0.23.0
pydantic>=2.0.0
joblib>=1.3.0
matplotlib>=3.7.0
seaborn>=0.12.0
plotly>=5.15.0
pytest>=7.0.0
```

---

# Resources

## Helpful Links

- **Scikit-learn** - https://scikit-learn.org/
- **XGBoost** - https://xgboost.readthedocs.io/
- **MLflow** - https://mlflow.org/
- **FastAPI** - https://fastapi.tiangolo.com/
- **Feature Engineering** - https://www.featuretools.com/
- **Model Deployment** - https://mlflow.org/docs/latest/models.html

---

# Let's Build ML Pipelines!

## Ready to Start?

**This assignment will teach you:**
- End-to-end ML pipeline development
- Data preprocessing and feature engineering
- Model training and evaluation
- Model deployment and serving
- ML model management and monitoring
- Best practices for production ML systems

**Start with basic preprocessing and build up to a comprehensive ML pipeline!**

---

# Next Steps

## After Completing This Assignment

1. **Deploy your models** - Set up production model serving
2. **Monitor performance** - Track model performance in production
3. **Share your work** - Document your ML pipeline and results
4. **Contribute to open source** - Share your ML pipeline components
5. **Move to the next track** - Try data visualization or advanced analytics next!

**Happy ML pipeline building! 🚀**
