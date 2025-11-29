"""
Ensemble Machine Learning Models for Epigenetic Age Prediction
Random Forest, XGBoost, ElasticNet with Cross-Validation
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import ElasticNet
from sklearn.model_selection import cross_val_score, KFold
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error, r2_score, mean_squared_error
import xgboost as xgb
from scipy import stats
import warnings
warnings.filterwarnings('ignore')


@dataclass
class ModelMetrics:
    """Performance metrics for a machine learning model"""
    model_name: str
    mae: float
    rmse: float
    r_squared: float
    cv_mae_mean: float
    cv_mae_std: float
    cv_r2_mean: float
    cv_r2_std: float
    feature_importance: Optional[Dict[str, float]] = None


@dataclass
class EnsemblePrediction:
    """Ensemble prediction result"""
    predicted_age: float
    confidence_interval: Tuple[float, float]
    model_predictions: Dict[str, float]
    model_weights: Dict[str, float]
    uncertainty: float


class EnsembleAgePredictor:
    """
    Ensemble machine learning model for epigenetic age prediction.
    Combines Random Forest, XGBoost, and ElasticNet with optimized weights.
    """
    
    def __init__(self, n_estimators: int = 100, random_state: int = 42):
        self.n_estimators = n_estimators
        self.random_state = random_state
        self.scaler = StandardScaler()
        self.models = {}
        self.model_weights = {}
        self.is_fitted = False
        self.feature_names = []
        
        self._initialize_models()
    
    def _initialize_models(self):
        """Initialize the ensemble models with optimized hyperparameters"""
        
        self.models['random_forest'] = RandomForestRegressor(
            n_estimators=self.n_estimators,
            max_depth=15,
            min_samples_split=5,
            min_samples_leaf=2,
            max_features='sqrt',
            random_state=self.random_state,
            n_jobs=-1
        )
        
        self.models['xgboost'] = xgb.XGBRegressor(
            n_estimators=self.n_estimators,
            max_depth=8,
            learning_rate=0.05,
            subsample=0.8,
            colsample_bytree=0.8,
            reg_alpha=0.1,
            reg_lambda=1.0,
            random_state=self.random_state,
            n_jobs=-1,
            verbosity=0
        )
        
        self.models['elasticnet'] = ElasticNet(
            alpha=0.1,
            l1_ratio=0.5,
            max_iter=10000,
            random_state=self.random_state
        )
        
        self.model_weights = {
            'random_forest': 0.35,
            'xgboost': 0.45,
            'elasticnet': 0.20
        }
    
    def fit(self, X: pd.DataFrame, y: np.ndarray, 
            cv_folds: int = 5) -> Dict[str, ModelMetrics]:
        """
        Fit all ensemble models and calculate performance metrics.
        
        Args:
            X: Feature matrix (CpG methylation values)
            y: Target vector (chronological ages)
            cv_folds: Number of cross-validation folds
        
        Returns:
            Dictionary of model performance metrics
        """
        self.feature_names = list(X.columns) if hasattr(X, 'columns') else [f'feature_{i}' for i in range(X.shape[1])]
        
        X_scaled = self.scaler.fit_transform(X)
        
        metrics = {}
        cv_scores = {}
        
        kfold = KFold(n_splits=cv_folds, shuffle=True, random_state=self.random_state)
        
        for model_name, model in self.models.items():
            model.fit(X_scaled, y)
            
            y_pred = model.predict(X_scaled)
            
            mae = mean_absolute_error(y, y_pred)
            rmse = np.sqrt(mean_squared_error(y, y_pred))
            r2 = r2_score(y, y_pred)
            
            cv_mae = -cross_val_score(model, X_scaled, y, 
                                       scoring='neg_mean_absolute_error', 
                                       cv=kfold)
            cv_r2 = cross_val_score(model, X_scaled, y, 
                                     scoring='r2', 
                                     cv=kfold)
            
            if model_name in ['random_forest', 'xgboost']:
                importance = model.feature_importances_
                top_indices = np.argsort(importance)[-20:][::-1]
                feature_importance = {
                    self.feature_names[i]: float(importance[i]) 
                    for i in top_indices
                }
            else:
                coef = np.abs(model.coef_)
                top_indices = np.argsort(coef)[-20:][::-1]
                feature_importance = {
                    self.feature_names[i]: float(coef[i]) 
                    for i in top_indices
                }
            
            metrics[model_name] = ModelMetrics(
                model_name=model_name,
                mae=round(mae, 3),
                rmse=round(rmse, 3),
                r_squared=round(r2, 4),
                cv_mae_mean=round(np.mean(cv_mae), 3),
                cv_mae_std=round(np.std(cv_mae), 3),
                cv_r2_mean=round(np.mean(cv_r2), 4),
                cv_r2_std=round(np.std(cv_r2), 4),
                feature_importance=feature_importance
            )
            
            cv_scores[model_name] = 1 / (np.mean(cv_mae) + 1)
        
        total_score = sum(cv_scores.values())
        self.model_weights = {
            name: score / total_score 
            for name, score in cv_scores.items()
        }
        
        self.is_fitted = True
        
        return metrics
    
    def predict(self, X: pd.DataFrame) -> EnsemblePrediction:
        """
        Make ensemble prediction for a single sample or batch.
        
        Args:
            X: Feature matrix
        
        Returns:
            EnsemblePrediction with weighted average and uncertainty
        """
        if not self.is_fitted:
            raise RuntimeError("Models must be fitted before prediction")
        
        X_scaled = self.scaler.transform(X)
        
        predictions = {}
        for model_name, model in self.models.items():
            pred = model.predict(X_scaled)
            predictions[model_name] = float(np.mean(pred))
        
        weighted_prediction = sum(
            predictions[name] * self.model_weights[name]
            for name in self.models.keys()
        )
        
        pred_values = list(predictions.values())
        uncertainty = np.std(pred_values)
        
        ci_width = 1.96 * uncertainty
        confidence_interval = (
            weighted_prediction - ci_width,
            weighted_prediction + ci_width
        )
        
        return EnsemblePrediction(
            predicted_age=round(weighted_prediction, 2),
            confidence_interval=(round(confidence_interval[0], 2), 
                                round(confidence_interval[1], 2)),
            model_predictions=predictions,
            model_weights=self.model_weights,
            uncertainty=round(uncertainty, 3)
        )
    
    def predict_batch(self, X: pd.DataFrame) -> List[EnsemblePrediction]:
        """Make predictions for multiple samples"""
        if not self.is_fitted:
            raise RuntimeError("Models must be fitted before prediction")
        
        X_scaled = self.scaler.transform(X)
        
        all_predictions = {}
        for model_name, model in self.models.items():
            all_predictions[model_name] = model.predict(X_scaled)
        
        results = []
        for i in range(len(X)):
            predictions = {
                name: float(preds[i]) 
                for name, preds in all_predictions.items()
            }
            
            weighted_prediction = sum(
                predictions[name] * self.model_weights[name]
                for name in self.models.keys()
            )
            
            pred_values = list(predictions.values())
            uncertainty = np.std(pred_values)
            
            ci_width = 1.96 * uncertainty
            confidence_interval = (
                weighted_prediction - ci_width,
                weighted_prediction + ci_width
            )
            
            results.append(EnsemblePrediction(
                predicted_age=round(weighted_prediction, 2),
                confidence_interval=(round(confidence_interval[0], 2),
                                    round(confidence_interval[1], 2)),
                model_predictions=predictions,
                model_weights=self.model_weights,
                uncertainty=round(uncertainty, 3)
            ))
        
        return results
    
    def get_feature_importance_aggregate(self) -> pd.DataFrame:
        """Get aggregated feature importance from all models"""
        if not self.is_fitted:
            raise RuntimeError("Models must be fitted first")
        
        all_importance = {}
        
        rf_importance = self.models['random_forest'].feature_importances_
        xgb_importance = self.models['xgboost'].feature_importances_
        en_importance = np.abs(self.models['elasticnet'].coef_)
        
        rf_importance = rf_importance / rf_importance.sum()
        xgb_importance = xgb_importance / xgb_importance.sum()
        en_importance = en_importance / (en_importance.sum() + 1e-10)
        
        for i, feature_name in enumerate(self.feature_names):
            all_importance[feature_name] = (
                rf_importance[i] * self.model_weights['random_forest'] +
                xgb_importance[i] * self.model_weights['xgboost'] +
                en_importance[i] * self.model_weights['elasticnet']
            )
        
        importance_df = pd.DataFrame({
            'feature': list(all_importance.keys()),
            'importance': list(all_importance.values())
        })
        importance_df = importance_df.sort_values('importance', ascending=False)
        
        return importance_df


class SubstanceClassifier:
    """
    Classifier to predict substance use type based on epigenetic patterns
    """
    
    SUBSTANCE_TYPES = ['control', 'alcohol', 'cocaine', 'opioids', 
                       'methamphetamine', 'cannabis', 'polysubstance']
    
    def __init__(self, random_state: int = 42):
        self.random_state = random_state
        self.model = None
        self.scaler = StandardScaler()
        self.is_fitted = False
    
    def fit(self, X: pd.DataFrame, y: np.ndarray):
        """Fit the classifier on labeled data"""
        from sklearn.ensemble import GradientBoostingClassifier
        
        X_scaled = self.scaler.fit_transform(X)
        
        self.model = GradientBoostingClassifier(
            n_estimators=100,
            max_depth=5,
            learning_rate=0.1,
            random_state=self.random_state
        )
        self.model.fit(X_scaled, y)
        self.is_fitted = True
    
    def predict_proba(self, X: pd.DataFrame) -> pd.DataFrame:
        """Get probability predictions for each substance type"""
        if not self.is_fitted:
            raise RuntimeError("Model must be fitted first")
        
        X_scaled = self.scaler.transform(X)
        probas = self.model.predict_proba(X_scaled)
        
        return pd.DataFrame(probas, columns=self.model.classes_)
    
    def predict(self, X: pd.DataFrame) -> np.ndarray:
        """Predict substance type"""
        if not self.is_fitted:
            raise RuntimeError("Model must be fitted first")
        
        X_scaled = self.scaler.transform(X)
        return self.model.predict(X_scaled)


def generate_synthetic_training_data(n_samples: int = 1000, 
                                      n_cpgs: int = 500,
                                      random_state: int = 42) -> Tuple[pd.DataFrame, np.ndarray]:
    """
    Generate synthetic DNA methylation data for model training/testing
    
    Args:
        n_samples: Number of samples to generate
        n_cpgs: Number of CpG features
        random_state: Random seed
    
    Returns:
        Tuple of (feature matrix, age labels)
    """
    np.random.seed(random_state)
    
    ages = np.random.uniform(18, 85, n_samples)
    
    cpg_names = [f"cg{str(i).zfill(8)}" for i in range(n_cpgs)]
    
    n_age_correlated = int(n_cpgs * 0.3)
    n_random = n_cpgs - n_age_correlated
    
    methylation_data = np.zeros((n_samples, n_cpgs))
    
    for i in range(n_age_correlated):
        direction = np.random.choice([-1, 1])
        slope = np.random.uniform(0.001, 0.008) * direction
        intercept = np.random.uniform(0.2, 0.8)
        noise = np.random.normal(0, 0.05, n_samples)
        
        values = intercept + slope * ages + noise
        methylation_data[:, i] = np.clip(values, 0, 1)
    
    for i in range(n_age_correlated, n_cpgs):
        alpha = np.random.uniform(1, 5)
        beta = np.random.uniform(1, 5)
        methylation_data[:, i] = np.random.beta(alpha, beta, n_samples)
    
    df = pd.DataFrame(methylation_data, columns=cpg_names)
    
    return df, ages
