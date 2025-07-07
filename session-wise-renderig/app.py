import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
from streamlit_autorefresh import st_autorefresh

st.set_page_config(page_title="Wildlife Incident Dashboard", layout="wide")

# --------------------------
# SESSION STATE INIT
# --------------------------
if 'active_chart' not in st.session_state:
    st.session_state.active_chart = None

# --------------------------
# GOOGLE SHEETS AUTH + LOAD
# --------------------------
@st.cache_data(ttl=60)
def load_data():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
    client = gspread.authorize(creds)
    sheet = client.open_by_key("18pGiKDj0WIrJBDZ5cAa3WRUvZQ1PvL2swqMe2lH8pbc")
    worksheet = sheet.worksheet("Form_responses_1")
    data = worksheet.get_all_records()
    df = pd.DataFrame(data)
    df['Timestamp'] = pd.to_datetime(df['Timestamp'], errors='coerce')
    return df

df = load_data()
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
# HEADER + KPIs
# --------------------------
st.markdown("""
<h1 style='text-align: center;'>🦁 Wildlife Incident Dashboard</h1>
""", unsafe_allow_html=True)

total_incidents = len(df_filtered)
wildlife_types_count = df_filtered['Type of Wildlife'].nunique()
villages_count = df_filtered['Village Name'].nunique()
total_calls = df_filtered["Caller's Name"].count()

st.markdown(f"""
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
        <div class="kpi-value">{total_incidents}</div>
    </div>
    <div class="kpi-box">
        <div class="kpi-title">🐾 Wildlife Types</div>
        <div class="kpi-value">{wildlife_types_count}</div>
    </div>
    <div class="kpi-box">
        <div class="kpi-title">🏘️ Affected Villages</div>
        <div class="kpi-value">{villages_count}</div>
    </div>
    <div class="kpi-box">
        <div class="kpi-title">📞 Total Calls</div>
        <div class="kpi-value">{total_calls}</div>
    </div>
</div>
""", unsafe_allow_html=True)

chart_buttons = {
    "Wildlife Incidents": "wildlife",
    "Taluka Distribution": "taluka",
    "Incident Types": "types",
    "Incident Frequency": "incident_freq",
    "Top Talukas": "top_talukas",
    "Monthly Trend": "monthly",
    "Repeat Taluka": "repeat",
    "Wildlife Timeline": "timeline",
    "Monthly by Taluka": "monthly_taluka",
    "Top Villages": "villages",
    "Frequent Callers": "callers",
    "Hourly Distribution": "hourly",
    "Heatmap": "heatmap",
    "Raw Data Table": "table"
}

st.markdown("""
<style>
.stButton > button {
    width: 100%;
    padding: 10px 6px;
    font-size: 14px;
    background-color: #4CAF50;
    color: white;
    border: none;
    border-radius: 6px;
    cursor: pointer;
    transition: all 0.2s ease-in-out;
    margin-bottom: 6px;
}
.stButton > button:hover {
    background-color: white;
    color: #4CAF50;
    border: 1px solid #4CAF50;
    transform: scale(1.03);
}
</style>
""", unsafe_allow_html=True)

# Grid layout: 7 buttons per row
cols = st.columns(7)
for i, (label, key) in enumerate(chart_buttons.items()):
    with cols[i % 7]:
        if st.button(label):
            st.session_state.active_chart = key

# --------------------------
# CHART RENDERING
# --------------------------
if st.session_state.active_chart == "wildlife":
    data = df_filtered['Type of Wildlife'].value_counts().reset_index()
    data.columns = ['Wildlife', 'Count']
    fig = px.bar(data, x='Wildlife', y='Count', color='Wildlife')
    st.plotly_chart(fig, use_container_width=True)

elif st.session_state.active_chart == "taluka":
    data = df_filtered['Location (Taluka)'].value_counts().reset_index()
    data.columns = ['Taluka', 'Count']
    fig = px.pie(data, names='Taluka', values='Count', hole=0.4)
    st.plotly_chart(fig, use_container_width=True)

elif st.session_state.active_chart == "types":
    combo = df_filtered.groupby(['Type of Wildlife', 'Type of Incident']).size().reset_index(name='Count')
    fig = px.bar(combo, x='Type of Wildlife', y='Count', color='Type of Incident', barmode='group')
    st.plotly_chart(fig, use_container_width=True)

elif st.session_state.active_chart == "incident_freq":
    freq = df_filtered['Type of Incident'].value_counts().reset_index()
    freq.columns = ['Type of Incident', 'Count']
    fig = px.bar(freq, x='Type of Incident', y='Count', color='Count')
    st.plotly_chart(fig, use_container_width=True)

elif st.session_state.active_chart == "top_talukas":
    top_talukas = df_filtered['Location (Taluka)'].value_counts().head(10).reset_index()
    top_talukas.columns = ['Taluka', 'Incidents']
    fig = px.bar(top_talukas.sort_values(by='Incidents'), x='Incidents', y='Taluka', orientation='h')
    st.plotly_chart(fig, use_container_width=True)

elif st.session_state.active_chart == "monthly":
    df_filtered['Month'] = df_filtered['Timestamp'].dt.to_period("M").astype(str)
    monthly = df_filtered.groupby("Month").size().reset_index(name="Incidents")
    fig = px.line(monthly, x='Month', y='Incidents', markers=True)
    st.plotly_chart(fig, use_container_width=True)

elif st.session_state.active_chart == "repeat":
    repeat = df_filtered.groupby([df_filtered['Timestamp'].dt.date, 'Location (Taluka)']).size().reset_index(name='Count')
    top = repeat['Location (Taluka)'].value_counts().head(5).index
    repeat = repeat[repeat['Location (Taluka)'].isin(top)]
    fig = px.line(repeat, x='Timestamp', y='Count', color='Location (Taluka)')
    st.plotly_chart(fig, use_container_width=True)

elif st.session_state.active_chart == "timeline":
    timeline = df_filtered.groupby([df_filtered['Timestamp'].dt.date, 'Type of Wildlife']).size().reset_index(name='Incidents')
    fig = px.line(timeline, x='Timestamp', y='Incidents', color='Type of Wildlife')
    st.plotly_chart(fig, use_container_width=True)

elif st.session_state.active_chart == "monthly_taluka":
    df_filtered['Month'] = df_filtered['Timestamp'].dt.to_period("M").astype(str)
    data = df_filtered.groupby(['Month', 'Location (Taluka)']).size().reset_index(name='Incidents')
    fig = px.line(data, x='Month', y='Incidents', color='Location (Taluka)', markers=True)
    st.plotly_chart(fig, use_container_width=True)

elif st.session_state.active_chart == "villages":
    top_villages = df_filtered['Village Name'].value_counts().head(10).reset_index()
    top_villages.columns = ['Village', 'Incidents']
    fig = px.bar(top_villages.sort_values(by='Incidents'), x='Incidents', y='Village', orientation='h')
    st.plotly_chart(fig, use_container_width=True)

elif st.session_state.active_chart == "callers":
    top_callers = df_filtered['Caller\'s Name'].value_counts().head(10).reset_index()
    top_callers.columns = ['Caller', 'Reports']
    fig = px.bar(top_callers.sort_values(by='Reports'), x='Reports', y='Caller', orientation='h')
    st.plotly_chart(fig, use_container_width=True)

elif st.session_state.active_chart == "hourly":
    df_filtered['Hour'] = df_filtered['Timestamp'].dt.hour
    fig = px.histogram(df_filtered, x='Hour', nbins=24)
    st.plotly_chart(fig, use_container_width=True)

elif st.session_state.active_chart == "heatmap":
    pivot = df_filtered.groupby(['Location (Taluka)', 'Type of Wildlife']).size().unstack(fill_value=0)
    if not pivot.empty:
        fig, ax = plt.subplots(figsize=(12, 6))
        sns.heatmap(pivot, annot=True, fmt='g', cmap='YlGnBu')
        st.pyplot(fig)
    else:
        st.info("No data available for selected filters to display heatmap.")

elif st.session_state.active_chart == "table":
    st.dataframe(df_filtered)

# Footer
st.markdown("---")
st.markdown("""
<p style='text-align: center;'>For Forest Department</p>
""", unsafe_allow_html=True)
