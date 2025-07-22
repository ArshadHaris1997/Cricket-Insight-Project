import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="DRS Bias Analyzer", page_icon="⚖️")
st.title("⚖️ Umpire & DRS Review Analyzer")
st.markdown("Analyze LBW/DRS patterns, success rates, and player-wise outcomes.")

# Load extracted review data
@st.cache_data
def load_data():
    return pd.read_csv("drs_review_events.csv")

df = load_data()

# Filter options
players = sorted(set(df['batsmanName'].dropna()) | set(df['bowlerName'].dropna()))
review_outcomes = df['review_outcome'].unique()

view = st.radio("🔍 View by", ['Batsman', 'Bowler', 'Review Outcome'])

if view == 'Batsman':
    batsman = st.selectbox("Select Batsman", sorted(df['batsmanName'].dropna().unique()))
    filtered = df[df['batsmanName'] == batsman]
    st.write(f"Total reviews involving `{batsman}`: {len(filtered)}")
    st.bar_chart(filtered['review_outcome'].value_counts())

elif view == 'Bowler':
    bowler = st.selectbox("Select Bowler", sorted(df['bowlerName'].dropna().unique()))
    filtered = df[df['bowlerName'] == bowler]
    st.write(f"Total reviews involving `{bowler}`: {len(filtered)}")
    st.bar_chart(filtered['review_outcome'].value_counts())

else:
    st.subheader("📊 Overall Review Outcome Distribution")
    st.bar_chart(df['review_outcome'].value_counts())

# Optional: Show commentary log
if st.checkbox("📝 Show raw commentary lines"):
    st.dataframe(df[['matchID', 'over', 'batsmanName', 'bowlerName', 'commentary', 'review_outcome']])
