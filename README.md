# Wildlife Call Management System

A comprehensive dashboard system for managing and visualizing wildlife incident data, built with both Next.js (React) and Streamlit (Python).

## Project Structure

This repository contains two separate dashboard implementations:

- **`next-dashboard/`** - Modern Next.js/React dashboard (main branch)
- **`Streamlit Dashboard/`** - Python Streamlit dashboard (python branch)

## Branches

- `main` - Next.js/React implementation
- `python` - Streamlit/Python implementation

## Setup Instructions

### Prerequisites

Both implementations require:
- Google Sheets API credentials
- A Google Sheet ID containing the wildlife incident data

### Configuration

1. **Get Google Sheets API Credentials:**
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project or select existing one
   - Enable Google Sheets API
   - Create a service account and download the JSON credentials file
   - Share your Google Sheet with the service account email

2. **Configure Credentials:**
   
   For **Next.js Dashboard**:
   ```bash
   cd next-dashboard
   cp credentials.json.example credentials.json
   cp sheetid.txt.example sheetid.txt
   # Edit both files with your actual credentials and sheet ID
   ```

   For **Streamlit Dashboard**:
   ```bash
   cd "Streamlit Dashboard/session-wise-rendering"
   cp credentials.json.example credentials.json
   cp sheetid.txt.example sheetid.txt
   # Edit both files with your actual credentials and sheet ID
   ```

### Next.js Dashboard (main branch)

```bash
cd next-dashboard
npm install
npm run dev
```

Open [http://localhost:3000](http://localhost:3000)

**Features:**
- Interactive charts with Plotly
- Dark/Light theme support
- Responsive design with Tailwind CSS
- Real-time data filtering
- Multiple chart types (heatmaps, trends, distributions)

### Streamlit Dashboard (python branch)

```bash
cd "Streamlit Dashboard/session-wise-rendering"
pip install -r requirements.txt
streamlit run app.py
```

**Features:**
- Python-based analytics
- Interactive filters
- Multiple visualization types
- Session-based state management

## Important Notes

⚠️ **Never commit sensitive files:**
- `credentials.json` - Contains your Google API credentials
- `sheetid.txt` - Contains your Google Sheet ID

These files are listed in `.gitignore` and example files are provided instead.

## Technologies Used

### Next.js Dashboard
- Next.js 16
- React 19
- TypeScript
- Tailwind CSS
- Plotly.js
- shadcn/ui components

### Streamlit Dashboard
- Python 3.x
- Streamlit
- Pandas
- Plotly
- Google Sheets API

## Contributing

When contributing, ensure you:
1. Never commit credentials or sensitive data
2. Use the appropriate branch for your changes
3. Test thoroughly before submitting PRs

## License

[Add your license here]
