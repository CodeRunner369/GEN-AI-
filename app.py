"""
Multimodal Construction Intelligence Platform (Skill Wallet Capstone Project 1)
Platform ID: 6ac4c98d1dcde6d7857c1642
Category: Generative AI | Real Estate Decision Support

Modules:
- Tab 1: Site Safety & PPE Audit (Epic 2)
- Tab 2: Crack Diagnostics & Structural Integrity (Epic 2)
- Tab 3: Planning & Real Estate Valuation (Epic 3)
- Tab 4: Daily Site Assistant & Weather-Aware Advisory (Epic 5)
"""

import streamlit as st
import os

# Configure Streamlit page settings
st.set_page_config(
    page_title="Multimodal Construction Intelligence Platform",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Import custom modules
from modules.ui_components import inject_custom_css, render_hero_banner
from modules.safety_audit import render_safety_tab
from modules.crack_diagnostics import render_crack_tab
from modules.valuation_planner import render_valuation_tab
from modules.weather_advisor import render_weather_tab
from sample_data.presets import get_all_sample_presets

# Inject CSS styling
inject_custom_css()

# Cache sample presets
@st.cache_resource
def load_cached_presets():
    return get_all_sample_presets()

sample_images = load_cached_presets()

# --- SIDEBAR CONFIGURATION ---
with st.sidebar:
    st.markdown("### ⚙️ System Configuration")
    
    # API Key Input with Secure Masking
    env_gemini_key = os.environ.get("GEMINI_API_KEY", "")
    api_key_input = st.text_input(
        "Google Gemini API Key:",
        value=env_gemini_key,
        type="password",
        placeholder="AIzaSy...",
        help="Paste your Gemini 1.5/2.0 API key for live multimodal neural inference. If left empty, the platform automatically engages the Smart Demonstration Engine."
    )

    # API Status Badge
    if api_key_input and api_key_input.strip():
        st.success("🟢 Mode: Live Multimodal Gemini AI")
    else:
        st.info("🔵 Mode: Intelligent Demonstration Engine (No API Key Required)")

    st.markdown("---")

    # Architecture Overview & Kanban Epics Coverage
    st.markdown("### 🏛️ System Architecture")
    with st.expander("📋 Kanban Epics Coverage", expanded=False):
        st.markdown("""
        - **Pre-requisites:** Python 3.9+, Streamlit, Multimodal LLM
        - **Epic 1:** Requirements & Modular Environment
        - **Epic 2:** PPE Safety Vision & Crack Diagnostics
        - **Epic 3:** Project Planning & Real Estate Valuation (INR)
        - **Epic 4:** Multimodal AI & Strict JSON Contracts
        - **Epic 5:** Site Chatbot & Weather Advisory
        - **Epic 6:** Interface, Robustness & Cloud Deployment
        """)

    with st.expander("📚 Governing Engineering Standards", expanded=False):
        st.markdown("""
        - **OSHA 1926:** Safety and Health Regulations for Construction
        - **IS 456:2000:** Code of Practice for Plain and Reinforced Concrete
        - **IS 3786:1983:** Methods for Computation of Frequency & Severity Rates
        - **ACI 224R-01:** Control of Cracking in Concrete Structures
        - **NBC 2016:** National Building Code of India
        """)

    st.markdown("---")
    st.markdown("### ℹ️ Platform Information")
    st.caption("Platform ID: **6ac4c98d1dcde6d7857c1642**")
    st.caption("Category: **Generative AI & Real Estate Decision Support**")
    st.caption("Ready for 1-Click Streamlit Community Cloud Deployment.")

# --- TOP EXECUTIVE BANNER ---
render_hero_banner()

# --- MAIN TAB NAVIGATION ---
tab_safety, tab_crack, tab_valuation, tab_weather = st.tabs([
    "🦺 Tab 1: Site Safety & PPE Audit",
    "🔍 Tab 2: Crack Diagnostics & Structural Integrity",
    "📈 Tab 3: Planning & Real Estate Valuation (INR)",
    "🌦️ Tab 4: Daily Site Assistant & Weather Advisory"
])

with tab_safety:
    render_safety_tab(api_key=api_key_input, sample_images=sample_images)

with tab_crack:
    render_crack_tab(api_key=api_key_input, sample_images=sample_images)

with tab_valuation:
    render_valuation_tab()

with tab_weather:
    render_weather_tab(api_key=api_key_input)

# --- FOOTER ---
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #64748B; font-size: 12px;'>"
    "Multimodal Construction Intelligence Platform • Capstone Project 1 • Built for Streamlit Cloud"
    "</div>",
    unsafe_allow_html=True
)
