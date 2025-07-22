# score_predictor_app.py

import streamlit as st
import joblib
import numpy as np

# ✅ Must be the first Streamlit command
st.set_page_config(page_title="🏏 First Innings Score Predictor", page_icon="🎯")

# Load the trained model
model = joblib.load("xgb_score_predictor.pkl")

st.title("🏏 First Innings Score Prediction App")
st.markdown("Estimate the final score in an ODI match using current match state.")

# User Inputs
st.subheader("📥 Enter Current Match Stats (After 25 Overs Recommended)")
current_score = st.number_input("Current Score (Runs):", min_value=0, max_value=400, value=140)
wickets_lost = st.slider("Wickets Lost:", 0, 10, value=3)
overs_completed = st.slider("Overs Completed:", min_value=10.0, max_value=40.0, step=0.1, value=25.0)
run_rate_last5 = st.number_input("Average Run Rate (Last 5 Overs):", min_value=0.0, max_value=15.0, value=6.5)

# Prepare features for prediction
features = np.array([[current_score, wickets_lost, overs_completed, run_rate_last5]])

# Predict button
if st.button("🔮 Predict Final Score"):
    prediction = model.predict(features)[0]
    st.success(f"📊 Predicted Final Score: **{round(prediction)} runs**")

    st.markdown("---")
    st.caption("Model: XGBoost Regressor trained with ball-by-ball ODI match data.")
    st.caption("Tip: Prediction improves after 25 overs. Use real-time data for best accuracy.")

# Footer
st.markdown("— Developed as part of the *Cricket Insights Intelligence System* 🎓")
