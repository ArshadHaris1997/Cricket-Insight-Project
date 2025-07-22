import streamlit as st
import pandas as pd

st.set_page_config(page_title="Bowler vs Batsman Matchups", page_icon="🎯")
st.title("🎯 Bowler vs Batsman Matchup Analyzer")

# Load match-up data
@st.cache_data
def load_data():
    return pd.read_csv("bowler_vs_batsman_matchups.csv")

df = load_data()

# User input: Select bowler or batsman focus
view_type = st.radio("🔍 View by:", ['Bowler-centric', 'Batsman-centric'])

if view_type == "Bowler-centric":
    bowler = st.selectbox("Select Bowler", sorted(df['bowlerName'].unique()))
    filtered = df[df['bowlerName'] == bowler].sort_values(by='strike_rate')
    st.subheader(f"Matchups for: {bowler}")
else:
    batsman = st.selectbox("Select Batsman", sorted(df['batsmanName'].unique()))
    filtered = df[df['batsmanName'] == batsman].sort_values(by='strike_rate')
    st.subheader(f"Matchups for: {batsman}")

# Display table
st.dataframe(filtered[['bowlerName', 'batsmanName', 'balls_faced', 'total_runs', 'strike_rate', 'dismissals']])

# Highlight key stats
st.markdown("🧠 **Insight:** Lower strike rate + high dismissals = strong bowler matchup.")
