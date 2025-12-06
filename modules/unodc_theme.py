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
    """Render UNODC-style main header - clean Tailwind-inspired design - nrcdnl94"""
    st.markdown("""
    <style>
    .unodc-page-header {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 8px;
        padding: 16px 20px;
        margin-bottom: 20px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    .unodc-page-header-content {
        display: flex;
        align-items: center;
        justify-content: space-between;
        flex-wrap: wrap;
        gap: 12px;
    }
    .unodc-page-title {
        font-size: 1.1rem;
        font-weight: 600;
        color: #0050A0;
        margin: 0;
    }
    .unodc-page-subtitle {
        font-size: 0.75rem;
        color: #64748B;
        margin: 4px 0 0 0;
    }
    .unodc-header-actions {
        display: flex;
        gap: 8px;
    }
    .unodc-btn-primary {
        background: #0050A0;
        color: white;
        border: 1px solid #0050A0;
        padding: 6px 14px;
        border-radius: 4px;
        font-size: 0.75rem;
        font-weight: 500;
        cursor: pointer;
        transition: all 0.2s;
    }
    .unodc-btn-primary:hover {
        background: #003D7A;
    }
    .unodc-btn-secondary {
        background: white;
        color: #475569;
        border: 1px solid #CBD5E1;
        padding: 6px 14px;
        border-radius: 4px;
        font-size: 0.75rem;
        font-weight: 500;
        cursor: pointer;
        transition: all 0.2s;
    }
    .unodc-btn-secondary:hover {
        border-color: #0050A0;
        color: #0050A0;
    }
    </style>
    <div class="unodc-page-header">
        <div class="unodc-page-header-content">
            <div>
                <h1 class="unodc-page-title">Dashboard - Ulusal DNA Analiz Sistemi</h1>
                <p class="unodc-page-subtitle">
                    Adli tip, klinik genetik ve populasyon genetigi icin ulusal duzeyde DNA analiz ve raporlama altyapisi.
                </p>
            </div>
            <div class="unodc-header-actions">
                <span class="unodc-btn-primary">Yeni Analiz Baslat</span>
                <span class="unodc-btn-secondary">Gelismis Arama</span>
            </div>
        </div>
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
    """Render recent analyses table - Tailwind-inspired - nrcdnl94"""
    st.markdown("""
    <style>
    .analyses-section {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 8px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }
    .analyses-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 12px 20px;
        border-bottom: 1px solid #E2E8F0;
    }
    .analyses-title {
        font-size: 0.875rem;
        font-weight: 600;
        color: #334155;
        margin: 0;
    }
    .analyses-view-all {
        font-size: 0.75rem;
        color: #0050A0;
        text-decoration: none;
        cursor: pointer;
    }
    .analyses-view-all:hover {
        text-decoration: underline;
    }
    .analyses-table {
        width: 100%;
        border-collapse: collapse;
        font-size: 0.75rem;
    }
    .analyses-table thead {
        background: #F8FAFC;
        border-bottom: 1px solid #E2E8F0;
    }
    .analyses-table th {
        padding: 8px 20px;
        text-align: left;
        font-weight: 600;
        color: #64748B;
        font-size: 0.7rem;
        text-transform: uppercase;
        letter-spacing: 0.03em;
    }
    .analyses-table th:last-child {
        text-align: right;
    }
    .analyses-table td {
        padding: 10px 20px;
        color: #334155;
        border-bottom: 1px solid #F1F5F9;
    }
    .analyses-table td:last-child {
        text-align: right;
    }
    .analyses-table tr:last-child td {
        border-bottom: none;
    }
    .status-badge {
        display: inline-flex;
        align-items: center;
        padding: 2px 8px;
        border-radius: 9999px;
        font-size: 0.65rem;
        font-weight: 500;
    }
    .status-completed {
        background: #F0FDF4;
        color: #166534;
        border: 1px solid #BBF7D0;
    }
    .status-inprogress {
        background: #FEFCE8;
        color: #A16207;
        border: 1px solid #FEF08A;
    }
    .status-qc {
        background: #FEF2F2;
        color: #DC2626;
        border: 1px solid #FECACA;
    }
    .detail-link {
        color: #0050A0;
        font-size: 0.7rem;
        text-decoration: none;
        cursor: pointer;
    }
    .detail-link:hover {
        text-decoration: underline;
    }
    </style>
    <div class="analyses-section">
        <div class="analyses-header">
            <h2 class="analyses-title">Son Analizler</h2>
            <span class="analyses-view-all">Tumunu Gor</span>
        </div>
        <table class="analyses-table">
            <thead>
                <tr>
                    <th>Ornek ID</th>
                    <th>Tur</th>
                    <th>Modul</th>
                    <th>Durum</th>
                    <th>Tarih</th>
                    <th>Islem</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>2025-STR-00123</td>
                    <td>Kan</td>
                    <td>STR / Adli</td>
                    <td><span class="status-badge status-completed">Tamamlandi</span></td>
                    <td>06.12.2025</td>
                    <td><span class="detail-link">Detay</span></td>
                </tr>
                <tr>
                    <td>2025-NGS-00456</td>
                    <td>Tam Kan</td>
                    <td>NGS</td>
                    <td><span class="status-badge status-inprogress">Devam Ediyor</span></td>
                    <td>05.12.2025</td>
                    <td><span class="detail-link">Detay</span></td>
                </tr>
                <tr>
                    <td>2025-CLN-00078</td>
                    <td>DNA Ekstrakt</td>
                    <td>Klinik Genetik</td>
                    <td><span class="status-badge status-qc">QC Gerekli</span></td>
                    <td>04.12.2025</td>
                    <td><span class="detail-link">Detay</span></td>
                </tr>
                <tr>
                    <td>2025-EPI-00891</td>
                    <td>Salya</td>
                    <td>Epigenetik Yas</td>
                    <td><span class="status-badge status-completed">Tamamlandi</span></td>
                    <td>03.12.2025</td>
                    <td><span class="detail-link">Detay</span></td>
                </tr>
            </tbody>
        </table>
    </div>
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
