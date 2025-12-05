# ============================================================================
# EpiClock Prototype - DNA Methylation Epigenetic Age Analysis Platform
# Copyright (c) 2024 Dr. Nurcan Denli Bayır (nrcdnl94)
# GitHub: https://github.com/mortemdulcem/epi-clock-DNA-mtl-prototype
# All rights reserved. See LICENSE file for details.
# Author Signature: nrcdnl94
# ============================================================================
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
from .database import DatabaseManager, Patient, Analysis, ClinicalData, GSEAResult, TreatmentRecommendation

__version__ = "2.0.0"
__author__ = "EpiClock Research Team"

__all__ = [
    'EpigeneticClockCalculator',
    'EnsembleAgePredictor',
    'MethylationDataProcessor',
    'StatisticalAnalyzer',
    'EpigeneticVisualizer',
    'ReportGenerator',
    'ReferenceDatabase',
    'DatabaseManager',
    'Patient',
    'Analysis',
    'ClinicalData',
    'GSEAResult',
    'TreatmentRecommendation'
]


# End of module - # nrcdnl94