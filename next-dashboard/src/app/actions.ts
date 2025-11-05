'use server'

import { google } from 'googleapis'
import fs from 'fs'
import path from 'path'
import { IncidentData } from '@/types'

export async function fetchIncidentData(): Promise<IncidentData[]> {
  try {
    // Read credentials
    const credentialsPath = path.join(process.cwd(), 'credentials.json')
    const credentials = JSON.parse(fs.readFileSync(credentialsPath, 'utf8'))

    // Hardcoded sheet ID from Streamlit app
    const sheetId = '1eey_a4t5EOL_nyEDau4FLvXomcnwgxWa5F3Rjd52OQg'

    // Authenticate with Google Sheets
    const auth = new google.auth.GoogleAuth({
      credentials,
      scopes: ['https://www.googleapis.com/auth/spreadsheets.readonly'],
    })

    const sheets = google.sheets({ version: 'v4', auth })

    // Fetch data from the sheet
    const response = await sheets.spreadsheets.values.get({
      spreadsheetId: sheetId,
      range: 'Form_responses_1!A:Z', // Get all columns
    })

    const rows = response.data.values

    if (!rows || rows.length === 0) {
      return []
    }

    // Convert to our data structure
    const headers = rows[0]
    const data = rows.slice(1).map((row: any[]) => {
      const obj: any = {}
      headers.forEach((header, index) => {
        obj[header] = row[index] || ''
      })
      return obj as IncidentData
    })

    console.log('Fetched rows from Google Sheets:', rows.length - 1) // -1 for header
    console.log('Sample data:', data[0])
    
    return data
  } catch (error) {
    console.error('Error fetching data from Google Sheets:', error)
    throw new Error('Failed to fetch incident data')
  }
}
