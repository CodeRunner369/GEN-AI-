"""
UI Components and Design System for Multimodal Construction Intelligence Platform.
Theme: High-contrast Construction Tech (Slate, Carbon, Safety Amber, Emerald, Ruby).
"""

import streamlit as st
import json
import inspect

def stretch_width() -> dict:
    """
    Returns {'width': 'stretch'} for modern Streamlit (>= 1.66 / Streamlit Cloud post-2025)
    or {'use_container_width': True} for legacy Streamlit versions, eliminating all deprecation warnings.
    """
    if "width" in inspect.signature(st.button).parameters:
        return {"width": "stretch"}
    return {"use_container_width": True}

def inject_custom_css():
    """Injects high-fidelity custom CSS styles for the construction platform."""
    st.markdown("""
    <style>
    /* Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    code, pre {
        font-family: 'JetBrains Mono', monospace !important;
    }

    /* Main Container Padding */
    .block-container {
        padding-top: 1.8rem;
        padding-bottom: 3rem;
        max-width: 95%;
    }

    /* Platform Hero Banner */
    .hero-banner {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.9) 0%, rgba(15, 23, 42, 0.95) 100%);
        border: 1px solid rgba(245, 158, 11, 0.25);
        border-radius: 14px;
        padding: 24px 28px;
        margin-bottom: 24px;
        box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.5);
        position: relative;
        overflow: hidden;
    }

    .hero-banner::before {
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        width: 6px;
        height: 100%;
        background: linear-gradient(180deg, #F59E0B 0%, #D97706 100%);
    }

    .hero-title {
        font-size: 26px;
        font-weight: 800;
        color: #F8FAFC;
        letter-spacing: -0.5px;
        margin-bottom: 6px;
        display: flex;
        align-items: center;
        gap: 12px;
    }

    .hero-subtitle {
        font-size: 14px;
        color: #94A3B8;
        line-height: 1.5;
        margin-bottom: 12px;
    }

    .tag-container {
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
        margin-top: 8px;
    }

    .meta-tag {
        font-size: 11px;
        font-weight: 600;
        padding: 4px 10px;
        border-radius: 6px;
        background: rgba(255, 255, 255, 0.06);
        color: #CBD5E1;
        border: 1px solid rgba(255, 255, 255, 0.1);
        display: inline-flex;
        align-items: center;
        gap: 5px;
    }

    .meta-tag.amber {
        background: rgba(245, 158, 11, 0.15);
        color: #FBBF24;
        border-color: rgba(245, 158, 11, 0.3);
    }

    .meta-tag.cyan {
        background: rgba(6, 182, 212, 0.15);
        color: #38BDF8;
        border-color: rgba(6, 182, 212, 0.3);
    }

    .meta-tag.emerald {
        background: rgba(16, 185, 129, 0.15);
        color: #34D399;
        border-color: rgba(16, 185, 129, 0.3);
    }

    /* Metric Card Styling */
    .metric-card {
        background: #1E293B;
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 18px 20px;
        transition: all 0.2s ease-in-out;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.25);
    }

    .metric-card:hover {
        border-color: rgba(245, 158, 11, 0.4);
        transform: translateY(-2px);
    }

    .metric-label {
        font-size: 12px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        color: #94A3B8;
        margin-bottom: 6px;
    }

    .metric-value {
        font-size: 26px;
        font-weight: 800;
        color: #F8FAFC;
        line-height: 1.1;
    }

    .metric-delta {
        font-size: 12px;
        font-weight: 600;
        margin-top: 6px;
    }

    /* Hazard & Protocol Cards */
    .hazard-card {
        background: #1E293B;
        border-radius: 10px;
        border-left: 5px solid;
        padding: 16px;
        margin-bottom: 12px;
    }

    .hazard-critical {
        border-left-color: #EF4444;
        background: linear-gradient(90deg, rgba(239, 68, 68, 0.1) 0%, rgba(30, 41, 59, 0.8) 100%);
    }

    .hazard-high {
        border-left-color: #F97316;
        background: linear-gradient(90deg, rgba(249, 115, 22, 0.1) 0%, rgba(30, 41, 59, 0.8) 100%);
    }

    .hazard-medium {
        border-left-color: #FBBF24;
        background: linear-gradient(90deg, rgba(251, 191, 36, 0.1) 0%, rgba(30, 41, 59, 0.8) 100%);
    }

    .hazard-low {
        border-left-color: #10B981;
        background: linear-gradient(90deg, rgba(16, 185, 129, 0.1) 0%, rgba(30, 41, 59, 0.8) 100%);
    }

    /* Badges */
    .badge-pill {
        display: inline-block;
        font-size: 12px;
        font-weight: 700;
        padding: 4px 12px;
        border-radius: 9999px;
        letter-spacing: 0.3px;
    }

    .badge-compliant {
        background: #064E3B;
        color: #34D399;
        border: 1px solid #059669;
    }

    .badge-minor {
        background: #78350F;
        color: #FCD34D;
        border: 1px solid #D97706;
    }

    .badge-critical {
        background: #7F1D1D;
        color: #FCA5A5;
        border: 1px solid #DC2626;
    }

    /* Tab styling overrides */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #0F172A;
        padding: 8px;
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.05);
    }

    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        padding: 10px 18px;
        font-weight: 600;
        color: #94A3B8;
    }

    .stTabs [aria-selected="true"] {
        background-color: #1E293B !important;
        color: #F59E0B !important;
        border: 1px solid rgba(245, 158, 11, 0.3) !important;
    }

    /* Sidebar Clean styling */
    section[data-testid="stSidebar"] {
        background-color: #0B1120;
        border-right: 1px solid rgba(255, 255, 255, 0.08);
    }
    </style>
    """, unsafe_allow_html=True)


def render_hero_banner():
    """Renders the top executive banner."""
    st.markdown("""
    <div class="hero-banner">
        <div class="hero-title">
            <span>🏗️ Multimodal Construction Intelligence Platform</span>
        </div>
        <div class="hero-subtitle">
            Autonomous decision-support platform integrating Computer Vision for PPE safety auditing & crack defect diagnostics, parametric construction estimation & real estate valuation in INR, and dynamic weather-aware operational protocols.
        </div>
        <div class="tag-container">
            <span class="meta-tag amber">ID: 6ac4c98d1dcde6d7857c1642</span>
            <span class="meta-tag cyan">Category: Generative AI & Decision Support</span>
            <span class="meta-tag emerald">Standards: OSHA 1926 • IS 456:2000 • NBC 2016</span>
            <span class="meta-tag">Multimodal: Gemini 1.5/2.0 Vision</span>
            <span class="meta-tag">3D Render: Pollinations/Flux</span>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_metric_card(label: str, value: str, delta: str = None, delta_color: str = "#10B981"):
    """Renders an engineered modern metric card."""
    delta_html = f'<div class="metric-delta" style="color: {delta_color};">{delta}</div>' if delta else ""
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">{label}</div>
        <div class="metric-value">{value}</div>
        {delta_html}
    </div>
    """, unsafe_allow_html=True)


def render_status_pill(status: str) -> str:
    """Returns HTML for formatted status pills."""
    status_lower = status.lower()
    if "compliant" in status_lower and "non" not in status_lower and "minor" not in status_lower:
        return f'<span class="badge-pill badge-compliant">● {status.upper()}</span>'
    elif "minor" in status_lower or "moderate" in status_lower:
        return f'<span class="badge-pill badge-minor">▲ {status.upper()}</span>'
    else:
        return f'<span class="badge-pill badge-critical">✕ {status.upper()}</span>'


def render_hazard_card(title: str, severity: str, remedy: str, rule: str = ""):
    """Renders an engineering hazard alert card."""
    sev_class = f"hazard-{severity.lower()}"
    rule_badge = f'<span class="meta-tag" style="margin-left:8px;">{rule}</span>' if rule else ""
    st.markdown(f"""
    <div class="hazard-card {sev_class}">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
            <strong style="color: #F8FAFC; font-size: 15px;">⚠️ {title}</strong>
            <div>
                <span class="meta-tag {'amber' if severity in ['High', 'Critical'] else 'cyan'}">{severity.upper()} SEVERITY</span>
                {rule_badge}
            </div>
        </div>
        <div style="font-size: 13px; color: #CBD5E1; line-height: 1.5;">
            <strong>Mandatory Corrective Action:</strong> {remedy}
        </div>
    </div>
    """, unsafe_allow_html=True)
