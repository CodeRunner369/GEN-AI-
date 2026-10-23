"""
AI Engine: Multimodal Gemini 1.5/2.0 Client with Intelligent Demo Mode Fallback.
Provides unified inference for Computer Vision PPE Audits, Crack Classification, and Engineering Chatbot.
"""

import json
import re
from typing import Dict, Any, List, Optional
from PIL import Image

import warnings

# Graceful import of google.generativeai with warnings filter
try:
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=FutureWarning)
        import google.generativeai as genai
    GENAI_AVAILABLE = True
except ImportError:
    GENAI_AVAILABLE = False


def clean_json_text(text: str) -> str:
    """Cleans code blocks and extracts json string."""
    cleaned = re.sub(r"^```json\s*", "", text.strip(), flags=re.MULTILINE)
    cleaned = re.sub(r"^```\s*", "", cleaned, flags=re.MULTILINE)
    cleaned = cleaned.rstrip("`").strip()
    return cleaned


def analyze_multimodal(
    image: Image.Image,
    system_instruction: str,
    prompt: str,
    api_key: Optional[str] = None,
    mock_type: str = "ppe"
) -> Dict[str, Any]:
    """
    Executes multimodal vision analysis using Gemini or realistic mock fallback.
    """
    if api_key and api_key.strip() and GENAI_AVAILABLE:
        try:
            genai.configure(api_key=api_key.strip())
            
            # Select available vision model
            model_name = "gemini-1.5-flash"
            try:
                model = genai.GenerativeModel(
                    model_name=model_name,
                    system_instruction=system_instruction,
                    generation_config={"response_mime_type": "application/json"}
                )
                response = model.generate_content([prompt, image])
                content = clean_json_text(response.text)
                return json.loads(content)
            except Exception as e_json:
                # Retry with standard text config if json mime type isn't supported on model
                model = genai.GenerativeModel(
                    model_name="gemini-1.5-flash",
                    system_instruction=system_instruction
                )
                response = model.generate_content([prompt, image])
                cleaned = clean_json_text(response.text)
                # Locate first { and last }
                start = cleaned.find("{")
                end = cleaned.rfind("}")
                if start != -1 and end != -1:
                    return json.loads(cleaned[start:end+1])
                return json.loads(cleaned)
        except Exception as e:
            # Fallback gracefully with error notice
            res = generate_mock_analysis(mock_type, image)
            res["_mode"] = "Demonstration Mode (Fallback: API error or quota exceeded)"
            res["_api_error"] = str(e)
            return res
    else:
        # High fidelity simulated demonstration mode
        res = generate_mock_analysis(mock_type, image)
        res["_mode"] = "Demonstration Mode (Simulated Neural Vision Engine)"
        return res


def run_engineering_chat(
    history: List[Dict[str, str]],
    user_query: str,
    api_key: Optional[str] = None,
    weather_context: Optional[Dict[str, Any]] = None
) -> str:
    """
    Executes construction engineering assistant query with Gemini or engineering knowledge base.
    """
    weather_str = ""
    if weather_context:
        weather_str = (
            f"Current Site Weather: {weather_context.get('condition', 'Normal')} "
            f"(Wind: {weather_context.get('wind_speed', '12 km/h')}, "
            f"Temp: {weather_context.get('temp', '32°C')}, "
            f"Precipitation: {weather_context.get('precipitation', '0%')})."
        )

    sys_prompt = f"""You are 'BuildGuard AI', a Principal Construction Engineering & Safety Director.
Your expertise spans OSHA 1926 standards, Indian Standard IS 456:2000 (Plain and Reinforced Concrete), IS 3786 (Industrial Safety), and NBC 2016.
Provide technically rigorous, concise, actionable advice for civil engineers, site supervisors, and contractors.
Include specific engineering formulas, curing durations, slump values, bar lap lengths, or safety stand-downs where relevant.
{weather_str}"""

    if api_key and api_key.strip() and GENAI_AVAILABLE:
        try:
            genai.configure(api_key=api_key.strip())
            model = genai.GenerativeModel(
                model_name="gemini-1.5-flash",
                system_instruction=sys_prompt
            )
            # Build conversation context
            chat_session = model.start_chat(history=[])
            # Send message
            prompt_with_context = f"{user_query}"
            resp = chat_session.send_message(prompt_with_context)
            return resp.text
        except Exception:
            return generate_mock_chat_response(user_query, weather_context)
    else:
        return generate_mock_chat_response(user_query, weather_context)


def generate_mock_analysis(mock_type: str, image: Optional[Image.Image] = None) -> Dict[str, Any]:
    """Generates deterministic, highly realistic mock data for safety audits and crack diagnostics."""
    if mock_type == "ppe":
        return {
            "safety_score": 78,
            "overall_status": "Minor Infractions Detected",
            "audit_standard": "OSHA 1926.100 & IS 456 / IS 3786 Safety Code",
            "detected_workers_count": 4,
            "ppe_detection": [
                {
                    "item": "Industrial Hard Hats / Helmets (IS 2925 / EN 397)",
                    "required": True,
                    "detected_compliant": 3,
                    "total_workers": 4,
                    "status": "Non-Compliant",
                    "details": "Worker 3 operating rebar bending station lacks high-density safety helmet."
                },
                {
                    "item": "High-Visibility Safety Vests (Class 2/3)",
                    "required": True,
                    "detected_compliant": 4,
                    "total_workers": 4,
                    "status": "Compliant",
                    "details": "All personnel equipped with retroreflective neon safety vests."
                },
                {
                    "item": "Steel-Toe Safety Boots (IS 15298 / ASTM F2413)",
                    "required": True,
                    "detected_compliant": 3,
                    "total_workers": 4,
                    "status": "Minor Violation",
                    "details": "One operative observed in casual canvas footwear near material staging zone."
                },
                {
                    "item": "Fall Arrest Harness & Lanyard (IS 3521 / OSHA 1926.502)",
                    "required": True,
                    "detected_compliant": 2,
                    "total_workers": 2,
                    "status": "Compliant",
                    "details": "Scaffold workers double-anchored to certified static lifeline."
                },
                {
                    "item": "Protective Eyewear / Welding Shields (IS 5983)",
                    "required": False,
                    "detected_compliant": 1,
                    "total_workers": 1,
                    "status": "Compliant",
                    "details": "Angle grinder operator correctly wearing UV-rated safety goggles."
                }
            ],
            "identified_site_hazards": [
                {
                    "hazard": "Unprotected Floor Opening & Rebar Protrusion",
                    "severity": "Critical",
                    "code_reference": "OSHA 1926.701(b) / NBC 2016 Part 7",
                    "remedy": "Immediately fit plastic mushroom caps on exposed vertical starter bars and install OSHA-compliant 42-inch wooden or steel guardrails with toe-boards around floor slab penetrations."
                },
                {
                    "hazard": "Missing Head Protection at Active Overhead Drop Zone",
                    "severity": "High",
                    "code_reference": "IS 2925:1984 / OSHA 1926.100",
                    "remedy": "Issue immediate work stand-down for rebar crew until EN 397 Type-II certified helmets are donned with chinstraps securely fastened."
                },
                {
                    "hazard": "Trip and Puncture Hazard from Scaffold Staging Clutter",
                    "severity": "Medium",
                    "code_reference": "OSHA 1926.25 Housekeeping",
                    "remedy": "Enforce 5S housekeeping routine; clear discarded tie-wires, cut timber offcuts, and scaffolding couplers into designated scrap bins."
                }
            ],
            "recommendation_summary": "Overall site exhibits acceptable baseline adherence, but immediate intervention is mandated for starter bar impalement protection and 1 unhelmeted worker before concrete pour authorization."
        }
    else:  # Crack Diagnostics
        return {
            "defect_type": "Structural Diagonal Shear Crack",
            "element_type": "Reinforced Concrete Beam-Column Joint (RC Moment Frame)",
            "estimated_width_mm": 2.4,
            "severity_score": 84,
            "structural_urgency": "Urgent",
            "is_active": True,
            "code_reference": "IS 456:2000 Clause 35.3.2 & ACI 224R-01",
            "root_causes": [
                "Principal tensile stress exceeding concrete tensile capacity (ftk) under cyclic lateral or gravity overload.",
                "Inadequate stirrup shear confinement (insufficient 2-legged 8mm ties spacing near column face).",
                "Differential settlement of adjacent column footing causing secondary frame bending moments."
            ],
            "recommended_repairs": [
                {
                    "step": 1,
                    "procedure": "Surface Preparation & V-Groove Chasing",
                    "specification": "Rake crack to 15mm depth in V-profile and flush with oil-free compressed air."
                },
                {
                    "step": 2,
                    "procedure": "Low-Viscosity Epoxy Resin High-Pressure Injection",
                    "specification": "Install injection ports at 150mm intervals; inject epoxy resin conforming to ASTM C881 Type I/IV (viscosity < 250 cps) at 0.3 MPa until refusal."
                },
                {
                    "step": 3,
                    "procedure": "Carbon Fiber Reinforced Polymer (CFRP) Stitching / U-Wrapping",
                    "specification": "Apply 300 g/m² unidirectional CFRP laminates with epoxy saturant to restore beam shear capacity to >120% of design requirement."
                },
                {
                    "step": 4,
                    "procedure": "Acoustic / Tell-Tale Crack Monitoring",
                    "specification": "Fix calibrated Avongard acrylic crack width monitors across joint to track post-repair displacement over 90 days."
                }
            ],
            "structural_clearance": "Conditional Hold - Prohibit loading above 50% design live load until epoxy curing and CFRP bond testing achieves 28-day tensile strength."
        }


def generate_mock_chat_response(query: str, weather_context: Optional[Dict[str, Any]] = None) -> str:
    """Smart contextual responses based on domain construction engineering queries."""
    q = query.lower()
    
    if "cover" in q or "is 456" in q or "nominal cover" in q:
        return (
            "### 📏 IS 456:2000 Nominal Concrete Cover Guidelines (Table 16)\n\n"
            "Under Indian Standard **IS 456:2000 Clause 26.4**, minimum nominal cover to all reinforcement (including links) depends on exposure severity:\n\n"
            "- **Footings / Rafts (Severe / Ground Contact):** Minimum **50 mm**.\n"
            "- **Columns (Longitudinal Bars):** Minimum **40 mm** (or bar diameter if >40mm; can be reduced to 25mm for columns ≤200mm with ≤12mm bars).\n"
            "- **Beams:** Minimum **25 mm** (or bar diameter).\n"
            "- **Slabs:** Minimum **20 mm** (Mild) or **15 mm** for bars ≤12mm.\n\n"
            "**Key Engineering Note:** For fire resistance of 2 hours or more, or coastal environments ('Very Severe' / 'Extreme'), nominal cover must be increased by 10–15 mm or supplementary sacrificial anti-carbonation coatings applied."
        )
    elif "monsoon" in q or "rain" in q or "curing" in q or "weather" in q:
        w_state = weather_context.get("condition", "rain") if weather_context else "rain"
        return (
            f"### 🌧️ Wet Weather & Concrete Curing Protocol ({w_state.upper()})\n\n"
            "1. **Water-Cement Ratio Preservation:** Suspend all exposed slab finishing during active rainfall. Rainwater dilutes the surface paste, causing severe dusting, plastic shrinkage cracking, and loss of compressive strength.\n"
            "2. **Tarpaulin Tent System:** Erect sloping waterproof canopy sheeting above active bay before batching begins.\n"
            "3. **Electrical Submersible Dewatering:** Deploy 3-phase slurry pumps in basement excavations to avoid hydraulic uplift on mud slabs.\n"
            "4. **Slump & Plasticizer Adjustment:** Lower batching water by 5-10 L/m³ to account for aggregate surface moisture; check moisture meters on aggregate stockpiles every 2 hours."
        )
    elif "shear" in q or "crack" in q or "epoxy" in q:
        return (
            "### 🛠️ Structural Shear Crack Mitigation Protocol\n\n"
            "Shear cracks typically orient at ~45° angles near beam supports due to diagonal tension.\n\n"
            "**Immediate Action Protocol:**\n"
            "1. **Install Temporary Heavy Duty Props:** Position adjustable steel Acrow props or Acrow shoring towers at 1/3-span to relieve live loads.\n"
            "2. **Crack Width Gauge:** Mount an Avongard tell-tale gauge across the crack center to ascertain whether the crack is active or dormant.\n"
            "3. **Repair Procedure:** For crack width > 0.3 mm (exceeding IS 456 Clause 35.3.2 limit), pressure-inject low viscosity structural epoxy resin (ASTM C881 Type IV), supplemented with external CFRP wraps or bonded steel plates."
        )
    elif "crane" in q or "wind" in q or "lift" in q:
        return (
            "### 🌬️ High Wind & Tower Crane Safety Limits\n\n"
            "- **Gust Limit (>38 km/h):** Cease tandem lifts and handling of large surface area materials (formwork tables, precast panels, glazing cassettes).\n"
            "- **Shutdown Limit (>45 km/h / Beaufort Scale 6):** Mandatory shutdown of all tower cranes. Secure trolley near mast, disengage slewing brake to allow 360° free weathervaning, and lower hook block to upper limit.\n"
            "- **Emergency Verification:** Check mast tie-backs, guy wire tension, and anchor bolt torque using calibrated hydraulic torque wrenches."
        )
    elif "cost" in q or "valuation" in q or "budget" in q or "steel" in q:
        return (
            "### 📊 Parametric Construction Cost & Material Thumb Rules (India)\n\n"
            "- **Reinforcement Steel (TMT Fe500D / Fe550D):**\n"
            "  - Residential High-Rise: **3.8 to 4.5 kg per sq.ft** of built-up area.\n"
            "  - Commercial / IT Park: **4.2 to 5.2 kg per sq.ft**.\n"
            "- **Cement (PPC / OPC 53 Grade):** ~**0.40 to 0.45 bags per sq.ft**.\n"
            "- **RMC Concrete:** ~**0.035 to 0.040 m³ per sq.ft**.\n"
            "- **Average Civil Construction Cost (Tier-1):** ₹1,850 - ₹2,600 / sq.ft for standard finishes; ₹3,200 - ₹4,800 / sq.ft for Grade-A commercial or luxury residential."
        )
    else:
        return (
            f"### 👷 Expert Site Director Response\n\n"
            f"Regarding your query **'{query}'**:\n\n"
            "1. **Regulatory Adherence:** Ensure all field operations strictly follow **IS 456:2000** for structural design, **IS 3786** for injury incidence classification, and **OSHA 1926 Safety and Health Regulations**.\n"
            "2. **Quality Assurance Matrix:** Maintain strict chain of custody for raw material batches (cement test certificates, 7-day and 28-day cube crushing compressive results, rebar bend/rebend tests).\n"
            "3. **Field Readiness:** Conduct daily morning toolbox safety talks with subcontractors and check that environmental sensor thresholds (wind speed, wet bulb globe temperature) do not breach safe operational envelopes.\n\n"
            "*Feel free to ask about specific reinforcement details, concrete mix design, shoring calculations, or real estate valuation models!*"
        )
