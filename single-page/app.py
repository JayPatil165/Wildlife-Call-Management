import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Wildlife Incident Dashboard", layout="wide")

# --------------------------
# GOOGLE SHEETS AUTH + LOAD
# --------------------------

@st.cache_data(ttl=60)

def load_data():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
    client = gspread.authorize(creds)

    sheet = client.open_by_key("18pGiKDj0WIrJBDZ5cAa3WRUvZQ1PvL2swqMe2lH8pbc")  # <-- Fix this ID
    worksheet = sheet.worksheet("Form_responses_1")
    data = worksheet.get_all_records()
    df = pd.DataFrame(data)
    df['Timestamp'] = pd.to_datetime(df['Timestamp'], errors='coerce')
    return df

df = load_data()

from streamlit_autorefresh import st_autorefresh
st_autorefresh(10*1000, key="datarefresh")

# --------------------------
# SIDEBAR FILTERS
# --------------------------
st.sidebar.title("🔎 Filter Data")

wildlife_types = st.sidebar.multiselect("🦝 Type of Wildlife", df['Type of Wildlife'].unique(), default=df['Type of Wildlife'].unique())
talukas = st.sidebar.multiselect("📍 Taluka", df['Location (Taluka)'].unique(), default=df['Location (Taluka)'].unique())

min_date = df['Timestamp'].min().date()
max_date = df['Timestamp'].max().date()
date_range = st.sidebar.date_input("📆 Date Range", [min_date, max_date])

# Apply filters
df_filtered = df[
    (df['Type of Wildlife'].isin(wildlife_types)) &
    (df['Location (Taluka)'].isin(talukas)) &
    (df['Timestamp'].dt.date >= date_range[0]) &
    (df['Timestamp'].dt.date <= date_range[1])
]

# --------------------------
# MAIN DASHBOARD UI
# --------------------------
st.markdown("<a name='top'></a>", unsafe_allow_html=True)
st.markdown("""
<h1 style='text-align: center;'>🦁 Wildlife Incident Dashboard</h1>
""", unsafe_allow_html=True)

# --------------------------
# KPIs
# --------------------------
st.markdown("""
<style>
.kpi-container {{
    display: flex;
    justify-content: space-between;
    gap: 20px;
    margin-bottom: 20px;
}}
.kpi-box {{
    flex: 1;
    background-color: #e0e0e0;
    padding: 20px;
    border-radius: 10px;
    text-align: center;
}}
.kpi-title {{
    font-size: 20px;
    color: #000000;
    margin-bottom: 8px;
    font-weight: 600;
}}
.kpi-value {{
    font-size: 30px;
    font-weight: bold;
    color: #333333;
}}
</style>

<div class="kpi-container">
    <div class="kpi-box">
        <div class="kpi-title">📊 Total Incidents</div>
        <div class="kpi-value">{0}</div>
    </div>
    <div class="kpi-box">
        <div class="kpi-title">🐾 Wildlife Types</div>
        <div class="kpi-value">{1}</div>
    </div>
    <div class="kpi-box">
        <div class="kpi-title">🏘️ Affected Villages</div>
        <div class="kpi-value">{2}</div>
    </div>
    <div class="kpi-box">
        <div class="kpi-title">📞 Total Calls</div>
        <div class="kpi-value">{3}</div>
    </div>
</div>
""".format(
    len(df_filtered),
    df_filtered['Type of Wildlife'].nunique(),
    df_filtered['Village Name'].nunique(),
    df_filtered["Caller's Name"].count()
), unsafe_allow_html=True)

st.markdown("---")

# Navigation Buttons
st.markdown("""
<style>
.nav-container button {
    padding: 6px 12px;
    font-size: 16px;
    margin: 4px;
    background-color: #4CAF50;
    color: white;
    border: none;
    border-radius: 6px;
    cursor: pointer;
    transition: background-color 0.3s;
}
.nav-container button:hover {
    color: #4CAF50;
    transform: scale(1.05);
    background-color: white;
}
</style>
            
<h4 style='margin-bottom: 10px;'>🔗 Quick Links</h4>

<div class='nav-container' style='display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 20px;'>
    <a href='#wildlife'><button>Wildlife Incidents</button></a>
    <a href='#taluka'><button>Taluka Distribution</button></a>
    <a href='#types'><button>Incident Types per Wildlife</button></a>
    <a href='#incident-freq'><button>Incident Frequency</button></a>
    <a href='#top-talukas'><button>Top Talukas</button></a>
    <a href='#monthly'><button>Monthly Trend</button></a>
    <a href='#repeat'><button>Repeat Taluka</button></a>
    <a href='#timeline'><button>Wildlife Timeline</button></a>
    <a href='#monthly-taluka'><button>Monthly Trend by Taluka</button></a>
    <a href='#villages'><button>Top Villages</button></a>
    <a href='#callers'><button>Frequent Callers</button></a>
    <a href='#hourly'><button>Hourly Distribution</button></a>
    <a href='#heatmap'><button>Heatmap</button></a>
    <a href='#table'><button>Raw Data Table</button></a>
</div>
""", unsafe_allow_html=True)

# Back-to-top button
st.markdown("""
<style>
.back-to-top-btn {
    padding: 4px 8px;
    background-color: black;
    color: white;
    font-size: 12px;
    border: 1px solid white;
    border-radius: 6px;
    cursor: pointer;
    transition: all 0.3s ease;
    font-weight: 500;
}

.back-to-top-btn:hover {
    background-color: white;
    color: black;
    border: none;
    transform: scale(1.01);
}
</style>""", unsafe_allow_html=True  )


# Incidents by Wildlife
st.markdown("<a name='wildlife'></a>", unsafe_allow_html=True)
st.markdown("---")
st.markdown("""
<div style='display: flex;  align-items: center;'>
    <h3 style='margin: 0;'>📈 Incidents by Wildlife Type</h3>
    <a href='#top'>
        <button class='back-to-top-btn'>⬆️ Back to Top</button>
    </a>
</div>
""", unsafe_allow_html=True)
wildlife_counts = df_filtered['Type of Wildlife'].value_counts().reset_index()
wildlife_counts.columns = ['Wildlife', 'Count']
wildlife_counts = wildlife_counts.sort_values(by='Count', ascending=False)
fig1 = px.bar(wildlife_counts, x='Wildlife', y='Count', color='Wildlife', title="Incidents by Wildlife", template="plotly")
st.plotly_chart(fig1, use_container_width=True)

# Taluka-wise Pie
st.markdown("<a name='taluka'></a>", unsafe_allow_html=True)
st.markdown("---")
st.markdown("""
<div style='display: flex;  align-items: center;'>
    <h3 style='margin: 0;'>🗺️ Taluka Distribution</h3>
    <a href='#top'>
        <button class='back-to-top-btn'>⬆️ Back to Top</button>
    </a>
</div>
""", unsafe_allow_html=True)
taluka_counts = df_filtered['Location (Taluka)'].value_counts().reset_index()
taluka_counts.columns = ['Taluka', 'Count']
taluka_counts = taluka_counts.sort_values(by='Count', ascending=False)
fig2 = px.pie(taluka_counts, names='Taluka', values='Count', title="Incidents by Taluka", hole=0.4)
st.plotly_chart(fig2, use_container_width=True)

# Incident Types vs Wildlife
st.markdown("<a name='types'></a>", unsafe_allow_html=True)
st.markdown("---")
st.markdown("""
<div style='display: flex;  align-items: center;'>
    <h3 style='margin: 0;'>🧩 Types of Incidents per Wildlife</h3>
    <a href='#top'>
        <button class='back-to-top-btn'>⬆️ Back to Top</button>
    </a>
</div>
""", unsafe_allow_html=True)
combo = df_filtered.groupby(['Type of Wildlife', 'Type of Incident']).size().reset_index(name='Count')
fig5 = px.bar(combo, x='Type of Wildlife', y='Count', color='Type of Incident', barmode='group', title="Types of Incidents per Wildlife")
st.plotly_chart(fig5, use_container_width=True)

# Incident type frequency
st.markdown("<a name='incident-freq'></a>", unsafe_allow_html=True)
st.markdown("---")
st.markdown("""
<div style='display: flex;  align-items: center;'>
    <h3 style='margin: 0;'>📌 Incident Type Frequency</h3>
    <a href='#top'>
        <button class='back-to-top-btn'>⬆️ Back to Top</button>
    </a>
</div>
""", unsafe_allow_html=True)
incident_freq = df_filtered['Type of Incident'].value_counts().reset_index()
incident_freq.columns = ['Type of Incident', 'Count']
incident_freq = incident_freq.sort_values(by='Count', ascending=False)
fig10 = px.bar(incident_freq, x='Type of Incident', y='Count', title="Frequency of Each Incident Type", color='Count')
st.plotly_chart(fig10, use_container_width=True)

# Top Talukas by Incident
st.markdown("<a name='top-talukas'></a>", unsafe_allow_html=True)
st.markdown("---")
st.markdown("""
<div style='display: flex;  align-items: center;'>
    <h3 style='margin: 0;'>📍 Top Talukas by Incident</h3>
    <a href='#top'>
        <button class='back-to-top-btn'>⬆️ Back to Top</button>
    </a>
</div>
""", unsafe_allow_html=True)
top_talukas = df_filtered['Location (Taluka)'].value_counts().head(10).reset_index()
top_talukas.columns = ['Taluka', 'Incidents']
top_talukas = top_talukas.sort_values(by='Incidents', ascending=True)

fig_top_talukas = px.bar(
    top_talukas,
    x='Incidents',
    y='Taluka',
    orientation='h',
    color='Incidents',
    title="Top Talukas by Incidents",
    template="plotly"
)

st.plotly_chart(fig_top_talukas, use_container_width=True)

# Monthly Trend
st.markdown("<a name='monthly'></a>", unsafe_allow_html=True)
st.markdown("---")
st.markdown("""
<div style='display: flex;  align-items: center;'>
    <h3 style='margin: 0;'>📆 Monthly Incident Trend</h3>
    <a href='#top'>
        <button class='back-to-top-btn'>⬆️ Back to Top</button>
    </a>
</div>
""", unsafe_allow_html=True)
df_filtered['Month'] = df_filtered['Timestamp'].dt.to_period("M").astype(str)
monthly = df_filtered.groupby("Month").size().reset_index(name="Incidents")
fig3 = px.line(monthly, x='Month', y='Incidents', markers=True, title="Monthly Incident Trend", template="plotly_dark")
st.plotly_chart(fig3, use_container_width=True)

# Taluka Repeat Pattern
st.markdown("<a name='repeat'></a>", unsafe_allow_html=True)
st.markdown("---")
st.markdown("""
<div style='display: flex;  align-items: center;'>
    <h3 style='margin: 0;'>🔁 Repeat Incidents Over Time by Taluka</h3>
    <a href='#top'>
        <button class='back-to-top-btn'>⬆️ Back to Top</button>
    </a>
</div>
""", unsafe_allow_html=True)
repeat_taluka = df_filtered.groupby([df_filtered['Timestamp'].dt.date, 'Location (Taluka)']).size().reset_index(name='Count')
top_repeat_talukas = repeat_taluka['Location (Taluka)'].value_counts().head(5).index
repeat_taluka = repeat_taluka[repeat_taluka['Location (Taluka)'].isin(top_repeat_talukas)]
fig9 = px.line(repeat_taluka, x='Timestamp', y='Count', color='Location (Taluka)', title="Repeat Incidents in Talukas Over Time")
st.plotly_chart(fig9, use_container_width=True) 

# Incident timeline per wildlife
st.markdown("<a name='timeline'></a>", unsafe_allow_html=True)
st.markdown("---")
st.markdown("""
<div style='display: flex;  align-items: center;'>
    <h3 style='margin: 0;'>📅 Incident Timeline per Wildlife</h3>
    <a href='#top'>
        <button class='back-to-top-btn'>⬆️ Back to Top</button>
    </a>
</div>
""", unsafe_allow_html=True)
timeline = df_filtered.groupby([df_filtered['Timestamp'].dt.date, 'Type of Wildlife']).size().reset_index(name='Incidents')
fig11 = px.line(timeline, x='Timestamp', y='Incidents', color='Type of Wildlife', title="Daily Wildlife Incidents Timeline")
st.plotly_chart(fig11, use_container_width=True)

# Monthly Incident Trend per Taluka
st.markdown("<a name='monthly-taluka'></a>", unsafe_allow_html=True)
st.markdown("---")
st.markdown("""
<div style='display: flex;  align-items: center;'>
    <h3 style='margin: 0;'>📈 Monthly Incident Trend per Taluka</h3>
    <a href='#top'>
        <button class='back-to-top-btn'>⬆️ Back to Top</button>
    </a>
</div>
""", unsafe_allow_html=True)
df_filtered['Month'] = df_filtered['Timestamp'].dt.to_period("M").astype(str)
monthly_taluka = df_filtered.groupby(['Month', 'Location (Taluka)']).size().reset_index(name='Incidents')

fig12 = px.line(
    monthly_taluka,
    x='Month',
    y='Incidents',
    color='Location (Taluka)',
    markers=True,
    title="Monthly Incident Trends by Taluka"
)

st.plotly_chart(fig12, use_container_width=True)

# Top Villages
st.markdown("<a name='villages'></a>", unsafe_allow_html=True)
st.markdown("---")
st.markdown("""
<div style='display: flex;  align-items: center;'>
    <h3 style='margin: 0;'>🏡 Top 10 Villages by Incident</h3>
    <a href='#top'>
        <button class='back-to-top-btn'>⬆️ Back to Top</button>
    </a>
</div>
""", unsafe_allow_html=True)
top_villages = df_filtered['Village Name'].value_counts().head(10).reset_index()
top_villages.columns = ['Village', 'Incidents']
top_villages = top_villages.sort_values(by='Incidents')
fig4 = px.bar(top_villages, x='Incidents', y='Village', orientation='h', color='Incidents', title="Top 10 Villages", template="seaborn")
st.plotly_chart(fig4, use_container_width=True)

# Callers
st.markdown("<a name='callers'></a>", unsafe_allow_html=True)
st.markdown("---")
st.markdown("""
<div style='display: flex;  align-items: center;'>
    <h3 style='margin: 0;'>📞 Frequent Callers</h3>
    <a href='#top'>
        <button class='back-to-top-btn'>⬆️ Back to Top</button>
    </a>
</div>
""", unsafe_allow_html=True)
top_callers = df_filtered['Caller\'s Name'].value_counts().nlargest(10).reset_index()
top_callers.columns = ['Caller', 'Reports']
top_callers = top_callers.sort_values(by='Reports')
fig8 = px.bar(top_callers, x='Reports', y='Caller', orientation='h', title="Top Callers", color='Reports')
st.plotly_chart(fig8, use_container_width=True)

# Hour of Day
st.markdown("<a name='hourly'></a>", unsafe_allow_html=True)
st.markdown("---")
st.markdown("""
<div style='display: flex;  align-items: center;'>
    <h3 style='margin: 0;'>⏰ Hourly Distribution of Incidents</h3>
    <a href='#top'>
        <button class='back-to-top-btn'>⬆️ Back to Top</button>
    </a>
</div>
""", unsafe_allow_html=True)
df_filtered['Hour'] = df_filtered['Timestamp'].dt.hour
fig6 = px.histogram(df_filtered, x='Hour', nbins=24, title="Incidents by Hour of Day", color_discrete_sequence=['#ffa15a'])
st.plotly_chart(fig6, use_container_width=True)

# Heatmap: Wildlife vs Taluka
st.markdown("<a name='heatmap'></a>", unsafe_allow_html=True)
st.markdown("---")
st.markdown("""
<div style='display: flex;  align-items: center;'>
    <h3 style='margin: 0;'>🌡️ Wildlife vs Taluka Heatmap</h3>
    <a href='#top'>
        <button class='back-to-top-btn'>⬆️ Back to Top</button>
    </a>
</div>
""", unsafe_allow_html=True)
pivot = df_filtered.groupby(['Location (Taluka)', 'Type of Wildlife']).size().unstack(fill_value=0)

if not pivot.empty:
    fig7, ax = plt.subplots(figsize=(12, 6))
    sns.heatmap(pivot, annot=True, fmt='g', cmap='YlGnBu')
    st.pyplot(fig7)
else:
    st.info("No data available for selected filters to display heatmap.")

# Final table
st.markdown("<a name='table'></a>", unsafe_allow_html=True)
st.markdown("---")
st.markdown("""
<div style='display: flex;  align-items: center;'>
    <h3 style='margin: 0;'>📋 Raw Data Table</h3>
    <a href='#top'>
        <button class='back-to-top-btn'>⬆️ Back to Top</button>
    </a>
</div>
""", unsafe_allow_html=True)
with st.expander("📋 Show Filtered Raw Data"):
    st.dataframe(df_filtered)

st.markdown("---")
st.markdown("""
<p style='text-align: center;'>For Forest Deparment</p>
""", unsafe_allow_html=True)
