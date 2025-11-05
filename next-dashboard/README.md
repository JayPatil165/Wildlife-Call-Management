# Next.js Wildlife Dashboard

A modern, interactive web dashboard for analyzing wildlife incident data with beautiful visualizations and real-time filtering.

## Features

### 📊 Comprehensive Visualizations
- **Wildlife Species Analysis** - Bar charts showing incident distribution by species
- **Geographic Distribution** - Pie charts and bar graphs for taluka and village hotspots
- **Temporal Trends** - Line charts for monthly patterns and time-based analysis
- **Heatmaps** - Visual intensity maps for day-wise incident patterns
- **Incident Types** - Breakdown of human-wildlife conflict categories
- **Response Analysis** - Frequent caller tracking and repeat location monitoring

### 🎨 User Experience
- **Dark/Light Themes** - Eye-friendly viewing in any environment
- **Responsive Design** - Works on desktop, tablet, and mobile
- **Interactive Charts** - Zoom, pan, hover for details, download as images
- **Real-time Filtering** - Filter by date range, taluka, wildlife type, and incident type
- **Export Capabilities** - Download filtered data as CSV for reports

### ⚡ Technical Highlights
- Built with Next.js 16 and React 19 for blazing-fast performance
- TypeScript for robust, error-free code
- Plotly.js for professional, interactive charts
- Google Sheets as live data source - no database setup needed

## Quick Start

See the main [SETUP.md](../SETUP.md) in the repository root for complete installation instructions.

**In short:**
```bash
npm install
# Configure credentials.json and sheetid.txt
npm run dev
```

Open http://localhost:3000

## Available Charts

- Wildlife Incidents by Species
- Taluka Distribution
- Incident Types Breakdown
- Incident Frequency Over Time
- Top Talukas (Most Incidents)
- Monthly Trend Analysis
- Repeat Taluka Analysis
- Wildlife Incident Timeline
- Monthly Incidents by Taluka
- Top Villages
- Frequent Callers
- Hourly Distribution
- Day/Hour Heatmap

## How It Helps

**For Forest Officers:**
- Identify high-priority areas needing immediate attention
- Track seasonal patterns to plan preventive measures
- Monitor response effectiveness through repeat incident analysis

**For Administrators:**
- Generate quick reports with filtered, exportable data
- Visualize team performance and coverage
- Make data-driven resource allocation decisions

**For Researchers:**
- Analyze wildlife movement and conflict patterns
- Study temporal correlations in incidents
- Export data for further statistical analysis

## Technologies

- **Next.js 16** - React framework with server-side rendering
- **React 19** - Modern UI library
- **TypeScript** - Type-safe JavaScript
- **Tailwind CSS** - Utility-first styling
- **Plotly.js** - Interactive, publication-quality charts
- **shadcn/ui** - Beautiful, accessible components
- **Google Sheets API** - Live data connection

## Scripts

```bash
npm run dev      # Development server (http://localhost:3000)
npm run build    # Production build
npm start        # Run production build
npm run lint     # Check code quality
```

## Support

For setup issues, see [SETUP.md](../SETUP.md) or open an issue on GitHub.
