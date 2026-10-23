"""
Module: Crack Diagnostics & Structural Integrity (Epic 2)
Analyzes concrete/wall defect surfaces, classifies crack types, estimates width (mm),
diagnoses root causes, and generates engineering repair specifications (ACI 224R / IS 456).
"""

import json
import streamlit as st
import pandas as pd
from PIL import Image
from typing import Dict, Any, Optional

from modules.ai_engine import analyze_multimodal
from modules.ui_components import (
    render_metric_card,
    render_status_pill,
    render_hazard_card
)

CRACK_SYSTEM_INSTRUCTION = """You are a Senior Structural Forensic Engineer and Concrete Repair Specialist adhering to IS 456:2000, ACI 224R-01 (Control of Cracking in Concrete Structures), and ICRI guidelines.
Examine the uploaded image of the concrete element (slab, beam, column, masonry wall, or foundation).
Classify the defect type precisely (e.g. Hairline Cracking, Settlement Crack, Structural Shear Crack, Thermal Expansion/Contraction, Concrete Spalling & Rebar Delamination, Honeycombing).
Estimate the crack aperture/width in millimeters (mm).
Determine root causes and produce step-by-step structural repair procedures.
Return ONLY valid JSON matching this exact schema:
{
  "defect_type": "<Hairline | Settlement | Structural Shear | Thermal Expansion | Spalling / Delamination | Honeycombing>",
  "element_type": "<e.g. RC Beam Support, Slab Soffit, Masonry Wall, Column Base>",
  "estimated_width_mm": <float or integer, e.g. 1.8>,
  "severity_score": <integer from 0 to 100>,
  "structural_urgency": "<Routine | Moderate | Urgent | Critical>",
  "is_active": <boolean>,
  "code_reference": "<relevant standard, e.g. IS 456 Cl 35.3.2 / ACI 224R-01>",
  "root_causes": [
    "<root cause factor 1>",
    "<root cause factor 2>"
  ],
  "recommended_repairs": [
    {
      "step": <integer>,
      "procedure": "<repair step title, e.g. High Pressure Epoxy Injection>",
      "specification": "<technical material and execution spec>"
    }
  ],
  "structural_clearance": "<statement regarding structural safety and load restrictions>"
}
Do not include any markdown backticks or commentary outside the JSON object.
"""

CRACK_USER_PROMPT = """Perform an in-depth structural defect and crack diagnostic on this concrete/masonry image.
1. Classify the defect morphology: Hairline, Settlement, Structural Shear, Thermal, or Spalling.
2. Estimate surface crack width in millimeters (mm).
3. Identify probable engineering root causes (overload, corrosion carbonation, thermal cycles, foundation subsidence).
4. Prescribe field repair procedures (epoxy injection, structural re-grouting, CFRP stitching, micro-concrete jacketing).
5. Specify structural urgency rating and IS 456 / ACI allowable crack width comparisons.
Output the structured JSON diagnosis.
"""

def render_crack_tab(api_key: Optional[str], sample_images: Dict[str, Image.Image]):
    """Renders the Tab 2 Crack Diagnostics & Structural Integrity interface."""
    st.subheader("🔍 Crack Diagnostics & Structural Integrity (ACI & IS 456)")
    st.caption("AI-powered concrete fracture mechanics: crack classification, estimated aperture (mm), root cause analysis, and repair protocols.")

    col_up, col_preview = st.columns([1.2, 1])

    with col_up:
        source_choice = st.radio(
            "Select Concrete Surface Image:",
            ["Use Sample Defect Surface", "Upload Custom Defect Photo"],
            horizontal=True,
            key="crack_source_choice"
        )

        image_to_analyze: Optional[Image.Image] = None

        if source_choice == "Use Sample Defect Surface":
            crack_samples = [k for k in sample_images.keys() if "crack" in k.lower() or "concrete" in k.lower() or "structural" in k.lower()]
            if not crack_samples:
                crack_samples = list(sample_images.keys())
            selected_sample = st.selectbox("Choose Sample Defect:", crack_samples, index=0, key="crack_preset_select")
            image_to_analyze = sample_images[selected_sample]
            st.info(f"Loaded preset: **{selected_sample}**")
        else:
            uploaded_file = st.file_uploader(
                "Upload Concrete/Wall Photo (JPG, PNG):",
                type=["jpg", "jpeg", "png"],
                key="crack_uploader",
                help="Upload a close-up or elevation photo of cracks or spalled concrete."
            )
            if uploaded_file:
                image_to_analyze = Image.open(uploaded_file)

        diagnose_btn = st.button("🔬 Execute Structural Crack Diagnostics", type="primary", use_container_width=True)

    with col_preview:
        if image_to_analyze:
            st.image(image_to_analyze, caption="Defect Visual Inspection Surface", use_container_width=True)
        else:
            st.info("Upload or select a concrete surface image to view preview.")

    st.markdown("---")

    if "crack_diagnostics_result" not in st.session_state:
        st.session_state["crack_diagnostics_result"] = None

    if diagnose_btn and image_to_analyze:
        with st.spinner("🧠 Analyzing fracture kinematics, crack width, and structural degradation..."):
            diag_result = analyze_multimodal(
                image=image_to_analyze,
                system_instruction=CRACK_SYSTEM_INSTRUCTION,
                prompt=CRACK_USER_PROMPT,
                api_key=api_key,
                mock_type="crack"
            )
            st.session_state["crack_diagnostics_result"] = diag_result

    result = st.session_state["crack_diagnostics_result"]

    if result:
        st.success(f"Diagnosis completed! Engine: **{result.get('_mode', 'Live Gemini Vision')}**")

        defect_type = result.get("defect_type", "Structural Shear Crack")
        width_mm = result.get("estimated_width_mm", 1.5)
        severity = result.get("severity_score", 70)
        urgency = result.get("structural_urgency", "Moderate")
        element = result.get("element_type", "Reinforced Concrete Element")

        # Metric Cards
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            render_metric_card("Classified Defect", defect_type, element)
        with c2:
            is456_limit = 0.3  # IS 456 allowable crack width for moderate exposure is 0.3mm
            delta_str = f"Limit: 0.3mm (Exceeded!)" if width_mm > is456_limit else "Within 0.3mm IS 456 limit"
            delta_col = "#EF4444" if width_mm > is456_limit else "#10B981"
            render_metric_card("Est. Crack Aperture", f"{width_mm} mm", delta_str, delta_col)
        with c3:
            sev_col = "#EF4444" if severity >= 75 else ("#F59E0B" if severity >= 40 else "#10B981")
            render_metric_card("Defect Severity Score", f"{severity} / 100", f"Urgency: {urgency}", sev_col)
        with c4:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Repair Urgency</div>
                <div style="margin-top: 8px;">{render_status_pill(urgency)}</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        tab_repair, tab_causes, tab_json = st.tabs([
            "🛠️ Recommended Engineering Repairs",
            "🔬 Root Cause & Structural Impact",
            "📄 Defect Report & JSON Contract"
        ])

        with tab_repair:
            st.markdown(f"**Structural Clearance Directive:** *{result.get('structural_clearance', 'Inspect periodically')}*")
            repairs = result.get("recommended_repairs", [])
            for rep in repairs:
                st.markdown(f"""
                <div style="background: #1E293B; border-left: 4px solid #38BDF8; border-radius: 8px; padding: 14px 18px; margin-bottom: 10px;">
                    <strong style="color: #38BDF8; font-size: 15px;">Step {rep.get('step')}: {rep.get('procedure')}</strong>
                    <div style="color: #CBD5E1; font-size: 13px; margin-top: 6px; line-height: 1.5;">
                        {rep.get('specification')}
                    </div>
                </div>
                """, unsafe_allow_html=True)

        with tab_causes:
            st.markdown(f"**Governing Standards Reference:** `{result.get('code_reference', 'IS 456:2000 Cl 35.3.2')}`")
            st.markdown("#### Primary Root Causes Identified:")
            for cause in result.get("root_causes", []):
                st.markdown(f"- ⚠️ {cause}")
            
            st.markdown("---")
            st.markdown("#### Allowable Crack Widths Benchmark (IS 456 & ACI 224R)")
            st.markdown("""
            | Environmental Exposure | IS 456:2000 Max Limit | ACI 224R Limit | Typical Intervention |
            | :--- | :--- | :--- | :--- |
            | **Mild / Interior dry** | **0.30 mm** | 0.41 mm | Surface cosmetic sealant |
            | **Moderate / Exterior** | **0.20 mm** | 0.30 mm | High pressure polyurethane / epoxy |
            | **Severe / Marine & Submerged** | **0.10 mm** | 0.15 mm | CFRP wrap + hydrophobic coating |
            """)

        with tab_json:
            json_str = json.dumps(result, indent=2)
            st.code(json_str, language="json")
            st.download_button(
                label="📥 Download Structural Crack Diagnostic JSON",
                data=json_str,
                file_name="structural_crack_diagnostic.json",
                mime="application/json",
                use_container_width=True
            )
