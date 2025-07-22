import streamlit as st
import joblib
import numpy as np

# Load trained model
model = joblib.load("match_outcome_model.pkl")

st.set_page_config(page_title="Match Outcome Predictor", page_icon="🏏")
st.title("🏏 Match Outcome Predictor (Second Innings)")
st.markdown("""
This app predicts whether a **chasing team** will win the match based on real-time inputs like current score, overs, wickets, and required run rate.
""")

# Input fields
target_score = st.number_input("🎯 Target Score", min_value=50, max_value=500, value=270)
current_score = st.slider("🏏 Current Score", 0, 500, 150)
wickets_in_hand = st.slider("🚨 Wickets Remaining", 0, 10, 7)
overs_remaining = st.slider("⏳ Overs Remaining", 0.1, 50.0, 20.0, step=0.1)

# Derived features
required_run_rate = (target_score - current_score) / overs_remaining if overs_remaining > 0 else 0.0
current_run_rate = current_score / (50 - overs_remaining + 0.1)
match_pressure_index = required_run_rate / (current_run_rate + 0.1)

# Match phase encoding
match_phase = st.selectbox("Match Phase", ["Early", "Middle", "Death"])
early, middle, death = 0, 0, 0
if match_phase == "Early":
    early = 1
elif match_phase == "Middle":
    middle = 1
else:
    death = 1

# Toss and venue flags
toss_winner = st.radio("Toss won by chasing team?", ["Yes", "No"]) == "Yes"
venue_advantage = st.radio("Venue favours chasing side?", ["Yes", "No"]) == "Yes"

# Final input vector
input_features = np.array([[
    target_score, current_score, wickets_in_hand, overs_remaining,
    required_run_rate, int(toss_winner), int(venue_advantage),
    match_pressure_index, early, middle, death
]])

# Predict
if st.button("🔮 Predict Outcome"):
    prediction = model.predict(input_features)[0]
    proba = model.predict_proba(input_features)[0][1]  # win probability

    if prediction == 1:
        st.success(f"✅ Predicted: Chasing team is likely to **WIN**")
    else:
        st.error(f"❌ Predicted: Chasing team is likely to **LOSE**")
