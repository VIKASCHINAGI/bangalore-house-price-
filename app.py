import streamlit as st
import pandas as pd
import joblib
from PIL import Image
import base64
import numpy as np
import os

# File paths (use relative paths, not local system paths)
MODEL_PATH = 'Project.joblib'
DATA_PATH = 'Cleaned_data.csv'
IMAGE_PATH = 'house.png'

# Load the trained model
model = joblib.load(MODEL_PATH)

# Load the data for dropdowns
data = pd.read_csv(DATA_PATH)

# Encode background image to base64
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        return base64.b64encode(f.read()).decode()

# Set background image in Streamlit
def set_bg_image(image_file):
    bin_str = get_base64_of_bin_file(image_file)
    page_bg_img = f"""
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{bin_str}");
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    </style>
    """
    st.markdown(page_bg_img, unsafe_allow_html=True)

# Set the custom background image
set_bg_image(IMAGE_PATH)

# App title and description
st.title('🏠 Bangalore House Price Predictor')
st.markdown("Predict house prices based on location, area, and amenities in Bangalore.")

# Sidebar: Additional Amenities
st.sidebar.header("✨ Additional Amenities")
parking = st.sidebar.selectbox('🚗 Car Parking', [0, 1, 2, 3])
gym = st.sidebar.checkbox("🏋️‍♂️ Gym")
pool = st.sidebar.checkbox("🏊‍♀️ Swimming Pool")
security = st.sidebar.checkbox("🔒 Security Services")

# Main inputs
loc = st.selectbox('📍 Choose the Location', sorted(data['location'].unique()))
sqft = st.number_input('📐 Total Square Feet', min_value=300.0, max_value=10000.0, step=50.0)
beds = st.number_input('🛏 Number of Bedrooms', min_value=1.0, max_value=10.0, step=1.0)
bath = st.number_input('🛁 Number of Bathrooms', min_value=1.0, max_value=10.0, step=1.0)
balc = st.number_input('🌇 Number of Balconies', min_value=0.0, max_value=5.0, step=1.0)

# Prediction button
if st.button("📊 Predict Price"):
    st.subheader("🔍 Input Summary")
    st.markdown(f"""
    - *Location*: **{loc}**  
    - *Area*: **{sqft} sqft**  
    - *Bedrooms*: **{beds}**  
    - *Bathrooms*: **{bath}**  
    - *Balconies*: **{balc}**  
    - *Parking Slots*: **{parking}**  
    - *Gym*: {'Yes' if gym else 'No'}  
    - *Swimming Pool*: {'Yes' if pool else 'No'}  
    - *Security*: {'Yes' if security else 'No'}  
    """, unsafe_allow_html=True)

    # Construct the input DataFrame
    input_df = pd.DataFrame({
        'location': [loc],
        'total_sqft': [sqft],
        'bath': [bath],
        'balcony': [balc],
        'bedrooms': [beds],
        'parking': [parking],
        'gym': [int(gym)],
        'pool': [int(pool)],
        'security': [int(security)]
    })

    try:
        prediction = model.predict(input_df)[0]  # prediction in lakhs
        st.success(f"💵 Estimated Price: ₹ {prediction * 100:,.0f} Thousands")
    except Exception as e:
        st.error(f"❌ Prediction failed. Error: {e}")
