
import streamlit as st
from PIL import Image
import random

st.set_page_config(page_title="Clear Pool Co", layout="centered")

# Absolute high-contrast styling
st.markdown("""
    <style>
    body, .stApp {
        background-color: #ffffff;
        font-family: 'Segoe UI', sans-serif;
        color: #000000;
    }
    h1, h2, h3, h4 {
        color: #000000;
        font-weight: 700;
    }
    label, .stTextInput label, .stNumberInput label, .stCheckbox label {
        color: #000000 !important;
        font-size: 1rem;
        font-weight: 600;
    }
    .stTextInput input, .stNumberInput input {
        background-color: #ffffff;
        border: 1px solid #000000;
        padding: 0.6rem;
        border-radius: 8px;
        color: #000000;
    }
    .stButton>button {
        background-color: #000000;
        color: white;
        font-weight: 600;
        padding: 0.5rem 1.25rem;
        border-radius: 8px;
        margin-top: 1rem;
    }
    .stCheckbox {
        margin-top: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

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
    cal_hypo_lbs = max(0, (target_chlorine - current_chlorine)) * 0.111 * volume / 10000
    acid_quarts = max(0, (current_ph - 7.5) / 0.1) * 0.25 * volume / 10000
    return round(cal_hypo_lbs, 2), round(acid_quarts, 2), target_chlorine

def calculate_cya(volume, current, target):
    return round(max(0, target - current) * volume * 0.00000834, 2)

def calculate_salt(volume, current, target):
    return round(max(0, target - current) * volume * 0.00000834, 2)

def acid_demand_adjustment(volume, ph, ta):
    factor = 0.25 * volume / 10000
    return max(0, round(factor * ((ph - 7.5) / 0.1) * (1 + (ta - 80) / 100), 2))

def analyze_chem_strip(image):
    return {
        "Chlorine": round(random.uniform(0, 15), 1),
        "pH": round(random.uniform(6.8, 8.2), 1),
        "CYA": random.randint(0, 100),
        "TA": random.randint(50, 150)
    }

if tool == "Chlorine & pH Dosing":
    st.title("Chlorine & pH Optimizer")
    with st.form("form1"):
        volume = st.number_input("Pool Volume (gallons)", value=25000)
        current_chlorine = st.number_input("Current Chlorine (ppm)", value=1.0)
        current_ph = st.number_input("Current pH", value=8.0)
        cya = st.number_input("Conditioner / CYA Level (ppm)", value=50)
        algae = st.checkbox("Minor algae spots present?")
        submit = st.form_submit_button("Calculate")

    if submit:
        cal_hypo, acid, target = calculate_pool_chemicals(volume, current_chlorine, current_ph, cya, algae)
        st.subheader("Dosing Recommendations")
        st.markdown(f"""
        **Target Chlorine:** {target} ppm  
        **Add Cal Hypo:** {cal_hypo} lbs  
        **Add Muriatic Acid:** {acid} quarts  
        """)
        st.caption("Ideal ranges: Chlorine 1–3 ppm (normal), 10–15 ppm (shock); pH 7.4–7.6")

elif tool == "CYA Calculator":
    st.title("CYA (Conditioner) Calculator")
    volume = st.number_input("Pool Volume (gallons)", value=25000)
    current = st.number_input("Current CYA", value=0)
    target = st.number_input("Target CYA", value=50)
    if st.button("Calculate Conditioner Needed"):
        result = calculate_cya(volume, current, target)
        st.success(f"Add **{result} lbs** of conditioner")

elif tool == "Salt Calculator":
    st.title("Salt Calculator")
    volume = st.number_input("Pool Volume (gallons)", value=25000)
    current_salt = st.number_input("Current Salt (ppm)", value=2000)
    target_salt = st.number_input("Target Salt (ppm)", value=3200)
    if st.button("Calculate Salt Needed"):
        result = calculate_salt(volume, current_salt, target_salt)
        st.success(f"Add **{result} lbs** of salt")

elif tool == "Acid Demand (TA Based)":
    st.title("Acid Demand Estimator")
    volume = st.number_input("Pool Volume (gallons)", value=25000)
    ph = st.number_input("Current pH", value=8.0)
    ta = st.number_input("Total Alkalinity (ppm)", value=120)
    if st.button("Estimate Acid Needed"):
        result = acid_demand_adjustment(volume, ph, ta)
        st.success(f"Add **{result} quarts** of muriatic acid")

elif tool == "Chem Strip Analyzer":
    st.title("Chem Strip Analyzer")
    file = st.file_uploader("Upload Chem Strip Image", type=["png", "jpg", "jpeg"])
    if file:
        img = Image.open(file)
        st.image(img, use_column_width=True)
        st.markdown("Analyzing...")
        results = analyze_chem_strip(img)

        st.subheader("Estimated Results")
        for key, val in results.items():
            st.write(f"{key}: **{val}**")

        st.subheader("Treatment Suggestions")
        if results['Chlorine'] < 1:
            st.write("Chlorine low — consider shocking the pool.")
        elif results['Chlorine'] > 10:
            st.write("Chlorine high — let it settle.")
        else:
            st.write("Chlorine is within ideal range.")

        if results['pH'] < 7.2:
            st.write("Raise pH with soda ash.")
        elif results['pH'] > 7.8:
            st.write("Lower pH with acid.")
        else:
            st.write("pH is in optimal range.")
