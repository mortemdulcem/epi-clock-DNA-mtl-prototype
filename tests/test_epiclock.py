"""
EpiClock v4.0 Test Suite
========================

pytest ile unit ve integration testleri

Calistirma:
    pytest tests/test_epiclock.py -v
    pytest tests/test_epiclock.py -v --cov=modules --cov-report=html

Coverage hedefi: %80+
"""

import pytest
import numpy as np
import pandas as pd
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# ============================================================================
# FIXTURES
# ============================================================================

@pytest.fixture
def sample_methylation_data():
    """Ornek metilasyon verisi"""
    np.random.seed(42)
    n_samples = 50
    n_cpgs = 100
    
    cpg_names = [f"cg{str(i).zfill(8)}" for i in range(n_cpgs)]
    sample_names = [f"sample_{i}" for i in range(n_samples)]
    
    beta_values = np.random.beta(5, 5, (n_cpgs, n_samples))
    
    return pd.DataFrame(beta_values, index=cpg_names, columns=sample_names)


@pytest.fixture
def sample_phenotype_data():
    """Ornek fenotip verisi"""
    np.random.seed(42)
    n_samples = 50
    
    return pd.DataFrame({
        'sample_id': [f"sample_{i}" for i in range(n_samples)],
        'age': np.random.uniform(20, 80, n_samples),
        'sex': np.random.choice(['M', 'F'], n_samples),
        'bmi': np.random.normal(25, 5, n_samples)
    })


@pytest.fixture
def sample_regression_data():
    """Ornek regresyon verisi"""
    np.random.seed(42)
    n = 100
    
    y_true = np.random.uniform(20, 80, n)
    y_pred = y_true + np.random.normal(0, 3, n)
    
    return y_true, y_pred


@pytest.fixture
def sample_classification_data():
    """Ornek siniflandirma verisi"""
    np.random.seed(42)
    n = 100
    
    y_true = np.random.choice([0, 1], n)
    y_scores = y_true * 0.7 + np.random.uniform(0, 0.3, n)
    
    return y_true, y_scores


# ============================================================================
# STATISTICAL VALIDATION TESTS
# ============================================================================

class TestMultipleTestingCorrection:
    """Coklu test duzeltmesi testleri"""
    
    def test_bonferroni_basic(self):
        """Bonferroni temel testi"""
        from modules.statistical_validation import MultipleTestingCorrection
        
        p_values = np.array([0.01, 0.04, 0.03, 0.001])
        result = MultipleTestingCorrection.bonferroni(p_values, alpha=0.05)
        
        assert result['method'] == 'Bonferroni'
        assert result['n_tests'] == 4
        assert result['alpha_adjusted'] == 0.05 / 4
        assert isinstance(result['n_significant'], int)
    
    def test_benjamini_hochberg_fdr(self):
        """FDR duzeltmesi testi"""
        from modules.statistical_validation import MultipleTestingCorrection
        
        np.random.seed(42)
        p_values = np.random.uniform(0, 1, 100)
        p_values[:5] = np.random.uniform(0, 0.001, 5)
        
        result = MultipleTestingCorrection.benjamini_hochberg(p_values, alpha=0.05)
        
        assert result['method'] == 'Benjamini-Hochberg (FDR)'
        assert result['n_tests'] == 100
        assert result['n_significant'] >= 0
        assert len(result['q_values']) == 100
        assert all(result['q_values'] <= 1.0)
    
    def test_holm_bonferroni(self):
        """Holm-Bonferroni testi"""
        from modules.statistical_validation import MultipleTestingCorrection
        
        p_values = np.array([0.001, 0.01, 0.05, 0.1])
        result = MultipleTestingCorrection.holm(p_values, alpha=0.05)
        
        assert result['method'] == 'Holm-Bonferroni'
        assert len(result['adjusted_p']) == 4
        assert all(result['adjusted_p'] <= 1.0)


class TestBootstrapCI:
    """Bootstrap guven araligi testleri"""
    
    def test_percentile_bootstrap(self):
        """Percentile bootstrap testi"""
        from modules.statistical_validation import BootstrapCI
        
        np.random.seed(42)
        data = np.random.normal(50, 10, 100)
        
        result = BootstrapCI.percentile(data, np.mean, n_bootstrap=1000)
        
        assert result['method'] == 'Percentile Bootstrap'
        assert result['ci_lower'] < result['point_estimate'] < result['ci_upper']
        assert 40 < result['point_estimate'] < 60
    
    def test_bca_bootstrap(self):
        """BCa bootstrap testi"""
        from modules.statistical_validation import BootstrapCI
        
        np.random.seed(42)
        data = np.random.normal(50, 10, 50)
        
        result = BootstrapCI.bca(data, np.mean, n_bootstrap=500)
        
        assert result['method'] == 'BCa Bootstrap'
        assert 'bias_correction' in result
        assert 'acceleration' in result


class TestClassificationMetrics:
    """Siniflandirma metrikleri testleri"""
    
    def test_roc_auc(self, sample_classification_data):
        """ROC-AUC testi"""
        from modules.statistical_validation import ClassificationMetrics
        
        y_true, y_scores = sample_classification_data
        auc = ClassificationMetrics.roc_auc(y_true, y_scores)
        
        assert 0.0 <= auc <= 1.0
        assert auc > 0.5  # Better than random
    
    def test_pr_auc(self, sample_classification_data):
        """PR-AUC testi"""
        from modules.statistical_validation import ClassificationMetrics
        
        y_true, y_scores = sample_classification_data
        auc = ClassificationMetrics.pr_auc(y_true, y_scores)
        
        assert 0.0 <= auc <= 1.0
    
    def test_confusion_matrix(self, sample_classification_data):
        """Confusion matrix testi"""
        from modules.statistical_validation import ClassificationMetrics
        
        y_true, y_scores = sample_classification_data
        cm = ClassificationMetrics.confusion_matrix(y_true, y_scores, threshold=0.5)
        
        assert 'tp' in cm
        assert 'tn' in cm
        assert 'fp' in cm
        assert 'fn' in cm
        assert cm['tp'] + cm['tn'] + cm['fp'] + cm['fn'] == len(y_true)


class TestEffectSize:
    """Effect size testleri"""
    
    def test_cohens_d(self):
        """Cohen's d testi"""
        from modules.statistical_validation import EffectSize
        
        np.random.seed(42)
        group1 = np.random.normal(50, 10, 50)
        group2 = np.random.normal(55, 10, 50)
        
        result = EffectSize.cohens_d(group1, group2)
        
        assert 'effect_size' in result
        assert 'interpretation' in result
        assert result['interpretation'] in ['negligible', 'small', 'medium', 'large']
    
    def test_hedges_g(self):
        """Hedge's g testi"""
        from modules.statistical_validation import EffectSize
        
        np.random.seed(42)
        group1 = np.random.normal(50, 10, 20)
        group2 = np.random.normal(55, 10, 20)
        
        result = EffectSize.hedges_g(group1, group2)
        
        assert result['method'] == "Hedge's g"
        assert 'correction_factor' in result


class TestRegressionMetrics:
    """Regresyon metrikleri testleri"""
    
    def test_calculate_all(self, sample_regression_data):
        """Tum regresyon metrikleri testi"""
        from modules.statistical_validation import RegressionMetrics
        
        y_true, y_pred = sample_regression_data
        metrics = RegressionMetrics.calculate_all(y_true, y_pred)
        
        assert 'mae' in metrics
        assert 'rmse' in metrics
        assert 'r_squared' in metrics
        assert 'correlation' in metrics
        
        assert metrics['mae'] >= 0
        assert metrics['rmse'] >= 0
        assert 0 <= metrics['r_squared'] <= 1
        assert -1 <= metrics['correlation'] <= 1


class TestPowerAnalysis:
    """Power analizi testleri"""
    
    def test_two_sample_ttest_power(self):
        """t-test power analizi testi"""
        from modules.statistical_validation import PowerAnalysis
        
        result = PowerAnalysis.two_sample_ttest(effect_size=0.5, power=0.80)
        
        assert result['n_per_group'] > 0
        assert result['n_total'] == result['n_group1'] + result['n_group2']
    
    def test_ewas_sample_size(self):
        """EWAS orneklem buyuklugu testi"""
        from modules.statistical_validation import PowerAnalysis
        
        result = PowerAnalysis.ewas_sample_size(n_cpgs=450000)
        
        assert result['n_recommended'] > 0
        assert result['alpha_adjusted'] < result['alpha_original']


# ============================================================================
# REPRODUCIBILITY TESTS
# ============================================================================

class TestSeedManager:
    """Seed yonetimi testleri"""
    
    def test_set_global_seed(self):
        """Global seed testi"""
        from modules.reproducibility import SeedManager, set_reproducibility_seed
        
        set_reproducibility_seed(42)
        
        assert SeedManager.get_seed() == 42
        assert SeedManager.is_initialized()
    
    def test_deterministic_random(self):
        """Deterministik random testi"""
        from modules.reproducibility import set_reproducibility_seed
        
        set_reproducibility_seed(42)
        arr1 = np.random.rand(10)
        
        set_reproducibility_seed(42)
        arr2 = np.random.rand(10)
        
        np.testing.assert_array_equal(arr1, arr2)


class TestDataChecksum:
    """Veri checksum testleri"""
    
    def test_dataframe_hash_consistency(self, sample_methylation_data):
        """DataFrame hash tutarliligi testi"""
        from modules.reproducibility import DataChecksum
        
        hash1 = DataChecksum.compute_dataframe_hash(sample_methylation_data)
        hash2 = DataChecksum.compute_dataframe_hash(sample_methylation_data)
        
        assert hash1 == hash2
        assert len(hash1) == 64  # SHA256
    
    def test_array_hash_consistency(self):
        """Array hash tutarliligi testi"""
        from modules.reproducibility import DataChecksum
        
        arr = np.array([1, 2, 3, 4, 5])
        
        hash1 = DataChecksum.compute_array_hash(arr)
        hash2 = DataChecksum.compute_array_hash(arr)
        
        assert hash1 == hash2
    
    def test_verify_checksum(self):
        """Checksum dogrulama testi"""
        from modules.reproducibility import DataChecksum
        
        arr = np.array([1, 2, 3, 4, 5])
        expected_hash = DataChecksum.compute_array_hash(arr)
        
        assert DataChecksum.verify_checksum(arr, expected_hash)
        assert not DataChecksum.verify_checksum(arr, "wrong_hash")


class TestEnvironmentCapture:
    """Ortam yakalama testleri"""
    
    def test_capture_environment(self):
        """Ortam yakalama testi"""
        from modules.reproducibility import EnvironmentCapture
        
        env = EnvironmentCapture.capture()
        
        assert env.python_version is not None
        assert env.platform is not None
        assert isinstance(env.packages, dict)
        assert 'numpy' in env.packages


class TestReproduciblePipeline:
    """Reproducible pipeline testleri"""
    
    def test_pipeline_creation(self):
        """Pipeline olusturma testi"""
        from modules.reproducibility import ReproduciblePipeline
        
        pipeline = ReproduciblePipeline("test", seed=42)
        
        assert pipeline.name == "test"
        assert pipeline.seed == 42
    
    def test_pipeline_step(self):
        """Pipeline adim testi"""
        from modules.reproducibility import ReproduciblePipeline
        
        pipeline = ReproduciblePipeline("test", seed=42)
        
        def double(x):
            return x * 2
        
        data = np.array([1, 2, 3])
        result = pipeline.add_step("double", double, data)
        
        np.testing.assert_array_equal(result, np.array([2, 4, 6]))
        assert len(pipeline.steps) == 1
    
    def test_pipeline_manifest(self):
        """Pipeline manifest testi"""
        from modules.reproducibility import ReproduciblePipeline
        
        pipeline = ReproduciblePipeline("test", seed=42)
        
        manifest = pipeline.get_pipeline_manifest()
        
        assert manifest['name'] == 'test'
        assert manifest['seed'] == 42
        assert 'environment' in manifest
        assert 'steps' in manifest


# ============================================================================
# ACADEMIC REPORTING TESTS
# ============================================================================

class TestSTROBEMEChecklist:
    """STROBE-ME checklist testleri"""
    
    def test_checklist_initialization(self):
        """Checklist baslatma testi"""
        from modules.academic_reporting import STROBEMEChecklist
        
        checklist = STROBEMEChecklist()
        
        assert len(checklist.items) > 0
        assert '1a' in checklist.items
        assert 'M1' in checklist.items
    
    def test_mark_complete(self):
        """Madde tamamlama testi"""
        from modules.academic_reporting import STROBEMEChecklist
        
        checklist = STROBEMEChecklist()
        checklist.mark_complete('1a', 'p.1', 'Title complete')
        
        assert checklist.items['1a'].completed
        assert checklist.items['1a'].page_reference == 'p.1'
    
    def test_completion_status(self):
        """Tamamlanma durumu testi"""
        from modules.academic_reporting import STROBEMEChecklist
        
        checklist = STROBEMEChecklist()
        checklist.mark_complete('1a')
        checklist.mark_complete('2')
        
        status = checklist.get_completion_status()
        
        assert status['completed_items'] == 2
        assert status['completion_rate'] > 0


class TestSupplementaryMaterials:
    """Supplementary materials testleri"""
    
    def test_sample_characteristics_table(self, sample_phenotype_data):
        """Sample characteristics tablosu testi"""
        from modules.academic_reporting import SupplementaryMaterialsGenerator
        
        gen = SupplementaryMaterialsGenerator()
        table = gen.add_sample_characteristics_table(sample_phenotype_data)
        
        assert table.table_id == "Table S1"
        assert table.data is not None
    
    def test_extended_methods(self):
        """Extended methods testi"""
        from modules.academic_reporting import SupplementaryMaterialsGenerator
        
        gen = SupplementaryMaterialsGenerator()
        
        methods = gen.generate_extended_methods(
            preprocessing={'platform': 'EPIC'},
            statistical={'primary': 'Linear regression'},
            validation={'cv': '5-fold'}
        )
        
        assert 'EPIC' in methods
        assert 'Linear regression' in methods


# ============================================================================
# PRISMA-NMA TESTS
# ============================================================================

class TestPRISMANMA:
    """PRISMA-NMA testleri"""
    
    def test_analyzer_initialization(self):
        """Analyzer baslatma testi"""
        from modules.prisma_nma_standards import PRISMANMAAnalyzer
        
        analyzer = PRISMANMAAnalyzer()
        
        assert analyzer.pubmed is not None
        assert analyzer.nma is not None
        assert analyzer.checklist is not None
    
    def test_network_setup(self):
        """Network kurulum testi"""
        from modules.prisma_nma_standards import PRISMANMAAnalyzer
        
        analyzer = PRISMANMAAnalyzer()
        analyzer.setup_epigenetic_addiction_network()
        
        assert len(analyzer.nma.treatments) > 0
    
    def test_nma_analysis(self):
        """NMA analiz testi"""
        from modules.prisma_nma_standards import PRISMANMAAnalyzer
        
        analyzer = PRISMANMAAnalyzer()
        analyzer.setup_epigenetic_addiction_network()
        
        results = analyzer.analyze_network()
        
        assert 'nma_results' in results
        assert 'heterogeneity' in results
        assert 'rankings' in results


# ============================================================================
# INTEGRATION TESTS
# ============================================================================

class TestIntegration:
    """Entegrasyon testleri"""
    
    def test_full_validation_pipeline(self, sample_methylation_data, sample_phenotype_data):
        """Tam validasyon pipeline testi"""
        from modules.reproducibility import set_reproducibility_seed, ReproduciblePipeline
        from modules.statistical_validation import RegressionMetrics, MultipleTestingCorrection
        
        set_reproducibility_seed(42)
        
        pipeline = ReproduciblePipeline("validation_test", seed=42)
        
        ages = sample_phenotype_data['age'].values
        predicted = ages + np.random.normal(0, 2, len(ages))
        
        metrics = RegressionMetrics.calculate_all(ages, predicted)
        
        assert metrics['mae'] < 10
        assert metrics['correlation'] > 0.9
    
    def test_full_reporting_pipeline(self):
        """Tam raporlama pipeline testi"""
        from modules.academic_reporting import AcademicReportGenerator
        
        generator = AcademicReportGenerator()
        
        methods = generator.generate_methods_section(
            study_design={'type': 'cohort', 'n_samples': 100},
            preprocessing={'platform': 'EPIC'},
            statistical={'clocks': 'Hannum'}
        )
        
        results = generator.generate_results_section(
            sample_stats={'n_total': 100, 'mean_age': 50},
            main_findings={'mean_epi_age': 52, 'correlation': 0.95},
            validation={'external': True}
        )
        
        assert len(methods) > 100
        assert len(results) > 100


# ============================================================================
# RUN TESTS
# ============================================================================

if __name__ == "__main__":
    pytest.main([__file__, '-v', '--tb=short'])
