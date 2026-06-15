# ============================================================================
# EpiClock Prototype - DNA Methylation Epigenetic Age Analysis Platform
# Copyright (c) 2024 Dr. Nurcan Denli Bayır (nrcdnl94)
# GitHub: https://github.com/mortemdulcem/epi-clock-DNA-mtl-prototype
# All rights reserved. See LICENSE file for details.
# Author Signature: nrcdnl94
# ============================================================================

"""
UNODC World Drug Report Style Theme for EpiClock
Professional UN-style design with blue color scheme
"""

import streamlit as st

# nrcdnl94 - UNODC Color Palette (Updated to match prompt specifications)
UNODC_COLORS = {
    'primary_blue': '#0050A0',      # Deep UN Blue (Primary)
    'dark_blue': '#003366',         # Dark Navy
    'light_blue': '#00A7D8',        # Light Blue / Turkuaz
    'accent_blue': '#0072BC',       # Accent Blue
    'gold': '#FFD100',              # UN Gold (minimal use)
    'white': '#FFFFFF',
    'light_gray': '#F5F7FA',
    'neutral_gray': '#E8EEF5',      # Panel background
    'dark_gray': '#333333',
    'text_gray': '#666666',
    'text_dark': '#1A1A2E',         # Dark text for readability
    'success': '#28A745',
    'warning': '#FFC107',
    'danger': '#DC3545',
    'info': '#17A2B8'
}

def apply_unodc_theme():
    """Apply UNODC-style professional theme to the app - nrcdnl94"""
    st.markdown("""
    <style>
    /* nrcdnl94 - UNODC Theme CSS - Tailwind-inspired clean design */
    
    /* Import Professional Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Main App Container */
    .stApp {
        background: #F8FAFC;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Hide Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Sidebar Styling - Clean White with Blue Accents */
    [data-testid="stSidebar"] {
        background: #FFFFFF;
        border-right: 1px solid #E2E8F0;
    }
    
    [data-testid="stSidebar"] * {
        color: #334155 !important;
    }
    
    [data-testid="stSidebar"] .stSelectbox label,
    [data-testid="stSidebar"] .stRadio label {
        color: #0050A0 !important;
        font-weight: 500;
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    /* Global Streamlit Button Styling - UNODC Corporate */
    .stButton > button {
        background: #0050A0 !important;
        color: #FFFFFF !important;
        border: 1px solid #0050A0 !important;
        padding: 8px 20px !important;
        border-radius: 6px !important;
        font-size: 0.85rem !important;
        font-weight: 600 !important;
        font-family: 'Inter', sans-serif !important;
        cursor: pointer !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 2px 4px rgba(0, 80, 160, 0.2) !important;
    }
    .stButton > button:hover {
        background: #003D7A !important;
        border-color: #003D7A !important;
        box-shadow: 0 4px 8px rgba(0, 80, 160, 0.3) !important;
    }
    .stButton > button:active {
        background: #002952 !important;
    }
    
    /* Secondary Button Style */
    .stButton > button[kind="secondary"] {
        background: #FFFFFF !important;
        color: #0050A0 !important;
        border: 1px solid #0050A0 !important;
    }
    .stButton > button[kind="secondary"]:hover {
        background: #E8F4FC !important;
        color: #003366 !important;
    }
    
    /* File Uploader Styling */
    [data-testid="stFileUploader"] {
        border: 2px dashed #0050A0 !important;
        border-radius: 8px !important;
        padding: 20px !important;
        background: #F8FAFC !important;
    }
    [data-testid="stFileUploader"] label {
        color: #0050A0 !important;
        font-weight: 600 !important;
    }
    
    /* Tab Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: #FFFFFF;
        border-bottom: 1px solid #E2E8F0;
    }
    .stTabs [data-baseweb="tab"] {
        color: #64748B !important;
        font-weight: 500 !important;
        font-size: 0.85rem !important;
        padding: 12px 16px !important;
        border-radius: 6px 6px 0 0 !important;
    }
    .stTabs [aria-selected="true"] {
        color: #0050A0 !important;
        background: #FFFFFF !important;
        border-bottom: 2px solid #0050A0 !important;
    }
    
    /* Main Header Banner */
    .main-header {
        background: linear-gradient(135deg, #1A3A5C 0%, #0072BC 50%, #009EDB 100%);
        color: white;
        padding: 30px 40px;
        border-radius: 0 0 20px 20px;
        margin: -1rem -1rem 2rem -1rem;
        box-shadow: 0 4px 20px rgba(0, 114, 188, 0.3);
        text-align: center;
    }
    
    .main-header h1 {
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .main-header p {
        font-size: 1.1rem;
        opacity: 0.9;
        margin-top: 10px;
    }
    
    /* UN Logo Badge */
    .un-badge {
        display: inline-flex;
        align-items: center;
        gap: 15px;
        background: rgba(255,255,255,0.1);
        padding: 10px 20px;
        border-radius: 50px;
        margin-bottom: 15px;
    }
    
    .un-badge img {
        height: 50px;
    }
    
    /* Hero Slider Section */
    .hero-slider {
        background: linear-gradient(135deg, #009EDB 0%, #0072BC 100%);
        border-radius: 15px;
        padding: 40px;
        margin-bottom: 30px;
        color: white;
        text-align: center;
        box-shadow: 0 8px 30px rgba(0, 114, 188, 0.4);
    }
    
    .hero-slider h2 {
        font-size: 2rem;
        margin-bottom: 15px;
    }
    
    .hero-slider p {
        font-size: 1.2rem;
        opacity: 0.95;
    }
    
    /* Module Cards Grid - Booklet Style */
    .module-card {
        background: white;
        border-radius: 12px;
        padding: 25px;
        margin: 10px 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        border-left: 4px solid #009EDB;
        transition: all 0.3s ease;
        cursor: pointer;
    }
    
    .module-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(0, 114, 188, 0.2);
        border-left-color: #FFD100;
    }
    
    .module-card h3 {
        color: #1A3A5C;
        font-size: 1.2rem;
        margin-bottom: 10px;
        font-weight: 600;
    }
    
    .module-card p {
        color: #666666;
        font-size: 0.95rem;
        line-height: 1.5;
    }
    
    .module-card .icon {
        font-size: 2.5rem;
        margin-bottom: 15px;
    }
    
    /* Booklet Icons Grid */
    .booklet-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 20px;
        margin: 30px 0;
    }
    
    .booklet-item {
        background: linear-gradient(145deg, #FFFFFF 0%, #F5F7FA 100%);
        border-radius: 15px;
        padding: 30px 20px;
        text-align: center;
        box-shadow: 0 5px 20px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
        border: 2px solid transparent;
    }
    
    .booklet-item:hover {
        border-color: #009EDB;
        transform: scale(1.03);
        box-shadow: 0 10px 30px rgba(0, 114, 188, 0.2);
    }
    
    .booklet-item .icon {
        font-size: 3rem;
        margin-bottom: 15px;
        display: block;
    }
    
    .booklet-item h4 {
        color: #1A3A5C;
        font-size: 1rem;
        font-weight: 600;
        margin: 10px 0;
    }
    
    .booklet-item p {
        color: #666;
        font-size: 0.85rem;
    }
    
    /* Stats Cards Row */
    .stats-row {
        display: flex;
        justify-content: space-around;
        gap: 20px;
        margin: 30px 0;
        flex-wrap: wrap;
    }
    
    .stat-card {
        background: linear-gradient(135deg, #1A3A5C 0%, #0072BC 100%);
        color: white;
        padding: 25px 35px;
        border-radius: 12px;
        text-align: center;
        min-width: 180px;
        box-shadow: 0 5px 20px rgba(0, 114, 188, 0.3);
    }
    
    .stat-card .number {
        font-size: 2.5rem;
        font-weight: 700;
        display: block;
        color: #FFD100;
    }
    
    .stat-card .label {
        font-size: 0.9rem;
        opacity: 0.9;
        margin-top: 5px;
    }
    
    /* Data Tables - Professional Style */
    .stDataFrame {
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 3px 15px rgba(0,0,0,0.1);
    }
    
    .stDataFrame table {
        border-collapse: collapse;
    }
    
    .stDataFrame th {
        background: linear-gradient(135deg, #1A3A5C 0%, #0072BC 100%) !important;
        color: white !important;
        font-weight: 600;
        padding: 12px 15px !important;
    }
    
    .stDataFrame td {
        padding: 10px 15px !important;
        border-bottom: 1px solid #E8EEF5;
    }
    
    .stDataFrame tr:hover td {
        background: #F0F8FF !important;
    }
    
    /* Buttons - UN Blue Style */
    .stButton > button {
        background: linear-gradient(135deg, #009EDB 0%, #0072BC 100%);
        color: white;
        border: none;
        padding: 12px 30px;
        border-radius: 8px;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0, 114, 188, 0.3);
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #0072BC 0%, #1A3A5C 100%);
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0, 114, 188, 0.4);
    }
    
    /* Tabs - Professional Style */
    .stTabs [data-baseweb="tab-list"] {
        background: white;
        border-radius: 10px;
        padding: 5px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    }
    
    .stTabs [data-baseweb="tab"] {
        color: #1A3A5C;
        font-weight: 500;
        border-radius: 8px;
        padding: 10px 20px;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #009EDB 0%, #0072BC 100%);
        color: white !important;
    }
    
    /* Metric Cards */
    [data-testid="stMetric"] {
        background: white;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 3px 15px rgba(0,0,0,0.08);
        border-left: 4px solid #009EDB;
    }
    
    [data-testid="stMetricLabel"] {
        color: #1A3A5C !important;
        font-weight: 600;
    }
    
    [data-testid="stMetricValue"] {
        color: #0072BC !important;
        font-size: 2rem !important;
    }
    
    /* Expanders */
    .streamlit-expanderHeader {
        background: linear-gradient(135deg, #F5F7FA 0%, #E8EEF5 100%);
        border-radius: 10px;
        border-left: 4px solid #009EDB;
        font-weight: 600;
        color: #1A3A5C;
    }
    
    /* Alerts / Info Boxes */
    .stAlert {
        border-radius: 10px;
        border-left: 4px solid;
    }
    
    /* Section Dividers */
    .section-divider {
        height: 3px;
        background: linear-gradient(90deg, #009EDB 0%, #FFD100 50%, #009EDB 100%);
        margin: 40px 0;
        border-radius: 2px;
    }
    
    /* Footer */
    .footer {
        background: linear-gradient(135deg, #1A3A5C 0%, #0D2137 100%);
        color: white;
        padding: 30px;
        margin-top: 50px;
        border-radius: 15px 15px 0 0;
        text-align: center;
    }
    
    .footer a {
        color: #4DB8E8;
        text-decoration: none;
    }
    
    .footer .copyright {
        margin-top: 15px;
        opacity: 0.8;
        font-size: 0.9rem;
    }
    
    /* Charts Container */
    .chart-container {
        background: white;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 3px 15px rgba(0,0,0,0.08);
        margin: 15px 0;
    }
    
    /* Progress Bars */
    .stProgress > div > div {
        background: linear-gradient(90deg, #009EDB 0%, #0072BC 100%);
        border-radius: 10px;
    }
    
    /* Selectbox */
    .stSelectbox > div > div {
        border-radius: 8px;
        border: 2px solid #E8EEF5;
    }
    
    .stSelectbox > div > div:focus-within {
        border-color: #009EDB;
        box-shadow: 0 0 0 3px rgba(0, 158, 219, 0.2);
    }
    
    /* Radio Buttons */
    .stRadio > div {
        background: white;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    }
    
    /* Number Input */
    .stNumberInput > div > div > input {
        border-radius: 8px;
        border: 2px solid #E8EEF5;
    }
    
    .stNumberInput > div > div > input:focus {
        border-color: #009EDB;
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: #F5F7FA;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #009EDB 0%, #0072BC 100%);
        border-radius: 5px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #1A3A5C;
    }
    
    </style>
    """, unsafe_allow_html=True)

def render_top_navigation():
    """Render UNODC-style top navigation bar - nrcdnl94"""
    st.markdown("""
    <style>
    .top-nav {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        z-index: 9999;
        background: #FFFFFF;
        border-bottom: 1px solid #E8EEF5;
        padding: 0;
        display: flex;
        align-items: center;
        justify-content: space-between;
        height: 60px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
    }
    .top-nav-logo {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 0 24px;
        font-weight: 700;
        color: #0050A0;
        font-size: 1.1rem;
    }
    .top-nav-menu {
        display: flex;
        align-items: center;
        gap: 0;
        height: 100%;
    }
    .top-nav-menu a {
        color: #333333;
        text-decoration: none;
        font-size: 0.9rem;
        font-weight: 500;
        padding: 20px 18px;
        height: 100%;
        display: flex;
        align-items: center;
        transition: all 0.2s ease;
        border-bottom: 3px solid transparent;
    }
    .top-nav-menu a:hover {
        background: #F5F7FA;
        color: #0050A0;
        border-bottom: 3px solid #00A7D8;
    }
    .top-nav-menu a.active {
        color: #0050A0;
        border-bottom: 3px solid #0050A0;
        font-weight: 600;
    }
    .top-nav-right {
        display: flex;
        align-items: center;
        gap: 16px;
        padding-right: 24px;
    }
    .lang-switch {
        font-size: 0.8rem;
        color: #666666;
    }
    .lang-switch a {
        color: #0050A0;
        text-decoration: none;
    }
    .top-spacer {
        height: 60px;
    }
    </style>
    <div class="top-nav">
        <div class="top-nav-logo">
            <svg width="32" height="32" viewBox="0 0 32 32" fill="none">
                <circle cx="16" cy="16" r="14" stroke="#0050A0" stroke-width="2" fill="none"/>
                <path d="M10 16 Q16 8 22 16 Q16 24 10 16" stroke="#00A7D8" stroke-width="1.5" fill="none"/>
                <path d="M10 16 Q16 24 22 16 Q16 8 10 16" stroke="#0050A0" stroke-width="1.5" fill="none"/>
            </svg>
            <span>National DNA Analysis System</span>
        </div>
        <div class="top-nav-menu">
            <a href="#" class="active">Dashboard</a>
            <a href="#">Samples</a>
            <a href="#">Analyses</a>
            <a href="#">Reports</a>
            <a href="#">Database</a>
            <a href="#">Settings</a>
        </div>
        <div class="top-nav-right">
            <span class="lang-switch"><a href="#">TR</a> | <a href="#">EN</a></span>
        </div>
    </div>
    <div class="top-spacer"></div>
    """, unsafe_allow_html=True)

def render_main_header():
    """Render UNODC-style main header with functional buttons - nrcdnl94"""
    st.markdown("""
    <style>
    .unodc-page-header-box {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 8px;
        padding: 16px 20px;
        margin-bottom: 20px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    .unodc-page-version {
        font-size: 1.6rem;
        font-weight: 700;
        color: #003366;
        margin: 0 0 8px 0;
    }
    .unodc-page-title-text {
        font-size: 0.95rem;
        font-weight: 600;
        color: #0050A0;
        margin: 0;
        line-height: 1.4;
    }
    .unodc-page-subtitle-text {
        font-size: 0.72rem;
        color: #64748B;
        margin: 6px 0 0 0;
        line-height: 1.5;
    }
    </style>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.markdown("""
        <div class="unodc-page-header-box">
            <div class="unodc-page-version">EpiClock v4.0</div>
            <h1 class="unodc-page-title-text">DNA Metilasyonu Temelli Epigenetik Yas Analiz Platformu</h1>
            <p class="unodc-page-subtitle-text">
                Madde bagimliligi maruziyetinin biyolojik etkilerini, epigenetik yas ivmesi (EAA) metrikleri ile degerlendiren multi-task learning temelli klinik analiz sistemi.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        if st.button("Arama", key="header_search_btn"):
            st.session_state['show_search_dialog'] = True
    
    if st.session_state.get('show_search_dialog', False):
        render_search_dialog()
    
    render_infographic_cards()


def render_search_dialog():
    """Render search dialog - nrcdnl94"""
    with st.expander("Arama", expanded=True):
        search_query = st.text_input("Anahtar kelime girin:", key="search_input", placeholder="CpG, gen adi, madde...")
        
        col1, col2 = st.columns(2)
        with col1:
            search_type = st.selectbox("Arama Tipi:", 
                ["Tum Veritabani", "CpG Markerlari", "Genler", "Maddeler", "NPS"], 
                key="search_type")
        with col2:
            if st.button("Ara", key="search_execute_btn"):
                if search_query:
                    st.session_state['search_results'] = f"'{search_query}' icin arama yapiliyor..."
                    st.info(f"Arama: '{search_query}' - Tip: {search_type}")
        
        if st.button("Kapat", key="close_search_btn"):
            st.session_state['show_search_dialog'] = False
            st.rerun()


def render_infographic_cards():
    """Render infographic cards explaining system capabilities using Streamlit native - nrcdnl94"""
    
    st.markdown("""
    <style>
    .info-card-box {
        background: linear-gradient(135deg, #FFFFFF 0%, #F8FAFC 100%);
        border: 1px solid #E2E8F0;
        border-radius: 8px;
        padding: 14px;
        height: 140px;
        position: relative;
    }
    .info-card-box:hover {
        border-color: #0050A0;
        box-shadow: 0 4px 12px rgba(0,80,160,0.1);
    }
    .info-badge {
        position: absolute;
        top: 8px;
        right: 8px;
        background: #00A7D8;
        color: #FFFFFF;
        font-size: 0.6rem;
        font-weight: 600;
        padding: 2px 6px;
        border-radius: 4px;
    }
    .info-icon-box {
        width: 32px;
        height: 32px;
        background: linear-gradient(135deg, #0050A0 0%, #00A7D8 100%);
        border-radius: 6px;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        color: #FFFFFF;
        font-size: 0.8rem;
        font-weight: 700;
        margin-bottom: 8px;
    }
    .info-title {
        font-size: 0.8rem;
        font-weight: 600;
        color: #0050A0;
        margin: 0 0 4px 0;
    }
    .info-desc {
        font-size: 0.65rem;
        color: #64748B;
        margin: 0;
        line-height: 1.3;
    }
    .info-stat {
        font-size: 0.95rem;
        font-weight: 700;
        color: #003366;
        margin-top: 6px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    cards_data = [
        {"badge": "29.4M", "icon": "CpG", "title": "CpG Genom Veritabani", 
         "desc": "29.4 milyon CpG sitesi, kromozom pozisyonlari", "stat": "28M Site"},
        {"badge": "850K", "icon": "AR", "title": "Illumina Array Destegi", 
         "desc": "EPIC, 450K, 27K array platformlari", "stat": "485K Prob"},
        {"badge": "750M", "icon": "VR", "title": "Genomik Varyantlar", 
         "desc": "gnomAD, UK Biobank, TOPMed entegrasyonu", "stat": "12M SNP"},
        {"badge": "36K+", "icon": "MK", "title": "Markush Yapilar", 
         "desc": "29,277 yapisal varyant, NPS tespiti", "stat": "10 Kural"},
        {"badge": "5", "icon": "EP", "title": "Epigenetik Saatler", 
         "desc": "Horvath, Hannum, PhenoAge, GrimAge, DunedinPACE", "stat": "2,140 CpG"},
        {"badge": "18", "icon": "MT", "title": "Madde Tespiti", 
         "desc": "Sigara, alkol, kokain, eroin, metamfetamin", "stat": "100+ Marker"},
        {"badge": "6,893", "icon": "NPS", "title": "NPS Veritabani", 
         "desc": "Sentetik kannabinoidler, fentanil analoglari", "stat": "1,920 Sanal"},
        {"badge": "12", "icon": "TK", "title": "Doku-Spesifik Saatler", 
         "desc": "Beyin, karaciger, bobrek, kalp, kan, deri", "stat": "Capraz Norm"},
        {"badge": "2,800+", "icon": "GN", "title": "Gen Veritabani", 
         "desc": "Bagimlilik genleri, 14 biyolojik sistem", "stat": "14 Sistem"},
        {"badge": "GWAS", "icon": "PRS", "title": "Poligenik Risk Skoru", 
         "desc": "Alkol, nikotin, opioid, kokain riskleri", "stat": "1.2M Ornek"},
        {"badge": "SHA-256", "icon": "BC", "title": "Blockchain Denetim", 
         "desc": "Hash zinciri, Daubert kriterleri", "stat": "Tamper-Proof"},
        {"badge": "10,542", "icon": "RF", "title": "Referans Veritabani", 
         "desc": "15 kohort, DNA metilasyon profilleri", "stat": "7 Kategori"},
    ]
    
    for row_start in range(0, len(cards_data), 4):
        cols = st.columns(4)
        for i, col in enumerate(cols):
            card_idx = row_start + i
            if card_idx < len(cards_data):
                card = cards_data[card_idx]
                with col:
                    st.markdown(f"""
                    <div class="info-card-box">
                        <div class="info-badge">{card['badge']}</div>
                        <div class="info-icon-box">{card['icon']}</div>
                        <div class="info-title">{card['title']}</div>
                        <div class="info-desc">{card['desc']}</div>
                        <div class="info-stat">{card['stat']}</div>
                    </div>
                    """, unsafe_allow_html=True)


def render_statistic_cards():
    """Render UNODC-style statistic cards - Tailwind-inspired - nrcdnl94"""
    st.markdown("""
    <style>
    .stat-cards-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 16px;
        margin-bottom: 20px;
    }
    .stat-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 8px;
        padding: 12px 16px;
    }
    .stat-card-label {
        font-size: 0.7rem;
        font-weight: 600;
        color: #64748B;
        text-transform: uppercase;
        letter-spacing: 0.03em;
        margin: 0;
    }
    .stat-card-value-row {
        display: flex;
        align-items: baseline;
        justify-content: space-between;
        margin-top: 8px;
    }
    .stat-card-value {
        font-size: 1.5rem;
        font-weight: 600;
        color: #0050A0;
        margin: 0;
    }
    .stat-card-value.danger {
        color: #DC2626;
    }
    .stat-card-meta {
        font-size: 0.65rem;
        color: #94A3B8;
    }
    @media (max-width: 768px) {
        .stat-cards-grid {
            grid-template-columns: repeat(2, 1fr);
        }
    }
    </style>
    <div class="stat-cards-grid">
        <div class="stat-card">
            <p class="stat-card-label">Toplam Ornek</p>
            <div class="stat-card-value-row">
                <span class="stat-card-value">1.248</span>
                <span class="stat-card-meta">Tumu</span>
            </div>
        </div>
        <div class="stat-card">
            <p class="stat-card-label">Aktif Analizler</p>
            <div class="stat-card-value-row">
                <span class="stat-card-value">37</span>
                <span class="stat-card-meta">Laboratuvar</span>
            </div>
        </div>
        <div class="stat-card">
            <p class="stat-card-label">Tamamlanan Raporlar</p>
            <div class="stat-card-value-row">
                <span class="stat-card-value">892</span>
                <span class="stat-card-meta">Son 12 ay</span>
            </div>
        </div>
        <div class="stat-card">
            <p class="stat-card-label">Uyarilar / QC Sorunlari</p>
            <div class="stat-card-value-row">
                <span class="stat-card-value danger">5</span>
                <span class="stat-card-meta">Inceleme bekleyen</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_recent_analyses_table():
    """Render recent analyses table with working navigation - Tailwind-inspired - nrcdnl94"""
    import pandas as pd
    
    st.markdown("""
    <style>
    .analyses-section-header {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-bottom: none;
        border-radius: 8px 8px 0 0;
        padding: 12px 20px;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    .analyses-title-text {
        font-size: 0.875rem;
        font-weight: 600;
        color: #334155;
        margin: 0;
    }
    </style>
    <div class="analyses-section-header">
        <span class="analyses-title-text">Son Analizler</span>
    </div>
    """, unsafe_allow_html=True)
    
    analyses_data = [
        {"id": "2025-STR-00123", "type": "Kan", "module": "STR / Adli", "status": "Tamamlandi", "date": "06.12.2025"},
        {"id": "2025-NGS-00456", "type": "Tam Kan", "module": "NGS", "status": "Devam Ediyor", "date": "05.12.2025"},
        {"id": "2025-CLN-00078", "type": "DNA Ekstrakt", "module": "Klinik Genetik", "status": "QC Gerekli", "date": "04.12.2025"},
        {"id": "2025-EPI-00891", "type": "Salya", "module": "Epigenetik Yas", "status": "Tamamlandi", "date": "03.12.2025"},
    ]
    
    cols = st.columns([2, 1, 2, 2, 1.5, 1])
    with cols[0]:
        st.markdown("**Ornek ID**")
    with cols[1]:
        st.markdown("**Tur**")
    with cols[2]:
        st.markdown("**Modul**")
    with cols[3]:
        st.markdown("**Durum**")
    with cols[4]:
        st.markdown("**Tarih**")
    with cols[5]:
        st.markdown("**Islem**")
    
    st.markdown("<hr style='margin: 0; border-color: #E2E8F0;'>", unsafe_allow_html=True)
    
    for i, analysis in enumerate(analyses_data):
        cols = st.columns([2, 1, 2, 2, 1.5, 1])
        
        with cols[0]:
            st.markdown(f"<span style='font-size: 0.8rem; color: #334155;'>{analysis['id']}</span>", unsafe_allow_html=True)
        with cols[1]:
            st.markdown(f"<span style='font-size: 0.8rem; color: #334155;'>{analysis['type']}</span>", unsafe_allow_html=True)
        with cols[2]:
            st.markdown(f"<span style='font-size: 0.8rem; color: #334155;'>{analysis['module']}</span>", unsafe_allow_html=True)
        with cols[3]:
            if analysis['status'] == 'Tamamlandi':
                st.markdown("<span style='background: #F0FDF4; color: #166534; border: 1px solid #BBF7D0; padding: 2px 8px; border-radius: 9999px; font-size: 0.7rem;'>Tamamlandi</span>", unsafe_allow_html=True)
            elif analysis['status'] == 'Devam Ediyor':
                st.markdown("<span style='background: #FEFCE8; color: #A16207; border: 1px solid #FEF08A; padding: 2px 8px; border-radius: 9999px; font-size: 0.7rem;'>Devam Ediyor</span>", unsafe_allow_html=True)
            else:
                st.markdown("<span style='background: #FEF2F2; color: #DC2626; border: 1px solid #FECACA; padding: 2px 8px; border-radius: 9999px; font-size: 0.7rem;'>QC Gerekli</span>", unsafe_allow_html=True)
        with cols[4]:
            st.markdown(f"<span style='font-size: 0.8rem; color: #334155;'>{analysis['date']}</span>", unsafe_allow_html=True)
        with cols[5]:
            if st.button("Detay", key=f"detail_{i}", type="secondary"):
                st.session_state['current_page'] = 'analysis_detail'
                st.session_state['selected_analysis'] = analysis
                st.rerun()


def render_analysis_detail_page():
    """Render analysis detail page with tabs - UNODC Tailwind style - nrcdnl94"""
    
    if 'selected_analysis' not in st.session_state:
        st.session_state['selected_analysis'] = {
            "id": "2025-NGS-00456", 
            "type": "Tam Kan", 
            "module": "NGS", 
            "status": "Devam Ediyor", 
            "date": "05.12.2025"
        }
    
    analysis = st.session_state['selected_analysis']
    
    st.markdown("""
    <style>
    .breadcrumb-nav {
        font-size: 0.7rem;
        color: #64748B;
        margin-bottom: 12px;
    }
    .breadcrumb-nav a {
        color: #0050A0;
        text-decoration: none;
    }
    .breadcrumb-nav a:hover {
        text-decoration: underline;
    }
    .detail-header-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 8px;
        padding: 16px 20px;
        margin-bottom: 16px;
    }
    .detail-title {
        font-size: 1.1rem;
        font-weight: 600;
        color: #0050A0;
        margin: 0;
    }
    .detail-subtitle {
        font-size: 0.75rem;
        color: #64748B;
        margin-top: 4px;
    }
    .summary-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 8px;
        padding: 16px;
    }
    .summary-title {
        font-size: 0.8rem;
        font-weight: 600;
        color: #334155;
        margin-bottom: 12px;
    }
    .summary-item {
        font-size: 0.75rem;
        color: #475569;
        margin-bottom: 4px;
    }
    .summary-label {
        font-weight: 600;
    }
    .metric-value {
        color: #0050A0;
        font-weight: 600;
    }
    </style>
    """, unsafe_allow_html=True)
    
    col_back, col_title = st.columns([1, 11])
    with col_back:
        if st.button("Geri", type="secondary"):
            st.session_state['current_page'] = 'dashboard'
            st.rerun()
    
    st.markdown(f"""
    <div class="breadcrumb-nav">
        <span style="cursor:pointer; color:#0050A0;">Dashboard</span> / 
        <span style="cursor:pointer; color:#0050A0;">Analizler</span> / 
        <span style="color:#334155; font-weight:500;">{analysis['module']} - {analysis['id']}</span>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown(f"""
        <div class="detail-header-card">
            <h1 class="detail-title">{analysis['module']} Analizi - Ornek ID: {analysis['id']}</h1>
            <p class="detail-subtitle">Ornek turu: {analysis['type']} | Platform: Illumina | Laboratuvar: Adli Genetik Birimi</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        if analysis['status'] == 'Tamamlandi':
            st.success("Durum: Tamamlandi")
        elif analysis['status'] == 'Devam Ediyor':
            st.warning("Durum: Devam Ediyor")
        else:
            st.error("Durum: QC Gerekli")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        <div class="summary-card">
            <div class="summary-title">Ornek Ozeti</div>
        </div>
        """, unsafe_allow_html=True)
        
        subcol1, subcol2 = st.columns(2)
        with subcol1:
            st.markdown(f"""
            <div class="summary-item"><span class="summary-label">Ornek ID:</span> {analysis['id']}</div>
            <div class="summary-item"><span class="summary-label">Ornek Turu:</span> {analysis['type']}</div>
            <div class="summary-item"><span class="summary-label">Alinma Tarihi:</span> {analysis['date']}</div>
            <div class="summary-item"><span class="summary-label">Laboratuvar Kodu:</span> AG-IST-01</div>
            """, unsafe_allow_html=True)
        with subcol2:
            st.markdown(f"""
            <div class="summary-item"><span class="summary-label">Analiz Turu:</span> {analysis['module']}</div>
            <div class="summary-item"><span class="summary-label">Platform:</span> Illumina NovaSeq</div>
            <div class="summary-item"><span class="summary-label">Sorumlu Uzman:</span> Uzm. Biyolog A.B.</div>
            <div class="summary-item"><span class="summary-label">Oncelik:</span> Yuksek</div>
            """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="summary-card">
            <div class="summary-title">NGS Ozet Metrikleri</div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("""
        <div class="summary-item">Toplam Okuma Sayisi: <span class="metric-value">85.2 M</span></div>
        <div class="summary-item">Ortalama Coverage: <span class="metric-value">102x</span></div>
        <div class="summary-item">Q30 Uzerindeki Okumalar: <span class="metric-value">93.5%</span></div>
        <div class="summary-item">Hizalanma Orani: <span class="metric-value">99.1%</span></div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "Genel Bakis",
        "Quality Control (QC)",
        "Alignment",
        "Varyantlar",
        "STR Profil"
    ])
    
    with tab1:
        render_overview_tab(analysis)
    
    with tab2:
        render_qc_tab(analysis)
    
    with tab3:
        render_alignment_tab(analysis)
    
    with tab4:
        render_variants_tab(analysis)
    
    with tab5:
        render_str_tab(analysis)


def render_overview_tab(analysis):
    """Render overview tab content - nrcdnl94"""
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="summary-card">
            <div class="summary-title">QC Durumu (Ozet)</div>
            <p style="font-size: 0.7rem; color: #64748B;">QC metrikleri genel olarak kabul edilebilir sinirlar icindedir.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="summary-item">Ortalama Base Kalitesi (Q-score): <span class="metric-value">Q35</span></div>
        <div class="summary-item">GC Icerigi: <span class="metric-value">49%</span></div>
        <div class="summary-item">Duplikasyon Orani: <span class="metric-value">8.2%</span></div>
        <div class="summary-item">Adaptor Kontaminasyonu: <span class="metric-value">0.3%</span></div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="summary-card">
            <div class="summary-title">Analiz Durumu</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="summary-item">Pre-processing: <span style="color: #166534;">Tamamlandi</span></div>
        <div class="summary-item">Alignment: <span style="color: #166534;">Tamamlandi</span></div>
        <div class="summary-item">Variant Calling: <span style="color: #A16207;">Devam Ediyor</span></div>
        <div class="summary-item">Raporlama: <span style="color: #64748B;">Beklemede</span></div>
        """, unsafe_allow_html=True)


def render_qc_tab(analysis):
    """Render QC tab content - nrcdnl94"""
    import plotly.graph_objects as go
    import numpy as np
    
    st.markdown("#### Quality Control Detaylari")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="summary-card">
            <div class="summary-title">FastQC Metrikleri</div>
        </div>
        """, unsafe_allow_html=True)
        
        metrics_data = {
            "Metrik": ["Toplam Okuma", "Ortalama Okuma Uzunlugu", "Q20 Orani", "Q30 Orani", "GC Icerigi", "N Orani"],
            "Deger": ["85.2 M", "150 bp", "97.8%", "93.5%", "49%", "0.02%"],
            "Durum": ["Pass", "Pass", "Pass", "Pass", "Pass", "Pass"]
        }
        
        import pandas as pd
        df = pd.DataFrame(metrics_data)
        st.dataframe(df, use_container_width=True, hide_index=True)
    
    with col2:
        positions = list(range(1, 151))
        quality_scores = [35 - (0.05 * i) + np.random.uniform(-1, 1) for i in range(150)]
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=positions,
            y=quality_scores,
            mode='lines',
            line=dict(color='#0050A0', width=2),
            name='Q-Score'
        ))
        fig.add_hline(y=30, line_dash="dash", line_color="#166534", annotation_text="Q30 Esik")
        fig.add_hline(y=20, line_dash="dash", line_color="#DC2626", annotation_text="Q20 Esik")
        
        fig.update_layout(
            title="Pozisyona Gore Base Kalitesi",
            xaxis_title="Pozisyon (bp)",
            yaxis_title="Q-Score",
            template="plotly_white",
            height=300,
            font=dict(family="Inter, sans-serif")
        )
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("#### Duplikasyon Analizi")
    col1, col2 = st.columns(2)
    
    with col1:
        labels = ['Tekil Okumalar', 'Duplike Okumalar']
        values = [91.8, 8.2]
        
        fig = go.Figure(data=[go.Pie(
            labels=labels,
            values=values,
            hole=0.5,
            marker_colors=['#0050A0', '#00A7D8']
        )])
        fig.update_layout(
            title="Duplikasyon Orani",
            template="plotly_white",
            height=250,
            font=dict(family="Inter, sans-serif")
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("""
        <div class="summary-card">
            <div class="summary-title">Kontaminasyon Kontrolu</div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("""
        <div class="summary-item">Adaptor Kontaminasyonu: <span class="metric-value">0.3%</span> <span style="color:#166534;">(Pass)</span></div>
        <div class="summary-item">Yabanci DNA: <span class="metric-value">0.1%</span> <span style="color:#166534;">(Pass)</span></div>
        <div class="summary-item">rRNA Kontaminasyonu: <span class="metric-value">0.05%</span> <span style="color:#166534;">(Pass)</span></div>
        """, unsafe_allow_html=True)


def render_alignment_tab(analysis):
    """Render alignment tab content - nrcdnl94"""
    import plotly.graph_objects as go
    import numpy as np
    
    st.markdown("#### Alignment Istatistikleri")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Hizalanma Orani", "99.1%")
    with col2:
        st.metric("Ortalama Coverage", "102x")
    with col3:
        st.metric("On-Target Orani", "85.3%")
    with col4:
        st.metric("Insert Size (ort.)", "350 bp")
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        chromosomes = [f"chr{i}" for i in range(1, 23)] + ["chrX", "chrY"]
        coverage = [100 + np.random.uniform(-15, 15) for _ in range(24)]
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=chromosomes,
            y=coverage,
            marker_color='#0050A0'
        ))
        fig.update_layout(
            title="Kromozom Bazli Coverage Dagilimi",
            xaxis_title="Kromozom",
            yaxis_title="Coverage (x)",
            template="plotly_white",
            height=350,
            font=dict(family="Inter, sans-serif")
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        insert_sizes = np.random.normal(350, 50, 1000)
        
        fig = go.Figure()
        fig.add_trace(go.Histogram(
            x=insert_sizes,
            nbinsx=50,
            marker_color='#00A7D8'
        ))
        fig.update_layout(
            title="Insert Size Dagilimi",
            xaxis_title="Insert Size (bp)",
            yaxis_title="Frekans",
            template="plotly_white",
            height=350,
            font=dict(family="Inter, sans-serif")
        )
        st.plotly_chart(fig, use_container_width=True)


def render_variants_tab(analysis):
    """Render variants tab content - nrcdnl94"""
    import pandas as pd
    
    st.markdown("#### Varyant Cagirma Sonuclari")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Toplam Varyant", "45,892")
    with col2:
        st.metric("SNV", "42,156")
    with col3:
        st.metric("Indel", "3,736")
    with col4:
        st.metric("Ti/Tv Orani", "2.1")
    
    st.markdown("---")
    st.markdown("#### Onemli Varyantlar")
    
    variants_data = {
        "Gen": ["BRCA1", "TP53", "EGFR", "KRAS", "BRAF"],
        "Pozisyon": ["chr17:43,044,295", "chr17:7,577,538", "chr7:55,174,772", "chr12:25,227,342", "chr7:140,453,136"],
        "Ref": ["A", "G", "T", "G", "A"],
        "Alt": ["G", "A", "G", "A", "T"],
        "Zygosity": ["Heterozigot", "Heterozigot", "Homozigot", "Heterozigot", "Heterozigot"],
        "Klinik Onemi": ["Patojenik", "VUS", "Benign", "Patojenik", "VUS"],
        "VAF": ["48%", "52%", "100%", "45%", "51%"]
    }
    
    df = pd.DataFrame(variants_data)
    st.dataframe(df, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    st.markdown("#### Fonksiyonel Etki Dagilimi")
    
    import plotly.graph_objects as go
    
    labels = ['Missense', 'Synonymous', 'Frameshift', 'Nonsense', 'Splice Site', 'Diger']
    values = [45, 30, 8, 5, 7, 5]
    
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=0.4,
        marker_colors=['#0050A0', '#00A7D8', '#003366', '#E8F4FC', '#64748B', '#94A3B8']
    )])
    fig.update_layout(
        title="Varyant Tiplerine Gore Dagılım",
        template="plotly_white",
        height=350,
        font=dict(family="Inter, sans-serif")
    )
    st.plotly_chart(fig, use_container_width=True)


def render_str_tab(analysis):
    """Render STR profile tab content - nrcdnl94"""
    import pandas as pd
    import plotly.graph_objects as go
    
    st.markdown("#### STR Profil Analizi")
    
    str_data = {
        "Marker": ["D3S1358", "vWA", "D16S539", "CSF1PO", "TPOX", "D8S1179", "D21S11", "D18S51", "D2S441", "D19S433"],
        "Allel 1": [15, 17, 11, 12, 8, 13, 30, 15, 11, 14],
        "Allel 2": [16, 18, 12, 13, 11, 14, 31.2, 17, 14, 15],
        "RFU 1": [8500, 9200, 7800, 8100, 6500, 8900, 9500, 7200, 8800, 9100],
        "RFU 2": [8200, 8900, 7500, 7900, 6200, 8600, 9200, 6900, 8500, 8800]
    }
    
    df = pd.DataFrame(str_data)
    st.dataframe(df, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        markers = str_data["Marker"]
        allel1 = str_data["Allel 1"]
        allel2 = str_data["Allel 2"]
        
        fig = go.Figure()
        fig.add_trace(go.Bar(name='Allel 1', x=markers, y=allel1, marker_color='#0050A0'))
        fig.add_trace(go.Bar(name='Allel 2', x=markers, y=allel2, marker_color='#00A7D8'))
        
        fig.update_layout(
            title="STR Marker Allel Dagilimi",
            xaxis_title="Marker",
            yaxis_title="Allel Degeri",
            barmode='group',
            template="plotly_white",
            height=350,
            font=dict(family="Inter, sans-serif")
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("""
        <div class="summary-card">
            <div class="summary-title">Profil Ozeti</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="summary-item">Toplam Marker: <span class="metric-value">24</span></div>
        <div class="summary-item">Basarili Cagri: <span class="metric-value">24/24 (100%)</span></div>
        <div class="summary-item">Ortalama RFU: <span class="metric-value">8,250</span></div>
        <div class="summary-item">Stutter Orani: <span class="metric-value">< 15%</span></div>
        <div class="summary-item">Profil Kalitesi: <span style="color:#166534; font-weight:600;">Yuksek</span></div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown("""
        <div class="summary-item"><span class="summary-label">Amelogenin:</span> X, Y</div>
        <div class="summary-item"><span class="summary-label">Cinsiyet:</span> Erkek</div>
        <div class="summary-item"><span class="summary-label">Match Probabilitesi:</span> 1 / 10^18</div>
        """, unsafe_allow_html=True)

def render_hero_slider():
    """Render hero slider section (legacy) - nrcdnl94"""
    slides = [
        {
            "title": "29.4 Million CpG Sites",
            "desc": "Full human genome coverage (hg38/GRCh38)"
        },
        {
            "title": "17 Epigenetic Clocks",
            "desc": "5 main + 12 tissue-specific clocks"
        },
        {
            "title": "1,815 Detectable Substances",
            "desc": "From international databases"
        },
        {
            "title": "10,542 Reference Profiles",
            "desc": "From 15 independent datasets"
        }
    ]
    
    cols = st.columns(4)
    for i, slide in enumerate(slides):
        with cols[i]:
            st.markdown(f"""
            <div class="hero-slider" style="padding: 25px;">
                <h3 style="font-size: 1.3rem; margin: 10px 0; color: white;">{slide['title']}</h3>
                <p style="font-size: 0.9rem; opacity: 0.9; color: white;">{slide['desc']}</p>
            </div>
            """, unsafe_allow_html=True)

def render_module_cards():
    """Render UNODC-style module cards grid - nrcdnl94"""
    st.markdown("""
    <style>
    .modules-section-title {
        font-size: 1.4rem;
        font-weight: 600;
        color: #003366;
        margin: 32px 0 16px 0;
        padding-bottom: 12px;
        border-bottom: 2px solid #E8EEF5;
    }
    .modules-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 16px;
        margin: 20px 0;
    }
    .module-card-item {
        background: white;
        border-radius: 8px;
        padding: 20px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.05);
        border: 1px solid #E8EEF5;
        transition: all 0.2s ease;
        cursor: pointer;
    }
    .module-card-item:hover {
        border-color: #0050A0;
        box-shadow: 0 4px 12px rgba(0,80,160,0.12);
        transform: translateY(-2px);
    }
    .module-icon {
        width: 40px;
        height: 40px;
        background: linear-gradient(135deg, #E8F4FC 0%, #D0E8F5 100%);
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-bottom: 12px;
    }
    .module-icon svg {
        width: 24px;
        height: 24px;
        stroke: #0050A0;
    }
    .module-card-title {
        font-size: 0.95rem;
        font-weight: 600;
        color: #003366;
        margin-bottom: 4px;
    }
    .module-card-desc {
        font-size: 0.8rem;
        color: #666666;
        line-height: 1.4;
    }
    .module-open-btn {
        display: inline-block;
        margin-top: 12px;
        font-size: 0.75rem;
        color: #0050A0;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.03em;
    }
    @media (max-width: 768px) {
        .modules-grid {
            grid-template-columns: repeat(2, 1fr);
        }
    }
    </style>
    <h2 class="modules-section-title">Modules and Programs</h2>
    <div class="modules-grid">
        <div class="module-card-item">
            <div class="module-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/>
                </svg>
            </div>
            <div class="module-card-title">Forensic STR Analysis</div>
            <div class="module-card-desc">Short tandem repeat profiling for forensic identification</div>
            <span class="module-open-btn">Open Module</span>
        </div>
        <div class="module-card-item">
            <div class="module-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/>
                </svg>
            </div>
            <div class="module-card-title">NGS Variant Analysis</div>
            <div class="module-card-desc">Next-generation sequencing variant calling and annotation</div>
            <span class="module-open-btn">Open Module</span>
        </div>
        <div class="module-card-item">
            <div class="module-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <circle cx="12" cy="12" r="10"/>
                    <line x1="2" y1="12" x2="22" y2="12"/>
                    <path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/>
                </svg>
            </div>
            <div class="module-card-title">Population Genetics</div>
            <div class="module-card-desc">Ancestry and population structure analysis</div>
            <span class="module-open-btn">Open Module</span>
        </div>
        <div class="module-card-item">
            <div class="module-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M22 12h-4l-3 9L9 3l-3 9H2"/>
                </svg>
            </div>
            <div class="module-card-title">Clinical Genomics</div>
            <div class="module-card-desc">Pharmacogenomics and clinical variant interpretation</div>
            <span class="module-open-btn">Open Module</span>
        </div>
        <div class="module-card-item">
            <div class="module-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                    <polyline points="14 2 14 8 20 8"/>
                    <line x1="16" y1="13" x2="8" y2="13"/>
                    <line x1="16" y1="17" x2="8" y2="17"/>
                </svg>
            </div>
            <div class="module-card-title">Reports and Legal Output</div>
            <div class="module-card-desc">Court-ready forensic reports with chain of custody</div>
            <span class="module-open-btn">Open Module</span>
        </div>
        <div class="module-card-item">
            <div class="module-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <line x1="18" y1="20" x2="18" y2="10"/>
                    <line x1="12" y1="20" x2="12" y2="4"/>
                    <line x1="6" y1="20" x2="6" y2="14"/>
                </svg>
            </div>
            <div class="module-card-title">Data and Statistics</div>
            <div class="module-card-desc">Laboratory performance metrics and analytics</div>
            <span class="module-open-btn">Open Module</span>
        </div>
        <div class="module-card-item">
            <div class="module-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <rect x="3" y="3" width="18" height="18" rx="2" ry="2"/>
                    <line x1="3" y1="9" x2="21" y2="9"/>
                    <line x1="9" y1="21" x2="9" y2="9"/>
                </svg>
            </div>
            <div class="module-card-title">Sample Management</div>
            <div class="module-card-desc">Chain of custody and sample tracking</div>
            <span class="module-open-btn">Open Module</span>
        </div>
        <div class="module-card-item">
            <div class="module-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
                </svg>
            </div>
            <div class="module-card-title">Data Protection</div>
            <div class="module-card-desc">GDPR/KVKK compliant anonymization</div>
            <span class="module-open-btn">Open Module</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_booklet_grid():
    """Render booklet-style module grid (legacy) - nrcdnl94"""
    modules = [
        {"title": "Individual Analysis", "desc": "Epigenetic age calculation"},
        {"title": "Batch Analysis", "desc": "Batch processing"},
        {"title": "Substance Detection", "desc": "1,815 substances"},
        {"title": "Combinations", "desc": "Synergistic effects"},
        {"title": "Chemoinformatics", "desc": "Molecular analysis"},
        {"title": "World Databases", "desc": "GWAS/EWAS"},
        {"title": "PRS Analysis", "desc": "Polygenic risk"},
        {"title": "Reports", "desc": "PDF output"}
    ]
    
    st.markdown('<div class="booklet-grid">', unsafe_allow_html=True)
    
    cols = st.columns(4)
    for i, mod in enumerate(modules):
        with cols[i % 4]:
            st.markdown(f"""
            <div class="booklet-item">
                <h4>{mod['title']}</h4>
                <p>{mod['desc']}</p>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_stats_row():
    """Render statistics row - nrcdnl94"""
    st.markdown("""
    <div class="stats-row">
        <div class="stat-card">
            <span class="number">29.4M</span>
            <span class="label">CpG Sitesi</span>
        </div>
        <div class="stat-card">
            <span class="number">1,815</span>
            <span class="label">Madde</span>
        </div>
        <div class="stat-card">
            <span class="number">10,542</span>
            <span class="label">Profil</span>
        </div>
        <div class="stat-card">
            <span class="number">17</span>
            <span class="label">Saat</span>
        </div>
        <div class="stat-card">
            <span class="number">1.7B+</span>
            <span class="label">Varyant</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_section_divider():
    """Render section divider - nrcdnl94"""
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

def render_footer():
    """Render UNODC-style footer - nrcdnl94"""
    st.markdown("""
    <div class="footer">
        <h3>🧬 EpiClock Platform v4.0</h3>
        <p>DNA Methylation-Based Epigenetic Age Acceleration Analysis</p>
        <div class="copyright">
            <p><strong>Author:</strong> Dr. Nurcan Denli Bayır (nrcdnl94)</p>
            <p>Adli Tıp Uzmanı | Yazılım Mühendisi | Sağlık Hukuku Uzmanı</p>
            <p style="margin-top: 10px;">
                <a href="https://github.com/mortemdulcem" target="_blank">GitHub</a> |
                Copyright © 2024 - All Rights Reserved
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_module_card(icon, title, description, key=None):
    """Render a single module card - nrcdnl94"""
    st.markdown(f"""
    <div class="module-card">
        <span class="icon">{icon}</span>
        <h3>{title}</h3>
        <p>{description}</p>
    </div>
    """, unsafe_allow_html=True)

def render_chart_container(title):
    """Render chart container start - nrcdnl94"""
    st.markdown(f"""
    <div class="chart-container">
        <h4 style="color: #1A3A5C; margin-bottom: 15px; font-weight: 600;">{title}</h4>
    """, unsafe_allow_html=True)

def close_chart_container():
    """Close chart container - nrcdnl94"""
    st.markdown('</div>', unsafe_allow_html=True)

# nrcdnl94 - End of UNODC Theme Module
