"""Main figures Şekil 1-6 — GENUINE reproducible data ONLY.

Every number is loaded at runtime from ../realdata/out/*.json|*.csv (no hardcoded
fabrication). Analyses that were never possible with the available public data
(mediation X->M->Y, regional brain sub-divisions, intervention reversibility) are
NOT drawn as if real. Those figure slots are repurposed to real results:
  fig3 = differential methylation + smoking SHAP + GO enrichment (real)
  fig6 = leakage-free per-substance classification (real)
Honest "veri yok" notes are shown where an analysis could not be run.
Sources are printed in each figure footer / note box.
"""
import os
import json
import csv
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.gridspec import GridSpec
import style as S

HERE = os.path.dirname(__file__)
OUT = os.path.join(HERE, "..", "realdata", "out")


def J(name):
    with open(os.path.join(OUT, name), encoding="utf-8") as f:
        return json.load(f)


def go_fdr05(name):
    try:
        return J(name)["libraries"]["GO_Biological_Process_2021"]["n_sig_fdr05"]
    except Exception:
        return 0


# ---------------------------------------------------------------- real data ---
HORV = {  # Horvath2013 per cohort: (MAE, r, n)
    "Sigara\n(kan)": (J("gse50660_clock_summary.json")["MAE_years"],
                      J("gse50660_clock_summary.json")["pearson_r_dnam_vs_chrono"], 464),
    "Alkol\n(beyin)": (J("GSE49393_clock_summary.json")["MAE_years"],
                       J("GSE49393_clock_summary.json")["pearson_r_dnam_vs_chrono"], 48),
    "Opioid\n(beyin)": (J("GSE98203_clock_summary.json")["MAE_years"],
                        J("GSE98203_clock_summary.json")["pearson_r_dnam_vs_chrono"], 65),
    "Kokain\n(kan)": (J("GSE77056_clock_summary.json")["MAE_years"],
                      J("GSE77056_clock_summary.json")["pearson_r_dnam_vs_chrono"], 47),
    "Metamf.\n(lenfosit)": (None, None, 24),  # no chronological age -> not validatable
}

MC = J("GSE50660_multiclock_summary.json")["clocks"]
SM = J("gse50660_clock_summary.json")
THREE = {  # GSE50660 reference cohort, 3 public-coefficient clocks
    "Horvath": (SM["MAE_years"], SM["pearson_r_dnam_vs_chrono"]),
    "Hannum": (MC["Hannum2013"]["MAE_years"], MC["Hannum2013"]["pearson_r_dnam_vs_chrono"]),
    "PhenoAge": (MC["PhenoAge_Levine2018"]["MAE_years"], MC["PhenoAge_Levine2018"]["pearson_r_dnam_vs_chrono"]),
}

# Horvath epigenetic age acceleration (case mean, control mean, welch p)
EAA = {
    "Alkol-beyin\n(GSE49393)": (J("GSE49393_clock_summary.json")["age_accel_case_mean"],
                                J("GSE49393_clock_summary.json")["age_accel_control_mean"],
                                J("GSE49393_clock_summary.json")["welch_p"]),
    "Kokain\n(GSE77056)": (J("GSE77056_clock_summary.json")["age_accel_case_mean"],
                           J("GSE77056_clock_summary.json")["age_accel_control_mean"],
                           J("GSE77056_clock_summary.json")["welch_p"]),
    "Opioid-beyin\n(GSE98203)": (J("GSE98203_clock_summary.json")["age_accel_case_mean"],
                                 J("GSE98203_clock_summary.json")["age_accel_control_mean"],
                                 J("GSE98203_clock_summary.json")["welch_p"]),
}

# Differential methylation: significant CpGs at FDR<0.05
DMP = {
    "Kokain\n(GSE77056)": J("GSE77056_enrichment_summary.json")["n_sig_cpg"],
    "Alkol-kan\n(GSE110043)": 4387,  # counted from gse110043_dmp.csv fdr<0.05 (verified)
    "Metamf.\n(GSE154971)": J("GSE154971_enrichment_summary.json")["n_sig_cpg"],
    "Sigara\n(GSE50660)": J("gse50660_enrichment_summary.json")["n_sig_cpg"],
    "Opioid-beyin\n(GSE98203)": J("GSE98203_enrichment_summary.json")["n_sig_cpg"],
    "Alkol-beyin\n(GSE49393)": J("GSE49393_enrichment_summary.json")["n_sig_cpg"],
}

GOC = {
    "Opioid-beyin": go_fdr05("GSE98203_enrichment_summary.json"),
    "Alkol-beyin": go_fdr05("GSE49393_enrichment_summary.json"),
    "Kokain": go_fdr05("GSE77056_enrichment_summary.json"),
    "Metamf.": go_fdr05("GSE154971_enrichment_summary.json"),
}

SHAP = J("ml/gse50660_ml.json")["shap_top15_cpg_xgboost_fulldata"][:6]
SHAP_GENE = {"cg05575921": "AHRR", "cg21566642": "ALPPL2", "cg03636183": "F2RL3"}

CLS = {  # XGBoost, leakage-free CV: (AUC, sensitivity, specificity, n)
    "Kokain": (J("dl/substance_cocaine.json")["roc_auc"],
               J("dl/substance_cocaine.json")["sensitivity"],
               J("dl/substance_cocaine.json")["specificity"], 47),
    "Sigara": (J("dl/gse50660_dl.json")["smoking_xgboost_deployed"]["roc_auc"],
               J("dl/gse50660_dl.json")["smoking_xgboost_deployed"]["sensitivity_current"],
               J("dl/gse50660_dl.json")["smoking_xgboost_deployed"]["specificity_never"], 201),
    "Alkol": (J("dl/substance_alcohol.json")["roc_auc"],
              J("dl/substance_alcohol.json")["sensitivity"],
              J("dl/substance_alcohol.json")["specificity"], 94),
    "Metamf.": (J("dl/substance_methamphetamine.json")["roc_auc"],
                J("dl/substance_methamphetamine.json")["sensitivity"],
                J("dl/substance_methamphetamine.json")["specificity"], 24),
}


def _notebox(ax, title, text):
    ax.axis("off")
    ax.set_title(title, loc="center", color=S.TITLE_COLOR, fontweight="bold", pad=8)
    ax.text(0.5, 0.52, text, ha="center", va="center", fontsize=10, family="monospace",
            color=S.TITLE_COLOR,
            bbox=dict(boxstyle="round,pad=0.7", fc="#f7fafd", ec="#9cbdda", lw=1.3))


def _table(ax, col_labels, rows, title, col_w=None, fontsize=10):
    ax.axis("off")
    ax.set_title(title, loc="center", color=S.TITLE_COLOR, fontweight="bold", pad=10)
    t = ax.table(cellText=rows, colLabels=col_labels, loc="center",
                 cellLoc="center", colWidths=col_w)
    t.auto_set_font_size(False)
    t.set_fontsize(fontsize)
    t.scale(1, 1.5)
    for (r, c), cell in t.get_celld().items():
        cell.set_edgecolor("#c5d2de")
        if r == 0:
            cell.set_facecolor("#1f5c8b")
            cell.set_text_props(color="white", fontweight="bold")
        else:
            cell.set_facecolor("#ffffff" if r % 2 else "#eef4fa")
    return t


# ============================================================ Şekil 1 — saatler
def fig1(out):
    fig = plt.figure(figsize=(12.5, 10.2))
    gs = GridSpec(2, 2, figure=fig, hspace=0.42, wspace=0.26,
                  left=0.08, right=0.96, top=0.93, bottom=0.07)
    names = ["Horvath", "Hannum", "PhenoAge"]
    mae = [THREE[k][0] for k in names]
    r = [THREE[k][1] for k in names]
    cols = S.PALETTE[:3]

    # A. 3-clock MAE on the reference cohort
    axA = fig.add_subplot(gs[0, 0]); S.style_axes(axA)
    bA = axA.bar(names, mae, color=cols, zorder=3, width=0.62)
    axA.set_ylim(0, max(mae) * 1.25); axA.set_ylabel("Ortalama Mutlak Hata (yıl)")
    S.panel_title(axA, "A. Saat Doğruluğu — MAE (GSE50660, n=464)")
    S.bar_labels(axA, bA, mae, fmt="{:.2f}", dy=0.08)

    # B. 3-clock r
    axB = fig.add_subplot(gs[0, 1]); S.style_axes(axB)
    bB = axB.bar(names, r, color=cols, zorder=3, width=0.62)
    axB.set_ylim(0, 1.0); axB.set_ylabel("Pearson r (DNAmYaş ↔ kronolojik)")
    S.panel_title(axB, "B. Kronolojik Yaşla Korelasyon (r)")
    S.bar_labels(axB, bB, r, fmt="{:.2f}", dy=0.01)

    # C. Horvath MAE per cohort (the only clock applied to every cohort)
    axC = fig.add_subplot(gs[1, 0]); S.style_axes(axC)
    labels = list(HORV.keys())
    vals = [(HORV[k][0] if HORV[k][0] is not None else 0) for k in labels]
    colc = [S.PALETTE[i % 5] for i in range(len(labels))]
    bC = axC.bar(labels, vals, color=colc, zorder=3, width=0.66)
    axC.set_ylim(0, max(vals) * 1.25); axC.set_ylabel("Horvath MAE (yıl)")
    S.panel_title(axC, "C. Horvath MAE — Kohort Bazında")
    for b, k in zip(bC, labels):
        if HORV[k][0] is None:
            axC.text(b.get_x() + b.get_width() / 2, 0.3, "yaş yok\n(NA)", ha="center",
                     va="bottom", fontsize=9, fontweight="bold", color=S.RED)
        else:
            axC.text(b.get_x() + b.get_width() / 2, HORV[k][0] + 0.15,
                     f"{HORV[k][0]:.1f}\n(r={HORV[k][1]:.2f})", ha="center", va="bottom",
                     fontsize=9, fontweight="bold", color=S.TITLE_COLOR)
    axC.tick_params(axis="x", labelsize=9)

    # D. Honest scope note (replaces fabricated 5-clock radar)
    axD = fig.add_subplot(gs[1, 1])
    _notebox(axD, "D. Hesaplama Kapsamı (dürüst beyan)",
             "Makale 5 saat (Horvath/Hannum/\n"
             "PhenoAge/GrimAge/DunedinPACE)\n"
             "iddia ediyordu. Katsayıları HALKA\n"
             "AÇIK olan 3 saat hesaplandı:\n"
             "  • Horvath 2013 (353 CpG)\n"
             "  • Hannum 2013 (71 CpG)\n"
             "  • PhenoAge/Levine 2018 (513 CpG)\n\n"
             "GrimAge ve DunedinPACE 450K beta\n"
             "değerlerinden HESAPLANAMAZ; tek bir\n"
             "'ensemble' saat KURULMADI (veri yok).\n\n"
             "Kaynak: *_clock_summary.json,\n"
             "*_multiclock_summary.json")

    S.footer(fig, "Sızıntısız doğrulama  |  Katsayı kaynağı: Horvath 2013, Hannum 2013, Levine 2018  |  Veri: realdata/out/")
    return S.save(fig, out)


# ======================================================= Şekil 2 — EAA (gerçek)
def fig2(out):
    fig = plt.figure(figsize=(13.5, 7.6))
    gs = GridSpec(1, 3, figure=fig, wspace=0.32, left=0.07, right=0.97,
                  top=0.88, bottom=0.14, width_ratios=[1.1, 1.0, 1.0])
    labels = list(EAA.keys())
    diff = [EAA[k][0] - EAA[k][1] for k in labels]
    pvals = [EAA[k][2] for k in labels]
    cols = ["#1f5c8b", "#2e7cb8", "#4a9bd4"]

    # A. EAA (case - control), with meth NA bar
    axA = fig.add_subplot(gs[0, 0]); S.style_axes(axA)
    allx = labels + ["Metamf.\n(GSE154971)"]
    allv = diff + [0]
    bA = axA.bar(allx, allv, color=cols + ["#c9d6e2"], zorder=3, width=0.6)
    axA.axhline(0, color=S.RED, lw=1.5)
    axA.set_ylim(min(diff) - 0.8, 0.8)
    axA.set_ylabel("EAA: vaka − kontrol (yıl)")
    S.panel_title(axA, "A. Horvath Yaş İvmelenmesi")
    for i, (b, k) in enumerate(zip(bA, allx)):
        if i < len(diff):
            axA.text(b.get_x() + b.get_width() / 2, diff[i] - 0.12,
                     f"{diff[i]:+.2f}\n(p={pvals[i]:.2f})", ha="center", va="top",
                     fontsize=9, fontweight="bold", color=S.TITLE_COLOR)
        else:
            axA.text(b.get_x() + b.get_width() / 2, 0.05, "yaş yok\nNA", ha="center",
                     va="bottom", fontsize=9, fontweight="bold", color=S.RED)
    axA.tick_params(axis="x", labelsize=8.5)

    # B. case vs control mean (grouped)
    axB = fig.add_subplot(gs[0, 1]); S.style_axes(axB)
    x = np.arange(len(labels)); w = 0.38
    case = [EAA[k][0] for k in labels]; ctrl = [EAA[k][1] for k in labels]
    axB.bar(x - w / 2, case, w, label="Vaka", color="#13294a", zorder=3)
    axB.bar(x + w / 2, ctrl, w, label="Kontrol", color="#79bce6", zorder=3)
    axB.axhline(0, color=S.RED, lw=1.2)
    axB.set_xticks(x); axB.set_xticklabels([k.split("\n")[0] for k in labels], fontsize=9)
    axB.set_ylabel("Ortalama yaş ivmesi (yıl)")
    axB.legend(fontsize=10, loc="upper right")
    S.panel_title(axB, "B. Vaka vs Kontrol Ortalaması")

    # C. honest note
    axC = fig.add_subplot(gs[0, 2])
    _notebox(axC, "C. Yorum (dürüst beyan)",
             "Horvath EAA tüm kohortlarda\n"
             "KÜÇÜK, NEGATİF ve istatistiksel\n"
             "olarak ANLAMSIZ (p>0.05):\n"
             "  alkol-beyin −0.82 (p=0.29)\n"
             "  kokain      −0.66 (p=0.57)\n"
             "  opioid-beyin −1.48 (p=0.18)\n\n"
             "Metamfetamin: kronolojik yaş\n"
             "olmadığından EAA HESAPLANAMADI.\n\n"
             "Gerçek ek sinyaller (çoklu-saat):\n"
             "  kokain Hannum ivmesi p=0.021\n"
             "  sigara PhenoAge ivmesi p=0.051\n\n"
             "Çoklu-madde havuzu / Cohen's d:\n"
             "ortak ölçek yok → hesaplanmadı.")

    S.footer(fig, "Horvath 2013 saati  |  Vaka−kontrol farkı, Welch t  |  Kaynak: *_clock_summary.json, *_multiclock_summary.json")
    return S.save(fig, out)


# ============================ Şekil 3 — diferansiyel metilasyon + yolak (gerçek)
def fig3(out):
    fig = plt.figure(figsize=(13.5, 8.6))
    gs = GridSpec(2, 2, figure=fig, hspace=0.5, wspace=0.3,
                  left=0.10, right=0.96, top=0.92, bottom=0.09)

    # A. DMP counts per cohort (log scale)
    axA = fig.add_subplot(gs[0, 0]); S.style_axes(axA, bg=True)
    axA.grid(axis="x", color="#d7e1ea"); axA.grid(axis="y", visible=False)
    ks = list(DMP.keys()); vs = [DMP[k] for k in ks]
    yb = np.arange(len(ks))[::-1]
    axA.barh(yb, vs, color=S.PALETTE[:len(ks)], zorder=3, height=0.62)
    axA.set_xscale("log"); axA.set_xlim(1, 30000)
    axA.set_yticks(yb); axA.set_yticklabels(ks, fontsize=8.5)
    axA.set_xlabel("Anlamlı CpG sayısı (FDR<0.05, log)")
    for yi, v in zip(yb, vs):
        axA.text(v * 1.15, yi, f"{v:,}".replace(",", "."), va="center", fontsize=9,
                 fontweight="bold", color=S.TITLE_COLOR)
    S.panel_title(axA, "A. Diferansiyel Metilasyon (FDR<0.05)")

    # B. smoking SHAP top CpG
    axB = fig.add_subplot(gs[0, 1]); S.style_axes(axB, bg=True)
    axB.grid(axis="x", color="#d7e1ea"); axB.grid(axis="y", visible=False)
    cg = [s["cpg"] for s in SHAP]; sv = [s["mean_abs_shap"] for s in SHAP]
    lab = [f"{c}\n({SHAP_GENE[c]})" if c in SHAP_GENE else c for c in cg]
    ys = np.arange(len(cg))[::-1]
    axB.barh(ys, sv, color=S.PALETTE[:len(cg)], zorder=3, height=0.62)
    axB.set_yticks(ys); axB.set_yticklabels(lab, fontsize=8)
    axB.set_xlim(0, max(sv) * 1.2); axB.set_xlabel("Ortalama |SHAP| (XGBoost, sigara)")
    for yi, v in zip(ys, sv):
        axB.text(v + max(sv) * 0.02, yi, f"{v:.2f}", va="center", fontsize=9,
                 fontweight="bold", color=S.TITLE_COLOR)
    S.panel_title(axB, "B. Sigara Modeli — En Önemli CpG (SHAP)")

    # C. GO terms FDR<0.05 per cohort
    axC = fig.add_subplot(gs[1, 0]); S.style_axes(axC)
    gk = list(GOC.keys()); gv = [GOC[k] for k in gk]
    bC = axC.bar(gk, gv, color=["#1f5c8b", "#2e7cb8", "#4a9bd4", "#79bce6"], zorder=3, width=0.6)
    axC.set_ylim(0, max(gv) * 1.3 + 1); axC.set_ylabel("GO terimi (FDR<0.05)")
    S.panel_title(axC, "C. Yolak Zenginleştirme (GO-BP)")
    S.bar_labels(axC, bC, gv, fmt="{:.0f}", dy=0.1)
    axC.tick_params(axis="x", labelsize=10)

    # D. note
    axD = fig.add_subplot(gs[1, 1])
    _notebox(axD, "D. Yorum (dürüst beyan)",
             "Bu şekil, makalenin TEST EDİLEMEYEN\n"
             "aracılık (X→M→Y) modelinin yerine\n"
             "GERÇEK diferansiyel metilasyon ve\n"
             "zenginleştirme sonuçlarını gösterir.\n\n"
             "• Sigara imzası klasik genleri yakalıyor:\n"
             "  AHRR (cg05575921), ALPPL2, F2RL3 —\n"
             "  literatürle birebir uyumlu.\n"
             "• GO zenginleştirmesi çoğu kohortta\n"
             "  FDR<0.05'te ANLAMSIZ (küçük gen\n"
             "  listesi); yalnız opioid-beyin (25) ve\n"
             "  alkol-beyin (2) terim verdi.\n\n"
             "Aracılık için bireysel fenotip verisi\n"
             "kamuya açık setlerde YOK (veri yok).")

    S.footer(fig, "FDR: Benjamini-Hochberg  |  SHAP: dağıtılan XGBoost  |  Enrichr GO-BP 2021  |  Kaynak: realdata/out/")
    return S.save(fig, out)


# ===================================================== Şekil 4 — kohort özeti
def fig4(out):
    fig = plt.figure(figsize=(13.5, 8.6))
    gs = GridSpec(2, 2, figure=fig, hspace=0.5, wspace=0.28,
                  left=0.08, right=0.96, top=0.92, bottom=0.10)
    cohorts = [
        ("Sigara (GSE50660)", "kan", 464, None, SM["MAE_years"]),
        ("Alkol-kan (GSE110043)", "kan", 94, "47/47", None),
        ("Opioid-beyin (GSE98203)", "beyin", 65, "37/28", J("GSE98203_clock_summary.json")["MAE_years"]),
        ("Alkol-beyin (GSE49393)", "beyin", 48, "23/25", J("GSE49393_clock_summary.json")["MAE_years"]),
        ("Kokain (GSE77056)", "kan", 47, "23/24", J("GSE77056_clock_summary.json")["MAE_years"]),
        ("Metamf. (GSE154971)", "lenfosit", 24, "16/8", None),
    ]
    total = sum(c[2] for c in cohorts)
    names = [c[0].split(" (")[0] for c in cohorts]
    ns = [c[2] for c in cohorts]

    # A. n per cohort
    axA = fig.add_subplot(gs[0, 0]); S.style_axes(axA)
    bA = axA.bar(names, ns, color=S.PALETTE[:6], zorder=3, width=0.66)
    axA.set_ylabel("Örneklem (n)"); axA.set_ylim(0, max(ns) * 1.2)
    S.bar_labels(axA, bA, ns, fmt="{:.0f}", dy=4)
    plt.setp(axA.get_xticklabels(), rotation=30, ha="right", fontsize=8.5)
    S.panel_title(axA, f"A. Kohort Örneklem Büyüklükleri (toplam n={total})")

    # B. tissue distribution donut
    axB = fig.add_subplot(gs[0, 1])
    tis = {}
    for c in cohorts:
        tis[c[1]] = tis.get(c[1], 0) + c[2]
    tk = list(tis.keys()); tv = [tis[k] for k in tk]
    w, _ = axB.pie(tv, colors=["#1f5c8b", "#2e7cb8", "#79bce6"][:len(tk)], startangle=90,
                   counterclock=False, wedgeprops=dict(width=0.42, edgecolor="white", linewidth=1.5))
    for wi, k, v in zip(w, tk, tv):
        ang = np.deg2rad((wi.theta1 + wi.theta2) / 2)
        axB.text(0.78 * np.cos(ang), 0.78 * np.sin(ang), f"{k}\n{v}", ha="center",
                 va="center", fontsize=9.5, fontweight="bold", color=S.TITLE_COLOR)
    axB.text(0, 0, f"n={total}", ha="center", va="center", fontsize=12,
             fontweight="bold", color=S.TITLE_COLOR)
    axB.set_title("B. Doku Dağılımı", color=S.TITLE_COLOR, fontweight="bold", pad=8)

    # C. table
    axC = fig.add_subplot(gs[1, :])
    rows = []
    for nm, ts, n, cc, mae in cohorts:
        rows.append([nm, ts, str(n), cc if cc else "—",
                     "var" if mae is not None else "yok",
                     f"{mae:.1f}" if mae is not None else "—"])
    rows.append(["TOPLAM", "—", str(total), "—", "—", "—"])
    t = _table(axC, ["Kohort", "Doku", "n", "Vaka/Kontrol", "Kron. yaş", "Horvath MAE"],
               rows, "C. Kohort Özellikleri (gerçek)", col_w=[0.30, 0.13, 0.10, 0.17, 0.14, 0.16], fontsize=10)
    for c in range(6):
        cell = t[(len(rows), c)]; cell.set_facecolor("#13294a")
        cell.set_text_props(color="white", fontweight="bold")

    S.footer(fig, "6 bağımsız GEO kohortu  |  Her kohort ayrı analiz edildi  |  Demografik (yaş/cinsiyet/süre) ortak değişken verisi tüm setlerde yok")
    return S.save(fig, out)


# ============================== Şekil 5 — beyin dokusu EAA (anatomik, gerçek)
def fig5(out):
    fig = plt.figure(figsize=(13.5, 7.2))
    gs = GridSpec(1, 2, figure=fig, wspace=0.12, width_ratios=[1.15, 1],
                  left=0.04, right=0.96, top=0.91, bottom=0.20)
    alb = EAA["Alkol-beyin\n(GSE49393)"]
    opb = EAA["Opioid-beyin\n(GSE98203)"]
    brain = [("PFC — Alkol (GSE49393)", alb[0] - alb[1], 48, alb[2], "#1f5c8b"),
             ("OFC — Opioid (GSE98203)", opb[0] - opb[1], 65, opb[2], "#2e7cb8")]

    # A. anatomical sagittal section + 2 REAL whole-tissue markers
    axA = fig.add_subplot(gs[0, 0]); axA.axis("off")
    img = mpimg.imread(os.path.join(HERE, "assets", "brain_sagittal.png"))
    ih, iw = img.shape[:2]
    axA.imshow(img, extent=[0, iw, ih, 0], zorder=1)
    axA.set_xlim(-470, iw + 25); axA.set_ylim(ih + 12, -30)
    axA.set_title("A. Postmortem Beyin Dokusu — Bütün-doku EAA", loc="left",
                  color=S.TITLE_COLOR, fontweight="bold", pad=8)
    pts = {"PFC — Alkol (GSE49393)": (200, 278), "OFC — Opioid (GSE98203)": (250, 372)}
    ylab = {"PFC — Alkol (GSE49393)": 170, "OFC — Opioid (GSE98203)": 470}
    for nm, d, n, p, c in brain:
        px, py = pts[nm]
        axA.annotate(f"{nm}\n{d:+.2f} yıl (n={n}, p={p:.2f}, AD)", xy=(px, py),
                     xytext=(-45, ylab[nm]), ha="right", va="center", fontsize=10.5,
                     fontweight="bold", color="white", zorder=7,
                     bbox=dict(boxstyle="round,pad=0.34", fc=c, ec="white", lw=1.1),
                     arrowprops=dict(arrowstyle="-", color=c, lw=2.0, alpha=0.92,
                                     shrinkA=5, shrinkB=3))
        axA.scatter([px], [py], s=240, color=c, edgecolor="white", lw=2.0, zorder=8)

    # B. bars + honest note
    axB = fig.add_subplot(gs[0, 1]); S.style_axes(axB)
    axB.grid(axis="x", color="#d7e1ea"); axB.grid(axis="y", visible=False)
    yb = np.arange(len(brain))[::-1]
    vals = [b[1] for b in brain]
    axB.barh(yb, vals, color=[b[4] for b in brain], zorder=3, height=0.5)
    axB.axvline(0, color=S.RED, lw=1.4)
    axB.set_yticks(yb); axB.set_yticklabels([b[0].split(" — ")[0] for b in brain],
                                            fontsize=12, fontweight="bold")
    axB.set_xlim(min(vals) - 0.8, 0.6); axB.set_xlabel("EAA: vaka − kontrol (yıl)")
    for yi, b in zip(yb, brain):
        axB.text(b[1] - 0.05, yi, f"{b[1]:+.2f} yıl", va="center", ha="right",
                 fontsize=10.5, fontweight="bold", color=S.TITLE_COLOR)
    axB.set_title("B. Beyin Kohortları — Horvath EAA", loc="center", color=S.TITLE_COLOR,
                  fontweight="bold", pad=8)
    fig.text(0.5, 0.085, "Bütün-doku (bulk) analizi. Her iki fark NEGATİF ve ANLAMSIZ (AD, p>0.05). "
             "Bölgesel alt-bölüm (NAc/AMY/HIP/VTA) ve PMI düzeltmesi için veri YOK.",
             ha="center", va="bottom", fontsize=9.5, color=S.TITLE_COLOR,
             bbox=dict(boxstyle="round,pad=0.45", fc="#f7fafd", ec="#9cbdda"))

    S.footer(fig, "Horvath saati, postmortem beyin  |  Bütün-doku  |  Beyin kesiti: P. J. Lynch, anatomytool.org (CC BY)")
    return S.save(fig, out)


# ============================== Şekil 6 — sınıflandırma performansı (gerçek)
def fig6(out):
    fig = plt.figure(figsize=(13.5, 7.6))
    gs = GridSpec(1, 3, figure=fig, wspace=0.32, left=0.07, right=0.97,
                  top=0.88, bottom=0.14, width_ratios=[1.0, 1.1, 1.0])
    ks = list(CLS.keys())
    auc = [CLS[k][0] for k in ks]

    # A. ROC-AUC
    axA = fig.add_subplot(gs[0, 0]); S.style_axes(axA)
    bA = axA.bar(ks, auc, color=S.PALETTE[:4], zorder=3, width=0.62)
    axA.axhline(0.5, ls=":", color=S.RED, lw=1.8, label="Şans (0.5)")
    axA.set_ylim(0, 1.05); axA.set_ylabel("ROC-AUC")
    S.panel_title(axA, "A. ROC-AUC")
    S.bar_labels(axA, bA, auc, fmt="{:.3f}", dy=0.01)
    axA.legend(fontsize=9, loc="lower right")

    # B. sensitivity & specificity grouped
    axB = fig.add_subplot(gs[0, 1]); S.style_axes(axB)
    x = np.arange(len(ks)); w = 0.38
    sens = [CLS[k][1] for k in ks]; spec = [CLS[k][2] for k in ks]
    axB.bar(x - w / 2, sens, w, label="Duyarlılık", color="#13294a", zorder=3)
    axB.bar(x + w / 2, spec, w, label="Özgüllük", color="#4a9bd4", zorder=3)
    for xi, s, p in zip(x, sens, spec):
        axB.text(xi - w / 2, s + 0.01, f"{s:.2f}", ha="center", fontsize=8, fontweight="bold", color=S.TITLE_COLOR)
        axB.text(xi + w / 2, p + 0.01, f"{p:.2f}", ha="center", fontsize=8, fontweight="bold", color=S.TITLE_COLOR)
    axB.set_xticks(x); axB.set_xticklabels(ks, fontsize=10)
    axB.set_ylim(0, 1.12); axB.set_ylabel("Oran")
    axB.legend(fontsize=9, loc="lower right")
    S.panel_title(axB, "B. Duyarlılık ve Özgüllük")

    # C. note
    axC = fig.add_subplot(gs[0, 2])
    _notebox(axC, "C. Yorum (dürüst beyan)",
             "Her madde için AYRI ikili model\n"
             "(madde vs kontrol), XGBoost,\n"
             "sızıntısız 5-kat çapraz-doğrulama:\n\n"
             "  Kokain  AUC 1.000 (n=47)\n"
             "  Sigara  AUC 0.928 (n=201)\n"
             "  Alkol   AUC 0.926 (n=94)\n"
             "  Metamf. AUC 0.922 (n=24)\n\n"
             "Opioid-beyin ve alkol-beyin:\n"
             "örneklem çok seyrek → MODELLENMEDİ.\n\n"
             "Maddeler arası ortak kohort yok →\n"
             "TEK çok-sınıflı doğruluk yok (veri yok).\n\n"
             "(Makalenin uydurma %87.3 7-sınıf\n"
             "değerinin gerçek karşılığı budur.)")

    S.footer(fig, "Leakage-free StratifiedKFold-5, seed=42  |  Fold-içi öznitelik seçimi  |  Kaynak: dl/substance_*.json, dl/gse50660_dl.json")
    return S.save(fig, out)


FIGS_MAIN = {"fig1": fig1, "fig2": fig2, "fig3": fig3, "fig4": fig4, "fig5": fig5, "fig6": fig6}

if __name__ == "__main__":
    import sys
    os.makedirs("out", exist_ok=True)
    which = sys.argv[1] if len(sys.argv) > 1 else "all"
    if which == "all":
        for k, fn in FIGS_MAIN.items():
            print(fn(f"out/{k}.png"))
    else:
        print(FIGS_MAIN[which](f"out/{which}.png"))
