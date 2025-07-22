import streamlit as st
import pandas as pd
import joblib
import matplotlib.pyplot as plt

# Load model
model = joblib.load("win_probability_xgb_model.pkl")

st.set_page_config(page_title="Win Probability Timeline", page_icon="📈")
st.title("📈 Win Probability Over Time")
st.markdown("Predict the chance of winning at each over based on current score, wickets, RRR.")

# Sample scenario input (manual for now)
target_score = st.number_input("🎯 Target Score", min_value=100, max_value=400, value=280)
wickets_by_over = st.text_area("✍️ Wickets at each over (comma-separated)", "0,0,1,1,2,2,2,3,3,3,4,4,5,5,5,6,7,7,8,9")
runs_by_over = st.text_area("✍️ Runs at each over (comma-separated)", "4,8,17,25,33,41,48,56,63,72,80,88,96,105,115,124,132,138,142,145")

if st.button("🔍 Predict Win Probability Trajectory"):
    try:
        wickets_list = list(map(int, wickets_by_over.strip().split(',')))
        runs_list = list(map(int, runs_by_over.strip().split(',')))
        overs = list(range(1, len(runs_list)+1))
        overs_remaining = [50 - o for o in overs]
        wickets_in_hand = [10 - w for w in wickets_list]
        required_run_rate = [(target_score - r) / (o if o != 0 else 1) for r, o in zip(runs_list, overs_remaining)]

        df = pd.DataFrame({
            'current_score': runs_list,
            'wickets_in_hand': wickets_in_hand,
            'overs_remaining': overs_remaining,
            'required_run_rate': required_run_rate
        })

        probs = model.predict_proba(df)[:, 1]  # Win probability
        df['win_probability'] = probs

        # Plot
        fig, ax = plt.subplots()
        ax.plot(overs, df['win_probability'] * 100, marker='o', color='blue')
        ax.set_xlabel("Overs")
        ax.set_ylabel("Win Probability (%)")
        ax.set_title("Win Probability Timeline")
        ax.grid(True)
        st.pyplot(fig)

        st.dataframe(df[['current_score', 'wickets_in_hand', 'overs_remaining', 'required_run_rate', 'win_probability']])
    except Exception as e:
        st.error(f"Error in input or prediction: {e}")
