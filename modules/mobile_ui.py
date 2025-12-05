# ============================================================================
# EpiClock Prototype - DNA Methylation Epigenetic Age Analysis Platform
# Copyright (c) 2024 Dr. Nurcan Denli Bayır (nrcdnl94)
# GitHub: https://github.com/mortemdulcem/epi-clock-DNA-mtl-prototype
# All rights reserved. See LICENSE file for details.
# Author Signature: nrcdnl94
# ============================================================================
"""
Mobile-Responsive UI Components Module
======================================

Provides mobile-friendly UI enhancements for Streamlit:
- Responsive CSS injection
- Touch-friendly components
- Collapsible sections
- Fluid containers
- Role-based presets (clinician/researcher)
- Wizard-style workflows

Designed for tablet and phone access to reports.
"""

import streamlit as st
from typing import Dict, List, Optional, Callable, Any
from enum import Enum
from dataclasses import dataclass
import json


class UserRole(Enum):
    # nrcdnl94
    """User role presets"""
    CLINICIAN = "clinician"
    RESEARCHER = "researcher"
    FORENSIC = "forensic"
    ADMIN = "admin"
    GUEST = "guest"


@dataclass
# nrcdnl94
class WizardStep:
    # nrcdnl94
    """Single step in a wizard workflow"""
    id: str
    title: str
    description: str
    icon: str
    required: bool = True
    completed: bool = False


RESPONSIVE_CSS = """
<style>
/* Mobile-First Responsive Design */
@media screen and (max-width: 768px) {
    /* Hide sidebar by default on mobile */
    [data-testid="stSidebar"] {
        min-width: 0 !important;
        max-width: 0 !important;
        padding: 0 !important;
    }
    
    [data-testid="stSidebar"][aria-expanded="true"] {
        min-width: 280px !important;
        max-width: 280px !important;
    }
    
    /* Full width containers */
    .main .block-container {
        padding: 1rem !important;
        max-width: 100% !important;
    }
    
    /* Stack columns vertically */
    [data-testid="column"] {
        width: 100% !important;
        flex: 100% !important;
        min-width: 100% !important;
    }
    
    /* Larger touch targets */
    .stButton > button {
        min-height: 48px !important;
        font-size: 16px !important;
        padding: 12px 24px !important;
    }
    
    /* Larger form inputs */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input,
    .stSelectbox > div > div > div {
        min-height: 44px !important;
        font-size: 16px !important;
    }
    
    /* Readable text */
    .stMarkdown p {
        font-size: 16px !important;
        line-height: 1.6 !important;
    }
    
    /* Tables scroll horizontally */
    .stDataFrame {
        overflow-x: auto !important;
    }
    
    /* Cards for better mobile layout */
    .mobile-card {
        background: white;
        border-radius: 12px;
        padding: 16px;
        margin: 8px 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    
    /* Hide horizontal scrollbar */
    ::-webkit-scrollbar {
        height: 4px;
    }
}

/* Tablet Breakpoint */
@media screen and (min-width: 769px) and (max-width: 1024px) {
    .main .block-container {
        padding: 2rem !important;
    }
    
    [data-testid="column"] {
        min-width: 45% !important;
    }
}

/* Desktop and larger */
@media screen and (min-width: 1025px) {
    .main .block-container {
        max-width: 1200px !important;
        margin: 0 auto !important;
    }
}

/* Universal Improvements */
.stButton > button {
    border-radius: 8px !important;
    transition: all 0.2s ease !important;
}

.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 12px rgba(0,0,0,0.15) !important;
}

/* Metric cards */
[data-testid="metric-container"] {
    background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
    border-radius: 12px;
    padding: 16px !important;
    border: 1px solid #dee2e6;
}

/* Info boxes */
.info-box {
    background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
    border-left: 4px solid #2196f3;
    padding: 16px;
    border-radius: 8px;
    margin: 16px 0;
}

.warning-box {
    background: linear-gradient(135deg, #fff3e0 0%, #ffe0b2 100%);
    border-left: 4px solid #ff9800;
    padding: 16px;
    border-radius: 8px;
    margin: 16px 0;
}

.success-box {
    background: linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 100%);
    border-left: 4px solid #4caf50;
    padding: 16px;
    border-radius: 8px;
    margin: 16px 0;
}

.error-box {
    background: linear-gradient(135deg, #ffebee 0%, #ffcdd2 100%);
    border-left: 4px solid #f44336;
    padding: 16px;
    border-radius: 8px;
    margin: 16px 0;
}

/* Progress indicators */
.wizard-progress {
    display: flex;
    justify-content: space-between;
    margin: 24px 0;
    padding: 0;
    list-style: none;
}

.wizard-step {
    flex: 1;
    text-align: center;
    position: relative;
}

.wizard-step::before {
    content: '';
    position: absolute;
    top: 15px;
    left: 50%;
    width: 100%;
    height: 2px;
    background: #dee2e6;
}

.wizard-step:last-child::before {
    display: none;
}

.wizard-step.completed::before {
    background: #4caf50;
}

.step-number {
    width: 32px;
    height: 32px;
    border-radius: 50%;
    background: #dee2e6;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    font-weight: bold;
    margin-bottom: 8px;
    position: relative;
    z-index: 1;
}

.wizard-step.completed .step-number {
    background: #4caf50;
    color: white;
}

.wizard-step.active .step-number {
    background: #2196f3;
    color: white;
}

/* Floating action button for mobile */
.fab {
    position: fixed;
    bottom: 20px;
    right: 20px;
    width: 56px;
    height: 56px;
    border-radius: 50%;
    background: #2196f3;
    color: white;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 4px 12px rgba(0,0,0,0.3);
    z-index: 1000;
    cursor: pointer;
}

/* Collapsible panels */
.collapsible-header {
    background: #f8f9fa;
    padding: 12px 16px;
    border-radius: 8px;
    cursor: pointer;
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin: 8px 0;
    border: 1px solid #dee2e6;
}

.collapsible-header:hover {
    background: #e9ecef;
}

/* Charts responsive */
.js-plotly-plot {
    width: 100% !important;
}

/* Navigation pills for mobile */
.nav-pills {
    display: flex;
    overflow-x: auto;
    gap: 8px;
    padding: 8px 0;
    margin: 16px 0;
}

.nav-pill {
    flex-shrink: 0;
    padding: 8px 16px;
    background: #e9ecef;
    border-radius: 20px;
    font-size: 14px;
    white-space: nowrap;
}

.nav-pill.active {
    background: #2196f3;
    color: white;
}

/* Bottom navigation for mobile */
.bottom-nav {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    background: white;
    display: flex;
    justify-content: space-around;
    padding: 8px 0;
    box-shadow: 0 -2px 10px rgba(0,0,0,0.1);
    z-index: 1000;
}

.bottom-nav-item {
    text-align: center;
    padding: 8px 16px;
    color: #666;
    text-decoration: none;
}

.bottom-nav-item.active {
    color: #2196f3;
}

/* Print styles */
@media print {
    .no-print {
        display: none !important;
    }
    
    .page-break {
        page-break-before: always;
    }
}
</style>
"""


def inject_responsive_css():
    """Inject responsive CSS into Streamlit app"""
    st.markdown(RESPONSIVE_CSS, unsafe_allow_html=True)


def create_mobile_card(title: str, content: str, icon: str = "📊") -> str:
    """Create a mobile-friendly card component"""
    return f"""
    <div class="mobile-card">
        <h4>{icon} {title}</h4>
        <p>{content}</p>
    </div>
    """


def create_info_box(content: str, box_type: str = "info") -> str:
    """Create styled info box"""
    return f"""
    <div class="{box_type}-box">
        {content}
    </div>
    """


class WizardWorkflow:
    # nrcdnl94
    """
    Multi-step wizard workflow for guided data entry
    """
    
    def __init__(self, wizard_id: str, steps: List[WizardStep]):
        self.wizard_id = wizard_id
        self.steps = steps
        self._init_session_state()
    
    def _init_session_state(self):
        """Initialize session state for wizard"""
        if f"wizard_{self.wizard_id}_step" not in st.session_state:
            st.session_state[f"wizard_{self.wizard_id}_step"] = 0
        if f"wizard_{self.wizard_id}_data" not in st.session_state:
            st.session_state[f"wizard_{self.wizard_id}_data"] = {}
    
    @property
    def current_step(self) -> int:
        return st.session_state[f"wizard_{self.wizard_id}_step"]
    
    @current_step.setter
    def current_step(self, value: int):
        st.session_state[f"wizard_{self.wizard_id}_step"] = max(0, min(value, len(self.steps) - 1))
    
    @property
    def data(self) -> Dict:
        return st.session_state[f"wizard_{self.wizard_id}_data"]
    
    def set_data(self, key: str, value: Any):
        """Store data for current step"""
        st.session_state[f"wizard_{self.wizard_id}_data"][key] = value
    
    def render_progress(self):
        """Render progress indicator"""
        cols = st.columns(len(self.steps))
        for i, (col, step) in enumerate(zip(cols, self.steps)):
            with col:
                if i < self.current_step:
                    status = "✅"
                    color = "#4caf50"
                elif i == self.current_step:
                    status = "🔵"
                    color = "#2196f3"
                else:
                    status = "⚪"
                    color = "#9e9e9e"
                
                st.markdown(
                    f"<div style='text-align:center'>"
                    f"<span style='font-size:24px'>{status}</span><br>"
                    f"<span style='font-size:12px;color:{color}'>{step.title}</span>"
                    f"</div>",
                    unsafe_allow_html=True
                )
    
    def render_navigation(self):
        """Render navigation buttons"""
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col1:
            if self.current_step > 0:
                if st.button("← Geri", key=f"wizard_{self.wizard_id}_back"):
                    self.current_step -= 1
                    st.rerun()
        
        with col3:
            if self.current_step < len(self.steps) - 1:
                if st.button("İleri →", key=f"wizard_{self.wizard_id}_next", type="primary"):
                    self.current_step += 1
                    st.rerun()
            else:
                if st.button("Tamamla ✓", key=f"wizard_{self.wizard_id}_finish", type="primary"):
                    return True
        
        return False
    
    def get_current_step_info(self) -> WizardStep:
        """Get current step details"""
        return self.steps[self.current_step]
    
    def reset(self):
        """Reset wizard to initial state"""
        st.session_state[f"wizard_{self.wizard_id}_step"] = 0
        st.session_state[f"wizard_{self.wizard_id}_data"] = {}


class RoleBasedUI:
    # nrcdnl94
    """
    Role-based UI customization
    """
    
    ROLE_CONFIGS = {
        UserRole.CLINICIAN: {
            'name': 'Klinisyen',
            'icon': '👨‍⚕️',
            'default_modules': ['Bireysel Analiz', 'Klinik Karar Destek', 'Rapor Oluştur'],
            'simplified_view': True,
            'show_technical_details': False,
            'primary_color': '#4caf50'
        },
        UserRole.RESEARCHER: {
            'name': 'Araştırmacı',
            'icon': '🔬',
            'default_modules': ['Toplu Analiz', 'Diferansiyel Metilasyon', 'GSEA', 'İstatistik'],
            'simplified_view': False,
            'show_technical_details': True,
            'primary_color': '#2196f3'
        },
        UserRole.FORENSIC: {
            'name': 'Adli Uzman',
            'icon': '⚖️',
            'default_modules': ['Postmortem Validasyon', 'Blockchain Denetim', 'Rapor Oluştur'],
            'simplified_view': False,
            'show_technical_details': True,
            'primary_color': '#9c27b0'
        },
        UserRole.ADMIN: {
            'name': 'Yönetici',
            'icon': '👑',
            'default_modules': 'all',
            'simplified_view': False,
            'show_technical_details': True,
            'primary_color': '#ff9800'
        },
        UserRole.GUEST: {
            'name': 'Misafir',
            'icon': '👤',
            'default_modules': ['Ana Sayfa', 'Referans Veritabanı'],
            'simplified_view': True,
            'show_technical_details': False,
            'primary_color': '#9e9e9e'
        }
    }
    
    def __init__(self):
        self._init_session_state()
    
    def _init_session_state(self):
        """Initialize role in session state"""
        if 'user_role' not in st.session_state:
            st.session_state['user_role'] = UserRole.GUEST
    
    @property
    def current_role(self) -> UserRole:
        return st.session_state['user_role']
    
    @current_role.setter
    def current_role(self, role: UserRole):
        st.session_state['user_role'] = role
    
    def get_config(self) -> Dict:
        """Get current role configuration"""
        return self.ROLE_CONFIGS.get(self.current_role, self.ROLE_CONFIGS[UserRole.GUEST])
    
    def render_role_selector(self):
        """Render role selection widget"""
        options = list(self.ROLE_CONFIGS.keys())
        option_labels = [f"{self.ROLE_CONFIGS[r]['icon']} {self.ROLE_CONFIGS[r]['name']}" for r in options]
        
        selected_idx = st.selectbox(
            "Kullanıcı Rolü",
            range(len(options)),
            format_func=lambda x: option_labels[x],
            index=options.index(self.current_role)
        )
        
        if options[selected_idx] != self.current_role:
            self.current_role = options[selected_idx]
            st.rerun()
    
    def should_show_module(self, module_name: str) -> bool:
        """Check if module should be shown for current role"""
        config = self.get_config()
        default_modules = config['default_modules']
        
        if default_modules == 'all':
            return True
        
        return any(m.lower() in module_name.lower() for m in default_modules)
    
    def get_welcome_message(self) -> str:
        """Get role-specific welcome message"""
        config = self.get_config()
        
        messages = {
            UserRole.CLINICIAN: "Hasta epigenetik yaş analizleri ve klinik karar desteği için hazır.",
            UserRole.RESEARCHER: "Gelişmiş istatistiksel analiz ve veri keşfi araçlarına erişim aktif.",
            UserRole.FORENSIC: "Adli kanıt analizi ve zincir-of-custody takibi etkin.",
            UserRole.ADMIN: "Tüm modüller ve yönetim araçlarına tam erişim.",
            UserRole.GUEST: "Temel özelliklere erişiminiz bulunmaktadır."
        }
        
        return f"{config['icon']} **{config['name']} Modu** - {messages.get(self.current_role, '')}"


def render_touch_friendly_tabs(tabs: List[str], key: str = "tabs") -> int:
    """Render touch-friendly horizontal tabs"""
    if f"{key}_selected" not in st.session_state:
        st.session_state[f"{key}_selected"] = 0
    
    cols = st.columns(len(tabs))
    for i, (col, tab) in enumerate(zip(cols, tabs)):
        with col:
            btn_type = "primary" if i == st.session_state[f"{key}_selected"] else "secondary"
            if st.button(tab, key=f"{key}_tab_{i}", type=btn_type, use_container_width=True):
                st.session_state[f"{key}_selected"] = i
                st.rerun()
    
    return st.session_state[f"{key}_selected"]


def create_quick_action_buttons(actions: List[Dict[str, Any]]):
    """Create quick action button grid"""
    n_cols = min(len(actions), 4)
    cols = st.columns(n_cols)
    
    for i, action in enumerate(actions):
        with cols[i % n_cols]:
            if st.button(
                f"{action.get('icon', '▶️')} {action['label']}", 
                key=f"quick_action_{i}",
                use_container_width=True
            ):
                if 'callback' in action and callable(action['callback']):
                    action['callback']()
                return action.get('id', i)
    
    return None


def render_mobile_summary_cards(data: List[Dict[str, Any]]):
    """Render summary cards optimized for mobile"""
    for item in data:
        st.markdown(
            f"""
            <div class="mobile-card">
                <div style="display:flex;justify-content:space-between;align-items:center">
                    <span style="font-size:24px">{item.get('icon', '📊')}</span>
                    <span style="font-size:24px;font-weight:bold;color:{item.get('color', '#333')}">{item.get('value', '-')}</span>
                </div>
                <div style="font-size:14px;color:#666;margin-top:8px">{item.get('label', '')}</div>
                {f"<div style='font-size:12px;color:#999'>{item.get('subtitle', '')}</div>" if item.get('subtitle') else ""}
            </div>
            """,
            unsafe_allow_html=True
        )


def init_mobile_ui():
    """Initialize mobile UI components"""
    inject_responsive_css()
    
    if 'mobile_ui_initialized' not in st.session_state:
        st.session_state['mobile_ui_initialized'] = True


# End of module - # nrcdnl94