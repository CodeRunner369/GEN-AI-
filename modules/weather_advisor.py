"""
Module: Daily Site Assistant & Weather-Aware Advisory (Epic 5)
Provides dynamic weather risk protocols, OSHA/IS 456 environmental stand-down directives,
and an interactive multi-turn construction engineering chatbot.
"""

from datetime import datetime
import streamlit as st
from typing import Dict, Any, Optional

from modules.ai_engine import run_engineering_chat
from modules.ui_components import render_hazard_card

WEATHER_PROTOCOLS = {
    "High Wind (>45 km/h / Gale Force)": {
        "condition": "High Wind",
        "wind_speed": "48 km/h",
        "temp": "28°C",
        "precipitation": "0%",
        "status_level": "Critical",
        "alerts": [
            {
                "title": "Mandatory Tower Crane & Hoist Suspension",
                "severity": "Critical",
                "rule": "OSHA 1926.1431 / IS 13367 (Cranes Code)",
                "remedy": "Immediately halt all tower crane lifting, jib movements, and exterior material hoists. Release slewing brake to enable 360° free weathervaning. Secure suspended hook blocks at upper travel limit."
            },
            {
                "title": "Scaffolding & Formwork Wind Tie Inspection",
                "severity": "High",
                "rule": "IS 4014 (Code of Practice for Steel Tubular Scaffolding)",
                "remedy": "Inspect all exterior debris netting and advertising banners—temporarily drop or slit mesh to reduce catastrophic wind sail load on perimeter scaffold frames."
            },
            {
                "title": "Cessation of Elevated External Work",
                "severity": "High",
                "rule": "OSHA 1926.501 Fall Protection",
                "remedy": "Suspend all curtain wall glazing, cradle gondola operations, and exterior painting above 3 meters height."
            }
        ],
        "curing_notes": "Rapid surface evaporation will accelerate plastic shrinkage cracking. Apply aliphatic alcohol evaporation retarders or seal with 100-micron polyethylene sheeting immediately post-troweling."
    },
    "Heavy Monsoon Rain (>50 mm/hr)": {
        "condition": "Heavy Rain",
        "wind_speed": "22 km/h",
        "temp": "25°C",
        "precipitation": "95%",
        "status_level": "Critical",
        "alerts": [
            {
                "title": "Unprotected Concrete Pour Stand-Down",
                "severity": "Critical",
                "rule": "IS 456:2000 Clause 13.3 (Concreting in Inclement Weather)",
                "remedy": "Prohibit pouring of open horizontal slabs without waterproof tenting. Rainwater increases effective water-cement ratio, drastically weakening compressive strength and causing severe dusting."
            },
            {
                "title": "Excavation Pit & Trench Cave-in Watch",
                "severity": "Critical",
                "rule": "OSHA 1926.651 Specific Excavation Requirements",
                "remedy": "Inspect soil slopes and shoring sheet piles for hydrostatic pressure buildup. Evacuate basement trenches if water ponding exceeds 100mm and activate automatic submersible slurry dewatering."
            },
            {
                "title": "Electrical Power Distribution Ground Fault Isolation",
                "severity": "High",
                "rule": "IS 732 / OSHA 1926.404 Wiring Design & Protection",
                "remedy": "Verify all 415V temporary power panels have active 30mA residual current circuit breakers (RCCB/ELCB). Disconnect all non-waterproof extension cables."
            }
        ],
        "curing_notes": "Naturally moist conditions aid hydration, but newly placed concrete must be shielded from rainwater erosion until reaching initial setting time (min 2.5 hours)."
    },
    "Extreme Heat (>42°C / Severe Sun)": {
        "condition": "Extreme Heat",
        "wind_speed": "14 km/h",
        "temp": "44°C",
        "precipitation": "5%",
        "status_level": "High",
        "alerts": [
            {
                "title": "Hot-Weather Concreting & Thermal Cracking Protocol",
                "severity": "High",
                "rule": "ACI 305R (Hot Weather Concreting) & IS 7861 (Part 1)",
                "remedy": "Concrete discharge temperature must not exceed 32°C. Mandate crushed ice batching water replacement, liquid nitrogen precooling, or night pours (8:00 PM to 4:00 AM)."
            },
            {
                "title": "Continuous Wet Curing Mandate",
                "severity": "High",
                "rule": "IS 456:2000 Clause 13.5 Curing",
                "remedy": "Extend wet burlap curing period to 14 days minimum. Keep saturated burlap continuously damp; apply white pigmented liquid membrane-forming curing compound (ASTM C309 Type 2)."
            },
            {
                "title": "Heat Stress Mitigation & Worker Shift Rotation",
                "severity": "High",
                "rule": "OSHA Heat Illness Prevention Directive",
                "remedy": "Enforce 45-minute work / 15-minute shaded rest cycles. Provide chilled electrolyte replenishment stations and station designated first-aid personnel trained in heatstroke identification."
            }
        ],
        "curing_notes": "Rapid hydration generates high peak temperatures. Ensure temperature differential between concrete core and surface does not exceed 20°C to avoid thermal cracking."
    },
    "Normal / Moderate Conditions (24°C - 30°C)": {
        "condition": "Normal",
        "wind_speed": "12 km/h",
        "temp": "27°C",
        "precipitation": "10%",
        "status_level": "Low",
        "alerts": [
            {
                "title": "Standard Operating Safety Envelope",
                "severity": "Low",
                "rule": "OSHA 1926 & NBC 2016",
                "remedy": "Optimal atmospheric conditions for continuous tower crane operation, exterior cladding, and standard 7-day ponding/wet-burlap concrete curing."
            },
            {
                "title": "Daily Routine Housekeeping & Barricading",
                "severity": "Low",
                "rule": "IS 3786 Safety Audits",
                "remedy": "Maintain regular 5S floor clearing and perimeter barricade checks at shaft penetrations."
            }
        ],
        "curing_notes": "Standard wet curing protocol: Maintain continuous ponding on flat slabs or saturated hessian cloth on vertical columns for minimum 7 days (OPC) or 10 days (pozzolanic PPC)."
    },
    "Dense Fog / Poor Visibility (<50 m)": {
        "condition": "Dense Fog",
        "wind_speed": "5 km/h",
        "temp": "16°C",
        "precipitation": "80%",
        "status_level": "Medium",
        "alerts": [
            {
                "title": "Blind Lift Restriction & Radiotelephone Mandate",
                "severity": "High",
                "rule": "OSHA 1926.1419 Signals",
                "remedy": "Cease all blind lifts where rigger/banksman lacks direct visual line-of-sight to crane hook. Require dual-band certified radio communications with dedicated channel."
            },
            {
                "title": "Vehicular & Heavy Machinery Perimeter Lighting",
                "severity": "Medium",
                "rule": "IS 13367 Construction Safety Code",
                "remedy": "Activate rotating amber warning beacons on all transit mixers, backhoes, and mobile cranes. Deploy high-output LED floodlight towers at site ingress/egress gates."
            }
        ],
        "curing_notes": "High humidity slows evaporation; beware delayed concrete setting times and surface condensates before waterproofing membrane application."
    }
}


def render_weather_tab(api_key: Optional[str]):
    """Renders the Tab 4 Daily Site Assistant & Weather-Aware Advisory interface."""
    st.subheader("🌦️ Daily Site Assistant & Weather-Aware Advisory (Epic 5)")
    st.caption("Real-time environmental risk matrix, automated safety stand-downs (wind/rain/heat), and multi-turn engineering chatbot.")

    col_w1, col_w2 = st.columns([1.1, 1.4])

    with col_w1:
        st.markdown("#### 📡 Environmental Sensor & Weather Selector")
        selected_weather_label = st.selectbox(
            "Current Site Weather State:",
            list(WEATHER_PROTOCOLS.keys()),
            index=0
        )
        weather_info = WEATHER_PROTOCOLS[selected_weather_label]

        st.markdown(f"""
        <div style="background: #1E293B; border-radius: 10px; padding: 16px; margin-top: 12px; border: 1px solid rgba(255,255,255,0.08);">
            <div style="display:flex; justify-content:space-between; margin-bottom:8px;">
                <span style="color:#94A3B8; font-size:13px;">Ambient Temperature:</span>
                <strong style="color:#F8FAFC;">{weather_info['temp']}</strong>
            </div>
            <div style="display:flex; justify-content:space-between; margin-bottom:8px;">
                <span style="color:#94A3B8; font-size:13px;">Wind Speed & Gusts:</span>
                <strong style="color:{'#EF4444' if 'Wind' in selected_weather_label else '#F8FAFC'};">{weather_info['wind_speed']}</strong>
            </div>
            <div style="display:flex; justify-content:space-between; margin-bottom:8px;">
                <span style="color:#94A3B8; font-size:13px;">Precipitation Probability:</span>
                <strong style="color:{'#38BDF8' if 'Rain' in selected_weather_label else '#F8FAFC'};">{weather_info['precipitation']}</strong>
            </div>
            <div style="display:flex; justify-content:space-between;">
                <span style="color:#94A3B8; font-size:13px;">Site Advisory Level:</span>
                <strong style="color:{'#EF4444' if weather_info['status_level']=='Critical' else '#F59E0B'};">{weather_info['status_level'].upper()} ALERT</strong>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("#### 🧪 Concrete Hydration & Curing Protocol")
        st.info(weather_info["curing_notes"])

    with col_w2:
        st.markdown("#### 🚨 Dynamic Operational Protocols & Stand-Down Alerts")
        for alert in weather_info["alerts"]:
            render_hazard_card(
                title=alert["title"],
                severity=alert["severity"],
                remedy=alert["remedy"],
                rule=alert["rule"]
            )

    st.markdown("---")

    # Multi-turn Interactive Construction Engineering Assistant Chatbot
    st.subheader("💬 BuildGuard Engineering Assistant (Multi-Turn Chatbot)")
    st.caption("Civil engineering, IS 456 / OSHA regulations, reinforcement detailing, and site troubleshooting companion.")

    # Preset chips
    st.markdown("**Quick Technical Prompts:**")
    preset_cols = st.columns(4)
    preset_clicked = None
    with preset_cols[0]:
        if st.button("📏 IS 456 Minimum Cover", use_container_width=True):
            preset_clicked = "What are the minimum concrete cover requirements under IS 456 for beams, columns, and foundations?"
    with preset_cols[1]:
        if st.button("🌧️ Monsoon Pour Precautions", use_container_width=True):
            preset_clicked = "What are the required field precautions and slump adjustments for pouring concrete during monsoon rain?"
    with preset_cols[2]:
        if st.button("🛠️ Shear Crack Shoring", use_container_width=True):
            preset_clicked = "How should we shore and epoxy-inject a 2.5mm 45-degree diagonal shear crack at a beam-column joint?"
    with preset_cols[3]:
        if st.button("🏗️ Tower Crane Wind Limit", use_container_width=True):
            preset_clicked = "What is the maximum wind speed allowable before shutting down tower cranes under OSHA and IS codes?"

    # Chat history state
    if "chat_messages" not in st.session_state:
        st.session_state["chat_messages"] = [
            {
                "role": "assistant",
                "content": "Hello Engineer! I am **BuildGuard AI**, your certified construction engineering and safety director. How can I assist you with site safety, IS 456/OSHA compliance, structural repairs, or material estimations today?",
                "time": datetime.now().strftime("%H:%M")
            }
        ]

    # Render previous messages
    for msg in st.session_state["chat_messages"]:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            if "time" in msg:
                st.caption(f"Sent at {msg['time']}")

    # Handle Input (via text input or chip click)
    user_prompt = st.chat_input("Ask BuildGuard AI any civil engineering, safety, or structural question...")
    
    # If chip was clicked, treat as prompt
    active_prompt = preset_clicked if preset_clicked else user_prompt

    if active_prompt:
        current_time = datetime.now().strftime("%H:%M")
        # Add user message
        st.session_state["chat_messages"].append({
            "role": "user",
            "content": active_prompt,
            "time": current_time
        })
        with st.chat_message("user"):
            st.markdown(active_prompt)
            st.caption(f"Sent at {current_time}")

        # Generate response
        with st.chat_message("assistant"):
            with st.spinner("👷 BuildGuard AI reviewing engineering standards..."):
                resp_text = run_engineering_chat(
                    history=st.session_state["chat_messages"],
                    user_query=active_prompt,
                    api_key=api_key,
                    weather_context=weather_info
                )
                st.markdown(resp_text)
                st.caption(f"Sent at {datetime.now().strftime('%H:%M')}")

        st.session_state["chat_messages"].append({
            "role": "assistant",
            "content": resp_text,
            "time": datetime.now().strftime("%H:%M")
        })

    # Clear chat utility
    st.markdown("<br>", unsafe_allow_html=True)
    c_btn1, c_btn2 = st.columns([1, 4])
    with c_btn1:
        if st.button("🗑️ Clear Chat History"):
            st.session_state["chat_messages"] = [
                {
                    "role": "assistant",
                    "content": "Chat history cleared. Ready for your next engineering inquiry.",
                    "time": datetime.now().strftime("%H:%M")
                }
            ]
            st.rerun()
