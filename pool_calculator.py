
import streamlit as st

def calculate_pool_chemicals(pool_volume_gallons, current_chlorine_ppm, current_ph):
    cal_hypo_required_per_ppm = 0.013 * pool_volume_gallons / 10000
    acid_required_per_ph_point = 0.25 * pool_volume_gallons / 10000

    target_chlorine_ppm = 3
    target_ph = 7.5

    chlorine_needed_ppm = max(0, target_chlorine_ppm - current_chlorine_ppm)
    cal_hypo_lbs = chlorine_needed_ppm * cal_hypo_required_per_ppm

    ph_difference = max(0, current_ph - target_ph)
    acid_quarts = (ph_difference / 0.1) * acid_required_per_ph_point

    return {
        "calcium_hypochlorite_lbs": round(cal_hypo_lbs, 2),
        "muriatic_acid_quarts": round(acid_quarts, 2)
    }

st.title("Pool Chemical Dosing Calculator")

pool_volume = st.number_input("Pool Volume (gallons)", min_value=1000, max_value=100000, value=25000, step=1000)
current_chlorine = st.number_input("Current Chlorine (ppm)", min_value=0.0, max_value=10.0, value=0.0, step=0.1)
current_ph = st.number_input("Current pH", min_value=6.0, max_value=9.0, value=8.0, step=0.1)

if st.button("Calculate Dosing"):
    dosing = calculate_pool_chemicals(pool_volume, current_chlorine, current_ph)
    st.subheader("Add:")
    st.write(f"- {dosing['calcium_hypochlorite_lbs']} lbs of Cal Hypo")
    st.write(f"- {dosing['muriatic_acid_quarts']} quarts of Muriatic Acid")
