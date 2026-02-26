import streamlit as st
import pandas as pd
from datetime import datetime
import os

# -----------------------------------
# PAGE CONFIG
# -----------------------------------
st.set_page_config(
    page_title="Insulin Dose Calculator",
    layout="centered"
)

# -----------------------------------
# MOBILE STYLING
# -----------------------------------
st.markdown("""
<style>
.stButton>button {
    width: 100%;
    background-color: #0F62FE;
    color: white;
    font-size: 18px;
    padding: 14px;
    border-radius: 12px;
    border: none;
}
.stNumberInput input {
    font-size: 18px !important;
}
.block-container {
    padding-top: 2rem;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------------
# TITLE
# -----------------------------------
st.title("💙 Insulin Dose Calculator")
st.caption("Based on prescribed insulin regimen")

st.divider()

# -----------------------------------
# INPUT SECTION
# -----------------------------------
blood_sugar = st.number_input(
    "Current Blood Sugar (mg/dL)",
    min_value=0,
    step=1
)

carbs = st.number_input(
    "Carbohydrates You Will Eat (grams)",
    min_value=0,
    step=1
)

st.divider()

# -----------------------------------
# CALCULATION BUTTON
# -----------------------------------
if st.button("Calculate Dose"):

    # ---------------------------
    # LOW BLOOD SUGAR SAFETY
    # ---------------------------
    if blood_sugar < 70:
        st.error("⚠️ LOW BLOOD SUGAR")
        st.success("Eat 15 grams of fast-acting carbohydrates immediately.")
        st.info("Examples: juice, glucose tablets, regular soda.")
        st.info("Recheck blood sugar in 15 minutes.")
        st.stop()

    # ---------------------------
    # CARB COVERAGE
    # ---------------------------
    carb_ratio = 10
    carb_dose = carbs / carb_ratio

    # ---------------------------
    # CORRECTION SCALE
    # ---------------------------
    if blood_sugar < 150:
        correction_dose = 0
    elif 150 <= blood_sugar <= 190:
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
    else:
        correction_dose = 7

    # ---------------------------
    # TOTAL DOSE (rounded)
    # ---------------------------
    total_dose = round(carb_dose + correction_dose)

    if total_dose < 0:
        total_dose = 0

    # ---------------------------
    # HIGH SUGAR WARNING
    # ---------------------------
    if blood_sugar > 300:
        st.warning("⚠️ Very high blood sugar. Monitor closely and consider ketone check.")

    # ---------------------------
    # DISPLAY RESULTS
    # ---------------------------
    st.success(f"Recommended Humalog Dose: {total_dose} units")

    st.info(f"""
Carb Coverage: {round(carb_dose,2)} units  
Correction Dose: {correction_dose} units
""")

    st.caption("I love you. Please take care of your health 💙")

    # ---------------------------
    # SAVE HISTORY
    # ---------------------------
    data = {
        "Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Blood Sugar": blood_sugar,
        "Carbs (g)": carbs,
        "Carb Dose": round(carb_dose,2),
        "Correction Dose": correction_dose,
        "Total Dose": total_dose
    }

    file_path = "insulin_log.csv"

    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
        df = pd.concat([df, pd.DataFrame([data])], ignore_index=True)
    else:
        df = pd.DataFrame([data])

    df.to_csv(file_path, index=False)

# -----------------------------------
# HISTORY SECTION
# -----------------------------------
st.divider()
st.subheader("📊 Dose History")

file_path = "insulin_log.csv"

if os.path.exists(file_path):
    df = pd.read_csv(file_path)
    st.dataframe(df, use_container_width=True)

    if len(df) > 0:
        df["Time"] = pd.to_datetime(df["Time"])
        df = df.sort_values("Time")
        st.line_chart(df.set_index("Time")["Total Dose"])
else:
    st.info("No records yet.")

# -----------------------------------
# BASAL INSULIN INFO (Display Only)
# -----------------------------------
st.divider()
st.subheader("🟢 Basal Insulin Schedule")

st.write("Morning: 10 units — Glargine-yfgn (Semglee)")
st.write("Evening: 14 units — Glargine-yfgn (Semglee)")

st.caption("Follow physician instructions strictly.")
