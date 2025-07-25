import streamlit as st
import matplotlib.pyplot as plt

# --- Page Configuration ---#
st.set_page_config(page_title="Pollution Predictor", layout="centered")

# --- Custom Styling ---#
st.markdown('<p class="title">Air Pollution Level Predictor 🌫</p>', unsafe_allow_html=True)
st.markdown("""
    <style>
        .stApp {
            background: linear-gradient(to right, #e0f7fa, #e1f5fe);
            font-family: 'Segoe UI', sans-serif;
        }

        .stButton > button {
            background-color: #4CAF50;
            color: white;
            padding: 10px 24px;
            border: none;
            border-radius: 12px;
            font-size: 16px;
            font-weight: bold;
            margin-top: 10px;
            transition: 0.3s;
        }

        .stButton > button:hover {
            background-color: #45a049;
        }

        .stRadio > div, .stSelectbox > div {
            background-color: #ffffff;
            padding: 10px;
            border-radius: 10px;
            border: 1px solid #ccc;
        }

        input[type="number"] {
            border-radius: 8px !important;
            padding: 10px !important;
        }

        .stMarkdown h2 {
            color: #00695c;
        }

        .stMarkdown p {
            font-size: 18px;
        }
    </style>
""", unsafe_allow_html=True)

# --- Fixed Weights ---#
weights = {
    'so2': 0.5,
    'co2': 0.3,
    'pm10': 0.8,
    'pm25': 1.0,
    'temperature': 0.2,
    'bias': 5.0
}

st.title("🌍 Pollution Level Predictor")
st.markdown("Enter air quality parameters below to *predict the pollution index*.")

# --- Input Fields ---#
so2 = st.number_input("SO₂ (µg/m³)", min_value=0.0, format="%.2f")
co2 = st.number_input("CO₂ (ppm)", min_value=0.0, format="%.2f")
pm10 = st.number_input("PM10 (µg/m³)", min_value=0.0, format="%.2f")
pm25 = st.number_input("PM2.5 (µg/m³)", min_value=0.0, format="%.2f")

unit = st.selectbox("Select temperature unit", ["Celsius (°C)", "Fahrenheit (°F)", "Kelvin (K)"])
temperature_input = st.number_input(f"Temperature ({unit})", format="%.2f", help="Enter the temperature in the selected unit.")

# --- Unit Conversion ---#
if unit == "Fahrenheit (°F)":
    temperature = (temperature_input - 32) * 5 / 9
elif unit == "Kelvin (K)":
    temperature = temperature_input - 273.15
else:
    temperature = temperature_input

# --- Predict Button ---#
if st.button("🔍 Predict Pollution Level"):
    # Calculate Pollution Index
    pollution_index = (
        weights['so2'] * so2 +
        weights['co2'] * co2 +
        weights['pm10'] * pm10 +
        weights['pm25'] * pm25 +
        weights['temperature'] * temperature +
        weights['bias']
    )

    # --- Result Display ---#
    st.success(f"Predicted Pollution Level Index: *{pollution_index:.2f}*")

    # --- Calculation Breakdown ---#
    st.markdown("### 📊 Calculation Details:")
    st.code(f"""
Input Temperature: {temperature_input:.2f} {unit} → {temperature:.2f} °C

Pollution Level = (0.5 × {so2}) +
                  (0.3 × {co2}) +
                  (0.8 × {pm10}) +
                  (1.0 × {pm25}) +
                  (0.2 × {temperature:.2f}) + 5.0
                = {pollution_index:.2f}
""", language='python')

    # --- Interpretation ---#
    st.markdown("### 📉 Interpretation:")
    if pollution_index < 50:
        st.info("Air Quality: *Good (AQI < 50)* — Enjoy the fresh air! 😊")
    elif pollution_index < 100:
        st.warning("Air Quality: *Moderate (AQI 50–100)* — Acceptable but may affect sensitive groups.")
    else:
        st.error("Air Quality: *Unhealthy (AQI > 100)* — Limit outdoor activity. 😷")

    # --- Visualization ---#
    st.markdown("### 📈 Pollutant Levels Overview:")
    labels = ['SO₂', 'CO₂', 'PM10', 'PM2.5', 'Temp (°C)']
    values = [so2, co2, pm10, pm25, temperature]

    fig, ax = plt.subplots()
    ax.bar(labels, values, color=['#0288d1', '#388e3c', '#fbc02d', '#d32f2f', '#7b1fa2'])
    ax.set_ylabel("Concentration")
    ax.set_title("Air Pollutant Levels")
    st.pyplot(fig)

# --- Footer ---#
st.markdown("---")
st.caption("📌 This is a demo using fixed weights. For real predictions, integrate with a trained ML model.")