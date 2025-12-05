# nrcdnl94
# EpiClock Platform - # nrcdnl94

"""
EpiClock Professional Theme Module
Prezi Biology Concept - Academic-Grade Scientific Visualization

Author: Dr. Nurcan Denli Bayır, M.D., Ph.D., M.Sc., J.D.
Version: 4.0.0
"""

import streamlit as st
from datetime import datetime
import pytz

EPICLOCK_VERSION = "4.0.0"
BUILD_DATE = "2025-12-01"
LAST_UPDATE = "2025-12-01 14:30:00"

def get_last_update_timestamp():
    """Get formatted last update timestamp in Turkish timezone"""
    turkey_tz = pytz.timezone('Europe/Istanbul')
    now = datetime.now(turkey_tz)
    return now.strftime("%d.%m.%Y %H:%M:%S")

def render_update_badge():
    """Render the last system update badge with live timestamp"""
    turkey_tz = pytz.timezone('Europe/Istanbul')
    now = datetime.now(turkey_tz)
    timestamp = now.strftime("%d.%m.%Y %H:%M:%S")
    
    st.markdown(f"""
    <div class="update-badge-container">
        <div class="update-badge">
            <span class="update-icon">🔄</span>
            <span class="update-text">Son Güncelleme: <strong>{timestamp}</strong></span>
            <span class="update-version">v{EPICLOCK_VERSION}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

def inject_professional_css():
    """Inject professional Prezi Biology-style CSS"""
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;500;600;700&family=Source+Sans+Pro:wght@300;400;600;700&family=Fira+Code:wght@400;500&display=swap');
        
        :root {
            --primary-dna: #0d4f4f;
            --secondary-helix: #1a7a7a;
            --accent-nucleotide: #2dd4bf;
            --highlight-gene: #5eead4;
            --warm-cytosine: #fbbf24;
            --alert-adenine: #ef4444;
            --background-cell: #f0fdfa;
            --surface-membrane: #ffffff;
            --text-genome: #134e4a;
            --text-light: #5f7472;
            --border-chromosome: #99f6e4;
            --gradient-bio: linear-gradient(135deg, #0d4f4f 0%, #1a7a7a 50%, #2dd4bf 100%);
            --shadow-bio: 0 8px 32px rgba(13, 79, 79, 0.15);
        }
        
        /* ============================================
           UPDATE BADGE - SYSTEM STATUS
           ============================================ */
        
        .update-badge-container {
            position: fixed;
            bottom: 20px;
            right: 20px;
            z-index: 9999;
        }
        
        .update-badge {
            background: linear-gradient(135deg, #0d4f4f 0%, #1a7a7a 100%);
            color: white;
            padding: 12px 20px;
            border-radius: 50px;
            font-family: 'Source Sans Pro', sans-serif;
            font-size: 0.85rem;
            display: flex;
            align-items: center;
            gap: 10px;
            box-shadow: 0 4px 20px rgba(13, 79, 79, 0.3);
            border: 2px solid #2dd4bf;
            animation: badgePulse 3s ease-in-out infinite;
        }
        
        .update-icon {
            font-size: 1.1rem;
            animation: iconSpin 4s linear infinite;
        }
        
        .update-version {
            background: rgba(45, 212, 191, 0.3);
            padding: 3px 10px;
            border-radius: 15px;
            font-weight: 600;
            font-size: 0.75rem;
        }
        
        @keyframes badgePulse {
            0%, 100% { box-shadow: 0 4px 20px rgba(13, 79, 79, 0.3); }
            50% { box-shadow: 0 4px 30px rgba(45, 212, 191, 0.5); }
        }
        
        @keyframes iconSpin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        /* ============================================
           PREZI BIOLOGY CONCEPT - BASE STYLES
           ============================================ */
        
        .stApp {
            background: linear-gradient(180deg, 
                #f0fdfa 0%, 
                #ccfbf1 30%, 
                #e0f2fe 70%, 
                #f0fdfa 100%) !important;
        }
        
        .main .block-container {
            background: transparent !important;
            padding: 2rem 3rem;
            max-width: 1400px;
        }
        
        /* ============================================
           SIDEBAR - SCIENTIFIC NAVIGATION
           ============================================ */
        
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #0d4f4f 0%, #134e4a 100%) !important;
            border-right: 3px solid var(--accent-nucleotide);
        }
        
        [data-testid="stSidebar"] * {
            color: #ffffff !important;
        }
        
        [data-testid="stSidebar"] .stRadio label {
            background: rgba(45, 212, 191, 0.1);
            padding: 12px 18px;
            border-radius: 12px;
            margin: 5px 0;
            transition: all 0.3s ease;
            border-left: 4px solid transparent;
            font-weight: 500;
        }
        
        [data-testid="stSidebar"] .stRadio label:hover {
            background: rgba(45, 212, 191, 0.25);
            border-left-color: var(--accent-nucleotide);
        }
        
        /* ============================================
           HEADER - DNA DOUBLE HELIX BRANDING
           ============================================ */
        
        .epiclock-hero {
            background: var(--gradient-bio);
            padding: 3rem 2rem;
            border-radius: 20px;
            margin-bottom: 2rem;
            position: relative;
            overflow: hidden;
            box-shadow: var(--shadow-bio);
        }
        
        .epiclock-hero::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M30 0L30 60M0 30L60 30' stroke='%23ffffff' stroke-width='0.5' opacity='0.1'/%3E%3C/svg%3E");
            opacity: 0.3;
        }
        
        .epiclock-title {
            font-family: 'Playfair Display', Georgia, serif;
            font-size: 3.5rem;
            font-weight: 700;
            color: #ffffff;
            text-align: center;
            margin-bottom: 0.5rem;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
            position: relative;
            z-index: 1;
            letter-spacing: 3px;
        }
        
        .epiclock-subtitle {
            font-family: 'Source Sans Pro', -apple-system, sans-serif;
            font-size: 1.3rem;
            color: rgba(255, 255, 255, 0.9);
            text-align: center;
            font-weight: 300;
            position: relative;
            z-index: 1;
            letter-spacing: 1px;
        }
        
        .epiclock-badge {
            display: inline-block;
            background: rgba(255, 255, 255, 0.2);
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 0.85rem;
            color: #ffffff;
            margin: 1rem auto 0;
            font-family: 'Source Sans Pro', sans-serif;
            border: 1px solid rgba(255, 255, 255, 0.3);
        }
        
        /* ============================================
           DNA HELIX ANIMATION
           ============================================ */
        
        .dna-helix-container {
            width: 100%;
            height: 120px;
            display: flex;
            justify-content: center;
            align-items: center;
            margin: 1rem 0;
            position: relative;
        }
        
        .dna-helix-animated {
            width: 300px;
            height: 100px;
            position: relative;
            perspective: 1000px;
        }
        
        .dna-strand {
            position: absolute;
            width: 100%;
            height: 100%;
            animation: dnaRotate 8s linear infinite;
            transform-style: preserve-3d;
        }
        
        .nucleotide-base {
            position: absolute;
            width: 16px;
            height: 16px;
            border-radius: 50%;
            box-shadow: 0 0 15px currentColor;
        }
        
        .adenine { background: #e74c3c; color: #e74c3c; }
        .thymine { background: #3498db; color: #3498db; }
        .guanine { background: #2ecc71; color: #2ecc71; }
        .cytosine { background: #f39c12; color: #f39c12; }
        
        .base-pair-bond {
            position: absolute;
            height: 3px;
            background: linear-gradient(90deg, #7fcdbb, #ffffff, #7fcdbb);
            box-shadow: 0 0 8px rgba(127, 205, 187, 0.5);
        }
        
        @keyframes dnaRotate {
            0% { transform: rotateY(0deg); }
            100% { transform: rotateY(360deg); }
        }
        
        @keyframes nucleotidePulse {
            0%, 100% { transform: scale(1); opacity: 1; }
            50% { transform: scale(1.15); opacity: 0.8; }
        }
        
        /* ============================================
           SECTION CARDS - BIOLOGY CONCEPT
           ============================================ */
        
        .bio-card {
            background: var(--surface-membrane);
            border-radius: 16px;
            padding: 1.5rem;
            margin: 1rem 0;
            box-shadow: 0 2px 12px rgba(30, 58, 95, 0.08);
            border: 1px solid var(--border-chromosome);
            transition: all 0.3s ease;
        }
        
        .bio-card:hover {
            box-shadow: 0 8px 30px rgba(30, 58, 95, 0.15);
            transform: translateY(-2px);
            border-color: var(--secondary-helix);
        }
        
        .bio-card-header {
            font-family: 'Playfair Display', serif;
            font-size: 1.5rem;
            font-weight: 600;
            color: var(--primary-dna);
            margin-bottom: 1rem;
            padding-bottom: 0.75rem;
            border-bottom: 2px solid var(--accent-nucleotide);
        }
        
        /* ============================================
           METRIC CARDS - SCIENTIFIC STATS
           ============================================ */
        
        .metric-card-bio {
            background: linear-gradient(135deg, var(--primary-dna) 0%, var(--secondary-helix) 100%);
            border-radius: 15px;
            padding: 1.5rem;
            color: #ffffff;
            text-align: center;
            box-shadow: var(--shadow-bio);
            transition: all 0.3s ease;
        }
        
        .metric-card-bio:hover {
            transform: translateY(-3px) scale(1.02);
            box-shadow: 0 12px 40px rgba(30, 58, 95, 0.25);
        }
        
        .metric-value {
            font-family: 'Playfair Display', serif;
            font-size: 2.5rem;
            font-weight: 700;
            color: #ffffff;
            margin-bottom: 0.25rem;
        }
        
        .metric-label {
            font-family: 'Source Sans Pro', sans-serif;
            font-size: 0.95rem;
            color: rgba(255, 255, 255, 0.85);
            font-weight: 400;
        }
        
        /* ============================================
           SCIENTIFIC INFO BOXES
           ============================================ */
        
        .info-box-bio {
            background: linear-gradient(135deg, #e8f4f8 0%, #f0f9ff 100%);
            border-left: 4px solid var(--secondary-helix);
            padding: 1.25rem;
            border-radius: 0 12px 12px 0;
            margin: 1rem 0;
            color: var(--text-genome);
            font-family: 'Source Sans Pro', sans-serif;
        }
        
        .warning-box-bio {
            background: linear-gradient(135deg, #fef5e7 0%, #fdf2e3 100%);
            border-left: 4px solid var(--warm-cytosine);
            padding: 1.25rem;
            border-radius: 0 12px 12px 0;
            margin: 1rem 0;
            color: #8b5a00;
        }
        
        .success-box-bio {
            background: linear-gradient(135deg, #e8f8f0 0%, #f0fdf4 100%);
            border-left: 4px solid #2ecc71;
            padding: 1.25rem;
            border-radius: 0 12px 12px 0;
            margin: 1rem 0;
            color: #1e8449;
        }
        
        .alert-box-bio {
            background: linear-gradient(135deg, #fdeaea 0%, #fef2f2 100%);
            border-left: 4px solid var(--alert-adenine);
            padding: 1.25rem;
            border-radius: 0 12px 12px 0;
            margin: 1rem 0;
            color: #922b21;
        }
        
        /* ============================================
           TABS - CHROMOSOME NAVIGATION
           ============================================ */
        
        .stTabs [data-baseweb="tab-list"] {
            gap: 6px;
            background: transparent;
            border-bottom: 2px solid var(--border-chromosome);
            padding-bottom: 0;
        }
        
        .stTabs [data-baseweb="tab"] {
            background: var(--surface-membrane);
            border: 1px solid var(--border-chromosome);
            border-bottom: none;
            border-radius: 12px 12px 0 0;
            padding: 14px 28px;
            color: var(--text-genome) !important;
            font-family: 'Source Sans Pro', sans-serif;
            font-weight: 500;
            transition: all 0.3s ease;
        }
        
        .stTabs [data-baseweb="tab"]:hover {
            background: linear-gradient(135deg, #e8f4f8 0%, #f0f9ff 100%);
            border-color: var(--secondary-helix);
        }
        
        .stTabs [aria-selected="true"] {
            background: var(--gradient-bio) !important;
            border-color: var(--primary-dna) !important;
            color: #ffffff !important;
            font-weight: 600;
            box-shadow: 0 -2px 10px rgba(30, 58, 95, 0.2);
        }
        
        /* ============================================
           BUTTONS - MOLECULAR DESIGN
           ============================================ */
        
        .stButton > button {
            background: var(--gradient-bio);
            border: none;
            color: #ffffff;
            border-radius: 10px;
            padding: 0.75rem 2rem;
            font-family: 'Source Sans Pro', sans-serif;
            font-weight: 600;
            font-size: 1rem;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(30, 58, 95, 0.2);
        }
        
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(30, 58, 95, 0.3);
        }
        
        .stButton > button:active {
            transform: translateY(0);
        }
        
        /* ============================================
           DATA TABLES - GENOMIC DATA DISPLAY
           ============================================ */
        
        .stDataFrame {
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 2px 12px rgba(30, 58, 95, 0.08);
        }
        
        .stDataFrame table {
            font-family: 'Source Sans Pro', sans-serif;
        }
        
        .stDataFrame thead tr th {
            background: var(--primary-dna) !important;
            color: #ffffff !important;
            font-weight: 600;
            padding: 12px 16px;
        }
        
        .stDataFrame tbody tr:hover {
            background: rgba(127, 205, 187, 0.1);
        }
        
        /* ============================================
           EXPANDERS - GENE DETAILS
           ============================================ */
        
        .streamlit-expanderHeader {
            background: linear-gradient(135deg, #f8fafc 0%, #e8f4f8 100%);
            border: 1px solid var(--border-chromosome);
            border-radius: 10px;
            padding: 1rem;
            font-family: 'Source Sans Pro', sans-serif;
            font-weight: 600;
            color: var(--primary-dna);
            transition: all 0.3s ease;
        }
        
        .streamlit-expanderHeader:hover {
            background: linear-gradient(135deg, #e8f4f8 0%, #d0e8f0 100%);
            border-color: var(--secondary-helix);
        }
        
        .streamlit-expanderContent {
            background: var(--surface-membrane);
            border: 1px solid var(--border-chromosome);
            border-top: none;
            border-radius: 0 0 10px 10px;
            padding: 1.5rem;
        }
        
        /* ============================================
           SELECT BOX & INPUTS - SCIENTIFIC FORMS
           ============================================ */
        
        .stSelectbox label, .stMultiSelect label, .stTextInput label {
            font-family: 'Source Sans Pro', sans-serif;
            font-weight: 600;
            color: var(--primary-dna);
            margin-bottom: 0.5rem;
        }
        
        .stSelectbox > div > div, .stMultiSelect > div > div {
            border-color: var(--border-chromosome);
            border-radius: 10px;
            transition: all 0.3s ease;
        }
        
        .stSelectbox > div > div:focus-within, .stMultiSelect > div > div:focus-within {
            border-color: var(--secondary-helix);
            box-shadow: 0 0 0 3px rgba(61, 126, 166, 0.15);
        }
        
        /* ============================================
           CHARTS - BIOLOGICAL VISUALIZATION
           ============================================ */
        
        .js-plotly-plot {
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 2px 12px rgba(30, 58, 95, 0.08);
        }
        
        /* ============================================
           FOOTER - ACADEMIC ATTRIBUTION
           ============================================ */
        
        .academic-footer {
            background: linear-gradient(135deg, var(--primary-dna) 0%, #2c5282 100%);
            padding: 2rem;
            border-radius: 16px;
            margin-top: 3rem;
            color: #ffffff;
            text-align: center;
            font-family: 'Source Sans Pro', sans-serif;
        }
        
        .academic-footer-title {
            font-family: 'Playfair Display', serif;
            font-size: 1.3rem;
            font-weight: 600;
            margin-bottom: 1rem;
            color: var(--accent-nucleotide);
        }
        
        .academic-footer-text {
            font-size: 0.95rem;
            color: rgba(255, 255, 255, 0.85);
            line-height: 1.6;
        }
        
        .update-timestamp {
            background: rgba(255, 255, 255, 0.1);
            padding: 0.5rem 1.5rem;
            border-radius: 20px;
            display: inline-block;
            margin-top: 1rem;
            font-size: 0.85rem;
            color: var(--accent-nucleotide);
            border: 1px solid rgba(127, 205, 187, 0.3);
        }
        
        /* ============================================
           STICKER BADGES - CANVA STYLE
           ============================================ */
        
        .sticker-badge {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
            padding: 8px 16px;
            border-radius: 25px;
            font-family: 'Source Sans Pro', sans-serif;
            font-weight: 600;
            font-size: 0.9rem;
            color: var(--primary-dna);
            box-shadow: 0 2px 10px rgba(30, 58, 95, 0.1);
            border: 1px solid var(--border-chromosome);
            margin: 4px;
        }
        
        .sticker-badge-success {
            background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
            color: #155724;
            border-color: #28a745;
        }
        
        .sticker-badge-warning {
            background: linear-gradient(135deg, #fff3cd 0%, #ffeeba 100%);
            color: #856404;
            border-color: #ffc107;
        }
        
        .sticker-badge-info {
            background: linear-gradient(135deg, #cce5ff 0%, #b8daff 100%);
            color: #004085;
            border-color: #007bff;
        }
        
        .sticker-badge-danger {
            background: linear-gradient(135deg, #f8d7da 0%, #f5c6cb 100%);
            color: #721c24;
            border-color: #dc3545;
        }
        
        /* ============================================
           BIOLOGICAL ICONS
           ============================================ */
        
        .bio-icon {
            font-size: 2rem;
            margin-bottom: 0.5rem;
            display: block;
        }
        
        .bio-icon-small {
            font-size: 1.2rem;
            vertical-align: middle;
            margin-right: 8px;
        }
        
        /* ============================================
           RESPONSIVE DESIGN
           ============================================ */
        
        @media (max-width: 768px) {
            .epiclock-title {
                font-size: 2.2rem;
            }
            
            .epiclock-subtitle {
                font-size: 1rem;
            }
            
            .main .block-container {
                padding: 1rem;
            }
            
            .bio-card {
                padding: 1rem;
            }
            
            .metric-value {
                font-size: 1.8rem;
            }
        }
        
        /* ============================================
           SCROLLBAR - BIOLOGY THEME
           ============================================ */
        
        ::-webkit-scrollbar {
            width: 10px;
            height: 10px;
        }
        
        ::-webkit-scrollbar-track {
            background: #f1f1f1;
            border-radius: 5px;
        }
        
        ::-webkit-scrollbar-thumb {
            background: var(--secondary-helix);
            border-radius: 5px;
        }
        
        ::-webkit-scrollbar-thumb:hover {
            background: var(--primary-dna);
        }
        
        /* ============================================
           LOADING ANIMATION
           ============================================ */
        
        @keyframes dnaLoader {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        .dna-loader {
            width: 60px;
            height: 60px;
            border: 4px solid var(--accent-nucleotide);
            border-top: 4px solid var(--primary-dna);
            border-radius: 50%;
            animation: dnaLoader 1s linear infinite;
            margin: 2rem auto;
        }
    </style>
    """, unsafe_allow_html=True)


def render_hero_section():
    """Render professional hero section with DNA animation"""
    st.markdown("""
    <div class="epiclock-hero">
        <div class="dna-helix-container">
            <svg width="400" height="100" viewBox="0 0 400 100" class="dna-helix-svg">
                <defs>
                    <linearGradient id="helixGrad1" x1="0%" y1="0%" x2="100%" y2="0%">
                        <stop offset="0%" style="stop-color:#7fcdbb;stop-opacity:1" />
                        <stop offset="100%" style="stop-color:#ffffff;stop-opacity:1" />
                    </linearGradient>
                    <linearGradient id="helixGrad2" x1="0%" y1="0%" x2="100%" y2="0%">
                        <stop offset="0%" style="stop-color:#c7e9b4;stop-opacity:1" />
                        <stop offset="100%" style="stop-color:#ffffff;stop-opacity:1" />
                    </linearGradient>
                </defs>
                
                <!-- DNA Strand 1 -->
                <path d="M 20,50 Q 60,20 100,50 T 180,50 T 260,50 T 340,50 T 420,50" 
                      stroke="url(#helixGrad1)" stroke-width="4" fill="none" opacity="0.9">
                    <animate attributeName="d" 
                             values="M 20,50 Q 60,20 100,50 T 180,50 T 260,50 T 340,50 T 420,50;
                                     M 20,50 Q 60,80 100,50 T 180,50 T 260,50 T 340,50 T 420,50;
                                     M 20,50 Q 60,20 100,50 T 180,50 T 260,50 T 340,50 T 420,50"
                             dur="3s" repeatCount="indefinite"/>
                </path>
                
                <!-- DNA Strand 2 -->
                <path d="M 20,50 Q 60,80 100,50 T 180,50 T 260,50 T 340,50 T 420,50" 
                      stroke="url(#helixGrad2)" stroke-width="4" fill="none" opacity="0.9">
                    <animate attributeName="d" 
                             values="M 20,50 Q 60,80 100,50 T 180,50 T 260,50 T 340,50 T 420,50;
                                     M 20,50 Q 60,20 100,50 T 180,50 T 260,50 T 340,50 T 420,50;
                                     M 20,50 Q 60,80 100,50 T 180,50 T 260,50 T 340,50 T 420,50"
                             dur="3s" repeatCount="indefinite"/>
                </path>
                
                <!-- Base pairs / Nucleotides -->
                <circle cx="50" cy="35" r="6" fill="#e74c3c" opacity="0.9">
                    <animate attributeName="cy" values="35;65;35" dur="3s" repeatCount="indefinite"/>
                </circle>
                <circle cx="50" cy="65" r="6" fill="#3498db" opacity="0.9">
                    <animate attributeName="cy" values="65;35;65" dur="3s" repeatCount="indefinite"/>
                </circle>
                
                <circle cx="130" cy="35" r="6" fill="#2ecc71" opacity="0.9">
                    <animate attributeName="cy" values="35;65;35" dur="3s" repeatCount="indefinite" begin="0.3s"/>
                </circle>
                <circle cx="130" cy="65" r="6" fill="#f39c12" opacity="0.9">
                    <animate attributeName="cy" values="65;35;65" dur="3s" repeatCount="indefinite" begin="0.3s"/>
                </circle>
                
                <circle cx="210" cy="35" r="6" fill="#e74c3c" opacity="0.9">
                    <animate attributeName="cy" values="35;65;35" dur="3s" repeatCount="indefinite" begin="0.6s"/>
                </circle>
                <circle cx="210" cy="65" r="6" fill="#3498db" opacity="0.9">
                    <animate attributeName="cy" values="65;35;65" dur="3s" repeatCount="indefinite" begin="0.6s"/>
                </circle>
                
                <circle cx="290" cy="35" r="6" fill="#2ecc71" opacity="0.9">
                    <animate attributeName="cy" values="35;65;35" dur="3s" repeatCount="indefinite" begin="0.9s"/>
                </circle>
                <circle cx="290" cy="65" r="6" fill="#f39c12" opacity="0.9">
                    <animate attributeName="cy" values="65;35;65" dur="3s" repeatCount="indefinite" begin="0.9s"/>
                </circle>
                
                <circle cx="370" cy="35" r="6" fill="#e74c3c" opacity="0.9">
                    <animate attributeName="cy" values="35;65;35" dur="3s" repeatCount="indefinite" begin="1.2s"/>
                </circle>
                <circle cx="370" cy="65" r="6" fill="#3498db" opacity="0.9">
                    <animate attributeName="cy" values="65;35;65" dur="3s" repeatCount="indefinite" begin="1.2s"/>
                </circle>
            </svg>
        </div>
        
        <h1 class="epiclock-title">🧬 EpiClock</h1>
        <p class="epiclock-subtitle">DNA Metilasyon Tabanlı Epigenetik Yaş İvmelenmesi Analiz Platformu</p>
        <div style="text-align: center;">
            <span class="epiclock-badge">📊 Akademik Araştırma Platformu • v2.0.0</span>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_academic_footer():
    """Render professional academic footer with timestamp"""
    timestamp = get_last_update_timestamp()
    
    st.markdown(f"""
    <style>
    .academic-footer-custom {{
        background: linear-gradient(135deg, #5D4037 0%, #4E342E 100%);
        padding: 1.5rem;
        border-radius: 10px;
        margin-top: 2rem;
        text-align: center;
        border-top: 3px solid #CD853F;
    }}
    .academic-footer-custom .footer-title {{
        color: #FFE4B5;
        font-size: 1.1rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }}
    .academic-footer-custom .footer-text {{
        color: #FFF8DC;
        font-size: 0.9rem;
        line-height: 1.6;
    }}
    .academic-footer-custom .footer-timestamp {{
        color: #CD853F;
        font-size: 0.85rem;
        margin-top: 0.5rem;
        font-style: italic;
    }}
    </style>
    <div class="academic-footer-custom">
        <div class="footer-title">EpiClock Prototype - Akademik Arastirma Platformu</div>
        <div class="footer-text">
            <strong>Arastirmaci:</strong> Dr. Nurcan Denli Bayir, M.D., Ph.D., M.Sc., J.D.<br>
            <strong>Platform:</strong> DNA Metilasyon Tabanli Epigenetik Yas Analizi<br>
            <strong>Versiyon:</strong> {EPICLOCK_VERSION} | <strong>Build:</strong> {BUILD_DATE}<br>
            Bu platform, bagimlilik arastirmalarinda epigenetik yas ivmelenmesini analiz etmek icin 
            tasarlanmis akademik bir arastirma aracidir.
        </div>
        <div class="footer-timestamp">
            Son Guncelleme: {timestamp} (Turkiye Saati)
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_metric_card(icon: str, value: str, label: str, color: str = "default"):
    """Render a professional metric card"""
    bg_colors = {
        "default": "linear-gradient(135deg, #1e3a5f 0%, #3d7ea6 100%)",
        "success": "linear-gradient(135deg, #27ae60 0%, #2ecc71 100%)",
        "warning": "linear-gradient(135deg, #f39c12 0%, #e67e22 100%)",
        "danger": "linear-gradient(135deg, #c0392b 0%, #e74c3c 100%)",
        "info": "linear-gradient(135deg, #2980b9 0%, #3498db 100%)"
    }
    
    bg = bg_colors.get(color, bg_colors["default"])
    
    st.markdown(f"""
    <div class="metric-card-bio" style="background: {bg};">
        <span class="bio-icon">{icon}</span>
        <div class="metric-value">{value}</div>
        <div class="metric-label">{label}</div>
    </div>
    """, unsafe_allow_html=True)


def render_sticker_badge(text: str, badge_type: str = "default"):
    """Render Canva-style sticker badge"""
    type_class = f"sticker-badge-{badge_type}" if badge_type != "default" else "sticker-badge"
    return f'<span class="{type_class}">{text}</span>'


def render_bio_card(title: str, content: str, icon: str = "🧬"):
    """Render a biology-themed card"""
    st.markdown(f"""
    <div class="bio-card">
        <div class="bio-card-header">
            <span class="bio-icon-small">{icon}</span>{title}
        </div>
        <div class="bio-card-content">{content}</div>
    </div>
    """, unsafe_allow_html=True)


def render_info_box(content: str, box_type: str = "info"):
    """Render scientific info box"""
    box_class = {
        "info": "info-box-bio",
        "warning": "warning-box-bio",
        "success": "success-box-bio",
        "alert": "alert-box-bio"
    }.get(box_type, "info-box-bio")
    
    st.markdown(f"""
    <div class="{box_class}">
        {content}
    </div>
    """, unsafe_allow_html=True)


# Biological color palette for charts
BIO_COLOR_PALETTE = {
    # nrcdnl94
    'primary': ['#1e3a5f', '#3d7ea6', '#7fcdbb', '#c7e9b4', '#edf8fb'],
    'nucleotides': ['#e74c3c', '#3498db', '#2ecc71', '#f39c12'],
    'scientific': ['#2c3e50', '#34495e', '#7f8c8d', '#95a5a6', '#bdc3c7'],
    'heatmap': ['#c0392b', '#e74c3c', '#f39c12', '#f1c40f', '#2ecc71', '#27ae60'],
    'diverging': ['#c0392b', '#e74c3c', '#f5f5f5', '#3498db', '#2980b9']
}

# Icon mappings for different sections
BIO_ICONS = {
    # nrcdnl94
    'dna': '🧬',
    'clock': '⏰',
    'analysis': '📊',
    'upload': '📤',
    'download': '📥',
    'gene': '🔬',
    'database': '🗄️',
    'report': '📋',
    'warning': '⚠️',
    'success': '✅',
    'info': 'ℹ️',
    'settings': '⚙️',
    'user': '👤',
    'group': '👥',
    'brain': '🧠',
    'heart': '❤️',
    'liver': '🫀',
    'pill': '💊',
    'syringe': '💉',
    'molecule': '🔷',
    'chart': '📈',
    'graph': '📉',
    'stats': '📊',
    'calendar': '📅',
    'time': '🕐',
    'link': '🔗',
    'lock': '🔐',
    'globe': '🌍',
    'book': '📚',
    'academic': '🎓',
    'lab': '🧪',
    'microscope': '🔬',
    'petri': '🧫',
    'test_tube': '🧪',
    'stethoscope': '🩺',
    'hospital': '🏥',
    'ambulance': '🚑',
    'fire': '🔥',
    'ice': '🧊',
    'lightning': '⚡',
    'star': '⭐',
    'trophy': '🏆',
    'medal': '🏅',
    'target': '🎯',
    'magnifier': '🔍',
    'check': '✓',
    'cross': '✗',
    'arrow_up': '⬆️',
    'arrow_down': '⬇️',
    'arrow_right': '➡️',
    'arrow_left': '⬅️'
}


# End of module - # nrcdnl94