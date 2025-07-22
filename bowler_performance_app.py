import streamlit as st
st.set_page_config(page_title="Bowler Performance Dashboard", page_icon="🎯")

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load bowler data
@st.cache_data
def load_data():
    return pd.read_csv("bowler_performance_stats.csv")

df = load_data()

st.title("🎯 Bowler Performance Analysis")

# User input
selected_bowler = st.selectbox("Select a Bowler", df['bowlerName'].unique())

# Extract selected stats
row = df[df['bowlerName'] == selected_bowler]

# Radar chart: Z-score normalized metrics
labels = ['Economy', 'Strike Rate', 'Dot %', 'Discipline', 'Wkts/Match']
values = row[['economy_z', 'strike_rate_z', 'dot_percent_z', 'discipline_ratio_z', 'wickets_per_match_z']].values.flatten().tolist()
values += values[:1]
angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
angles += angles[:1]

# Plot
fig, ax = plt.subplots(figsize=(6,6), subplot_kw=dict(polar=True))
ax.fill(angles, values, color='green', alpha=0.25)
ax.plot(angles, values, color='green', linewidth=2)
ax.set_xticks(angles[:-1])
ax.set_xticklabels(labels)
ax.set_title(f"{selected_bowler} - Performance Radar", y=1.1)
st.pyplot(fig)

# Show raw values
st.subheader("📊 Bowler Stats Summary")
st.write(row[['matches', 'balls_bowled', 'wickets', 'economy', 'strike_rate', 'dot_percent', 'discipline_ratio', 'wickets_per_match']])
