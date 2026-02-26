import streamlit as st
import pandas as pd
from datetime import datetime
st.line_chart(df.set_index("Time")["Dose"])

# ----------------------------
# PAGE CONFIG (Mobile Friendly)
# ----------------------------
st.set_page_config(
    page_title="Diabetes Assistant",
    layout="centered"  # Better for mobile
)

st.title("💙 Diabetes Assistant")
st.caption("Personal use only — follow doctor's instructions.")

# ----------------------------
# INPUTS (Stacked for Mobile)
# ----------------------------
blood_sugar = st.number_input("Current Blood Sugar (mg/dL)", min_value=0)
carbs = st.number_input("Carbohydrates (grams)", min_value=0)

# Fixed regimen
carb_ratio = 10  # 1 unit per 10g carbs

# ----------------------------
# CALCULATIONS
# ----------------------------
carb_dose = carbs / carb_ratio
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

total_dose = round(carb_dose + correction_dose)

# Safety check
if total_dose > 20:
    st.warning("⚠️ High dose — please verify.")

# ----------------------------
# BIG RESULT DISPLAY (Mobile Friendly)
# ----------------------------
st.divider()

if st.button("🧮 Calculate Dose", use_container_width=True):

    st.success(f"Recommended Humalog Dose: {total_dose} units")

    st.write("Carb Dose:", round(carb_dose, 2), "units")
    st.write("Correction Dose:", correction_dose, "units")

    # Save history
    if "history" not in st.session_state:
        st.session_state.history = []

    st.session_state.history.append({
        "Time": datetime.now(),
        "Blood Sugar": blood_sugar,
        "Carbs": carbs,
        "Dose": total_dose
    })

# ----------------------------
# HISTORY (Simplified for Mobile)
# ----------------------------
if "history" in st.session_state and len(st.session_state.history) > 0:

    st.divider()
    st.subheader("📊 Recent Doses")

    df = pd.DataFrame(st.session_state.history)
    st.dataframe(df, use_container_width=True)

    # Simple Graph
    st.subheader("Dose Trend")

    fig, ax = plt.subplots()
    ax.plot(df["Time"], df["Dose"], marker="o")
    ax.set_xlabel("Time")
    ax.set_ylabel("Units")
    plt.xticks(rotation=45)

    st.pyplot(fig)

# ----------------------------
# BASAL INFO (Compact)
# ----------------------------
st.divider()
st.subheader("Basal Insulin Schedule")

st.write("Morning: 10 units")
st.write("Evening: 14 units")

