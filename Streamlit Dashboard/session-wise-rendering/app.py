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
    # Read Sheet ID from file
    try:
        with open("sheetid.txt", "r") as f:
            sheet_id = f.read().strip()
    except FileNotFoundError:
        st.error("❌ Missing sheetid.txt file! Please create it with your Google Sheet ID.")
        return pd.DataFrame()
    
    if not sheet_id:
        st.error("❌ Empty Google Sheet ID! Please add your sheet ID to sheetid.txt.")
        return pd.DataFrame()

    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    
    try:
        creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
    except FileNotFoundError:
        st.error("❌ Missing credentials.json file! Please add your Google service account credentials.")
        return pd.DataFrame()
    
    client = gspread.authorize(creds)

    try:
        sheet = client.open_by_key(sheet_id)
        worksheet = sheet.worksheet("Form_responses_1")
        data = worksheet.get_all_records()
        df = pd.DataFrame(data)
        df['Timestamp'] = pd.to_datetime(df['Timestamp'], errors='coerce')
        return df
    except Exception as e:
        st.error(f"⚠️ Error loading data: {e}")
        return pd.DataFrame()

df = load_data()
st_autorefresh(10*1000, key="datarefresh")

# --------------------------
# SIDEBAR FILTERS
# --------------------------
st.sidebar.title("🔎 Filter Data")

if not df.empty:
    wildlife_types = st.sidebar.multiselect(
        "🦝 Type of Wildlife",
        df['कोणत्या वन्यप्राण्याची नोंद करू इच्छिता:'].unique(),
        default=df['कोणत्या वन्यप्राण्याची नोंद करू इच्छिता:'].unique()
    )

    talukas = st.sidebar.multiselect(
        "📍 Taluka",
        df['तालुका:'].unique(),
        default=df['तालुका:'].unique()
    )

    min_date = df['Timestamp'].min().date()
    max_date = df['Timestamp'].max().date()
    date_range = st.sidebar.date_input("📆 Date Range", [min_date, max_date])

    df_filtered = df[
        (df['कोणत्या वन्यप्राण्याची नोंद करू इच्छिता:'].isin(wildlife_types)) &
        (df['तालुका:'].isin(talukas)) &
        (df['Timestamp'].dt.date >= date_range[0]) &
        (df['Timestamp'].dt.date <= date_range[1])
    ]
else:
    st.warning("No data loaded yet. Check your Google Sheet ID or credentials.")
    st.stop()

# --------------------------
# HEADER + KPIs
# --------------------------
st.markdown("""
<h1 style='text-align: center;'>🦁 Wildlife Incident Dashboard</h1>
""", unsafe_allow_html=True)

total_incidents = len(df_filtered)
wildlife_types_count = df_filtered['कोणत्या वन्यप्राण्याची नोंद करू इच्छिता:'].nunique()
villages_count = df_filtered['गावाचे नाव:'].nunique()
total_calls = df_filtered["संपर्क करणाऱ्याचे नाव:"].count()

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

cols = st.columns(7)
for i, (label, key) in enumerate(chart_buttons.items()):
    with cols[i % 7]:
        if st.button(label):
            st.session_state.active_chart = key

# --------------------------
# CHART RENDERING
# --------------------------
if st.session_state.active_chart == "wildlife":
    data = df_filtered['कोणत्या वन्यप्राण्याची नोंद करू इच्छिता:'].value_counts().reset_index()
    data.columns = ['Wildlife', 'Count']
    fig = px.bar(data, x='Wildlife', y='Count', color='Wildlife')
    st.plotly_chart(fig, use_container_width=True)

elif st.session_state.active_chart == "taluka":
    data = df_filtered['तालुका:'].value_counts().reset_index()
    data.columns = ['Taluka', 'Count']
    fig = px.pie(data, names='Taluka', values='Count', hole=0.4)
    st.plotly_chart(fig, use_container_width=True)

elif st.session_state.active_chart == "types":
    combo = df_filtered.groupby(['कोणत्या वन्यप्राण्याची नोंद करू इच्छिता:', 'वन्यजीवांच्या बाबत आपण काय कळवू इच्छिता याची नोंद करा:']).size().reset_index(name='Count')
    fig = px.bar(combo, x='कोणत्या वन्यप्राण्याची नोंद करू इच्छिता:', y='Count', color='वन्यजीवांच्या बाबत आपण काय कळवू इच्छिता याची नोंद करा:', barmode='group')
    st.plotly_chart(fig, use_container_width=True)

elif st.session_state.active_chart == "incident_freq":
    freq = df_filtered['वन्यजीवांच्या बाबत आपण काय कळवू इच्छिता याची नोंद करा:'].value_counts().reset_index()
    freq.columns = ['वन्यजीवांच्या बाबत आपण काय कळवू इच्छिता याची नोंद करा:', 'Count']
    fig = px.bar(freq, x='वन्यजीवांच्या बाबत आपण काय कळवू इच्छिता याची नोंद करा:', y='Count', color='Count')
    st.plotly_chart(fig, use_container_width=True)

elif st.session_state.active_chart == "top_talukas":
    top_talukas = df_filtered['तालुका:'].value_counts().head(10).reset_index()
    top_talukas.columns = ['Taluka', 'Incidents']
    fig = px.bar(top_talukas.sort_values(by='Incidents'), x='Incidents', y='Taluka', orientation='h')
    st.plotly_chart(fig, use_container_width=True)

elif st.session_state.active_chart == "monthly":
    df_filtered['Month'] = df_filtered['Timestamp'].dt.to_period("M").astype(str)
    monthly = df_filtered.groupby("Month").size().reset_index(name="Incidents")
    fig = px.line(monthly, x='Month', y='Incidents', markers=True)
    st.plotly_chart(fig, use_container_width=True)

elif st.session_state.active_chart == "repeat":
    repeat = df_filtered.groupby([df_filtered['Timestamp'].dt.date, 'तालुका:']).size().reset_index(name='Count')
    top = repeat['तालुका:'].value_counts().head(5).index
    repeat = repeat[repeat['तालुका:'].isin(top)]
    fig = px.line(repeat, x='Timestamp', y='Count', color='तालुका:')
    st.plotly_chart(fig, use_container_width=True)

elif st.session_state.active_chart == "timeline":
    timeline = df_filtered.groupby([df_filtered['Timestamp'].dt.date, 'कोणत्या वन्यप्राण्याची नोंद करू इच्छिता:']).size().reset_index(name='Incidents')
    fig = px.line(timeline, x='Timestamp', y='Incidents', color='कोणत्या वन्यप्राण्याची नोंद करू इच्छिता:')
    st.plotly_chart(fig, use_container_width=True)

elif st.session_state.active_chart == "monthly_taluka":
    df_filtered['Month'] = df_filtered['Timestamp'].dt.to_period("M").astype(str)
    data = df_filtered.groupby(['Month', 'तालुका:']).size().reset_index(name='Incidents')
    fig = px.line(data, x='Month', y='Incidents', color='तालुका:', markers=True)
    st.plotly_chart(fig, use_container_width=True)

elif st.session_state.active_chart == "villages":
    top_villages = df_filtered['गावाचे नाव:'].value_counts().head(10).reset_index()
    top_villages.columns = ['Village', 'Incidents']
    fig = px.bar(top_villages.sort_values(by='Incidents'), x='Incidents', y='Village', orientation='h')
    st.plotly_chart(fig, use_container_width=True)

elif st.session_state.active_chart == "callers":
    top_callers = df_filtered['संपर्क करणाऱ्याचे नाव:'].value_counts().head(10).reset_index()
    top_callers.columns = ['Caller', 'Reports']
    fig = px.bar(top_callers.sort_values(by='Reports'), x='Reports', y='Caller', orientation='h')
    st.plotly_chart(fig, use_container_width=True)

elif st.session_state.active_chart == "hourly":
    df_filtered['Hour'] = df_filtered['Timestamp'].dt.hour
    fig = px.histogram(df_filtered, x='Hour', nbins=24)
    st.plotly_chart(fig, use_container_width=True)

elif st.session_state.active_chart == "heatmap":
    pivot = df_filtered.groupby(['तालुका:', 'कोणत्या वन्यप्राण्याची नोंद करू इच्छिता:']).size().unstack(fill_value=0)
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.heatmap(pivot, annot=True, fmt='g', cmap='YlGnBu', ax=ax)
    ax.set_xlabel("कोणत्या वन्यप्राण्याची नोंद करू इच्छिता:")
    ax.set_ylabel("तालुका:")
    ax.set_title("तालुका व वन्यप्राणी प्रकारावर आधारित उष्णता नकाशा")
    st.pyplot(fig)

elif st.session_state.active_chart == "table":
    st.dataframe(df_filtered)

# Footer
st.markdown("---")
st.markdown("""
<p style='text-align: center;'>For Forest Department</p>
""", unsafe_allow_html=True)
