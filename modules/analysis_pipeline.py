# ============================================================================
# EpiClock v4.0 - Complete DNA Methylation Analysis Pipeline
# Integrates: Data Loading, Preprocessing, ML, Deep Learning, Explainability
# Author: nrcdnl94
# ============================================================================
"""
Complete Analysis Pipeline for DNA Methylation Data

Integrates all EpiClock modules:
1. RealDataLoader - File upload and validation
2. MethylationPreprocessor - QC, normalization, batch correction
3. EpigeneticClockCalculator - Hannum, DunedinPACE clocks
4. EnsembleAgePredictor - ML ensemble (RF, XGB, ElasticNet)
5. DeepLearningTrainer - MLP, Autoencoder, MTL-NN
6. ModelAgnosticExplainer - SHAP feature importance
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Optional, Tuple, Any, Union
from dataclasses import dataclass, field
from datetime import datetime
import warnings

from modules.real_data_loader import RealDataLoader, LoadedMethylationData
from modules.methylation_preprocessing import (
    MethylationPreprocessor, PreprocessingResult, 
    BetaMValueConverter, QualityControl
)

try:
    from modules.epigenetic_clocks import EpigeneticClockCalculator
    CLOCKS_AVAILABLE = True
except ImportError:
    CLOCKS_AVAILABLE = False
    warnings.warn("Epigenetic clocks module not available")

try:
    from modules.ml_models import EnsembleAgePredictor
    ML_AVAILABLE = True
except ImportError:
    ML_AVAILABLE = False
    warnings.warn("ML models module not available")

try:
    from modules.deep_learning_methylation import (
        DeepLearningTrainer, MethylationMLP, 
        MethylationAutoencoder, MultiTaskMethylationNetwork,
        TORCH_AVAILABLE
    )
    DL_AVAILABLE = TORCH_AVAILABLE
except ImportError:
    DL_AVAILABLE = False
    warnings.warn("Deep learning module not available")

try:
    from modules.model_explainability import (
        ModelAgnosticExplainer, TreeSHAPExplainer, 
        EpigeneticExplainer, ExplanationResult
    )
    SHAP_AVAILABLE = True
except ImportError:
    SHAP_AVAILABLE = False
    warnings.warn("Explainability module not available")


@dataclass
class AnalysisResult:
    """Complete analysis result from pipeline"""
    sample_id: str
    chronological_age: Optional[float]
    
    biological_age_hannum: Optional[float] = None
    biological_age_dunedinpace: Optional[float] = None
    biological_age_ensemble: Optional[float] = None
    biological_age_deep_learning: Optional[float] = None
    
    age_acceleration_hannum: Optional[float] = None
    age_acceleration_dunedinpace: Optional[float] = None
    age_acceleration_ensemble: Optional[float] = None
    
    confidence_interval: Optional[Tuple[float, float]] = None
    uncertainty: Optional[float] = None
    
    substance_probabilities: Optional[Dict[str, float]] = None
    risk_score: Optional[float] = None
    
    top_cpg_contributors: Optional[List[Tuple[str, float]]] = None
    clinical_interpretation: Optional[str] = None
    
    preprocessing_applied: bool = False
    models_used: List[str] = field(default_factory=list)
    timestamp: str = ""


@dataclass
class BatchAnalysisResult:
    """Results for batch analysis of multiple samples"""
    n_samples: int
    n_cpgs_analyzed: int
    individual_results: List[AnalysisResult]
    summary_statistics: Dict[str, float]
    clock_coverage: Dict[str, float]
    preprocessing_summary: Optional[Dict[str, Any]] = None
    feature_importance: Optional[Dict[str, float]] = None
    timestamp: str = ""


class DNAMethylationAnalysisPipeline:
    """
    Complete DNA Methylation Analysis Pipeline
    
    Workflow:
    1. Load data (CSV/Excel/Parquet)
    2. Validate and preprocess
    3. Calculate epigenetic clock ages
    4. Run ML/DL predictions
    5. Generate explanations
    6. Create clinical reports
    """
    
    SUBSTANCE_CLASSES = [
        'Control', 'Alcohol', 'Cocaine', 'Methamphetamine',
        'Opioids', 'Cannabis', 'Polysubstance'
    ]
    
    def __init__(self, use_preprocessing: bool = True,
                 use_deep_learning: bool = True,
                 use_explainability: bool = True):
        """
        Initialize analysis pipeline
        
        Args:
            use_preprocessing: Apply QC and normalization
            use_deep_learning: Use deep learning models
            use_explainability: Generate SHAP explanations
        """
        self.use_preprocessing = use_preprocessing
        self.use_deep_learning = use_deep_learning and DL_AVAILABLE
        self.use_explainability = use_explainability and SHAP_AVAILABLE
        
        self.data_loader = RealDataLoader()
        self.preprocessor = MethylationPreprocessor()
        
        if CLOCKS_AVAILABLE:
            self.clock_calculator = EpigeneticClockCalculator()
        else:
            self.clock_calculator = None
        
        if ML_AVAILABLE:
            self.ml_predictor = EnsembleAgePredictor()
        else:
            self.ml_predictor = None
        
        self.dl_trainer = None
        self.explainer = None
        
        self.loaded_data = None
        self.preprocessed_data = None
        self.is_fitted = False
    
    def load_data(self, file_input: Union[str, Any],
                  file_type: Optional[str] = None) -> LoadedMethylationData:
        """
        Load methylation data from file
        
        Args:
            file_input: File path or uploaded file object
            file_type: Optional file type hint
        
        Returns:
            LoadedMethylationData with validation info
        """
        self.loaded_data = self.data_loader.load_file(file_input, file_type)
        return self.loaded_data
    
    def preprocess(self, batch_labels: Optional[np.ndarray] = None,
                   adjust_cells: bool = True) -> PreprocessingResult:
        """
        Apply preprocessing pipeline
        
        Args:
            batch_labels: Optional batch labels for ComBat
            adjust_cells: Whether to adjust for cell composition
        
        Returns:
            PreprocessingResult with cleaned data
        """
        if self.loaded_data is None:
            raise ValueError("No data loaded. Call load_data() first.")
        
        self.preprocessed_data = self.preprocessor.preprocess(
            self.loaded_data.data,
            batch=batch_labels,
            adjust_cell_composition=adjust_cells
        )
        
        return self.preprocessed_data
    
    def fit_models(self, ages: np.ndarray,
                   substance_labels: Optional[np.ndarray] = None,
                   fit_deep_learning: bool = True) -> Dict[str, Any]:
        """
        Fit ML and DL models on training data
        
        Args:
            ages: Chronological ages for training
            substance_labels: Optional substance use labels
            fit_deep_learning: Whether to train deep learning models
        
        Returns:
            Training metrics for all models
        """
        if self.preprocessed_data is not None:
            X = self.preprocessed_data.data
        elif self.loaded_data is not None:
            X = self.loaded_data.data
        else:
            raise ValueError("No data available. Load and preprocess first.")
        
        metrics = {}
        
        if self.ml_predictor is not None:
            ml_metrics = self.ml_predictor.fit(X, ages)
            metrics['ensemble'] = ml_metrics
            self.is_fitted = True
        
        if fit_deep_learning and self.use_deep_learning:
            self.dl_trainer = DeepLearningTrainer(model_type='mlp')
            self.dl_trainer.create_model(X.shape[1], hidden_dims=[256, 128, 64])
            dl_metrics = self.dl_trainer.train_mlp(X.values, ages, epochs=50)
            metrics['deep_learning'] = dl_metrics
        
        if self.use_explainability and self.ml_predictor is not None:
            self.explainer = EpigeneticExplainer(
                self.ml_predictor.models['random_forest']
            )
            self.explainer.fit(X)
        
        return metrics
    
    def analyze_sample(self, sample_data: pd.DataFrame,
                       chronological_age: Optional[float] = None,
                       sample_id: Optional[str] = None) -> AnalysisResult:
        """
        Analyze a single sample
        
        Args:
            sample_data: Single row of methylation data
            chronological_age: Known age for EAA calculation
            sample_id: Sample identifier
        
        Returns:
            AnalysisResult with all predictions
        """
        if sample_id is None:
            sample_id = str(sample_data.index[0]) if hasattr(sample_data, 'index') else "Unknown"
        
        result = AnalysisResult(
            sample_id=sample_id,
            chronological_age=chronological_age,
            timestamp=datetime.now().isoformat()
        )
        
        if self.clock_calculator is not None:
            try:
                clock_results = self.clock_calculator.calculate_all_clocks(sample_data)
                
                if 'hannum' in clock_results:
                    result.biological_age_hannum = clock_results['hannum'].predicted_age
                    result.models_used.append('Hannum')
                    if chronological_age:
                        result.age_acceleration_hannum = (
                            result.biological_age_hannum - chronological_age
                        )
                
                if 'dunedinpace' in clock_results:
                    pace = clock_results['dunedinpace'].pace_of_aging
                    result.biological_age_dunedinpace = chronological_age * pace if chronological_age else pace
                    result.models_used.append('DunedinPACE')
            except Exception as e:
                warnings.warn(f"Clock calculation failed: {e}")
        
        if self.ml_predictor is not None and self.is_fitted:
            try:
                prediction = self.ml_predictor.predict(sample_data)
                result.biological_age_ensemble = prediction.predicted_age
                result.confidence_interval = prediction.confidence_interval
                result.uncertainty = prediction.uncertainty
                result.models_used.append('ML_Ensemble')
                
                if chronological_age:
                    result.age_acceleration_ensemble = (
                        prediction.predicted_age - chronological_age
                    )
            except Exception as e:
                warnings.warn(f"ML prediction failed: {e}")
        
        if self.dl_trainer is not None and self.dl_trainer.model is not None:
            try:
                dl_prediction = self.dl_trainer.predict(sample_data.values)
                result.biological_age_deep_learning = float(dl_prediction.mean())
                result.models_used.append('Deep_Learning')
            except Exception as e:
                warnings.warn(f"Deep learning prediction failed: {e}")
        
        if self.explainer is not None:
            try:
                explanation = self.explainer.explain_age_prediction(
                    sample_data, chronological_age or 50
                )
                result.top_cpg_contributors = explanation.get('aging_cpgs', [])[:10]
                result.clinical_interpretation = explanation.get('interpretation', '')
            except Exception as e:
                warnings.warn(f"Explanation generation failed: {e}")
        
        result.preprocessing_applied = self.preprocessed_data is not None
        
        return result
    
    def analyze_batch(self, ages: Optional[np.ndarray] = None,
                      sample_ids: Optional[List[str]] = None) -> BatchAnalysisResult:
        """
        Analyze all loaded samples
        
        Args:
            ages: Optional chronological ages for each sample
            sample_ids: Optional sample identifiers
        
        Returns:
            BatchAnalysisResult with all sample analyses
        """
        if self.preprocessed_data is not None:
            data = self.preprocessed_data.data
        elif self.loaded_data is not None:
            data = self.loaded_data.data
        else:
            raise ValueError("No data available. Load data first.")
        
        n_samples = len(data)
        
        if sample_ids is None:
            sample_ids = list(data.index)
        
        if ages is None:
            ages = [None] * n_samples
        
        results = []
        for i in range(n_samples):
            sample_data = data.iloc[[i]]
            age = ages[i] if i < len(ages) else None
            sample_id = sample_ids[i] if i < len(sample_ids) else f"Sample_{i}"
            
            result = self.analyze_sample(sample_data, age, sample_id)
            results.append(result)
        
        summary = self._calculate_summary_statistics(results)
        
        clock_coverage = self.loaded_data.metadata.get('clock_coverage', {}) if self.loaded_data else {}
        
        feature_importance = None
        if self.ml_predictor is not None and self.is_fitted:
            try:
                importance_df = self.ml_predictor.get_feature_importance_aggregate()
                feature_importance = dict(zip(
                    importance_df['feature'].head(50),
                    importance_df['importance'].head(50)
                ))
            except:
                pass
        
        return BatchAnalysisResult(
            n_samples=n_samples,
            n_cpgs_analyzed=data.shape[1],
            individual_results=results,
            summary_statistics=summary,
            clock_coverage=clock_coverage,
            preprocessing_summary=self.preprocessed_data.summary_stats if self.preprocessed_data else None,
            feature_importance=feature_importance,
            timestamp=datetime.now().isoformat()
        )
    
    def _calculate_summary_statistics(self, results: List[AnalysisResult]) -> Dict[str, float]:
        """Calculate summary statistics from batch results"""
        summary = {}
        
        hannum_ages = [r.biological_age_hannum for r in results if r.biological_age_hannum is not None]
        if hannum_ages:
            summary['mean_bio_age_hannum'] = np.mean(hannum_ages)
            summary['std_bio_age_hannum'] = np.std(hannum_ages)
        
        ensemble_ages = [r.biological_age_ensemble for r in results if r.biological_age_ensemble is not None]
        if ensemble_ages:
            summary['mean_bio_age_ensemble'] = np.mean(ensemble_ages)
            summary['std_bio_age_ensemble'] = np.std(ensemble_ages)
        
        eaa_values = [r.age_acceleration_hannum for r in results if r.age_acceleration_hannum is not None]
        if eaa_values:
            summary['mean_eaa'] = np.mean(eaa_values)
            summary['std_eaa'] = np.std(eaa_values)
            summary['accelerated_samples'] = sum(1 for e in eaa_values if e > 2)
            summary['decelerated_samples'] = sum(1 for e in eaa_values if e < -2)
        
        return summary
    
    def generate_clinical_report(self, result: AnalysisResult) -> Dict[str, Any]:
        """
        Generate clinical report for a sample
        
        Args:
            result: AnalysisResult from analyze_sample
        
        Returns:
            Structured clinical report
        """
        report = {
            'header': {
                'sample_id': result.sample_id,
                'analysis_date': result.timestamp,
                'report_type': 'Epigenetic Age Analysis'
            },
            'summary': {
                'chronological_age': result.chronological_age,
                'biological_age': result.biological_age_ensemble or result.biological_age_hannum,
                'age_acceleration': result.age_acceleration_ensemble or result.age_acceleration_hannum,
                'models_used': result.models_used
            },
            'interpretation': {
                'clinical_significance': result.clinical_interpretation,
                'risk_category': self._determine_risk_category(result),
                'recommendations': self._generate_recommendations(result)
            },
            'details': {
                'hannum_age': result.biological_age_hannum,
                'dunedinpace_age': result.biological_age_dunedinpace,
                'ensemble_age': result.biological_age_ensemble,
                'deep_learning_age': result.biological_age_deep_learning,
                'confidence_interval': result.confidence_interval,
                'uncertainty': result.uncertainty
            },
            'biomarkers': {
                'top_contributors': result.top_cpg_contributors
            }
        }
        
        return report
    
    def _determine_risk_category(self, result: AnalysisResult) -> str:
        """Determine risk category based on age acceleration"""
        eaa = result.age_acceleration_ensemble or result.age_acceleration_hannum
        
        if eaa is None:
            return "Unknown"
        elif eaa > 10:
            return "High Risk - Severe Acceleration"
        elif eaa > 5:
            return "Moderate Risk - Significant Acceleration"
        elif eaa > 2:
            return "Low-Moderate Risk - Mild Acceleration"
        elif eaa > -2:
            return "Normal - Within Expected Range"
        elif eaa > -5:
            return "Favorable - Mild Deceleration"
        else:
            return "Exceptional - Significant Deceleration"
    
    def _generate_recommendations(self, result: AnalysisResult) -> List[str]:
        """Generate clinical recommendations"""
        recommendations = []
        
        eaa = result.age_acceleration_ensemble or result.age_acceleration_hannum
        
        if eaa is not None:
            if eaa > 5:
                recommendations.append("Comprehensive health evaluation recommended")
                recommendations.append("Consider lifestyle intervention program")
                recommendations.append("Follow-up methylation analysis in 6 months")
            elif eaa > 2:
                recommendations.append("Monitor biological age markers regularly")
                recommendations.append("Lifestyle optimization may reduce acceleration")
            else:
                recommendations.append("Continue current health maintenance")
        
        recommendations.append("Annual methylation monitoring recommended")
        
        return recommendations


def test_analysis_pipeline():
    """Test the complete analysis pipeline"""
    print("Testing DNA Methylation Analysis Pipeline")
    print("=" * 60)
    
    n_samples = 30
    n_cpgs = 200
    
    cpg_names = [f"cg{i:08d}" for i in range(n_cpgs)]
    sample_names = [f"Sample_{i}" for i in range(n_samples)]
    
    np.random.seed(42)
    beta_values = np.random.beta(2.5, 4, (n_samples, n_cpgs))
    ages = np.random.uniform(25, 75, n_samples)
    
    df = pd.DataFrame(beta_values, index=sample_names, columns=cpg_names)
    csv_path = "/tmp/test_pipeline_data.csv"
    df.to_csv(csv_path)
    
    print("\n1. Initializing pipeline...")
    pipeline = DNAMethylationAnalysisPipeline(
        use_preprocessing=True,
        use_deep_learning=False,
        use_explainability=True
    )
    
    print("\n2. Loading data...")
    loaded = pipeline.load_data(csv_path)
    print(f"   Loaded: {loaded.n_samples} samples x {loaded.n_cpgs} CpGs")
    print(f"   Valid: {loaded.is_valid}")
    
    print("\n3. Preprocessing...")
    preprocessed = pipeline.preprocess()
    print(f"   QC passed: {preprocessed.qc_passed}")
    print(f"   Final shape: {preprocessed.n_samples} x {preprocessed.n_cpgs}")
    
    print("\n4. Fitting models...")
    metrics = pipeline.fit_models(ages, fit_deep_learning=False)
    print(f"   Models trained: {list(metrics.keys())}")
    
    print("\n5. Analyzing samples...")
    batch_result = pipeline.analyze_batch(ages, sample_names)
    print(f"   Samples analyzed: {batch_result.n_samples}")
    print(f"   Summary: {batch_result.summary_statistics}")
    
    print("\n6. Generating clinical report...")
    if batch_result.individual_results:
        report = pipeline.generate_clinical_report(batch_result.individual_results[0])
        print(f"   Report sections: {list(report.keys())}")
        print(f"   Risk category: {report['interpretation']['risk_category']}")
    
    print("\n" + "=" * 60)
    print("Analysis pipeline tested successfully!")
    
    return batch_result


if __name__ == "__main__":
    test_analysis_pipeline()
