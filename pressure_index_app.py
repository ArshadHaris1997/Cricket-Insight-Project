import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Pressure Index Visualizer", page_icon="🔥")
st.title("🔥 Pressure Index Timeline")
st.markdown("Visualizes pressure during the second innings: `Pressure Index = RRR / CRR`")

@st.cache_data
def load_data():
    return pd.read_csv("pressure_index_over_time.csv")

df = load_data()

# Select match to display
match_ids = sorted(df['match_id'].unique())
match_id = st.selectbox("Select Match ID", match_ids)

match_df = df[df['match_id'] == match_id]

# Plot Pressure Index
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(match_df['over'], match_df['pressure_index'], marker='o', color='crimson', label='Pressure Index')
ax.axhline(1, color='gray', linestyle='--', label='Balanced Line (1.0)')
ax.set_title(f"📈 Pressure Index - Match {match_id}")
ax.set_xlabel("Over")
ax.set_ylabel("Pressure Index")
ax.legend()
st.pyplot(fig)

# Optional: Show critical overs
high_pressure = match_df[match_df['pressure_index'] > 1.5]
if not high_pressure.empty:
    st.subheader("🛑 High Pressure Moments")
    st.dataframe(high_pressure[['over', 'pressure_index', 'current_run_rate', 'required_run_rate', 'wickets']])
