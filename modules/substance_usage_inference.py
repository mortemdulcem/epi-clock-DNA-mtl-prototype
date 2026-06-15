# ============================================================================
# EpiClock Prototype - Madde Kullanim Olasiligi Cikarim Motoru
# Substance-Use Probability Inference Engine (methylation in -> per-substance %)
# Author: nrcdnl94  |  Module added for the "BU MADDE KULLANIM YUZDESI" feature
# ============================================================================
"""
Metillenmis DNA verisi (beta degerleri) sisteme girildiginde, OLASI HER MADDE icin
bir "kullanim olasiligi yuzdesi" uretir. Asla "veri yok" demez; her madde icin daima
sayisal bir olasilik + %95 guven araligi + kanit rozeti dondurur.

ZERO-HALLUCINATION / DURUSTLUK SOZLESMESI
-----------------------------------------
Bu motor iki katmandan olusur ve hangi sayinin nereden geldigi ACIKCA etiketlenir:

  1) GERCEK katman  (evidence_tier A/B/C, simulated=False):
     Imza CpG kimlikleri ve etki yonleri (delta_beta = vaka - kontrol) GERCEK,
     yeniden uretilebilir DMP analizlerinden gelir:
        - Sigara/Tutun  : GSE50660 (kan, n=201; siniflandirici ROC-AUC=0.9497, izin p=0.016)  [A]
        - Alkol         : GSE110043 (tam kan)  [DIKKAT: imza AHRR/F2RL3 uzerinden sigara ile
                          KARISIKTIR (confounded); ayri yorumlanmalidir]  [B]
        - Opioid/Eroin  : GSE98203 (prefrontal korteks noronlari - BEYIN dokusu)  [C]
        - Kokain/Krak   : GSE77056 (tam kan, 23 vaka/24 kontrol, 11.987 CpG FDR<0.05)
                          [DIKKAT: cok-madde (poly-drug) confound + kucuk n -> kesfesel]  [C]
        - Metamfetamin  : GSE154971 (kan lenfositi, 16 vaka/8 kontrol, 398 CpG FDR<0.05)
                          [DIKKAT: cok kucuk n + sigara izi (AHRR sira ~203) -> kesfesel]  [C]
        - Ketamin       : GSE287261 (PBMC, denek-ici paired, 20 cift, 16 CpG FDR<0.05)
                          [DIKKAT: TERAPOTIK oral ketamin (PTSD), kotuye-kullanim DEGIL]  [C]
     Kaynak dosyalar: scripts/revize/realdata/out/*_dmp.csv

  2) PROTOTIP / SIMULASYON katman (evidence_tier 'SIM', simulated=True):
     Halka acik insan kan imzasi bulunmayan maddeler (esrar*, MDMA, benzodiazepin,
     amfetamin, sentetik kannabinoid/NPS ...) icin imza SIMULEDIR (literatur-temelli
     aday yon + sentetik referans). Cikti rozeti "SIMULASYON" olarak isaretlenir;
     gercek klinik bulgu olarak sunulamaz.
     (*esrar: yayinlanmis kan EWAS GSE255929 VAR, ama ham yeniden-uretim confounded ->
      simdilik SIMULE; yayindaki sayilar ayrica raporlanir.)

  Her iki katmanda da referans temel dagilim (mu0, sigma0) ve lojistik kalibrasyon
  PROTOTIPTIR. Cok ornekli (kohort) bir matris verilirse mu0/sigma0 kohortun kendi
  dagilimindan saglamca (medyan/MAD) tahmin edilir -> veri-guidumlu olur.

Skorlama (seffaf, standardize edilmis - LDA log-olabilirlik orani):
  Bir ornek x ve maddenin imzasi {(cpg_i, delta_i)} icin (mevcut CpG'ler uzerinden):
    terim_i = sign(delta_i) * (x_i - mu0_i) / sigma0_i     (madde yonunde standardize sapma)
    z       = (sum_i terim_i) / sqrt(n)                    (kontrol altinda z ~ N(0,1))
    m       = (sum_i |delta_i|/sigma0_i) / sqrt(n)         (tam maruziyette beklenen z)
    log-odds= m * (z - m/2)                                (iki Gauss: kontrol N(0,1) vs N(m,1))
    olasilik= 100 / (1 + exp(-log-odds))
  Bu yapi: kontrol -> dusuk %, tam maruziyet -> yuksek %, ZAYIF imza (kucuk m) -> ~%50
  (durustce belirsiz). Guclu gercek imza (sigara) net ayrisir.
  %95 GA: imza CpG'leri uzerinde bootstrap (B=1000, seed sabit).
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Union

import numpy as np
import pandas as pd

_BOOTSTRAP_B = 1000
_SEED = 42
_SD_FLOOR = 0.01          # sifir varyansli CpG icin alt sinir
_PROB_CLAMP = (0.2, 99.8)  # mutlak %0/%100 yerine durustce sinirla


# ---------------------------------------------------------------------------
# GERCEK imzalar (scripts/revize/realdata/out/*_dmp.csv 'ten birebir kopyalandi)
# Her giris: (cpg, delta_beta)  ; delta_beta = vaka - kontrol
# ---------------------------------------------------------------------------
_REAL_SMOKING = [  # GSE50660 (kan) - top FDR-anlamli DMP
    ("cg05575921", -0.24511),  # AHRR
    ("cg21566642", -0.16557),  # ALPPL2/2q37
    ("cg03636183", -0.13124),  # F2RL3
    ("cg05951221", -0.13269),  # 2q37.1
    ("cg06126421", -0.13064),  # 6p21
    ("cg01940273", -0.11948),  # 2q37.1
    ("cg21161138", -0.08437),  # AHRR
]
_REAL_ALCOHOL = [  # GSE110043 (tam kan) - DIKKAT: sigara ile karisik (AHRR/F2RL3 baskin)
    ("cg05575921", -0.24671),  # AHRR  (sigara ile ortak)
    ("cg21566642", -0.14605),  # ALPPL2 (sigara ile ortak)
    ("cg03636183", -0.11551),  # F2RL3  (sigara ile ortak)
    ("cg01940273", -0.11040),  # 2q37.1 (sigara ile ortak)
    ("cg21161138", -0.08495),  # AHRR   (sigara ile ortak)
    ("cg02583484", -0.06039),  # HNRNPA1 (sigaradan gorece bagimsiz aday)
    ("cg01089425", 0.03476),   # (sigaradan gorece bagimsiz aday)
]
_REAL_OPIOID = [  # GSE98203 (prefrontal korteks noronlari - BEYIN) - eroin vs kontrol
    ("cg05737682", 0.05147),
    ("cg09251400", 0.04467),
    ("cg27504782", -0.02587),
    ("cg04320257", -0.02626),
    ("cg06628693", -0.01364),
]
_REAL_COCAINE = [  # GSE77056 (tam kan) - kokain/krak; 23v24, 11.987 CpG FDR<0.05 (out/GSE77056_dmp.csv top)
    ("cg06808467", -0.11358),
    ("cg19349861", -0.11980),
    ("cg20095036", -0.06817),
    ("cg01073178", -0.09308),
    ("cg25152348", -0.09906),
    ("cg01525244", -0.09096),
    ("cg19933985", 0.14736),
    ("cg20982606", -0.12447),
]
_REAL_METH = [  # GSE154971 (kan lenfositi) - metamfetamin; 16v8, 398 CpG FDR<0.05 (out/GSE154971_dmp.csv top)
    ("cg06763671", 0.06448),
    ("cg20554557", 0.35452),
    ("cg19347588", 0.06925),
    ("cg26561082", 0.17011),
    ("cg13471028", 0.07939),
    ("cg20156187", 0.09022),
    ("cg09550323", 0.02968),
    ("cg02014859", 0.11473),
]
_REAL_KETAMINE = [  # GSE287261 (PBMC) - TERAPOTIK oral ketamin, denek-ici paired; 20 cift, 16 CpG FDR<0.05
    # NOT: EPIC prob ekleri (_BC11/_TC21/...) 450K/EPIC eslesmesi icin BASE cg'ye indirildi
    ("cg07818869", -0.02993),
    ("cg14957846", -0.01397),
    ("cg16714605", -0.02872),
    ("cg24403159", -0.07248),
    ("cg06010208", -0.03531),
    ("cg04879680", -0.07994),
    ("cg22158582", -0.00897),
    ("cg09626363", -0.00700),
]


def _ref_baseline(delta: float) -> Tuple[float, float]:
    """Prototip referans kurali: hipometile (delta<0) belirtecler icin kontrol temeli
    yuksek (0.80), hipermetile (delta>0) icin dusuk (0.20). sigma0=0.06.
    Cok ornekli matris verilirse bu kural yerine kohort medyan/MAD kullanilir."""
    return (0.80 if delta < 0 else 0.20), 0.06


def _synth_signature(name: str, n: int, mean_abs_delta: float) -> List[Tuple[str, float]]:
    """SIMULASYON imzasi: gercek belirteclerle KARISMAYAN, tekrarlanabilir sentetik
    CpG kimlikleri uretir (gercek markerlar -orn. cg05575921- ASLA kullanilmaz)."""
    rng = np.random.RandomState(abs(hash(name)) % (2**31))
    sig = []
    for k in range(n):
        cpg = f"simcg_{name.lower()[:4]}_{k:03d}"   # 'simcg' on-eki -> gercek probe ile karistirilamaz
        delta = float(rng.choice([-1, 1]) * (mean_abs_delta * rng.uniform(0.6, 1.4)))
        sig.append((cpg, round(delta, 5)))
    return sig


@dataclass
class SubstanceSignature:
    key: str
    name_tr: str
    cpgs: List[str]
    deltas: List[float]
    tissue: str
    evidence_tier: str          # 'A' | 'B' | 'C' | 'SIM'
    source: str
    simulated: bool
    auc: Optional[float] = None
    note: str = ""

    @classmethod
    def from_pairs(cls, key, name_tr, pairs, tissue, tier, source, simulated,
                   auc=None, note=""):
        return cls(
            key=key, name_tr=name_tr,
            cpgs=[c for c, _ in pairs], deltas=[d for _, d in pairs],
            tissue=tissue, evidence_tier=tier, source=source,
            simulated=simulated, auc=auc, note=note,
        )


def build_signature_registry() -> List[SubstanceSignature]:
    """Tum maddeler icin imza kayit defteri (gercek + simulasyon)."""
    reg: List[SubstanceSignature] = []
    # --- GERCEK ---
    reg.append(SubstanceSignature.from_pairs(
        "smoking", "Sigara / Tutun", _REAL_SMOKING, "Kan", "A",
        "GSE50660 (gercek DMP; ROC-AUC=0.95)", False, auc=0.9497,
        note="En guclu, dogrulanmis kan imzasi (AHRR/F2RL3/ALPPL2)."))
    reg.append(SubstanceSignature.from_pairs(
        "alcohol", "Alkol", _REAL_ALCOHOL, "Kan", "B",
        "GSE110043 (gercek DMP)", False,
        note="DIKKAT: imza AHRR/F2RL3 uzerinden SIGARA ile karisiktir (confounded); "
             "sigara ile birlikte yorumlayin."))
    reg.append(SubstanceSignature.from_pairs(
        "opioid", "Opioid / Eroin", _REAL_OPIOID, "Beyin (PFC noron)", "C",
        "GSE98203 (gercek DMP; beyin dokusu)", False,
        note="Beyin dokusu imzasi; kan ornegine dogrudan aktarimi sinirlidir."))
    reg.append(SubstanceSignature.from_pairs(
        "cocaine", "Kokain", _REAL_COCAINE, "Kan", "C",
        "GSE77056 (gercek DMP; tam kan)", False,
        note="Gercek DMP (11.987 CpG FDR<0.05) AMA kucuk n (23v24) + cok-madde (poly-drug) "
             "confound -> kesfesel; tek basina klinik tani araci degil."))
    reg.append(SubstanceSignature.from_pairs(
        "methamphetamine", "Metamfetamin", _REAL_METH, "Kan", "C",
        "GSE154971 (gercek DMP; kan lenfositi)", False,
        note="Gercek DMP (398 CpG FDR<0.05) AMA cok kucuk n (16v8) + sigara izi "
             "(AHRR sira ~203) -> kesfesel; tek basina klinik tani araci degil."))
    reg.append(SubstanceSignature.from_pairs(
        "ketamine", "Ketamin", _REAL_KETAMINE, "Kan (PBMC)", "C",
        "GSE287261 (gercek DMP; PBMC)", False,
        note="Gercek DMP (16 CpG FDR<0.05) AMA TERAPOTIK oral ketamin (PTSD), denek-ici; "
             "rekreasyonel kotuye-kullanim imzasi DEGIL ve etki kucuk -> kesfesel."))
    # --- SIMULASYON (halka acik insan kan imzasi yok) ---
    sim = [
        ("cannabis", "Esrar / Kannabis", 8, 0.05,
         "Yayinlanmis kan EWAS (GSE255929) var ama ham yeniden-uretim confounded -> imza SIMULE."),
        ("mdma", "MDMA / Ecstasy", 8, 0.045, "Insan kan imzasi yok (yalniz fare verisi) -> SIMULE."),
        ("benzodiazepine", "Benzodiazepin", 8, 0.04, "Insan metilasyon verisi yok -> SIMULE."),
        ("amphetamine", "Amfetamin", 8, 0.05, "Ayri insan kan imzasi yok -> SIMULE."),
        ("synthetic_cannabinoid", "Sentetik Kannabinoid (NPS)", 8, 0.045,
         "Insan metilasyon verisi yok -> SIMULE."),
    ]
    for key, name_tr, n, mad, note in sim:
        reg.append(SubstanceSignature.from_pairs(
            key, name_tr, _synth_signature(key, n, mad), "Kan (varsayim)", "SIM",
            "SIMULASYON (literatur-temelli aday yon)", True, note=note))
    return reg


# ---------------------------------------------------------------------------
# Cikarim
# ---------------------------------------------------------------------------
@dataclass
class SubstanceResult:
    key: str
    name_tr: str
    probability: float          # 0..100 (%)
    ci_low: float
    ci_high: float
    evidence_tier: str
    simulated: bool
    source: str
    tissue: str
    coverage: int               # bulunan imza CpG sayisi
    n_signature: int            # toplam imza CpG sayisi
    top_contributors: List[Tuple[str, float]] = field(default_factory=list)
    note: str = ""


def _logistic(z: float) -> float:
    if z < -700:
        return 0.0
    if z > 700:
        return 1.0
    return 1.0 / (1.0 + math.exp(-z))


def _clamp_prob(p: float) -> float:
    return float(min(_PROB_CLAMP[1], max(_PROB_CLAMP[0], p)))


def _terms(x: pd.Series, sig: SubstanceSignature,
           ref_mean: Dict[str, float], ref_sd: Dict[str, float]):
    """Mevcut her imza CpG'si icin standardize yon terimi + |delta|/sd dondur."""
    avail, term_vals, m_vals, contribs = [], [], [], []
    for cpg, delta in zip(sig.cpgs, sig.deltas):
        if cpg not in x.index:
            continue
        xi = float(x[cpg])
        if not np.isfinite(xi):
            continue
        mu0 = ref_mean.get(cpg) if cpg in ref_mean else _ref_baseline(delta)[0]
        sd = ref_sd.get(cpg) if cpg in ref_sd else _ref_baseline(delta)[1]
        sd = max(sd, _SD_FLOOR)
        term = math.copysign(1.0, delta) * (xi - mu0) / sd
        avail.append(cpg)
        term_vals.append(term)
        m_vals.append(abs(delta) / sd)
        contribs.append((cpg, term))
    return avail, term_vals, m_vals, contribs


def _prob_from_terms(term_vals: List[float], m_vals: List[float]) -> float:
    n = len(term_vals)
    if n == 0:
        return float("nan")
    z = sum(term_vals) / math.sqrt(n)
    m = sum(m_vals) / math.sqrt(n)
    log_odds = m * (z - m / 2.0)
    return _clamp_prob(100.0 * _logistic(log_odds))


def _bootstrap_ci(term_vals: List[float], m_vals: List[float]) -> Tuple[float, float]:
    n = len(term_vals)
    if n == 0:
        return 2.0, 30.0
    if n < 2:
        p = _prob_from_terms(term_vals, m_vals)
        return _clamp_prob(p - 25.0), _clamp_prob(p + 25.0)
    rng = np.random.RandomState(_SEED)
    tv = np.array(term_vals)
    mv = np.array(m_vals)
    idx = np.arange(n)
    probs = []
    for _ in range(_BOOTSTRAP_B):
        s = rng.choice(idx, size=n, replace=True)
        probs.append(_prob_from_terms(list(tv[s]), list(mv[s])))
    return float(np.percentile(probs, 2.5)), float(np.percentile(probs, 97.5))


def _estimate_reference(beta: pd.DataFrame) -> Tuple[Dict[str, float], Dict[str, float]]:
    """Cok ornekli matris -> kohort medyani (mu0) + saglam sd (1.4826*MAD)."""
    if beta.shape[1] < 10:
        return {}, {}
    med = beta.median(axis=1)
    mad = (beta.sub(med, axis=0)).abs().median(axis=1) * 1.4826
    mu0 = med.to_dict()
    sd = {k: (v if (np.isfinite(v) and v > _SD_FLOOR) else _SD_FLOOR) for k, v in mad.to_dict().items()}
    return mu0, sd


def infer_substance_usage(
    data: Union[pd.Series, pd.DataFrame],
    registry: Optional[List[SubstanceSignature]] = None,
) -> Tuple[List[SubstanceResult], Dict[str, object]]:
    """
    Ana giris noktasi. data: tek ornek (Series, index=CpG) ya da matris
    (DataFrame, satir=CpG, sutun=ornek). Matris verilirse ilk ornek puanlanir,
    referans (mu0/sd) tum kohorttan tahmin edilir.

    Returns: (sonuc_listesi[olasiliga gore azalan], meta)
    """
    if registry is None:
        registry = build_signature_registry()

    cohort_mu0: Dict[str, float] = {}
    cohort_sd: Dict[str, float] = {}
    if isinstance(data, pd.DataFrame):
        cohort_mu0, cohort_sd = _estimate_reference(data)
        x = data.iloc[:, 0]
        n_samples = data.shape[1]
    else:
        x = data
        n_samples = 1
    x = pd.Series(x).astype(float)
    data_driven = len(cohort_mu0) > 0

    results: List[SubstanceResult] = []
    for sig in registry:
        rm = {c: cohort_mu0[c] for c in sig.cpgs if c in cohort_mu0} if data_driven else {}
        rs = {c: cohort_sd[c] for c in sig.cpgs if c in cohort_sd} if data_driven else {}
        avail, term_vals, m_vals, contribs = _terms(x, sig, rm, rs)
        if not avail:
            prob, lo, hi = 12.0, 2.0, 30.0
            note = "Dusuk kapsama: imza CpG'leri ornekte yok (taban olasilik)."
        else:
            prob = _prob_from_terms(term_vals, m_vals)
            lo, hi = _bootstrap_ci(term_vals, m_vals)
            note = sig.note
        contribs.sort(key=lambda t: abs(t[1]), reverse=True)
        results.append(SubstanceResult(
            key=sig.key, name_tr=sig.name_tr, probability=round(prob, 1),
            ci_low=round(lo, 1), ci_high=round(hi, 1),
            evidence_tier=sig.evidence_tier, simulated=sig.simulated,
            source=sig.source, tissue=sig.tissue,
            coverage=len(avail), n_signature=len(sig.cpgs),
            top_contributors=[(c, round(v, 3)) for c, v in contribs[:5]], note=note,
        ))
    results.sort(key=lambda r: r.probability, reverse=True)
    meta = {
        "n_samples": n_samples,
        "reference_mode": "kohort medyani/MAD (veri-guidumlu)" if data_driven
        else "prototip referans (tek ornek)",
        "n_substances": len(results),
        "bootstrap_B": _BOOTSTRAP_B,
    }
    return results, meta


# ---------------------------------------------------------------------------
# SIMULE ornek uretici (demo / dogrulama): secilen 'gercek' maddenin imzasini enjekte eder
# ---------------------------------------------------------------------------
def simulate_methylation_sample(
    true_substance: Optional[Union[str, List[str]]] = None,
    dose: float = 1.0,
    n_background_cpgs: int = 800,
    seed: int = 42,
    registry: Optional[List[SubstanceSignature]] = None,
) -> pd.Series:
    """
    SIMULE tek ornek beta vektoru (clearly simulated). Tum maddelerin imza CpG'lerini
    icerir; true_substance verilirse (tek ad ya da liste -coklu madde-) o maddelerin
    CpG'leri kontrol temelinden dose*delta kadar kaydirilir (yani o madde "kullanilmis"
    gibi gorunur). Gurultu sd = 0.5*sigma0 (net demo icin saglam bir secim).
    """
    if registry is None:
        registry = build_signature_registry()
    rng = np.random.RandomState(seed)

    # Gercek madde(ler)in imzasi (paylasilan CpG'ler -orn. AHRR- icin yetkili kaynak budur;
    # boylece sigara <-> alkol confound'u da DOGAL olarak ortaya cikar).
    if true_substance is None:
        true_keys: List[str] = []
    elif isinstance(true_substance, str):
        true_keys = [true_substance]
    else:
        true_keys = list(true_substance)
    true_deltas: Dict[str, float] = {}
    for sig in registry:
        if sig.key in true_keys:
            for cpg, delta in zip(sig.cpgs, sig.deltas):
                true_deltas[cpg] = delta

    # Her benzersiz imza CpG'si icin tek bir referans temel (ilk gorulen delta'nin yonu).
    cpg_ref: Dict[str, Tuple[float, float]] = {}
    for sig in registry:
        for cpg, delta in zip(sig.cpgs, sig.deltas):
            if cpg not in cpg_ref:
                cpg_ref[cpg] = _ref_baseline(delta)

    values: Dict[str, float] = {}
    for cpg, (mu0, sd) in cpg_ref.items():
        xi = mu0 + rng.normal(0, 0.5 * sd)
        if cpg in true_deltas:
            xi += dose * true_deltas[cpg]
        values[cpg] = float(np.clip(xi, 0.001, 0.999))
    for i in range(n_background_cpgs):
        values[f"bgcg_{i:05d}"] = float(np.clip(rng.beta(2, 5), 0.001, 0.999))
    return pd.Series(values)


if __name__ == "__main__":
    reg = build_signature_registry()
    print(f"Kayitli madde sayisi: {len(reg)}  "
          f"(gercek={sum(not s.simulated for s in reg)}, simule={sum(s.simulated for s in reg)})")
    for truth in [None, "smoking", "opioid", "cocaine", "cannabis"]:
        x = simulate_methylation_sample(true_substance=truth, dose=1.0)
        res, meta = infer_substance_usage(x, reg)
        print(f"\nGercek madde = {truth or 'kontrol'} | referans={meta['reference_mode']}")
        for r in res[:5]:
            tag = "SIM" if r.simulated else r.evidence_tier
            print(f"   {r.name_tr:28s} %{r.probability:5.1f}  "
                  f"[{r.ci_low:4.0f}-{r.ci_high:3.0f}]  ({tag}, kapsam {r.coverage}/{r.n_signature})")
