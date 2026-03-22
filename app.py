import streamlit as st
from PIL import Image
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import os
from dotenv import load_dotenv

from image_analysis import analyse_rooftop
from ai_analysis import analyse_rooftop_with_ai, get_suitability_color, get_shading_adjustment
from roi_calculator import calculate_solar_estimates
from pdf_report import generate_pdf_report
from data.india_data import CITY_SOLAR_DATA, STATE_ELECTRICITY_RATES, PANEL_TYPES
from utils import format_inr

load_dotenv()

st.set_page_config(
    page_title="Solar AI Assistant",
    page_icon="☀️",
    layout="wide",
    initial_sidebar_state="expanded"
)


st.markdown("""
<style>
    .main-title {
        font-size: 2.5rem;
        font-weight: 800;
        color: #FF8C00;
        text-align: center;
        margin-bottom: 0;
    }
    .subtitle {
        font-size: 1rem;
        color: #888;
        text-align: center;
        margin-bottom: 2rem;
    }
    .section-header {
        font-size: 1.2rem;
        font-weight: 700;
        color: #FF8C00;
        border-left: 4px solid #FF8C00;
        padding-left: 10px;
        margin: 1.5rem 0 1rem 0;
    }
    .ai-card {
        background: rgba(0, 39, 101, 0.15);
        border-radius: 10px;
        padding: 1rem;
        border-left: 4px solid #FF8C00;
        line-height: 2;
    }
    .stDownloadButton button {
        background-color: #FF8C00 !important;
        color: white !important;
        font-weight: bold !important;
        border-radius: 8px !important;
        width: 100% !important;
    }
</style>
""", unsafe_allow_html=True)


st.markdown('<p class="main-title">☀️ Solar AI Assistant</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">AI-powered rooftop analysis for solar panel installation in India</p>', unsafe_allow_html=True)


with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/sun.png", width=80)
    st.title("Configuration")

    st.subheader("📍 Location")
    city = st.selectbox("Select your city", list(CITY_SOLAR_DATA.keys()))
    city_data = CITY_SOLAR_DATA[city]
    state = city_data["state"]
    electricity_rate = STATE_ELECTRICITY_RATES.get(state, 7.0)

    st.info(f"🏛️ State: **{state}**\n\n⚡ Rate: **₹{electricity_rate}/kWh**\n\n☀️ Sun Hours: **{city_data['sun_hours']} hrs/day**")

    st.subheader("🔲 Panel Type")
    panel_type = st.selectbox("Select panel type", list(PANEL_TYPES.keys()))
    panel_info = PANEL_TYPES[panel_type]
    st.info(f"⚡ {panel_info['watt']}W | ₹{panel_info['cost']:,}/panel\n\n{panel_info['description']}")

    st.subheader("📥 Input Method")
    input_method = st.radio("Choose:", ["Upload Rooftop Image", "Enter Area Manually"])

    api_key = os.getenv("ANTHROPIC_API_KEY", "")

    st.markdown("---")
    st.markdown("**How to use:**")
    st.markdown("1. Select your city & panel type\n2. Upload image or enter area\n3. Get full solar estimates\n4. Download PDF report")


area_m2 = 0
ai_data = None
image_used = False

if input_method == "Upload Rooftop Image":
    st.markdown('<p class="section-header">📤 Upload Rooftop Image</p>', unsafe_allow_html=True)
    uploaded = st.file_uploader("Upload a satellite or top-down image of your rooftop",
                                 type=["jpg", "jpeg", "png"])

    if uploaded:
        pil_img = Image.open(uploaded).convert("RGB")
        col1, col2 = st.columns(2)
        with col1:
            st.image(pil_img, caption="Uploaded Image", use_container_width=True)

        with st.spinner("🔍 Detecting rooftop area..."):
            mask, area_m2, overlay = analyse_rooftop(pil_img)

        if area_m2 == 0:
            st.error("❌ No rooftop detected. Try a clearer satellite/top-down image.")
        else:
            with col2:
                if overlay is not None:
                    st.image(overlay, caption=f"Detected Rooftop — {area_m2} m²",
                             use_container_width=True)
            image_used = True
            st.success(f"✅ Rooftop detected! Usable area: **{area_m2} m²**")

        if image_used:
            if not api_key:
                st.info("💡 Add your ANTHROPIC_API_KEY in the .env file to enable AI analysis.")
            else:
                st.markdown('<p class="section-header">🧠 AI Rooftop Analysis</p>', unsafe_allow_html=True)
                with st.spinner("🤖 Claude AI is analysing your rooftop..."):
                    ai_data, error = analyse_rooftop_with_ai(pil_img, api_key)

                if error:
                    st.warning(f"⚠️ AI Analysis failed: {error}")
                elif ai_data:
                    suitability_icon = get_suitability_color(ai_data.get("solar_suitability", ""))
                    shading_adj = get_shading_adjustment(ai_data.get("shading_level", "none"))

                    col1, col2, col3, col4 = st.columns(4)
                    col1.metric("Roof Type",  ai_data.get("roof_type", "N/A").capitalize())
                    col2.metric("Shading",    ai_data.get("shading_level", "N/A").capitalize())
                    col3.metric("Condition",  ai_data.get("roof_condition", "N/A").capitalize())
                    col4.metric("Confidence", f"{round(ai_data.get('confidence', 0) * 100, 1)}%")

                    st.markdown(f"""
                    <div class="ai-card">
                        <b>Solar Suitability:</b> {suitability_icon} {ai_data.get('solar_suitability','').capitalize()}<br>
                        <b>Orientation:</b> {ai_data.get('orientation','N/A').capitalize()}<br>
                        <b>Obstacles:</b> {', '.join(ai_data.get('obstacles', [])) or 'None detected'}<br>
                        <b>Recommendation:</b> {ai_data.get('recommended_placement','N/A')}
                    </div>
                    """, unsafe_allow_html=True)

                    if shading_adj < 1.0:
                        st.info(f"ℹ️ Energy output adjusted by **{int(shading_adj*100)}%** due to shading.")
                        area_m2 = round(area_m2 * shading_adj, 2)

else:
    st.markdown('<p class="section-header">📐 Enter Rooftop Area</p>', unsafe_allow_html=True)
    area_m2 = st.number_input("Enter your rooftop area (m²):", min_value=0.0,
                               max_value=5000.0, step=1.0, value=50.0)
    if area_m2 > 0:
        st.success(f"✅ Rooftop area set to **{area_m2} m²**")


if area_m2 > 0:
    results = calculate_solar_estimates(area_m2, city_data, panel_type, electricity_rate)

    if results is None:
        st.error("❌ Rooftop area too small to fit even one solar panel.")
    else:
        st.markdown('<p class="section-header">🔋 Solar Installation Overview</p>', unsafe_allow_html=True)
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Solar Panels",   f"{results['num_panels']}")
        col2.metric("System Size",    f"{results['system_kw']} kW")
        col3.metric("Energy/Year",    f"{format_inr(results['energy_kwh_year'])} kWh")
        col4.metric("Payback Period", f"{results['payback_years']} yrs")

        st.markdown('<p class="section-header">💰 Financial Estimates</p>', unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Installation Cost", format_inr(results['install_cost']))
            st.metric("Govt Subsidy (PM Surya Ghar)", format_inr(results['subsidy']))
            st.metric("Net Cost", format_inr(results['net_cost']))

        with col2:
            st.metric("Yearly Savings",     format_inr(results['yearly_savings']))
            st.metric("Yearly Maintenance", format_inr(results['yearly_maintenance']))
            st.metric("Net Yearly Savings", format_inr(results['net_yearly_savings']))

        with col3:
            st.metric("ROI",              f"{results['roi_percent']}%")
            st.metric("Lifetime Savings", format_inr(results['total_lifetime_savings']))
            st.metric("CO₂ Saved/Year",   f"{results['co2_kg']:,.0f} kg")

        st.markdown('<p class="section-header">📊 Charts & Projections</p>', unsafe_allow_html=True)
        tab1, tab2, tab3 = st.tabs(["📈 ROI Projection", "🌤️ Monthly Energy", "💸 Cost Breakdown"])

        chart_layout = dict(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#cccccc"),
            xaxis=dict(gridcolor="rgba(255,255,255,0.1)"),
            yaxis=dict(gridcolor="rgba(255,255,255,0.1)"),
        )

        with tab1:
            projection_df = pd.DataFrame(results["yearly_projection"])
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=projection_df["year"],
                y=projection_df["cumulative"],
                mode="lines+markers",
                name="Cumulative Savings",
                line=dict(color="#FF8C00", width=3),
                marker=dict(size=6),
                fill="tozeroy",
                fillcolor="rgba(255,140,0,0.15)"
            ))
            fig.add_hline(y=0, line_dash="dash", line_color="#ff4444",
                          annotation_text="Break-even point",
                          annotation_font_color="#ff4444")
            fig.update_layout(
                title=dict(text=f"{panel_type} — 25 Year ROI Projection", font=dict(color="#FF8C00")),
                xaxis_title="Year",
                yaxis_title="Cumulative Savings (₹)",
                hovermode="x unified",
                **chart_layout
            )
            st.plotly_chart(fig, use_container_width=True)

        with tab2:
            monthly_df = pd.DataFrame(
                list(results["monthly_energy"].items()),
                columns=["Month", "Energy (kWh)"]
            )
            fig2 = px.bar(
                monthly_df, x="Month", y="Energy (kWh)",
                title="Monthly Energy Production (kWh)",
                color="Energy (kWh)",
                color_continuous_scale="Oranges"
            )
            fig2.update_layout(**chart_layout)
            fig2.update_layout(
                title=dict(font=dict(color="#FF8C00")),
                coloraxis_colorbar=dict(
                    tickfont=dict(color="#cccccc"),
                    title=dict(font=dict(color="#cccccc"))
                )
            )
            st.plotly_chart(fig2, use_container_width=True)

        with tab3:
            fig3 = go.Figure(go.Pie(
                labels=["Panel Cost", "Labor Cost"],
                values=[results["panel_cost"], results["labor_cost"]],
                hole=0.4,
                marker_colors=["#FF8C00", "#002765"],
                textfont=dict(color="white", size=14)
            ))
            fig3.update_layout(
                title=dict(text="Installation Cost Breakdown", font=dict(color="#FF8C00")),
                legend=dict(font=dict(color="#cccccc")),
                **chart_layout
            )
            st.plotly_chart(fig3, use_container_width=True)

        st.markdown('<p class="section-header">🌱 Environmental Impact</p>', unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        col1.metric("CO₂ Saved/Year",     f"{results['co2_kg']:,.0f} kg")
        col2.metric("CO₂ (Tonnes/Year)",  f"{results['co2_tonnes']} t")
        col3.metric("Carbon Credit Value", format_inr(results['carbon_credit_value']) + "/yr")

        st.markdown('<p class="section-header">📄 Download Report</p>', unsafe_allow_html=True)
        pdf_buffer = generate_pdf_report(results, ai_data, city, panel_type, area_m2)
        st.download_button(
            label="📥 Download Full PDF Report",
            data=pdf_buffer,
            file_name=f"solar_report_{city.lower()}_{panel_type.lower()}.pdf",
            mime="application/pdf"
        )
