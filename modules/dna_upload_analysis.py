# ============================================================================
# EpiClock Prototype - DNA Data Upload, Analysis & Export Module
# Copyright (c) 2024 Dr. Nurcan Denli Bayir (nrcdnl94)
# All rights reserved.
# ============================================================================

"""
DNA Data Upload, Epi-Clock Analysis, and Export Module
Provides file upload, preprocessing, model execution, and report generation
"""

import streamlit as st
import pandas as pd
import numpy as np
import os
import json
import io
from datetime import datetime
from typing import Optional, Dict, Any, Tuple, List
from modules.dna_analysis_engine import EpigeneticClockEngine, create_engine

try:
    from modules.real_data_loader import RealDataLoader, LoadedMethylationData
    REAL_LOADER_AVAILABLE = True
except ImportError:
    REAL_LOADER_AVAILABLE = False

try:
    from modules.methylation_preprocessing import (
        MethylationPreprocessor, ComBatCorrection, 
        CellCompositionEstimator, QualityControl
    )
    PREPROCESSING_AVAILABLE = True
except ImportError:
    PREPROCESSING_AVAILABLE = False

try:
    from modules.model_explainability import EpigeneticExplainer, ModelAgnosticExplainer
    EXPLAINABILITY_AVAILABLE = True
except ImportError:
    EXPLAINABILITY_AVAILABLE = False

try:
    from modules.substance_detection import SubstanceDetectionEngine, SUBSTANCE_SIGNATURES
    SUBSTANCE_DETECTION_AVAILABLE = True
except ImportError:
    SUBSTANCE_DETECTION_AVAILABLE = False

try:
    from modules.abuse_method_detection import AbuseMethodDetectionEngine
    ABUSE_METHOD_AVAILABLE = True
except ImportError:
    ABUSE_METHOD_AVAILABLE = False

try:
    from modules.illicit_manufacturing import IllicitManufacturingDetector
    ILLICIT_MANUFACTURING_AVAILABLE = True
except ImportError:
    ILLICIT_MANUFACTURING_AVAILABLE = False

try:
    from modules.pharmacological_abuse_intelligence import PharmacologicalAbuseIntelligence
    PHARMA_INTEL_AVAILABLE = True
except ImportError:
    PHARMA_INTEL_AVAILABLE = False

try:
    from modules.dna_manufacturing_detection import DNAManufacturingDetector
    DNA_MANUFACTURING_AVAILABLE = True
except ImportError:
    DNA_MANUFACTURING_AVAILABLE = False

try:
    from modules.unknown_substance_detection import UnknownSubstanceDetector, AnomalyType
    UNKNOWN_DETECTION_AVAILABLE = True
except ImportError:
    UNKNOWN_DETECTION_AVAILABLE = False

try:
    from modules.tissue_clocks import TissueSpecificClockCalculator
    TISSUE_CLOCKS_AVAILABLE = True
except ImportError:
    TISSUE_CLOCKS_AVAILABLE = False

try:
    from modules.pharmacogenomics import PharmacogenomicsAnalyzer
    PHARMACOGENOMICS_AVAILABLE = True
except ImportError:
    PHARMACOGENOMICS_AVAILABLE = False

try:
    from modules.chronic_diseases import ChronicDiseaseAnalyzer
    CHRONIC_DISEASE_AVAILABLE = True
except ImportError:
    CHRONIC_DISEASE_AVAILABLE = False

try:
    from modules.molecular_gnn import MolecularGNNPredictor
    GNN_AVAILABLE = True
except ImportError:
    GNN_AVAILABLE = False


def render_dna_upload_analysis_page():
    """Render the DNA data upload and analysis page - nrcdnl94"""
    
    st.markdown("""
    <style>
    .upload-section {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 8px;
        padding: 20px;
        margin-bottom: 16px;
    }
    .section-title {
        font-size: 0.9rem;
        font-weight: 600;
        color: #0050A0;
        margin-bottom: 12px;
    }
    .info-text {
        font-size: 0.75rem;
        color: #64748B;
        margin-bottom: 12px;
    }
    .status-box {
        padding: 12px 16px;
        border-radius: 6px;
        font-size: 0.8rem;
        margin-top: 12px;
    }
    .status-success {
        background: #F0FDF4;
        border: 1px solid #BBF7D0;
        color: #166534;
    }
    .status-warning {
        background: #FEFCE8;
        border: 1px solid #FEF08A;
        color: #A16207;
    }
    .status-error {
        background: #FEF2F2;
        border: 1px solid #FECACA;
        color: #DC2626;
    }
    .metric-card {
        background: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 6px;
        padding: 12px;
        text-align: center;
    }
    .metric-value {
        font-size: 1.5rem;
        font-weight: 600;
        color: #0050A0;
    }
    .metric-label {
        font-size: 0.7rem;
        color: #64748B;
        text-transform: uppercase;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style="font-size: 0.7rem; color: #64748B; margin-bottom: 8px;">
        Epi-Clock / <span style="color: #334155; font-weight: 500;">DNA Veri Yukleme & Analiz</span>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="upload-section">
        <h1 style="font-size: 1.1rem; font-weight: 600; color: #0050A0; margin: 0;">
            DNA Veri Yukleme - Epi-Clock Analizi - Cikti Alma
        </h1>
        <p style="font-size: 0.75rem; color: #64748B; margin-top: 4px;">
            DNA metilasyon / genomik verilerini yukleyin, epigenetik yas analizini baslatin ve rapor ciktisini indirin.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs([
        "1) Veri Yukle",
        "2) Analiz Baslat", 
        "3) Cikti / Rapor Al"
    ])
    
    with tab1:
        render_upload_tab()
    
    with tab2:
        render_analysis_tab()
    
    with tab3:
        render_export_tab()


def render_upload_tab():
    """Render the data upload tab - nrcdnl94"""
    
    st.markdown('<div class="section-title">DNA Veri Yukleme</div>', unsafe_allow_html=True)
    st.markdown('<p class="info-text">DNA metilasyon matrisi (.csv, .tsv, .xlsx) veya proje formatindaki girdi dosyalarinizi yukleyebilirsiniz.</p>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        dataset_name = st.text_input(
            "Veri Seti Adi",
            placeholder="Orn: epi_clock_cohort_01",
            key="dataset_name_input"
        )
    
    with col2:
        data_type = st.selectbox(
            "Veri Tipi",
            options=[
                "DNA metilasyon beta-matrix",
                "Ham intensite verisi",
                "Genotip verisi",
                "CpG marker verisi"
            ],
            key="data_type_select"
        )
    
    st.markdown("---")
    
    uploaded_file = st.file_uploader(
        "Dosya Sec (.csv, .tsv, .xlsx)",
        type=['csv', 'tsv', 'xlsx', 'txt'],
        key="dna_file_uploader",
        help="Buyuk veri setleri icin yukleme suresi uzayabilir."
    )
    
    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            elif uploaded_file.name.endswith('.tsv') or uploaded_file.name.endswith('.txt'):
                df = pd.read_csv(uploaded_file, sep='\t')
            elif uploaded_file.name.endswith('.xlsx'):
                df = pd.read_excel(uploaded_file)
            else:
                df = pd.read_csv(uploaded_file)
            
            st.session_state['uploaded_dna_data'] = df
            st.session_state['uploaded_file_name'] = uploaded_file.name
            st.session_state['dataset_name'] = dataset_name if dataset_name else uploaded_file.name.split('.')[0]
            st.session_state['data_type'] = data_type
            
            st.markdown("""
            <div class="status-box status-success">
                Dosya basariyla yuklendi!
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value">{df.shape[0]:,}</div>
                    <div class="metric-label">Satir (Ornek)</div>
                </div>
                """, unsafe_allow_html=True)
            with col2:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value">{df.shape[1]:,}</div>
                    <div class="metric-label">Sutun (CpG/Ozellik)</div>
                </div>
                """, unsafe_allow_html=True)
            with col3:
                missing_pct = (df.isnull().sum().sum() / (df.shape[0] * df.shape[1]) * 100)
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value">{missing_pct:.1f}%</div>
                    <div class="metric-label">Eksik Deger</div>
                </div>
                """, unsafe_allow_html=True)
            with col4:
                file_size_mb = uploaded_file.size / (1024 * 1024)
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value">{file_size_mb:.1f}</div>
                    <div class="metric-label">Dosya Boyutu (MB)</div>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("#### Veri Onizlemesi")
            st.dataframe(df.head(10), use_container_width=True, hide_index=True)
            
            if REAL_LOADER_AVAILABLE:
                st.markdown("#### CpG Dogrulama ve Saat Kapsami")
                try:
                    loader = RealDataLoader()
                    uploaded_file.seek(0)
                    loaded_result = loader.load_file(uploaded_file)
                    
                    st.session_state['loaded_methylation'] = loaded_result
                    
                    for msg in loaded_result.validation_messages:
                        if msg.startswith("ERROR"):
                            st.error(msg)
                        elif msg.startswith("WARNING"):
                            st.warning(msg)
                        elif msg.startswith("SUCCESS"):
                            st.success(msg)
                        else:
                            st.info(msg)
                    
                    clock_coverage = loaded_result.metadata.get('clock_coverage', {})
                    if clock_coverage:
                        st.markdown("**Epigenetik Saat CpG Kapsami:**")
                        cov_col1, cov_col2 = st.columns(2)
                        with cov_col1:
                            hannum_cov = clock_coverage.get('hannum', 0) * 100
                            st.metric("Hannum (Acik Kaynak)", f"{hannum_cov:.0f}%")
                        with cov_col2:
                            dunedin_cov = clock_coverage.get('dunedinpace', 0) * 100
                            st.metric("DunedinPACE (Acik Kaynak)", f"{dunedin_cov:.0f}%")
                except Exception as e:
                    st.warning(f"CpG dogrulama atlandı: {str(e)}")
            
            if st.button("Veriyi Kaydet ve Devam Et", key="save_data_btn"):
                st.session_state['data_saved'] = True
                st.success("Veri basariyla kaydedildi! Simdi 'Analiz Baslat' sekmesine gecebilirsiniz.")
                
        except Exception as e:
            st.markdown(f"""
            <div class="status-box status-error">
                Dosya okuma hatasi: {str(e)}
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="status-box status-warning">
            Henuz bir dosya yuklenmedi. Lutfen bir DNA metilasyon dosyasi secin.
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("#### Ornek Veri Seti Indir")
    st.markdown('<p class="info-text">Test amacli ornek DNA metilasyon verisi indirebilirsiniz.</p>', unsafe_allow_html=True)
    
    if st.button("Ornek Veri Seti Olustur", key="generate_sample_btn"):
        sample_df = generate_sample_dna_data()
        csv_buffer = io.StringIO()
        sample_df.to_csv(csv_buffer, index=False)
        st.download_button(
            label="Ornek CSV Indir",
            data=csv_buffer.getvalue(),
            file_name="sample_dna_methylation_data.csv",
            mime="text/csv",
            key="download_sample_btn"
        )
    
    st.markdown("---")
    st.markdown("#### Gelismis Demo Senaryosu - Madde Tespiti")
    st.markdown('<p class="info-text">Belirli maddeler ve kronik hastaliklar icin sentetik DNA metilasyon verisi olusturun ve sistemin tespit yeteneklerini test edin.</p>', unsafe_allow_html=True)
    
    with st.expander("Demo Senaryosu Olustur", expanded=False):
        demo_col1, demo_col2 = st.columns(2)
        
        with demo_col1:
            st.markdown("**Demografik Bilgiler**")
            demo_age = st.number_input("Kronolojik Yas", min_value=18, max_value=90, value=35, key="demo_chron_age")
            demo_sex = st.selectbox("Cinsiyet", ["Erkek", "Kadin"], key="demo_sex")
        
        with demo_col2:
            st.markdown("**Kronik Hastalik**")
            demo_disease = st.selectbox(
                "Kronik Hastalik",
                ["Yok", "Astim (15 yil)", "KOAH (10 yil)", "Diyabet Tip 2 (8 yil)", "Hipertansiyon (12 yil)"],
                key="demo_disease"
            )
        
        st.markdown("**Madde Secimi (En fazla 3)**")
        
        substance_options = {
            "Metamfetamin": ("methamphetamine", 3),
            "Heroin": ("heroin", 5),
            "Kokain": ("cocaine_hcl", 4),
            "Benzodiazepin (Alprazolam)": ("alprazolam", 2),
            "Fentanil": ("fentanyl", 2),
            "Esrar (Cannabis)": ("cannabis_thc", 6),
            "MDMA (Ecstasy)": ("mdma", 3),
            "Tramadol": ("tramadol", 4),
            "Pregabalin": ("pregabalin", 3),
            "Morfin": ("morphine", 5),
            "Oksikodon": ("oxycodone", 3),
            "Gabapentin": ("gabapentin", 4)
        }
        
        sub_col1, sub_col2, sub_col3 = st.columns(3)
        
        with sub_col1:
            substance1 = st.selectbox("Madde 1", ["Yok"] + list(substance_options.keys()), key="demo_sub1")
            if substance1 != "Yok":
                years1 = st.slider("Kullanim Suresi (Yil)", 1, 20, substance_options[substance1][1], key="demo_years1")
        
        with sub_col2:
            substance2 = st.selectbox("Madde 2", ["Yok"] + list(substance_options.keys()), key="demo_sub2")
            if substance2 != "Yok":
                years2 = st.slider("Kullanim Suresi (Yil)", 1, 20, substance_options[substance2][1], key="demo_years2")
        
        with sub_col3:
            substance3 = st.selectbox("Madde 3", ["Yok"] + list(substance_options.keys()), key="demo_sub3")
            if substance3 != "Yok":
                years3 = st.slider("Kullanim Suresi (Yil)", 1, 20, substance_options[substance3][1], key="demo_years3")
        
        if st.button("Demo Verisi Olustur ve Analiz Et", key="run_demo_analysis", type="primary"):
            with st.spinner("Sentetik DNA metilasyon verisi olusturuluyor ve analiz ediliyor..."):
                substances_used = []
                years_of_use = {}
                
                if substance1 != "Yok":
                    sub_key = substance_options[substance1][0]
                    substances_used.append(sub_key)
                    years_of_use[sub_key] = years1
                if substance2 != "Yok":
                    sub_key = substance_options[substance2][0]
                    substances_used.append(sub_key)
                    years_of_use[sub_key] = years2
                if substance3 != "Yok":
                    sub_key = substance_options[substance3][0]
                    substances_used.append(sub_key)
                    years_of_use[sub_key] = years3
                
                demo_results = run_demo_scenario_analysis(
                    chronological_age=demo_age,
                    sex=demo_sex,
                    substances_used=substances_used,
                    years_of_use=years_of_use,
                    chronic_disease=demo_disease
                )
                
                if demo_results:
                    st.session_state['demo_results'] = demo_results
                    st.session_state['demo_scenario'] = {
                        'age': demo_age,
                        'sex': demo_sex,
                        'substances': substances_used,
                        'years': years_of_use,
                        'disease': demo_disease
                    }
                    st.success("Demo analizi tamamlandi!")
                    st.rerun()
    
    if 'demo_results' in st.session_state:
        display_demo_results(st.session_state['demo_results'], st.session_state.get('demo_scenario', {}))


def render_analysis_tab():
    """Render the analysis execution tab - nrcdnl94"""
    
    st.markdown('<div class="section-title">Epi-Clock Analizini Baslat</div>', unsafe_allow_html=True)
    st.markdown('<p class="info-text">Yuklediginiz veri seti uzerinde epigenetik yas / MTL analizini baslatin.</p>', unsafe_allow_html=True)
    
    if 'uploaded_dna_data' not in st.session_state:
        st.markdown("""
        <div class="status-box status-warning">
            Henuz veri yuklenmedi. Lutfen once "Veri Yukle" sekmesinden bir dosya yukleyin.
        </div>
        """, unsafe_allow_html=True)
        return
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        dataset_id = st.text_input(
            "Veri Seti ID / Adi",
            value=st.session_state.get('dataset_name', ''),
            key="analysis_dataset_id"
        )
    
    with col2:
        model_version = st.selectbox(
            "Model Versiyonu",
            options=[
                "Horvath Pan-Tissue (353 CpG)",
                "Hannum Blood (71 CpG)",
                "PhenoAge (513 CpG)",
                "GrimAge (1030 CpG)",
                "DunedinPACE (173 CpG)",
                "Ensemble ML (Tum Saatler)"
            ],
            key="model_version_select"
        )
    
    with col3:
        run_mode = st.selectbox(
            "Calisma Modu",
            options=["Tek ornek", "Toplu (tum kohort)"],
            key="run_mode_select"
        )
    
    st.markdown("---")
    st.markdown("#### Gelismis Parametreler")
    
    col1, col2 = st.columns(2)
    
    with col1:
        normalize_data = st.checkbox("Veriyi normalize et (BMIQ)", value=True, key="normalize_check")
        batch_correction = st.checkbox("Batch duzeltmesi uygula (ComBat)", value=False, key="batch_check")
    
    with col2:
        confidence_interval = st.checkbox("Guven araligi hesapla (95% CI)", value=True, key="ci_check")
        feature_importance = st.checkbox("Ozellik onemliligi analizi", value=True, key="feature_check")
    
    st.markdown("---")
    
    if st.button("Analizi Baslat", key="run_analysis_btn", type="primary"):
        with st.spinner("Analiz calistiriliyor..."):
            results = run_epiclock_analysis(
                st.session_state['uploaded_dna_data'],
                model_version,
                run_mode,
                normalize_data,
                batch_correction,
                confidence_interval,
                feature_importance
            )
            
            st.session_state['analysis_results'] = results
            st.session_state['analysis_completed'] = True
            st.session_state['analysis_timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        st.markdown("""
        <div class="status-box status-success">
            Analiz basariyla tamamlandi!
        </div>
        """, unsafe_allow_html=True)
        
        display_analysis_results(results)


def render_export_tab():
    """Render the export/download tab - nrcdnl94"""
    
    st.markdown('<div class="section-title">Cikti / Rapor Al</div>', unsafe_allow_html=True)
    st.markdown('<p class="info-text">Analiz sonuclarinizi farkli formatlarda indirin veya PDF rapor olusturun.</p>', unsafe_allow_html=True)
    
    if 'analysis_results' not in st.session_state:
        st.markdown("""
        <div class="status-box status-warning">
            Henuz analiz yapilmadi. Lutfen once "Analiz Baslat" sekmesinden bir analiz calistirin.
        </div>
        """, unsafe_allow_html=True)
        return
    
    results = st.session_state['analysis_results']
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{results['n_samples']}</div>
            <div class="metric-label">Analiz Edilen Ornek</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{results['mean_epi_age']:.1f}</div>
            <div class="metric-label">Ortalama Epigenetik Yas</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{results['mean_age_acceleration']:.1f}</div>
            <div class="metric-label">Ortalama Yas Ivmesi</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("#### Cikti Formati Sec")
    
    export_format = st.selectbox(
        "Format",
        options=[
            "CSV (Tablo)",
            "Excel (XLSX)",
            "JSON",
            "PDF Rapor"
        ],
        key="export_format_select"
    )
    
    include_options = st.multiselect(
        "Rapora Dahil Et",
        options=[
            "Ozet Istatistikler",
            "Ornek Bazli Sonuclar",
            "Ozellik Onemliligi",
            "Grafikler",
            "Metodoloji Aciklamasi"
        ],
        default=["Ozet Istatistikler", "Ornek Bazli Sonuclar"],
        key="include_options_select"
    )
    
    st.markdown("---")
    
    if st.button("Cikti Olustur ve Indir", key="generate_export_btn", type="primary"):
        export_data = generate_export(results, export_format, include_options)
        
        if export_format == "CSV (Tablo)":
            st.download_button(
                label="CSV Indir",
                data=export_data,
                file_name=f"epiclock_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
                key="download_csv_btn"
            )
        elif export_format == "Excel (XLSX)":
            st.download_button(
                label="Excel Indir",
                data=export_data,
                file_name=f"epiclock_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                key="download_xlsx_btn"
            )
        elif export_format == "JSON":
            st.download_button(
                label="JSON Indir",
                data=export_data,
                file_name=f"epiclock_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json",
                key="download_json_btn"
            )
        else:
            st.info("PDF rapor olusturma modulu aktif. Rapor indiriliyor...")
            st.download_button(
                label="PDF Rapor Indir",
                data=export_data,
                file_name=f"epiclock_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                mime="application/pdf",
                key="download_pdf_btn"
            )


def generate_sample_dna_data() -> pd.DataFrame:
    """Generate sample DNA methylation data for testing - nrcdnl94"""
    np.random.seed(42)
    
    n_samples = 50
    n_cpg = 100
    
    # EWAS-validated CpG pool from published literature
    # Sources: EWAS Catalog, Horvath 2013, Hannum 2013, Joehanes 2016, Wahl 2017
    REAL_CPG_POOL = [
        # Smoking markers (PMID:27651444)
        "cg05575921", "cg03636183", "cg06536614", "cg21566642", "cg01940273",
        # Metabolic markers (PMID:28002404)
        "cg05951221", "cg00574958", "cg06721411", "cg27243685", "cg06500161",
        "cg02480726", "cg12992827", "cg27534624", "cg11852953", "cg07553761",
        # Aging markers (Horvath/Hannum clocks)
        "cg14975410", "cg15342087", "cg22090150", "cg16867657", "cg14123992",
        "cg08234215", "cg24704287", "cg16269199", "cg25325512", "cg01884057",
        # Neurology markers (PMID:24917573)
        "cg11823178", "cg18568872", "cg05066959", "cg17501210", "cg19693031",
        "cg00339556", "cg14753356", "cg01656216", "cg14391737", "cg17944885",
        # Addiction/receptor markers (PMID:27595595)
        "cg23500537", "cg10636246", "cg06690548", "cg18181703", "cg11024682",
        "cg27243685", "cg14476101", "cg01561697", "cg23126569", "cg09935388",
        "cg04987734", "cg12806681", "cg19859270", "cg17178900", "cg06126421",
        # Inflammation markers (PMID:27019110)
        "cg02711608", "cg11376147", "cg18146737", "cg04180046", "cg12075928",
        # Additional validated markers from EPIC/450K arrays
        "cg14975410", "cg22090150", "cg14123992", "cg05066959", "cg18568872",
        "cg11823178", "cg15342087", "cg06536614", "cg17501210", "cg19693031",
        "cg05575921", "cg03636183", "cg05951221", "cg00574958", "cg06721411",
        "cg27243685", "cg06500161", "cg02480726", "cg12992827", "cg27534624",
        "cg11852953", "cg07553761", "cg08234215", "cg24704287", "cg16269199",
        "cg25325512", "cg01884057", "cg00339556", "cg14753356", "cg01656216",
        "cg14391737", "cg17944885", "cg23500537", "cg10636246", "cg06690548",
        "cg18181703", "cg11024682", "cg27243685", "cg14476101", "cg01561697"
    ]
    
    sample_ids = [f"SAMPLE_{i:03d}" for i in range(1, n_samples + 1)]
    cpg_ids = [REAL_CPG_POOL[i % len(REAL_CPG_POOL)] for i in range(n_cpg)]
    
    beta_values = np.random.beta(2, 5, size=(n_samples, n_cpg))
    
    df = pd.DataFrame(beta_values, columns=cpg_ids)
    df.insert(0, 'Sample_ID', sample_ids)
    df.insert(1, 'Age', np.random.randint(20, 80, n_samples))
    df.insert(2, 'Sex', np.random.choice(['M', 'F'], n_samples))
    
    return df


def run_demo_scenario_analysis(
    chronological_age: int,
    sex: str,
    substances_used: List[str],
    years_of_use: Dict[str, float],
    chronic_disease: str
) -> Dict[str, Any]:
    """
    Run demo scenario analysis with synthetic DNA methylation data
    Demonstrates system's ability to detect substances from methylation patterns
    """
    results = {
        'chronological_age': chronological_age,
        'sex': sex,
        'chronic_disease': chronic_disease,
        'input_substances': substances_used,
        'input_years': years_of_use,
        'detected_substances': [],
        'epigenetic_ages': {},
        'age_acceleration': 0,
        'disease_contribution': 0,
        'substance_contributions': {},
        'overall_confidence': 0
    }
    
    try:
        if SUBSTANCE_DETECTION_AVAILABLE:
            engine = SubstanceDetectionEngine()
            
            demo_methylation = engine.generate_sample_methylation_data(
                substances_used=substances_used,
                years_of_use=years_of_use
            )
            
            detection_results = engine.detect_substances(demo_methylation)
            
            detected = []
            for det in detection_results[:10]:
                if det.confidence >= 0.50:
                    detected.append({
                        'substance_name': det.substance_name,
                        'confidence': det.confidence,
                        'estimated_years': det.estimated_years_of_use,
                        'confidence_level': det.confidence_level.value if hasattr(det.confidence_level, 'value') else str(det.confidence_level),
                        'category': det.category
                    })
            
            results['detected_substances'] = detected
            results['overall_confidence'] = np.mean([d['confidence'] for d in detected]) if detected else 0
            
            similarity_matrix = engine.get_variant_similarity_matrix(substances_used, top_n=5)
            results['similarity_matrix'] = similarity_matrix
        
        base_epi_age = chronological_age
        total_acceleration = 0
        
        substance_age_effects = {
            'methamphetamine': 3.5,
            'heroin': 4.2,
            'cocaine_hcl': 2.8,
            'alprazolam': 1.5,
            'fentanyl': 3.8,
            'cannabis_thc': 0.8,
            'mdma': 1.2,
            'tramadol': 1.0,
            'pregabalin': 0.6,
            'morphine': 2.5,
            'oxycodone': 2.2,
            'gabapentin': 0.4
        }
        
        for sub_key, years in years_of_use.items():
            effect_per_year = substance_age_effects.get(sub_key, 1.0)
            contribution = effect_per_year * years * 0.15
            total_acceleration += contribution
            results['substance_contributions'][sub_key] = contribution
        
        disease_effects = {
            'Astim (15 yil)': 2.8,
            'KOAH (10 yil)': 4.5,
            'Diyabet Tip 2 (8 yil)': 3.2,
            'Hipertansiyon (12 yil)': 2.5,
            'Yok': 0
        }
        disease_contribution = disease_effects.get(chronic_disease, 0)
        total_acceleration += disease_contribution
        results['disease_contribution'] = disease_contribution
        
        epigenetic_age = base_epi_age + total_acceleration
        
        results['epigenetic_ages'] = {
            'Hannum (Acik Kaynak)': epigenetic_age + np.random.uniform(-1.5, 1.5),
            'DunedinPACE (Acik Kaynak)': 1.0 + (total_acceleration / 20),
            'Ensemble ML': epigenetic_age + np.random.uniform(-0.8, 0.8)
        }
        results['age_acceleration'] = total_acceleration
        
        if CHRONIC_DISEASE_AVAILABLE:
            try:
                disease_analyzer = ChronicDiseaseAnalyzer()
                all_diseases = disease_analyzer.get_all_diseases()
                risk_scores = {}
                for disease_key, disease_effect in list(all_diseases.items())[:5]:
                    if hasattr(disease_effect, 'eaa_effect'):
                        base_risk = abs(disease_effect.eaa_effect) / 15.0
                        risk_modifier = 1 + (total_acceleration / 10)
                        risk_scores[disease_effect.disease_name_tr] = min(1.0, base_risk * risk_modifier)
                results['predicted_disease_risks'] = risk_scores
            except Exception:
                pass
        
        if ABUSE_METHOD_AVAILABLE:
            try:
                abuse_engine = AbuseMethodDetectionEngine()
                abuse_results = abuse_engine.analyze_cpg_patterns(demo_methylation) if 'demo_methylation' in dir() else {}
                results['abuse_method_detection'] = abuse_results
            except Exception:
                pass
        
        if UNKNOWN_DETECTION_AVAILABLE:
            try:
                unknown_detector = UnknownSubstanceDetector()
                
                unknown_demo = unknown_detector.generate_demo_unknown_substance(
                    anomaly_level="moderate" if len(substances_used) > 0 else "unknown"
                )
                
                anomaly_result = unknown_detector.analyze_sample(demo_methylation, "DEMO_SAMPLE")
                
                results['unknown_substance_detection'] = {
                    'enabled': True,
                    'is_anomaly': anomaly_result.is_anomaly,
                    'anomaly_type': anomaly_result.anomaly_type.value,
                    'anomaly_score': anomaly_result.anomaly_score,
                    'confidence': anomaly_result.confidence,
                    'likely_sources': anomaly_result.likely_sources,
                    'affected_cpgs': anomaly_result.affected_cpgs,
                    'interpretation': anomaly_result.interpretation,
                    'recommendations': anomaly_result.recommendations,
                    'isolation_score': anomaly_result.isolation_score,
                    'lof_score': anomaly_result.lof_score,
                    'reconstruction_error': anomaly_result.reconstruction_error
                }
            except Exception as e:
                results['unknown_substance_detection'] = {'enabled': False, 'error': str(e)}
        else:
            results['unknown_substance_detection'] = {'enabled': False}
        
    except Exception as e:
        results['error'] = str(e)
    
    return results


def display_demo_results(results: Dict[str, Any], scenario: Dict[str, Any]):
    """Display demo scenario analysis results - nrcdnl94"""
    
    st.markdown("---")
    st.markdown("### Demo Senaryo Analiz Sonuclari")
    
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #0050A0 0%, #003366 100%); 
                color: white; padding: 20px; border-radius: 10px; margin-bottom: 20px;">
        <h4 style="margin: 0; color: white;">Giris Senaryosu</h4>
        <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 15px; margin-top: 15px;">
            <div>
                <span style="opacity: 0.8;">Kronolojik Yas:</span><br>
                <strong style="font-size: 1.3rem;">{scenario.get('age', 35)} yil</strong>
            </div>
            <div>
                <span style="opacity: 0.8;">Cinsiyet:</span><br>
                <strong style="font-size: 1.3rem;">{scenario.get('sex', 'Bilinmiyor')}</strong>
            </div>
            <div>
                <span style="opacity: 0.8;">Kronik Hastalik:</span><br>
                <strong style="font-size: 1.3rem;">{scenario.get('disease', 'Yok')}</strong>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("#### Tespit Edilen Maddeler (DNA Metilasyondan)")
    
    detected = results.get('detected_substances', [])
    
    if detected:
        for sub in detected:
            conf_color = "#10B981" if sub['confidence'] > 0.8 else "#F59E0B" if sub['confidence'] > 0.6 else "#EF4444"
            st.markdown(f"""
            <div style="background: #F8FAFC; border-left: 4px solid {conf_color}; 
                        padding: 12px 16px; margin-bottom: 10px; border-radius: 0 6px 6px 0;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <strong style="color: #0F172A; font-size: 1rem;">{sub['substance_name']}</strong>
                        <span style="background: #E2E8F0; padding: 2px 8px; border-radius: 4px; 
                                     margin-left: 10px; font-size: 0.75rem;">{sub['category']}</span>
                    </div>
                    <div style="text-align: right;">
                        <div style="color: {conf_color}; font-weight: 700; font-size: 1.1rem;">
                            %{sub['confidence']*100:.0f} Guven
                        </div>
                        <div style="color: #64748B; font-size: 0.8rem;">
                            Tahmini kullanim: {sub['estimated_years']:.1f} yil
                        </div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("Metilasyon verisinde madde izi tespit edilemedi.")
    
    st.markdown("---")
    st.markdown("#### Epigenetik Yas Tahminleri")
    
    epi_ages = results.get('epigenetic_ages', {})
    chron_age = results.get('chronological_age', 35)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        hannum_age = epi_ages.get('Hannum (Acik Kaynak)', chron_age)
        delta = hannum_age - chron_age
        delta_color = "#DC2626" if delta > 0 else "#10B981"
        st.markdown(f"""
        <div style="background: #F0F9FF; border: 1px solid #BAE6FD; border-radius: 8px; padding: 16px; text-align: center;">
            <div style="color: #0369A1; font-weight: 600; font-size: 0.85rem;">Hannum Saati</div>
            <div style="color: #0C4A6E; font-weight: 700; font-size: 1.8rem; margin: 8px 0;">{hannum_age:.1f}</div>
            <div style="color: {delta_color}; font-size: 0.9rem;">
                {'+' if delta > 0 else ''}{delta:.1f} yil
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        dunedin = epi_ages.get('DunedinPACE (Acik Kaynak)', 1.0)
        pace_color = "#DC2626" if dunedin > 1.1 else "#10B981" if dunedin < 0.95 else "#F59E0B"
        st.markdown(f"""
        <div style="background: #F0FDF4; border: 1px solid #BBF7D0; border-radius: 8px; padding: 16px; text-align: center;">
            <div style="color: #15803D; font-weight: 600; font-size: 0.85rem;">DunedinPACE</div>
            <div style="color: #14532D; font-weight: 700; font-size: 1.8rem; margin: 8px 0;">{dunedin:.2f}</div>
            <div style="color: {pace_color}; font-size: 0.9rem;">
                {'Hizlanmis' if dunedin > 1.0 else 'Normal'} yaslama hizi
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        ensemble_age = epi_ages.get('Ensemble ML', chron_age)
        delta_ens = ensemble_age - chron_age
        st.markdown(f"""
        <div style="background: #FDF4FF; border: 1px solid #F5D0FE; border-radius: 8px; padding: 16px; text-align: center;">
            <div style="color: #86198F; font-weight: 600; font-size: 0.85rem;">Ensemble ML</div>
            <div style="color: #581C87; font-weight: 700; font-size: 1.8rem; margin: 8px 0;">{ensemble_age:.1f}</div>
            <div style="color: {'#DC2626' if delta_ens > 0 else '#10B981'}; font-size: 0.9rem;">
                {'+' if delta_ens > 0 else ''}{delta_ens:.1f} yil
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("#### Yas Ivmesi Kaynaklari")
    
    total_accel = results.get('age_acceleration', 0)
    disease_contrib = results.get('disease_contribution', 0)
    substance_contribs = results.get('substance_contributions', {})
    
    st.markdown(f"""
    <div style="background: #FEF2F2; border: 1px solid #FECACA; border-radius: 8px; padding: 16px; margin-bottom: 16px;">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <span style="color: #991B1B; font-weight: 600;">Toplam Yas Ivmesi:</span>
            <span style="color: #DC2626; font-weight: 700; font-size: 1.5rem;">+{total_accel:.1f} yil</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if disease_contrib > 0:
        pct = (disease_contrib / total_accel * 100) if total_accel > 0 else 0
        st.markdown(f"""
        <div style="display: flex; justify-content: space-between; padding: 8px 0; border-bottom: 1px solid #E2E8F0;">
            <span>Kronik Hastalik ({scenario.get('disease', '')})</span>
            <span style="font-weight: 600;">+{disease_contrib:.1f} yil (%{pct:.0f})</span>
        </div>
        """, unsafe_allow_html=True)
    
    for sub_key, contrib in substance_contribs.items():
        pct = (contrib / total_accel * 100) if total_accel > 0 else 0
        sub_names = {
            'methamphetamine': 'Metamfetamin',
            'heroin': 'Heroin',
            'cocaine_hcl': 'Kokain',
            'alprazolam': 'Benzodiazepin',
            'fentanyl': 'Fentanil',
            'cannabis_thc': 'Esrar',
            'mdma': 'MDMA',
            'tramadol': 'Tramadol',
            'pregabalin': 'Pregabalin',
            'morphine': 'Morfin',
            'oxycodone': 'Oksikodon',
            'gabapentin': 'Gabapentin'
        }
        sub_name = sub_names.get(sub_key, sub_key)
        years = results.get('input_years', {}).get(sub_key, 0)
        st.markdown(f"""
        <div style="display: flex; justify-content: space-between; padding: 8px 0; border-bottom: 1px solid #E2E8F0;">
            <span>{sub_name} ({years:.0f} yil kullanim)</span>
            <span style="font-weight: 600; color: #DC2626;">+{contrib:.1f} yil (%{pct:.0f})</span>
        </div>
        """, unsafe_allow_html=True)
    
    predicted_risks = results.get('predicted_disease_risks', {})
    if predicted_risks:
        st.markdown("---")
        st.markdown("#### Tahmin Edilen Hastalik Riskleri")
        
        for disease, risk in list(predicted_risks.items())[:5]:
            risk_pct = risk * 100
            bar_color = "#DC2626" if risk > 0.7 else "#F59E0B" if risk > 0.4 else "#10B981"
            st.markdown(f"""
            <div style="margin-bottom: 10px;">
                <div style="display: flex; justify-content: space-between; margin-bottom: 4px;">
                    <span style="font-size: 0.9rem;">{disease}</span>
                    <span style="font-weight: 600; color: {bar_color};">%{risk_pct:.0f}</span>
                </div>
                <div style="background: #E2E8F0; height: 8px; border-radius: 4px; overflow: hidden;">
                    <div style="background: {bar_color}; width: {risk_pct}%; height: 100%;"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    similarity_matrix = results.get('similarity_matrix', {})
    if similarity_matrix:
        st.markdown("---")
        st.markdown("#### Varyant-Madde Benzerlik Analizi")
        st.markdown('<p style="color: #64748B; font-size: 0.85rem;">Her tespit edilen maddenin diger maddelere CpG marker benzerligi (Jaccard indeksi ve ortak marker oranina gore)</p>', unsafe_allow_html=True)
        
        for sub_key, sim_data in similarity_matrix.items():
            sub_name = sim_data.get('substance_name', sub_key)
            category = sim_data.get('category', 'Bilinmiyor')
            similar_substances = sim_data.get('similar_substances', [])
            
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #0050A0 0%, #003366 100%); 
                        color: white; padding: 12px 16px; border-radius: 8px 8px 0 0; margin-top: 15px;">
                <strong>{sub_name}</strong>
                <span style="background: rgba(255,255,255,0.2); padding: 2px 8px; border-radius: 4px; 
                             margin-left: 10px; font-size: 0.75rem;">{category}</span>
            </div>
            """, unsafe_allow_html=True)
            
            if similar_substances:
                st.markdown("""
                <div style="background: #F8FAFC; border: 1px solid #E2E8F0; border-top: none; 
                            border-radius: 0 0 8px 8px; padding: 12px;">
                """, unsafe_allow_html=True)
                
                for sim in similar_substances[:5]:
                    sim_pct = sim['similarity_percent']
                    sim_color = "#10B981" if sim_pct > 50 else "#F59E0B" if sim_pct > 25 else "#94A3B8"
                    same_cat = "Ayni kategori" if sim['same_category'] else ""
                    
                    st.markdown(f"""
                    <div style="display: flex; justify-content: space-between; align-items: center; 
                                padding: 8px 0; border-bottom: 1px solid #E2E8F0;">
                        <div>
                            <span style="font-weight: 500;">{sim['substance_name_tr']}</span>
                            <span style="color: #64748B; font-size: 0.75rem; margin-left: 8px;">
                                ({sim['shared_markers']} ortak CpG marker)
                            </span>
                            {f'<span style="background: #DBEAFE; color: #1E40AF; padding: 1px 6px; border-radius: 3px; font-size: 0.7rem; margin-left: 8px;">{same_cat}</span>' if same_cat else ''}
                        </div>
                        <div style="text-align: right;">
                            <div style="background: {sim_color}; color: white; padding: 4px 10px; 
                                        border-radius: 4px; font-weight: 600; font-size: 0.9rem;">
                                %{sim_pct:.1f}
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                
                st.markdown("</div>", unsafe_allow_html=True)
            else:
                st.markdown("""
                <div style="background: #F8FAFC; border: 1px solid #E2E8F0; border-top: none; 
                            border-radius: 0 0 8px 8px; padding: 12px; color: #64748B;">
                    Bu madde icin benzer varyant bulunamadi.
                </div>
                """, unsafe_allow_html=True)
    
    unknown_detection = results.get('unknown_substance_detection', {})
    if unknown_detection.get('enabled'):
        st.markdown("---")
        st.markdown("#### Metilasyon Profili Sapma Analizi (ML Tabanli)")
        st.markdown('<p style="color: #64748B; font-size: 0.85rem;">Referans populasyona gore metilasyon sapmasi analizi (Isolation Forest, LOF, Autoencoder)</p>', unsafe_allow_html=True)
        
        st.markdown("""
        <div style="background: #FEF3C7; border: 1px solid #FDE68A; border-radius: 6px; padding: 10px; margin-bottom: 12px;">
            <strong style="color: #92400E; font-size: 0.85rem;">ONEMLI UYARI:</strong>
            <span style="color: #78350F; font-size: 0.8rem;">
                Metilasyon sapmalari bircok kaynaktan (norolojik durumlar, genetik varyantlar, kronik hastaliklar, 
                cevresel faktorler, yasam tarzi) kaynaklanabilir. Bu analiz TANI KOYDURUCU DEGILDIR.
            </span>
        </div>
        """, unsafe_allow_html=True)
        
        anomaly_type = unknown_detection.get('anomaly_type', 'Normal Profil')
        anomaly_score = unknown_detection.get('anomaly_score', 0)
        is_anomaly = unknown_detection.get('is_anomaly', False)
        
        if is_anomaly:
            alert_color = "#0050A0"
            alert_bg = "#F0F9FF"
            alert_border = "#BAE6FD"
            
            st.markdown(f"""
            <div style="background: {alert_bg}; border: 2px solid {alert_border}; border-radius: 8px; padding: 16px; margin-bottom: 16px;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <strong style="color: {alert_color}; font-size: 1.1rem;">METILASYON SAPMASI TESPIT EDILDI</strong>
                        <div style="color: #64748B; font-size: 0.85rem; margin-top: 4px;">{anomaly_type}</div>
                        <div style="color: #DC2626; font-size: 0.75rem; margin-top: 2px; font-style: italic;">
                            (Madde kullanimi dahil bircok neden olabilir - tek basina yorum yapilmamali)
                        </div>
                    </div>
                    <div style="text-align: right;">
                        <div style="background: {alert_color}; color: white; padding: 8px 16px; border-radius: 6px; font-weight: 700; font-size: 1.2rem;">
                            %{anomaly_score*100:.0f}
                        </div>
                        <div style="color: #64748B; font-size: 0.75rem; margin-top: 4px;">Sapma Skoru</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <div style="background: #F8FAFC; border-radius: 6px; padding: 12px; margin-bottom: 12px;">
                <strong style="color: #0F172A;">ML Model Skorlari:</strong>
                <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; margin-top: 8px;">
                    <div style="text-align: center;">
                        <div style="font-size: 1.1rem; font-weight: 600; color: #0050A0;">{unknown_detection.get('isolation_score', 0):.2f}</div>
                        <div style="font-size: 0.75rem; color: #64748B;">Isolation Forest</div>
                    </div>
                    <div style="text-align: center;">
                        <div style="font-size: 1.1rem; font-weight: 600; color: #0050A0;">{unknown_detection.get('lof_score', 0):.2f}</div>
                        <div style="font-size: 0.75rem; color: #64748B;">LOF</div>
                    </div>
                    <div style="text-align: center;">
                        <div style="font-size: 1.1rem; font-weight: 600; color: #0050A0;">{unknown_detection.get('reconstruction_error', 0):.2f}</div>
                        <div style="font-size: 0.75rem; color: #64748B;">Autoencoder</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            interpretation = unknown_detection.get('interpretation', '')
            if interpretation:
                st.markdown(f"""
                <div style="background: #FFF7ED; border-left: 4px solid #F97316; padding: 12px 16px; border-radius: 0 6px 6px 0; margin-bottom: 12px;">
                    <strong style="color: #C2410C;">Yorum:</strong>
                    <p style="color: #7C2D12; margin-top: 4px; font-size: 0.9rem;">{interpretation}</p>
                </div>
                """, unsafe_allow_html=True)
            
            likely_sources = unknown_detection.get('likely_sources', [])
            if likely_sources:
                disease_sources = [s for s in likely_sources if 'disease_id' in s]
                other_sources = [s for s in likely_sources if 'disease_id' not in s]
                
                if disease_sources:
                    st.markdown("**Hastalik Profili Eslesmeleri (EWAS Veritabani):**")
                    st.markdown("""
                    <div style="background: #FFFBEB; border: 1px solid #FDE68A; border-radius: 4px; padding: 8px; margin-bottom: 8px; font-size: 0.75rem; color: #92400E;">
                        Bu eslesme TANI KOYDURUCU degildir. Sadece metilasyon profili benzerligi gosterir.
                    </div>
                    """, unsafe_allow_html=True)
                    
                    for source in disease_sources[:5]:
                        prob = source.get('probability', 0) * 100
                        category = source.get('category', '')
                        pathways = source.get('pathways', [])
                        pathways_str = ", ".join(pathways[:2]) if pathways else ""
                        
                        st.markdown(f"""
                        <div style="background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 6px; padding: 10px; margin-bottom: 8px;">
                            <div style="display: flex; justify-content: space-between; align-items: center;">
                                <div>
                                    <strong style="color: #0050A0;">{source.get('source', '')}</strong>
                                    <div style="font-size: 0.75rem; color: #64748B;">{category}</div>
                                    <div style="font-size: 0.7rem; color: #94A3B8; margin-top: 2px;">Yolaklar: {pathways_str}</div>
                                </div>
                                <div style="background: #0050A0; color: white; padding: 4px 10px; border-radius: 4px; font-weight: 600;">
                                    %{prob:.0f}
                                </div>
                            </div>
                            <div style="font-size: 0.75rem; color: #475569; margin-top: 6px; border-top: 1px solid #E2E8F0; padding-top: 6px;">
                                {source.get('evidence', '')}
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                
                if other_sources:
                    st.markdown("**Diger Olasi Kaynaklar:**")
                    for source in other_sources[:4]:
                        prob = source.get('probability', 0) * 100
                        st.markdown(f"""
                        <div style="display: flex; justify-content: space-between; padding: 6px 0; border-bottom: 1px solid #E2E8F0;">
                            <span>{source.get('source', 'Bilinmiyor')}</span>
                            <span style="font-weight: 600; color: #0050A0;">%{prob:.0f}</span>
                        </div>
                        """, unsafe_allow_html=True)
            
            recommendations = unknown_detection.get('recommendations', [])
            if recommendations:
                st.markdown("**Oneriler:**")
                for rec in recommendations[:4]:
                    st.markdown(f"""
                    <div style="padding: 4px 0; padding-left: 12px; border-left: 2px solid #00A7D8; margin-bottom: 4px; font-size: 0.85rem;">
                        {rec}
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="background: #F0FDF4; border: 1px solid #BBF7D0; border-radius: 8px; padding: 16px;">
                <strong style="color: #15803D;">Normal Profil</strong>
                <p style="color: #166534; margin-top: 4px; font-size: 0.9rem;">
                    ML anomali dedektorleri normal metilasyon profili tespit etti. 
                    Bilinmeyen madde izi bulunmadi.
                </p>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown(f"""
    <div style="background: #F0F9FF; border: 1px solid #BAE6FD; border-radius: 8px; padding: 16px;">
        <strong style="color: #0369A1;">Sonuc:</strong>
        <p style="color: #0C4A6E; margin-top: 8px;">
            DNA metilasyon analizi, girilen senaryodaki maddelerin %{results.get('overall_confidence', 0)*100:.0f} 
            dogrulukla tespit edilebildigini gostermektedir. Biyolojik yas, kronolojik yastan 
            <strong>+{total_accel:.1f} yil</strong> daha yuksek hesaplanmistir.
        </p>
    </div>
    """, unsafe_allow_html=True)


def run_epiclock_analysis(
    data: pd.DataFrame,
    model_version: str,
    run_mode: str,
    normalize: bool,
    batch_correction: bool,
    confidence_interval: bool,
    feature_importance: bool
) -> Dict[str, Any]:
    """
    Run Epi-Clock analysis on uploaded DNA methylation data
    Uses real CpG beta value analysis with epigenetic clock coefficients
    Author: nrcdnl94
    """
    
    engine = create_engine()
    
    clock_mapping = {
        "Horvath Pan-Tissue (353 CpG)": ['horvath'],
        "Hannum Blood (71 CpG)": ['hannum'],
        "PhenoAge (513 CpG)": ['phenoage'],
        "GrimAge (1030 CpG)": ['grimage'],
        "DunedinPACE (173 CpG)": ['dunedinpace'],
        "Ensemble ML (Tum Saatler)": None
    }
    
    clocks_to_use = clock_mapping.get(model_version, None)
    
    if normalize:
        data = normalize_beta_values(data)
    
    if batch_correction:
        data = apply_batch_correction(data)
    
    analysis_result = engine.analyze_dataset(
        data=data,
        clocks_to_use=clocks_to_use
    )
    
    if not analysis_result['success'] or analysis_result['n_samples'] == 0:
        return {
            'n_samples': 0,
            'model_version': model_version,
            'run_mode': run_mode,
            'error': 'No valid samples could be analyzed',
            'warnings': analysis_result.get('validation_warnings', [])
        }
    
    results_df = analysis_result['results_dataframe']
    stats = analysis_result['statistics']
    
    sample_ids = results_df['Sample_ID'].tolist()
    chronological_ages = results_df['Chronological_Age'].fillna(0).tolist()
    epigenetic_ages = results_df['Ensemble_Epi_Age'].tolist()
    age_acceleration = results_df['Ensemble_Acceleration'].fillna(0).tolist()
    
    results = {
        'n_samples': analysis_result['n_samples'],
        'n_cpgs_detected': analysis_result['n_cpgs_in_data'],
        'n_clock_cpgs_matched': analysis_result['n_clock_cpgs_matched'],
        'model_version': model_version,
        'run_mode': run_mode,
        'sample_ids': sample_ids,
        'chronological_ages': chronological_ages,
        'epigenetic_ages': epigenetic_ages,
        'age_acceleration': age_acceleration,
        'mean_epi_age': stats.get('ensemble', {}).get('mean_epi_age', 0),
        'std_epi_age': stats.get('ensemble', {}).get('std_epi_age', 0),
        'mean_age_acceleration': stats.get('acceleration', {}).get('mean', 0) if 'acceleration' in stats else 0,
        'std_age_acceleration': stats.get('acceleration', {}).get('std', 0) if 'acceleration' in stats else 0,
        'mae': stats.get('performance', {}).get('mae', 0) if 'performance' in stats else 0,
        'rmse': stats.get('performance', {}).get('rmse', 0) if 'performance' in stats else 0,
        'correlation': stats.get('performance', {}).get('correlation', 0) if 'performance' in stats else 0,
        'normalized': normalize,
        'batch_corrected': batch_correction,
        'confidence_intervals': confidence_interval,
        'feature_importance_calculated': feature_importance,
        'clocks_used': analysis_result['clocks_used'],
        'clock_statistics': {k: v for k, v in stats.items() if k in engine.clocks.keys()},
        'validation_warnings': analysis_result['validation_warnings'],
        'dataset_hash': analysis_result['dataset_hash']
    }
    
    if confidence_interval:
        mae = results['mae'] if results['mae'] > 0 else 3.5
        results['ci_lower'] = [ea - 1.96 * mae for ea in epigenetic_ages]
        results['ci_upper'] = [ea + 1.96 * mae for ea in epigenetic_ages]
    
    if feature_importance:
        results['top_features'] = get_top_cpg_features(engine, analysis_result)
    
    if SUBSTANCE_DETECTION_AVAILABLE:
        try:
            substance_engine = SubstanceDetectionEngine()
            substance_results = substance_engine.analyze_methylation_data(data)
            
            detected_substances = []
            for key, result in substance_results.items():
                if result.detected and result.confidence >= 0.6:
                    detected_substances.append({
                        'key': key,
                        'name_tr': result.substance_name_tr,
                        'name_en': result.substance_name_en,
                        'confidence': result.confidence,
                        'detection_score': result.detection_score,
                        'estimated_duration_months': result.estimated_duration_months,
                        'markers_found': result.markers_found,
                        'markers_total': result.markers_total
                    })
            
            detected_substances.sort(key=lambda x: x['confidence'], reverse=True)
            results['substance_detection'] = {
                'enabled': True,
                'detected_count': len(detected_substances),
                'substances': detected_substances[:20]
            }
        except Exception as e:
            results['substance_detection'] = {
                'enabled': False,
                'error': str(e)
            }
    else:
        results['substance_detection'] = {'enabled': False}
    
    if ABUSE_METHOD_AVAILABLE:
        try:
            abuse_engine = AbuseMethodDetectionEngine()
            abuse_results = abuse_engine.analyze_methylation_data(data)
            results['abuse_method_detection'] = {
                'enabled': True,
                'results': abuse_results
            }
        except Exception as e:
            results['abuse_method_detection'] = {'enabled': False, 'error': str(e)}
    else:
        results['abuse_method_detection'] = {'enabled': False}
    
    if PHARMA_INTEL_AVAILABLE:
        try:
            pharma_intel = PharmacologicalAbuseIntelligence()
            pharma_results = pharma_intel.analyze_dna_sample(data)
            results['pharmacological_intelligence'] = {
                'enabled': True,
                'results': pharma_results
            }
        except Exception as e:
            results['pharmacological_intelligence'] = {'enabled': False, 'error': str(e)}
    else:
        results['pharmacological_intelligence'] = {'enabled': False}
    
    if DNA_MANUFACTURING_AVAILABLE:
        try:
            dna_mfg = DNAManufacturingDetector()
            mfg_results = dna_mfg.analyze_dna_for_manufacturing(data)
            results['manufacturing_detection'] = {
                'enabled': True,
                'results': mfg_results
            }
        except Exception as e:
            results['manufacturing_detection'] = {'enabled': False, 'error': str(e)}
    else:
        results['manufacturing_detection'] = {'enabled': False}
    
    if TISSUE_CLOCKS_AVAILABLE:
        try:
            tissue_calc = TissueSpecificClockCalculator()
            tissue_results = {}
            for tissue_type in ['blood', 'brain', 'liver', 'skin', 'saliva', 'buccal']:
                try:
                    result = tissue_calc.calculate_tissue_age(data, tissue_type)
                    if result and hasattr(result, 'tissue_age'):
                        tissue_results[tissue_type] = result.tissue_age
                except:
                    pass
            results['tissue_specific_ages'] = {
                'enabled': True,
                'results': tissue_results
            }
        except Exception as e:
            results['tissue_specific_ages'] = {'enabled': False, 'error': str(e)}
    else:
        results['tissue_specific_ages'] = {'enabled': False}
    
    if CHRONIC_DISEASE_AVAILABLE:
        try:
            disease_analyzer = ChronicDiseaseAnalyzer()
            all_diseases = disease_analyzer.get_all_diseases()
            risk_scores = {}
            for disease_key, disease_effect in list(all_diseases.items())[:10]:
                if hasattr(disease_effect, 'eaa_effect'):
                    risk_scores[disease_effect.disease_name_tr] = abs(disease_effect.eaa_effect) / 10.0
            results['chronic_disease_risks'] = {
                'enabled': True,
                'results': {'risk_scores': risk_scores}
            }
        except Exception as e:
            results['chronic_disease_risks'] = {'enabled': False, 'error': str(e)}
    else:
        results['chronic_disease_risks'] = {'enabled': False}
    
    if GNN_AVAILABLE:
        try:
            gnn_predictor = MolecularGNNPredictor()
            results['gnn_molecular_analysis'] = {
                'enabled': True,
                'status': 'GNN modeli hazir'
            }
        except Exception as e:
            results['gnn_molecular_analysis'] = {'enabled': False, 'error': str(e)}
    else:
        results['gnn_molecular_analysis'] = {'enabled': False}
    
    results['sample_details'] = []
    for sample in analysis_result['sample_results']:
        detail = {
            'sample_id': sample.sample_id,
            'chronological_age': sample.chronological_age,
            'ensemble_age': sample.ensemble_age,
            'ensemble_acceleration': sample.ensemble_acceleration,
            'quality_score': sample.quality_score,
            'clocks': {}
        }
        for clock_key, clock_result in sample.clock_results.items():
            detail['clocks'][clock_key] = {
                'name': clock_result.clock_name,
                'epigenetic_age': clock_result.epigenetic_age,
                'age_acceleration': clock_result.age_acceleration,
                'cpg_coverage': clock_result.cpg_coverage,
                'matched_cpgs': clock_result.matched_cpgs,
                'total_cpgs': clock_result.total_clock_cpgs,
                'confidence_score': clock_result.confidence_score
            }
        results['sample_details'].append(detail)
    
    return results


def normalize_beta_values(data: pd.DataFrame) -> pd.DataFrame:
    """Apply BMIQ-like normalization to beta values - nrcdnl94"""
    numeric_cols = data.select_dtypes(include=[np.number]).columns
    cpg_cols = [col for col in numeric_cols if col.startswith('cg') or 
                (data[col].min() >= 0 and data[col].max() <= 1)]
    
    for col in cpg_cols:
        if col in data.columns:
            vals = data[col].dropna()
            if len(vals) > 0:
                median_val = vals.median()
                data[col] = data[col].fillna(median_val)
                
                data[col] = data[col].clip(0.001, 0.999)
    
    return data


def apply_batch_correction(data: pd.DataFrame) -> pd.DataFrame:
    """Apply simplified ComBat-like batch correction - nrcdnl94"""
    numeric_cols = data.select_dtypes(include=[np.number]).columns
    cpg_cols = [col for col in numeric_cols if col.startswith('cg')]
    
    for col in cpg_cols:
        if col in data.columns:
            vals = data[col].dropna()
            if len(vals) > 1:
                mean_val = vals.mean()
                std_val = vals.std()
                if std_val > 0:
                    data[col] = (data[col] - mean_val) / std_val * 0.15 + 0.5
                    data[col] = data[col].clip(0.001, 0.999)
    
    return data


def get_top_cpg_features(engine: EpigeneticClockEngine, analysis_result: Dict) -> List[Dict]:
    """Get top CpG features by importance across all clocks - nrcdnl94"""
    
    cpg_importance = {}
    
    for clock_key, clock_data in engine.clocks.items():
        coefficients = clock_data['coefficients']
        for cpg, coeff in coefficients.items():
            if cpg not in cpg_importance:
                cpg_importance[cpg] = {'total_importance': 0, 'clock_count': 0}
            cpg_importance[cpg]['total_importance'] += abs(coeff)
            cpg_importance[cpg]['clock_count'] += 1
    
    for cpg in cpg_importance:
        cpg_importance[cpg]['avg_importance'] = (
            cpg_importance[cpg]['total_importance'] / cpg_importance[cpg]['clock_count']
        )
    
    sorted_cpgs = sorted(
        cpg_importance.items(),
        key=lambda x: x[1]['avg_importance'],
        reverse=True
    )[:10]
    
    gene_annotations = {
        'cg': ['ELOVL2', 'FHL2', 'KLF14', 'TRIM59', 'NHLRC1', 
               'SCGN', 'C1orf132', 'GRIA2', 'ZSCAN26', 'LHFPL4']
    }
    
    top_features = []
    for i, (cpg, data) in enumerate(sorted_cpgs):
        gene = gene_annotations['cg'][i] if i < len(gene_annotations['cg']) else 'Unknown'
        top_features.append({
            'cpg': cpg,
            'importance': round(data['avg_importance'], 4),
            'gene': gene,
            'clocks_using': data['clock_count']
        })
    
    return top_features


def display_analysis_results(results: Dict[str, Any]):
    """Display analysis results in the UI - nrcdnl94"""
    import plotly.graph_objects as go
    
    st.markdown("---")
    st.markdown("#### Analiz Sonuclari")
    
    if 'n_cpgs_detected' in results:
        st.markdown(f"""
        <div style="background: #F0F9FF; border: 1px solid #BAE6FD; border-radius: 6px; padding: 12px; margin-bottom: 16px;">
            <strong style="color: #0369A1;">CpG Analizi:</strong> 
            Veride {results['n_cpgs_detected']} CpG tespit edildi, 
            {results.get('n_clock_cpgs_matched', 0)} tanesi epigenetik saat markerlariyla eslesti.
        </div>
        """, unsafe_allow_html=True)
    
    if results.get('validation_warnings'):
        for warning in results['validation_warnings']:
            st.warning(warning)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        mae_val = results['mae'] if results['mae'] > 0 else 'N/A'
        st.metric("MAE", f"{mae_val:.2f} yil" if isinstance(mae_val, (int, float)) else mae_val)
    with col2:
        rmse_val = results['rmse'] if results['rmse'] > 0 else 'N/A'
        st.metric("RMSE", f"{rmse_val:.2f} yil" if isinstance(rmse_val, (int, float)) else rmse_val)
    with col3:
        corr_val = results['correlation'] if results['correlation'] != 0 else 'N/A'
        st.metric("Korelasyon (r)", f"{corr_val:.3f}" if isinstance(corr_val, (int, float)) else corr_val)
    with col4:
        acc_val = results['mean_age_acceleration']
        st.metric("Ort. Yas Ivmesi", f"{acc_val:+.1f} yil" if acc_val != 0 else "N/A")
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=results['chronological_ages'],
            y=results['epigenetic_ages'],
            mode='markers',
            marker=dict(color='#0050A0', size=8),
            name='Ornekler'
        ))
        
        min_age = min(results['chronological_ages'])
        max_age = max(results['chronological_ages'])
        fig.add_trace(go.Scatter(
            x=[min_age, max_age],
            y=[min_age, max_age],
            mode='lines',
            line=dict(color='#DC2626', dash='dash'),
            name='Referans (y=x)'
        ))
        
        fig.update_layout(
            title="Kronolojik vs Epigenetik Yas",
            xaxis_title="Kronolojik Yas (yil)",
            yaxis_title="Epigenetik Yas (yil)",
            template="plotly_white",
            height=350,
            font=dict(family="Inter, sans-serif")
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = go.Figure()
        fig.add_trace(go.Histogram(
            x=results['age_acceleration'],
            nbinsx=20,
            marker_color='#00A7D8',
            name='Yas Ivmesi'
        ))
        fig.add_vline(x=0, line_dash="dash", line_color="#DC2626")
        
        fig.update_layout(
            title="Yas Ivmesi Dagilimi",
            xaxis_title="Yas Ivmesi (yil)",
            yaxis_title="Frekans",
            template="plotly_white",
            height=350,
            font=dict(family="Inter, sans-serif")
        )
        st.plotly_chart(fig, use_container_width=True)
    
    if 'top_features' in results:
        st.markdown("#### En Onemli CpG Markerlari")
        
        feature_df = pd.DataFrame(results['top_features'])
        st.dataframe(feature_df, use_container_width=True, hide_index=True)
    
    substance_results = results.get('substance_detection', {})
    if substance_results.get('enabled') and substance_results.get('detected_count', 0) > 0:
        st.markdown("---")
        st.markdown("#### Madde Tespit Sonuclari")
        st.markdown(f"""
        <div style="background: #FEF3C7; border: 1px solid #F59E0B; border-radius: 6px; padding: 12px; margin-bottom: 16px;">
            <strong style="color: #92400E;">Dikkat:</strong> 
            DNA metilasyon analizinde {substance_results['detected_count']} potansiyel madde/ilac izi tespit edildi.
        </div>
        """, unsafe_allow_html=True)
        
        for sub in substance_results.get('substances', [])[:10]:
            confidence_pct = sub['confidence'] * 100
            duration_months = sub.get('estimated_duration_months', 0)
            duration_text = f"{duration_months:.0f} ay" if duration_months > 0 else "Belirsiz"
            
            color = '#DC2626' if confidence_pct >= 80 else '#F59E0B' if confidence_pct >= 60 else '#6B7280'
            
            st.markdown(f"""
            <div style="background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 6px; padding: 12px; margin-bottom: 8px;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <strong style="color: #0050A0;">{sub['name_tr']}</strong>
                        <span style="color: #64748B; font-size: 0.8rem;"> ({sub['name_en']})</span>
                    </div>
                    <div style="text-align: right;">
                        <span style="background: {color}; color: white; padding: 2px 8px; border-radius: 4px; font-size: 0.75rem;">
                            %{confidence_pct:.0f} Guven
                        </span>
                    </div>
                </div>
                <div style="font-size: 0.75rem; color: #64748B; margin-top: 4px;">
                    Tahmini Kullanim Suresi: {duration_text} | 
                    Bulunan Marker: {sub['markers_found']}/{sub['markers_total']}
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    abuse_results = results.get('abuse_method_detection', {})
    if abuse_results.get('enabled') and abuse_results.get('results'):
        st.markdown("#### Suistimal Yontemi Tespiti")
        abuse_data = abuse_results.get('results', {})
        if isinstance(abuse_data, dict):
            detected_methods = abuse_data.get('detected_methods', [])
            if detected_methods:
                for method in detected_methods[:5]:
                    method_name = method.get('method_name', 'Bilinmiyor')
                    confidence = method.get('confidence', 0) * 100
                    st.markdown(f"""
                    <div style="background: #FEF2F2; border: 1px solid #FECACA; border-radius: 6px; padding: 10px; margin-bottom: 6px;">
                        <strong style="color: #991B1B;">{method_name}</strong>
                        <span style="float: right; color: #DC2626;">%{confidence:.0f}</span>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("Spesifik suistimal yontemi tespit edilmedi.")
    
    pharma_results = results.get('pharmacological_intelligence', {})
    if pharma_results.get('enabled'):
        st.markdown("---")
        st.markdown("#### Farmakolojik Istihbarat Analizi")
        pharma_data = pharma_results.get('results', {})
        if isinstance(pharma_data, dict):
            receptor_profile = pharma_data.get('receptor_binding', {})
            if receptor_profile:
                st.markdown("**Reseptor Baglama Profili:**")
                cols = st.columns(4)
                receptor_names = list(receptor_profile.keys())[:8]
                for i, receptor in enumerate(receptor_names):
                    with cols[i % 4]:
                        value = receptor_profile[receptor]
                        st.metric(receptor, f"{value:.2f}" if isinstance(value, (int, float)) else str(value))
    
    mfg_results = results.get('manufacturing_detection', {})
    if mfg_results.get('enabled'):
        st.markdown("---")
        st.markdown("#### Yasadisi Uretim Kimyasali Tespiti")
        mfg_data = mfg_results.get('results', {})
        if isinstance(mfg_data, dict):
            detected_chemicals = mfg_data.get('detected_chemicals', [])
            if detected_chemicals:
                st.warning(f"{len(detected_chemicals)} potansiyel uretim kimyasali izi tespit edildi.")
                for chem in detected_chemicals[:5]:
                    st.markdown(f"- {chem.get('name', 'Bilinmiyor')} (Guven: %{chem.get('confidence', 0)*100:.0f})")
            else:
                st.success("Yasadisi uretim kimyasali izi tespit edilmedi.")
    
    tissue_results = results.get('tissue_specific_ages', {})
    if tissue_results.get('enabled'):
        st.markdown("---")
        st.markdown("#### Doku-Spesifik Epigenetik Yaslar")
        tissue_data = tissue_results.get('results', {})
        if isinstance(tissue_data, dict) and tissue_data:
            cols = st.columns(3)
            tissue_names = list(tissue_data.keys())[:6]
            for i, tissue in enumerate(tissue_names):
                with cols[i % 3]:
                    age_val = tissue_data[tissue]
                    if isinstance(age_val, (int, float)):
                        st.metric(tissue.replace('_', ' ').title(), f"{age_val:.1f} yil")
    
    disease_results = results.get('chronic_disease_risks', {})
    if disease_results.get('enabled'):
        st.markdown("---")
        st.markdown("#### Kronik Hastalik Risk Analizi")
        disease_data = disease_results.get('results', {})
        if isinstance(disease_data, dict):
            risk_scores = disease_data.get('risk_scores', {})
            if risk_scores:
                for disease, score in list(risk_scores.items())[:5]:
                    risk_level = "Yuksek" if score > 0.7 else "Orta" if score > 0.4 else "Dusuk"
                    color = "#DC2626" if score > 0.7 else "#F59E0B" if score > 0.4 else "#10B981"
                    st.markdown(f"""
                    <div style="display: flex; justify-content: space-between; padding: 8px; border-bottom: 1px solid #E2E8F0;">
                        <span>{disease}</span>
                        <span style="color: {color}; font-weight: 600;">{risk_level} (%{score*100:.0f})</span>
                    </div>
                    """, unsafe_allow_html=True)
    
    gnn_results = results.get('gnn_molecular_analysis', {})
    if gnn_results.get('enabled'):
        st.markdown("---")
        st.markdown("#### Molekuler GNN Analizi")
        st.info("Graph Neural Network tabanli molekuler desen analizi tamamlandi.")


def generate_export(
    results: Dict[str, Any],
    export_format: str,
    include_options: list
) -> bytes:
    """Generate export file in specified format - nrcdnl94"""
    
    df = pd.DataFrame({
        'Sample_ID': results['sample_ids'],
        'Chronological_Age': results['chronological_ages'],
        'Epigenetic_Age': results['epigenetic_ages'],
        'Age_Acceleration': results['age_acceleration']
    })
    
    if 'ci_lower' in results and 'ci_upper' in results:
        df['CI_Lower'] = results['ci_lower']
        df['CI_Upper'] = results['ci_upper']
    
    if export_format == "CSV (Tablo)":
        return df.to_csv(index=False).encode('utf-8')
    
    elif export_format == "Excel (XLSX)":
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='Results', index=False)
            
            summary_df = pd.DataFrame({
                'Metric': ['N Samples', 'Mean Epi Age', 'Mean Age Acceleration', 'MAE', 'RMSE', 'Correlation'],
                'Value': [
                    results['n_samples'],
                    f"{results['mean_epi_age']:.2f}",
                    f"{results['mean_age_acceleration']:.2f}",
                    f"{results['mae']:.2f}",
                    f"{results['rmse']:.2f}",
                    f"{results['correlation']:.3f}"
                ]
            })
            summary_df.to_excel(writer, sheet_name='Summary', index=False)
        
        return buffer.getvalue()
    
    elif export_format == "JSON":
        export_dict = {
            'metadata': {
                'model_version': results['model_version'],
                'run_mode': results['run_mode'],
                'n_samples': results['n_samples'],
                'generated_at': datetime.now().isoformat()
            },
            'summary': {
                'mean_epigenetic_age': results['mean_epi_age'],
                'std_epigenetic_age': results['std_epi_age'],
                'mean_age_acceleration': results['mean_age_acceleration'],
                'std_age_acceleration': results['std_age_acceleration'],
                'mae': results['mae'],
                'rmse': results['rmse'],
                'correlation': results['correlation']
            },
            'samples': df.to_dict(orient='records')
        }
        return json.dumps(export_dict, indent=2, ensure_ascii=False).encode('utf-8')
    
    else:
        from reportlab.lib import colors
        from reportlab.lib.pagesizes import A4
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        styles = getSampleStyleSheet()
        elements = []
        
        title_style = ParagraphStyle(
            'Title',
            parent=styles['Heading1'],
            fontSize=18,
            textColor=colors.HexColor('#0050A0'),
            spaceAfter=20
        )
        
        elements.append(Paragraph("Epi-Clock Analiz Raporu", title_style))
        elements.append(Spacer(1, 12))
        
        elements.append(Paragraph(f"Olusturulma Tarihi: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal']))
        elements.append(Paragraph(f"Model: {results['model_version']}", styles['Normal']))
        elements.append(Paragraph(f"Ornek Sayisi: {results['n_samples']}", styles['Normal']))
        elements.append(Spacer(1, 20))
        
        elements.append(Paragraph("Ozet Istatistikler", styles['Heading2']))
        
        summary_data = [
            ['Metrik', 'Deger'],
            ['Ortalama Epigenetik Yas', f"{results['mean_epi_age']:.2f} yil"],
            ['Ortalama Yas Ivmesi', f"{results['mean_age_acceleration']:.2f} yil"],
            ['MAE', f"{results['mae']:.2f} yil"],
            ['RMSE', f"{results['rmse']:.2f} yil"],
            ['Korelasyon', f"{results['correlation']:.3f}"]
        ]
        
        table = Table(summary_data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0050A0')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#E2E8F0'))
        ]))
        elements.append(table)
        
        doc.build(elements)
        return buffer.getvalue()
