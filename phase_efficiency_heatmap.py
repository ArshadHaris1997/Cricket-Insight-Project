import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Configure app
st.set_page_config(page_title="Phase Efficiency Heatmap", page_icon="🔥")

st.title("🔥 Phase-Wise Batting Efficiency Heatmap")
st.markdown("""
Visualize how different batsmen perform across the three phases of a T20 innings:
- **Powerplay** (0–5 overs)
- **Middle** (6–15 overs)
- **Death** (16–20 overs)
""")

# Load CSV
@st.cache_data
def load_data():
    return pd.read_csv("phase_efficiency_batsman_proxy.csv")

df = load_data()

# Select top players to display
top_n = st.slider("Select number of players to display", 5, 50, 15)
df_top = df.sort_values(by='Powerplay', ascending=False).head(top_n)

# Set index and plot heatmap
df_heatmap = df_top.set_index('batsmanName')[['Powerplay', 'Middle', 'Death']]

fig, ax = plt.subplots(figsize=(10, 0.6 * top_n))
sns.heatmap(df_heatmap, annot=True, fmt=".2f", cmap="YlGnBu", linewidths=0.5, ax=ax)
ax.set_title("Run Rate per Phase", fontsize=14)
st.pyplot(fig)

st.caption("🎯 Data from `phase_efficiency_batsman_proxy.csv` — run rate = total runs / overs faced in each phase.")
