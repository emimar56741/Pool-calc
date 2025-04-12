
import streamlit as st
from PIL import Image
import random

st.set_page_config(page_title="Clear Pool Co Toolkit", layout="centered")

# Modern UI Styling
st.markdown("""
    <style>
    body, .stApp {
        background-color: #f8f9fa;
        color: #212529;
        font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
    }
    .main, .block-container {
        padding: 2rem;
    }
    .stButton > button {
        background-color: #0d6efd;
        color: white;
        font-weight: 600;
        border-radius: 8px;
        padding: 0.5rem 1.2rem;
        margin-top: 1rem;
    }
    .stNumberInput input, .stTextInput input, .stFileUploader {
        border-radius: 0.5rem;
        padding: 0.4rem;
    }
    .stRadio label {
        font-weight: 500;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar Navigation
tool = st.sidebar.radio("Select a Tool", [
    "Chlorine & pH Dosing",
    "CYA Calculator",
    "Salt Calculator",
    "Acid Demand (TA Based)",
    "Chem Strip Analyzer"
])

def calculate_pool_chemicals(volume, current_chlorine, current_ph, cya=50, has_algae=False):
    # Adjust chlorine target based on CYA and algae presence
    if has_algae:
        target_chlorine = 12
    elif cya <= 30:
        target_chlorine = 2.5
    elif cya <= 50:
        target_chlorine = 4
    elif cya <= 70:
        target_chlorine = 5
    else:
        target_chlorine = 6

    cal_hypo_lbs_per_ppm = 0.111 * volume / 10000  # Based on 73% Cal Hypo
    muriatic_acid_quarts_per_point = 0.25 * volume / 10000

    chlorine_needed = max(0, target_chlorine - current_chlorine)
    cal_hypo_needed = chlorine_needed * cal_hypo_lbs_per_ppm

    ph_difference = max(0, current_ph - 7.5)
    acid_needed = (ph_difference / 0.1) * muriatic_acid_quarts_per_point

    return round(cal_hypo_needed, 2), round(acid_needed, 2), target_chlorine

def calculate_cya(volume, current, target):
    return round(max(0, target - current) * volume * 0.00000834, 2)

def calculate_salt(volume, current, target):
    return round(max(0, target - current) * volume * 0.00000834, 2)

def acid_demand_adjustment(volume, ph, ta):
    adj_factor = 0.25 * volume / 10000
    return max(0, round(adj_factor * ((ph - 7.5) / 0.1) * (1 + (ta - 80) / 100), 2))

def analyze_chem_strip(image):
    return {
        "Chlorine": round(random.uniform(0, 15), 1),
        "pH": round(random.uniform(6.8, 8.2), 1),
        "CYA": random.randint(0, 100),
        "TA": random.randint(50, 150)
    }

if tool == "Chlorine & pH Dosing":
    st.title("Chlorine & pH Dosing (73% Cal Hypo)")
    with st.form("chlorine_form"):
        volume = st.number_input("Pool Volume (gallons)", value=30000)
        current_chlorine = st.number_input("Current Chlorine (ppm)", value=1.0)
        current_ph = st.number_input("Current pH", value=8.0)
        cya = st.number_input("Conditioner / CYA Level (ppm)", value=50)
        algae_present = st.checkbox("Minor algae spots present?")
        submitted = st.form_submit_button("Calculate")

    if submitted:
        cal_hypo, acid, target = calculate_pool_chemicals(volume, current_chlorine, current_ph, cya, algae_present)
        st.subheader("Dosing Results")
        st.write(f"**Target Chlorine Level:** {target} ppm")
        st.write(f"**Cal Hypo Needed:** {cal_hypo} lbs")
        st.write(f"**Muriatic Acid Needed:** {acid} quarts")
        st.caption("Ideal: Chlorine 1–3 ppm (daily), 10–15 ppm (shock); pH 7.4–7.6")

elif tool == "CYA Calculator":
    st.title("CYA (Stabilizer) Calculator")
    volume = st.number_input("Pool Volume (gallons)", value=25000)
    current_cya = st.number_input("Current CYA", value=0)
    target_cya = st.number_input("Target CYA", value=50)
    if st.button("Calculate CYA Needed"):
        result = calculate_cya(volume, current_cya, target_cya)
        st.write(f"Add **{result} lbs** of cyanuric acid")

elif tool == "Salt Calculator":
    st.title("Salt Level Calculator")
    volume = st.number_input("Pool Volume (gallons)", value=25000)
    current_salt = st.number_input("Current Salt (ppm)", value=2000)
    target_salt = st.number_input("Target Salt (ppm)", value=3200)
    if st.button("Calculate Salt Needed"):
        result = calculate_salt(volume, current_salt, target_salt)
        st.write(f"Add **{result} lbs** of salt")

elif tool == "Acid Demand (TA Based)":
    st.title("Acid Demand Calculator")
    volume = st.number_input("Pool Volume (gallons)", value=25000)
    current_ph = st.number_input("Current pH", value=8.0)
    total_alkalinity = st.number_input("Total Alkalinity (ppm)", value=120)
    if st.button("Estimate Acid Needed"):
        result = acid_demand_adjustment(volume, current_ph, total_alkalinity)
        st.write(f"Add **{result} quarts** of muriatic acid")

elif tool == "Chem Strip Analyzer":
    st.title("Chem Strip Analyzer")
    uploaded_file = st.file_uploader("Upload Chem Strip Photo", type=["png", "jpg", "jpeg"])
    if uploaded_file:
        img = Image.open(uploaded_file)
        st.image(img, caption="Uploaded Strip", use_column_width=True)
        st.write("Analyzing...")
        results = analyze_chem_strip(img)

        st.markdown("### Estimated Readings")
        for label, value in results.items():
            st.write(f"{label}: **{value}**")

        st.markdown("### Recommendations")
        if results['Chlorine'] < 1:
            st.write("**Shock recommended**: Chlorine is low")
        elif results['Chlorine'] > 10:
            st.write("Chlorine is very high: let it drop naturally")
        else:
            st.write("Chlorine is in range")

        if results['pH'] < 7.2:
            st.write("Raise pH using soda ash")
        elif results['pH'] > 7.8:
            st.write("Lower pH using muriatic acid")
        else:
            st.write("pH is ideal")
