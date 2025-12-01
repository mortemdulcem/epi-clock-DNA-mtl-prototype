"""
EpiClock Academic User Guide Module
Comprehensive documentation and tutorials for researchers

Author: Dr. Nurcan Denli Bayır
"""

import streamlit as st
from datetime import datetime
from typing import Dict, List, Optional

GUIDE_VERSION = "1.0.0"
LAST_UPDATED = "2024-12-01"

EPICLOCK_MODULES = {
    "dna_upload": {
        "name": "DNA Verisi Yükleme",
        "icon": "📤",
        "description": "Illumina 450K/EPIC array verilerinizi platforma yükleyin",
        "steps": [
            "CSV, TXT veya Excel formatında beta değerleri hazırlayın",
            "İlk sütunda CpG ID'leri (cg00000029 formatında) olmalı",
            "Diğer sütunlar örnek beta değerlerini içermeli (0-1 arası)",
            "Dosyayı yükleyin ve platform seçin (450K veya EPIC)",
            "Otomatik kalite kontrolü sonuçlarını inceleyin"
        ],
        "output": "Normalize edilmiş beta değerleri ve kalite raporu",
        "tips": [
            "Beta değerleri 0-1 arasında olmalıdır",
            "Eksik değerler için NA kullanın",
            "En az 5000 CpG sitesi önerilir"
        ]
    },
    "cpg_database": {
        "name": "CpG Veritabanı",
        "icon": "🧬",
        "description": "29,716 bağımlılık-ilişkili CpG sitesi veritabanı",
        "steps": [
            "Madde panellerinden ilgili substance seçin",
            "CpG veya gen adıyla arama yapın",
            "Kanıt düzeylerine göre filtreleme uygulayın",
            "Sonuçları CSV, BED, JSON veya SQL formatında dışa aktarın"
        ],
        "output": "CpG siteleri, genomik koordinatlar, p-değerleri",
        "tips": [
            "BED formatı genome browser'larda (UCSC, IGV) görüntüleme için idealdir",
            "JSON formatı programatik erişim için uygundur",
            "SQL şeması kendi veritabanınızı oluşturmak için kullanılabilir"
        ]
    },
    "variant_analysis": {
        "name": "Varyant Analizi",
        "icon": "🔬",
        "description": "Genetik varyantların bağımlılık riskiyle ilişkisini analiz edin",
        "steps": [
            "VCF dosyası veya SNP listesi yükleyin",
            "GWAS veritabanlarıyla karşılaştırma yapın",
            "Fonksiyonel anotasyon sonuçlarını inceleyin",
            "Risk skorlarını hesaplayın"
        ],
        "output": "Varyant anotasyonları, GWAS p-değerleri, risk skorları",
        "tips": [
            "gnomAD frekansları popülasyon karşılaştırması için kullanılır",
            "CADD skorları fonksiyonel önem göstergesidir"
        ]
    },
    "pharmacogenomics": {
        "name": "Farmakogenomik",
        "icon": "💊",
        "description": "İlaç-gen etkileşimlerini ve dozaj önerilerini analiz edin",
        "steps": [
            "Hastanın genotip verilerini girin",
            "İlgili ilaçları seçin (metadon, naltrexone, buprenorfin vb.)",
            "PharmGKB ve CPIC yönergelerini inceleyin",
            "Kişiselleştirilmiş dozaj önerilerini alın"
        ],
        "output": "Metabolizör fenotipi, dozaj önerileri, ilaç etkileşimleri",
        "tips": [
            "CYP2D6 ve CYP2C19 opioid metabolizması için kritiktir",
            "OPRM1 A118G polimorfizmi naltrexone yanıtını etkiler"
        ]
    },
    "prs_analysis": {
        "name": "Poligenik Risk Skoru",
        "icon": "📊",
        "description": "Çoklu varyantları kullanarak bağımlılık risk skorunu hesaplayın",
        "steps": [
            "Genotip verilerini yükleyin",
            "Risk özelliği seçin (alkol, nikotin, opioid vb.)",
            "PRS hesaplamasını başlatın",
            "Popülasyon normlarıyla karşılaştırın"
        ],
        "output": "PRS skoru, persentil, risk kategorisi",
        "tips": [
            "PRS tek başına tanı aracı değildir",
            "Çevresel faktörlerle birlikte değerlendirilmelidir"
        ]
    },
    "world_databases": {
        "name": "Dünya Veritabanları",
        "icon": "🌍",
        "description": "GWAS, EWAS, PharmGKB ve GEO veritabanlarına erişim",
        "steps": [
            "Veritabanı sekmesini seçin",
            "Anahtar kelime veya gen adıyla arama yapın",
            "Çalışma detaylarını inceleyin",
            "Verileri dışa aktarın"
        ],
        "output": "Çalışma listesi, SNP/CpG verileri, referanslar",
        "tips": [
            "GWAS Catalog en güncel genom-çapı çalışmaları içerir",
            "EWAS Catalog epigenetik belirteçler için ana kaynaktır"
        ]
    },
    "epigenetic_clocks": {
        "name": "Epigenetik Saatler",
        "icon": "⏰",
        "description": "5 farklı saatle biyolojik yaş hesaplaması",
        "steps": [
            "DNA metilasyon verisini yükleyin",
            "Hesaplanacak saatleri seçin",
            "Kronolojik yaşı girin",
            "Epigenetik Yaş İvmelenmesi (EAA) sonuçlarını inceleyin"
        ],
        "output": "Biyolojik yaş, EAA, saat-spesifik sonuçlar",
        "tips": [
            "GrimAge mortalite tahmini için en güçlü prediktördür",
            "DunedinPACE yaşlanma hızını ölçer"
        ]
    },
    "tissue_clocks": {
        "name": "Doku-Spesifik Saatler",
        "icon": "🫀",
        "description": "12 farklı doku tipi için optimize edilmiş saatler",
        "steps": [
            "Doku tipini seçin (beyin, karaciğer, kan vb.)",
            "Metilasyon verisini yükleyin",
            "Doku-spesifik yaş hesaplamasını başlatın",
            "Çapraz-doku karşılaştırmasını inceleyin"
        ],
        "output": "Doku yaşı, diskordans analizi",
        "tips": [
            "Karaciğer saati alkol hasarını tespit etmede hassastır",
            "Beyin saatleri nörodejenerasyonu erken tespit edebilir"
        ]
    }
}

EPIGENETIC_CLOCKS_INFO = {
    "horvath": {
        "name": "Horvath Multi-tissue Clock",
        "year": 2013,
        "n_cpg": 353,
        "tissue": "Çoklu doku",
        "description": "İlk pan-doku epigenetik saat. Tüm doku tipleri için kalibre edilmiş.",
        "mae": 3.6,
        "r2": 0.96,
        "pmid": "24138928",
        "use_case": "Genel biyolojik yaş tahmini, doku-bağımsız çalışmalar"
    },
    "hannum": {
        "name": "Hannum Blood Clock",
        "year": 2013,
        "n_cpg": 71,
        "tissue": "Kan",
        "description": "Kan örnekleri için optimize edilmiş. Kompakt CpG seti.",
        "mae": 4.9,
        "r2": 0.91,
        "pmid": "23177740",
        "use_case": "Kan bazlı çalışmalar, klinik uygulamalar"
    },
    "phenoage": {
        "name": "PhenoAge",
        "year": 2018,
        "n_cpg": 513,
        "tissue": "Kan",
        "description": "Mortalite ve morbidite tahmini için optimize edilmiş.",
        "mae": 2.8,
        "r2": 0.94,
        "pmid": "29676998",
        "use_case": "Hastalık riski, mortalite tahmini"
    },
    "grimage": {
        "name": "GrimAge",
        "year": 2019,
        "n_cpg": 1030,
        "tissue": "Kan",
        "description": "En güçlü mortalite prediktörü. Sigara ve plazma proteinlerini içerir.",
        "mae": 2.1,
        "r2": 0.96,
        "pmid": "30669119",
        "use_case": "Yaşam süresi tahmini, sigara etkisi"
    },
    "dunedinpace": {
        "name": "DunedinPACE",
        "year": 2022,
        "n_cpg": 173,
        "tissue": "Kan",
        "description": "Yaşlanma hızını ölçer. Longitudinal verilerden türetilmiş.",
        "mae": None,
        "r2": None,
        "pmid": "35029144",
        "use_case": "Yaşlanma hızı, müdahale etkinliği"
    }
}

SUBSTANCE_EAA_EFFECTS = {
    "polysubstance": {"eaa": 7.3, "ci_low": 6.4, "ci_high": 8.3, "name": "Çoklu Madde"},
    "methamphetamine": {"eaa": 6.2, "ci_low": 4.5, "ci_high": 8.1, "name": "Metamfetamin"},
    "cocaine": {"eaa": 4.1, "ci_low": 3.5, "ci_high": 4.7, "name": "Kokain"},
    "alcohol": {"eaa": 3.6, "ci_low": 3.1, "ci_high": 4.2, "name": "Alkol"},
    "opioid": {"eaa": 2.9, "ci_low": 2.5, "ci_high": 3.4, "name": "Opioid"},
    "cannabis": {"eaa": 0.8, "ci_low": 0.3, "ci_high": 1.4, "name": "Esrar"}
}

ACADEMIC_REFERENCES = [
    {
        "authors": "Horvath S",
        "title": "DNA methylation age of human tissues and cell types",
        "journal": "Genome Biology",
        "year": 2013,
        "volume": "14(10)",
        "pages": "R115",
        "pmid": "24138928",
        "doi": "10.1186/gb-2013-14-10-r115",
        "category": "Epigenetic Clocks"
    },
    {
        "authors": "Hannum G, Guinney J, Zhao L, et al.",
        "title": "Genome-wide methylation profiles reveal quantitative views of human aging rates",
        "journal": "Molecular Cell",
        "year": 2013,
        "volume": "49(2)",
        "pages": "359-367",
        "pmid": "23177740",
        "doi": "10.1016/j.molcel.2012.10.016",
        "category": "Epigenetic Clocks"
    },
    {
        "authors": "Levine ME, Lu AT, Quach A, et al.",
        "title": "An epigenetic biomarker of aging for lifespan and healthspan",
        "journal": "Aging",
        "year": 2018,
        "volume": "10(4)",
        "pages": "573-591",
        "pmid": "29676998",
        "doi": "10.18632/aging.101414",
        "category": "Epigenetic Clocks"
    },
    {
        "authors": "Lu AT, Quach A, Wilson JG, et al.",
        "title": "DNA methylation GrimAge strongly predicts lifespan and healthspan",
        "journal": "Aging",
        "year": 2019,
        "volume": "11(2)",
        "pages": "303-327",
        "pmid": "30669119",
        "doi": "10.18632/aging.101684",
        "category": "Epigenetic Clocks"
    },
    {
        "authors": "Belsky DW, Caspi A, Corcoran DL, et al.",
        "title": "DunedinPACE, a DNA methylation biomarker of the pace of aging",
        "journal": "eLife",
        "year": 2022,
        "volume": "11",
        "pages": "e73420",
        "pmid": "35029144",
        "doi": "10.7554/eLife.73420",
        "category": "Epigenetic Clocks"
    },
    {
        "authors": "Dugué PA, Bassett JK, Joo JE, et al.",
        "title": "Association of DNA Methylation-Based Biological Age With Health Risk Factors and Overall and Cause-Specific Mortality",
        "journal": "American Journal of Epidemiology",
        "year": 2018,
        "volume": "187(3)",
        "pages": "529-538",
        "pmid": "29020168",
        "doi": "10.1093/aje/kwx291",
        "category": "Epidemiology"
    },
    {
        "authors": "Beach SRH, Dogan MV, Lei MK, et al.",
        "title": "Methylomic Aging as a Window onto the Influence of Lifestyle: Tobacco and Alcohol Use Alter the Rate of Biological Aging",
        "journal": "Journal of the American Geriatrics Society",
        "year": 2015,
        "volume": "63(12)",
        "pages": "2519-2525",
        "pmid": "26566992",
        "doi": "10.1111/jgs.13830",
        "category": "Substance Use"
    },
    {
        "authors": "Rosen AD, Robertson KD, Hlady RA, et al.",
        "title": "DNA methylation age is accelerated in alcohol dependence",
        "journal": "Translational Psychiatry",
        "year": 2018,
        "volume": "8(1)",
        "pages": "182",
        "pmid": "30185788",
        "doi": "10.1038/s41398-018-0233-4",
        "category": "Substance Use"
    },
    {
        "authors": "Joehanes R, Just AC, Marioni RE, et al.",
        "title": "Epigenetic Signatures of Cigarette Smoking",
        "journal": "Circulation: Cardiovascular Genetics",
        "year": 2016,
        "volume": "9(5)",
        "pages": "436-447",
        "pmid": "27651444",
        "doi": "10.1161/CIRCGENETICS.116.001506",
        "category": "Tobacco/Nicotine"
    },
    {
        "authors": "Zeilinger S, Kühnel B, Klopp N, et al.",
        "title": "Tobacco smoking leads to extensive genome-wide changes in DNA methylation",
        "journal": "PLoS ONE",
        "year": 2013,
        "volume": "8(5)",
        "pages": "e63812",
        "pmid": "23691101",
        "doi": "10.1371/journal.pone.0063812",
        "category": "Tobacco/Nicotine"
    }
]

GLOSSARY_TERMS = {
    "Epigenetik": "DNA dizisini değiştirmeden gen ekspresyonunu düzenleyen mekanizmalar",
    "DNA Metilasyon": "Sitozin bazına metil grubu eklenmesi, genellikle CpG dinükleotidlerinde",
    "CpG Sitesi": "Sitozin-fosfat-guanin dinükleotidi, DNA metilasyonunun ana hedefi",
    "Beta Değeri": "Metilasyon oranı (0=metilasyonsuz, 1=tam metilasyon)",
    "EAA (Epigenetic Age Acceleration)": "Biyolojik yaş - kronolojik yaş farkı",
    "Epigenetik Saat": "CpG metilasyonundan biyolojik yaş tahmin eden algoritma",
    "GWAS": "Genom-çapı ilişkilendirme çalışması (Genome-Wide Association Study)",
    "EWAS": "Epigenom-çapı ilişkilendirme çalışması (Epigenome-Wide Association Study)",
    "SNP": "Tek nükleotid polimorfizmi, DNA'daki tek baz varyasyonu",
    "PRS": "Poligenik risk skoru, çoklu varyantların kümülatif etkisi",
    "MAE": "Ortalama mutlak hata (Mean Absolute Error)",
    "R²": "Determinasyon katsayısı, model açıklayıcılığı",
    "Horvath Clock": "İlk pan-doku epigenetik saat (353 CpG)",
    "GrimAge": "Mortalite-optimized epigenetik saat (1030 CpG)",
    "DunedinPACE": "Yaşlanma hızını ölçen en yeni saat",
    "PharmGKB": "Farmakogenomik bilgi veritabanı",
    "CPIC": "Klinik Farmakogenetik Uygulama Konsorsiyumu"
}


def render_academic_guide():
    """Render the comprehensive academic user guide"""
    
    st.markdown("## 📚 EpiClock Akademik Kullanım Kılavuzu")
    
    st.markdown(f"""
    <div class="info-box">
    <b>🎓 Araştırmacılar İçin Kapsamlı Rehber</b><br>
    Bu kılavuz, EpiClock platformunun tüm özelliklerini akademik araştırmacılar için detaylı şekilde açıklar.
    Versiyon: {GUIDE_VERSION} | Son Güncelleme: {LAST_UPDATED}
    </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "📖 Platform Rehberi",
        "⏰ Epigenetik Saatler",
        "📊 Veri Formatları",
        "🔬 Metodoloji",
        "📚 Referanslar",
        "📝 Terimler Sözlüğü"
    ])
    
    with tab1:
        render_platform_guide()
    
    with tab2:
        render_clocks_guide()
    
    with tab3:
        render_data_formats_guide()
    
    with tab4:
        render_methodology_guide()
    
    with tab5:
        render_references_section()
    
    with tab6:
        render_glossary()


def render_platform_guide():
    """Render platform module guide"""
    
    st.markdown("### 🖥️ Platform Modülleri")
    
    st.markdown("""
    EpiClock, DNA metilasyon verilerini kullanarak epigenetik yaş ivmelenmesini tespit eden 
    kapsamlı bir araştırma platformudur. Aşağıda her modülün detaylı kullanım kılavuzunu bulabilirsiniz.
    """)
    
    for module_id, module in EPICLOCK_MODULES.items():
        with st.expander(f"{module['icon']} {module['name']}", expanded=False):
            st.markdown(f"**Açıklama:** {module['description']}")
            
            st.markdown("**Adım Adım Kullanım:**")
            for i, step in enumerate(module['steps'], 1):
                st.markdown(f"{i}. {step}")
            
            st.markdown(f"**Çıktı:** {module['output']}")
            
            st.markdown("**İpuçları:**")
            for tip in module['tips']:
                st.markdown(f"• {tip}")


def render_clocks_guide():
    """Render epigenetic clocks detailed guide"""
    
    st.markdown("### ⏰ Epigenetik Saatler Karşılaştırması")
    
    import plotly.express as px
    import pandas as pd
    
    clock_data = []
    for clock_id, clock in EPIGENETIC_CLOCKS_INFO.items():
        clock_data.append({
            'Saat': clock['name'],
            'Yıl': clock['year'],
            'CpG Sayısı': clock['n_cpg'],
            'MAE (yıl)': clock['mae'] if clock['mae'] else 'N/A',
            'R²': clock['r2'] if clock['r2'] else 'N/A',
            'Doku': clock['tissue'],
            'PMID': clock['pmid']
        })
    
    clock_df = pd.DataFrame(clock_data)
    st.dataframe(clock_df, use_container_width=True, hide_index=True)
    
    st.markdown("### 📈 Madde Bazlı EAA Etkileri (GrimAge)")
    
    eaa_data = []
    for substance, data in SUBSTANCE_EAA_EFFECTS.items():
        eaa_data.append({
            'Madde': data['name'],
            'EAA (yıl)': data['eaa'],
            'CI Alt': data['ci_low'],
            'CI Üst': data['ci_high']
        })
    
    eaa_df = pd.DataFrame(eaa_data).sort_values('EAA (yıl)', ascending=False)
    
    fig = px.bar(eaa_df, x='Madde', y='EAA (yıl)', 
                 error_y=eaa_df['CI Üst'] - eaa_df['EAA (yıl)'],
                 error_y_minus=eaa_df['EAA (yıl)'] - eaa_df['CI Alt'],
                 title='Madde Türüne Göre Epigenetik Yaş İvmelenmesi',
                 color='EAA (yıl)',
                 color_continuous_scale='Reds')
    fig.update_layout(template='plotly_white', height=400)
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("### 🔬 Saat Detayları")
    
    for clock_id, clock in EPIGENETIC_CLOCKS_INFO.items():
        with st.expander(f"⏰ {clock['name']} ({clock['year']})"):
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"""
                - **CpG Sayısı:** {clock['n_cpg']}
                - **Doku Tipi:** {clock['tissue']}
                - **MAE:** {clock['mae']} yıl
                - **R²:** {clock['r2']}
                """)
            with col2:
                st.markdown(f"""
                - **PMID:** [{clock['pmid']}](https://pubmed.ncbi.nlm.nih.gov/{clock['pmid']}/)
                - **Kullanım Alanı:** {clock['use_case']}
                """)
            st.markdown(f"**Açıklama:** {clock['description']}")


def render_data_formats_guide():
    """Render data formats and export guide"""
    
    st.markdown("### 📊 Veri Formatları ve Dışa Aktarım")
    
    st.markdown("""
    EpiClock, verilerinizi farklı formatlarda dışa aktarmanıza olanak tanır. 
    Her format farklı kullanım senaryoları için optimize edilmiştir.
    """)
    
    format_info = {
        "CSV": {
            "icon": "📄",
            "description": "Virgülle ayrılmış değerler - Excel ve istatistik yazılımları için ideal",
            "use_case": "Veri analizi, R/Python işleme, tablo görüntüleme",
            "software": "Excel, R, Python (pandas), SPSS, SAS"
        },
        "BED": {
            "icon": "🧬",
            "description": "Browser Extensible Data - Genom tarayıcıları için standart format",
            "use_case": "UCSC Genome Browser, IGV, genomik görselleştirme",
            "software": "UCSC Genome Browser, IGV, Ensembl, bedtools"
        },
        "JSON": {
            "icon": "📋",
            "description": "JavaScript Object Notation - Programatik erişim ve API entegrasyonu",
            "use_case": "Web uygulamaları, API'ler, veri alışverişi",
            "software": "JavaScript, Python, R (jsonlite), web servisleri"
        },
        "SQL": {
            "icon": "🗄️",
            "description": "Yapılandırılmış Sorgu Dili - İlişkisel veritabanı şeması",
            "use_case": "Kendi veritabanınızı oluşturma, kurumsal entegrasyon",
            "software": "PostgreSQL, MySQL, SQLite, SQL Server"
        }
    }
    
    for fmt, info in format_info.items():
        with st.expander(f"{info['icon']} {fmt} Formatı"):
            st.markdown(f"**Açıklama:** {info['description']}")
            st.markdown(f"**Kullanım Alanı:** {info['use_case']}")
            st.markdown(f"**Uyumlu Yazılımlar:** {info['software']}")
    
    st.markdown("### 📥 Örnek Veri Yapıları")
    
    st.markdown("#### CSV Örneği")
    st.code("""cpg_id,gene,chromosome,delta_beta,p_value,evidence_level
cg05575921,AHRR,chr5,-0.15,1e-50,Strong
cg03636183,F2RL3,chr19,-0.12,1e-45,Strong
cg19859270,GPR15,chr3,0.08,1e-30,Moderate""", language="csv")
    
    st.markdown("#### BED Örneği")
    st.code("""chr5	373378	373379	cg05575921	1000	+	AHRR	tobacco	Strong
chr19	17000585	17000586	cg03636183	950	+	F2RL3	tobacco	Strong
chr3	98250620	98250621	cg19859270	800	+	GPR15	tobacco	Moderate""", language="text")
    
    st.markdown("#### JSON Örneği")
    st.code("""{
  "metadata": {
    "version": "1.0.0",
    "author": "Dr. Nurcan Denli Bayır"
  },
  "cpg_markers": [
    {
      "cpg_id": "cg05575921",
      "gene": "AHRR",
      "delta_beta": -0.15,
      "evidence": "Strong"
    }
  ]
}""", language="json")


def render_methodology_guide():
    """Render methodology and statistical analysis guide"""
    
    st.markdown("### 🔬 Metodoloji ve İstatistiksel Analiz")
    
    st.markdown("""
    #### Epigenetik Yaş Hesaplama
    
    Epigenetik yaş, DNA metilasyon beta değerlerinin lineer kombinasyonu olarak hesaplanır:
    """)
    
    st.latex(r"DNAm\_Age = \sum_{i=1}^{n} \beta_i \times w_i + intercept")
    
    st.markdown("""
    Burada:
    - **βᵢ**: i. CpG sitesinin beta değeri (metilasyon oranı)
    - **wᵢ**: i. CpG sitesinin ağırlığı (saat katsayısı)
    - **n**: Saatin kullandığı toplam CpG sayısı
    
    #### Epigenetik Yaş İvmelenmesi (EAA)
    """)
    
    st.latex(r"EAA = DNAm\_Age - Chronological\_Age")
    
    st.markdown("""
    **Yorumlama:**
    - **EAA > 0**: Biyolojik olarak kronolojik yaştan daha yaşlı (hızlı yaşlanma)
    - **EAA < 0**: Biyolojik olarak kronolojik yaştan daha genç (yavaş yaşlanma)
    - **EAA = 0**: Biyolojik yaş kronolojik yaşa eşit
    
    #### Kalite Kontrol Kriterleri
    
    | Parametre | Eşik Değer | Açıklama |
    |-----------|------------|----------|
    | Beta Aralığı | 0-1 | Geçerli metilasyon değerleri |
    | Eksik Veri | <5% | Maksimum izin verilen eksik CpG |
    | CpG Kapsam | >95% | Saat CpG'lerinin minimum kapsanması |
    | Batch Etkisi | p>0.05 | ComBat normalizasyonu sonrası |
    
    #### İstatistiksel Testler
    
    - **t-testi**: Grup karşılaştırmaları (örn: bağımlı vs kontrol)
    - **ANOVA**: Çoklu grup karşılaştırmaları
    - **Regresyon**: EAA ile kovaryatlar arasındaki ilişki
    - **Mediyasyon Analizi**: Dolaylı etkiler
    """)


def render_references_section():
    """Render academic references"""
    
    st.markdown("### 📚 Akademik Referanslar")
    
    categories = set(ref['category'] for ref in ACADEMIC_REFERENCES)
    
    for category in sorted(categories):
        st.markdown(f"#### {category}")
        
        refs_in_category = [r for r in ACADEMIC_REFERENCES if r['category'] == category]
        
        for ref in refs_in_category:
            st.markdown(f"""
            **{ref['authors']}** ({ref['year']})  
            *{ref['title']}*  
            {ref['journal']}. {ref['volume']}:{ref['pages']}.  
            PMID: [{ref['pmid']}](https://pubmed.ncbi.nlm.nih.gov/{ref['pmid']}/) | 
            DOI: [{ref['doi']}](https://doi.org/{ref['doi']})
            
            ---
            """)


def render_glossary():
    """Render glossary of terms"""
    
    st.markdown("### 📝 Terimler Sözlüğü")
    
    search_term = st.text_input("Terim ara:", placeholder="Örn: epigenetik, GWAS, CpG")
    
    for term, definition in sorted(GLOSSARY_TERMS.items()):
        if search_term.lower() in term.lower() or search_term.lower() in definition.lower() or not search_term:
            with st.expander(f"📌 {term}"):
                st.markdown(definition)


def get_guide_statistics() -> Dict:
    """Get statistics about the guide content"""
    
    return {
        "modules": len(EPICLOCK_MODULES),
        "clocks": len(EPIGENETIC_CLOCKS_INFO),
        "references": len(ACADEMIC_REFERENCES),
        "glossary_terms": len(GLOSSARY_TERMS),
        "version": GUIDE_VERSION,
        "last_updated": LAST_UPDATED
    }
