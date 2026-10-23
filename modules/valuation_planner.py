"""
Module: Planning & Real Estate Valuation (Epic 3)
Calculates construction budgets, CapEx incurred, real estate market valuation in INR (Lakhs/Crores),
material requirement takeoffs (Steel, Cement, Concrete), and generates conceptual 3D renders via Pollinations AI.
"""

import urllib.parse
import streamlit as st
import pandas as pd
from typing import Dict, Any

from modules.ui_components import render_metric_card, stretch_width

# City benchmark rates (INR per sq.ft) for Construction and Market Real Estate
LOCATION_TIERS = {
    "Tier 1 (Mumbai, Delhi-NCR, Bengaluru, Hyderabad, Chennai)": {
        "base_const_cost": 2400,
        "market_base_psf": 11500,
        "tier_name": "Tier 1"
    },
    "Tier 2 (Pune, Ahmedabad, Kolkata, Kochi, Chandigarh)": {
        "base_const_cost": 1950,
        "market_base_psf": 6800,
        "tier_name": "Tier 2"
    },
    "Tier 3 (Emerging Hubs, Smart Cities, State Capitals)": {
        "base_const_cost": 1600,
        "market_base_psf": 4200,
        "tier_name": "Tier 3"
    }
}

STRUCTURE_FACTORS = {
    "Residential High-Rise (G+25)": {
        "cost_multiplier": 1.25,
        "steel_kg_per_sqft": 4.5,
        "cement_bags_per_sqft": 0.45,
        "rmc_cum_per_sqft": 0.038,
        "desc": "Reinforced concrete shear wall & moment frame structure"
    },
    "Commercial Complex / IT Park (Grade-A)": {
        "cost_multiplier": 1.40,
        "steel_kg_per_sqft": 5.2,
        "cement_bags_per_sqft": 0.48,
        "rmc_cum_per_sqft": 0.042,
        "desc": "Post-tensioned flat slabs with high-performance glass curtain wall facade"
    },
    "Luxury Villa Gated Township": {
        "cost_multiplier": 1.30,
        "steel_kg_per_sqft": 3.8,
        "cement_bags_per_sqft": 0.42,
        "rmc_cum_per_sqft": 0.034,
        "desc": "Load-bearing RCC frames with premium marble finishes and landscaped terraces"
    },
    "Industrial Pre-Engineered Warehouse": {
        "cost_multiplier": 0.90,
        "steel_kg_per_sqft": 6.5,
        "cement_bags_per_sqft": 0.28,
        "rmc_cum_per_sqft": 0.024,
        "desc": "High-tensile structural steel portal frame with laser-screeded FM2 flooring"
    },
    "Mixed-Use Retail & Residential": {
        "cost_multiplier": 1.35,
        "steel_kg_per_sqft": 4.8,
        "cement_bags_per_sqft": 0.46,
        "rmc_cum_per_sqft": 0.040,
        "desc": "Multi-tier podium retail with residential twin towers above"
    }
}

QUALITY_GRADES = {
    "Standard (Affordable / Mid-Segment)": 1.0,
    "Premium (High-End Finishes / Home Automation)": 1.25,
    "Ultra-Luxury (Italian Marble / Triple Glazing / Platinum LEED)": 1.65
}


def format_inr(amount: float) -> str:
    """Formats numeric amount into INR Lakhs or Crores."""
    if amount >= 10_000_000:
        crores = amount / 10_000_000
        return f"₹ {crores:.2f} Cr"
    elif amount >= 100_000:
        lakhs = amount / 100_000
        return f"₹ {lakhs:.2f} L"
    else:
        return f"₹ {amount:,.0f}"


def calculate_project_metrics(
    structure_type: str,
    built_up_sqft: float,
    location_key: str,
    quality_grade: str,
    completion_pct: float
) -> Dict[str, Any]:
    """Computes budget, capex, valuation, and material takeoffs."""
    loc_data = LOCATION_TIERS[location_key]
    struct_data = STRUCTURE_FACTORS[structure_type]
    quality_mult = QUALITY_GRADES[quality_grade]

    # Construction Cost Calculation
    effective_const_rate_psf = loc_data["base_const_cost"] * struct_data["cost_multiplier"] * quality_mult
    total_budget_inr = built_up_sqft * effective_const_rate_psf

    # CapEx Incurred
    capex_incurred_inr = total_budget_inr * (completion_pct / 100.0)
    cost_to_complete_inr = total_budget_inr - capex_incurred_inr

    # Real Estate Market Valuation
    # Fully completed market rate
    market_rate_psf = loc_data["market_base_psf"] * (1.0 + (quality_mult - 1.0) * 0.6)
    full_market_valuation_inr = built_up_sqft * market_rate_psf

    # Current Market Asset Valuation (Incurred value + land/progress premium)
    # Progressive valuation accounts for land equity plus construction progress
    land_equity_component = full_market_valuation_inr * 0.35  # Land & approvals typically 35% of end value
    construction_market_component = (full_market_valuation_inr * 0.65) * (completion_pct / 100.0)
    current_asset_valuation_inr = land_equity_component + construction_market_component

    # Material Requirement Takeoffs
    steel_mt = (built_up_sqft * struct_data["steel_kg_per_sqft"]) / 1000.0
    cement_bags = built_up_sqft * struct_data["cement_bags_per_sqft"]
    cement_mt = (cement_bags * 50) / 1000.0
    rmc_cum = built_up_sqft * struct_data["rmc_cum_per_sqft"]

    return {
        "total_budget_inr": total_budget_inr,
        "capex_incurred_inr": capex_incurred_inr,
        "cost_to_complete_inr": cost_to_complete_inr,
        "current_asset_valuation_inr": current_asset_valuation_inr,
        "full_market_valuation_inr": full_market_valuation_inr,
        "const_rate_psf": effective_const_rate_psf,
        "market_rate_psf": market_rate_psf,
        "steel_mt": steel_mt,
        "cement_bags": cement_bags,
        "cement_mt": cement_mt,
        "rmc_cum": rmc_cum,
        "completion_pct": completion_pct
    }


def generate_pollinations_url(prompt: str, seed: int = 42) -> str:
    """Builds a direct Pollinations AI / Flux rendering URL."""
    encoded = urllib.parse.quote(prompt.strip())
    return f"https://image.pollinations.ai/prompt/{encoded}?width=1024&height=640&nologo=true&seed={seed}&model=flux"


def render_valuation_tab():
    """Renders the Tab 3 Planning & Real Estate Valuation interface."""
    st.subheader("📐 Planning, CapEx Estimation & Real Estate Valuation (INR)")
    st.caption("Parametric construction budget calculator, Bill of Quantities (BOQ) material takeoffs, and 3D architectural AI rendering.")

    col_input, col_results = st.columns([1.1, 1.4])

    with col_input:
        st.markdown("#### ⚙️ Parametric Project Specifications")
        structure_type = st.selectbox(
            "Structure Classification:",
            list(STRUCTURE_FACTORS.keys()),
            index=0
        )

        built_up_sqft = st.number_input(
            "Total Built-up Area (sq.ft):",
            min_value=5000,
            max_value=2_000_000,
            value=75_000,
            step=5000,
            help="Gross Floor Area (GFA) including super built-up common zones."
        )

        location_key = st.selectbox(
            "Geographical Location Tier:",
            list(LOCATION_TIERS.keys()),
            index=0
        )

        quality_grade = st.selectbox(
            "Construction & Specification Grade:",
            list(QUALITY_GRADES.keys()),
            index=1
        )

        completion_pct = st.slider(
            "Current Milestone Completion (%):",
            min_value=0,
            max_value=100,
            value=45,
            step=5,
            help="Physical site completion progress across superstructure, MEP, and finishes."
        )

        st.progress(completion_pct / 100.0, text=f"Milestone Progress: {completion_pct}% Execution")

    # Run Calculations
    metrics = calculate_project_metrics(
        structure_type=structure_type,
        built_up_sqft=built_up_sqft,
        location_key=location_key,
        quality_grade=quality_grade,
        completion_pct=completion_pct
    )

    with col_results:
        st.markdown("#### 💼 Financial Capitalization & Asset Valuation (INR)")
        
        f1, f2 = st.columns(2)
        with f1:
            render_metric_card(
                "Total Project Budget",
                format_inr(metrics["total_budget_inr"]),
                f"₹ {metrics['const_rate_psf']:,.0f} / sq.ft const. rate"
            )
        with f2:
            render_metric_card(
                "Current Market Valuation",
                format_inr(metrics["current_asset_valuation_inr"]),
                f"Peak Value: {format_inr(metrics['full_market_valuation_inr'])}",
                "#10B981"
            )

        f3, f4 = st.columns(2)
        with f3:
            render_metric_card(
                "CapEx Incurred to Date",
                format_inr(metrics["capex_incurred_inr"]),
                f"{completion_pct}% Funds Disbursed",
                "#38BDF8"
            )
        with f4:
            render_metric_card(
                "Remaining Cost-to-Complete",
                format_inr(metrics["cost_to_complete_inr"]),
                f"{100 - completion_pct}% Remaining Budget",
                "#F59E0B"
            )

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("#### 🏗️ Bill of Quantities (BOQ) Primary Materials")

        m1, m2, m3 = st.columns(3)
        with m1:
            render_metric_card("TMT Steel Rebar", f"{metrics['steel_mt']:,.1f} MT", "Fe500D / Fe550D")
        with m2:
            render_metric_card("Cement Intake", f"{metrics['cement_bags']:,.0f} Bags", f"~{metrics['cement_mt']:,.1f} Metric Tonnes")
        with m3:
            render_metric_card("RMC Concrete", f"{metrics['rmc_cum']:,.0f} m³", "M25 to M40 Grade")

    st.markdown("---")

    # Conceptual 3D Architectural Rendering via Pollinations AI
    st.subheader("🎨 Conceptual 3D Architectural AI Rendering (Pollinations / Flux)")
    st.caption("Generates high-resolution architectural concept visualizations for client presentations, investor decks, and BIM planning.")

    render_col1, render_col2 = st.columns([1.2, 1])

    default_prompt = (
        f"hyperrealistic modern architectural 3D render of a {structure_type.split('(')[0].strip()}, "
        f"contemporary facade, cinematic golden hour lighting, construction stage at {completion_pct}% progress, "
        f"tower crane in background, landscaped podium, glass and steel architecture, 8k resolution, octane render, architectural photography"
    )

    with render_col1:
        custom_prompt = st.text_area(
            "Architectural Visualization Prompt:",
            value=default_prompt,
            height=110,
            help="Prompt fed directly into the Pollinations/Flux diffusion model."
        )

        col_seed, col_gen = st.columns([1, 1])
        with col_seed:
            seed_val = st.number_input("Random Seed:", min_value=1, max_value=99999, value=1024, step=1)
        with col_gen:
            st.markdown("<div style='margin-top: 28px;'></div>", unsafe_allow_html=True)
            gen_render_btn = st.button("✨ Generate 3D Concept Render", type="primary", **stretch_width())

    # State for render URL
    if "pollinations_render_url" not in st.session_state:
        st.session_state["pollinations_render_url"] = generate_pollinations_url(default_prompt, 1024)

    if gen_render_btn:
        st.session_state["pollinations_render_url"] = generate_pollinations_url(custom_prompt, seed_val)

    with render_col2:
        img_url = st.session_state["pollinations_render_url"]
        st.image(
            img_url,
            caption="Pollinations / Flux 3D Conceptual Architectural Rendering",
            **stretch_width()
        )
        st.markdown(f"[🔗 Open Full-Res Image in Browser]({img_url})")
