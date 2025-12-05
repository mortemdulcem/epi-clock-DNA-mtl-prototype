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

# nrcdnl94 - UNODC Color Palette
UNODC_COLORS = {
    'primary_blue': '#009EDB',      # UN Blue
    'dark_blue': '#1A3A5C',         # Dark Navy
    'light_blue': '#4DB8E8',        # Light Blue
    'accent_blue': '#0072BC',       # Accent Blue
    'gold': '#FFD100',              # UN Gold
    'white': '#FFFFFF',
    'light_gray': '#F5F7FA',
    'dark_gray': '#333333',
    'text_gray': '#666666',
    'success': '#28A745',
    'warning': '#FFC107',
    'danger': '#DC3545',
    'info': '#17A2B8'
}

def apply_unodc_theme():
    """Apply UNODC-style professional theme to the app - nrcdnl94"""
    st.markdown("""
    <style>
    /* nrcdnl94 - UNODC Theme CSS */
    
    /* Import Professional Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&family=Open+Sans:wght@300;400;600;700&display=swap');
    
    /* Main App Container */
    .stApp {
        background: linear-gradient(135deg, #F5F7FA 0%, #E8EEF5 100%);
        font-family: 'Roboto', 'Open Sans', sans-serif;
    }
    
    /* Hide Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Sidebar Styling - UN Blue */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1A3A5C 0%, #0D2137 100%);
        border-right: 3px solid #009EDB;
    }
    
    [data-testid="stSidebar"] * {
        color: #FFFFFF !important;
    }
    
    [data-testid="stSidebar"] .stSelectbox label,
    [data-testid="stSidebar"] .stRadio label {
        color: #4DB8E8 !important;
        font-weight: 500;
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

def render_main_header():
    """Render UNODC-style main header - nrcdnl94"""
    st.markdown("""
    <div class="main-header">
        <div class="un-badge">
            <span style="font-size: 2.5rem;">🧬</span>
            <span style="font-size: 1.5rem; font-weight: 700;">EpiClock</span>
        </div>
        <h1>DNA Methylation Epigenetic Age Analysis Platform</h1>
        <p>Computational Forensics | Molecular Toxicology | Epigenetic Chronology</p>
        <p style="font-size: 0.9rem; opacity: 0.7; margin-top: 15px;">
            Author: Dr. Nurcan Denli Bayır (nrcdnl94) | Copyright © 2024
        </p>
    </div>
    """, unsafe_allow_html=True)

def render_hero_slider():
    """Render hero slider section - nrcdnl94"""
    slides = [
        {
            "icon": "🔬",
            "title": "29.4 Milyon CpG Sitesi",
            "desc": "Tam insan genomu kapsama (hg38/GRCh38)"
        },
        {
            "icon": "⏰",
            "title": "17 Epigenetik Saat",
            "desc": "5 ana + 12 doku-spesifik saat"
        },
        {
            "icon": "💊",
            "title": "1,815 Tespit Edilebilir Madde",
            "desc": "Uluslararası veritabanlarından"
        },
        {
            "icon": "📊",
            "title": "10,542 Referans Profil",
            "desc": "15 bağımsız veri setinden"
        }
    ]
    
    cols = st.columns(4)
    for i, slide in enumerate(slides):
        with cols[i]:
            st.markdown(f"""
            <div class="hero-slider" style="padding: 25px;">
                <span style="font-size: 3rem;">{slide['icon']}</span>
                <h3 style="font-size: 1.3rem; margin: 10px 0;">{slide['title']}</h3>
                <p style="font-size: 0.9rem; opacity: 0.9;">{slide['desc']}</p>
            </div>
            """, unsafe_allow_html=True)

def render_booklet_grid():
    """Render booklet-style module grid - nrcdnl94"""
    modules = [
        {"icon": "🧬", "title": "Bireysel Analiz", "desc": "Epigenetik yaş hesaplama"},
        {"icon": "📊", "title": "Toplu Analiz", "desc": "Batch işleme"},
        {"icon": "🔬", "title": "Madde Tespiti", "desc": "1,815 madde"},
        {"icon": "💊", "title": "Kombinasyonlar", "desc": "Sinerjik etkiler"},
        {"icon": "🧪", "title": "Chemoinformatics", "desc": "Moleküler analiz"},
        {"icon": "🌐", "title": "Dünya Veritabanları", "desc": "GWAS/EWAS"},
        {"icon": "📈", "title": "PRS Analizi", "desc": "Poligenik risk"},
        {"icon": "📋", "title": "Raporlar", "desc": "PDF çıktı"}
    ]
    
    st.markdown('<div class="booklet-grid">', unsafe_allow_html=True)
    
    cols = st.columns(4)
    for i, mod in enumerate(modules):
        with cols[i % 4]:
            st.markdown(f"""
            <div class="booklet-item">
                <span class="icon">{mod['icon']}</span>
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
