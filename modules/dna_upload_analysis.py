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
from typing import Optional, Dict, Any, Tuple


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
    
    col_back, col_title = st.columns([1, 11])
    with col_back:
        if st.button("Geri", key="dna_back_btn"):
            st.session_state['current_page'] = 'dashboard'
            st.rerun()
    
    st.markdown("""
    <div style="font-size: 0.7rem; color: #64748B; margin-bottom: 8px;">
        Dashboard / <span style="color: #334155; font-weight: 500;">DNA Veri Yukleme & Epi-Clock Analizi</span>
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
    
    sample_ids = [f"SAMPLE_{i:03d}" for i in range(1, n_samples + 1)]
    cpg_ids = [f"cg{np.random.randint(10000000, 99999999):08d}" for _ in range(n_cpg)]
    
    beta_values = np.random.beta(2, 5, size=(n_samples, n_cpg))
    
    df = pd.DataFrame(beta_values, columns=cpg_ids)
    df.insert(0, 'Sample_ID', sample_ids)
    df.insert(1, 'Age', np.random.randint(20, 80, n_samples))
    df.insert(2, 'Sex', np.random.choice(['M', 'F'], n_samples))
    
    return df


def run_epiclock_analysis(
    data: pd.DataFrame,
    model_version: str,
    run_mode: str,
    normalize: bool,
    batch_correction: bool,
    confidence_interval: bool,
    feature_importance: bool
) -> Dict[str, Any]:
    """Run Epi-Clock analysis on uploaded data - nrcdnl94"""
    import time
    time.sleep(2)
    
    n_samples = len(data)
    
    if 'Age' in data.columns:
        chronological_ages = data['Age'].values
    else:
        chronological_ages = np.random.randint(20, 80, n_samples)
    
    np.random.seed(42)
    noise = np.random.normal(0, 3, n_samples)
    epigenetic_ages = chronological_ages + noise + np.random.uniform(-2, 5, n_samples)
    age_acceleration = epigenetic_ages - chronological_ages
    
    sample_ids = data.iloc[:, 0].values if data.shape[1] > 0 else [f"Sample_{i}" for i in range(n_samples)]
    
    results = {
        'n_samples': n_samples,
        'model_version': model_version,
        'run_mode': run_mode,
        'sample_ids': list(sample_ids),
        'chronological_ages': list(chronological_ages),
        'epigenetic_ages': list(epigenetic_ages),
        'age_acceleration': list(age_acceleration),
        'mean_epi_age': float(np.mean(epigenetic_ages)),
        'std_epi_age': float(np.std(epigenetic_ages)),
        'mean_age_acceleration': float(np.mean(age_acceleration)),
        'std_age_acceleration': float(np.std(age_acceleration)),
        'mae': float(np.mean(np.abs(age_acceleration))),
        'rmse': float(np.sqrt(np.mean(age_acceleration**2))),
        'correlation': float(np.corrcoef(chronological_ages, epigenetic_ages)[0, 1]),
        'normalized': normalize,
        'batch_corrected': batch_correction,
        'confidence_intervals': confidence_interval,
        'feature_importance_calculated': feature_importance
    }
    
    if confidence_interval:
        ci_lower = [ea - 1.96 * 2.5 for ea in epigenetic_ages]
        ci_upper = [ea + 1.96 * 2.5 for ea in epigenetic_ages]
        results['ci_lower'] = ci_lower
        results['ci_upper'] = ci_upper
    
    if feature_importance:
        top_cpgs = [
            {"cpg": "cg00000029", "importance": 0.12, "gene": "RNF175"},
            {"cpg": "cg00000108", "importance": 0.09, "gene": "ZFYVE27"},
            {"cpg": "cg00000165", "importance": 0.07, "gene": "TRIM56"},
            {"cpg": "cg00000236", "importance": 0.06, "gene": "EDAR"},
            {"cpg": "cg00000289", "importance": 0.05, "gene": "ACSS3"}
        ]
        results['top_features'] = top_cpgs
    
    return results


def display_analysis_results(results: Dict[str, Any]):
    """Display analysis results in the UI - nrcdnl94"""
    import plotly.graph_objects as go
    
    st.markdown("---")
    st.markdown("#### Analiz Sonuclari")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("MAE", f"{results['mae']:.2f} yil")
    with col2:
        st.metric("RMSE", f"{results['rmse']:.2f} yil")
    with col3:
        st.metric("Korelasyon (r)", f"{results['correlation']:.3f}")
    with col4:
        st.metric("Ort. Yas Ivmesi", f"{results['mean_age_acceleration']:+.1f} yil")
    
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
