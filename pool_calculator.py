
import streamlit as st
from PIL import Image
import random

# App Configuration
st.set_page_config(page_title="Clear Pool Co", layout="centered", initial_sidebar_state="expanded")

# Premium Visual Styling
st.markdown("""
    <style>
    body {
        background-color: #f4f4f5;
        font-family: 'Segoe UI', sans-serif;
        color: #1f2937;
    }
    .stApp {
        background-color: #ffffff;
        border-radius: 16px;
        padding: 2rem;
        margin: auto;
        max-width: 800px;
        box-shadow: 0px 4px 20px rgba(0, 0, 0, 0.05);
    }
    h1, h2, h3 {
        color: #111827;
        font-weight: 600;
    }
    .stButton > button {
        background-color: #2563eb;
        color: white;
        font-weight: bold;
        padding: 0.5rem 1.5rem;
        border-radius: 10px;
        border: none;
    }
    .stNumberInput input {
        border-radius: 10px;
        padding: 0.4rem;
    }
    .stFileUploader {
        border: 1px solid #d1d5db;
        border-radius: 10px;
    }
    .stCheckbox > label {
        font-weight: 500;
    }
    </style>
""", unsafe_allow_html=True)

# Navigation
tool = st.sidebar.radio("Tool", [
    "Chlorine & pH Dosing",
    "CYA Calculator",
    "Salt Calculator",
    "Acid Demand (TA Based)",
    "Chem Strip Analyzer"
])

def calculate_pool_chemicals(volume, current_chlorine, current_ph, cya=50, has_algae=False):
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

    cal_hypo_lbs_per_ppm = 0.111 * volume / 10000
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

# Tool Pages
if tool == "Chlorine & pH Dosing":
    st.title("Chlorine & pH Optimizer")
    with st.form("chlorine_form"):
        volume = st.number_input("Pool Volume (gallons)", value=25000)
        current_chlorine = st.number_input("Current Chlorine Level (ppm)", value=1.0)
        current_ph = st.number_input("Current pH", value=8.0)
        cya = st.number_input("Conditioner / CYA (ppm)", value=50)
        has_algae = st.checkbox("Minor algae spots?")
        submit = st.form_submit_button("Calculate")

    if submit:
        cal_hypo, acid, target = calculate_pool_chemicals(volume, current_chlorine, current_ph, cya, has_algae)
        st.success("Dosing Recommendation")
        st.markdown(f"""
        - **Target Chlorine Level**: {target} ppm  
        - **Cal Hypo Needed**: {cal_hypo} lbs  
        - **Muriatic Acid Needed**: {acid} quarts  
        """)
        st.caption("Ideal Ranges — Chlorine: 1–3 ppm (daily), 10–15 ppm (shock); pH: 7.4–7.6")

elif tool == "CYA Calculator":
    st.title("CYA (Stabilizer) Calculator")
    volume = st.number_input("Pool Volume (gallons)", value=25000)
    current = st.number_input("Current CYA (ppm)", value=0)
    target = st.number_input("Target CYA (ppm)", value=50)
    if st.button("Calculate CYA Needed"):
        cya_needed = calculate_cya(volume, current, target)
        st.success(f"Add **{cya_needed} lbs** of conditioner")

elif tool == "Salt Calculator":
    st.title("Salt Level Calculator")
    volume = st.number_input("Pool Volume (gallons)", value=25000)
    current_salt = st.number_input("Current Salt (ppm)", value=2000)
    target_salt = st.number_input("Target Salt (ppm)", value=3200)
    if st.button("Calculate Salt Needed"):
        salt_needed = calculate_salt(volume, current_salt, target_salt)
        st.success(f"Add **{salt_needed} lbs** of salt")

elif tool == "Acid Demand (TA Based)":
    st.title("Acid Demand Estimator")
    volume = st.number_input("Pool Volume (gallons)", value=25000)
    ph = st.number_input("Current pH", value=8.0)
    ta = st.number_input("Total Alkalinity (ppm)", value=120)
    if st.button("Estimate Acid"):
        acid = acid_demand_adjustment(volume, ph, ta)
        st.success(f"Estimated acid required: **{acid} quarts**")

elif tool == "Chem Strip Analyzer":
    st.title("Chem Strip Snapshot")
    file = st.file_uploader("Upload a chem strip photo", type=["jpg", "png", "jpeg"])
    if file:
        img = Image.open(file)
        st.image(img, use_column_width=True)
        st.info("Analyzing strip...")
        result = analyze_chem_strip(img)

        st.markdown("### Strip Results")
        for k, v in result.items():
            st.write(f"- {k}: **{v}**")

        st.markdown("### Treatment Suggestions")
        if result['Chlorine'] < 1:
            st.write("**Add chlorine** — levels are too low.")
        elif result['Chlorine'] > 10:
            st.write("**Let chlorine settle** — too high for now.")
        else:
            st.write("Chlorine is within ideal range.")

        if result['pH'] < 7.2:
            st.write("Raise pH using soda ash")
        elif result['pH'] > 7.8:
            st.write("Lower pH using muriatic acid")
        else:
            st.write("pH is within ideal range.")
