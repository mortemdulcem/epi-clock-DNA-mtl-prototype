# ============================================================================
# Illicit Manufacturing Detection System - Yasadisi Uretim Tespit Sistemi
# Copyright (c) 2024 Dr. Nurcan Denli Bayir (nrcdnl94)
# ============================================================================
"""
Yasadisi madde uretim yontemlerini tespit ve analiz eden modul.
Prekursor kimyasallar, sentez rotalari, safsizlik profilleri ve uretici imzalari.
"""

import pandas as pd
import numpy as np
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple
from datetime import datetime

# Prekursor Kimyasallar Veritabani
PRECURSOR_CHEMICALS = {
    "ephedrine": {
        "name": "Efedrin",
        "cas": "299-42-3",
        "formula": "C10H15NO",
        "mw": 165.23,
        "category": "Stimulan Prekursoru",
        "target_drugs": ["Metamfetamin", "Methcathinone"],
        "control_status": "BM Liste I",
        "detection_methods": ["GC-MS", "HPLC-UV", "TLC"],
        "typical_sources": ["Soguk alginligi ilaclari", "Yasadisi ithalat"],
        "conversion_yield": 0.65
    },
    "pseudoephedrine": {
        "name": "Psodoefedrin",
        "cas": "90-82-4",
        "formula": "C10H15NO",
        "mw": 165.23,
        "category": "Stimulan Prekursoru",
        "target_drugs": ["Metamfetamin"],
        "control_status": "BM Liste I",
        "detection_methods": ["GC-MS", "HPLC-UV"],
        "typical_sources": ["OTC ilaclari", "Yasadisi laboratuvarlar"],
        "conversion_yield": 0.60
    },
    "phenylacetic_acid": {
        "name": "Fenilasetik Asit",
        "cas": "103-82-2",
        "formula": "C8H8O2",
        "mw": 136.15,
        "category": "Stimulan Prekursoru",
        "target_drugs": ["Amfetamin", "Metamfetamin", "P2P"],
        "control_status": "BM Liste I",
        "detection_methods": ["GC-MS", "HPLC"],
        "typical_sources": ["Kimya endustrisi", "Yasadisi sentez"],
        "conversion_yield": 0.55
    },
    "acetic_anhydride": {
        "name": "Asetik Anhidrit",
        "cas": "108-24-7",
        "formula": "C4H6O3",
        "mw": 102.09,
        "category": "Opioid Prekursoru",
        "target_drugs": ["Eroin (Diasetilmorfin)"],
        "control_status": "BM Liste I",
        "detection_methods": ["GC-MS", "IR"],
        "typical_sources": ["Kimya endustrisi", "Kacakcilik"],
        "conversion_yield": 0.85
    },
    "ergotamine": {
        "name": "Ergotamin",
        "cas": "113-15-5",
        "formula": "C33H35N5O5",
        "mw": 581.66,
        "category": "Halusinojen Prekursoru",
        "target_drugs": ["LSD (Liserjik Asit Dietilamid)"],
        "control_status": "BM Liste I",
        "detection_methods": ["HPLC-MS", "GC-MS"],
        "typical_sources": ["Ilac endustrisi", "Ergot mantari"],
        "conversion_yield": 0.15
    },
    "lysergic_acid": {
        "name": "Liserjik Asit",
        "cas": "82-58-6",
        "formula": "C16H16N2O2",
        "mw": 268.31,
        "category": "Halusinojen Prekursoru",
        "target_drugs": ["LSD"],
        "control_status": "Kontrollu",
        "detection_methods": ["HPLC-MS", "GC-MS"],
        "typical_sources": ["Ergotamin donusumu"],
        "conversion_yield": 0.70
    },
    "piperonal": {
        "name": "Piperonal (Heliotropin)",
        "cas": "120-57-0",
        "formula": "C8H6O3",
        "mw": 150.13,
        "category": "Stimulan Prekursoru",
        "target_drugs": ["MDMA", "MDA"],
        "control_status": "BM Liste I",
        "detection_methods": ["GC-MS", "HPLC"],
        "typical_sources": ["Parfum endustrisi", "Yasadisi ithalat"],
        "conversion_yield": 0.45
    },
    "safrole": {
        "name": "Safrol",
        "cas": "94-59-7",
        "formula": "C10H10O2",
        "mw": 162.19,
        "category": "Stimulan Prekursoru",
        "target_drugs": ["MDMA", "MDA"],
        "control_status": "BM Liste I",
        "detection_methods": ["GC-MS", "GC-FID"],
        "typical_sources": ["Sassafras yagi", "Kamphor yagi"],
        "conversion_yield": 0.50
    },
    "potassium_permanganate": {
        "name": "Potasyum Permanganat",
        "cas": "7722-64-7",
        "formula": "KMnO4",
        "mw": 158.03,
        "category": "Kokain Isleme",
        "target_drugs": ["Kokain HCl"],
        "control_status": "BM Liste II",
        "detection_methods": ["UV-Vis", "Titrasyon"],
        "typical_sources": ["Kimya endustrisi", "Su aritma"],
        "conversion_yield": 0.90
    },
    "benzyl_cyanide": {
        "name": "Benzil Siyanur (Fenilasetonitril)",
        "cas": "140-29-4",
        "formula": "C8H7N",
        "mw": 117.15,
        "category": "Stimulan Prekursoru",
        "target_drugs": ["Amfetamin", "Metamfetamin"],
        "control_status": "BM Liste I",
        "detection_methods": ["GC-MS", "HPLC"],
        "typical_sources": ["Kimya endustrisi"],
        "conversion_yield": 0.60
    },
    "fentanyl_precursors": {
        "name": "NPP (N-Fenilpiperidin-4-on)",
        "cas": "39742-60-4",
        "formula": "C11H13NO",
        "mw": 175.23,
        "category": "Opioid Prekursoru",
        "target_drugs": ["Fentanil", "Karfentanil"],
        "control_status": "BM Liste I (2017)",
        "detection_methods": ["GC-MS", "LC-MS/MS"],
        "typical_sources": ["Cin", "Meksika"],
        "conversion_yield": 0.75
    },
    "anpp": {
        "name": "ANPP (4-Anilino-N-feniletilpiperidin)",
        "cas": "21409-26-7",
        "formula": "C19H24N2",
        "mw": 284.40,
        "category": "Opioid Prekursoru",
        "target_drugs": ["Fentanil"],
        "control_status": "BM Liste I (2017)",
        "detection_methods": ["GC-MS", "LC-MS/MS"],
        "typical_sources": ["NPP donusumu"],
        "conversion_yield": 0.80
    }
}

# Yasadisi Uretim Yontemleri
MANUFACTURING_METHODS = {
    "birch_reduction": {
        "name": "Birch Indirgemesi",
        "description": "Sivi amonyak ve alkali metal kullanarak efedrin/psodoefedrinden metamfetamin uretimi",
        "target_drug": "Metamfetamin",
        "precursors": ["Efedrin", "Psodoefedrin", "Lityum", "Amonyak"],
        "solvents": ["Sivi amonyak", "Eter"],
        "equipment": ["Sogutucu", "Cam reaktor", "Karıstirici"],
        "yield_range": (0.50, 0.70),
        "purity_range": (0.85, 0.95),
        "impurity_signature": ["Efedrin kalintisi", "Lityum izleri", "N-metil izomerleri"],
        "detection_markers": ["d-metamfetamin/l-metamfetamin orani", "Efedrin eser miktari"],
        "risk_level": "Yuksek (patlama riski)"
    },
    "red_phosphorus": {
        "name": "Kirmizi Fosfor Yontemi",
        "description": "Kirmizi fosfor ve hidroiyodik asit ile efedrin indirgenmesi",
        "target_drug": "Metamfetamin",
        "precursors": ["Efedrin", "Psodoefedrin", "Kirmizi fosfor", "Iyot"],
        "solvents": ["Su", "Aseton"],
        "equipment": ["Cam balon", "Kondenser", "Isitici"],
        "yield_range": (0.60, 0.80),
        "purity_range": (0.70, 0.90),
        "impurity_signature": ["Fosfor kalintisi", "Iyot izleri", "Klorlu bilesikler"],
        "detection_markers": ["Kirmizi fosfor partikuleri", "HI asit kalintisi"],
        "risk_level": "Cok yuksek (toksik gaz)"
    },
    "p2p_method": {
        "name": "P2P (Fenilaseton) Yontemi",
        "description": "Fenilasetondan reduktif aminasyon ile amfetamin/metamfetamin",
        "target_drug": "Amfetamin/Metamfetamin",
        "precursors": ["Fenilasetik asit", "Fenilaseton", "Metilalanin"],
        "solvents": ["Etanol", "Toluen", "Aseton"],
        "equipment": ["Distilasyon aparati", "Vakum pompasi", "Reaktor"],
        "yield_range": (0.40, 0.60),
        "purity_range": (0.60, 0.85),
        "impurity_signature": ["Rasemik karisim", "Fenilaseton kalintisi", "Aldehit urunleri"],
        "detection_markers": ["d/l-amfetamin 50:50 orani", "Benzaldehit izleri"],
        "risk_level": "Orta"
    },
    "cocaine_extraction": {
        "name": "Kokain Ekstraksiyonu",
        "description": "Koka yapraklarindan kokain alkaloid ekstraksiyonu",
        "target_drug": "Kokain",
        "precursors": ["Koka yapraklari", "Potasyum permanganat", "Amonyak"],
        "solvents": ["Kerosen", "Aseton", "Eter", "Hidroklorik asit"],
        "equipment": ["Ekstraksiyon tanki", "Separasyon hunisi", "Evaporator"],
        "yield_range": (0.005, 0.015),
        "purity_range": (0.80, 0.95),
        "impurity_signature": ["Tropakok alkaloidleri", "Benzoilekgonin", "Metilekgonin"],
        "detection_markers": ["Cis/trans-sinnamoilkokain", "Tropakokain"],
        "risk_level": "Orta"
    },
    "heroin_synthesis": {
        "name": "Eroin Sentezi",
        "description": "Morfinden asetik anhidrit ile diasetilmorfin (eroin) uretimi",
        "target_drug": "Eroin",
        "precursors": ["Morfin", "Asetik anhidrit"],
        "solvents": ["Kloroform", "Aseton", "Etanol"],
        "equipment": ["Cam reaktor", "Kondenser", "Filtrasyon sistemi"],
        "yield_range": (0.80, 0.95),
        "purity_range": (0.60, 0.90),
        "impurity_signature": ["6-MAM", "Asetilkodein", "Papaverin"],
        "detection_markers": ["6-Monoasetilmorfin (6-MAM)", "Asetik asit kalintisi"],
        "risk_level": "Yuksek"
    },
    "fentanyl_synthesis": {
        "name": "Fentanil Sentezi",
        "description": "NPP ve ANPP'den fentanil ve turevleri uretimi",
        "target_drug": "Fentanil",
        "precursors": ["NPP", "ANPP", "Propionil klorur"],
        "solvents": ["Diklorometan", "Aseton", "Etanol"],
        "equipment": ["Laboratuvar reaktoru", "Rotary evaporator", "HPLC"],
        "yield_range": (0.60, 0.80),
        "purity_range": (0.70, 0.95),
        "impurity_signature": ["ANPP kalintisi", "Despropionil fentanil", "Benzilfentanil"],
        "detection_markers": ["NPP/ANPP izleri", "Asetil fentanil kontaminasyonu"],
        "risk_level": "Kritik (olumcul dozlar)"
    },
    "mdma_synthesis": {
        "name": "MDMA Sentezi",
        "description": "Safrol veya piperonaldan MDMA uretimi",
        "target_drug": "MDMA",
        "precursors": ["Safrol", "Piperonal", "Metilamin"],
        "solvents": ["Aseton", "Izopropanol", "Eter"],
        "equipment": ["Reflux aparati", "Vakum distilasyon", "Kristalizor"],
        "yield_range": (0.35, 0.55),
        "purity_range": (0.75, 0.92),
        "impurity_signature": ["MDA", "MDEA", "Piperonal kalintisi", "Safrol izleri"],
        "detection_markers": ["MDA/MDMA orani", "Izosafrol metabolitleri"],
        "risk_level": "Orta"
    },
    "lsd_synthesis": {
        "name": "LSD Sentezi",
        "description": "Liserjik asitten LSD uretimi",
        "target_drug": "LSD",
        "precursors": ["Ergotamin", "Liserjik asit", "Dietilamin"],
        "solvents": ["Kloroform", "Metanol", "Piridin"],
        "equipment": ["Karanlik laboratuvar", "Vakum sistemi", "Kromatografi"],
        "yield_range": (0.10, 0.25),
        "purity_range": (0.85, 0.99),
        "impurity_signature": ["iso-LSD", "Liserjik asit kalintisi", "Ergotamin izleri"],
        "detection_markers": ["iso-LSD orani", "Ergotamin metabolitleri"],
        "risk_level": "Dusuk (kimyasal)"
    },
    "ghb_synthesis": {
        "name": "GHB Sentezi",
        "description": "GBL veya 1,4-butandiolden GHB donusumu",
        "target_drug": "GHB",
        "precursors": ["GBL (Gamma-butirolakton)", "1,4-Butandiol", "NaOH"],
        "solvents": ["Su", "Etanol"],
        "equipment": ["Basit mutfak malzemeleri", "pH metre"],
        "yield_range": (0.85, 0.95),
        "purity_range": (0.80, 0.95),
        "impurity_signature": ["GBL kalintisi", "1,4-BD izleri", "Sodyum tuzu"],
        "detection_markers": ["GBL/GHB orani", "pH degeri"],
        "risk_level": "Dusuk"
    }
}

# Safsizlik Imzalari ve Uretici Profilleri
IMPURITY_SIGNATURES = {
    "mexican_meth": {
        "origin": "Meksika Kartelleri",
        "drug": "Metamfetamin",
        "method": "P2P Super Lab",
        "characteristic_impurities": [
            {"name": "Benzaldehit", "range": (0.1, 0.5), "unit": "%"},
            {"name": "Fenilaseton", "range": (0.05, 0.2), "unit": "%"},
            {"name": "N-formil-metamfetamin", "range": (0.01, 0.1), "unit": "%"}
        ],
        "stereochemistry": "Rasemik (d/l 50:50)",
        "purity_range": (0.90, 0.99),
        "color": "Beyaz kristal",
        "signature_ratio": "Benzaldehit/Fenilaseton > 2.0"
    },
    "domestic_meth": {
        "origin": "Yerel Uretim (Kucuk Olcek)",
        "drug": "Metamfetamin",
        "method": "Kirmizi Fosfor / Birch",
        "characteristic_impurities": [
            {"name": "Efedrin/Psodoefedrin", "range": (0.5, 3.0), "unit": "%"},
            {"name": "Kloropsodoefedrin", "range": (0.1, 1.0), "unit": "%"},
            {"name": "Fosfor kalintisi", "range": (0.01, 0.1), "unit": "%"}
        ],
        "stereochemistry": "d-metamfetamin dominant (>95%)",
        "purity_range": (0.60, 0.85),
        "color": "Sari-kahverengi kristal",
        "signature_ratio": "Efedrin/Kloropsodoefedrin < 5.0"
    },
    "afghan_heroin": {
        "origin": "Afganistan",
        "drug": "Eroin",
        "method": "Geleneksel Asetilasyon",
        "characteristic_impurities": [
            {"name": "6-MAM", "range": (1.0, 5.0), "unit": "%"},
            {"name": "Asetilkodein", "range": (0.5, 3.0), "unit": "%"},
            {"name": "Papaverin", "range": (0.1, 1.0), "unit": "%"},
            {"name": "Noskapin", "range": (0.5, 2.0), "unit": "%"}
        ],
        "stereochemistry": "Dogal konfigrasyon",
        "purity_range": (0.40, 0.70),
        "color": "Kahverengi toz (Brown Sugar)",
        "signature_ratio": "Asetilkodein/Papaverin 2-4"
    },
    "colombian_cocaine": {
        "origin": "Kolombiya",
        "drug": "Kokain HCl",
        "method": "Asit-Baz Ekstraksiyon",
        "characteristic_impurities": [
            {"name": "Benzoilekgonin", "range": (0.1, 0.5), "unit": "%"},
            {"name": "Metilekgonin", "range": (0.05, 0.3), "unit": "%"},
            {"name": "Cis-sinnamoilkokain", "range": (0.1, 0.8), "unit": "%"},
            {"name": "Trans-sinnamoilkokain", "range": (0.05, 0.4), "unit": "%"}
        ],
        "stereochemistry": "Dogal (-) konfigrasyon",
        "purity_range": (0.80, 0.95),
        "color": "Beyaz kristal pul",
        "signature_ratio": "Cis/Trans sinnamoilkokain 1.5-2.5"
    },
    "chinese_fentanyl": {
        "origin": "Cin (Yasadisi Laboratuvarlar)",
        "drug": "Fentanil",
        "method": "Kimyasal Sentez",
        "characteristic_impurities": [
            {"name": "ANPP", "range": (0.01, 0.5), "unit": "%"},
            {"name": "Despropionil fentanil", "range": (0.05, 0.3), "unit": "%"},
            {"name": "Asetil fentanil", "range": (0.1, 1.0), "unit": "%"},
            {"name": "Benzilfentanil", "range": (0.01, 0.2), "unit": "%"}
        ],
        "stereochemistry": "Rasemik veya enantiyomerik olarak zenginlestirilmis",
        "purity_range": (0.70, 0.95),
        "color": "Beyaz-krem toz",
        "signature_ratio": "ANPP/Despropionil < 0.5"
    },
    "dutch_mdma": {
        "origin": "Hollanda",
        "drug": "MDMA",
        "method": "PMK Glidat Yontemi",
        "characteristic_impurities": [
            {"name": "MDA", "range": (0.5, 3.0), "unit": "%"},
            {"name": "MDEA", "range": (0.1, 0.5), "unit": "%"},
            {"name": "Piperonal", "range": (0.05, 0.3), "unit": "%"},
            {"name": "PMK glidat kalintisi", "range": (0.01, 0.1), "unit": "%"}
        ],
        "stereochemistry": "Rasemik",
        "purity_range": (0.80, 0.95),
        "color": "Beyaz-krem kristal",
        "signature_ratio": "MDA/MDEA > 5.0"
    }
}

# Analitik Tespit Yontemleri
DETECTION_METHODS = {
    "gc_ms": {
        "name": "GC-MS (Gaz Kromatografisi-Kutle Spektrometrisi)",
        "principle": "Ucucu bilesiklerin gaz fazinda ayrilmasi ve kutle analizi",
        "applications": ["Amfetaminler", "Metamfetamin", "Kannabinoidler", "Opioidler"],
        "detection_limit": "ng/mL",
        "advantages": ["Yuksek secicilik", "Kutuphane eslestirme", "Kantitatif"],
        "sample_prep": ["Sivi-sivi ekstraksiyon", "SPE", "Derivatizasyon"],
        "run_time": "15-30 dakika"
    },
    "lc_ms_ms": {
        "name": "LC-MS/MS (Sivi Kromatografisi-Tandem Kutle Spektrometrisi)",
        "principle": "Sivi fazda ayirma ve coklu kutle analizi",
        "applications": ["Fentanil analoglari", "NPS", "Peptidler", "Polar bilesikler"],
        "detection_limit": "pg/mL",
        "advantages": ["En yuksek duyarlilik", "Termal kararsiz bilesikler", "Hizli"],
        "sample_prep": ["Protein cokturmesi", "SPE", "Direkt enjeksiyon"],
        "run_time": "5-15 dakika"
    },
    "ftir": {
        "name": "FTIR (Fourier Donusum Infrared Spektroskopisi)",
        "principle": "Molekuler titresim modlarinin olcumu",
        "applications": ["Bulk madde tanimlamasi", "Kesici madde tespiti"],
        "detection_limit": "%",
        "advantages": ["Hizli tarama", "Tahribatsiz", "Portatif cihazlar"],
        "sample_prep": ["ATR direkt olcum", "KBr pellet"],
        "run_time": "1-5 dakika"
    },
    "raman": {
        "name": "Raman Spektroskopisi",
        "principle": "Raman sacilimi ile molekuler parmak izi",
        "applications": ["Saha tespiti", "Paket ici tarama", "Polimorf analizi"],
        "detection_limit": "%",
        "advantages": ["Tahribatsiz", "Cam/plastik uzerinden olcum", "Portatif"],
        "sample_prep": ["Hazirlama gerektirmez"],
        "run_time": "Saniyeler"
    },
    "nmr": {
        "name": "NMR (Nukleer Manyetik Rezonans)",
        "principle": "Nukleer spin gecisleri ile yapisal analiz",
        "applications": ["Yapisal aydinlatma", "Izomer ayirimi", "Safsizlik profili"],
        "detection_limit": "ug",
        "advantages": ["Kesin yapi tayini", "Kantitatif", "Stereokimya"],
        "sample_prep": ["Cozuculerde cozme"],
        "run_time": "30-120 dakika"
    },
    "hplc_uv": {
        "name": "HPLC-UV/DAD",
        "principle": "Sivi kromatografisi ile UV absorpsiyon dedeksiyonu",
        "applications": ["Safsizlik profilleme", "Kalite kontrolu"],
        "detection_limit": "ug/mL",
        "advantages": ["Robust", "Dusuk maliyet", "Rutin analiz"],
        "sample_prep": ["Seyrelme", "Filtrasyon"],
        "run_time": "10-30 dakika"
    }
}

# Sentez Rota Veritabani
SYNTHESIS_ROUTES = {
    "meth_from_ephedrine": {
        "name": "Efedrin -> Metamfetamin",
        "steps": [
            {"step": 1, "reaction": "Hidroksil grubunun indirgenmesi", "reagents": ["HI", "Kirmizi P"], "conditions": "Reflux, 2-4 saat"},
            {"step": 2, "reaction": "Notralizasyon", "reagents": ["NaOH", "NaHCO3"], "conditions": "pH 10-12"},
            {"step": 3, "reaction": "Ekstraksiyon", "reagents": ["Toluen", "Eter"], "conditions": "Oda sicakligi"},
            {"step": 4, "reaction": "Tuz olusumu", "reagents": ["HCl gazi", "Aseton"], "conditions": "Soguk"}
        ],
        "overall_yield": 0.65,
        "critical_impurities": ["Efedrin", "Kloropsodoefedrin", "HI kalintisi"]
    },
    "meth_from_p2p": {
        "name": "P2P -> Metamfetamin",
        "steps": [
            {"step": 1, "reaction": "Reduktif aminasyon", "reagents": ["Metilamin", "Al/Hg"], "conditions": "Oda sicakligi, 24 saat"},
            {"step": 2, "reaction": "Hidroliz", "reagents": ["NaOH"], "conditions": "Isitma"},
            {"step": 3, "reaction": "Ekstraksiyon", "reagents": ["Eter"], "conditions": "Coklu ekstraksiyon"},
            {"step": 4, "reaction": "Tuz olusumu", "reagents": ["HCl"], "conditions": "Soguk kristalizasyon"}
        ],
        "overall_yield": 0.50,
        "critical_impurities": ["Fenilaseton", "Benzaldehit", "Aluminyum"]
    },
    "heroin_from_morphine": {
        "name": "Morfin -> Eroin",
        "steps": [
            {"step": 1, "reaction": "O-asetilasyon", "reagents": ["Asetik anhidrit"], "conditions": "85C, 2-4 saat"},
            {"step": 2, "reaction": "Notralizasyon", "reagents": ["Na2CO3", "NH4OH"], "conditions": "pH 8-9"},
            {"step": 3, "reaction": "Cokturme", "reagents": ["Su"], "conditions": "Sogutma"},
            {"step": 4, "reaction": "Saflaştirma", "reagents": ["Aseton", "Etanol"], "conditions": "Yeniden kristalizasyon"}
        ],
        "overall_yield": 0.85,
        "critical_impurities": ["6-MAM", "Asetilkodein", "Morfin kalintisi"]
    },
    "cocaine_extraction": {
        "name": "Koka Yapragi -> Kokain",
        "steps": [
            {"step": 1, "reaction": "Alkali ekstraksiyon", "reagents": ["Na2CO3", "Kerosen"], "conditions": "Islatma, karistirma"},
            {"step": 2, "reaction": "Asit ekstraksiyonu", "reagents": ["H2SO4 seyreltik"], "conditions": "Ayirma hunisi"},
            {"step": 3, "reaction": "Baz cokturme", "reagents": ["NH4OH", "KMnO4"], "conditions": "pH 10"},
            {"step": 4, "reaction": "Tuz olusumu", "reagents": ["HCl", "Aseton"], "conditions": "Kristalizasyon"}
        ],
        "overall_yield": 0.01,
        "critical_impurities": ["Benzoilekgonin", "Tropakok alkaloidleri", "Solvent kalintilari"]
    },
    "fentanyl_synthesis": {
        "name": "NPP -> Fentanil",
        "steps": [
            {"step": 1, "reaction": "Anilin kondensasyonu", "reagents": ["Anilin", "NaBH3CN"], "conditions": "Reflux"},
            {"step": 2, "reaction": "N-alkilasyon", "reagents": ["2-feniletil bromur"], "conditions": "K2CO3, DMF"},
            {"step": 3, "reaction": "Asilasyon", "reagents": ["Propionil klorur", "Et3N"], "conditions": "0C, DCM"},
            {"step": 4, "reaction": "Saflaştirma", "reagents": ["Kolon kromatografisi"], "conditions": "Silika jel"}
        ],
        "overall_yield": 0.60,
        "critical_impurities": ["ANPP", "NPP", "Despropionil fentanil"]
    }
}


@dataclass
class ManufacturingAnalysisResult:
    """Uretim analizi sonuc sinifi"""
    detected_method: str
    confidence: float
    precursors_detected: List[str]
    impurity_profile: Dict[str, float]
    origin_estimate: str
    synthesis_route: str
    risk_assessment: str
    recommendations: List[str]


class IllicitManufacturingDetector:
    """Yasadisi uretim tespit ve analiz sinifi"""
    
    def __init__(self):
        self.precursors = PRECURSOR_CHEMICALS
        self.methods = MANUFACTURING_METHODS
        self.signatures = IMPURITY_SIGNATURES
        self.detection_methods = DETECTION_METHODS
        self.synthesis_routes = SYNTHESIS_ROUTES
    
    def analyze_impurity_profile(self, impurities: Dict[str, float], drug_type: str) -> ManufacturingAnalysisResult:
        """Safsizlik profilinden uretim yontemi ve kaynak tahmini"""
        
        best_match = None
        best_score = 0
        
        for sig_id, signature in self.signatures.items():
            if drug_type.lower() in signature['drug'].lower():
                score = self._calculate_signature_match(impurities, signature)
                if score > best_score:
                    best_score = score
                    best_match = sig_id
        
        if best_match:
            sig = self.signatures[best_match]
            return ManufacturingAnalysisResult(
                detected_method=sig['method'],
                confidence=best_score,
                precursors_detected=list(impurities.keys()),
                impurity_profile=impurities,
                origin_estimate=sig['origin'],
                synthesis_route=sig['method'],
                risk_assessment=self._assess_risk(impurities),
                recommendations=self._generate_recommendations(sig, impurities)
            )
        
        return ManufacturingAnalysisResult(
            detected_method="Bilinmiyor",
            confidence=0.0,
            precursors_detected=list(impurities.keys()),
            impurity_profile=impurities,
            origin_estimate="Belirlenemedi",
            synthesis_route="Belirlenemedi",
            risk_assessment="Veri yetersiz",
            recommendations=["Ek analiz gerekli", "LC-MS/MS ile detayli profilleme onerilir"]
        )
    
    def _calculate_signature_match(self, impurities: Dict[str, float], signature: Dict) -> float:
        """Safsizlik profili eslestirme skoru hesapla"""
        total_score = 0
        matched = 0
        
        for char_imp in signature['characteristic_impurities']:
            imp_name = char_imp['name'].lower()
            for detected, value in impurities.items():
                if imp_name in detected.lower():
                    min_val, max_val = char_imp['range']
                    if min_val <= value <= max_val:
                        total_score += 1.0
                    else:
                        total_score += 0.5
                    matched += 1
                    break
        
        if len(signature['characteristic_impurities']) > 0:
            return total_score / len(signature['characteristic_impurities'])
        return 0.0
    
    def _assess_risk(self, impurities: Dict[str, float]) -> str:
        """Risk degerlendirmesi"""
        high_risk_markers = ['fentanil', 'karfentanil', 'anpp', 'npp']
        
        for imp in impurities.keys():
            if any(marker in imp.lower() for marker in high_risk_markers):
                return "KRITIK - Olumcul doz riski"
        
        total_impurity = sum(impurities.values())
        if total_impurity > 10:
            return "Yuksek - Ciddi safsizlik kontaminasyonu"
        elif total_impurity > 5:
            return "Orta - Onemli safsizlik seviyeleri"
        else:
            return "Dusuk - Standart safsizlik profili"
    
    def _generate_recommendations(self, signature: Dict, impurities: Dict) -> List[str]:
        """Oneriler olustur"""
        recs = []
        
        recs.append(f"Tahmini kaynak: {signature['origin']}")
        recs.append(f"Uretim yontemi: {signature['method']}")
        
        if signature['purity_range'][0] > 0.85:
            recs.append("Yuksek safiyet - Profesyonel uretim tesisi muhtemel")
        else:
            recs.append("Dusuk safiyet - Kucuk olcekli/amatör uretim muhtemel")
        
        recs.append("Kolluk kuvvetleri ile istihbarat paylasimi onerilir")
        
        return recs
    
    def get_precursor_info(self, precursor_id: str) -> Optional[Dict]:
        """Prekursor bilgisi getir"""
        return self.precursors.get(precursor_id)
    
    def get_method_info(self, method_id: str) -> Optional[Dict]:
        """Uretim yontemi bilgisi getir"""
        return self.methods.get(method_id)
    
    def get_synthesis_route(self, route_id: str) -> Optional[Dict]:
        """Sentez rotasi bilgisi getir"""
        return self.synthesis_routes.get(route_id)
    
    def search_by_drug(self, drug_name: str) -> List[Dict]:
        """Maddeye gore arama"""
        results = []
        
        for prec_id, prec in self.precursors.items():
            if drug_name.lower() in [d.lower() for d in prec['target_drugs']]:
                results.append({"type": "precursor", "id": prec_id, "data": prec})
        
        for method_id, method in self.methods.items():
            if drug_name.lower() in method['target_drug'].lower():
                results.append({"type": "method", "id": method_id, "data": method})
        
        return results
    
    def get_detection_method_recommendation(self, drug_type: str, sample_type: str) -> List[str]:
        """Tespit yontemi onerisi"""
        recommendations = []
        
        if "fentanil" in drug_type.lower():
            recommendations.append("LC-MS/MS (en yuksek duyarlilik)")
            recommendations.append("Immunoassay tarama (hizli)")
        elif "metamfetamin" in drug_type.lower() or "amfetamin" in drug_type.lower():
            recommendations.append("GC-MS (altin standart)")
            recommendations.append("Kiral analiz (stereokimya)")
        elif "kokain" in drug_type.lower():
            recommendations.append("GC-MS")
            recommendations.append("HPLC-UV (safsizlik profili)")
        elif "eroin" in drug_type.lower():
            recommendations.append("GC-MS")
            recommendations.append("6-MAM tespiti icin LC-MS")
        else:
            recommendations.append("FTIR (hizli tarama)")
            recommendations.append("GC-MS (teyit)")
            recommendations.append("LC-MS/MS (NPS)")
        
        return recommendations


def get_manufacturing_statistics() -> Dict:
    """Istatistikler"""
    return {
        "total_precursors": len(PRECURSOR_CHEMICALS),
        "total_methods": len(MANUFACTURING_METHODS),
        "total_signatures": len(IMPURITY_SIGNATURES),
        "total_detection_methods": len(DETECTION_METHODS),
        "total_synthesis_routes": len(SYNTHESIS_ROUTES)
    }


def get_precursor_dataframe() -> pd.DataFrame:
    """Prekursor veritabanini DataFrame olarak getir"""
    data = []
    for prec_id, prec in PRECURSOR_CHEMICALS.items():
        data.append({
            "ID": prec_id,
            "Kimyasal": prec['name'],
            "CAS No": prec['cas'],
            "Formul": prec['formula'],
            "MW": prec['mw'],
            "Kategori": prec['category'],
            "Hedef Maddeler": ", ".join(prec['target_drugs']),
            "Kontrol Durumu": prec['control_status'],
            "Verim": f"{prec['conversion_yield']*100:.0f}%"
        })
    return pd.DataFrame(data)


def get_methods_dataframe() -> pd.DataFrame:
    """Uretim yontemlerini DataFrame olarak getir"""
    data = []
    for method_id, method in MANUFACTURING_METHODS.items():
        data.append({
            "ID": method_id,
            "Yontem": method['name'],
            "Hedef Madde": method['target_drug'],
            "Prekursorler": ", ".join(method['precursors'][:3]) + ("..." if len(method['precursors']) > 3 else ""),
            "Verim Araligi": f"{method['yield_range'][0]*100:.0f}-{method['yield_range'][1]*100:.0f}%",
            "Safiyet": f"{method['purity_range'][0]*100:.0f}-{method['purity_range'][1]*100:.0f}%",
            "Risk": method['risk_level']
        })
    return pd.DataFrame(data)


def get_signatures_dataframe() -> pd.DataFrame:
    """Safsizlik imzalarini DataFrame olarak getir"""
    data = []
    for sig_id, sig in IMPURITY_SIGNATURES.items():
        data.append({
            "ID": sig_id,
            "Kaynak": sig['origin'],
            "Madde": sig['drug'],
            "Yontem": sig['method'],
            "Safiyet": f"{sig['purity_range'][0]*100:.0f}-{sig['purity_range'][1]*100:.0f}%",
            "Stereokimya": sig['stereochemistry'],
            "Goruntu": sig['color'],
            "Imza Orani": sig['signature_ratio']
        })
    return pd.DataFrame(data)


# End of module - nrcdnl94
