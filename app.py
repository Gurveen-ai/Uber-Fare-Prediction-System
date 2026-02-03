import streamlit as st
import numpy as np
from joblib import load
from geopy.distance import geodesic

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Uber Fare Prediction Pro",
    layout="centered"
)

# ---------------- LOAD MODEL ----------------
@st.cache_resource
def load_model():
    return load("uber_fare_model.pkl")

model = load_model()

# ---------------- HEADER ----------------
st.markdown("""
<div style="text-align:center">
    <h1> Uber Fare Prediction Pro</h1>
    
</div>
""", unsafe_allow_html=True)

st.divider()

# ---------------- INPUT MODE ----------------
st.subheader("Trip Location Mode")
mode = st.radio("Choose input type:", ["Manual Distance", "Coordinates (Map-Based)"])

# ---------------- INPUT SECTION ----------------
st.subheader("Trip Details")

col1, col2 = st.columns(2)

with col1:
    passengers = st.selectbox("Passengers", [1, 2, 3, 4, 5, 6])
    hour = st.slider("Pickup Hour (0-23)", 0, 23)
    surge = st.slider("Surge Multiplier", 1.0, 3.0, 1.0, 0.1)

with col2:
    day = st.slider("Day of Month", 1, 31)
    month = st.slider("Month", 1, 12)

# ---------------- DISTANCE INPUT ----------------
distance = 0

if mode == "Manual Distance":
    distance = st.number_input("Distance (km)", min_value=0.5, step=0.1)
else:
    st.markdown("###  Pickup Coordinates")
    plat = st.number_input("Pickup Latitude", format="%.6f")
    plon = st.number_input("Pickup Longitude", format="%.6f")

    st.markdown("###  Drop Coordinates")
    dlat = st.number_input("Drop Latitude", format="%.6f")
    dlon = st.number_input("Drop Longitude", format="%.6f")

    if plat and plon and dlat and dlon:
        distance = round(geodesic((plat, plon), (dlat, dlon)).km, 2)
        st.info(f" Calculated Distance: {distance} km")

st.divider()

# ---------------- PREDICTION ----------------
if st.button(" Predict Fare", use_container_width=True):

    input_data = np.array([[distance, passengers, hour, day, month]])
    base_fare = float(model.predict(input_data)[0])

    final_fare = round(base_fare * surge, 2)

    # ---------------- DISPLAY RESULTS ----------------
    st.success(" Fare Predicted Successfully!")

    col1, col2, col3 = st.columns(3)

    col1.metric("Base Fare", f"₹{round(base_fare, 2)}")
    col2.metric("Surge Multiplier", f"x{surge}")
    col3.metric("Final Fare", f"₹{final_fare}")

    st.markdown("###  Trip Summary")
    st.write(f"""
    -  Distance: **{distance} km**
    -  Passengers: **{passengers}**
    -  Pickup Time: **{hour}:00**
    -  Date: **{day}/{month}**
    """)

# ---------------- FOOTER ----------------
st.markdown("""
<hr>
<div style="text-align:center; color:gray;">
    Built with Machine Learning, Geolocation & Streamlit | Portfolio Project
</div>
""", unsafe_allow_html=True)
