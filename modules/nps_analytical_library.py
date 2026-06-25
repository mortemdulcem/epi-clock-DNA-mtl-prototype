"""
NPS Analitik Referans Kütüphanesi — GC-MS / LC-MS/MS / LC-HRMS
EpiClock — Madde Kimya katmanının analitik tespit genişlemesi

AMAÇ
----
Bilinmeyen Yeni Psikoaktif Madde (NPS) türevlerinin GC-MS, LC-MS/MS ve
LC-HRMS ile tanımlanması için *referans kütüphanesi hazırlama* sürecini,
mevcut spektral kütüphane kataloğunu, in-silico tahmin araçlarını,
moleküler ağ yaklaşımlarını, Schymanski güven düzeylerini ve ISO 17025
validasyon çerçevesini kodlar.

BİLİMSEL DÜRÜSTLÜK (Zero-Hallucination)
---------------------------------------
1. KATALOG/ÇERÇEVE VERİSİ (kütüphaneler, tedarikçiler, in-silico araçlar,
   iş akışı, Schymanski düzeyleri, ISO 17025 parametreleri, MRM tasarım
   kuralları) doğrudan kullanıcının sağladığı kaynak dokümandan
   alınmıştır:
   "Bilinmeyen NPS Türevlerinin LC-MS/MS ve GC-MS ile Analizi İçin
   Referans Kütüphanesi Hazırlama Süreci" (attached_assets, 2026).
   Bu metni `SOURCE_DOC` olarak attribute ediyoruz.

2. HESAPLANAN VERİ: Bir bileşiğin öncü/addukt m/z değerleri molekül
   formülünden IUPAC monoizotopik kütlelerle DETERMİNİSTİK olarak
   hesaplanır (reprodüklenebilir). Bu gerçek kimyadır, uydurma değildir.

3. KESİNLİKLE ÜRETİLMEYEN: Belirli bir bileşiğe ait DENEYSEL MRM
   geçişleri, EI fragман spektrumları veya retansiyon indeksleri bu
   modülde UYDURULMAZ. Bunlar gerçek cihaz verisi veya in-silico tahmin
   (CFM-ID / NPS-MS) gerektirir; modül yalnızca bunların nasıl elde
   edileceğini (kural + araç) tarif eder, sahte sayı vermez.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Dict, List, Optional

SOURCE_DOC = (
    "Bilinmeyen NPS Türevlerinin LC-MS/MS ve GC-MS ile Analizi İçin "
    "Referans Kütüphanesi Hazırlama Süreci (kullanıcı sağladı, 2026)"
)

# ---------------------------------------------------------------------------
# 1. MONOİZOTOPİK KÜTLE & ADDUKT m/z HESABI (gerçek, deterministik)
# ---------------------------------------------------------------------------
# Kaynak: CODATA / IUPAC en bol izotop monoizotopik kütleleri (Da).
MONOISOTOPIC_MASS: Dict[str, float] = {
    "H": 1.0078250319, "D": 2.0141017779,
    "C": 12.0000000000, "N": 14.0030740052, "O": 15.9949146221,
    "F": 18.9984031627, "Na": 22.9897692820, "Mg": 23.9850417,
    "Si": 27.9769265327, "P": 30.9737615120, "S": 31.9720706912,
    "Cl": 34.9688527100, "K": 38.9637069, "Br": 78.9183376000,
    "I": 126.9044730000,
}

# Tek yüklü iyon hesabı için temel sabitler (Da)
_PROTON = 1.0072764669      # H+ (proton) kütlesi
_ELECTRON = 0.000548579909
_NA_CATION = MONOISOTOPIC_MASS["Na"] - _ELECTRON          # [Na]+
_NH4_CATION = (MONOISOTOPIC_MASS["N"] + 4 * MONOISOTOPIC_MASS["H"]
               - _ELECTRON)                               # [NH4]+

_FORMULA_TOKEN = re.compile(r"([A-Z][a-z]?)(\d*)")


def parse_formula(formula: str) -> Dict[str, int]:
    """Molekül formülünü element->sayı sözlüğüne çevirir. (Parantez yok;
    NPS düz formülleri için yeterli.) Bilinmeyen element ValueError verir."""
    formula = (formula or "").replace(" ", "")
    if not formula:
        raise ValueError("Boş formül")
    counts: Dict[str, int] = {}
    pos = 0
    for m in _FORMULA_TOKEN.finditer(formula):
        if m.start() != pos:
            raise ValueError(f"Formül çözümlenemedi: {formula!r}")
        pos = m.end()
        el, num = m.group(1), m.group(2)
        if el not in MONOISOTOPIC_MASS:
            raise ValueError(f"Bilinmeyen element: {el} ({formula})")
        counts[el] = counts.get(el, 0) + (int(num) if num else 1)
    if pos != len(formula):
        raise ValueError(f"Formül çözümlenemedi: {formula!r}")
    return counts


def monoisotopic_mass(formula: str) -> float:
    """Nötr molekülün monoizotopik kütlesi (Da) — hesaplanır."""
    counts = parse_formula(formula)
    return round(sum(MONOISOTOPIC_MASS[el] * n for el, n in counts.items()), 5)


def adduct_mz(formula: str) -> Dict[str, float]:
    """Sık kullanılan tek yüklü addukt m/z değerleri (hesaplanır).
    Kaynak doküman: pozitif ESI'de çoğunlukla [M+H]+ kullanılır; [M+Na]+
    ve [M+NH4]+ daha yüksek duyarlılık verebilir ancak fragmentasyonu
    güçleştirir."""
    m = monoisotopic_mass(formula)
    return {
        "[M+H]+": round(m + _PROTON, 5),
        "[M+Na]+": round(m + _NA_CATION, 5),
        "[M+NH4]+": round(m + _NH4_CATION, 5),
        "[M-H]-": round(m - _PROTON, 5),
    }


# ---------------------------------------------------------------------------
# 2. MEVCUT SPEKTRAL KÜTÜPHANE KATALOĞU (kaynak doküman §6)
# ---------------------------------------------------------------------------
@dataclass
class ReferenceLibrary:
    name: str
    technique: str
    compound_count: str
    access: str
    features: str
    url: str = ""


REFERENCE_LIBRARIES: List[ReferenceLibrary] = [
    ReferenceLibrary(
        "NIST/EPA/NIH 2026", "GC-MS EI", "350.000+", "Ücretli",
        "Genel amaçlı, en kapsamlı EI spektral kütüphanesi",
        "https://www.nist.gov/srd"),
    ReferenceLibrary(
        "SWGDRUG", "GC-MS EI", "3.598", "Ücretsiz",
        "Adli odaklı, yüksek kalite; topluluk katkısına açık",
        "https://www.swgdrug.org/ms.htm"),
    ReferenceLibrary(
        "Cayman Spectral Library", "GC-MS EI", "2.750+", "Ücretsiz/topluluk",
        "NPS odaklı; CRM tedarikçisiyle eşleşik",
        "https://www.caymanchem.com/forensics/publications/csl"),
    ReferenceLibrary(
        "HighResNPS (TIAFT)", "LC-HRMS", "2.394 NPS / 1.776 ürün iyonu",
        "Ücretsiz / kalabalık-kaynaklı",
        "Aylık güncellenir; Agilent/Sciex/Bruker/Waters/Thermo/Shimadzu "
        "formatları; konsensüs fragment iyonları (frekans+yoğunluk)",
        "https://highresnps.com"),
    ReferenceLibrary(
        "NPS Data Hub (NIST)", "GC-MS / LC-MS/MS (çok teknikli)",
        "Topluluk deposu", "Ücretsiz",
        "Spektral veri paylaşımı + akran değerlendirmesi",
        "https://nps-datahub.nist.gov"),
    ReferenceLibrary(
        "GNPS", "LC-MS/MS (moleküler ağ)", "Açık depo", "Açık erişim",
        "MS/MS yükle → moleküler ağ; fentanil/sentetik kannabinoid uyg.",
        "https://gnps.ucsd.edu"),
]


# ---------------------------------------------------------------------------
# 3. SERTİFİKALI REFERANS STANDART TEDARİKÇİLERİ (kaynak doküman §3.2)
# ---------------------------------------------------------------------------
@dataclass
class StandardSupplier:
    name: str
    product_type: str
    features: str


STANDARD_SUPPLIERS: List[StandardSupplier] = [
    StandardSupplier("Cayman Chemical", "CRM çözeltileri, toz, iç standartlar",
                     "2.750+ GC-MS spektral kütüphanesi, NPS odaklı"),
    StandardSupplier("Cerilliant (Sigma-Aldrich)", "CRM çözeltileri, metabolitler",
                     "2.800+ katalog ürünü, DEA akreditasyonu"),
    StandardSupplier("LGC Group", "CRM çözeltileri, döteryum etiketli",
                     "Avrupa odaklı, geniş NPS yelpazesi"),
    StandardSupplier("NIST SRM", "Sertifikalı referans materyaller",
                     "Metrolojik düzeyde doğruluk"),
]


# ---------------------------------------------------------------------------
# 4. TEKNİK KARŞILAŞTIRMASI (kaynak doküman §2)
# ---------------------------------------------------------------------------
TECHNIQUE_COMPARISON: List[Dict[str, str]] = [
    {"Özellik": "Kütüphane kapsamı", "GC-MS (EI)": "Çok geniş (NIST 350.000+)",
     "LC-MS/MS (QQQ)": "Hedef bazlı (MRM listesi)",
     "LC-HRMS (QTOF/Orbitrap)": "Şüpheli/hedefsiz tarama"},
    {"Özellik": "İzomer ayrımı", "GC-MS (EI)": "Zor (derivatizasyon gerekir)",
     "LC-MS/MS (QQQ)": "Kromatografi ile mümkün",
     "LC-HRMS (QTOF/Orbitrap)": "Kesin kütle + RT"},
    {"Özellik": "Duyarlılık", "GC-MS (EI)": "Orta",
     "LC-MS/MS (QQQ)": "Yüksek", "LC-HRMS (QTOF/Orbitrap)": "Orta-yüksek"},
    {"Özellik": "Termal kararsız bileşikler", "GC-MS (EI)": "Uygun değil",
     "LC-MS/MS (QQQ)": "Uygun", "LC-HRMS (QTOF/Orbitrap)": "Uygun"},
    {"Özellik": "Retrospektif analiz", "GC-MS (EI)": "Sınırlı",
     "LC-MS/MS (QQQ)": "Hayır", "LC-HRMS (QTOF/Orbitrap)": "Evet (tam tarama)"},
    {"Özellik": "Bilinmeyen tanımlama", "GC-MS (EI)": "Kütüphane eşleşmesi",
     "LC-MS/MS (QQQ)": "Hayır", "LC-HRMS (QTOF/Orbitrap)": "In silico + MN"},
    {"Özellik": "Akreditasyon kolaylığı", "GC-MS (EI)": "Yüksek",
     "LC-MS/MS (QQQ)": "Yüksek", "LC-HRMS (QTOF/Orbitrap)": "Orta"},
]


# ---------------------------------------------------------------------------
# 5. IN-SILICO TAHMİN ARAÇLARI (kaynak doküman §4)
# ---------------------------------------------------------------------------
@dataclass
class InSilicoTool:
    name: str
    approach: str
    use_case: str
    note: str = ""


IN_SILICO_TOOLS: List[InSilicoTool] = [
    InSilicoTool("CFM-ID", "Rekabetçi fragmentasyon modellemesi (ML)",
                 "EI-MS ve ESI-MS/MS spektrum tahmini",
                 "Yapıdan olası fragmentasyon yollarını modeller"),
    InSilicoTool("SIRIUS + CSI:FingerID", "Formül + parmak izi tabanlı yapı",
                 "Kesin kütle/izotoptan formül; HRMS MS/MS'ten yapı tahmini"),
    InSilicoTool("NPS-MS (Wang ve ark., 2023)", "Derin öğrenme + transfer öğr.",
                 "Yalnızca kimyasal yapıdan ESI-QTOF MS/MS tahmini",
                 "DarkNPS: 8,7M tahmini bileşik / 24,5M spektrum; "
                 "referans standartsız PCP türevi tanımlama örneği"),
    InSilicoTool("PS2MS", "Derin öğrenme",
                 "EI-MS spektrumundan NPS yapı tahmini",
                 "Bilinen+tahmini NPS türevlerine karşı eşleştirme"),
    InSilicoTool("NORMAN in-silico kütüphanesi", "LC-ESI-HRMS/MS fragmentasyon",
                 "120.514 kimyasal — 'karanlık kimyasal uzay' taraması",
                 "Çevresel + gıda güvenliği + adli"),
]


# ---------------------------------------------------------------------------
# 6. MOLEKÜLER AĞ YAKLAŞIMLARI (kaynak doküman §5)
# ---------------------------------------------------------------------------
@dataclass
class NetworkingApproach:
    name: str
    principle: str
    application: str


MOLECULAR_NETWORKING: List[NetworkingApproach] = [
    NetworkingApproach(
        "GNPS (Global Natural Products Social)",
        "Düğüm = iyon+MS/MS; kenar = spektral benzerlik; benzer "
        "fragmentasyon → aynı küme → sınıf düzeyi tanımlama",
        "Fentanil türevleri, sentetik kannabinoidler"),
    NetworkingApproach(
        "ABMN — Anchor-Based MN (Fournié ve ark., 2025)",
        "122 bileşiklik referans karışımı (Mix122) ile referans ağa klinik "
        "örnek entegrasyonu; P1 protokolü 50/5/0,5 ng/mL'de %100/%97/%42 "
        "MS/MS alımı",
        "Bromazolam, florometamfetamin, MDPHP gibi yapısal analoglar"),
    NetworkingApproach(
        "Entegre GC-EI-HRMS + LC-ESI-HRMS (Magny ve ark., 2026)",
        "GC tespitleri LC ağında 'çapa (anchor)' düğümü; iki platformun "
        "tamamlayıcı gücü (EI kütüphane eşleşmesi + öncü iyon/CID/Faz II)",
        "Arilcyclohexylamine ve cathinone ailesi zehirlenme vakaları"),
]


# ---------------------------------------------------------------------------
# 7. REFERANS KÜTÜPHANESİ HAZIRLAMA İŞ AKIŞI (kaynak doküman akış şeması)
# ---------------------------------------------------------------------------
WORKFLOW_STAGES: List[Dict[str, str]] = [
    {"Aşama": "1", "Adım": "NPS tehdidinin belirlenmesi",
     "Kaynak/Araç": "UNODC EWS, EMCDDA, Interpol, CFSRE (3 aylık), NFLIS"},
    {"Aşama": "2", "Adım": "Referans standart temini",
     "Kaynak/Araç": "Cayman, Cerilliant, LGC, NIST SRM; CRM yoksa 1 mg/mL "
                    "metanol; döteryum/¹³C iç standart"},
    {"Aşama": "3", "Adım": "Tekniğe özgü spektral veri + optimizasyon",
     "Kaynak/Araç": "GC-MS EI 70 eV + RI (Kovats/Lee); LC-MS/MS MRM; LC-HRMS"},
    {"Aşama": "4", "Adım": "Standart yoksa in-silico tahmin",
     "Kaynak/Araç": "CFM-ID / SIRIUS+CSI:FingerID / NPS-MS / PS2MS"},
    {"Aşama": "5", "Adım": "Moleküler ağ (bilinmeyen türevler)",
     "Kaynak/Araç": "GNPS / ABMN / FBMN; GC-HRMS + LC-HRMS entegrasyonu"},
    {"Aşama": "6", "Adım": "Tanımlama ve güven düzeyi atama",
     "Kaynak/Araç": "Schymanski Düzey 1–5"},
    {"Aşama": "7", "Adım": "Validasyon",
     "Kaynak/Araç": "ISO 17025:2017 — LOD/LOQ, doğruluk, seçicilik, iyon oranı"},
    {"Aşama": "8", "Adım": "Rutin tarama + sürekli güncelleme",
     "Kaynak/Araç": "Aylık kütüphane güncellemeleri, retrospektif DIA sorgu"},
]


# ---------------------------------------------------------------------------
# 8. SCHYMANSKI GÜVEN DÜZEYLERİ (kaynak doküman — tanımlama çerçevesi)
# ---------------------------------------------------------------------------
SCHYMANSKI_LEVELS: List[Dict[str, str]] = [
    {"Düzey": "1", "Tanım": "Doğrulanmış yapı",
     "Kanıt": "Referans standart ile eşleşme (RT + MS + MS/MS)"},
    {"Düzey": "2", "Tanım": "Olası yapı",
     "Kanıt": "Kütüphane eşleşmesi / tanısal kanıt (standart yok)"},
    {"Düzey": "3", "Tanım": "Geçici aday(lar)",
     "Kanıt": "Olası yapı(lar) önerilebilir ancak ayrım yapılamaz"},
    {"Düzey": "4", "Tanım": "Kesin molekül formülü",
     "Kanıt": "Kesin kütle + izotop deseni; yapı atanamaz"},
    {"Düzey": "5", "Tanım": "İlgi çeken kesin kütle",
     "Kanıt": "Yalnızca m/z; formül/yapı yok"},
]


# ---------------------------------------------------------------------------
# 9. ISO 17025:2017 VALİDASYON PARAMETRELERİ (kaynak doküman §7 aşaması)
# ---------------------------------------------------------------------------
ISO17025_VALIDATION: List[Dict[str, str]] = [
    {"Parametre": "LOD / LOQ", "Açıklama": "Tespit ve tayin alt sınırları"},
    {"Parametre": "Doğruluk (accuracy)", "Açıklama": "Geri kazanım / sapma"},
    {"Parametre": "Seçicilik (selectivity)", "Açıklama": "Matris girişimi yokluğu"},
    {"Parametre": "İyon oranı", "Açıklama": "Kantitatif/niteleyici oran ±%20 tolerans"},
    {"Parametre": "Doğrusallık / kalibrasyon", "Açıklama": "Çalışma aralığı"},
]


# ---------------------------------------------------------------------------
# 10. MRM GEÇİŞ TASARIM KURALLARI (kaynak doküman §3.4) — KURAL, sayı DEĞİL
# ---------------------------------------------------------------------------
MRM_DESIGN_RULES: List[str] = [
    "Öncü iyon: pozitif ESI'de çoğunlukla protonlanmış molekül [M+H]+.",
    "Her analit için en az 2 geçiş: 1 kantitatif (en yüksek sinyal) + "
    "1 niteleyici (qualifier).",
    "Önemsiz nötr kayıplardan kaçın: su (−18 Da), amonyak (−17 Da), "
    "CO₂ (−44 Da).",
    "50 Da altındaki düşük kütleli (özgül olmayan) ürün iyonlarından kaçın.",
    "İyon oranı doğrulaması: kantitatif/niteleyici oranı ±%20 tolerans.",
    "Çarpışma enerjisi (CE) optimizasyonu: vendor yazılımı "
    "(MassHunter Optimizer / Waters MS Optimization) ile otomatize edilir.",
]


# ---------------------------------------------------------------------------
# BİLEŞİK ANALİTİK PROFİLİ (hesaplanan m/z + dürüst yönlendirme)
# ---------------------------------------------------------------------------
@dataclass
class CompoundAnalyticalProfile:
    name: str
    formula: str
    monoisotopic_mass: float
    adducts: Dict[str, float]
    recommended_workflow: List[str]
    suspect_screening: Dict[str, float] = field(default_factory=dict)
    notes: str = ""


def compound_analytical_profile(name: str, formula: str) -> CompoundAnalyticalProfile:
    """Bir NPS bileşiği için HESAPLANAN analitik profil.

    - monoizotopik kütle ve addukt m/z: formülden hesaplanır (gerçek).
    - suspect_screening: HRMS şüpheli-tarama listesi için kesin kütleler.
    - DENEYSEL MRM/EI fragman ÜRETİLMEZ; ürün iyonu için CFM-ID/NPS-MS
      (in-silico) veya referans standart gerekir.
    """
    m = monoisotopic_mass(formula)
    add = adduct_mz(formula)
    profile = CompoundAnalyticalProfile(
        name=name,
        formula=formula,
        monoisotopic_mass=m,
        adducts=add,
        recommended_workflow=[s["Adım"] for s in WORKFLOW_STAGES],
        suspect_screening={
            "neutral_monoisotopic": m,
            "[M+H]+": add["[M+H]+"],
            "[M-H]-": add["[M-H]-"],
        },
        notes=(
            "Addukt m/z formülden hesaplandı (deterministik). Deneysel ürün "
            "iyonu / RI bu modülde verilmez; referans standart veya in-silico "
            "(CFM-ID/NPS-MS) ile elde edilmelidir."
        ),
    )
    return profile


# ---------------------------------------------------------------------------
# Erişim yardımcıları (Streamlit görünümleri için)
# ---------------------------------------------------------------------------
def get_reference_libraries() -> List[Dict[str, str]]:
    return [{"Kütüphane": x.name, "Teknik": x.technique,
             "Bileşik Sayısı": x.compound_count, "Erişim": x.access,
             "Özellikler": x.features, "URL": x.url}
            for x in REFERENCE_LIBRARIES]


def get_standard_suppliers() -> List[Dict[str, str]]:
    return [{"Tedarikçi": x.name, "Ürün Türü": x.product_type,
             "Özellikler": x.features} for x in STANDARD_SUPPLIERS]


def get_in_silico_tools() -> List[Dict[str, str]]:
    return [{"Araç": x.name, "Yaklaşım": x.approach,
             "Kullanım": x.use_case, "Not": x.note} for x in IN_SILICO_TOOLS]


def get_molecular_networking() -> List[Dict[str, str]]:
    return [{"Yaklaşım": x.name, "İlke": x.principle, "Uygulama": x.application}
            for x in MOLECULAR_NETWORKING]


def get_statistics() -> Dict[str, int]:
    return {
        "reference_libraries": len(REFERENCE_LIBRARIES),
        "standard_suppliers": len(STANDARD_SUPPLIERS),
        "in_silico_tools": len(IN_SILICO_TOOLS),
        "networking_approaches": len(MOLECULAR_NETWORKING),
        "workflow_stages": len(WORKFLOW_STAGES),
        "schymanski_levels": len(SCHYMANSKI_LEVELS),
    }


if __name__ == "__main__":
    # Hızlı kendi-kendine doğrulama (gerçek değerler)
    for nm, fo in [("Mephedrone", "C11H15NO"), ("JWH-018", "C24H23NO")]:
        p = compound_analytical_profile(nm, fo)
        print(nm, fo, "M=", p.monoisotopic_mass, "[M+H]+=", p.adducts["[M+H]+"])
    print("İstatistik:", get_statistics())
