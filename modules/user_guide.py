"""
User Guide and Glossary Module
Comprehensive help system for non-technical users

Features:
- Interactive glossary with tooltips
- Step-by-step wizards for complex tasks
- Academic citations and references
- Evidence level badges
- Methodology transparency panels

Author: Dr. Nurcan Denli Bayır
Platform: EpiClock Prototype
"""

import streamlit as st
from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum


class EvidenceLevel(Enum):
    """Evidence grading based on GRADE criteria"""
    STRONG = ("🟢", "Güçlü", "Çoklu replike edilmiş GWAS (p < 5×10⁻⁸)")
    MODERATE = ("🟡", "Orta", "Tek GWAS veya meta-analiz (p < 5×10⁻⁶)")
    SUGGESTIVE = ("🟠", "Suggestive", "Suggestive ilişki (p < 1×10⁻⁵)")
    PRELIMINARY = ("🔴", "Ön Kanıt", "Replikasyon gerekli (p < 1×10⁻³)")
    EXPERT_OPINION = ("⚪", "Uzman Görüşü", "Literatür tabanlı, GWAS dışı")


@dataclass
class GlossaryEntry:
    """Single glossary entry with detailed explanation"""
    term: str
    short_definition: str
    detailed_explanation: str
    example: Optional[str] = None
    related_terms: Optional[List[str]] = None
    academic_reference: Optional[str] = None


GENOMICS_GLOSSARY = {
    'prs': GlossaryEntry(
        term="Poligenik Risk Skoru (PRS)",
        short_definition="Birçok genetik varyantın toplam etkisini gösteren sayısal skor",
        detailed_explanation="""
        Poligenik Risk Skoru (PRS), bir hastalık veya özellik için birçok genin 
        küçük etkilerinin toplamını hesaplar. Her bir genetik varyantın etkisi 
        (beta katsayısı) ile o varyantın kişideki kopyası çarpılır ve tüm 
        varyantlar toplanır.
        
        **Formül:** PRS = Σ(βᵢ × Genotipᵢ)
        
        **Neden önemli?**
        - Birçok hastalık tek bir gen tarafından değil, yüzlerce genin 
          küçük etkilerinin toplamı ile belirlenir
        - PRS bu karmaşık genetik mimariyi tek bir anlamlı sayıya dönüştürür
        """,
        example="Alkol bağımlılığı için PRS = 0.85 → 85. persentilde, popülasyonun %85'inden yüksek genetik risk",
        related_terms=['GWAS', 'Beta Katsayısı', 'Persentil'],
        academic_reference="Lewis & Vassos (2020) Nat Rev Genet"
    ),
    
    'gwas': GlossaryEntry(
        term="GWAS (Genome-Wide Association Study)",
        short_definition="Tüm genom çapında hastalık-varyant ilişkilerini arayan araştırma",
        detailed_explanation="""
        GWAS, binlerce veya milyonlarca kişinin DNA'sını tarayarak belirli 
        hastalıklar veya özelliklerle ilişkili genetik varyantları bulur.
        
        **Nasıl çalışır?**
        1. Hastalar ve sağlıklı kontrollerden DNA toplanır
        2. Milyonlarca genetik varyant (SNP) incelenir
        3. Her varyant için hastalık ilişkisi test edilir
        4. Anlamlı olanlar (p < 5×10⁻⁸) raporlanır
        
        **Sonuç:** Her hastalık için risk artıran/azaltan varyant listesi
        """,
        example="MVP 2020 opioid GWAS: 82,707 kişi, OPRM1 geninde rs1799971 → opioid bağımlılığı riski",
        related_terms=['SNP', 'P-değeri', 'Meta-analiz'],
        academic_reference="Visscher et al. (2017) Am J Hum Genet"
    ),
    
    'snp': GlossaryEntry(
        term="SNP (Tek Nükleotid Polimorfizmi)",
        short_definition="DNA'daki tek harflik farklılık",
        detailed_explanation="""
        SNP (Single Nucleotide Polymorphism), DNA dizisinde tek bir baz 
        çiftindeki farklılıktır. İnsan genomunda yaklaşık 10 milyon SNP vardır.
        
        **Örnek:**
        - Referans: ...AACGTA...
        - Varyant:  ...AACATA... (G→A değişimi)
        
        **Tanımlama:** rsID formatı (örn: rs1799971)
        
        **Frekans:** Popülasyonda ne sıklıkta görüldüğü (MAF)
        """,
        example="rs1229984: ADH1B genindeki SNP, alkol metabolizmasını etkiler",
        related_terms=['MAF', 'Alel', 'Genotip']
    ),
    
    'maf': GlossaryEntry(
        term="MAF (Minor Allel Frekansı)",
        short_definition="Nadir alelin popülasyondaki sıklığı",
        detailed_explanation="""
        MAF, bir genetik varyantın daha nadir olan versiyonunun popülasyondaki 
        frekansıdır. %1-5 arası nadir, %5-50 arası yaygın kabul edilir.
        
        **Örnek:**
        - Popülasyonun %80'i: G/G genotipi
        - Popülasyonun %18'i: G/A genotipi
        - Popülasyonun %2'si: A/A genotipi
        - MAF = 0.11 (A aleli %11)
        """,
        example="rs16969968 MAF=0.35 → CHRNA5'teki risk aleli oldukça yaygın"
    ),
    
    'heritability': GlossaryEntry(
        term="Kalıtılabilirlik (Heritability)",
        short_definition="Bir özelliğin genetik faktörlerden etkilenme oranı",
        detailed_explanation="""
        Kalıtılabilirlik, bir özellik veya hastalığın ne kadarının genetik 
        faktörlerle açıklandığını gösterir.
        
        **İki tip:**
        1. **İkiz kalıtılabilirliği (h²):** İkiz çalışmalarından hesaplanır, 
           tüm genetik etkiyi ölçer (~%40-60 bağımlılık için)
        
        2. **SNP kalıtılabilirliği:** GWAS ile bulunan varyantların açıkladığı 
           kısım (~%5-15, "missing heritability" sorunu)
        
        **Dikkat:** %50 kalıtılabilirlik, %50 şansla hasta olacaksınız demek DEĞİL!
        """,
        example="Alkol bağımlılığı h²=49% → Genetik faktörler riskin yarısını açıklıyor"
    ),
    
    'eaa': GlossaryEntry(
        term="EAA (Epigenetik Yaş İvmelenmesi)",
        short_definition="Biyolojik yaşın kronolojik yaştan sapması",
        detailed_explanation="""
        Epigenetik Yaş İvmelenmesi, DNA metilasyon saatlerinden hesaplanan 
        biyolojik yaşın kronolojik yaştan ne kadar farklı olduğunu gösterir.
        
        **Hesaplama:**
        EAA = Epigenetik Yaş - Kronolojik Yaş
        
        **Yorum:**
        - EAA > 0: Hızlı yaşlanma (kötü)
        - EAA < 0: Yavaş yaşlanma (iyi)
        
        **Bağımlılıkta:**
        - Alkol: +3.6 yıl (ortalama)
        - Opioid: +2.9 yıl
        - Polimadde: +7.3 yıl
        """,
        example="35 yaşında, epigenetik yaş 42 → EAA = +7 yıl",
        related_terms=['DNA Metilasyonu', 'Horvath Saati', 'GrimAge'],
        academic_reference="Horvath & Raj (2018) Nat Rev Genet"
    ),
    
    'dna_methylation': GlossaryEntry(
        term="DNA Metilasyonu",
        short_definition="DNA'ya metil grubu eklenmesi - gen ifadesini düzenler",
        detailed_explanation="""
        DNA metilasyonu, genellikle CpG bölgelerinde sitozin bazına metil 
        grubu (CH₃) eklenmesidir. Bu epigenetik modifikasyon gen ifadesini 
        düzenler - genellikle susturur.
        
        **Önemli:**
        - Çevresel faktörlerden etkilenir (sigara, alkol, stres)
        - Kalıcı değişikliklere yol açabilir
        - Yaşlanma ile karakteristik değişimler gösterir
        
        **Ölçüm:**
        - Illumina 450K/EPIC array: ~850,000 CpG bölgesi
        - Beta değeri: 0 (metilsiz) - 1 (tam metilli)
        """,
        example="OPRM1 promoter metilasyonu → Opioid reseptör ekspresyonu azalır"
    ),
    
    'cpg': GlossaryEntry(
        term="CpG Bölgesi",
        short_definition="Sitozin-Guanin nükleotid çifti - metilasyon hedefi",
        detailed_explanation="""
        CpG, Sitozin (C) ve Guanin (G) nükleotidlerinin ardışık olduğu 
        bölgelerdir. "p" aradaki fosfat bağını temsil eder.
        
        **Özellikler:**
        - İnsan genomunda ~28 milyon CpG
        - Promoter bölgelerinde yoğun (CpG adaları)
        - Metilasyon hedefi
        
        **Epigenetik saatler:**
        - Horvath: 353 CpG
        - PhenoAge: 513 CpG
        - GrimAge: 1030 CpG
        """,
        example="cg00000292: Kromozom 16'da, ABAT geninde, yaşlanma ile metilasyonu artar"
    ),
    
    'persentil': GlossaryEntry(
        term="Persentil",
        short_definition="Popülasyondaki sıralama yüzdesi",
        detailed_explanation="""
        Persentil, bir değerin popülasyonun yüzde kaçından yüksek olduğunu 
        gösterir.
        
        **Örnek:**
        - 75. persentil = Popülasyonun %75'inden yüksek
        - 50. persentil = Medyan (ortanca değer)
        - 90. persentil = Popülasyonun %90'ından yüksek
        
        **Risk kategorileri:**
        - < 10. persentil: Çok Düşük Risk
        - 10-25. persentil: Düşük Risk
        - 25-75. persentil: Ortalama
        - 75-90. persentil: Yüksek Risk
        - > 90. persentil: Çok Yüksek Risk
        """,
        example="PRS 85. persentil → 100 kişiden 85'inden yüksek genetik risk"
    ),
    
    'beta': GlossaryEntry(
        term="Beta Katsayısı (β)",
        short_definition="Varyantın hastalık riskine etkisi",
        detailed_explanation="""
        Beta katsayısı, bir genetik varyantın her ek kopyasının hastalık 
        riskini ne kadar artırdığını (veya azalttığını) gösterir.
        
        **Yorum:**
        - β > 0: Risk artırıcı etki
        - β < 0: Koruyucu etki
        - |β| büyüklüğü: Etki gücü
        
        **Lojistik regresyonda:**
        - exp(β) = Odds Ratio
        - β = 0.15 → OR = 1.16 → %16 risk artışı/kopya
        """,
        example="rs1799971 β=0.15 → Her G aleli opioid bağımlılığı riskini ~%16 artırır"
    ),
    
    'odds_ratio': GlossaryEntry(
        term="Odds Ratio (OR)",
        short_definition="Risk varyantı taşıyanlar vs taşımayanlardaki hastalık oranı",
        detailed_explanation="""
        Odds Ratio, bir genetik varyantı taşıyanlarda hastalık olasılığının 
        taşımayanlara göre kaç kat fazla olduğunu gösterir.
        
        **Yorum:**
        - OR = 1: Varyant riskle ilişkili değil
        - OR > 1: Varyant riski artırıyor
        - OR < 1: Varyant koruyucu
        
        **Örnek:**
        OR = 1.5 → Risk varyantı taşıyanların hasta olma olasılığı %50 fazla
        """,
        example="DRD2 rs1800497 OR=1.3 → Taşıyanlarda bağımlılık riski %30 fazla"
    ),
    
    'pharmacogenomics': GlossaryEntry(
        term="Farmakogenomik",
        short_definition="Genetiğin ilaç yanıtına etkisini inceleyen bilim",
        detailed_explanation="""
        Farmakogenomik, genetik varyasyonların ilaçların etkinlik ve 
        güvenliğini nasıl etkilediğini araştırır.
        
        **Bağımlılık tedavisinde:**
        - CYP2D6: Opioid metabolizması (kodein → morfin)
        - CYP2C19: Metadon metabolizması
        - OPRM1: Naltrexon yanıtı
        - COMT: Psikoterapi yanıtı
        
        **Klinik uygulama:**
        - Doğru ilaç seçimi
        - Doz ayarlaması
        - Yan etki önleme
        """,
        example="CYP2D6 poor metabolizer → Kodein etkisiz, alternatif opioid gerekli"
    ),
    
    'imputation': GlossaryEntry(
        term="İmputasyon",
        short_definition="Ölçülmeyen varyantların tahmin edilmesi",
        detailed_explanation="""
        İmputasyon, genotiplenmemiş varyantların referans panel kullanılarak 
        istatistiksel olarak tahmin edilmesidir.
        
        **Neden gerekli?**
        - Array'ler tüm varyantları ölçmez (~700K)
        - Referans paneller (1000G, TOPMed) ile ~40M varyant tahmin edilebilir
        
        **Kalite:**
        - R² > 0.8: Yüksek güvenilir
        - R² 0.3-0.8: Orta güvenilir
        - R² < 0.3: Düşük güvenilir
        """,
        example="Array: 700K SNP → 1000 Genomes ile imputasyon → 40M SNP tahmin"
    )
}


ACADEMIC_REFERENCES = {
    'alcohol_gwas': {
        'citation': 'Walters et al. (2018)',
        'title': 'Transancestral GWAS of alcohol dependence reveals common genetic underpinnings with psychiatric disorders',
        'journal': 'Nature Neuroscience',
        'pmid': '30643251',
        'year': 2018,
        'n_samples': 274424,
        'key_findings': ['ADH1B, ALDH2 en güçlü sinyaller', 'Psikiyatrik bozukluklarla genetik örtüşme', 'Kalıtılabilirlik ~%9']
    },
    'opioid_gwas': {
        'citation': 'Polimanti et al. (2020)',
        'title': 'Multi-ancestry genome-wide association study of opioid use disorder',
        'journal': 'Nature Neuroscience',
        'pmid': '32042166',
        'year': 2020,
        'n_samples': 82707,
        'key_findings': ['OPRM1 rs1799971 en güçlü sinyal', 'FURIN yeni locus', 'Ağrı duyarlılığı ile ilişki']
    },
    'nicotine_gwas': {
        'citation': 'Liu et al. (2019)',
        'title': 'Association studies of up to 1.2 million individuals yield new insights into the genetic etiology of tobacco and alcohol use',
        'journal': 'Nature Genetics',
        'pmid': '30643251',
        'year': 2019,
        'n_samples': 1232091,
        'key_findings': ['CHRNA3-CHRNA5-CHRNB4 kümesi', '378 bağımsız sinyal', 'Sigara miktarı/bırakma ile farklı ilişkiler']
    },
    'prs_review': {
        'citation': 'Lewis & Vassos (2020)',
        'title': 'Polygenic risk scores: from research tools to clinical instruments',
        'journal': 'Genome Medicine',
        'pmid': '32423416',
        'year': 2020,
        'key_findings': ['PRS klinik uygulamalara geçiş', 'Etik ve toplumsal konular', 'Çoklu-ata popülasyonlarda zorluklar']
    },
    'epigenetic_clock': {
        'citation': 'Horvath & Raj (2018)',
        'title': 'DNA methylation-based biomarkers and the epigenetic clock theory of ageing',
        'journal': 'Nature Reviews Genetics',
        'pmid': '29643443',
        'year': 2018,
        'key_findings': ['Epigenetik saatlerin teorik temeli', 'Biyolojik yaş kavramı', 'Hastalık ve mortalite tahmini']
    },
    'addiction_epigenetics': {
        'citation': 'Robison & Nestler (2011)',
        'title': 'Transcriptional and epigenetic mechanisms of addiction',
        'journal': 'Nature Reviews Neuroscience',
        'pmid': '21931334',
        'year': 2011,
        'key_findings': ['Bağımlılıkta epigenetik değişiklikler', 'HDAC ve DNMT rolleri', 'Tedavi hedefleri']
    }
}


def render_glossary_sidebar():
    """Render interactive glossary in sidebar"""
    with st.sidebar:
        with st.expander("📖 Terimler Sözlüğü", expanded=False):
            search_term = st.text_input("Terim ara:", placeholder="PRS, GWAS...")
            
            filtered_terms = {k: v for k, v in GENOMICS_GLOSSARY.items() 
                            if search_term.lower() in k.lower() or 
                               search_term.lower() in v.term.lower() or
                               search_term.lower() in v.short_definition.lower()}
            
            for key, entry in (filtered_terms if search_term else GENOMICS_GLOSSARY).items():
                with st.expander(f"**{entry.term}**"):
                    st.markdown(f"_{entry.short_definition}_")
                    st.markdown("---")
                    st.markdown(entry.detailed_explanation)
                    if entry.example:
                        st.info(f"📌 **Örnek:** {entry.example}")
                    if entry.related_terms:
                        st.caption(f"İlişkili: {', '.join(entry.related_terms)}")
                    if entry.academic_reference:
                        st.caption(f"📚 {entry.academic_reference}")


def render_methodology_panel(analysis_type: str):
    """Render methodology transparency panel"""
    methodologies = {
        'prs': {
            'title': 'Poligenik Risk Skoru Metodolojisi',
            'steps': [
                '1. GWAS özet istatistikleri yüklenir (beta katsayıları)',
                '2. Kullanıcı varyantları ile GWAS varyantları eşleştirilir',
                '3. Her eşleşen varyant için: katkı = beta × genotip dozajı',
                '4. Tüm katkılar toplanarak ham PRS hesaplanır',
                '5. Z-skor standardizasyonu yapılır',
                '6. Persentil ve risk kategorisi belirlenir'
            ],
            'formula': 'PRS = Σᵢ(βᵢ × Genotipᵢ)',
            'quality': [
                'GWAS p-değeri < 5×10⁻⁸ (genom çapında anlamlılık)',
                'Çoklu popülasyonlarda replikasyon',
                'Meta-analiz ile güç artırımı'
            ]
        },
        'eaa': {
            'title': 'Epigenetik Yaş İvmelenmesi Metodolojisi',
            'steps': [
                '1. DNA metilasyon verileri yüklenir (beta değerleri)',
                '2. Saat-spesifik CpG siteleri seçilir',
                '3. Ağırlıklı toplam ile epigenetik yaş hesaplanır',
                '4. Kronolojik yaştan çıkarılarak EAA bulunur',
                '5. Popülasyon ortalaması ile karşılaştırılır'
            ],
            'formula': 'EAA = Epigenetik Yaş - Kronolojik Yaş',
            'quality': [
                'Horvath (2013) orijinal 353-CpG saati',
                'Çoklu doku validasyonu',
                'r > 0.96 kronolojik yaş korelasyonu'
            ]
        }
    }
    
    if analysis_type in methodologies:
        method = methodologies[analysis_type]
        
        with st.expander(f"🔬 {method['title']}", expanded=False):
            st.markdown("### Analiz Adımları")
            for step in method['steps']:
                st.markdown(step)
            
            st.markdown("### Matematiksel Formül")
            st.latex(method['formula'])
            
            st.markdown("### Kalite Kriterleri")
            for q in method['quality']:
                st.markdown(f"✅ {q}")


def render_evidence_badge(level: EvidenceLevel) -> str:
    """Render evidence level badge"""
    color, label, description = level.value
    return f"{color} **{label}** _{description}_"


def render_academic_citations(reference_keys: List[str]):
    """Render academic citations panel"""
    with st.expander("📚 Akademik Referanslar", expanded=False):
        for key in reference_keys:
            if key in ACADEMIC_REFERENCES:
                ref = ACADEMIC_REFERENCES[key]
                st.markdown(f"""
                **{ref['citation']}**
                
                {ref['title']}
                
                _{ref['journal']}_, {ref['year']} | PMID: {ref['pmid']}
                
                n = {ref['n_samples']:,} | Bulgular: {', '.join(ref['key_findings'][:2])}...
                
                ---
                """)


def get_tooltip(term: str) -> str:
    """Get tooltip text for a term"""
    if term.lower() in GENOMICS_GLOSSARY:
        entry = GENOMICS_GLOSSARY[term.lower()]
        return f"{entry.term}: {entry.short_definition}"
    return ""


def render_step_by_step_wizard(wizard_type: str):
    """Render step-by-step analysis wizard"""
    
    wizards = {
        'prs_analysis': {
            'title': '📊 PRS Analizi Sihirbazı',
            'description': 'Adım adım poligenik risk skoru hesaplama',
            'steps': [
                {
                    'name': 'Veri Yükleme',
                    'instruction': 'VCF dosyanızı yükleyin veya demo veri oluşturun',
                    'tips': ['VCF formatı gerekli', 'rsID bilgisi önemli', 'Genotip bilgisi şart'],
                    'estimated_time': '1-2 dakika'
                },
                {
                    'name': 'Özellik Seçimi',
                    'instruction': 'Analiz edilecek hastalık/özellikleri seçin',
                    'tips': ['Birden fazla seçilebilir', 'Bağımlılık türleri listelenmiştir', 'Komorbiditeleri de ekleyin'],
                    'estimated_time': '30 saniye'
                },
                {
                    'name': 'Hesaplama',
                    'instruction': '"PRS Hesapla" butonuna tıklayın',
                    'tips': ['Birkaç saniye sürer', 'Her özellik ayrı hesaplanır', 'Birleşik skor da verilir'],
                    'estimated_time': '10-30 saniye'
                },
                {
                    'name': 'Sonuç Yorumu',
                    'instruction': 'Persentil ve risk kategorilerine bakın',
                    'tips': ['>75. persentil dikkat gerektir', 'Genetik risk tek başına yeterli değil', 'Klinik değerlendirme önemli'],
                    'estimated_time': '2-3 dakika'
                }
            ]
        },
        'integrated_analysis': {
            'title': '🔗 Entegre Analiz Sihirbazı',
            'description': 'Genetik ve epigenetik verileri birleştirme',
            'steps': [
                {
                    'name': 'Metilasyon Verisi',
                    'instruction': 'DNA metilasyon verilerini yükleyin',
                    'tips': ['IDAT veya beta değerleri', 'En az 1000 CpG', 'Kalite kontrolü otomatik'],
                    'estimated_time': '2-3 dakika'
                },
                {
                    'name': 'Varyant Verisi',
                    'instruction': 'VCF dosyasını yükleyin',
                    'tips': ['Aynı hastadan olmalı', 'rsID bilgisi gerekli'],
                    'estimated_time': '1-2 dakika'
                },
                {
                    'name': 'Klinik Bilgiler',
                    'instruction': 'Demografik ve klinik bilgileri girin',
                    'tips': ['Yaş zorunlu', 'Madde kullanım öyküsü', 'Aile öyküsü'],
                    'estimated_time': '1 dakika'
                },
                {
                    'name': 'Entegre Analiz',
                    'instruction': '"Entegre Risk Hesapla" butonuna tıklayın',
                    'tips': ['3 bileşen birleştirilir', 'Ağırlıklar otomatik', 'Kapsamlı rapor üretilir'],
                    'estimated_time': '30 saniye'
                }
            ]
        }
    }
    
    if wizard_type in wizards:
        wizard = wizards[wizard_type]
        
        st.markdown(f"## {wizard['title']}")
        st.info(wizard['description'])
        
        current_step = st.session_state.get(f'{wizard_type}_step', 0)
        
        progress = (current_step + 1) / len(wizard['steps'])
        st.progress(progress)
        st.caption(f"Adım {current_step + 1} / {len(wizard['steps'])}")
        
        step = wizard['steps'][current_step]
        
        st.markdown(f"### {step['name']}")
        st.markdown(f"**Talimat:** {step['instruction']}")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**İpuçları:**")
            for tip in step['tips']:
                st.markdown(f"- {tip}")
        with col2:
            st.metric("Tahmini Süre", step['estimated_time'])
        
        col1, col2, col3 = st.columns(3)
        with col1:
            if current_step > 0:
                if st.button("⬅️ Önceki"):
                    st.session_state[f'{wizard_type}_step'] = current_step - 1
                    st.rerun()
        with col3:
            if current_step < len(wizard['steps']) - 1:
                if st.button("Sonraki ➡️"):
                    st.session_state[f'{wizard_type}_step'] = current_step + 1
                    st.rerun()
            else:
                st.success("✅ Sihirbaz tamamlandı!")
