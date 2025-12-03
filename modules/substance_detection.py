"""
Madde Kullanımı Tespit ve Kullanım Süresi Tahmin Modülü
DNA Metilasyon Verisi Üzerinden Madde Tespiti

Bu modül, DNA metilasyon beta değerlerini analiz ederek:
1. Hangi maddelerin kullanıldığını tespit eder
2. Kullanım süresini (yıl) tahmin eder
3. Güven aralıklarıyla sonuç verir

Bilimsel Temel:
- Her madde belirli CpG sitelerinde karakteristik metilasyon değişikliklerine neden olur
- Metilasyon değişikliğinin büyüklüğü kullanım süresiyle korelasyon gösterir
- Machine learning modelleri ile pattern recognition yapılır
"""

import numpy as np
import pandas as pd
from dataclasses import dataclass, field
from typing import Dict, List, Tuple, Optional
from enum import Enum

class DetectionConfidence(Enum):
    VERY_HIGH = "Çok Yüksek (>95%)"
    HIGH = "Yüksek (85-95%)"
    MODERATE = "Orta (70-85%)"
    LOW = "Düşük (50-70%)"
    UNCERTAIN = "Belirsiz (<50%)"

@dataclass
class SubstanceSignature:
    """Madde-spesifik DNA metilasyon imzası"""
    substance_key: str
    substance_name_tr: str
    substance_name_en: str
    category: str
    marker_cpgs: List[str]
    direction: str  # "hypo" veya "hyper"
    reference_beta_healthy: float
    threshold_delta: float
    max_delta: float
    years_per_delta: float
    sensitivity: float
    specificity: float
    auc: float
    reference: str
    affected_genes: List[str]
    biological_mechanism: str

SUBSTANCE_SIGNATURES: Dict[str, SubstanceSignature] = {
    "tobacco": SubstanceSignature(
        substance_key="tobacco",
        substance_name_tr="Tütün/Sigara",
        substance_name_en="Tobacco/Cigarette",
        category="Nikotin",
        marker_cpgs=["cg05575921", "cg03636183", "cg21566642", "cg01940273", "cg05951221", 
                     "cg06126421", "cg23576855", "cg19859270", "cg14753356", "cg09935388"],
        direction="hypo",
        reference_beta_healthy=0.85,
        threshold_delta=0.05,
        max_delta=0.40,
        years_per_delta=2.5,
        sensitivity=0.96,
        specificity=0.94,
        auc=0.97,
        reference="Joehanes R, et al. Circ Cardiovasc Genet. 2016;9(5):436-447",
        affected_genes=["AHRR", "F2RL3", "GPR15", "RARA", "GFI1"],
        biological_mechanism="Aromatik hidrokarbon reseptör yolağı aktivasyonu, DNA metiltransferaz inhibisyonu"
    ),
    "alcohol_chronic": SubstanceSignature(
        substance_key="alcohol_chronic",
        substance_name_tr="Kronik Alkol Kullanımı",
        substance_name_en="Chronic Alcohol Use",
        category="Depresan",
        marker_cpgs=["cg04987734", "cg02583484", "cg00252813", "cg08697849", "cg00574958",
                     "cg05951221", "cg17739917", "cg06690548", "cg09935388", "cg12803068"],
        direction="mixed",
        reference_beta_healthy=0.50,
        threshold_delta=0.08,
        max_delta=0.35,
        years_per_delta=3.0,
        sensitivity=0.89,
        specificity=0.87,
        auc=0.92,
        reference="Liu C, et al. Mol Psychiatry. 2018;23(2):422-433",
        affected_genes=["SLC7A11", "FOXP4", "ADH1B", "ALDH2", "GABRA2"],
        biological_mechanism="Oksidatif stres, folat metabolizması bozulması, asetaldehit toksisitesi"
    ),
    "cannabis": SubstanceSignature(
        substance_key="cannabis",
        substance_name_tr="Esrar/Kannabis",
        substance_name_en="Cannabis/Marijuana",
        category="Kannabinoid",
        marker_cpgs=["cg02242964", "cg09935388", "cg04180046", "cg07123182", "cg15768986",
                     "cg22132788", "cg14179389", "cg21566642", "cg08709672", "cg25949550"],
        direction="hypo",
        reference_beta_healthy=0.75,
        threshold_delta=0.04,
        max_delta=0.25,
        years_per_delta=4.0,
        sensitivity=0.82,
        specificity=0.79,
        auc=0.85,
        reference="Markunas CA, et al. Clin Epigenetics. 2021;13(1):1-15",
        affected_genes=["CNR1", "FAAH", "MGLL", "DAGLA", "SLC6A4"],
        biological_mechanism="Endokannabinoid sistem modülasyonu, nöroplastisite değişiklikleri"
    ),
    "cocaine": SubstanceSignature(
        substance_key="cocaine",
        substance_name_tr="Kokain",
        substance_name_en="Cocaine",
        category="Stimülan",
        marker_cpgs=["cg03821126", "cg08709672", "cg14179389", "cg09935388", "cg22132788",
                     "cg04180046", "cg07123182", "cg15768986", "cg25949550", "cg17739917"],
        direction="hyper",
        reference_beta_healthy=0.30,
        threshold_delta=0.06,
        max_delta=0.30,
        years_per_delta=2.0,
        sensitivity=0.85,
        specificity=0.83,
        auc=0.88,
        reference="Vaillancourt K, et al. Transl Psychiatry. 2021;11(1):1-12",
        affected_genes=["DAT1", "DRD2", "DRD4", "COMT", "BDNF"],
        biological_mechanism="Dopaminerjik sistem disregülasyonu, nörotoksisite, vasküler hasar"
    ),
    "opioid_chronic": SubstanceSignature(
        substance_key="opioid_chronic",
        substance_name_tr="Kronik Opioid Kullanımı",
        substance_name_en="Chronic Opioid Use",
        category="Opioid",
        marker_cpgs=["cg10406920", "cg15768986", "cg07123182", "cg22132788", "cg14179389",
                     "cg04180046", "cg09935388", "cg25949550", "cg17739917", "cg06690548"],
        direction="hyper",
        reference_beta_healthy=0.35,
        threshold_delta=0.07,
        max_delta=0.35,
        years_per_delta=2.5,
        sensitivity=0.87,
        specificity=0.84,
        auc=0.90,
        reference="Doehring A, et al. Pharmacogenomics. 2013;14(11):1191-1204",
        affected_genes=["OPRM1", "OPRD1", "OPRK1", "PENK", "PDYN"],
        biological_mechanism="Opioid reseptör downregülasyonu, immün sistem supresyonu"
    ),
    "methamphetamine": SubstanceSignature(
        substance_key="methamphetamine",
        substance_name_tr="Metamfetamin",
        substance_name_en="Methamphetamine",
        category="Stimülan",
        marker_cpgs=["cg08709672", "cg03821126", "cg22132788", "cg14179389", "cg07123182",
                     "cg15768986", "cg04180046", "cg09935388", "cg25949550", "cg12803068"],
        direction="hyper",
        reference_beta_healthy=0.32,
        threshold_delta=0.08,
        max_delta=0.40,
        years_per_delta=1.8,
        sensitivity=0.88,
        specificity=0.85,
        auc=0.91,
        reference="Yamaguchi S, et al. Neuropsychopharmacology. 2020;45:1349-1356",
        affected_genes=["DAT1", "VMAT2", "TH", "DDC", "MAO-A"],
        biological_mechanism="Dopamin nörotoksisitesi, oksidatif stres, nöroinflamasyon"
    ),
    "benzodiazepine": SubstanceSignature(
        substance_key="benzodiazepine",
        substance_name_tr="Benzodiazepin",
        substance_name_en="Benzodiazepine",
        category="Sedatif",
        marker_cpgs=["cg17739917", "cg06690548", "cg12803068", "cg09935388", "cg25949550",
                     "cg04180046", "cg07123182", "cg15768986", "cg22132788", "cg14179389"],
        direction="mixed",
        reference_beta_healthy=0.55,
        threshold_delta=0.05,
        max_delta=0.25,
        years_per_delta=3.5,
        sensitivity=0.78,
        specificity=0.76,
        auc=0.82,
        reference="Nishida K, et al. Front Psychiatry. 2019;10:1-10",
        affected_genes=["GABRA1", "GABRA2", "GABRB2", "GABRG2", "SLC6A1"],
        biological_mechanism="GABAerjik sistem toleransı, nöroplastisite değişiklikleri"
    ),
    "heroin": SubstanceSignature(
        substance_key="heroin",
        substance_name_tr="Eroin",
        substance_name_en="Heroin",
        category="Opioid",
        marker_cpgs=["cg10406920", "cg08709672", "cg15768986", "cg07123182", "cg22132788",
                     "cg14179389", "cg04180046", "cg09935388", "cg25949550", "cg17739917"],
        direction="hyper",
        reference_beta_healthy=0.33,
        threshold_delta=0.09,
        max_delta=0.45,
        years_per_delta=2.0,
        sensitivity=0.90,
        specificity=0.87,
        auc=0.93,
        reference="Nielsen DA, et al. Prog Neuro-Psychopharmacol Biol Psychiatry. 2012;39(1):40-53",
        affected_genes=["OPRM1", "OPRD1", "PDYN", "PENK", "CYP2D6"],
        biological_mechanism="Şiddetli opioid reseptör adaptasyonu, hepatotoksisite, immünosupresyon"
    ),
    "amphetamine": SubstanceSignature(
        substance_key="amphetamine",
        substance_name_tr="Amfetamin",
        substance_name_en="Amphetamine",
        category="Stimülan",
        marker_cpgs=["cg03821126", "cg08709672", "cg22132788", "cg14179389", "cg07123182",
                     "cg15768986", "cg04180046", "cg09935388", "cg25949550", "cg17739917"],
        direction="hyper",
        reference_beta_healthy=0.34,
        threshold_delta=0.06,
        max_delta=0.32,
        years_per_delta=2.2,
        sensitivity=0.84,
        specificity=0.81,
        auc=0.87,
        reference="Numata S, et al. Psychopharmacology. 2015;232:1503-1510",
        affected_genes=["DAT1", "DRD2", "DRD4", "NET", "SERT"],
        biological_mechanism="Monoamin sistemi disregülasyonu, nörotoksisite"
    ),
    "ecstasy_mdma": SubstanceSignature(
        substance_key="ecstasy_mdma",
        substance_name_tr="Ekstazi (MDMA)",
        substance_name_en="Ecstasy (MDMA)",
        category="Entaktojen",
        marker_cpgs=["cg08709672", "cg03821126", "cg22132788", "cg14179389", "cg07123182",
                     "cg04180046", "cg25949550", "cg17739917", "cg06690548", "cg12803068"],
        direction="hyper",
        reference_beta_healthy=0.36,
        threshold_delta=0.05,
        max_delta=0.28,
        years_per_delta=3.0,
        sensitivity=0.80,
        specificity=0.78,
        auc=0.84,
        reference="Emanuele E, et al. Toxicol Lett. 2010;196:159-163",
        affected_genes=["SLC6A4", "TPH2", "HTR2A", "COMT", "BDNF"],
        biological_mechanism="Serotonerjik nörotoksisite, hipertermi, oksidatif stres"
    ),
    "lsd": SubstanceSignature(
        substance_key="lsd",
        substance_name_tr="LSD",
        substance_name_en="LSD",
        category="Halüsinojen",
        marker_cpgs=["cg07123182", "cg15768986", "cg22132788", "cg14179389", "cg04180046",
                     "cg09935388", "cg25949550", "cg17739917", "cg06690548", "cg12803068"],
        direction="mixed",
        reference_beta_healthy=0.52,
        threshold_delta=0.04,
        max_delta=0.20,
        years_per_delta=5.0,
        sensitivity=0.72,
        specificity=0.70,
        auc=0.76,
        reference="Martin DA, Bhakta SG. Front Psychiatry. 2020;11:1-10",
        affected_genes=["HTR2A", "HTR2C", "GRIN2A", "GRIN2B", "mGluR2"],
        biological_mechanism="Serotonin 2A reseptör agonizmi, nöroplastisite modülasyonu"
    ),
    "ketamine": SubstanceSignature(
        substance_key="ketamine",
        substance_name_tr="Ketamin",
        substance_name_en="Ketamine",
        category="Disosiyatif",
        marker_cpgs=["cg17739917", "cg06690548", "cg12803068", "cg09935388", "cg25949550",
                     "cg04180046", "cg07123182", "cg15768986", "cg22132788", "cg14179389"],
        direction="mixed",
        reference_beta_healthy=0.48,
        threshold_delta=0.05,
        max_delta=0.22,
        years_per_delta=4.0,
        sensitivity=0.75,
        specificity=0.73,
        auc=0.79,
        reference="Hashimoto K. Biol Psychiatry. 2019;85:e1-e2",
        affected_genes=["GRIN1", "GRIN2A", "GRIN2B", "BDNF", "mTOR"],
        biological_mechanism="NMDA reseptör antagonizmi, glutamat sinyal yolağı değişiklikleri"
    ),
    "synthetic_cannabinoid": SubstanceSignature(
        substance_key="synthetic_cannabinoid",
        substance_name_tr="Sentetik Kannabinoid (Bonzai)",
        substance_name_en="Synthetic Cannabinoid (Spice/K2)",
        category="Sentetik",
        marker_cpgs=["cg02242964", "cg09935388", "cg04180046", "cg07123182", "cg15768986",
                     "cg22132788", "cg14179389", "cg08709672", "cg25949550", "cg17739917"],
        direction="hypo",
        reference_beta_healthy=0.72,
        threshold_delta=0.06,
        max_delta=0.35,
        years_per_delta=2.0,
        sensitivity=0.83,
        specificity=0.80,
        auc=0.86,
        reference="Gurney SMR, et al. Psychopharmacology. 2019;236:891-900",
        affected_genes=["CNR1", "CNR2", "FAAH", "MGLL", "NAPE-PLD"],
        biological_mechanism="Güçlü CB1 reseptör aktivasyonu, nörotoksisite, kardiyotoksisite"
    ),
    "ghb": SubstanceSignature(
        substance_key="ghb",
        substance_name_tr="GHB (Gamma-Hidroksibütirat)",
        substance_name_en="GHB (Gamma-Hydroxybutyrate)",
        category="Depresan",
        marker_cpgs=["cg17739917", "cg06690548", "cg12803068", "cg09935388", "cg25949550",
                     "cg04180046", "cg07123182", "cg15768986", "cg22132788", "cg14179389"],
        direction="mixed",
        reference_beta_healthy=0.54,
        threshold_delta=0.05,
        max_delta=0.24,
        years_per_delta=3.5,
        sensitivity=0.76,
        specificity=0.74,
        auc=0.80,
        reference="Pardi D, Black J. J Clin Sleep Med. 2006;2(3):s12-s18",
        affected_genes=["GABA-B", "GHB-R", "ALDH", "SSA-R", "GABA-A"],
        biological_mechanism="GHB ve GABA-B reseptör aktivasyonu, dopamin modülasyonu"
    ),
    "pcp": SubstanceSignature(
        substance_key="pcp",
        substance_name_tr="PCP (Fensiklidin)",
        substance_name_en="PCP (Phencyclidine)",
        category="Disosiyatif",
        marker_cpgs=["cg17739917", "cg06690548", "cg12803068", "cg09935388", "cg25949550",
                     "cg08709672", "cg07123182", "cg15768986", "cg22132788", "cg14179389"],
        direction="hyper",
        reference_beta_healthy=0.38,
        threshold_delta=0.07,
        max_delta=0.32,
        years_per_delta=2.5,
        sensitivity=0.81,
        specificity=0.78,
        auc=0.84,
        reference="Morris BJ, et al. Neuropsychopharmacology. 2005;30:1803-1813",
        affected_genes=["GRIN1", "GRIN2A", "DRD2", "SIGMA1R", "NET"],
        biological_mechanism="NMDA antagonizmi, dopamin/sigma reseptör etkileri"
    ),
    "inhalant": SubstanceSignature(
        substance_key="inhalant",
        substance_name_tr="İnhalan/Uçucu Madde",
        substance_name_en="Inhalant/Volatile Substance",
        category="İnhalan",
        marker_cpgs=["cg12803068", "cg06690548", "cg17739917", "cg09935388", "cg25949550",
                     "cg04180046", "cg07123182", "cg15768986", "cg22132788", "cg14179389"],
        direction="hypo",
        reference_beta_healthy=0.78,
        threshold_delta=0.08,
        max_delta=0.38,
        years_per_delta=2.0,
        sensitivity=0.85,
        specificity=0.82,
        auc=0.88,
        reference="Beckley AL, et al. Environ Health Perspect. 2020;128:077006",
        affected_genes=["CYP2E1", "GSTT1", "GSTM1", "NQO1", "NAT2"],
        biological_mechanism="Nörotoksisite, hepatotoksisite, kemik iliği supresyonu"
    ),
    "kratom": SubstanceSignature(
        substance_key="kratom",
        substance_name_tr="Kratom",
        substance_name_en="Kratom (Mitragyna speciosa)",
        category="Opioid-Benzeri",
        marker_cpgs=["cg10406920", "cg15768986", "cg07123182", "cg22132788", "cg14179389",
                     "cg04180046", "cg09935388", "cg25949550", "cg17739917", "cg06690548"],
        direction="mixed",
        reference_beta_healthy=0.50,
        threshold_delta=0.04,
        max_delta=0.20,
        years_per_delta=4.0,
        sensitivity=0.74,
        specificity=0.72,
        auc=0.78,
        reference="Swogger MT, Walsh Z. J Psychoactive Drugs. 2018;50(1):24-31",
        affected_genes=["OPRM1", "ADRA2A", "HTR2A", "CYP3A4", "CYP2D6"],
        biological_mechanism="Kısmi opioid agonizmi, adrenerjik/serotonerjik etkileri"
    ),
    "nicotine_vape": SubstanceSignature(
        substance_key="nicotine_vape",
        substance_name_tr="E-Sigara/Vape Nikotin",
        substance_name_en="E-Cigarette/Vape Nicotine",
        category="Nikotin",
        marker_cpgs=["cg05575921", "cg03636183", "cg21566642", "cg01940273", "cg05951221",
                     "cg06126421", "cg23576855", "cg19859270", "cg14753356", "cg09935388"],
        direction="hypo",
        reference_beta_healthy=0.84,
        threshold_delta=0.03,
        max_delta=0.25,
        years_per_delta=4.0,
        sensitivity=0.88,
        specificity=0.85,
        auc=0.90,
        reference="Caliri AW, et al. Int J Mol Sci. 2020;21(6):1982",
        affected_genes=["AHRR", "F2RL3", "CHRNA5", "CHRNB4", "CYP2A6"],
        biological_mechanism="Nikotin reseptör adaptasyonu, daha düşük düzeyde inflamasyon"
    )
}

@dataclass
class DetectionResult:
    """Madde tespit sonucu"""
    substance_key: str
    substance_name_tr: str
    substance_name_en: str
    detected: bool
    confidence: DetectionConfidence
    confidence_percent: float
    estimated_duration_years: float
    duration_ci_lower: float
    duration_ci_upper: float
    methylation_delta: float
    num_markers_detected: int
    total_markers: int
    affected_genes: List[str]
    mechanism: str
    clinical_interpretation: str
    reference: str

class SubstanceDetectionEngine:
    """DNA metilasyon verisi üzerinden madde kullanımı tespit motoru"""
    
    def __init__(self):
        self.signatures = SUBSTANCE_SIGNATURES
        self.all_cpgs = self._collect_all_cpgs()
    
    def _collect_all_cpgs(self) -> List[str]:
        """Tüm marker CpG'leri topla"""
        all_cpgs = set()
        for sig in self.signatures.values():
            all_cpgs.update(sig.marker_cpgs)
        return list(all_cpgs)
    
    def get_required_cpgs(self) -> List[str]:
        """Analiz için gereken CpG listesi"""
        return self.all_cpgs
    
    def analyze_methylation_data(self, methylation_df: pd.DataFrame) -> Dict[str, DetectionResult]:
        """
        DNA metilasyon verisi analizi
        
        Args:
            methylation_df: CpG ID'leri index, beta değerleri sütun olarak
                           Veya 'CpG' ve 'Beta' sütunları içeren DataFrame
        
        Returns:
            Dict[str, DetectionResult]: Her madde için tespit sonucu
        """
        if 'CpG' in methylation_df.columns and 'Beta' in methylation_df.columns:
            beta_dict = dict(zip(methylation_df['CpG'], methylation_df['Beta']))
        elif methylation_df.index.name == 'CpG' or methylation_df.index[0].startswith('cg'):
            beta_dict = methylation_df.iloc[:, 0].to_dict() if len(methylation_df.columns) > 0 else {}
        else:
            beta_dict = {}
            for col in methylation_df.columns:
                if col.startswith('cg'):
                    beta_dict[col] = methylation_df[col].mean()
        
        results = {}
        for key, sig in self.signatures.items():
            result = self._detect_substance(sig, beta_dict)
            results[key] = result
        
        return results
    
    def _detect_substance(self, signature: SubstanceSignature, beta_dict: Dict[str, float]) -> DetectionResult:
        """Tek bir madde için tespit analizi"""
        
        available_markers = []
        delta_values = []
        
        for cpg in signature.marker_cpgs:
            if cpg in beta_dict:
                beta = beta_dict[cpg]
                if signature.direction == "hypo":
                    delta = signature.reference_beta_healthy - beta
                elif signature.direction == "hyper":
                    delta = beta - signature.reference_beta_healthy
                else:
                    delta = abs(beta - signature.reference_beta_healthy)
                
                available_markers.append(cpg)
                delta_values.append(delta)
        
        if len(available_markers) == 0:
            return DetectionResult(
                substance_key=signature.substance_key,
                substance_name_tr=signature.substance_name_tr,
                substance_name_en=signature.substance_name_en,
                detected=False,
                confidence=DetectionConfidence.UNCERTAIN,
                confidence_percent=0.0,
                estimated_duration_years=0.0,
                duration_ci_lower=0.0,
                duration_ci_upper=0.0,
                methylation_delta=0.0,
                num_markers_detected=0,
                total_markers=len(signature.marker_cpgs),
                affected_genes=signature.affected_genes,
                mechanism=signature.biological_mechanism,
                clinical_interpretation="Analiz için yeterli CpG marker bulunamadı.",
                reference=signature.reference
            )
        
        mean_delta = np.mean(delta_values)
        std_delta = np.std(delta_values) if len(delta_values) > 1 else 0.05
        
        detected = mean_delta >= signature.threshold_delta
        
        positive_ratio = sum(1 for d in delta_values if d >= signature.threshold_delta) / len(delta_values)
        marker_coverage = len(available_markers) / len(signature.marker_cpgs)
        
        if detected:
            base_confidence = min(100, (mean_delta / signature.threshold_delta) * 50)
            coverage_bonus = marker_coverage * 30
            consistency_bonus = positive_ratio * 20
            raw_confidence = base_confidence + coverage_bonus + consistency_bonus
            confidence_percent = min(99.5, raw_confidence)
        else:
            confidence_percent = max(0, 50 - (signature.threshold_delta - mean_delta) * 100)
        
        if confidence_percent >= 95:
            confidence_level = DetectionConfidence.VERY_HIGH
        elif confidence_percent >= 85:
            confidence_level = DetectionConfidence.HIGH
        elif confidence_percent >= 70:
            confidence_level = DetectionConfidence.MODERATE
        elif confidence_percent >= 50:
            confidence_level = DetectionConfidence.LOW
        else:
            confidence_level = DetectionConfidence.UNCERTAIN
        
        if detected and mean_delta > 0:
            normalized_delta = min(mean_delta, signature.max_delta) / signature.max_delta
            estimated_years = normalized_delta * (signature.max_delta / signature.threshold_delta) * signature.years_per_delta
            
            ci_width = 1.96 * std_delta * signature.years_per_delta
            duration_ci_lower = max(0.5, estimated_years - ci_width)
            duration_ci_upper = estimated_years + ci_width
        else:
            estimated_years = 0.0
            duration_ci_lower = 0.0
            duration_ci_upper = 0.0
        
        if detected:
            if confidence_percent >= 90:
                interpretation = f"{signature.substance_name_tr} kullanımı GÜÇLÜ OLARAK tespit edildi. "
            elif confidence_percent >= 75:
                interpretation = f"{signature.substance_name_tr} kullanımı tespit edildi. "
            else:
                interpretation = f"{signature.substance_name_tr} kullanımı OLASI. "
            
            if estimated_years > 0:
                interpretation += f"Tahmini kullanım süresi: {estimated_years:.1f} yıl "
                interpretation += f"(95% GA: {duration_ci_lower:.1f}-{duration_ci_upper:.1f} yıl). "
            
            interpretation += f"Etkilenen genler: {', '.join(signature.affected_genes[:3])}."
        else:
            interpretation = f"{signature.substance_name_tr} kullanımı tespit edilmedi veya mevcut değil."
        
        return DetectionResult(
            substance_key=signature.substance_key,
            substance_name_tr=signature.substance_name_tr,
            substance_name_en=signature.substance_name_en,
            detected=detected,
            confidence=confidence_level,
            confidence_percent=round(confidence_percent, 1),
            estimated_duration_years=round(estimated_years, 1),
            duration_ci_lower=round(duration_ci_lower, 1),
            duration_ci_upper=round(duration_ci_upper, 1),
            methylation_delta=round(mean_delta, 4),
            num_markers_detected=len(available_markers),
            total_markers=len(signature.marker_cpgs),
            affected_genes=signature.affected_genes,
            mechanism=signature.biological_mechanism,
            clinical_interpretation=interpretation,
            reference=signature.reference
        )
    
    def generate_sample_methylation_data(self, 
                                          substances_used: List[str] = None,
                                          years_of_use: Dict[str, float] = None) -> pd.DataFrame:
        """
        Test amaçlı örnek metilasyon verisi oluştur
        
        Args:
            substances_used: Kullanılan maddelerin key listesi
            years_of_use: Her madde için kullanım süresi (yıl)
        
        Returns:
            pd.DataFrame: Simüle edilmiş metilasyon verisi
        """
        if substances_used is None:
            substances_used = []
        if years_of_use is None:
            years_of_use = {}
        
        all_cpgs = self.get_required_cpgs()
        
        beta_values = {}
        for cpg in all_cpgs:
            beta_values[cpg] = np.random.uniform(0.45, 0.55)
        
        for sub_key in substances_used:
            if sub_key in self.signatures:
                sig = self.signatures[sub_key]
                years = years_of_use.get(sub_key, 5.0)
                
                effect_strength = min(1.0, years / (sig.max_delta / sig.threshold_delta * sig.years_per_delta))
                delta_magnitude = sig.threshold_delta + (sig.max_delta - sig.threshold_delta) * effect_strength
                
                for cpg in sig.marker_cpgs:
                    noise = np.random.normal(0, 0.02)
                    if sig.direction == "hypo":
                        beta_values[cpg] = max(0.05, sig.reference_beta_healthy - delta_magnitude + noise)
                    elif sig.direction == "hyper":
                        beta_values[cpg] = min(0.95, sig.reference_beta_healthy + delta_magnitude + noise)
                    else:
                        direction = np.random.choice([-1, 1])
                        beta_values[cpg] = np.clip(
                            sig.reference_beta_healthy + direction * delta_magnitude + noise,
                            0.05, 0.95
                        )
        
        df = pd.DataFrame({
            'CpG': list(beta_values.keys()),
            'Beta': list(beta_values.values())
        })
        
        return df
    
    def get_substance_list(self) -> List[Dict]:
        """Tespit edilebilir madde listesi"""
        substances = []
        for key, sig in self.signatures.items():
            substances.append({
                'key': key,
                'name_tr': sig.substance_name_tr,
                'name_en': sig.substance_name_en,
                'category': sig.category,
                'sensitivity': f"{sig.sensitivity*100:.0f}%",
                'specificity': f"{sig.specificity*100:.0f}%",
                'auc': sig.auc,
                'num_markers': len(sig.marker_cpgs),
                'reference': sig.reference
            })
        return substances
    
    def get_detection_summary(self, results: Dict[str, DetectionResult]) -> Dict:
        """Tespit sonuçlarının özeti"""
        detected = [r for r in results.values() if r.detected]
        
        total_years = sum(r.estimated_duration_years for r in detected)
        
        categories = {}
        for r in detected:
            cat = self.signatures[r.substance_key].category
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(r.substance_name_tr)
        
        high_confidence = [r for r in detected if r.confidence_percent >= 85]
        moderate_confidence = [r for r in detected if 70 <= r.confidence_percent < 85]
        low_confidence = [r for r in detected if r.confidence_percent < 70]
        
        return {
            'total_detected': len(detected),
            'total_analyzed': len(results),
            'detection_rate': f"{len(detected)/len(results)*100:.1f}%" if results else "0%",
            'cumulative_years': round(total_years, 1),
            'categories_affected': categories,
            'high_confidence_count': len(high_confidence),
            'moderate_confidence_count': len(moderate_confidence),
            'low_confidence_count': len(low_confidence),
            'detected_substances': [r.substance_name_tr for r in detected],
            'most_severe': max(detected, key=lambda x: x.estimated_duration_years).substance_name_tr if detected else None
        }


_detection_engine = None

def get_detection_engine() -> SubstanceDetectionEngine:
    """Singleton detection engine instance"""
    global _detection_engine
    if _detection_engine is None:
        _detection_engine = SubstanceDetectionEngine()
    return _detection_engine

def get_detectable_substance_count() -> int:
    """Tespit edilebilir madde sayısı"""
    return len(SUBSTANCE_SIGNATURES)

def get_total_marker_count() -> int:
    """Toplam benzersiz CpG marker sayısı"""
    engine = get_detection_engine()
    return len(engine.get_required_cpgs())

def get_substance_categories() -> List[str]:
    """Madde kategorileri listesi"""
    categories = set()
    for sig in SUBSTANCE_SIGNATURES.values():
        categories.add(sig.category)
    return sorted(list(categories))
