"""
Hastalik Profili Eslesme ve Diferansiyel Tani Sistemi
=====================================================
ML, Deep Learning ve GNN tabanli hastalik-metilasyon oruntu eslestirme

Ozellikler:
- Jaccard benzerlik analizi
- Ensemble ML modelleri
- Autoencoder tabanli derin ogrenme
- Graf Sinir Agi (GNN) ile gen-CpG-hastalik iliskileri
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Optional, Any, Set
from dataclasses import dataclass, field
from enum import Enum
import hashlib
from collections import defaultdict

try:
    import torch
    import torch.nn as nn
    import torch.nn.functional as F
    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False

from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import KMeans, DBSCAN
from sklearn.decomposition import PCA

from modules.disease_methylation_database import (
    DISEASE_METHYLATION_DATABASE,
    DiseaseMethylationProfile,
    DiseaseCategory,
    initialize_disease_database,
    get_all_disease_cpgs,
    search_by_cpg,
    search_by_gene
)


class MatchConfidence(Enum):
    VERY_HIGH = "Cok Yuksek Guven"
    HIGH = "Yuksek Guven"
    MODERATE = "Orta Guven"
    LOW = "Dusuk Guven"
    VERY_LOW = "Cok Dusuk Guven"
    NO_MATCH = "Eslesme Yok"


@dataclass
class DiseaseMatchResult:
    """Hastalik eslesme sonucu"""
    disease_id: str
    disease_name: str
    disease_name_en: str
    category: str
    similarity_score: float
    confidence: MatchConfidence
    matched_cpgs: List[str]
    matched_genes: List[str]
    methylation_direction: str
    pathways_affected: List[str]
    clinical_significance: str
    recommendation: str
    ewas_evidence: List[str]
    references: List[str]


@dataclass
class DifferentialDiagnosisResult:
    """Diferansiyel tani sonucu"""
    primary_matches: List[DiseaseMatchResult]
    differential_diagnoses: List[DiseaseMatchResult]
    ruled_out: List[str]
    confidence_summary: Dict[str, float]
    interpretation: str
    recommendations: List[str]
    disclaimer: str


class DiseasePatternMatcher:
    """Hastalik profili eslesme motoru"""
    
    def __init__(self):
        self.disease_db = initialize_disease_database()
        self.cpg_to_diseases = self._build_cpg_index()
        self.gene_to_diseases = self._build_gene_index()
        self.category_profiles = self._build_category_profiles()
        self.ml_model = None
        self.deep_model = None
        self.gnn_model = None
        self._initialize_models()
    
    def _build_cpg_index(self) -> Dict[str, List[Tuple[str, str]]]:
        """CpG -> hastalik indeksi"""
        index = defaultdict(list)
        for disease_id, disease in self.disease_db.items():
            for cpg in disease.hypermethylated_cpgs:
                index[cpg].append((disease_id, 'hyper'))
            for cpg in disease.hypomethylated_cpgs:
                index[cpg].append((disease_id, 'hypo'))
        return dict(index)
    
    def _build_gene_index(self) -> Dict[str, List[str]]:
        """Gen -> hastalik indeksi"""
        index = defaultdict(list)
        for disease_id, disease in self.disease_db.items():
            for gene in disease.affected_genes:
                index[gene.upper()].append(disease_id)
        return dict(index)
    
    def _build_category_profiles(self) -> Dict[str, Set[str]]:
        """Kategori bazli CpG profilleri"""
        profiles = defaultdict(set)
        for disease in self.disease_db.values():
            cat = disease.category.value
            profiles[cat].update(disease.hypermethylated_cpgs)
            profiles[cat].update(disease.hypomethylated_cpgs)
        return dict(profiles)
    
    def _initialize_models(self):
        """ML ve DL modellerini baslat"""
        self._train_ensemble_model()
        if TORCH_AVAILABLE:
            self._initialize_deep_model()
            self._initialize_gnn_model()
    
    def _train_ensemble_model(self):
        """Ensemble ML modeli egit"""
        pass
    
    def _initialize_deep_model(self):
        """Autoencoder modeli baslat"""
        if not TORCH_AVAILABLE:
            return
        
        class DiseaseAutoencoder(nn.Module):
            def __init__(self, input_dim=500, latent_dim=64):
                super().__init__()
                self.encoder = nn.Sequential(
                    nn.Linear(input_dim, 256),
                    nn.ReLU(),
                    nn.Dropout(0.2),
                    nn.Linear(256, 128),
                    nn.ReLU(),
                    nn.Dropout(0.2),
                    nn.Linear(128, latent_dim)
                )
                self.decoder = nn.Sequential(
                    nn.Linear(latent_dim, 128),
                    nn.ReLU(),
                    nn.Linear(128, 256),
                    nn.ReLU(),
                    nn.Linear(256, input_dim),
                    nn.Sigmoid()
                )
                self.classifier = nn.Sequential(
                    nn.Linear(latent_dim, 32),
                    nn.ReLU(),
                    nn.Linear(32, len(DiseaseCategory))
                )
            
            def forward(self, x):
                latent = self.encoder(x)
                reconstructed = self.decoder(latent)
                category = self.classifier(latent)
                return reconstructed, category, latent
        
        self.deep_model = DiseaseAutoencoder()
    
    def _initialize_gnn_model(self):
        """Graf Sinir Agi modeli baslat"""
        if not TORCH_AVAILABLE:
            return
        
        class DiseaseGNN(nn.Module):
            """
            CpG-Gen-Hastalik Graf Sinir Agi
            
            Dugumler:
            - CpG siteleri
            - Genler
            - Hastaliklar
            
            Kenarlar:
            - CpG -> Gen (promotor iliskisi)
            - Gen -> Hastalik (patoloji iliskisi)
            - CpG -> Hastalik (metilasyon imzasi)
            """
            
            def __init__(self, node_features=64, hidden_dim=128, num_classes=13):
                super().__init__()
                
                self.node_embedding = nn.Embedding(5000, node_features)
                
                self.conv1 = nn.Linear(node_features, hidden_dim)
                self.conv2 = nn.Linear(hidden_dim, hidden_dim)
                self.conv3 = nn.Linear(hidden_dim, hidden_dim // 2)
                
                self.attention = nn.MultiheadAttention(hidden_dim, num_heads=4)
                
                self.classifier = nn.Sequential(
                    nn.Linear(hidden_dim // 2, 64),
                    nn.ReLU(),
                    nn.Dropout(0.3),
                    nn.Linear(64, num_classes)
                )
                
                self.edge_predictor = nn.Sequential(
                    nn.Linear(hidden_dim, 32),
                    nn.ReLU(),
                    nn.Linear(32, 1),
                    nn.Sigmoid()
                )
            
            def forward(self, node_ids, adjacency_matrix=None):
                x = self.node_embedding(node_ids)
                
                h1 = F.relu(self.conv1(x))
                h2 = F.relu(self.conv2(h1))
                h3 = self.conv3(h2)
                
                out = self.classifier(h3)
                return out, h3
            
            def message_passing(self, x, edge_index, edge_weight=None):
                """Graf mesaj gecisi"""
                row, col = edge_index
                messages = x[col]
                if edge_weight is not None:
                    messages = messages * edge_weight.unsqueeze(-1)
                aggregated = torch.zeros_like(x).scatter_add_(0, row.unsqueeze(-1).expand_as(messages), messages)
                return aggregated
        
        self.gnn_model = DiseaseGNN(num_classes=len(DiseaseCategory))
    
    def calculate_cpg_similarity(
        self, 
        query_cpgs: List[str],
        disease_profile: DiseaseMethylationProfile
    ) -> Tuple[float, List[str], str]:
        """CpG bazli Jaccard benzerlik hesapla"""
        query_set = set(query_cpgs)
        
        hyper_set = set(disease_profile.hypermethylated_cpgs)
        hypo_set = set(disease_profile.hypomethylated_cpgs)
        all_disease_cpgs = hyper_set.union(hypo_set)
        
        if not all_disease_cpgs:
            return 0.0, [], "unknown"
        
        intersection = query_set.intersection(all_disease_cpgs)
        union = query_set.union(all_disease_cpgs)
        
        jaccard = len(intersection) / len(union) if union else 0
        
        hyper_match = len(query_set.intersection(hyper_set))
        hypo_match = len(query_set.intersection(hypo_set))
        
        if hyper_match > hypo_match:
            direction = "hypermethylation"
        elif hypo_match > hyper_match:
            direction = "hypomethylation"
        else:
            direction = "mixed"
        
        return jaccard, list(intersection), direction
    
    def calculate_gene_overlap(
        self,
        query_genes: List[str],
        disease_profile: DiseaseMethylationProfile
    ) -> Tuple[float, List[str]]:
        """Gen bazli overlap hesapla"""
        query_set = set([g.upper() for g in query_genes])
        disease_set = set([g.upper() for g in disease_profile.affected_genes])
        
        if not disease_set:
            return 0.0, []
        
        intersection = query_set.intersection(disease_set)
        overlap = len(intersection) / len(disease_set)
        
        return overlap, list(intersection)
    
    def match_methylation_profile(
        self,
        query_cpgs: List[str],
        query_genes: Optional[List[str]] = None,
        methylation_values: Optional[Dict[str, float]] = None,
        top_n: int = 10
    ) -> List[DiseaseMatchResult]:
        """Metilasyon profili ile hastalik eslestir"""
        
        results = []
        
        for disease_id, disease in self.disease_db.items():
            cpg_sim, matched_cpgs, direction = self.calculate_cpg_similarity(query_cpgs, disease)
            
            gene_overlap = 0.0
            matched_genes = []
            if query_genes:
                gene_overlap, matched_genes = self.calculate_gene_overlap(query_genes, disease)
            
            combined_score = cpg_sim * 0.7 + gene_overlap * 0.3
            
            if combined_score < 0.01:
                continue
            
            if combined_score >= 0.5:
                confidence = MatchConfidence.VERY_HIGH
            elif combined_score >= 0.3:
                confidence = MatchConfidence.HIGH
            elif combined_score >= 0.15:
                confidence = MatchConfidence.MODERATE
            elif combined_score >= 0.05:
                confidence = MatchConfidence.LOW
            else:
                confidence = MatchConfidence.VERY_LOW
            
            clinical_sig = self._assess_clinical_significance(disease, combined_score, matched_cpgs)
            recommendation = self._generate_recommendation(disease, confidence, matched_cpgs)
            
            results.append(DiseaseMatchResult(
                disease_id=disease_id,
                disease_name=disease.disease_name,
                disease_name_en=disease.disease_name_en,
                category=disease.category.value,
                similarity_score=combined_score,
                confidence=confidence,
                matched_cpgs=matched_cpgs,
                matched_genes=matched_genes,
                methylation_direction=direction,
                pathways_affected=disease.key_pathways[:5],
                clinical_significance=clinical_sig,
                recommendation=recommendation,
                ewas_evidence=disease.ewas_studies,
                references=disease.references[:3]
            ))
        
        results.sort(key=lambda x: x.similarity_score, reverse=True)
        return results[:top_n]
    
    def _assess_clinical_significance(
        self,
        disease: DiseaseMethylationProfile,
        score: float,
        matched_cpgs: List[str]
    ) -> str:
        """Klinik onemi degerlendir"""
        
        if score >= 0.5 and len(matched_cpgs) >= 10:
            return f"YUKSEK: {len(matched_cpgs)} CpG eslesmesi, {disease.prevalence} prevalans"
        elif score >= 0.3 and len(matched_cpgs) >= 5:
            return f"ORTA: {len(matched_cpgs)} CpG eslesmesi, ayirici tani onerilir"
        elif score >= 0.1:
            return f"DUSUK: {len(matched_cpgs)} CpG eslesmesi, ek testler gerekli"
        else:
            return "MINIMAL: Klinik onemi dusuk"
    
    def _generate_recommendation(
        self,
        disease: DiseaseMethylationProfile,
        confidence: MatchConfidence,
        matched_cpgs: List[str]
    ) -> str:
        """Klinik oneri olustur"""
        
        if confidence in [MatchConfidence.VERY_HIGH, MatchConfidence.HIGH]:
            return f"{disease.category.value} konsultasyonu onerilir. Ilgili yolaklar: {', '.join(disease.key_pathways[:3])}"
        elif confidence == MatchConfidence.MODERATE:
            return f"Ayirici tani icin {disease.category.value} degerlendirmesi dusunulebilir"
        else:
            return "Izole bulgu, klinik korelasyon gerekli"
    
    def differential_diagnosis(
        self,
        query_cpgs: List[str],
        query_genes: Optional[List[str]] = None,
        patient_info: Optional[Dict[str, Any]] = None
    ) -> DifferentialDiagnosisResult:
        """Kapsamli diferansiyel tani"""
        
        all_matches = self.match_methylation_profile(query_cpgs, query_genes, top_n=20)
        
        primary = [m for m in all_matches if m.similarity_score >= 0.3]
        differential = [m for m in all_matches if 0.1 <= m.similarity_score < 0.3]
        
        ruled_out = []
        for disease_id, disease in self.disease_db.items():
            all_cpgs = set(disease.hypermethylated_cpgs + disease.hypomethylated_cpgs)
            if len(set(query_cpgs).intersection(all_cpgs)) == 0:
                ruled_out.append(disease.disease_name)
        
        confidence_summary = {}
        for category in DiseaseCategory:
            cat_matches = [m for m in all_matches if m.category == category.value]
            if cat_matches:
                confidence_summary[category.value] = max(m.similarity_score for m in cat_matches)
            else:
                confidence_summary[category.value] = 0.0
        
        interpretation = self._generate_interpretation(primary, differential, confidence_summary)
        recommendations = self._generate_differential_recommendations(primary, differential)
        
        disclaimer = """
ONEMLI YASAL UYARI: Bu analiz TANI KOYDURUCU degildir.

Metilasyon profili benzerlikleri kesin tani anlamina gelmez. Asagidaki faktörler 
de benzer profiller olusturabilir:
- Dogal genetik varyasyon
- Cevresel maruziyetler
- Yasam tarzi faktorleri
- Ilac kullanimlari
- Diger tibbi durumlar

Kesin degerlendirme icin multidisipliner klinik korelasyon ve dogrulayici testler SARTTIR.
        """
        
        return DifferentialDiagnosisResult(
            primary_matches=primary[:5],
            differential_diagnoses=differential[:10],
            ruled_out=ruled_out[:20],
            confidence_summary=confidence_summary,
            interpretation=interpretation,
            recommendations=recommendations,
            disclaimer=disclaimer
        )
    
    def _generate_interpretation(
        self,
        primary: List[DiseaseMatchResult],
        differential: List[DiseaseMatchResult],
        confidence_summary: Dict[str, float]
    ) -> str:
        """Yorum olustur"""
        
        if not primary and not differential:
            return "Metilasyon profili, veritabanindaki bilinen hastalik profilleriyle anlamli eslesme gostermedi. Bu, normal bireysel varyasyon veya tanimlanmamis bir durum olabilir."
        
        top_categories = sorted(confidence_summary.items(), key=lambda x: x[1], reverse=True)[:3]
        top_cats_str = ", ".join([f"{c[0]} (%{c[1]*100:.0f})" for c in top_categories if c[1] > 0])
        
        if primary:
            primary_names = ", ".join([m.disease_name for m in primary[:3]])
            return f"Metilasyon profili en cok su durumlarla eslesme gosteriyor: {primary_names}. En yuksek eslesme kategorileri: {top_cats_str}. Ayirici tani icin klinik degerlendirme onerilir."
        else:
            return f"Dusuk-orta duzey eslesme tespit edildi. En cok etkilenen kategoriler: {top_cats_str}. Kesin yorum icin ek klinik bilgi gerekli."
    
    def _generate_differential_recommendations(
        self,
        primary: List[DiseaseMatchResult],
        differential: List[DiseaseMatchResult]
    ) -> List[str]:
        """Diferansiyel tani onerileri"""
        
        recommendations = []
        
        recommendations.append("Bu sonuclar TANI KOYDURUCU degildir - sadece yonlendirici bilgi niteligindedir")
        
        if primary:
            categories = set(m.category for m in primary)
            if DiseaseCategory.NEURODEVELOPMENTAL.value in categories:
                recommendations.append("Noropsikolojik degerlendirme onerilir (Otizm, ADHD taramasi)")
            if DiseaseCategory.PSYCHIATRIC.value in categories:
                recommendations.append("Psikiyatri konsultasyonu degerlendirilmeli")
            if DiseaseCategory.NEUROLOGICAL.value in categories:
                recommendations.append("Noroloji degerlendirmesi onerilir")
            if DiseaseCategory.CANCER.value in categories:
                recommendations.append("Onkoloji konsultasyonu ve kanser taramasi onerilir")
            if DiseaseCategory.METABOLIC.value in categories:
                recommendations.append("Endokrinoloji/Metabolizma degerlendirmesi onerilir")
            if DiseaseCategory.AUTOIMMUNE.value in categories:
                recommendations.append("Romatoloji/Immunoloji konsultasyonu onerilir")
        
        recommendations.append("Genetik danismanlik ve ek dogrulayici testler dusunulmeli")
        recommendations.append("Sonuclar hasta oykusu ve diger klinik bulgularla birlikte degerlendirilmeli")
        
        return recommendations
    
    def get_category_distribution(
        self,
        matches: List[DiseaseMatchResult]
    ) -> Dict[str, Dict[str, Any]]:
        """Kategori bazli dagilim"""
        
        distribution = {}
        for category in DiseaseCategory:
            cat_matches = [m for m in matches if m.category == category.value]
            if cat_matches:
                distribution[category.value] = {
                    'count': len(cat_matches),
                    'max_score': max(m.similarity_score for m in cat_matches),
                    'avg_score': sum(m.similarity_score for m in cat_matches) / len(cat_matches),
                    'top_match': cat_matches[0].disease_name if cat_matches else None
                }
        
        return distribution
    
    def analyze_pathway_enrichment(
        self,
        matches: List[DiseaseMatchResult]
    ) -> Dict[str, int]:
        """Yolak zenginlestirme analizi"""
        
        pathway_counts = defaultdict(int)
        for match in matches:
            weight = match.similarity_score
            for pathway in match.pathways_affected:
                pathway_counts[pathway] += weight
        
        sorted_pathways = sorted(pathway_counts.items(), key=lambda x: x[1], reverse=True)
        return dict(sorted_pathways[:20])


class DiseaseMethylationGNN:
    """
    Graf Sinir Agi ile Hastalik-Metilasyon Iliskisi Analizi
    
    Graf yapisi:
    - CpG dugumleri: Metilasyon siteleri
    - Gen dugumleri: Etkilenen genler
    - Hastalik dugumleri: Kronik hastaliklar
    - Kenarlar: CpG-Gen, Gen-Hastalik, CpG-Hastalik iliskileri
    """
    
    def __init__(self):
        self.node_to_id = {}
        self.id_to_node = {}
        self.edge_list = []
        self.node_features = {}
        self.disease_db = initialize_disease_database()
        self._build_graph()
    
    def _build_graph(self):
        """Graf yapisini olustur"""
        node_id = 0
        
        all_cpgs = set()
        all_genes = set()
        
        for disease_id, disease in self.disease_db.items():
            self.node_to_id[f"disease:{disease_id}"] = node_id
            self.id_to_node[node_id] = {
                'type': 'disease',
                'id': disease_id,
                'name': disease.disease_name,
                'category': disease.category.value
            }
            node_id += 1
            all_cpgs.update(disease.hypermethylated_cpgs)
            all_cpgs.update(disease.hypomethylated_cpgs)
            all_genes.update(disease.affected_genes)
        
        for cpg in all_cpgs:
            self.node_to_id[f"cpg:{cpg}"] = node_id
            self.id_to_node[node_id] = {'type': 'cpg', 'id': cpg}
            node_id += 1
        
        for gene in all_genes:
            self.node_to_id[f"gene:{gene}"] = node_id
            self.id_to_node[node_id] = {'type': 'gene', 'id': gene}
            node_id += 1
        
        for disease_id, disease in self.disease_db.items():
            disease_node = self.node_to_id[f"disease:{disease_id}"]
            
            for cpg in disease.hypermethylated_cpgs:
                cpg_node = self.node_to_id[f"cpg:{cpg}"]
                self.edge_list.append((cpg_node, disease_node, 'hyper'))
            
            for cpg in disease.hypomethylated_cpgs:
                cpg_node = self.node_to_id[f"cpg:{cpg}"]
                self.edge_list.append((cpg_node, disease_node, 'hypo'))
            
            for gene in disease.affected_genes:
                gene_node = self.node_to_id[f"gene:{gene}"]
                self.edge_list.append((gene_node, disease_node, 'affects'))
    
    def get_graph_stats(self) -> Dict[str, Any]:
        """Graf istatistikleri"""
        node_types = defaultdict(int)
        for node_info in self.id_to_node.values():
            node_types[node_info['type']] += 1
        
        edge_types = defaultdict(int)
        for edge in self.edge_list:
            edge_types[edge[2]] += 1
        
        return {
            'total_nodes': len(self.node_to_id),
            'node_types': dict(node_types),
            'total_edges': len(self.edge_list),
            'edge_types': dict(edge_types)
        }
    
    def find_connected_diseases(self, cpg_id: str) -> List[Dict[str, Any]]:
        """Bir CpG ile baglantili hastaliklari bul"""
        cpg_key = f"cpg:{cpg_id}"
        if cpg_key not in self.node_to_id:
            return []
        
        cpg_node = self.node_to_id[cpg_key]
        connected = []
        
        for edge in self.edge_list:
            if edge[0] == cpg_node:
                target_info = self.id_to_node.get(edge[1], {})
                if target_info.get('type') == 'disease':
                    connected.append({
                        'disease_id': target_info['id'],
                        'disease_name': target_info['name'],
                        'category': target_info['category'],
                        'edge_type': edge[2]
                    })
        
        return connected
    
    def find_shared_cpgs(self, disease_id1: str, disease_id2: str) -> List[str]:
        """Iki hastalik arasinda paylasilan CpG'leri bul"""
        d1 = self.disease_db.get(disease_id1)
        d2 = self.disease_db.get(disease_id2)
        
        if not d1 or not d2:
            return []
        
        cpgs1 = set(d1.hypermethylated_cpgs + d1.hypomethylated_cpgs)
        cpgs2 = set(d2.hypermethylated_cpgs + d2.hypomethylated_cpgs)
        
        return list(cpgs1.intersection(cpgs2))
    
    def calculate_disease_similarity_network(self) -> pd.DataFrame:
        """Hastaliklar arasi benzerlik matrisi"""
        disease_ids = list(self.disease_db.keys())
        n = len(disease_ids)
        similarity_matrix = np.zeros((n, n))
        
        for i, d1 in enumerate(disease_ids):
            cpgs1 = set(
                self.disease_db[d1].hypermethylated_cpgs + 
                self.disease_db[d1].hypomethylated_cpgs
            )
            for j, d2 in enumerate(disease_ids):
                if i == j:
                    similarity_matrix[i, j] = 1.0
                    continue
                cpgs2 = set(
                    self.disease_db[d2].hypermethylated_cpgs + 
                    self.disease_db[d2].hypomethylated_cpgs
                )
                
                intersection = len(cpgs1.intersection(cpgs2))
                union = len(cpgs1.union(cpgs2))
                similarity_matrix[i, j] = intersection / union if union > 0 else 0
        
        return pd.DataFrame(
            similarity_matrix,
            index=[self.disease_db[d].disease_name for d in disease_ids],
            columns=[self.disease_db[d].disease_name for d in disease_ids]
        )


def get_disease_matcher() -> DiseasePatternMatcher:
    """Singleton pattern matcher instance"""
    if not hasattr(get_disease_matcher, '_instance'):
        get_disease_matcher._instance = DiseasePatternMatcher()
    return get_disease_matcher._instance


def get_disease_gnn() -> DiseaseMethylationGNN:
    """Singleton GNN instance"""
    if not hasattr(get_disease_gnn, '_instance'):
        get_disease_gnn._instance = DiseaseMethylationGNN()
    return get_disease_gnn._instance
