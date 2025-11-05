'use client'

import { useMemo } from 'react'
import { useTheme } from 'next-themes'
import { PlotlyWrapper } from './plotly-wrapper'
import { getLayout, plotConfig, colorPalette } from '@/lib/plotly-config'
import { IncidentData } from '@/types'
import { parseIncidentDate } from '@/utils/date-parser'

interface WildlifeTimelineChartProps {
  data: IncidentData[]
}

export function WildlifeTimelineChart({ data }: WildlifeTimelineChartProps) {
  const { theme } = useTheme()
  const isDark = theme === 'dark'

  const chartData = useMemo(() => {
    // Group by date and wildlife type
    const dailyWildlifeData = data.reduce((acc, incident) => {
      const date = parseIncidentDate(incident.Timestamp)
      if (date) {
        const dateStr = date.toISOString().split('T')[0] // YYYY-MM-DD
        const wildlife = incident['कोणत्या वन्यप्राण्याची नोंद करू इच्छिता:']
        
        if (wildlife) {
          const key = `${dateStr}|||${wildlife}`
          acc[key] = (acc[key] || 0) + 1
        }
      }
      return acc
    }, {} as Record<string, number>)

    // Get all wildlife types by total incidents
    const wildlifeCounts = data.reduce((acc, incident) => {
      const wildlife = incident['कोणत्या वन्यप्राण्याची नोंद करू इच्छिता:']
      if (wildlife) {
        acc[wildlife] = (acc[wildlife] || 0) + 1
      }
      return acc
    }, {} as Record<string, number>)

    const allWildlife = Object.entries(wildlifeCounts)
      .sort(([, a], [, b]) => b - a)
      .map(([wildlife]) => wildlife)

    // Create a trace for each wildlife type
    return allWildlife.map((wildlife, index) => {
      // Get all dates for this wildlife
      const wildlifeData = Object.entries(dailyWildlifeData)
        .filter(([key]) => key.endsWith(`|||${wildlife}`))
        .map(([key, count]) => ({
          date: key.split('|||')[0],
          count
        }))
        .sort((a, b) => a.date.localeCompare(b.date))

      const dates = wildlifeData.map(d => d.date)
      const counts = wildlifeData.map(d => d.count)

      return {
        type: 'scatter' as const,
        mode: 'lines+markers' as const,
        name: wildlife,
        x: dates,
        y: counts,
        line: {
          color: colorPalette.wildlife[index % colorPalette.wildlife.length],
          width: 2,
        },
        marker: {
          color: colorPalette.wildlife[index % colorPalette.wildlife.length],
          size: 5,
        },
        hovertemplate: `<b>${wildlife}</b><br>%{x}<br>Incidents: %{y}<extra></extra>`,
      }
    })
  }, [data])

  const layout = useMemo(
    () =>
      getLayout(isDark, {
        title: {
          text: 'Wildlife Incident Timeline (All Species)',
        },
        xaxis: {
          title: {
            text: 'Date',
          },
          tickangle: -45,
          automargin: true,
        },
        yaxis: {
          title: {
            text: 'Daily Incident Count',
          },
        },
        height: 600,
        margin: { t: 50, b: 100, l: 60, r: 200 },
        showlegend: true,
        legend: {
          orientation: 'v',
          yanchor: 'top',
          y: 1,
          xanchor: 'left',
          x: 1.02,
          font: {
            size: 10,
          },
        },
      }),
    [isDark]
  )

  return (
    <PlotlyWrapper
      data={chartData}
      layout={layout}
      config={plotConfig}
      className="w-full"
      useResizeHandler
      style={{ width: '100%', height: '600px' }}
    />
  )
}
