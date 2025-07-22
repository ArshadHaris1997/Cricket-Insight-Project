import streamlit as st
import pandas as pd

st.set_page_config(page_title="LLM Commentary Summarizer", page_icon="🧠")

st.title("🧠 LLM-Based Commentary Summarizer")
st.markdown("Auto-generated over-wise match summaries using BART (transformers).")

@st.cache_data
def load_data():
    return pd.read_csv("llm_generated_summaries.csv")

df = load_data()

# Dropdowns
match_ids = sorted(df['matchID'].unique())
match = st.selectbox("Select Match", match_ids)

bowler_names = sorted(df[df['matchID'] == match]['bowlerName'].unique())
selected_bowler = st.selectbox("Select Bowler (Optional)", ["All"] + bowler_names)

# Filter based on selection
filtered_df = df[df['matchID'] == match]
if selected_bowler != "All":
    filtered_df = filtered_df[filtered_df['bowlerName'] == selected_bowler]

st.subheader("🎙️ Summarized Commentary")
st.dataframe(filtered_df[['over', 'bowlerName', 'summary']], use_container_width=True)

st.markdown("---")
st.caption("Built with 🤗 Transformers + Streamlit + World Cup 2024 commentary.")
