"""
EpiClock Prototype - DNA Methylation Age Analysis Platform
Epigenetik Yaş İvmelenmesi Tespit Sistemi
"""

from .epigenetic_clocks import EpigeneticClockCalculator
from .ml_models import EnsembleAgePredictor
from .data_processing import MethylationDataProcessor
from .statistics import StatisticalAnalyzer
from .visualization import EpigeneticVisualizer
from .report_generator import ReportGenerator
from .reference_database import ReferenceDatabase

__version__ = "1.0.0"
__author__ = "EpiClock Research Team"

__all__ = [
    'EpigeneticClockCalculator',
    'EnsembleAgePredictor',
    'MethylationDataProcessor',
    'StatisticalAnalyzer',
    'EpigeneticVisualizer',
    'ReportGenerator',
    'ReferenceDatabase'
]
