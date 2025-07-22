<<<<<<< HEAD
import streamlit as st
import numpy as np
import joblib

# Load the trained model
model = joblib.load("xgb_score_predictor.pkl")

st.set_page_config(page_title="Innings Score Predictor", page_icon="🏏")
st.title("🏏 Final Innings Score Predictor")

st.markdown("""
This app predicts the **final innings score** based on current match statistics after the 25th over.
Use the sliders below to adjust the match situation and get predictions in real-time.
""")

# Input features
cumulative_runs = st.slider("🏏 Cumulative Runs", min_value=0, max_value=350, value=180)
cumulative_wickets = st.slider("💥 Wickets Fallen", min_value=0, max_value=10, value=5)
over = st.slider("⏱️ Current Over", min_value=25.0, max_value=50.0, step=0.1, value=35.0)
run_rate_last_5 = st.slider("📈 Run Rate (Last 5 Overs)", min_value=2.0, max_value=15.0, step=0.1, value=7.5)

# Create feature array
input_data = np.array([[cumulative_runs, cumulative_wickets, over, run_rate_last_5]])

# Prediction
if st.button("🔮 Predict Final Score"):
    prediction = model.predict(input_data)[0]
    st.success(f"🏁 Predicted Final Score: **{prediction:.0f} runs**")
    st.metric("📊 Current Run Rate", f"{cumulative_runs / over:.2f}")
    st.metric("⚡ Projected Run Rate", f"{run_rate_last_5:.2f}")
=======
import streamlit as st
import numpy as np
import joblib

# Load the trained model
model = joblib.load("xgb_score_predictor.pkl")

st.set_page_config(page_title="Innings Score Predictor", page_icon="🏏")
st.title("🏏 Final Innings Score Predictor")

st.markdown("""
This app predicts the **final innings score** based on current match statistics after the 25th over.
Use the sliders below to adjust the match situation and get predictions in real-time.
""")

# Input features
cumulative_runs = st.slider("🏏 Cumulative Runs", min_value=0, max_value=350, value=180)
cumulative_wickets = st.slider("💥 Wickets Fallen", min_value=0, max_value=10, value=5)
over = st.slider("⏱️ Current Over", min_value=25.0, max_value=50.0, step=0.1, value=35.0)
run_rate_last_5 = st.slider("📈 Run Rate (Last 5 Overs)", min_value=2.0, max_value=15.0, step=0.1, value=7.5)

# Create feature array
input_data = np.array([[cumulative_runs, cumulative_wickets, over, run_rate_last_5]])

# Prediction
if st.button("🔮 Predict Final Score"):
    prediction = model.predict(input_data)[0]
    st.success(f"🏁 Predicted Final Score: **{prediction:.0f} runs**")
    st.metric("📊 Current Run Rate", f"{cumulative_runs / over:.2f}")
    st.metric("⚡ Projected Run Rate", f"{run_rate_last_5:.2f}")
>>>>>>> 6c7c001 (Add Streamlit app, model, and requirements)
