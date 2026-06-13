# One-shot surgical replace of fabricated s5-s8 figure functions with honest
# "veri yok" placeholders. Run once from figgen/, then delete.
import io

P = "figs_supp.py"
src = io.open(P, encoding="utf-8").read()
start = src.index("def _med_panel(")
endmark = "FIGS_SUPP = {"
end = src.index(endmark)
assert 0 < start < end, "markers not found"

NEW = '''# ----------------------------------------------------------------------------- Ek 5-8
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
        "Ek 5. Madde Kullanım Süresi \\u2192 GrimAge EAA: Aracılık (Mediasyon) Modeli",
        "Aracılık analizi için gereken bireysel düzey mediatör ölçümleri\\n"
        "(HOMA-IR / insülin direnci, kortizol\\u2013ACTH / HPA ekseni, "
        "CRP\\u2013IL-6 / inflamasyon)\\n"
        "kamuya açık DNA metilasyon kohortlarında bulunmamaktadır.",
        "Yol katsayıları (a, b, c\\u2032) ve aracılık yüzdeleri bu çalışmanın "
        "verisiyle hesaplanamamıştır;\\n"
        "bu mekanizmalar yalnızca literatürde hipotez düzeyinde tartışılmaktadır.")


def fig_s6(out):
    return _veri_yok_fig(out, (14.0, 6.6),
        "Ek 6. Psikolojik Dayanıklılığın Moderasyon (Düzenleyici) Rolü",
        "Moderasyon analizi için gereken psikolojik ölçek verileri\\n"
        "(DERS \\u2014 Duygu Düzenleme Güçlükleri, SCS-B \\u2014 Öz-Kontrol)\\n"
        "kamuya açık DNA metilasyon kohortlarında bulunmamaktadır.",
        "Etkileşim katsayıları, Johnson\\u2013Neyman eşikleri ve \\u0394R\\u00b2 "
        "değerleri\\nbu çalışmanın verisiyle hesaplanamamıştır.")


def fig_s7(out):
    return _veri_yok_fig(out, (15.0, 5.6),
        "Ek 7. Postmortem Aralık (PMI) Düzeltmesi",
        "PMI düzeltmesi için gereken postmortem beyin dokusu verileri\\n"
        "(PMI saati, doku pH değeri, eşleştirilmiş yaş tahmin hataları)\\n"
        "bu çalışmada mevcut değildir.",
        "Düzeltme öncesi/sonrası MAE, R\\u00b2 ve kalibrasyon değerleri veri "
        "olmadan\\nhesaplanamamıştır (krş. PMI ve doku pH tabloları \\u2014 "
        "veri yok / kaynak gerekli).")


def fig_s8(out):
    return _veri_yok_fig(out, (13.0, 8.6),
        "Ek 8. Beyin Bölgesine Özgü Epigenetik Yaş Hızlanması",
        "Bölgeye özgü (prefrontal korteks, nükleus akumbens, hipokampus)\\n"
        "epigenetik yaş hızlanması için gereken bölge-ayrıştırılmış metilasyon "
        "verisi\\nbu çalışmada mevcut değildir.",
        "Mevcut beyin dokusu kohortu bütün-doku düzeyindedir; bölgesel ANOVA, "
        "Tukey HSD\\nve bölge ortalamaları hesaplanamamıştır.")


'''

src2 = src[:start] + NEW + src[end:]
io.open(P, "w", encoding="utf-8").write(src2)
print("OK rewrote figs_supp.py; new length", len(src2))
