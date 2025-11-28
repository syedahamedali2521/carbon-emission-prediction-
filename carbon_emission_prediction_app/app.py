import streamlit as st
import pickle
import pandas as pd
import plotly.graph_objects as go
from utils.preprocess import preprocess_input
from fpdf import FPDF
import datetime

# Load model
with open('carbon_emission_prediction_app/model/model.pkl', 'rb') as f:
    model = pickle.load(f)

# Page config
st.set_page_config(page_title="Carbon Emission Predictor", page_icon="🌱", layout="wide")

# Custom CSS for green/dark theme
st.markdown("""
<style>
    /* Main Page Background */
    .main {
        background-color: #000000 !important;
        color: #39FF14 !important;
    }

    /* Global Text */
    body, .stTextInput, .stSelectbox, .stNumberInput, .stMarkdown, label {
        color: #39FF14 !important;
    }

    /* Buttons */
    .stButton>button {
        background-color: #39FF14 !important;
        color: black !important;
        border-radius: 10px !important;
        border: none !important;
        padding: 10px 20px !important;
        font-size: 16px !important;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #2ECC10 !important;
        color: #000 !important;
    }

    /* Glass Card */
    .card {
        background: rgba(57, 255, 20, 0.05);
        border: 1px solid rgba(57, 255, 20, 0.2);
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0;
        backdrop-filter: blur(10px);
        color: #39FF14 !important;
    }

    /* Prediction Text */
    .prediction {
        font-size: 48px;
        font-weight: bold;
        color: #39FF14 !important;
        text-shadow: 0 0 10px #39FF14;
        text-align: center;
    }

    /* Sidebar */
    .sidebar .sidebar-content {
        background-color: #000000 !important;
        color: #39FF14 !important;
    }
    .sidebar .sidebar-content * {
        color: #39FF14 !important;
    }
</style>
""", unsafe_allow_html=True)


# Title
st.title("🌱 Carbon Emission Prediction App")
st.markdown("Predict your carbon footprint and get tips to reduce it!")

# Sidebar inputs
st.sidebar.header("Input Parameters")
fuel_consumption = st.sidebar.slider("Fuel Consumption (L/100km)", 5.0, 20.0, 10.0)
vehicle_type = st.sidebar.selectbox("Vehicle Type", ["car", "truck", "bus"])
distance = st.sidebar.slider("Distance Traveled (km)", 10, 500, 100)
engine_size = st.sidebar.slider("Engine Size (cc)", 1000, 5000, 2000)
country_factor = st.sidebar.slider("Country Emission Factor", 1.0, 5.0, 2.5)

# Predict button
if st.sidebar.button("Predict Emissions"):
    input_data = preprocess_input(fuel_consumption, vehicle_type, distance, engine_size, country_factor)
    prediction = model.predict(input_data)[0]
    
    # Store in session state for history
    if 'history' not in st.session_state:
        st.session_state.history = []
    st.session_state.history.append({
        'date': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'prediction': prediction,
        'inputs': {
            'fuel': fuel_consumption,
            'vehicle': vehicle_type,
            'distance': distance,
            'engine': engine_size,
            'country': country_factor
        }
    })

    # Main panel
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown(f"<div class='card'><h2>Predicted Carbon Emission</h2><div class='prediction'>{prediction:.2f} g CO₂</div></div>", unsafe_allow_html=True)
        
        # Gauge
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=prediction,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Emission Level"},
            gauge={'axis': {'range': [None, 200]},
                   'bar': {'color': "#4CAF50"},
                   'steps': [
                       {'range': [0, 50], 'color': "lightgreen"},
                       {'range': [50, 100], 'color': "yellow"},
                       {'range': [100, 150], 'color': "orange"},
                       {'range': [150, 200], 'color': "red"}]}
        ))
        st.plotly_chart(fig)
        
        # Tips
        st.markdown("<div class='card'><h3>Tips to Reduce Emissions</h3>", unsafe_allow_html=True)
        tips = [
            "Use public transport or carpool to reduce fuel consumption.",
            "Maintain your vehicle for better fuel efficiency.",
            "Consider electric or hybrid vehicles.",
            "Reduce unnecessary trips and combine errands."
        ]
        for tip in tips:
            st.markdown(f"- {tip}")
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        # Comparison chart
        avg_emission = 120  # hypothetical average
        fig2 = go.Figure()
        fig2.add_trace(go.Bar(x=['Your Emission', 'Average Emission'], y=[prediction, avg_emission], marker_color=['#4CAF50', '#FFA500']))
        fig2.update_layout(title="Comparison with Average", yaxis_title="g CO₂")
        st.plotly_chart(fig2)
        
        # Export PDF
        if st.button("Export Report as PDF"):
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            pdf.cell(200, 10, txt="Carbon Emission Report", ln=True, align='C')
            pdf.cell(200, 10, txt=f"Predicted Emission: {prediction:.2f} g CO₂", ln=True)
            pdf.cell(200, 10, txt=f"Fuel Consumption: {fuel_consumption} L/100km", ln=True)
            pdf.cell(200, 10, txt=f"Vehicle Type: {vehicle_type}", ln=True)
            pdf.cell(200, 10, txt=f"Distance: {distance} km", ln=True)
            pdf.cell(200, 10, txt=f"Engine Size: {engine_size} cc", ln=True)
            pdf.cell(200, 10, txt=f"Country Factor: {country_factor}", ln=True)
            pdf.output("emission_report.pdf")
            st.success("Report exported as emission_report.pdf")

# History
if 'history' in st.session_state and st.session_state.history:
    st.header("Prediction History")
    history_df = pd.DataFrame(st.session_state.history)
    st.dataframe(history_df[['date', 'prediction']])

# Footer
st.markdown("---")
st.markdown("Built with ❤️ for a greener future.")
st.markdown("Built by ❤️ Syed Ahamed Ali.")
