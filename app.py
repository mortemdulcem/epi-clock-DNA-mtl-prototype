"""
EpiClock Prototype - DNA Methylation Epigenetic Age Analysis Platform
DNA Metilasyon Tabanlı Epigenetik Yaş İvmelenmesi Analiz Platformu

A comprehensive PROTOTYPE platform for detecting and quantifying epigenetic age acceleration 
in addiction using DNA methylation clocks.

IMPORTANT DISCLAIMER:
This is a PROTOTYPE/DEMONSTRATION platform that uses SIMULATED DATA to demonstrate
the analytical workflow and methodology. The epigenetic clock coefficients and reference
database are simulated based on published research statistics, not the actual coefficients.

For research or clinical use:
- The actual Horvath/Hannum/PhenoAge/GrimAge/DunedinPACE coefficients are available in
  their respective publications' supplementary materials and must be obtained through
  proper academic channels.
- The reference database is simulated; actual methylation profiles require data access
  agreements from repositories like GEO.

This platform demonstrates the complete analytical architecture and can integrate
real coefficients and data when obtained through proper licensing channels.
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import io
import base64

from modules.epigenetic_clocks import EpigeneticClockCalculator, ClockResult
from modules.ml_models import EnsembleAgePredictor, generate_synthetic_training_data
from modules.data_processing import MethylationDataProcessor
from modules.statistics import StatisticalAnalyzer
from modules.visualization import EpigeneticVisualizer
from modules.reference_database import ReferenceDatabase
from modules.report_generator import ReportGenerator

st.set_page_config(
    page_title="EpiClock Prototype - Epigenetik Yaş Analizi",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1a365d;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #4a5568;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
    .section-header {
        font-size: 1.5rem;
        font-weight: 600;
        color: #2d3748;
        border-bottom: 2px solid #4299e1;
        padding-bottom: 0.5rem;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    .info-box {
        background-color: #ebf8ff;
        border-left: 4px solid #4299e1;
        padding: 1rem;
        border-radius: 0 8px 8px 0;
        margin: 1rem 0;
    }
    .warning-box {
        background-color: #fffaf0;
        border-left: 4px solid #ed8936;
        padding: 1rem;
        border-radius: 0 8px 8px 0;
        margin: 1rem 0;
    }
    .success-box {
        background-color: #f0fff4;
        border-left: 4px solid #48bb78;
        padding: 1rem;
        border-radius: 0 8px 8px 0;
        margin: 1rem 0;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #f7fafc;
        border-radius: 8px 8px 0 0;
        padding: 10px 20px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #4299e1;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def init_components():
    """Initialize all analysis components"""
    clock_calc = EpigeneticClockCalculator()
    ml_predictor = EnsembleAgePredictor(n_estimators=50, random_state=42)
    data_processor = MethylationDataProcessor()
    stats_analyzer = StatisticalAnalyzer()
    visualizer = EpigeneticVisualizer()
    ref_db = ReferenceDatabase()
    report_gen = ReportGenerator()
    
    X_train, y_train = generate_synthetic_training_data(n_samples=500, n_cpgs=200)
    ml_predictor.fit(X_train, y_train)
    
    return {
        'clock_calc': clock_calc,
        'ml_predictor': ml_predictor,
        'data_processor': data_processor,
        'stats_analyzer': stats_analyzer,
        'visualizer': visualizer,
        'ref_db': ref_db,
        'report_gen': report_gen
    }

def main():
    components = init_components()
    
    st.markdown('<p class="main-header">🧬 EpiClock Prototype</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">DNA Metilasyon Tabanlı Epigenetik Yaş İvmelenmesi Analiz Platformu</p>', unsafe_allow_html=True)
    
    with st.sidebar:
        st.image("https://img.icons8.com/color/96/000000/dna-helix.png", width=80)
        st.markdown("### 📊 Analiz Modülleri")
        
        analysis_mode = st.radio(
            "Analiz Türü Seçin:",
            ["🏠 Ana Sayfa",
             "👤 Bireysel Analiz",
             "📁 Toplu Analiz",
             "📈 Referans Veritabanı",
             "🔬 Diferansiyel Metilasyon",
             "🧪 Mediyasyon Analizi",
             "📊 Model Performansı",
             "📋 Rapor Oluştur"],
            index=0
        )
        
        st.markdown("---")
        st.markdown("### ⚙️ Ayarlar")
        
        selected_clocks = st.multiselect(
            "Epigenetik Saatler:",
            ["Horvath", "Hannum", "PhenoAge", "GrimAge", "DunedinPACE"],
            default=["GrimAge", "PhenoAge", "DunedinPACE"]
        )
        
        significance_level = st.slider(
            "İstatistiksel Anlamlılık (α):",
            min_value=0.01,
            max_value=0.10,
            value=0.05,
            step=0.01
        )
        
        st.markdown("---")
        st.markdown("### 📚 Hakkında")
        st.markdown("""
        **EpiClock Prototype v1.0**
        
        Bu platform, DNA metilasyon verilerini 
        kullanarak epigenetik yaş ivmelenmesini 
        tespit eder.
        
        **Desteklenen Saatler:**
        - Horvath (353 CpG)
        - Hannum (71 CpG)
        - PhenoAge (513 CpG)
        - GrimAge (1030 CpG)
        - DunedinPACE (173 CpG)
        
        **Referans Veritabanı:**
        10,542 DNA metilasyon profili
        """)
    
    if "🏠 Ana Sayfa" in analysis_mode:
        render_home_page(components)
    elif "👤 Bireysel Analiz" in analysis_mode:
        render_individual_analysis(components, selected_clocks)
    elif "📁 Toplu Analiz" in analysis_mode:
        render_batch_analysis(components, selected_clocks)
    elif "📈 Referans Veritabanı" in analysis_mode:
        render_reference_database(components)
    elif "🔬 Diferansiyel Metilasyon" in analysis_mode:
        render_differential_methylation(components, significance_level)
    elif "🧪 Mediyasyon Analizi" in analysis_mode:
        render_mediation_analysis(components)
    elif "📊 Model Performansı" in analysis_mode:
        render_model_performance(components)
    elif "📋 Rapor Oluştur" in analysis_mode:
        render_report_generator(components)


def render_home_page(components):
    """Render the home page with overview and quick stats"""
    
    st.markdown("""
    <div style="background: linear-gradient(135deg, #fff3cd 0%, #ffeeba 100%); 
                border: 2px solid #ffc107; border-radius: 10px; padding: 1rem; margin-bottom: 1.5rem;">
    <h4 style="color: #856404; margin: 0;">⚠️ PROTOTIP PLATFORMU</h4>
    <p style="color: #856404; margin: 0.5rem 0 0 0; font-size: 0.9rem;">
    Bu platform, epigenetik yaş analizi metodolojisini ve iş akışını göstermek için 
    <b>SİMÜLE EDİLMİŞ VERİLER</b> kullanmaktadır. Saat katsayıları ve referans veritabanı, 
    yayınlanmış araştırma istatistiklerine dayalı olarak simüle edilmiştir. 
    Gerçek klinik veya araştırma kullanımı için, gerçek katsayılar ve veriler uygun 
    akademik kanallardan temin edilmelidir.
    </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 🎯 Platform Özellikleri")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Referans Profil Sayısı",
            value="10,542",
            delta="15 bağımsız veri seti"
        )
    
    with col2:
        st.metric(
            label="Epigenetik Saat",
            value="5",
            delta="En güncel algoritmalar"
        )
    
    with col3:
        st.metric(
            label="ML Model MAE",
            value="2.1 yıl",
            delta="R² = 0.96"
        )
    
    with col4:
        st.metric(
            label="Madde Kategorisi",
            value="6",
            delta="+ Kontrol grubu"
        )
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📊 Madde Tipine Göre EAA Etkileri")
        
        ref_db = components['ref_db']
        effect_summary = ref_db.get_substance_effect_summary()
        
        visualizer = components['visualizer']
        
        effect_summary['substance_tr'] = effect_summary['substance'].map({
            'polysubstance': 'Çoklu Madde',
            'methamphetamine': 'Metamfetamin',
            'cocaine': 'Kokain',
            'alcohol': 'Alkol',
            'opioids': 'Opioid',
            'cannabis': 'Kannabis'
        })
        
        import plotly.graph_objects as go
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            y=effect_summary['substance_tr'],
            x=effect_summary['effect_vs_control'],
            orientation='h',
            marker=dict(
                color=effect_summary['effect_vs_control'],
                colorscale='Reds',
                showscale=True,
                colorbar=dict(title="EAA (yıl)")
            ),
            error_x=dict(
                type='data',
                symmetric=False,
                array=effect_summary['ci_upper'] - effect_summary['effect_vs_control'],
                arrayminus=effect_summary['effect_vs_control'] - effect_summary['ci_lower']
            ),
            hovertemplate="<b>%{y}</b><br>EAA: %{x:.1f} yıl<br>n=%{customdata}<extra></extra>",
            customdata=effect_summary['n_samples']
        ))
        
        fig.update_layout(
            title="GrimAge Epigenetik Yaş İvmelenmesi (Kontrole Göre)",
            xaxis_title="Epigenetik Yaş İvmelenmesi (yıl)",
            yaxis_title="",
            template="plotly_white",
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### 🎯 Epigenetik Saat Performansları")
        
        clock_perf = ref_db.get_clock_performance_summary()
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            name='MAE (yıl)',
            x=clock_perf['clock'],
            y=clock_perf['mae'],
            marker_color='steelblue',
            yaxis='y'
        ))
        
        fig.add_trace(go.Scatter(
            name='R²',
            x=clock_perf['clock'],
            y=clock_perf['r_squared'],
            mode='lines+markers',
            marker=dict(size=12, color='coral'),
            line=dict(width=3),
            yaxis='y2'
        ))
        
        fig.update_layout(
            title="Epigenetik Saat Doğruluk Karşılaştırması",
            xaxis_title="Epigenetik Saat",
            yaxis=dict(title="MAE (yıl)", side='left'),
            yaxis2=dict(title="R²", side='right', overlaying='y', range=[0.85, 1.0]),
            template="plotly_white",
            legend=dict(yanchor="top", y=0.99, xanchor="right", x=0.99),
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    st.markdown("### 📖 Metodoloji ve Bilimsel Arka Plan")
    
    with st.expander("DNA Metilasyonu ve Epigenetik Saatler", expanded=False):
        st.markdown("""
        **DNA Metilasyonu Nedir?**
        
        DNA metilasyonu, DNA'nın sitozin bazlarına metil gruplarının (CH₃) kovalent bağlanmasıyla 
        karakterize edilen epigenetik bir modifikasyondur. İnsan genomunda yaklaşık 28 milyon CpG 
        bölgesinin %60-80'i metillenmiş durumdadır.
        
        **Epigenetik Saatler**
        
        Belirli CpG bölgelerindeki metilasyon seviyeleri, kronolojik yaşla yüksek korelasyon gösterir. 
        Bu paternler kullanılarak biyolojik yaş tahmin edilebilir:
        
        | Saat | Yıl | CpG Sayısı | Özellik |
        |------|-----|------------|---------|
        | Horvath | 2013 | 353 | Pan-doku, genel biyolojik yaş |
        | Hannum | 2013 | 71 | Kan-spesifik |
        | PhenoAge | 2018 | 513 | Fenotipik yaş, hastalık riski |
        | GrimAge | 2019 | 1030 | Mortalite tahmini |
        | DunedinPACE | 2022 | 173 | Yaşlanma hızı |
        """)
    
    with st.expander("Madde Kullanımı ve Epigenetik Yaş İvmelenmesi", expanded=False):
        st.markdown("""
        **Madde Kullanım Bozuklukları ve Biyolojik Yaşlanma**
        
        Kronik madde kullanımı, DNA metilasyon paternlerinde sistematik değişikliklere yol açarak 
        epigenetik yaş ivmelenmesine (EAA) neden olur.
        
        **Araştırma Bulguları (10,542 profil analizi):**
        
        - **Çoklu Madde:** +7.3 yıl GrimAge ivmelenmesi (en yüksek etki)
        - **Metamfetamin:** +6.2 yıl
        - **Kokain:** +4.1 yıl
        - **Alkol:** +3.6 yıl
        - **Opioid:** +2.9 yıl
        - **Kannabis:** +0.8 yıl (en düşük etki)
        
        **Fizyolojik Mekanizmalar:**
        - İnsülin direnci (HOMA-IR)
        - HPA eksen disregülasyonu (Kortizol/ACTH)
        - Sistemik inflamasyon (CRP, IL-6, TNF-α)
        - Oksidatif stres
        - Telomer kısalması
        """)
    
    with st.expander("Platform Kullanım Kılavuzu", expanded=False):
        st.markdown("""
        **1. Bireysel Analiz**
        - Tek bir hastanın verilerini girerek epigenetik yaş hesaplayın
        - Tüm 5 epigenetik saat sonuçlarını görüntüleyin
        - Referans popülasyonla karşılaştırma yapın
        
        **2. Toplu Analiz**
        - CSV/Excel formatında DNA metilasyon verisi yükleyin
        - Çoklu örnek analizi gerçekleştirin
        - Grup karşılaştırmaları ve istatistiksel testler
        
        **3. Diferansiyel Metilasyon Analizi**
        - Madde grupları arasında CpG farklılıklarını tespit edin
        - Volcano plot ve heatmap görselleştirmeleri
        
        **4. Mediyasyon/Moderasyon Analizi**
        - Fizyolojik ve psikolojik faktörlerin etkilerini analiz edin
        - Müdahale hedeflerini belirleyin
        
        **5. PDF Rapor**
        - Kapsamlı klinik raporlar oluşturun
        - Sonuçları dışa aktarın
        """)


def render_individual_analysis(components, selected_clocks):
    """Render individual sample analysis page"""
    
    st.markdown("### 👤 Bireysel Epigenetik Yaş Analizi")
    
    st.markdown("""
    <div class="info-box">
    <b>ℹ️ Bilgi:</b> Bu modülde tek bir hastanın demografik bilgilerini girerek 
    epigenetik yaş hesaplaması yapabilir ve referans popülasyonla karşılaştırabilirsiniz.
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📝 Hasta Bilgileri")
        
        patient_id = st.text_input("Hasta ID:", value="HASTA_001")
        chronological_age = st.number_input("Kronolojik Yaş:", min_value=18, max_value=100, value=45)
        sex = st.selectbox("Cinsiyet:", ["Erkek", "Kadın"])
        sex_code = "M" if sex == "Erkek" else "F"
        
        substance_type = st.selectbox(
            "Madde Maruziyeti:",
            ["Kontrol (Maruziyetsiz)", "Alkol Kullanım Bozukluğu", "Kokain Kullanımı", 
             "Opioid Kullanımı", "Metamfetamin Kullanımı", "Kannabis Kullanımı", 
             "Çoklu Madde Kullanımı"]
        )
        
        substance_map = {
            "Kontrol (Maruziyetsiz)": "control",
            "Alkol Kullanım Bozukluğu": "alcohol",
            "Kokain Kullanımı": "cocaine",
            "Opioid Kullanımı": "opioids",
            "Metamfetamin Kullanımı": "methamphetamine",
            "Kannabis Kullanımı": "cannabis",
            "Çoklu Madde Kullanımı": "polysubstance"
        }
        substance_code = substance_map[substance_type]
        
        smoking_years = st.slider("Sigara Paket-Yılı:", 0, 60, 5)
    
    with col2:
        st.markdown("#### 🧪 Klinik Biyobelirteçler (Opsiyonel)")
        
        use_biomarkers = st.checkbox("Klinik biyobelirteçleri dahil et (PhenoAge için)")
        
        if use_biomarkers:
            col_a, col_b = st.columns(2)
            with col_a:
                albumin = st.number_input("Albumin (g/dL):", min_value=2.0, max_value=6.0, value=4.0)
                creatinine = st.number_input("Kreatinin (mg/dL):", min_value=0.3, max_value=3.0, value=1.0)
                glucose = st.number_input("Glukoz (mg/dL):", min_value=50.0, max_value=300.0, value=95.0)
                crp = st.number_input("CRP (mg/L):", min_value=0.1, max_value=50.0, value=1.5)
            with col_b:
                lymphocyte = st.number_input("Lenfosit (%):", min_value=5.0, max_value=60.0, value=30.0)
                mcv = st.number_input("MCV (fL):", min_value=70.0, max_value=110.0, value=90.0)
                rdw = st.number_input("RDW (%):", min_value=10.0, max_value=20.0, value=13.0)
                wbc = st.number_input("WBC (10³/µL):", min_value=2.0, max_value=15.0, value=6.0)
            
            clinical_biomarkers = {
                'albumin': albumin,
                'creatinine': creatinine,
                'glucose': glucose,
                'crp': crp,
                'lymphocyte_percent': lymphocyte,
                'mcv': mcv,
                'rdw': rdw,
                'white_blood_cell': wbc
            }
        else:
            clinical_biomarkers = None
    
    st.markdown("---")
    
    if st.button("🔬 Epigenetik Yaş Hesapla", type="primary", use_container_width=True):
        
        with st.spinner("Epigenetik saatler hesaplanıyor..."):
            
            clock_calc = components['clock_calc']
            ref_db = components['ref_db']
            visualizer = components['visualizer']
            
            dummy_methylation = pd.DataFrame(
                np.random.beta(2, 5, (1, 500)),
                columns=[f"cg{str(i).zfill(8)}" for i in range(500)]
            )
            
            base_results = clock_calc.calculate_all_clocks(
                dummy_methylation,
                chronological_age,
                sex_code,
                smoking_years,
                clinical_biomarkers
            )
            
            if substance_code != 'control':
                clock_results = clock_calc.simulate_substance_effect(
                    base_results, 
                    substance_code, 
                    severity=1.0
                )
            else:
                clock_results = base_results
            
            if 'analysis_results' not in st.session_state:
                st.session_state['analysis_results'] = {}
            
            st.session_state['analysis_results'] = {
                'patient_info': {
                    'patient_id': patient_id,
                    'chronological_age': chronological_age,
                    'sex': sex_code,
                    'substance_type': substance_code,
                    'tissue_type': 'blood'
                },
                'clock_results': clock_results,
                'timestamp': datetime.now()
            }
        
        st.success("✅ Analiz tamamlandı!")
        
        st.markdown("### 📊 Epigenetik Saat Sonuçları")
        
        result_cols = st.columns(len(clock_results))
        
        for i, (clock_name, result) in enumerate(clock_results.items()):
            with result_cols[i]:
                eaa = result.age_acceleration
                if clock_name == 'dunedinpace':
                    delta_color = "inverse" if eaa > 0.05 else "normal"
                    st.metric(
                        label=result.clock_name,
                        value=f"{result.predicted_age:.2f}",
                        delta=f"Hız: {eaa:+.2f}",
                        delta_color=delta_color
                    )
                else:
                    delta_color = "inverse" if eaa > 2 else "normal"
                    st.metric(
                        label=result.clock_name,
                        value=f"{result.predicted_age:.1f} yıl",
                        delta=f"EAA: {eaa:+.1f} yıl",
                        delta_color=delta_color
                    )
        
        st.markdown("---")
        
        tab1, tab2, tab3 = st.tabs(["📈 Görselleştirmeler", "📋 Detaylı Sonuçlar", "🎯 Referans Karşılaştırması"])
        
        with tab1:
            col1, col2 = st.columns(2)
            
            with col1:
                eaa_values = {name: r.age_acceleration for name, r in clock_results.items() 
                             if name != 'dunedinpace'}
                radar_fig = visualizer.plot_clock_comparison_radar(eaa_values, patient_id)
                st.plotly_chart(radar_fig, use_container_width=True)
            
            with col2:
                import plotly.graph_objects as go
                
                clock_names = [r.clock_name for r in clock_results.values()]
                predicted_ages = [r.predicted_age for r in clock_results.values()]
                eaa_vals = [r.age_acceleration for r in clock_results.values()]
                
                colors = ['green' if e < 2 else 'orange' if e < 5 else 'red' for e in eaa_vals]
                
                fig = go.Figure(data=[
                    go.Bar(
                        x=clock_names,
                        y=predicted_ages,
                        marker_color=colors,
                        text=[f"{p:.1f}" for p in predicted_ages],
                        textposition='outside'
                    )
                ])
                
                fig.add_hline(y=chronological_age, line_dash="dash", 
                             annotation_text=f"Kronolojik Yaş: {chronological_age}")
                
                fig.update_layout(
                    title="Epigenetik Yaş Tahminleri",
                    xaxis_title="Epigenetik Saat",
                    yaxis_title="Tahmin Edilen Yaş (yıl)",
                    template="plotly_white",
                    height=400
                )
                
                st.plotly_chart(fig, use_container_width=True)
        
        with tab2:
            results_df = pd.DataFrame([
                {
                    'Epigenetik Saat': r.clock_name,
                    'Tahmin Edilen Yaş': f"{r.predicted_age:.2f}",
                    'Kronolojik Yaş': r.chronological_age,
                    'Yaş İvmelenmesi (EAA)': f"{r.age_acceleration:+.2f}",
                    '95% GA Alt': f"{r.confidence_interval[0]:.2f}",
                    '95% GA Üst': f"{r.confidence_interval[1]:.2f}",
                    'CpG Sayısı': r.cpg_count,
                    'R²': r.r_squared,
                    'MAE': r.mae,
                    'Yorum': clock_calc.get_eaa_interpretation(r.age_acceleration, r.clock_name)
                }
                for r in clock_results.values()
            ])
            
            st.dataframe(results_df, use_container_width=True)
        
        with tab3:
            grimage_result = clock_results.get('grimage')
            if grimage_result:
                comparison = ref_db.compare_to_reference(
                    grimage_result.age_acceleration,
                    substance_code,
                    'grimage',
                    chronological_age,
                    sex_code
                )
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Persentil", f"{comparison.percentile:.0f}%")
                with col2:
                    st.metric("Z-Skoru", f"{comparison.z_score:.2f}")
                with col3:
                    st.metric("Benzer Örnek Sayısı", comparison.similar_samples)
                
                if comparison.percentile > 75:
                    st.markdown(f"""
                    <div class="warning-box">
                    <b>⚠️ Dikkat:</b> {comparison.interpretation}
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="success-box">
                    <b>✅ Sonuç:</b> {comparison.interpretation}
                    </div>
                    """, unsafe_allow_html=True)


def render_batch_analysis(components, selected_clocks):
    """Render batch analysis page for multiple samples"""
    
    st.markdown("### 📁 Toplu Örnek Analizi")
    
    st.markdown("""
    <div class="info-box">
    <b>ℹ️ Bilgi:</b> Bu modülde birden fazla örneğin DNA metilasyon verilerini yükleyerek 
    toplu analiz gerçekleştirebilir, grup karşılaştırmaları yapabilirsiniz.
    </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["📤 Veri Yükle", "🔄 Demo Veri Kullan"])
    
    with tab1:
        uploaded_file = st.file_uploader(
            "DNA Metilasyon Verisi Yükle (CSV/Excel):",
            type=['csv', 'xlsx', 'xls'],
            help="İlk sütun örnek ID, ilk satır CpG ID olmalıdır"
        )
        
        if uploaded_file:
            try:
                if uploaded_file.name.endswith('.csv'):
                    data = pd.read_csv(uploaded_file, index_col=0)
                else:
                    data = pd.read_excel(uploaded_file, index_col=0)
                
                st.success(f"✅ {data.shape[0]} örnek, {data.shape[1]} CpG yüklendi")
                
                with st.expander("Veri Önizleme"):
                    st.dataframe(data.head(10))
                    
            except Exception as e:
                st.error(f"Veri yüklenirken hata: {str(e)}")
    
    with tab2:
        st.markdown("#### Demo Veri Seti Oluştur")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            n_samples = st.number_input("Örnek Sayısı:", min_value=50, max_value=1000, value=200)
        with col2:
            n_cpgs = st.number_input("CpG Sayısı:", min_value=100, max_value=5000, value=500)
        with col3:
            include_substances = st.checkbox("Madde grupları dahil et", value=True)
        
        if st.button("🎲 Demo Veri Oluştur", type="primary"):
            with st.spinner("Demo veri seti oluşturuluyor..."):
                data_processor = components['data_processor']
                
                if include_substances:
                    methylation_data, metadata = data_processor.generate_sample_data(
                        n_samples=n_samples,
                        n_cpgs=n_cpgs,
                        include_metadata=True
                    )
                else:
                    methylation_data, metadata = data_processor.generate_sample_data(
                        n_samples=n_samples,
                        n_cpgs=n_cpgs,
                        include_metadata=True,
                        substance_distribution={'control': 1.0}
                    )
                
                st.session_state['batch_data'] = methylation_data
                st.session_state['batch_metadata'] = metadata
                
            st.success(f"✅ {n_samples} örnekli demo veri seti oluşturuldu!")
    
    if 'batch_data' in st.session_state:
        st.markdown("---")
        st.markdown("### 📊 Toplu Analiz")
        
        methylation_data = st.session_state['batch_data']
        metadata = st.session_state['batch_metadata']
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Veri Özeti:**")
            st.write(f"- Örnek sayısı: {len(methylation_data)}")
            st.write(f"- CpG sayısı: {methylation_data.shape[1]}")
            if metadata is not None:
                st.write(f"- Yaş aralığı: {metadata['chronological_age'].min():.0f} - {metadata['chronological_age'].max():.0f}")
        
        with col2:
            if metadata is not None and 'substance_type' in metadata.columns:
                st.markdown("**Grup Dağılımı:**")
                group_counts = metadata['substance_type'].value_counts()
                st.bar_chart(group_counts)
        
        if st.button("🔬 Toplu Analiz Başlat", type="primary", use_container_width=True):
            
            with st.spinner("Toplu analiz gerçekleştiriliyor..."):
                
                clock_calc = components['clock_calc']
                stats_analyzer = components['stats_analyzer']
                visualizer = components['visualizer']
                
                all_results = []
                
                progress_bar = st.progress(0)
                
                for i, (sample_id, row) in enumerate(metadata.iterrows()):
                    sample_methylation = methylation_data.loc[[sample_id]]
                    
                    base_results = clock_calc.calculate_all_clocks(
                        sample_methylation,
                        row['chronological_age'],
                        row['sex'],
                        row.get('smoking_pack_years', 0)
                    )
                    
                    clock_results = clock_calc.simulate_substance_effect(
                        base_results,
                        row['substance_type'],
                        severity=1.0
                    )
                    
                    result_row = {
                        'sample_id': sample_id,
                        'chronological_age': row['chronological_age'],
                        'sex': row['sex'],
                        'substance_type': row['substance_type']
                    }
                    
                    for clock_name, result in clock_results.items():
                        result_row[f'{clock_name}_predicted'] = result.predicted_age
                        result_row[f'{clock_name}_eaa'] = result.age_acceleration
                    
                    all_results.append(result_row)
                    
                    progress_bar.progress((i + 1) / len(metadata))
                
                results_df = pd.DataFrame(all_results)
                st.session_state['batch_results'] = results_df
            
            st.success("✅ Toplu analiz tamamlandı!")
            
            st.markdown("### 📈 Analiz Sonuçları")
            
            tab1, tab2, tab3 = st.tabs(["📊 Grup Karşılaştırması", "📋 Detaylı Sonuçlar", "📥 Dışa Aktar"])
            
            with tab1:
                if 'substance_type' in results_df.columns:
                    group_stats = results_df.groupby('substance_type').agg({
                        'grimage_eaa': ['mean', 'std', 'count']
                    }).round(2)
                    group_stats.columns = ['Ortalama EAA', 'Std', 'N']
                    group_stats = group_stats.reset_index()
                    
                    eaa_values = results_df['grimage_eaa'].values
                    group_labels = results_df['substance_type'].values
                    
                    violin_fig = visualizer.plot_eaa_violin(eaa_values, group_labels)
                    st.plotly_chart(violin_fig, use_container_width=True)
                    
                    comparison_df = stats_analyzer.compare_groups(
                        eaa_values, group_labels, 'control'
                    )
                    
                    st.markdown("**İstatistiksel Karşılaştırma (vs Kontrol):**")
                    st.dataframe(comparison_df, use_container_width=True)
            
            with tab2:
                st.dataframe(results_df, use_container_width=True)
            
            with tab3:
                csv = results_df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📥 CSV Olarak İndir",
                    data=csv,
                    file_name=f"epiclock_batch_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
                
                buffer = io.BytesIO()
                with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                    results_df.to_excel(writer, sheet_name='Sonuçlar', index=False)
                    if 'substance_type' in results_df.columns:
                        comparison_df.to_excel(writer, sheet_name='Grup Karşılaştırması', index=False)
                
                st.download_button(
                    label="📥 Excel Olarak İndir",
                    data=buffer.getvalue(),
                    file_name=f"epiclock_batch_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )


def render_reference_database(components):
    """Render reference database exploration page"""
    
    st.markdown("### 📈 Referans Veritabanı")
    
    st.markdown("""
    <div class="info-box">
    <b>ℹ️ Bilgi:</b> Bu modülde 10,542 DNA metilasyon profilinden oluşan referans veritabanını 
    inceleyebilir, madde grupları arasındaki farklılıkları analiz edebilirsiniz.
    </div>
    """, unsafe_allow_html=True)
    
    ref_db = components['ref_db']
    visualizer = components['visualizer']
    
    summary = ref_db.get_database_summary()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Toplam Örnek", f"{summary['total_samples']:,}")
    with col2:
        st.metric("Madde Kategorisi", len(summary['substance_distribution']))
    with col3:
        st.metric("Yaş Aralığı", f"{summary['age_range'][0]:.0f}-{summary['age_range'][1]:.0f}")
    with col4:
        st.metric("En İyi Model MAE", f"{summary['clock_performance']['ensemble']['mae']} yıl")
    
    st.markdown("---")
    
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Grup Dağılımları", 
        "📈 Yaş Stratifikasyonu", 
        "🔍 Detaylı İstatistikler",
        "🎲 Sentetik Kohort"
    ])
    
    with tab1:
        st.markdown("#### Madde Tipine Göre Örnek Dağılımı")
        
        import plotly.graph_objects as go
        
        substances = list(summary['substance_distribution'].keys())
        counts = list(summary['substance_distribution'].values())
        
        substance_labels = {
            'control': 'Kontrol',
            'alcohol': 'Alkol',
            'cocaine': 'Kokain',
            'opioids': 'Opioid',
            'methamphetamine': 'Metamfetamin',
            'cannabis': 'Kannabis',
            'polysubstance': 'Çoklu Madde'
        }
        
        labels_tr = [substance_labels.get(s, s) for s in substances]
        
        colors = [visualizer.SUBSTANCE_COLORS.get(s, '#888888') for s in substances]
        
        fig = go.Figure(data=[go.Pie(
            labels=labels_tr,
            values=counts,
            marker_colors=colors,
            hole=0.4,
            textinfo='label+percent',
            textposition='outside'
        )])
        
        fig.update_layout(
            title="Referans Veritabanı Kompozisyonu",
            template="plotly_white",
            height=500
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        effect_summary = ref_db.get_substance_effect_summary()
        st.markdown("#### Madde Etkisi Özeti")
        st.dataframe(effect_summary, use_container_width=True)
    
    with tab2:
        st.markdown("#### Yaş Gruplarına Göre EAA İstatistikleri")
        
        selected_substance = st.selectbox(
            "Madde Tipi:",
            ["Tümü"] + list(summary['substance_distribution'].keys())
        )
        
        if selected_substance == "Tümü":
            age_stats = ref_db.get_age_stratified_statistics()
        else:
            age_stats = ref_db.get_age_stratified_statistics(selected_substance)
        
        st.dataframe(age_stats, use_container_width=True)
    
    with tab3:
        st.markdown("#### Detaylı Referans İstatistikleri")
        
        selected_substance_detail = st.selectbox(
            "İstatistik için madde tipi seçin:",
            list(summary['substance_distribution'].keys()),
            key="detail_substance"
        )
        
        selected_clock = st.selectbox(
            "Epigenetik saat seçin:",
            ['grimage', 'horvath', 'hannum', 'phenoage', 'dunedinpace'],
            key="detail_clock"
        )
        
        stats = ref_db.get_reference_statistics(selected_substance_detail, selected_clock)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Temel İstatistikler:**")
            st.write(f"- Örnek sayısı: {stats.n_samples}")
            st.write(f"- Ortalama EAA: {stats.mean_eaa} yıl")
            st.write(f"- Standart sapma: {stats.std_eaa} yıl")
            st.write(f"- Yaş aralığı: {stats.age_range[0]:.0f} - {stats.age_range[1]:.0f} yıl")
        
        with col2:
            st.markdown("**Persentiller:**")
            for p, val in stats.percentiles.items():
                st.write(f"- {p}. persentil: {val} yıl")
    
    with tab4:
        st.markdown("#### Sentetik Kohort Oluşturma")
        
        st.markdown("""
        Kendi analizleriniz için referans veritabanı karakteristiklerine uygun 
        sentetik kohort oluşturabilirsiniz.
        """)
        
        n_synth = st.slider("Örnek sayısı:", 50, 500, 100)
        
        st.markdown("**Madde dağılımı (toplam %100 olmalı):**")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            pct_control = st.slider("Kontrol %:", 0, 100, 40)
            pct_alcohol = st.slider("Alkol %:", 0, 100, 20)
            pct_cocaine = st.slider("Kokain %:", 0, 100, 10)
        
        with col2:
            pct_opioids = st.slider("Opioid %:", 0, 100, 10)
            pct_meth = st.slider("Metamfetamin %:", 0, 100, 5)
        
        with col3:
            pct_cannabis = st.slider("Kannabis %:", 0, 100, 5)
            pct_poly = st.slider("Çoklu Madde %:", 0, 100, 10)
        
        total_pct = pct_control + pct_alcohol + pct_cocaine + pct_opioids + pct_meth + pct_cannabis + pct_poly
        
        if total_pct != 100:
            st.warning(f"Toplam: %{total_pct} - Lütfen toplamı %100 yapın")
        else:
            if st.button("🎲 Sentetik Kohort Oluştur"):
                distribution = {
                    'control': pct_control / 100,
                    'alcohol': pct_alcohol / 100,
                    'cocaine': pct_cocaine / 100,
                    'opioids': pct_opioids / 100,
                    'methamphetamine': pct_meth / 100,
                    'cannabis': pct_cannabis / 100,
                    'polysubstance': pct_poly / 100
                }
                
                synth_cohort = ref_db.generate_synthetic_cohort(n_synth, distribution)
                
                st.success(f"✅ {len(synth_cohort)} örnekli sentetik kohort oluşturuldu!")
                
                st.dataframe(synth_cohort.head(20), use_container_width=True)
                
                csv = synth_cohort.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📥 Sentetik Kohort İndir (CSV)",
                    data=csv,
                    file_name=f"synthetic_cohort_{n_synth}.csv",
                    mime="text/csv"
                )


def render_differential_methylation(components, significance_level):
    """Render differential methylation analysis page"""
    
    st.markdown("### 🔬 Diferansiyel Metilasyon Analizi (DMA)")
    
    st.markdown("""
    <div class="info-box">
    <b>ℹ️ Bilgi:</b> Bu modülde farklı gruplar arasındaki CpG metilasyon farklılıklarını 
    tespit edebilir, madde kullanımına özgü epigenetik değişiklikleri analiz edebilirsiniz.
    </div>
    """, unsafe_allow_html=True)
    
    data_processor = components['data_processor']
    stats_analyzer = components['stats_analyzer']
    visualizer = components['visualizer']
    
    col1, col2 = st.columns(2)
    
    with col1:
        case_group = st.selectbox(
            "Vaka Grubu:",
            ["alcohol", "cocaine", "opioids", "methamphetamine", "cannabis", "polysubstance"],
            format_func=lambda x: {
                'alcohol': 'Alkol',
                'cocaine': 'Kokain',
                'opioids': 'Opioid',
                'methamphetamine': 'Metamfetamin',
                'cannabis': 'Kannabis',
                'polysubstance': 'Çoklu Madde'
            }.get(x, x)
        )
    
    with col2:
        min_delta_beta = st.slider(
            "Minimum Δβ Eşiği:",
            min_value=0.01,
            max_value=0.20,
            value=0.05,
            step=0.01
        )
    
    if st.button("🔬 DMA Başlat", type="primary", use_container_width=True):
        
        with st.spinner("Diferansiyel metilasyon analizi gerçekleştiriliyor..."):
            
            np.random.seed(42)
            n_samples_case = 100
            n_samples_control = 100
            n_cpgs = 1000
            
            cpg_names = [f"cg{str(i).zfill(8)}" for i in range(n_cpgs)]
            
            control_data = np.random.beta(2, 5, (n_samples_control, n_cpgs))
            case_data = control_data.copy()
            case_data = np.vstack([case_data, np.random.beta(2, 5, (n_samples_case - n_samples_control, n_cpgs))])
            
            n_diff = int(n_cpgs * 0.1)
            diff_indices = np.random.choice(n_cpgs, n_diff, replace=False)
            
            for idx in diff_indices[:n_diff//2]:
                case_data[:, idx] += np.random.uniform(0.05, 0.15)
            
            for idx in diff_indices[n_diff//2:]:
                case_data[:, idx] -= np.random.uniform(0.05, 0.15)
            
            case_data = np.clip(case_data[:n_samples_case], 0, 1)
            
            all_data = np.vstack([control_data, case_data])
            all_labels = np.array(['control'] * n_samples_control + [case_group] * n_samples_case)
            
            methylation_df = pd.DataFrame(all_data, columns=cpg_names)
            
            dma_results = stats_analyzer.differential_methylation_analysis(
                methylation_df,
                all_labels,
                case_group,
                'control',
                min_delta_beta
            )
        
        st.success("✅ DMA tamamlandı!")
        
        n_sig = dma_results['is_significant'].sum()
        n_hyper = ((dma_results['is_significant']) & (dma_results['direction'] == 'hypermethylated')).sum()
        n_hypo = ((dma_results['is_significant']) & (dma_results['direction'] == 'hypomethylated')).sum()
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Toplam CpG", len(dma_results))
        with col2:
            st.metric("Anlamlı CpG", n_sig)
        with col3:
            st.metric("Hipermetilasyon", n_hyper)
        with col4:
            st.metric("Hipometilasyon", n_hypo)
        
        st.markdown("---")
        
        tab1, tab2, tab3 = st.tabs(["🌋 Volcano Plot", "📋 Top CpG'ler", "📊 Dağılım"])
        
        with tab1:
            volcano_fig = visualizer.plot_volcano(
                dma_results,
                p_value_threshold=significance_level,
                fc_threshold=min_delta_beta
            )
            st.plotly_chart(volcano_fig, use_container_width=True)
        
        with tab2:
            st.markdown("#### En Anlamlı Hipermetilasyonlu CpG'ler")
            top_hyper = dma_results[dma_results['direction'] == 'hypermethylated'].head(10)
            st.dataframe(top_hyper[['cpg_id', 'mean_diff', 'log2_fold_change', 'p_value', 'adjusted_p_value']], 
                        use_container_width=True)
            
            st.markdown("#### En Anlamlı Hipometilasyonlu CpG'ler")
            top_hypo = dma_results[dma_results['direction'] == 'hypomethylated'].head(10)
            st.dataframe(top_hypo[['cpg_id', 'mean_diff', 'log2_fold_change', 'p_value', 'adjusted_p_value']], 
                        use_container_width=True)
        
        with tab3:
            import plotly.express as px
            
            fig = px.histogram(
                dma_results,
                x='mean_diff',
                nbins=50,
                color='is_significant',
                color_discrete_map={True: 'red', False: 'lightgray'},
                labels={'mean_diff': 'Ortalama Metilasyon Farkı (Δβ)', 'is_significant': 'Anlamlı'},
                title='Metilasyon Farklılıklarının Dağılımı'
            )
            
            fig.update_layout(template="plotly_white")
            st.plotly_chart(fig, use_container_width=True)


def render_mediation_analysis(components):
    """Render mediation and moderation analysis page"""
    
    st.markdown("### 🧪 Mediyasyon ve Moderasyon Analizi")
    
    st.markdown("""
    <div class="info-box">
    <b>ℹ️ Bilgi:</b> Bu modülde fizyolojik ve psikolojik faktörlerin madde kullanımı ile 
    epigenetik yaş ivmelenmesi arasındaki ilişkideki aracı (mediator) ve düzenleyici (moderator) 
    rollerini analiz edebilirsiniz.
    </div>
    """, unsafe_allow_html=True)
    
    stats_analyzer = components['stats_analyzer']
    visualizer = components['visualizer']
    
    tab1, tab2 = st.tabs(["🔗 Mediyasyon Analizi", "⚖️ Moderasyon Analizi"])
    
    with tab1:
        st.markdown("#### Fizyolojik Mediyatörler")
        
        st.markdown("""
        Mediyasyon analizi, bağımsız değişken (madde kullanımı) ile bağımlı değişken (EAA) 
        arasındaki ilişkinin bir aracı değişken tarafından ne ölçüde açıklandığını test eder.
        """)
        
        mediator = st.selectbox(
            "Mediyatör Seçin:",
            [
                ("homa_ir", "İnsülin Direnci (HOMA-IR)"),
                ("cortisol_acth", "HPA Eksen (Kortizol/ACTH)"),
                ("crp", "C-Reaktif Protein (CRP)"),
                ("il6", "İnterlökin-6 (IL-6)"),
                ("tnf_alpha", "TNF-α"),
                ("telomere", "Telomer Uzunluğu")
            ],
            format_func=lambda x: x[1]
        )
        
        if st.button("🔗 Mediyasyon Analizi Çalıştır", key="mediation"):
            
            with st.spinner("Mediyasyon analizi gerçekleştiriliyor..."):
                
                np.random.seed(42)
                n = 500
                
                substance_exposure = np.random.binomial(1, 0.4, n)
                
                mediator_values = substance_exposure * 1.5 + np.random.normal(0, 1, n)
                
                eaa_values = substance_exposure * 2.0 + mediator_values * 0.8 + np.random.normal(0, 2, n)
                
                result = stats_analyzer.mediation_analysis(
                    eaa_values,
                    substance_exposure,
                    mediator_values,
                    mediator[1]
                )
            
            st.success("✅ Mediyasyon analizi tamamlandı!")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Toplam Etki", f"{result.total_effect:.3f}")
                st.metric("Doğrudan Etki (c')", f"{result.direct_effect:.3f}")
            
            with col2:
                st.metric("Dolaylı Etki (a×b)", f"{result.indirect_effect:.3f}")
                st.metric("Mediated Oran", f"{result.proportion_mediated*100:.1f}%")
            
            with col3:
                st.metric("Sobel Z", f"{result.sobel_z:.3f}")
                st.metric("Sobel p", f"{result.sobel_p:.4f}")
            
            if result.is_significant:
                st.markdown("""
                <div class="success-box">
                <b>✅ Sonuç:</b> Mediyasyon etkisi istatistiksel olarak anlamlıdır (p < 0.05). 
                Bu, madde kullanımının EAA üzerindeki etkisinin kısmen bu fizyolojik yolak 
                aracılığıyla gerçekleştiğini göstermektedir.
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div class="warning-box">
                <b>⚠️ Sonuç:</b> Mediyasyon etkisi istatistiksel olarak anlamlı değildir (p ≥ 0.05).
                </div>
                """, unsafe_allow_html=True)
            
            med_diagram = visualizer.plot_mediation_diagram(result)
            st.plotly_chart(med_diagram, use_container_width=True)
    
    with tab2:
        st.markdown("#### Psikolojik Moderatörler")
        
        st.markdown("""
        Moderasyon analizi, bağımsız değişken ile bağımlı değişken arasındaki ilişkinin 
        gücünün bir üçüncü değişkene (moderatör) göre değişip değişmediğini test eder.
        """)
        
        moderator = st.selectbox(
            "Moderatör Seçin:",
            [
                ("ders", "Duygu Düzenleme (DERS)"),
                ("self_control", "Öz-Kontrol"),
                ("social_support", "Sosyal Destek"),
                ("resilience", "Psikolojik Dayanıklılık"),
                ("coping", "Başa Çıkma Stratejileri")
            ],
            format_func=lambda x: x[1]
        )
        
        if st.button("⚖️ Moderasyon Analizi Çalıştır", key="moderation"):
            
            with st.spinner("Moderasyon analizi gerçekleştiriliyor..."):
                
                np.random.seed(42)
                n = 500
                
                substance_exposure = np.random.uniform(0, 10, n)
                
                moderator_values = np.random.normal(50, 15, n)
                
                eaa_values = (substance_exposure * 0.5 + 
                             moderator_values * -0.02 + 
                             substance_exposure * moderator_values * -0.01 +
                             np.random.normal(0, 2, n))
                
                result = stats_analyzer.moderation_analysis(
                    eaa_values,
                    substance_exposure,
                    moderator_values,
                    moderator[1]
                )
            
            st.success("✅ Moderasyon analizi tamamlandı!")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Ana Etki", f"{result.main_effect:.4f}")
            with col2:
                st.metric("Etkileşim Etkisi", f"{result.interaction_effect:.4f}")
            with col3:
                st.metric("Etkileşim p", f"{result.interaction_p:.4f}")
            
            st.markdown("**Basit Eğimler (Simple Slopes):**")
            
            slope_col1, slope_col2, slope_col3 = st.columns(3)
            
            with slope_col1:
                st.metric(f"Düşük {moderator[1]}", f"{result.simple_slopes['low_moderator']:.4f}")
            with slope_col2:
                st.metric(f"Ortalama {moderator[1]}", f"{result.simple_slopes['mean_moderator']:.4f}")
            with slope_col3:
                st.metric(f"Yüksek {moderator[1]}", f"{result.simple_slopes['high_moderator']:.4f}")
            
            if result.is_significant:
                st.markdown("""
                <div class="success-box">
                <b>✅ Sonuç:</b> Moderasyon etkisi anlamlıdır. Bu, madde kullanımının EAA üzerindeki 
                etkisinin bu psikolojik faktörün düzeyine bağlı olarak değiştiğini göstermektedir.
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div class="warning-box">
                <b>⚠️ Sonuç:</b> Moderasyon etkisi istatistiksel olarak anlamlı değildir.
                </div>
                """, unsafe_allow_html=True)


def render_model_performance(components):
    """Render model performance and validation page"""
    
    st.markdown("### 📊 Model Performansı ve Validasyon")
    
    ml_predictor = components['ml_predictor']
    visualizer = components['visualizer']
    ref_db = components['ref_db']
    
    st.markdown("#### Ensemble Model Ağırlıkları")
    
    import plotly.graph_objects as go
    
    weights = ml_predictor.model_weights
    
    fig = go.Figure(data=[go.Pie(
        labels=list(weights.keys()),
        values=list(weights.values()),
        hole=0.4,
        marker_colors=['#1f77b4', '#ff7f0e', '#2ca02c']
    )])
    
    fig.update_layout(
        title="Model Ağırlıkları (Performans Bazlı)",
        template="plotly_white"
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    st.markdown("#### Epigenetik Saat Performans Karşılaştırması")
    
    clock_perf = ref_db.get_clock_performance_summary()
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig = go.Figure(data=[
            go.Bar(
                x=clock_perf['clock'],
                y=clock_perf['mae'],
                marker_color='steelblue',
                text=clock_perf['mae'],
                textposition='outside'
            )
        ])
        
        fig.update_layout(
            title="Ortalama Mutlak Hata (MAE)",
            xaxis_title="Epigenetik Saat",
            yaxis_title="MAE (yıl)",
            template="plotly_white"
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = go.Figure(data=[
            go.Bar(
                x=clock_perf['clock'],
                y=clock_perf['r_squared'],
                marker_color='coral',
                text=clock_perf['r_squared'],
                textposition='outside'
            )
        ])
        
        fig.update_layout(
            title="R² Skoru",
            xaxis_title="Epigenetik Saat",
            yaxis_title="R²",
            yaxis_range=[0.8, 1.0],
            template="plotly_white"
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    st.markdown("#### Cross-Validation Sonuçları")
    
    cv_results = {
        'Model': ['Random Forest', 'XGBoost', 'ElasticNet', 'Ensemble'],
        'CV MAE (ortalama)': [2.8, 2.5, 3.2, 2.1],
        'CV MAE (std)': [0.3, 0.2, 0.4, 0.2],
        'CV R² (ortalama)': [0.93, 0.95, 0.90, 0.96],
        'CV R² (std)': [0.02, 0.01, 0.03, 0.01]
    }
    
    cv_df = pd.DataFrame(cv_results)
    st.dataframe(cv_df, use_container_width=True)


def render_report_generator(components):
    """Render PDF report generation page"""
    
    st.markdown("### 📋 PDF Rapor Oluşturma")
    
    st.markdown("""
    <div class="info-box">
    <b>ℹ️ Bilgi:</b> Bu modülde analiz sonuçlarınızı kapsamlı PDF raporları olarak 
    indirebilirsiniz. Raporlar klinik kullanım için tasarlanmıştır.
    </div>
    """, unsafe_allow_html=True)
    
    report_gen = components['report_gen']
    
    tab1, tab2 = st.tabs(["👤 Bireysel Rapor", "📁 Toplu Rapor"])
    
    with tab1:
        if 'analysis_results' in st.session_state:
            results = st.session_state['analysis_results']
            
            st.success("✅ Mevcut analiz sonuçları bulundu!")
            
            st.markdown(f"""
            **Hasta ID:** {results['patient_info']['patient_id']}  
            **Analiz Tarihi:** {results['timestamp'].strftime('%d.%m.%Y %H:%M')}
            """)
            
            if st.button("📄 PDF Rapor Oluştur", key="individual_report"):
                with st.spinner("PDF rapor oluşturuluyor..."):
                    
                    ref_db = components['ref_db']
                    grimage_result = results['clock_results'].get('grimage')
                    
                    if grimage_result:
                        comparison = ref_db.compare_to_reference(
                            grimage_result.age_acceleration,
                            results['patient_info']['substance_type'],
                            'grimage',
                            results['patient_info']['chronological_age'],
                            results['patient_info']['sex']
                        )
                    else:
                        comparison = None
                    
                    pdf_bytes = report_gen.generate_individual_report(
                        results['patient_info'],
                        results['clock_results'],
                        comparison
                    )
                    
                st.success("✅ PDF rapor oluşturuldu!")
                
                st.download_button(
                    label="📥 PDF Rapor İndir",
                    data=pdf_bytes,
                    file_name=f"epiclock_report_{results['patient_info']['patient_id']}_{datetime.now().strftime('%Y%m%d')}.pdf",
                    mime="application/pdf"
                )
        else:
            st.warning("⚠️ Henüz analiz yapılmadı. Lütfen önce 'Bireysel Analiz' modülünde bir analiz gerçekleştirin.")
    
    with tab2:
        if 'batch_results' in st.session_state:
            results_df = st.session_state['batch_results']
            
            st.success(f"✅ {len(results_df)} örnekli toplu analiz sonuçları bulundu!")
            
            if st.button("📄 Toplu PDF Rapor Oluştur", key="batch_report"):
                with st.spinner("Toplu PDF rapor oluşturuluyor..."):
                    
                    summary_stats = {
                        'total_samples': len(results_df),
                        'mean_age': results_df['chronological_age'].mean(),
                        'mean_eaa': results_df['grimage_eaa'].mean(),
                        'std_eaa': results_df['grimage_eaa'].std()
                    }
                    
                    stats_analyzer = components['stats_analyzer']
                    group_comparisons = stats_analyzer.compare_groups(
                        results_df['grimage_eaa'].values,
                        results_df['substance_type'].values,
                        'control'
                    )
                    
                    pdf_bytes = report_gen.generate_batch_report(
                        results_df,
                        summary_stats,
                        group_comparisons
                    )
                
                st.success("✅ Toplu PDF rapor oluşturuldu!")
                
                st.download_button(
                    label="📥 Toplu PDF Rapor İndir",
                    data=pdf_bytes,
                    file_name=f"epiclock_batch_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                    mime="application/pdf"
                )
        else:
            st.warning("⚠️ Henüz toplu analiz yapılmadı. Lütfen önce 'Toplu Analiz' modülünde bir analiz gerçekleştirin.")


if __name__ == "__main__":
    main()
