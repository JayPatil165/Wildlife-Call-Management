'use client'

import { useMemo } from 'react'
import { useTheme } from 'next-themes'
import { PlotlyWrapper } from './plotly-wrapper'
import { getLayout, plotConfig, colorPalette } from '@/lib/plotly-config'
import { IncidentData } from '@/types'

interface FrequentCallersChartProps {
  data: IncidentData[]
}

export function FrequentCallersChart({ data }: FrequentCallersChartProps) {
  const { theme } = useTheme()
  const isDark = theme === 'dark'

  const chartData = useMemo(() => {
    // Count reports by caller
    const callerCounts = data.reduce((acc, incident) => {
      const caller = incident['संपर्क करणाऱ्याचे नाव:']
      if (caller) {
        acc[caller] = (acc[caller] || 0) + 1
      }
      return acc
    }, {} as Record<string, number>)

    // Get top 10 and sort by count (ascending for horizontal bar)
    const sorted = Object.entries(callerCounts)
      .sort(([, a], [, b]) => b - a)
      .slice(0, 10)
      .reverse() // Reverse for horizontal bar so highest is on top

    const labels = sorted.map(([name]) => name)
    const values = sorted.map(([, count]) => count)

    return [
      {
        type: 'bar' as const,
        orientation: 'h' as const,
        y: labels,
        x: values,
        marker: {
          color: colorPalette.wildlife,
          line: {
            color: isDark ? '#1e293b' : '#ffffff',
            width: 2,
          },
        },
        hovertemplate: '<b>%{y}</b><br>Reports: %{x}<extra></extra>',
      },
    ]
  }, [data, isDark])

  const layout = useMemo(
    () =>
      getLayout(isDark, {
        title: {
          text: 'Top 10 Frequent Callers',
        },
        xaxis: {
          title: {
            text: 'Number of Reports',
          },
        },
        yaxis: {
          title: {
            text: 'Caller Name',
          },
          automargin: true,
        },
        height: 500,
        margin: { t: 50, b: 60, l: 200, r: 20 },
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
