'use client'

import { useMemo } from 'react'
import { useTheme } from 'next-themes'
import { PlotlyWrapper } from './plotly-wrapper'
import { getLayout, plotConfig, colorPalette } from '@/lib/plotly-config'
import { IncidentData } from '@/types'
import { parseIncidentDate } from '@/utils/date-parser'

interface MonthlyByTalukaChartProps {
  data: IncidentData[]
}

export function MonthlyByTalukaChart({ data }: MonthlyByTalukaChartProps) {
  const { theme } = useTheme()
  const isDark = theme === 'dark'

  const chartData = useMemo(() => {
    // Group by month and taluka
    const monthlyTalukaData = data.reduce((acc, incident) => {
      const date = parseIncidentDate(incident.Timestamp)
      if (date) {
        const year = date.getFullYear()
        const month = date.getMonth() + 1
        const monthStr = `${year}-${month.toString().padStart(2, '0')}`
        const taluka = incident['तालुका:']
        
        if (taluka) {
          const key = `${monthStr}|||${taluka}`
          acc[key] = (acc[key] || 0) + 1
        }
      }
      return acc
    }, {} as Record<string, number>)

    // Get all talukas by total incidents
    const talukaCounts = data.reduce((acc, incident) => {
      const taluka = incident['तालुका:']
      if (taluka) {
        acc[taluka] = (acc[taluka] || 0) + 1
      }
      return acc
    }, {} as Record<string, number>)

    const allTalukas = Object.entries(talukaCounts)
      .sort(([, a], [, b]) => b - a)
      .map(([taluka]) => taluka)

    // Create a trace for each taluka
    return allTalukas.map((taluka, index) => {
      // Get all months for this taluka
      const talukaData = Object.entries(monthlyTalukaData)
        .filter(([key]) => key.endsWith(`|||${taluka}`))
        .map(([key, count]) => ({
          month: key.split('|||')[0],
          count
        }))
        .sort((a, b) => a.month.localeCompare(b.month))

      const months = talukaData.map(d => d.month)
      const counts = talukaData.map(d => d.count)

      return {
        type: 'scatter' as const,
        mode: 'lines+markers' as const,
        name: taluka,
        x: months,
        y: counts,
        line: {
          color: colorPalette.primary[index % colorPalette.primary.length],
          width: 2,
        },
        marker: {
          color: colorPalette.primary[index % colorPalette.primary.length],
          size: 7,
        },
        hovertemplate: `<b>${taluka}</b><br>%{x}<br>Incidents: %{y}<extra></extra>`,
      }
    })
  }, [data])

  const layout = useMemo(
    () =>
      getLayout(isDark, {
        title: {
          text: 'Monthly Incidents by Taluka (All Talukas)',
        },
        xaxis: {
          title: {
            text: 'Month',
          },
          tickangle: -45,
          automargin: true,
        },
        yaxis: {
          title: {
            text: 'Monthly Incident Count',
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
