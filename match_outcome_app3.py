
import streamlit as st
import joblib
import numpy as np

# Load model
model = joblib.load("match_outcome_model_retrained.pkl")

st.set_page_config(page_title="Match Outcome Predictor", page_icon="🏏")
st.title("🏏 Match Outcome Predictor (2nd Innings)")

st.markdown("Predict whether the chasing team will win the match based on current match conditions.")

# Inputs
current_score = st.slider("🏏 Current Score", 0, 500, value=150)
wickets_in_hand = st.slider("🧤 Wickets Remaining", 0, 10, value=7)
overs_remaining = st.slider("⏳ Overs Remaining", 0.1, 50.0, value=20.0, step=0.1)
required_run_rate = st.number_input("📈 Required Run Rate", value=6.5)
current_run_rate = current_score / (50 - overs_remaining + 0.1)
match_pressure_index = required_run_rate / (current_run_rate + 0.1)

# Phase encoding
phase = st.selectbox("📍 Match Phase", ["Early", "Middle", "Death"])
early, middle, death = int(phase == "Early"), int(phase == "Middle"), int(phase == "Death")

# Feature vector
features = np.array([[[
    current_score, wickets_in_hand, overs_remaining,
    required_run_rate, match_pressure_index,
    early, middle, death
]]])

# Predict
if st.button("🔮 Predict Outcome"):
    prediction = model.predict(features)[0]
    try:
        win_prob = model.predict_proba(features)[0][1]
    except IndexError:
        win_prob = 1.0 if prediction == 1 else 0.0

    if prediction == 1:
        st.success("✅ Prediction: The chasing team is likely to **WIN**.")
    else:
        st.error("❌ Prediction: The chasing team is likely to **LOSE**.")

    st.metric("📈 Win Probability", f"{win_prob * 100:.2f}%")
