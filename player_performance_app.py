import streamlit as st
st.set_page_config(page_title="Player Performance Dashboard", page_icon="🏏")

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load player performance data
@st.cache_data
def load_data():
    return pd.read_csv("batsman_performance_stats.csv")

df = load_data()

st.title("🏏 Player Performance Analysis")

# Sidebar selection
selected_player = st.selectbox("🔎 Select a Player", df['batsmanName'].unique())

# Get player data
player_row = df[df['batsmanName'] == selected_player]

# Radar chart values (Z-scores)
labels = ['Batting Avg', 'Strike Rate', 'Boundary Rate']
values = player_row[['batting_avg_z', 'strike_rate_z', 'boundary_rate_z']].values.flatten().tolist()
values += values[:1]  # close the radar loop

# Radar plot
angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
angles += angles[:1]

fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
ax.fill(angles, values, color='skyblue', alpha=0.5)
ax.plot(angles, values, color='blue', linewidth=2)
ax.set_xticks(angles[:-1])
ax.set_xticklabels(labels)
ax.set_title(f"Radar Chart for {selected_player}", y=1.1)

st.pyplot(fig)

# Display raw stats
st.subheader("📋 Player Summary")
st.write(player_row[['matches', 'innings', 'total_runs', 'balls_faced', 'batting_avg', 'strike_rate', 'boundary_rate']])
