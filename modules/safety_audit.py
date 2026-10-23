"""
Module: Site Safety & PPE Audit (Epic 2)
Audits worker PPE compliance under OSHA 1926 and IS 456 / IS 3786.
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
    render_hazard_card,
    stretch_width
)

PPE_SYSTEM_INSTRUCTION = """You are a certified Lead Safety Auditor with OSHA 30-Hour Construction and Bureau of Indian Standards (IS 3786 / IS 456) accreditation.
Analyze the provided construction site photo with high precision.
Evaluate worker PPE compliance and identify potential physical hazards.
Return ONLY valid JSON matching this exact schema:
{
  "safety_score": <integer from 0 to 100>,
  "overall_status": "<Compliant | Minor Infractions Detected | Critical Non-Compliance>",
  "audit_standard": "<e.g. OSHA 1926 & IS 3786:1983>",
  "detected_workers_count": <integer>,
  "ppe_detection": [
    {
      "item": "<e.g. Industrial Hard Hats / Helmets>",
      "required": <boolean>,
      "detected_compliant": <integer>,
      "total_workers": <integer>,
      "status": "<Compliant | Minor Violation | Non-Compliant>",
      "details": "<concise observation note>"
    }
  ],
  "identified_site_hazards": [
    {
      "hazard": "<hazard title>",
      "severity": "<Low | Medium | High | Critical>",
      "code_reference": "<relevant standard reference, e.g. OSHA 1926.501 or IS 456>",
      "remedy": "<mandatory engineering corrective remedy>"
    }
  ],
  "recommendation_summary": "<2-sentence executive summary>"
}
Do not include any markdown backticks or commentary outside the JSON object.
"""

PPE_USER_PROMPT = """Conduct a comprehensive safety and PPE compliance audit on this construction site image.
Audit requirements:
1. Detect all visible construction personnel.
2. Verify Hard Hats (IS 2925 / EN 397), High-Visibility Vests, Steel-Toe Safety Boots, Safety Harnesses at elevation, and Protective Eyewear.
3. Identify site physical hazards including unprotected edges, rebar impalement risks, trip hazards, and scaffolding defects.
4. Calculate a holistic Safety Compliance Score (0-100) based on severity-weighted infraction penalties.
Output the structured JSON report.
"""

def render_safety_tab(api_key: Optional[str], sample_images: Dict[str, Image.Image]):
    """Renders the Tab 1 Site Safety & PPE Audit interface."""
    st.subheader("🛡️ Site Safety & PPE Vision Audit (OSHA & IS Standards)")
    st.caption("Automated multimodal inspection analyzing worker PPE adherence, edge protections, and hazard severity grading.")

    col_up, col_preview = st.columns([1.2, 1])

    with col_up:
        source_choice = st.radio(
            "Select Image Source:",
            ["Use Sample Construction Photo", "Upload Custom Site Photo"],
            horizontal=True
        )

        image_to_analyze: Optional[Image.Image] = None

        if source_choice == "Use Sample Construction Photo":
            sample_keys = list(sample_images.keys())
            selected_sample = st.selectbox("Choose Sample Site Scene:", sample_keys, index=0)
            image_to_analyze = sample_images[selected_sample]
            st.info(f"Loaded preset: **{selected_sample}**")
        else:
            uploaded_file = st.file_uploader(
                "Upload Site Photo (JPG, PNG):",
                type=["jpg", "jpeg", "png"],
                help="Upload a clear image of workers or construction site zones."
            )
            if uploaded_file:
                image_to_analyze = Image.open(uploaded_file)

        audit_btn = st.button("🚀 Run Multimodal Safety Audit", type="primary", **stretch_width())

    with col_preview:
        if image_to_analyze:
            st.image(image_to_analyze, caption="Site Inspection Viewport", **stretch_width())
        else:
            st.info("Upload or select a sample image to view preview.")

    st.markdown("---")

    # Session state preservation for audit results
    if "safety_audit_result" not in st.session_state:
        st.session_state["safety_audit_result"] = None

    if audit_btn and image_to_analyze:
        with st.spinner("🤖 Multimodal AI auditing PPE items, personnel postures, and site hazards..."):
            audit_result = analyze_multimodal(
                image=image_to_analyze,
                system_instruction=PPE_SYSTEM_INSTRUCTION,
                prompt=PPE_USER_PROMPT,
                api_key=api_key,
                mock_type="ppe"
            )
            st.session_state["safety_audit_result"] = audit_result

    result = st.session_state["safety_audit_result"]

    if result:
        st.success(f"Audit completed successfully! Mode: **{result.get('_mode', 'Live Gemini Vision')}**")

        # Top Executive Metrics
        score = result.get("safety_score", 75)
        status = result.get("overall_status", "Compliant")
        workers_count = result.get("detected_workers_count", 0)
        hazards = result.get("identified_site_hazards", [])
        critical_count = sum(1 for h in hazards if h.get("severity") in ["Critical", "High"])

        m1, m2, m3, m4 = st.columns(4)
        with m1:
            score_color = "#10B981" if score >= 80 else ("#F59E0B" if score >= 60 else "#EF4444")
            render_metric_card("Safety Compliance Score", f"{score} / 100", f"Standard: {result.get('audit_standard', 'OSHA / IS')}", score_color)
        with m2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Compliance Status</div>
                <div style="margin-top: 8px;">{render_status_pill(status)}</div>
            </div>
            """, unsafe_allow_html=True)
        with m3:
            render_metric_card("Detected Personnel", f"{workers_count} Workers", "Active in Frame")
        with m4:
            render_metric_card("High/Critical Hazards", f"{critical_count} Flagged", "Immediate Action Req.", "#EF4444" if critical_count > 0 else "#10B981")

        st.markdown("<br>", unsafe_allow_html=True)

        # Tabbed Detail View: Checklist vs Hazards vs Raw JSON
        tab_ppe, tab_hazards, tab_json = st.tabs(["📋 PPE Detection Checklist", "⚠️ Identified Site Hazards", "📄 Structured JSON Contract & Export"])

        with tab_ppe:
            ppe_items = result.get("ppe_detection", [])
            if ppe_items:
                df_ppe = pd.DataFrame(ppe_items)
                # Display clean customized cards
                for item in ppe_items:
                    st_val = item.get("status", "Compliant")
                    icon = "✅" if "compliant" in st_val.lower() and "non" not in st_val.lower() and "minor" not in st_val.lower() else ("⚠️" if "minor" in st_val.lower() else "❌")
                    
                    with st.expander(f"{icon} **{item.get('item')}** — *{st_val}* ({item.get('detected_compliant', 0)}/{item.get('total_workers', 0)} Compliant)", expanded=True):
                        st.write(f"**Observation:** {item.get('details')}")
                        st.write(f"**Regulatory Mandatory Status:** {'Mandatory' if item.get('required') else 'Optional / Task-Specific'}")
            else:
                st.info("No explicit PPE line items returned.")

        with tab_hazards:
            if hazards:
                for h in hazards:
                    render_hazard_card(
                        title=h.get("hazard", "Unknown Hazard"),
                        severity=h.get("severity", "Medium"),
                        remedy=h.get("remedy", "Take safety precautions."),
                        rule=h.get("code_reference", "")
                    )
            else:
                st.success("No physical site hazards flagged in the current camera frame.")

        with tab_json:
            st.markdown("#### Structured JSON Data Contract (API / ERP Integrated)")
            json_str = json.dumps(result, indent=2)
            st.code(json_str, language="json")

            col_d1, col_d2 = st.columns(2)
            with col_d1:
                st.download_button(
                    label="📥 Download JSON Audit Report",
                    data=json_str,
                    file_name="site_safety_ppe_audit.json",
                    mime="application/json",
                    **stretch_width()
                )
            with col_d2:
                # Convert to CSV table
                if ppe_items:
                    df_export = pd.DataFrame(ppe_items)
                    csv_data = df_export.to_csv(index=False)
                    st.download_button(
                        label="📊 Download PPE Checklist (CSV)",
                        data=csv_data,
                        file_name="ppe_compliance_checklist.csv",
                        mime="text/csv",
                        **stretch_width()
                    )
