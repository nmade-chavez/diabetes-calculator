import streamlit as st
import pandas as pd
from datetime import datetime
import os

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="Diabetes Care Dashboard",
    layout="centered"
)

# -----------------------------
# PROFESSIONAL MOBILE STYLE
# -----------------------------
st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
        background-color: #2563eb;
        color: white;
        font-size: 18px;
        padding: 12px;
        border-radius: 12px;
        border: none;
    }
    .stNumberInput>div>div>input {
        font-size: 18px;
    }
    </style>
""", unsafe_allow_html=True)

# -----------------------------
# TITLE
# -----------------------------
st.title("Diabetes Care Dashboard 💙 ")
st.caption("Personal medical tool — follow physician instructions.")

st.divider()

# -----------------------------
# INPUTS
# -----------------------------
blood_sugar = st.number_input(
    "Current Blood Sugar (mg/dL)",
    min_value=0,
    step=1
)

carbs = st.number_input(
    "Carbohydrates (grams)",
    min_value=0,
    step=1
)

st.divider()

# -----------------------------
# CALCULATION BUTTON
# -----------------------------
if st.button("Calculate"):

    carb_ratio = 10  # 1 unit per 10g carbs

    # -----------------------------
    # LOW BLOOD SUGAR LOGIC
    # -----------------------------
    if blood_sugar < 70:
        st.error("⚠️ LOW BLOOD SUGAR")
        st.success("Eat 15 grams of fast-acting carbohydrates immediately.")
        st.info("Recheck blood sugar in 15 minutes.")
    
    else:
        # -----------------------------
        # CARB COVERAGE
        # -----------------------------
        carb_dose = carbs / carb_ratio

        # -----------------------------
        # EXACT CORRECTION SCALE
        # -----------------------------
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

        total_dose = round(carb_dose + correction_dose)

        st.success(f"Recommended Humalog Dose: {total_dose} units")
        st.info(f"Carb Coverage: {round(carb_dose,2)} units")
        st.info(f"Correction Dose: {correction_dose} units")

        if blood_sugar > 300:
            st.warning("⚠️ Very high blood sugar — monitor closely.")

    # -----------------------------
    # SAFETY WARNINGS
    # -----------------------------
    if blood_sugar < 70:
        st.error("⚠️ Blood sugar is LOW (<70). Treat hypoglycemia before insulin.")
    elif blood_sugar > 300:
        st.warning("⚠️ Blood sugar very high (>300). Monitor closely.")

    if total_dose > 25:
        st.warning("⚠️ High insulin dose. Verify before injecting.")

    # -----------------------------
    # DISPLAY RESULT
    # -----------------------------
    st.success(f"Recommended Humalog Dose: {total_dose} units")

    st.info(f"""
    Carb Coverage: {round(carb_dose, 2)} units  
    Correction Dose: {correction_dose} units  
    """)

    # -----------------------------
    # SAVE TO CSV
    # -----------------------------
    data = {
        "Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Blood Sugar": blood_sugar,
        "Carbs": carbs,
        "Carb Dose": round(carb_dose, 2),
        "Correction Dose": correction_dose,
        "Total Dose": total_dose
    }

    file_path = "glucose_log.csv"

    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
        df = pd.concat([df, pd.DataFrame([data])], ignore_index=True)
    else:
        df = pd.DataFrame([data])

    df.to_csv(file_path, index=False)

# -----------------------------
# HISTORY SECTION
# -----------------------------
st.divider()
st.subheader("📊 Dose History")

file_path = "glucose_log.csv"

if os.path.exists(file_path):
    df = pd.read_csv(file_path)

    st.dataframe(df, use_container_width=True)

    if len(df) > 0:
        df["Time"] = pd.to_datetime(df["Time"])
        df = df.sort_values("Time")
        st.line_chart(df.set_index("Time")["Total Dose"])
else:
    st.info("No records yet.")

# -----------------------------
# BASAL INSULIN INFO
# -----------------------------
st.divider()
st.subheader("🟢 Basal Insulin Schedule")

st.write("Morning: 10 units (Glargine-yfgn / Semglee)")
st.write("Evening: 14 units (Glargine-yfgn / Semglee)")

st.caption("Follow prescribed insulin regimen strictly.")


