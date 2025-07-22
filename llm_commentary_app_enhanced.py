import streamlit as st
import pandas as pd

st.set_page_config("🧠 LLM Cricket Summarizer+", page_icon="🏏")

st.title("🧠 Enhanced LLM Commentary Summarizer")
st.markdown("With **sentiment tags**, **impact ratings**, and **batsman details**.")

@st.cache_data
def load_data():
    return pd.read_csv("llm_commentary_enhanced.csv")

df = load_data()

# Sidebar filters
match_ids = sorted(df['matchID'].unique())
selected_match = st.selectbox("Match ID", match_ids)

bowlers = sorted(df[df['matchID'] == selected_match]['bowlerName'].unique())
selected_bowler = st.selectbox("Bowler", ["All"] + bowlers)

# Filter
filtered = df[df['matchID'] == selected_match]
if selected_bowler != "All":
    filtered = filtered[filtered['bowlerName'] == selected_bowler]

st.subheader("🎙️ Summary Table")
st.dataframe(
    filtered[['over', 'bowlerName', 'batsmanName', 'runs', 'isWicket', 'summary', 'sentiment', 'impact']],
    use_container_width=True
)

# Optional: Filter by impact/sentiment
with st.expander("📊 Filter by Sentiment or Impact"):
    sentiment_filter = st.multiselect("Sentiment", ["Positive", "Neutral", "Negative"], default=["Positive", "Neutral", "Negative"])
    impact_filter = st.multiselect("Impact", ["High", "Medium", "Low"], default=["High", "Medium", "Low"])
    filtered_view = filtered[
        filtered['sentiment'].isin(sentiment_filter) &
        filtered['impact'].isin(impact_filter)
    ]
    st.dataframe(filtered_view, use_container_width=True)
