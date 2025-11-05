'use client'

import { useMemo } from 'react'
import { useTheme } from 'next-themes'
import { PlotlyWrapper } from './plotly-wrapper'
import { getLayout, plotConfig, colorPalette } from '@/lib/plotly-config'
import { IncidentData } from '@/types'

interface TalukaDistributionChartProps {
  data: IncidentData[]
}

export function TalukaDistributionChart({ data }: TalukaDistributionChartProps) {
  const { theme } = useTheme()
  const isDark = theme === 'dark'

  const chartData = useMemo(() => {
    // Count incidents by taluka
    const talukaCounts = data.reduce((acc, incident) => {
      const taluka = incident['तालुका:']
      if (taluka) {
        acc[taluka] = (acc[taluka] || 0) + 1
      }
      return acc
    }, {} as Record<string, number>)

    // Sort by count for better visualization
    const sorted = Object.entries(talukaCounts)
      .sort(([, a], [, b]) => b - a)

    const labels = sorted.map(([name]) => name)
    const values = sorted.map(([, count]) => count)

    return [
      {
        type: 'pie' as const,
        labels: labels,
        values: values,
        marker: {
          colors: colorPalette.primary,
          line: {
            color: isDark ? '#1e293b' : '#ffffff',
            width: 2,
          },
        },
        textinfo: 'label+percent' as const,
        textposition: 'auto' as const,
        hovertemplate: '<b>%{label}</b><br>Incidents: %{value}<br>Percentage: %{percent}<extra></extra>',
        hole: 0.3, // Makes it a donut chart for better aesthetics
      },
    ]
  }, [data, isDark])

  const layout = useMemo(
    () =>
      getLayout(isDark, {
        title: {
          text: 'Incident Distribution by Taluka',
        },
        height: 500,
        showlegend: true,
        legend: {
          orientation: 'v',
          yanchor: 'middle',
          y: 0.5,
          xanchor: 'left',
          x: 1.02,
        },
        margin: { t: 50, b: 20, l: 20, r: 150 },
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
      style={{ width: '100%', height: '500px' }}
    />
  )
}
