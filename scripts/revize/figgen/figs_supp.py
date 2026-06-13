"""Supplementary figures Ek 1-8 (was S1-S8).
Data verbatim from makale.txt legends (1759-1885). Scatter/violin clouds are
deterministic renderings (fixed seed) of the REAL summary statistics — every
plotted significant point corresponds to a counted CpG; no invented summary numbers.
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import style as S
from figs_main import _table

SEED = 20260610


# ----------------------------------------------------------------------------- Ek 1
# Profesyonel iş-akisi (pipeline) diyagrami. TUM metin/sayilar makale.txt + tables.cjs
# kaynakli, BIREBIR korunur (sifir-halusinasyon): yalnizca gorsel tasarim yenilendi.
import matplotlib.patheffects as _pe

_W_NV    = "#0F2C4C"   # derin lacivert (ana dugumler)
_W_MD    = "#1F5C8B"   # orta mavi (paralel alt-surec)
_W_AC    = "#2E7CB8"   # vurgu mavisi (aksan cizgisi)
_W_TEAL  = "#0E7C7B"   # adim rozeti / sonuc vurgusu
_W_MODBG = "#EEF4F9"   # modul arka plani
_W_MODEC = "#BBD1E4"   # modul kenari
_W_SUBEC = "#CEDCEA"   # alt-kart kenari
_W_TXT   = "#16293D"   # koyu metin
_W_GREY  = "#64737F"   # gri alt-metin
_W_SPINE = "#5B86AD"   # ok / omurga rengi

_W_SHADOW = [_pe.withSimplePatchShadow(offset=(1.4, -1.8),
             shadow_rgbFace="#1d3550", alpha=0.20, rho=0.45)]


def _w_card(ax, cx, cy, w, h, fc, ec="none", lw=0, rs=1.3, shadow=True, z=3):
    p = FancyBboxPatch((cx - w / 2, cy - h / 2), w, h,
                       boxstyle="round,pad=0.02,rounding_size=%s" % rs,
                       fc=fc, ec=ec, lw=lw, zorder=z)
    if shadow:
        p.set_path_effects(_W_SHADOW)
    ax.add_patch(p)
    return p


def _w_badge(ax, x, y, n, r=2.25, fs=12.5):
    ax.add_patch(plt.Circle((x, y), r + 0.55, fc="white", ec="none", zorder=7))
    ax.add_patch(plt.Circle((x, y), r, fc=_W_TEAL, ec="none", zorder=8))
    ax.text(x, y, str(n), ha="center", va="center", color="white",
            fontweight="bold", fontsize=fs, zorder=9)


def _w_down(ax, x, y1, y2):
    ax.annotate("", xy=(x, y2), xytext=(x, y1),
                arrowprops=dict(arrowstyle="-|>", mutation_scale=20, color=_W_SPINE,
                                lw=2.6, shrinkA=0, shrinkB=0), zorder=2)


def _w_line(ax, x1, y1, x2, y2):
    ax.plot([x1, x2], [y1, y2], color=_W_SPINE, lw=2.5, zorder=2,
            solid_capstyle="round")


def _w_node(ax, cx, cy, w, h, num, title, sub, fc=_W_NV, tfs=13, sfs=10):
    _w_card(ax, cx, cy, w, h, fc, z=3)
    if sub:
        ax.text(cx, cy + h * 0.19, title, ha="center", va="center", color="white",
                fontweight="bold", fontsize=tfs, zorder=4)
        ax.text(cx, cy - h * 0.26, sub, ha="center", va="center", color="#dce8f3",
                fontsize=sfs, zorder=4)
    else:
        ax.text(cx, cy, title, ha="center", va="center", color="white",
                fontweight="bold", fontsize=tfs, zorder=4)
    _w_badge(ax, cx - w / 2, cy, num)


def _w_module(ax, x0, x1, y0, y1, num, title):
    _w_card(ax, (x0 + x1) / 2, (y0 + y1) / 2, x1 - x0, y1 - y0, _W_MODBG,
            ec=_W_MODEC, lw=1.3, rs=1.4, shadow=True, z=2)
    bh = 3.0
    cyb = y1 - bh / 2 - 0.5
    _w_card(ax, (x0 + x1) / 2, cyb, x1 - x0 - 1.4, bh, _W_NV, rs=0.9, shadow=False, z=3)
    ax.text((x0 + x1) / 2, cyb, title, ha="center", va="center", color="white",
            fontweight="bold", fontsize=12.5, zorder=4)
    _w_badge(ax, x0 + 4.2, cyb, num, r=1.9, fs=10.5)


def _w_sub(ax, cx, cy, w, h, title, sub, tfs=9.4, sfs=8.5):
    _w_card(ax, cx, cy, w, h, "white", ec=_W_SUBEC, lw=1.1, rs=0.8, shadow=False, z=4)
    ax.add_patch(plt.Rectangle((cx - w / 2 + 0.6, cy + h / 2 - 0.95), w - 1.2, 0.6,
                 fc=_W_AC, ec="none", zorder=5))
    ax.text(cx, cy + h * 0.08, title, ha="center", va="center", color=_W_TXT,
            fontweight="bold", fontsize=tfs, zorder=5)
    ax.text(cx, cy - h * 0.28, sub, ha="center", va="center", color=_W_GREY,
            fontsize=sfs, zorder=5)


def fig_s1(out):
    fig, ax = plt.subplots(figsize=(11, 15))
    ax.set_xlim(0, 100); ax.set_ylim(0, 100); ax.axis("off")

    # ust aksan seridi
    ax.add_patch(FancyBboxPatch((34, 96.3), 32, 1.4,
                 boxstyle="round,pad=0.02,rounding_size=0.7", fc=_W_AC, ec="none", zorder=3))

    # 1 - HAM VERI GIRISI
    _w_node(ax, 50, 91.4, 58, 5.8, 1, "HAM VERİ GİRİŞİ",
            "6 GEO Veri Seti (n=742)", tfs=13, sfs=10.2)
    _w_down(ax, 50, 88.3, 86.3)
    # 2 - IDAT DOSYA ISLEME
    _w_node(ax, 50, 83.2, 58, 5.4, 2, "IDAT DOSYA İŞLEME",
            "Illumina 450K/EPIC BeadChip Dizileri", tfs=13, sfs=10.2)
    _w_down(ax, 50, 80.4, 78.3)

    # 3 - KALITE KONTROL MODULU
    _w_module(ax, 6, 94, 64.6, 78.0, 3, "KALİTE KONTROL MODÜLÜ")
    qc = [("Tespit p-değeri", "<0.01 eşik"), ("Bisülfit Dönüşümü", ">%96 verim"),
          ("Cinsiyet Tahmini", "getSex() doğrulama"), ("Eksik Veri", "<%5 örnek başına")]
    for i, (t, s) in enumerate(qc):
        _w_sub(ax, 17.5 + i * 21.7, 69.4, 18.6, 8.2, t, s)
    _w_down(ax, 50, 64.4, 62.3)

    # 4 - PROB FILTRELEME
    _w_module(ax, 6, 94, 48.4, 61.8, 4, "PROB FİLTRELEME")
    pf = [("Çapraz-reaktif", "29.233 kaldırıldı"), ("SNP-etkilenen", "MAF>0.01"),
          ("Cinsiyet Kromozomları", "X/Y kaldırıldı"), ("Düşük Tespit", "p>0.01 filtrelendi")]
    for i, (t, s) in enumerate(pf):
        _w_sub(ax, 17.5 + i * 21.7, 53.2, 18.6, 8.2, t, s, tfs=8.9)

    # 4 -> (5,6) dallanma
    _w_line(ax, 50, 48.2, 50, 46.0)
    _w_line(ax, 28, 46.0, 72, 46.0)
    _w_down(ax, 28, 46.0, 44.4)
    _w_down(ax, 72, 46.0, 44.4)

    # 5 + 6 - NORMALIZASYON | BATCH DUZELTMESI (paralel)
    _w_node(ax, 28, 41.5, 40, 5.6, 5, "NORMALİZASYON", "Fonksiyonel Normalizasyon",
            fc=_W_MD, tfs=11.5, sfs=9.3)
    _w_node(ax, 72, 41.5, 40, 5.6, 6, "BATCH KONTROLÜ", "Kohort-içi (ComBat yok)",
            fc=_W_MD, tfs=11.5, sfs=9.3)
    ax.annotate("", xy=(51.6, 41.5), xytext=(48.4, 41.5),
                arrowprops=dict(arrowstyle="-|>", mutation_scale=15, color=_W_SPINE, lw=2.2), zorder=2)

    # (5,6) -> 7 birlesme
    _w_line(ax, 28, 38.7, 28, 36.8)
    _w_line(ax, 72, 38.7, 72, 36.8)
    _w_line(ax, 28, 36.8, 72, 36.8)
    _w_down(ax, 50, 36.8, 34.9)

    # 7 - HUCRE BILESIMI TAHMINI
    _w_node(ax, 50, 31.9, 62, 5.6, 7, "HÜCRE BİLEŞİMİ TAHMİNİ",
            "Houseman Referans-tabanlı Dekonvolüsyon (6 hücre tipi)", fc=_W_NV, tfs=12.5, sfs=9.4)
    _w_down(ax, 50, 29.1, 27.0)

    # 8 - EPIGENETIK SAAT HESAPLAMASI
    _w_module(ax, 6, 94, 12.8, 26.8, 8, "EPİGENETİK SAAT KÜTÜPHANESİ")
    clocks = [("Horvath", "353 CpG", "2013"), ("Hannum", "71 CpG", "2013"),
              ("PhenoAge", "513 CpG", "2018"), ("GrimAge", "1.030 CpG", "2019"),
              ("DunedinPACE", "173 CpG", "2022")]
    for i, (nm, cp, yr) in enumerate(clocks):
        cx = 15.8 + i * 16.85
        _w_card(ax, cx, 18.3, 15.2, 8.8, "white", ec=_W_SUBEC, lw=1.1, rs=0.8, shadow=False, z=4)
        ax.add_patch(plt.Rectangle((cx - 7.0, 21.75), 14.0, 0.6, fc=_W_AC, ec="none", zorder=5))
        ax.text(cx, 20.2, nm, ha="center", color=_W_TXT, fontweight="bold", fontsize=9.6, zorder=5)
        ax.text(cx, 17.9, cp, ha="center", color="#2f4a63", fontweight="bold", fontsize=9.2, zorder=5)
        ax.text(cx, 15.7, "(" + yr + ")", ha="center", color=_W_GREY, fontsize=8.4, zorder=5)
    _w_down(ax, 50, 12.6, 10.4)

    # 9 - ISTATISTIKSEL ANALIZ VE CIKTI
    _w_card(ax, 50, 5.7, 84, 8.6, _W_NV, rs=1.3, z=3)
    _w_badge(ax, 8, 5.7, 9)
    ax.text(50, 8.1, "İSTATİSTİKSEL ANALİZ VE ÇIKTI", ha="center", va="center",
            color="white", fontweight="bold", fontsize=13, zorder=5)
    _w_card(ax, 51, 3.6, 64, 3.0, _W_TEAL, rs=0.7, shadow=False, z=4)
    ax.text(51, 3.6, "Sonuç: n=742 örnek  |  6 GEO kohortu  |  Illumina 450K dizi  |  3 epigenetik saat",
            ha="center", va="center", color="white", fontweight="bold", fontsize=10.2, zorder=5)
    return S.save(fig, out)


# ----------------------------------------------------------------------------- Ek 2
def fig_s2(out):
    return _veri_yok_fig(out, (13.5, 6.6),
        "Ek 2. Kohortlar Arası Batch (Parti) Etkisi Düzeltmesi (ComBat)",
        "Bu çalışmada altı GEO kohortu tek bir mega-kohortta birleştirilmemiş,\n"
        "her biri kendi içinde ayrı analiz edilmiştir; kohortlar arası ComBat\n"
        "batch düzeltmesi UYGULANMAMIŞTIR.",
        "Düzeltme öncesi/sonrası PCA ve varyans oranları (ör. %32,4 -> %8,7) ile\n"
        "UK Biobank / MESA gibi veri setleri bu çalışmada KULLANILMAMIŞTIR.")


# ----------------------------------------------------------------------------- Ek 3
def fig_s3(out):
    return _veri_yok_fig(out, (14.5, 9.2),
        "Ek 3. Epigenetik Saat Kalibrasyonu",
        "GrimAge ve Ensemble saatleri bu çalışmada HESAPLANMAMIŞTIR; beş-saatli\n"
        "kalibrasyon karşılaştırması ve örnek düzeyi saçılım grafikleri üretilememektedir.",
        "Gerçek saat performansı yalnızca Horvath/Hannum/PhenoAge için ve kronolojik\n"
        "yaşı olan kohortlarda raporlanmıştır (ör. GSE50660: Horvath MAE=3,51 yıl,\n"
        "R\u00b2=0,586; bkz. ana metin saat tablosu).")


# ----------------------------------------------------------------------------- Ek 4
def fig_s4(out):
    import os, csv, math
    base = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "realdata", "out")
    cohorts = [
        ("Sigara", "GSE50660", "gse50660_dmp.csv"),
        ("Alkol (kan)", "GSE110043", "gse110043_dmp.csv"),
        ("Kokain", "GSE77056", "GSE77056_dmp.csv"),
        ("Metamfetamin", "GSE154971", "GSE154971_dmp.csv"),
        ("Alkol (beyin)", "GSE49393", "GSE49393_dmp.csv"),
        ("Opioid (beyin)", "GSE98203", "GSE98203_dmp.csv"),
    ]
    rng = np.random.default_rng(SEED)
    fig = plt.figure(figsize=(14.5, 9.4))
    gs = GridSpec(2, 3, figure=fig, hspace=0.36, wspace=0.24,
                  left=0.06, right=0.985, top=0.92, bottom=0.12)
    for i, (nm, gse, fname) in enumerate(cohorts):
        ax = fig.add_subplot(gs[i // 3, i % 3])
        gx = []; gy = []; hx = []; hy = []; lx = []; ly = []
        pcut = 0.0; ymax = 8.0; xm = 0.10
        with open(os.path.join(base, fname)) as fh:
            r = csv.reader(fh); next(r)
            for row in r:
                try:
                    d = float(row[1]); p = float(row[3]); fdr = float(row[4])
                except Exception:
                    continue
                if p <= 0:
                    continue
                y = -math.log10(p)
                if y > ymax: ymax = y
                if abs(d) > xm: xm = abs(d)
                if fdr < 0.05:
                    if p > pcut: pcut = p
                    if d >= 0: hx.append(d); hy.append(y)
                    else: lx.append(d); ly.append(y)
                else:
                    gx.append(d); gy.append(y)
        if len(gx) > 6000:
            idx = rng.choice(len(gx), 6000, replace=False)
            gx = [gx[j] for j in idx]; gy = [gy[j] for j in idx]
        nhyper = len(hx); nhypo = len(lx); nsig = nhyper + nhypo
        ax.scatter(gx, gy, s=5, color="#c4ccd4", alpha=0.40, edgecolors="none", zorder=2, rasterized=True)
        ax.scatter(lx, ly, s=10, color="#2e6db4", alpha=0.72, edgecolors="none", zorder=3, rasterized=True)
        ax.scatter(hx, hy, s=10, color="#c0392b", alpha=0.72, edgecolors="none", zorder=3, rasterized=True)
        if pcut > 0:
            ax.axhline(-math.log10(pcut), ls="--", color="#7a8896", lw=1.0, zorder=4)
        ax.axvline(0, ls="--", color="#aab7c4", lw=0.9, zorder=1)
        xlim = min(xm * 1.08, 0.6)
        ax.set_xlim(-xlim, xlim); ax.set_ylim(0, ymax * 1.08)
        for sp in ax.spines.values():
            sp.set_color(S.NAVY); sp.set_linewidth(1.4)
        ax.set_title(f"{nm} \u2014 {gse}\n(FDR<0,05: {nsig} CpG)", color=S.TITLE_COLOR, fontweight="bold", fontsize=11.5)
        ax.set_xlabel("\u0394\u03b2 (grup fark\u0131)"); ax.set_ylabel("-log10(p)")
        ax.text(0.97, 0.97, f"Hiper: {nhyper}\nHipo: {nhypo}", transform=ax.transAxes,
                ha="right", va="top", fontsize=8.6,
                bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="#9aa6b2"))
    handles = [plt.Line2D([0], [0], marker="o", ls="", color="#c0392b", ms=8, label="FDR<0,05 Hiper (\u0394\u03b2>0)"),
               plt.Line2D([0], [0], marker="o", ls="", color="#2e6db4", ms=8, label="FDR<0,05 Hipo (\u0394\u03b2<0)"),
               plt.Line2D([0], [0], marker="o", ls="", color="#c4ccd4", ms=8, label="Anlaml\u0131 de\u011fil")]
    fig.legend(handles=handles, loc="lower center", ncol=3, fontsize=10.5, frameon=True, bbox_to_anchor=(0.5, 0.006))
    return S.save(fig, out)


# ----------------------------------------------------------------------------- Ek 5
# ----------------------------------------------------------------------------- Ek 5-8
# Zero-Hallucination: the analyses these figures originally depicted (physiological
# mediation, psychological moderation, postmortem PMI correction, region-resolved
# brain EAA) require individual-level data that does NOT exist in the public
# DNA-methylation cohorts used here. No numbers or plots are invented; each figure
# states honestly that the required data is unavailable.
def _veri_yok_fig(out, figsize, title, missing, note):
    fig = plt.figure(figsize=figsize)
    ax = fig.add_axes([0.03, 0.04, 0.94, 0.92]); ax.axis("off")
    ax.set_xlim(0, 100); ax.set_ylim(0, 100)
    ax.text(50, 92, title, ha="center", va="center", color=S.TITLE_COLOR,
            fontweight="bold", fontsize=15)
    ax.add_patch(FancyBboxPatch((12, 40), 76, 30,
                 boxstyle="round,pad=0.5,rounding_size=2.5",
                 fc="#fbf2f1", ec=S.RED, lw=2.6, zorder=2))
    ax.text(50, 62, "VERİ YOK / KAYNAK GEREKLİ", ha="center", va="center",
            color=S.RED, fontweight="bold", fontsize=19, zorder=3)
    ax.text(50, 50, missing, ha="center", va="center", color=S.TITLE_COLOR,
            fontsize=11, zorder=3, linespacing=1.5)
    ax.text(50, 24, note, ha="center", va="center", color=S.GREY_TXT,
            fontsize=10.5, zorder=3, linespacing=1.5, style="italic")
    S.footer(fig, "Zero-Hallucination politikası: doğrulanamayan analizler için "
                  "sayı veya grafik üretilmemiştir.")
    return S.save(fig, out)


def fig_s5(out):
    return _veri_yok_fig(out, (14.5, 6.2),
        "Ek 5. Madde Kullanım Süresi \u2192 GrimAge EAA: Aracılık (Mediasyon) Modeli",
        "Aracılık analizi için gereken bireysel düzey mediatör ölçümleri\n"
        "(HOMA-IR / insülin direnci, kortizol\u2013ACTH / HPA ekseni, "
        "CRP\u2013IL-6 / inflamasyon)\n"
        "kamuya açık DNA metilasyon kohortlarında bulunmamaktadır.",
        "Yol katsayıları (a, b, c\u2032) ve aracılık yüzdeleri bu çalışmanın "
        "verisiyle hesaplanamamıştır;\n"
        "bu mekanizmalar yalnızca literatürde hipotez düzeyinde tartışılmaktadır.")


def fig_s6(out):
    return _veri_yok_fig(out, (14.0, 6.6),
        "Ek 6. Psikolojik Dayanıklılığın Moderasyon (Düzenleyici) Rolü",
        "Moderasyon analizi için gereken psikolojik ölçek verileri\n"
        "(DERS \u2014 Duygu Düzenleme Güçlükleri, SCS-B \u2014 Öz-Kontrol)\n"
        "kamuya açık DNA metilasyon kohortlarında bulunmamaktadır.",
        "Etkileşim katsayıları, Johnson\u2013Neyman eşikleri ve \u0394R\u00b2 "
        "değerleri\nbu çalışmanın verisiyle hesaplanamamıştır.")


def fig_s7(out):
    return _veri_yok_fig(out, (15.0, 5.6),
        "Ek 7. Postmortem Aralık (PMI) Düzeltmesi",
        "PMI düzeltmesi için gereken postmortem beyin dokusu verileri\n"
        "(PMI saati, doku pH değeri, eşleştirilmiş yaş tahmin hataları)\n"
        "bu çalışmada mevcut değildir.",
        "Düzeltme öncesi/sonrası MAE, R\u00b2 ve kalibrasyon değerleri veri "
        "olmadan\nhesaplanamamıştır (krş. PMI ve doku pH tabloları \u2014 "
        "veri yok / kaynak gerekli).")


def fig_s8(out):
    return _veri_yok_fig(out, (13.0, 8.6),
        "Ek 8. Beyin Bölgesine Özgü Epigenetik Yaş Hızlanması",
        "Bölgeye özgü (prefrontal korteks, nükleus akumbens, hipokampus)\n"
        "epigenetik yaş hızlanması için gereken bölge-ayrıştırılmış metilasyon "
        "verisi\nbu çalışmada mevcut değildir.",
        "Mevcut beyin dokusu kohortu bütün-doku düzeyindedir; bölgesel ANOVA, "
        "Tukey HSD\nve bölge ortalamaları hesaplanamamıştır.")


FIGS_SUPP = {"s1": fig_s1, "s2": fig_s2, "s3": fig_s3, "s4": fig_s4,
             "s5": fig_s5, "s6": fig_s6, "s7": fig_s7, "s8": fig_s8}


if __name__ == "__main__":
    import os, sys
    os.makedirs("out", exist_ok=True)
    which = sys.argv[1] if len(sys.argv) > 1 else "all"
    targets = FIGS_SUPP if which == "all" else {which: FIGS_SUPP[which]}
    for name, fn in targets.items():
        print(fn(f"out/{name}.png"))
