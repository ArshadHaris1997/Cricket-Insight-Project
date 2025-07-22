import streamlit as st
import pandas as pd

st.set_page_config(page_title="Death Over Bowler Recommender", page_icon="🏏")
st.title("🏏 Best Death Over Bowler Recommender")

st.markdown("""
Select a pressure level and get recommended bowlers based on wickets, dot ball %, economy, and discipline (death overs only).
""")

# 📁 Load pre-computed stats (create this CSV from your notebook)
try:
    bowler_stats = pd.read_csv("death_over_bowler_stats.csv")
except FileNotFoundError:
    st.error("Please make sure 'death_over_bowler_stats.csv' exists in the same folder.")
    st.stop()

# 🔍 Scenario Selection
scenario = st.selectbox("Select Pressure Scenario", ["Low", "Medium", "High"])

# 🎯 Sort logic based on scenario
if scenario == "Low":
    result = bowler_stats.sort_values(by=["discipline_ratio", "dot_percent"], ascending=False)
elif scenario == "Medium":
    result = bowler_stats.sort_values(by=["wickets", "dot_percent"], ascending=False)
else:  # High pressure
    result = bowler_stats.sort_values(by=["wickets", "discipline_ratio"], ascending=False)

# 📊 Display top 5
st.subheader("Top Recommended Bowlers")
st.dataframe(result.head(5)[["bowlerName", "wickets", "dot_percent", "economy", "discipline_ratio"]])

st.caption("🔍 Based on overs 16–20 only (death overs)")
