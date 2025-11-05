# Wildlife Call Management - Next.js Dashboard

A modern, interactive dashboard for visualizing wildlife incident data built with Next.js, React, and TypeScript.

## Features

- 📊 Interactive charts with Plotly (heatmaps, trends, distributions)
- 🌓 Dark/Light theme support
- 📱 Responsive design
- 🔍 Advanced filtering options
- 📈 Real-time data visualization
- 🎨 Beautiful UI with shadcn/ui components

## Prerequisites

- Node.js 18+ and npm
- Google Sheets API credentials
- A Google Sheet with wildlife incident data

## Setup Instructions

### 1. Install Dependencies

```bash
npm install
```

### 2. Configure Google Sheets API

#### Get Credentials:

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project (or select an existing one)
3. Enable the **Google Sheets API**:
   - Go to "APIs & Services" > "Library"
   - Search for "Google Sheets API"
   - Click "Enable"
4. Create a Service Account:
   - Go to "APIs & Services" > "Credentials"
   - Click "Create Credentials" > "Service Account"
   - Fill in the details and create
   - Click on the created service account
   - Go to "Keys" tab > "Add Key" > "Create New Key" > "JSON"
   - Download the JSON file

#### Configure the Dashboard:

1. **Copy the example files:**
   ```bash
   cp credentials.json.example credentials.json
   cp sheetid.txt.example sheetid.txt
   ```

2. **Add your credentials:**
   - Open `credentials.json` and paste the entire content of the downloaded JSON file from Google Cloud

3. **Add your Sheet ID:**
   - Open your Google Sheet in a browser
   - The URL looks like: `https://docs.google.com/spreadsheets/d/SHEET_ID_HERE/edit`
   - Copy the `SHEET_ID_HERE` part
   - Paste it into `sheetid.txt`

4. **Share the Google Sheet:**
   - Open your Google Sheet
   - Click "Share" button
   - Add the `client_email` from your `credentials.json` file
   - Give it "Viewer" or "Editor" access

### 3. Run the Development Server

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

### 4. Build for Production

```bash
npm run build
npm start
```

## Project Structure

```
next-dashboard/
├── src/
│   ├── app/              # Next.js app router pages
│   │   ├── page.tsx      # Main dashboard page
│   │   ├── layout.tsx    # Root layout
│   │   └── actions.ts    # Server actions for data fetching
│   ├── components/       # React components
│   │   ├── charts/       # Chart components
│   │   ├── layout/       # Layout components
│   │   └── ui/           # shadcn/ui components
│   ├── lib/              # Utility functions
│   ├── types/            # TypeScript types
│   └── utils/            # Helper functions
├── public/               # Static assets
├── credentials.json      # Google API credentials (gitignored)
├── sheetid.txt          # Google Sheet ID (gitignored)
└── package.json         # Dependencies
```

## Important Files (Not in Git)

These files contain sensitive information and are **not committed to the repository**:

- `credentials.json` - Your Google Service Account credentials
- `sheetid.txt` - Your Google Sheet ID

You must create these files locally using the example files provided.

## Technologies Used

- **Next.js 16** - React framework
- **React 19** - UI library
- **TypeScript** - Type safety
- **Tailwind CSS** - Styling
- **Plotly.js** - Interactive charts
- **shadcn/ui** - UI components
- **Google Sheets API** - Data source

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm start` - Start production server
- `npm run lint` - Run ESLint

## Troubleshooting

### "Failed to fetch data" error

- Verify `credentials.json` has the correct service account details
- Verify `sheetid.txt` contains the correct Sheet ID
- Ensure the Google Sheet is shared with the service account email
- Check that Google Sheets API is enabled in your Google Cloud project

### Build errors

- Run `npm install` to ensure all dependencies are installed
- Delete `.next` folder and rebuild: `rm -rf .next && npm run build`

## Support

For issues or questions, please open an issue on the repository.

