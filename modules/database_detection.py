"""
Veritabani Tabanli Tespit Sistemi
=================================

PostgreSQL veritabanindan hastalik, madde ve ilac
imzalarini kullanarak DNA metilasyon analizi yapar.

Author: EpiClock Team
Version: 1.0
"""

import os
import json
import numpy as np
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
from datetime import datetime

try:
    from sqlalchemy import create_engine, text
    HAS_DB = True
except ImportError:
    HAS_DB = False


@dataclass
class DetectionResult:
    """Tespit sonucu"""
    target_id: str
    target_name_tr: str
    target_name_en: str
    category: str
    result_type: str  # 'disease', 'substance', 'medication'
    probability: float
    confidence: float
    matched_cpgs: int
    total_cpgs: int
    affected_genes: List[str]
    duration_estimate: Optional[Dict] = None
    pubmed_refs: List[str] = None


class DatabaseDetectionSystem:
    """
    Veritabani Tabanli Tespit Sistemi
    
    Veritabanindaki imzalari kullanarak DNA metilasyon
    verilerinden hastalik, madde ve ilac tespiti yapar.
    """
    
    def __init__(self, db_url: str = None):
        self.db_url = db_url or os.environ.get('DATABASE_URL')
        self.engine = None
        
        if self.db_url and HAS_DB:
            try:
                self.engine = create_engine(self.db_url)
            except:
                pass
        
        # Cache
        self._disease_cache = None
        self._substance_cache = None
        self._medication_cache = None
    
    def _load_disease_signatures(self) -> List[Dict]:
        """Hastalik imzalarini yukle"""
        if self._disease_cache:
            return self._disease_cache
        
        if not self.engine:
            return []
        
        try:
            with self.engine.connect() as conn:
                result = conn.execute(text("""
                    SELECT disease_id, disease_name_tr, disease_name_en, 
                           category, cpg_markers, affected_genes,
                           sensitivity, specificity, pubmed_ids
                    FROM disease_signatures
                """))
                
                signatures = []
                for row in result:
                    signatures.append({
                        'id': row[0],
                        'name_tr': row[1],
                        'name_en': row[2],
                        'category': row[3],
                        'cpg_markers': row[4] if isinstance(row[4], dict) else json.loads(row[4] or '{}'),
                        'affected_genes': row[5] or [],
                        'sensitivity': row[6] or 0.8,
                        'specificity': row[7] or 0.8,
                        'pubmed_ids': row[8] or []
                    })
                
                self._disease_cache = signatures
                return signatures
                
        except Exception as e:
            print(f"Hastalik imzalari yukleme hatasi: {e}")
            return []
    
    def _load_substance_signatures(self) -> List[Dict]:
        """Madde imzalarini yukle"""
        if self._substance_cache:
            return self._substance_cache
        
        if not self.engine:
            return []
        
        try:
            with self.engine.connect() as conn:
                result = conn.execute(text("""
                    SELECT substance_id, substance_name_tr, substance_name_en,
                           substance_class, cpg_markers, dose_response_cpgs,
                           affected_genes, min_detectable_months, pubmed_ids
                    FROM substance_signatures
                """))
                
                signatures = []
                for row in result:
                    signatures.append({
                        'id': row[0],
                        'name_tr': row[1],
                        'name_en': row[2],
                        'substance_class': row[3],
                        'cpg_markers': row[4] if isinstance(row[4], dict) else json.loads(row[4] or '{}'),
                        'dose_response': row[5] if isinstance(row[5], dict) else json.loads(row[5] or '{}'),
                        'affected_genes': row[6] or [],
                        'min_detectable_months': row[7] or 6,
                        'pubmed_ids': row[8] or []
                    })
                
                self._substance_cache = signatures
                return signatures
                
        except Exception as e:
            print(f"Madde imzalari yukleme hatasi: {e}")
            return []
    
    def _load_medication_effects(self) -> List[Dict]:
        """Ilac etkilerini yukle"""
        if self._medication_cache:
            return self._medication_cache
        
        if not self.engine:
            return []
        
        try:
            with self.engine.connect() as conn:
                result = conn.execute(text("""
                    SELECT medication_id, name_tr, name_en, category,
                           eaa_effect, eaa_direction, mechanism_tr,
                           target_genes, affected_cpgs, pubmed_ids
                    FROM therapeutic_medications
                """))
                
                medications = []
                for row in result:
                    medications.append({
                        'id': row[0],
                        'name_tr': row[1],
                        'name_en': row[2],
                        'category': row[3],
                        'eaa_effect': row[4] or 0,
                        'eaa_direction': row[5] or 'bilinmiyor',
                        'mechanism_tr': row[6] or '',
                        'target_genes': row[7] or [],
                        'affected_cpgs': row[8] if isinstance(row[8], dict) else json.loads(row[8] or '{}'),
                        'pubmed_ids': row[9] or []
                    })
                
                self._medication_cache = medications
                return medications
                
        except Exception as e:
            print(f"Ilac etkileri yukleme hatasi: {e}")
            return []
    
    def _calculate_probability(self, signature_cpgs: Dict[str, float],
                                patient_cpgs: Dict[str, float],
                                sensitivity: float = 0.8) -> Tuple[float, float, int]:
        """
        Olasilik hesapla - Gelismis Algoritma
        
        Args:
            signature_cpgs: Imza CpG katsayilari {cpg: expected_beta_change}
            patient_cpgs: Hasta CpG degerleri {cpg: measured_beta}
            sensitivity: Model duyarliligi
        
        Returns:
            (probability, confidence, matched_count)
        """
        if not signature_cpgs:
            return 0.0, 0.0, 0
        
        matched_cpgs = set(signature_cpgs.keys()) & set(patient_cpgs.keys())
        
        if len(matched_cpgs) == 0:
            return 0.0, 0.0, 0
        
        # Gelismis skor hesaplama - Beta katsayilarina gore
        concordant_count = 0
        total_score = 0.0
        
        for cpg in matched_cpgs:
            coef = signature_cpgs[cpg]  # EWAS beta katsayisi (- veya +)
            measured = patient_cpgs[cpg]  # Olculen beta (0-1 arasi)
            
            # Normal referans: 0.5 (orta metilasyon)
            deviation = measured - 0.5
            
            # Katsayi ile ayni yonde sapma = pozitif katki
            if coef < 0:  # Hipometilasyon bekleniyor
                if deviation < 0:  # Olcum de dusuk = uyumlu
                    concordant_count += 1
                    # Sapma buyuklugu * katsayi buyuklugu
                    total_score += abs(deviation) * abs(coef) * 20
                elif deviation > 0.1:  # Ters yonde belirgin sapma
                    total_score -= abs(deviation) * abs(coef) * 5
            else:  # Hipermetilasyon bekleniyor
                if deviation > 0:  # Olcum de yuksek = uyumlu
                    concordant_count += 1
                    total_score += abs(deviation) * abs(coef) * 20
                elif deviation < -0.1:  # Ters yonde belirgin sapma
                    total_score -= abs(deviation) * abs(coef) * 5
        
        # Uyumluluk orani
        concordance_rate = concordant_count / len(matched_cpgs)
        
        # Normalize skor (0-1 arasi)
        max_possible = len(matched_cpgs) * 0.5 * 0.1 * 20  # max deviation * max coef * multiplier
        normalized_score = min(1.0, max(0, total_score / max_possible)) if max_possible > 0 else 0
        
        # Olasilik: concordance + skor birlesimi
        base_prob = concordance_rate * 0.6 + normalized_score * 0.4
        
        # En az 1 CpG eslesirse ve uyumluluk yuksekse
        if concordant_count >= 1 and concordance_rate >= 0.3:
            probability = min(0.95, base_prob + 0.2)
        else:
            probability = base_prob * 0.5
        
        # Confidence: kapsam * duyarlilik * uyumluluk
        coverage = len(matched_cpgs) / len(signature_cpgs)
        confidence = coverage * sensitivity * (0.5 + concordance_rate * 0.5)
        
        return float(probability), float(confidence), len(matched_cpgs)
    
    def detect_diseases(self, methylation_data: Dict[str, float],
                        min_probability: float = 0.3,
                        min_coverage: float = 0.2) -> List[DetectionResult]:
        """
        Hastaliklari tespit et
        
        Args:
            methylation_data: {cpg: beta_value}
            min_probability: Minimum olasilik esigi
            min_coverage: Minimum CpG kapsami
        
        Returns:
            DetectionResult listesi
        """
        signatures = self._load_disease_signatures()
        results = []
        
        for sig in signatures:
            cpg_markers = sig.get('cpg_markers', {})
            if not cpg_markers:
                continue
            
            prob, conf, matched = self._calculate_probability(
                cpg_markers, methylation_data, sig.get('sensitivity', 0.8)
            )
            
            coverage = matched / len(cpg_markers) if cpg_markers else 0
            
            if prob >= min_probability and coverage >= min_coverage:
                results.append(DetectionResult(
                    target_id=sig['id'],
                    target_name_tr=sig['name_tr'],
                    target_name_en=sig['name_en'],
                    category=sig['category'],
                    result_type='disease',
                    probability=prob,
                    confidence=conf,
                    matched_cpgs=matched,
                    total_cpgs=len(cpg_markers),
                    affected_genes=sig.get('affected_genes', []),
                    pubmed_refs=sig.get('pubmed_ids', [])
                ))
        
        # Olasiliga gore sirala
        results.sort(key=lambda x: x.probability, reverse=True)
        return results
    
    def detect_substances(self, methylation_data: Dict[str, float],
                          min_probability: float = 0.3,
                          min_coverage: float = 0.2) -> List[DetectionResult]:
        """
        Maddeleri tespit et
        
        Args:
            methylation_data: {cpg: beta_value}
            min_probability: Minimum olasilik esigi
            min_coverage: Minimum CpG kapsami
        
        Returns:
            DetectionResult listesi
        """
        signatures = self._load_substance_signatures()
        results = []
        
        for sig in signatures:
            cpg_markers = sig.get('cpg_markers', {})
            if not cpg_markers:
                continue
            
            prob, conf, matched = self._calculate_probability(
                cpg_markers, methylation_data, 0.75  # Maddeler icin daha dusuk sensitivity
            )
            
            coverage = matched / len(cpg_markers) if cpg_markers else 0
            
            if prob >= min_probability and coverage >= min_coverage:
                # Sure tahmini
                duration_estimate = self._estimate_duration(
                    sig.get('dose_response', {}),
                    methylation_data
                )
                
                results.append(DetectionResult(
                    target_id=sig['id'],
                    target_name_tr=sig['name_tr'],
                    target_name_en=sig['name_en'],
                    category=sig['substance_class'],
                    result_type='substance',
                    probability=prob,
                    confidence=conf,
                    matched_cpgs=matched,
                    total_cpgs=len(cpg_markers),
                    affected_genes=sig.get('affected_genes', []),
                    duration_estimate=duration_estimate,
                    pubmed_refs=sig.get('pubmed_ids', [])
                ))
        
        results.sort(key=lambda x: x.probability, reverse=True)
        return results
    
    def _estimate_duration(self, dose_response: Dict, 
                           methylation_data: Dict[str, float]) -> Optional[Dict]:
        """Maruziyet suresini tahmin et"""
        if not dose_response:
            return None
        
        for cpg, params in dose_response.items():
            if cpg in methylation_data:
                baseline = params.get('baseline', 0.5)
                annual_change = params.get('annual_change', -0.01)
                measured = methylation_data[cpg]
                
                delta = measured - baseline
                
                if annual_change != 0:
                    years = abs(delta / annual_change)
                    
                    return {
                        'estimated_years': round(years, 1),
                        'min_years': round(max(0, years * 0.7), 1),
                        'max_years': round(years * 1.3, 1),
                        'confidence': min(0.85, 0.5 + abs(delta) * 2),
                        'marker_cpg': cpg,
                        'baseline': baseline,
                        'measured': measured
                    }
        
        return None
    
    def detect_medication_effects(self, methylation_data: Dict[str, float]) -> List[Dict]:
        """
        Terapotik ilac etkilerini tespit et
        
        Args:
            methylation_data: {cpg: beta_value}
        
        Returns:
            Tespit edilen ilac etkileri listesi
        """
        medications = self._load_medication_effects()
        results = []
        
        for med in medications:
            affected_cpgs = med.get('affected_cpgs', {})
            if not affected_cpgs:
                continue
            
            matched = set(affected_cpgs.keys()) & set(methylation_data.keys())
            
            if len(matched) > 0:
                # Etki skoru hesapla
                effect_score = 0
                for cpg in matched:
                    expected = affected_cpgs[cpg]
                    measured = methylation_data[cpg]
                    
                    # Beklenen yonde degisim
                    if (expected > 0 and measured > 0.55) or (expected < 0 and measured < 0.45):
                        effect_score += 1
                
                if effect_score > 0:
                    results.append({
                        'medication_id': med['id'],
                        'name_tr': med['name_tr'],
                        'name_en': med['name_en'],
                        'category': med['category'],
                        'eaa_effect': med['eaa_effect'],
                        'eaa_direction': med['eaa_direction'],
                        'mechanism': med['mechanism_tr'],
                        'matched_cpgs': len(matched),
                        'effect_score': effect_score / len(matched),
                        'target_genes': med['target_genes']
                    })
        
        return results
    
    def run_full_analysis(self, methylation_data: Dict[str, float],
                          chronological_age: float = None,
                          sex: str = None) -> Dict[str, Any]:
        """
        Tam analiz calistir
        
        Args:
            methylation_data: {cpg: beta_value}
            chronological_age: Kronolojik yas
            sex: Cinsiyet (M/F)
        
        Returns:
            {diseases, substances, medications, summary}
        """
        # Hastaliklari tespit et
        diseases = self.detect_diseases(methylation_data)
        
        # Maddeleri tespit et
        substances = self.detect_substances(methylation_data)
        
        # Ilac etkilerini tespit et
        medications = self.detect_medication_effects(methylation_data)
        
        # Epigenetik yas tahmini (basit)
        eaa = 0.0
        
        # Hastalik kaynaklı EAA
        for d in diseases:
            if d.probability > 0.5:
                if d.category == 'Kanser':
                    eaa += 3.0 * d.probability
                elif d.category == 'Metabolik':
                    eaa += 2.0 * d.probability
                elif d.category == 'Norolojik':
                    eaa += 2.5 * d.probability
                else:
                    eaa += 1.0 * d.probability
        
        # Madde kaynakli EAA
        for s in substances:
            if s.probability > 0.5:
                if s.duration_estimate:
                    years = s.duration_estimate.get('estimated_years', 1)
                    eaa += years * 0.8 * s.probability
                else:
                    eaa += 1.5 * s.probability
        
        # Ilac kaynakli EAA
        for m in medications:
            eaa += m.get('eaa_effect', 0) * m.get('effect_score', 0.5)
        
        epigenetic_age = (chronological_age or 40) + eaa
        
        return {
            'diseases': [
                {
                    'id': d.target_id,
                    'name_tr': d.target_name_tr,
                    'name_en': d.target_name_en,
                    'category': d.category,
                    'probability': round(d.probability * 100, 1),
                    'confidence': round(d.confidence * 100, 1),
                    'matched_cpgs': d.matched_cpgs,
                    'total_cpgs': d.total_cpgs,
                    'affected_genes': d.affected_genes[:5],
                    'pubmed_refs': d.pubmed_refs[:3] if d.pubmed_refs else []
                }
                for d in diseases
            ],
            'substances': [
                {
                    'id': s.target_id,
                    'name_tr': s.target_name_tr,
                    'name_en': s.target_name_en,
                    'class': s.category,
                    'probability': round(s.probability * 100, 1),
                    'confidence': round(s.confidence * 100, 1),
                    'matched_cpgs': s.matched_cpgs,
                    'total_cpgs': s.total_cpgs,
                    'affected_genes': s.affected_genes[:5],
                    'duration': s.duration_estimate,
                    'pubmed_refs': s.pubmed_refs[:3] if s.pubmed_refs else []
                }
                for s in substances
            ],
            'medications': medications,
            'summary': {
                'chronological_age': chronological_age,
                'epigenetic_age': round(epigenetic_age, 1),
                'eaa': round(eaa, 1),
                'diseases_detected': len(diseases),
                'substances_detected': len(substances),
                'medications_detected': len(medications),
                'analysis_timestamp': datetime.now().isoformat()
            }
        }
    
    def get_statistics(self) -> Dict[str, Any]:
        """Veritabani istatistikleri"""
        diseases = self._load_disease_signatures()
        substances = self._load_substance_signatures()
        medications = self._load_medication_effects()
        
        return {
            'total_diseases': len(diseases),
            'total_substances': len(substances),
            'total_medications': len(medications),
            'disease_categories': list(set(d['category'] for d in diseases)),
            'substance_classes': list(set(s['substance_class'] for s in substances)),
            'medication_categories': list(set(m['category'] for m in medications))
        }


# Singleton instance
_detection_system = None

def get_detection_system() -> DatabaseDetectionSystem:
    """Global detection system instance"""
    global _detection_system
    if _detection_system is None:
        _detection_system = DatabaseDetectionSystem()
    return _detection_system
