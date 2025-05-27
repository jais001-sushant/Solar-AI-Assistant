import streamlit as st
from PIL import Image
import numpy as np
import cv2
from image_analysis import analyse_rooftop
from roi_calculator import calculate_solar_estimates
from ai_simulation import simulate_ai_rooftop_analysis

st.set_page_config(page_title="Solar Industry AI Assistant", layout="wide")
st.title("☀️ Solar Industry AI Assistant")

# Sidebar instructions
st.sidebar.header("Instructions")
st.sidebar.markdown("""
1. Choose how you want to input your rooftop area.<br>
2. Either upload a clear satellite/top-down image of your roof, **or** enter area manually.<br>
3. Get detailed solar panel, energy, financial, and environmental estimates.<br>
4. Plus AI-generated roof type, shading, and confidence.
""", unsafe_allow_html=True)

# Input method selection
st.sidebar.subheader("Choose Input Method")
input_method = st.sidebar.radio("Input type:", ["Upload Image", "Enter Area Manually"])

area = 0  # default
image_used = False  # track if image uploaded

if input_method == "Upload Image":
    uploaded = st.file_uploader("📤 Upload rooftop image (jpg/png)", type=["jpg", "jpeg", "png"])

    if uploaded:
        pil_img = Image.open(uploaded).convert("RGB")
        st.image(pil_img, caption="Uploaded image", use_column_width=True)

        st.subheader("🔍 Analyzing rooftop…")
        mask, area = analyse_rooftop(pil_img)

        if area == 0:
            st.error("No rooftop detected. Try another image or adjust the detection method.")
        else:
            image_used = True
            # Create semi-transparent mask overlay
            mask_rgb = cv2.cvtColor(mask, cv2.COLOR_GRAY2RGB)
            blended = cv2.addWeighted(np.array(pil_img), 1.0, mask_rgb, 0.4, 0)
            st.image(blended, caption=f"Detected rooftop — usable area ≈ **{area:.2f} m²**", use_column_width=True)

elif input_method == "Enter Area Manually":
    area = st.number_input("🏠 Enter your rooftop area (m²):", min_value=0.0, step=1.0)

# Only run if area is entered or detected
if area > 0:
    st.success(f"Estimated usable roof area: **{area:.2f} m²**")

    # Run simulated AI analysis if image was used
    if image_used:
        ai_data = simulate_ai_rooftop_analysis()
        st.header("🧠 AI Rooftop Insights")
        st.markdown(f"- **Roof Type:** {ai_data['roof_type'].capitalize()}")
        st.markdown(f"- **Shading Level:** {ai_data['shading'].capitalize()}")
        st.markdown(f"- **Confidence Score:** {ai_data['confidence']}")

    # Solar and financial calculations
    results = calculate_solar_estimates(area)

    st.header("🔋 Solar Panel Installation Potential")
    st.markdown(f"- Number of panels that can fit: **{results['num_panels']}**")
    st.markdown(f"- Estimated energy production: **{results['energy_output_kwh']:.2f} kWh/year**")

    st.header("💰 Financial & Environmental Estimates")
    st.markdown(f"- Total installation cost: **₹{results['install_cost']:,.2f}**")
    st.markdown(f"- Yearly maintenance cost: **₹{results['yearly_maintenance']:,.2f}**")
    st.markdown(f"- Yearly electricity savings: **₹{results['yearly_savings']:,.2f}**")
    st.markdown(f"- Estimated payback period: **{results['payback_years']} years**")
    st.markdown(f"- Estimated ROI: **{results['roi_percent']:.2f}%**")
    st.markdown(f"- Estimated CO₂ emissions saved: **{results['co2_savings']:,.0f} kg/year**")

