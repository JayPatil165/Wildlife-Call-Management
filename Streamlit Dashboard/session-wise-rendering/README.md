# Streamlit Wildlife Dashboard

Python-based interactive dashboard for analyzing wildlife incident data using Streamlit.

## Features

- 📊 **Comprehensive Charts** - All wildlife analytics in one place
- 🔄 **Auto-Refresh** - Configurable auto-sync with Google Sheets data
- 🎯 **Session Management** - All charts rendered on single page
- 📋 **Raw Data Export** - Download filtered data as CSV
- 🔍 **Advanced Filters** - Date range, taluka, wildlife type, incident type
- ⚡ **Real-time Updates** - Automatic data synchronization

## Charts Included

- Wildlife Species Distribution (Top 10)
- Taluka Incident Distribution
- Monthly Trend Analysis
- Incident Types Breakdown
- Top Villages by Incidents
- Frequent Callers Analysis
- Hourly Distribution
- Day vs Hour Heatmap
- Wildlife Incident Timeline
- Monthly Incidents by Taluka

## Quick Start

See the main [SETUP.md](../../SETUP.md) for detailed setup instructions.

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Auto-Refresh Feature

The dashboard includes automatic data refresh:
- Enable/disable in sidebar
- Set refresh interval (1-60 minutes)
- Manual refresh button available
- Shows countdown to next refresh

## Technologies

- **Streamlit** - Web framework
- **Pandas** - Data processing
- **Plotly** - Interactive charts
- **gspread** - Google Sheets integration
