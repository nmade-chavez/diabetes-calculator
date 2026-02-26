import streamlit as st
from datetime import datetime

st.title("Personal Diabetes Calculator")

st.header("Meal Bolus Calculator (Humalog)")

# Inputs
blood_sugar = st.number_input("Current Blood Sugar (mg/dL)", min_value=0)
carbs = st.number_input("Carbohydrates (grams)", min_value=0)

# Fixed regimen
carb_ratio = 10  # 1 unit per 10g carbs

# ----- Carb Dose -----
carb_dose = carbs / carb_ratio

# ----- Correction Scale -----
correction_dose = 0

if blood_sugar >= 150:
    if 150 <= blood_sugar <= 190:
        correction_dose = 1
    elif 191 <= blood_sugar <= 230:
        correction_dose = 2
    elif 231 <= blood_sugar <= 270:
        correction_dose = 3
    elif 271 <= blood_sugar <= 310:
        correction_dose = 4
    elif 311 <= blood_sugar <= 350:
        correction_dose = 5
    elif 351 <= blood_sugar <= 390:
        correction_dose = 6
    elif blood_sugar > 390:
        correction_dose = 7

# ----- Total Dose -----
total_dose = carb_dose + correction_dose

# Round to whole units (as requested)
total_dose = round(total_dose)

# Safety limits
if total_dose < 0:
    total_dose = 0

if total_dose > 20:
    st.warning("Dose is unusually high. Please verify with healthcare provider.⚠️ ")

# Display results
if st.button("Calculate Dose"):
    st.subheader("Results")
    st.write("Carb Dose:", round(carb_dose, 2), "units")
    st.write("Correction Dose:", correction_dose, "units")
    st.success("Total Humalog Dose (Rounded): " + str(total_dose) + " units")

    # Simple logging
    log_entry = f"{datetime.now()} | BG: {blood_sugar} | Carbs: {carbs}g | Dose: {total_dose}u\n"

    with open("dose_log.txt", "a") as f:
        f.write(log_entry)

    st.info("Entry saved to local log file.")

# ----- Basal Insulin Reminder -----
st.header("Basal Insulin (Semglee)")

st.write("Morning: 10 units")
st.write("Evening: 14 units")

st.caption("Always confirm doses with medical guidance.⚠️ ")
