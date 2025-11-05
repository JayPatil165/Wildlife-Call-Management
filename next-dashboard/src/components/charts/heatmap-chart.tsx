'use client'

import { useMemo } from 'react'
import { useTheme } from 'next-themes'
import { PlotlyWrapper } from './plotly-wrapper'
import { getLayout, plotConfig } from '@/lib/plotly-config'
import { IncidentData } from '@/types'

interface HeatmapChartProps {
  data: IncidentData[]
}

export function HeatmapChart({ data }: HeatmapChartProps) {
  const { theme } = useTheme()
  const isDark = theme === 'dark'

  const chartData = useMemo(() => {
    // Group by taluka and wildlife type
    const grouped = data.reduce((acc, incident) => {
      const taluka = incident['तालुका:']
      const wildlife = incident['कोणत्या वन्यप्राण्याची नोंद करू इच्छिता:']
      
      if (taluka && wildlife) {
        const key = `${taluka}|||${wildlife}`
        acc[key] = (acc[key] || 0) + 1
      }
      return acc
    }, {} as Record<string, number>)

    // Get unique talukas and wildlife types (sorted by total count)
    const talukaCounts = data.reduce((acc, incident) => {
      const taluka = incident['तालुका:']
      if (taluka) acc[taluka] = (acc[taluka] || 0) + 1
      return acc
    }, {} as Record<string, number>)

    const wildlifeCounts = data.reduce((acc, incident) => {
      const wildlife = incident['कोणत्या वन्यप्राण्याची नोंद करू इच्छिता:']
      if (wildlife) acc[wildlife] = (acc[wildlife] || 0) + 1
      return acc
    }, {} as Record<string, number>)

    // Get top 15 of each for better visualization
    const talukas = Object.entries(talukaCounts)
      .sort(([, a], [, b]) => b - a)
      .slice(0, 15)
      .map(([t]) => t)

    const wildlifeTypes = Object.entries(wildlifeCounts)
      .sort(([, a], [, b]) => b - a)
      .slice(0, 15)
      .map(([w]) => w)

    // Create the z-matrix (2D array) for the heatmap
    const zMatrix = talukas.map(taluka => 
      wildlifeTypes.map(wildlife => {
        const key = `${taluka}|||${wildlife}`
        return grouped[key] || 0
      })
    )

    // Create text annotations for each cell
    const textMatrix = zMatrix.map(row => row.map(val => val > 0 ? val.toString() : ''))

    return [
      {
        type: 'heatmap' as const,
        x: wildlifeTypes,
        y: talukas,
        z: zMatrix,
        text: textMatrix as any,
        texttemplate: '%{text}',
        textfont: {
          color: isDark ? '#f1f5f9' : '#1e293b',
          size: 10,
        },
        colorscale: [
          [0, isDark ? '#0f172a' : '#f1f5f9'],
          [0.2, isDark ? '#1e3a5f' : '#dbeafe'],
          [0.4, isDark ? '#2563eb' : '#93c5fd'],
          [0.6, isDark ? '#059669' : '#6ee7b7'],
          [0.8, isDark ? '#f59e0b' : '#fcd34d'],
          [1, isDark ? '#dc2626' : '#f87171'],
        ] as Array<[number, string]>,
        hovertemplate: '<b>Taluka:</b> %{y}<br><b>Wildlife:</b> %{x}<br><b>Incidents:</b> %{z}<extra></extra>',
        colorbar: {
          title: {
            text: 'Incidents',
            side: 'right' as const,
          },
          tickfont: {
            color: isDark ? '#cbd5e1' : '#6b7280',
          },
        },
      },
    ]
  }, [data, isDark])

  const layout = useMemo(
    () =>
      getLayout(isDark, {
        title: {
          text: 'Incident Heatmap: Taluka vs Wildlife Type',
        },
        xaxis: {
          title: {
            text: 'Wildlife Type',
          },
          tickangle: -45,
          automargin: true,
          side: 'bottom',
        },
        yaxis: {
          title: {
            text: 'Taluka',
          },
          automargin: true,
        },
        height: 600,
        margin: { t: 50, b: 150, l: 150, r: 100 },
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
