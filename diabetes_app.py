import streamlit as st

st.title("💙 Personal Diabetes Calculator")

st.write("Enter values based on doctor's instructions.")

blood_sugar = st.number_input("Current Blood Sugar (mg/dL)", min_value=0)
target_sugar = st.number_input("Target Blood Sugar (mg/dL)", value=100)
correction_factor = st.number_input("Correction Factor (1 unit lowers by how much)", min_value=1)

carbs = st.number_input("Carbs to Eat (grams)", min_value=0)
carb_ratio = st.number_input("Carb Ratio (grams per 1 unit insulin)", min_value=1)

if st.button("Calculate"):

    correction = 0
    if blood_sugar > target_sugar:
        correction = (blood_sugar - target_sugar) / correction_factor

    carb_dose = carbs / carb_ratio
    total = correction + carb_dose

    st.subheader("Results")
    st.write("Correction Dose:", round(correction, 2), "units")
    st.write("Carb Dose:", round(carb_dose, 2), "units")
    st.success("Total Suggested Dose: " + str(round(total, 2)) + " units")

    st.warning("⚠️ Always confirm with medical advice.")