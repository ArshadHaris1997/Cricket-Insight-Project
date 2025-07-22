import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Momentum Shift Detector", page_icon="💥")
st.title("💥 Momentum Shift Detector")
st.markdown("Identify **game-changing overs** via sudden shifts in run rate or wicket clusters.")

@st.cache_data
def load_data():
    return pd.read_csv("momentum_shift_events.csv")

df = load_data()
match_ids = sorted(df['match_id'].unique())
match_id = st.selectbox("Select Match ID", match_ids)

match_df = df[df['match_id'] == match_id]

# Plot run rate and mark shifts
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(match_df['over'], match_df['run_rate'], marker='o', label="Run Rate", color="blue")

# Highlight shifts
for i, row in match_df.iterrows():
    if row['momentum_shift'] == 1:
        ax.axvline(x=row['over'], color='red', linestyle='--', alpha=0.6)
        ax.text(row['over']+0.1, row['run_rate']+0.3, "⚡", fontsize=14, color='crimson')

ax.set_xlabel("Over")
ax.set_ylabel("Run Rate")
ax.set_title(f"Momentum Timeline – Match {match_id}")
ax.grid(True)
ax.legend()
st.pyplot(fig)

# Table of shift overs
shifts = match_df[match_df['momentum_shift'] == 1]
st.subheader("🔻 Momentum Shift Overs")
st.dataframe(shifts[['over', 'run_rate', 'rr_delta', 'wickets']])
