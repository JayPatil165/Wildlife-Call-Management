import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import time

# Page configuration
st.set_page_config(
    page_title="Wildlife Call Management Dashboard",
    page_icon="🐾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main {
        padding: 0rem 1rem;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
    }
    .stTabs [data-baseweb="tab"] {
        padding: 1rem 2rem;
        font-size: 1.1rem;
    }
    h1 {
        color: #059669;
        padding-bottom: 1rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #059669 0%, #047857 100%);
        padding: 1.5rem;
        border-radius: 0.5rem;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state for auto-refresh
if 'last_refresh' not in st.session_state:
    st.session_state.last_refresh = datetime.now()
if 'auto_refresh' not in st.session_state:
    st.session_state.auto_refresh = False
if 'refresh_interval' not in st.session_state:
    st.session_state.refresh_interval = 300  # 5 minutes default

@st.cache_data(ttl=300)
def load_data():
    """Load data from Google Sheets"""
    try:
        # Setup credentials
        with open('sheetid.txt', 'r') as f:
            SHEET_ID = f.read().strip()
        
        scope = ['https://spreadsheets.google.com/feeds',
                 'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
        client = gspread.authorize(creds)
        
        # Open the sheet
        sheet = client.open_by_key(SHEET_ID).sheet1
        
        # Get all data
        data = sheet.get_all_records()
        df = pd.DataFrame(data)
        
        # Clean column names
        df.columns = df.columns.str.strip()
        
        # Parse timestamp
        if 'टाइमस्टॅम्प' in df.columns:
            df['parsed_date'] = pd.to_datetime(df['टाइमस्टॅम्प'], format='%d/%m/%Y %H:%M:%S', errors='coerce')
            df['date'] = df['parsed_date'].dt.date
            df['month'] = df['parsed_date'].dt.to_period('M').astype(str)
            df['hour'] = df['parsed_date'].dt.hour
            df['day_name'] = df['parsed_date'].dt.day_name()
        
        return df
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return pd.DataFrame()

def check_auto_refresh():
    """Check if auto-refresh should trigger"""
    if st.session_state.auto_refresh:
        time_since_refresh = (datetime.now() - st.session_state.last_refresh).total_seconds()
        if time_since_refresh >= st.session_state.refresh_interval:
            st.session_state.last_refresh = datetime.now()
            st.cache_data.clear()
            st.rerun()

# Sidebar
with st.sidebar:
    st.title("🐾 Wildlife Dashboard")
    st.markdown("---")
    
    # Auto-refresh settings
    st.subheader("Auto-Refresh")
    st.session_state.auto_refresh = st.checkbox("Enable Auto-Refresh", value=st.session_state.auto_refresh)
    
    if st.session_state.auto_refresh:
        interval_minutes = st.slider("Refresh Interval (minutes)", 1, 60, st.session_state.refresh_interval // 60)
        st.session_state.refresh_interval = interval_minutes * 60
        
        time_until_refresh = st.session_state.refresh_interval - (datetime.now() - st.session_state.last_refresh).total_seconds()
        if time_until_refresh > 0:
            st.info(f"Next refresh in: {int(time_until_refresh // 60)}m {int(time_until_refresh % 60)}s")
    
    # Manual refresh button
    if st.button("🔄 Refresh Now", use_container_width=True):
        st.session_state.last_refresh = datetime.now()
        st.cache_data.clear()
        st.rerun()
    
    st.markdown("---")
    
    # Load data
    df = load_data()
    
    if not df.empty:
        st.subheader("Filters")
        
        # Date range filter
        if 'parsed_date' in df.columns:
            min_date = df['parsed_date'].min().date()
            max_date = df['parsed_date'].max().date()
            
            date_range = st.date_input(
                "Date Range",
                value=(min_date, max_date),
                min_value=min_date,
                max_value=max_date
            )
            
            if len(date_range) == 2:
                df = df[(df['date'] >= date_range[0]) & (df['date'] <= date_range[1])]
        
        # Taluka filter
        if 'तालुका:' in df.columns:
            talukas = ['All'] + sorted(df['तालुका:'].dropna().unique().tolist())
            selected_taluka = st.multiselect("Taluka", talukas, default=['All'])
            
            if 'All' not in selected_taluka and selected_taluka:
                df = df[df['तालुका:'].isin(selected_taluka)]
        
        # Wildlife type filter
        if 'कोणत्या वन्यप्राण्याची नोंद करू इच्छिता:' in df.columns:
            wildlife_types = ['All'] + sorted(df['कोणत्या वन्यप्राण्याची नोंद करू इच्छिता:'].dropna().unique().tolist())
            selected_wildlife = st.multiselect("Wildlife Type", wildlife_types, default=['All'])
            
            if 'All' not in selected_wildlife and selected_wildlife:
                df = df[df['कोणत्या वन्यप्राण्याची नोंद करू इच्छिता:'].isin(selected_wildlife)]
        
        # Incident type filter
        if 'वन्यजीवांच्या बाबत आपण काय कळवू इच्छिता याची नोंद करा:' in df.columns:
            incident_types = ['All'] + sorted(df['वन्यजीवांच्या बाबत आपण काय कळवू इच्छिता याची नोंद करा:'].dropna().unique().tolist())
            selected_incident = st.multiselect("Incident Type", incident_types, default=['All'])
            
            if 'All' not in selected_incident and selected_incident:
                df = df[df['वन्यजीवांच्या बाबत आपण काय कळवू इच्छिता याची नोंद करा:'].isin(selected_incident)]
        
        st.markdown("---")
        st.caption(f"Last updated: {st.session_state.last_refresh.strftime('%H:%M:%S')}")

# Main content
if df.empty:
    st.error("No data available. Please check your Google Sheets connection.")
else:
    # Header with metrics
    st.title("Wildlife Incident Management Dashboard")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Incidents", len(df))
    
    with col2:
        if 'तालुका:' in df.columns:
            st.metric("Unique Talukas", df['तालुका:'].nunique())
    
    with col3:
        if 'गावाचे नाव:' in df.columns:
            st.metric("Unique Villages", df['गावाचे नाव:'].nunique())
    
    with col4:
        if 'कोणत्या वन्यप्राण्याची नोंद करू इच्छिता:' in df.columns:
            st.metric("Wildlife Species", df['कोणत्या वन्यप्राण्याची नोंद करू इच्छिता:'].nunique())
    
    st.markdown("---")
    
    # Tabs
    tabs = st.tabs(["📊 Overview", "📈 Charts", "📋 Raw Data"])
    
    # Overview Tab
    with tabs[0]:
        st.subheader("Key Insights")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Wildlife incidents by species
            if 'कोणत्या वन्यप्राण्याची नोंद करू इच्छिता:' in df.columns:
                wildlife_counts = df['कोणत्या वन्यप्राण्याची नोंद करू इच्छिता:'].value_counts().head(10)
                
                fig = go.Figure(data=[go.Bar(
                    x=wildlife_counts.index,
                    y=wildlife_counts.values,
                    marker_color='#059669'
                )])
                fig.update_layout(
                    title="Top 10 Wildlife Species by Incidents",
                    xaxis_title="Wildlife Species",
                    yaxis_title="Number of Incidents",
                    height=400
                )
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Taluka distribution
            if 'तालुका:' in df.columns:
                taluka_counts = df['तालुका:'].value_counts().head(10)
                
                fig = px.pie(
                    values=taluka_counts.values,
                    names=taluka_counts.index,
                    title="Incident Distribution by Taluka (Top 10)"
                )
                fig.update_traces(marker=dict(colors=px.colors.sequential.Greens))
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
        
        col3, col4 = st.columns(2)
        
        with col3:
            # Monthly trend
            if 'month' in df.columns:
                monthly_counts = df['month'].value_counts().sort_index()
                
                fig = go.Figure(data=[go.Scatter(
                    x=monthly_counts.index,
                    y=monthly_counts.values,
                    mode='lines+markers',
                    line=dict(color='#059669', width=3),
                    marker=dict(size=8)
                )])
                fig.update_layout(
                    title="Monthly Incident Trend",
                    xaxis_title="Month",
                    yaxis_title="Number of Incidents",
                    height=400
                )
                st.plotly_chart(fig, use_container_width=True)
        
        with col4:
            # Incident types
            if 'वन्यजीवांच्या बाबत आपण काय कळवू इच्छिता याची नोंद करा:' in df.columns:
                incident_counts = df['वन्यजीवांच्या बाबत आपण काय कळवू इच्छिता याची नोंद करा:'].value_counts()
                
                fig = go.Figure(data=[go.Bar(
                    y=incident_counts.index,
                    x=incident_counts.values,
                    orientation='h',
                    marker_color='#047857'
                )])
                fig.update_layout(
                    title="Incident Types",
                    xaxis_title="Count",
                    yaxis_title="Incident Type",
                    height=400
                )
                st.plotly_chart(fig, use_container_width=True)
    
    # Charts Tab
    with tabs[1]:
        chart_col1, chart_col2 = st.columns(2)
        
        with chart_col1:
            # Top villages
            if 'गावाचे नाव:' in df.columns:
                village_counts = df['गावाचे नाव:'].value_counts().head(15)
                
                fig = go.Figure(data=[go.Bar(
                    y=village_counts.index[::-1],
                    x=village_counts.values[::-1],
                    orientation='h',
                    marker_color='#10b981'
                )])
                fig.update_layout(
                    title="Top 15 Villages by Incidents",
                    xaxis_title="Number of Incidents",
                    yaxis_title="Village",
                    height=500
                )
                st.plotly_chart(fig, use_container_width=True)
            
            # Hourly distribution
            if 'hour' in df.columns:
                hourly_counts = df['hour'].value_counts().sort_index()
                
                fig = go.Figure(data=[go.Bar(
                    x=hourly_counts.index,
                    y=hourly_counts.values,
                    marker_color='#059669'
                )])
                fig.update_layout(
                    title="Incidents by Hour of Day",
                    xaxis_title="Hour",
                    yaxis_title="Number of Incidents",
                    height=400
                )
                st.plotly_chart(fig, use_container_width=True)
        
        with chart_col2:
            # Frequent callers
            if 'संपर्क क्रमांक:' in df.columns:
                caller_counts = df['संपर्क क्रमांक:'].value_counts().head(15)
                
                fig = go.Figure(data=[go.Bar(
                    y=caller_counts.index[::-1],
                    x=caller_counts.values[::-1],
                    orientation='h',
                    marker_color='#0d9488'
                )])
                fig.update_layout(
                    title="Top 15 Frequent Callers",
                    xaxis_title="Number of Calls",
                    yaxis_title="Contact Number",
                    height=500
                )
                st.plotly_chart(fig, use_container_width=True)
            
            # Heatmap - Day vs Hour
            if 'day_name' in df.columns and 'hour' in df.columns:
                # Create pivot table
                day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
                heatmap_data = df.groupby(['day_name', 'hour']).size().reset_index(name='count')
                heatmap_pivot = heatmap_data.pivot(index='day_name', columns='hour', values='count').fillna(0)
                heatmap_pivot = heatmap_pivot.reindex([d for d in day_order if d in heatmap_pivot.index])
                
                fig = go.Figure(data=go.Heatmap(
                    z=heatmap_pivot.values,
                    x=heatmap_pivot.columns,
                    y=heatmap_pivot.index,
                    colorscale='Greens',
                    hoverongaps=False
                ))
                fig.update_layout(
                    title="Incident Heatmap: Day vs Hour",
                    xaxis_title="Hour of Day",
                    yaxis_title="Day of Week",
                    height=400
                )
                st.plotly_chart(fig, use_container_width=True)
        
        # Full width charts
        st.markdown("---")
        
        # Wildlife timeline
        if 'parsed_date' in df.columns and 'कोणत्या वन्यप्राण्याची नोंद करू इच्छिता:' in df.columns:
            top_wildlife = df['कोणत्या वन्यप्राण्याची नोंद करू इच्छिता:'].value_counts().head(5).index
            
            fig = go.Figure()
            for wildlife in top_wildlife:
                wildlife_df = df[df['कोणत्या वन्यप्राण्याची नोंद करू इच्छिता:'] == wildlife]
                daily_counts = wildlife_df.groupby('date').size()
                
                fig.add_trace(go.Scatter(
                    x=daily_counts.index,
                    y=daily_counts.values,
                    mode='lines+markers',
                    name=wildlife
                ))
            
            fig.update_layout(
                title="Wildlife Incident Timeline (Top 5 Species)",
                xaxis_title="Date",
                yaxis_title="Number of Incidents",
                height=500,
                hovermode='x unified'
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Monthly incidents by taluka
        if 'month' in df.columns and 'तालुका:' in df.columns:
            top_talukas = df['तालुका:'].value_counts().head(5).index
            
            fig = go.Figure()
            for taluka in top_talukas:
                taluka_df = df[df['तालुका:'] == taluka]
                monthly_counts = taluka_df['month'].value_counts().sort_index()
                
                fig.add_trace(go.Scatter(
                    x=monthly_counts.index,
                    y=monthly_counts.values,
                    mode='lines+markers',
                    name=taluka
                ))
            
            fig.update_layout(
                title="Monthly Incidents by Taluka (Top 5)",
                xaxis_title="Month",
                yaxis_title="Number of Incidents",
                height=500,
                hovermode='x unified'
            )
            st.plotly_chart(fig, use_container_width=True)
    
    # Raw Data Tab
    with tabs[2]:
        st.subheader("Raw Data")
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.info(f"Showing {len(df)} records")
        
        with col2:
            # Download button
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Download CSV",
                data=csv,
                file_name=f"wildlife_incidents_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
                use_container_width=True
            )
        
        # Display data
        st.dataframe(
            df,
            use_container_width=True,
            height=600
        )

# Auto-refresh check (at the end)
check_auto_refresh()
