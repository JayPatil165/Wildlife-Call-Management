# Plotly Chart Setup Guide

## Overview
Plotly has been successfully integrated into the Wildlife Call Management Dashboard with theme-aware configurations.

## Files Created

### 1. `src/components/charts/plotly-wrapper.tsx`
- Dynamic wrapper for Plotly to handle client-side rendering
- Prevents SSR issues with Next.js
- Shows loading spinner while chart loads

### 2. `src/lib/plotly-config.ts`
- Light and dark theme layouts
- Common configuration settings
- Color palettes matching dashboard design
- Helper function `getLayout(isDark, customLayout)`

### 3. `src/components/charts/wildlife-incidents-chart.tsx`
- Example implementation of a bar chart
- Shows top 15 wildlife species by incident count
- Theme-aware using `useTheme()` hook

## Creating New Charts

### Template for new chart component:

```typescript
'use client'

import { useMemo } from 'react'
import { useTheme } from 'next-themes'
import { PlotlyWrapper } from './plotly-wrapper'
import { getLayout, plotConfig, colorPalette } from '@/lib/plotly-config'
import { IncidentData } from '@/types'

interface YourChartProps {
  data: IncidentData[]
}

export function YourChart({ data }: YourChartProps) {
  const { theme } = useTheme()
  const isDark = theme === 'dark'

  const chartData = useMemo(() => {
    // Process your data here
    // Return Plotly data format
    return [
      {
        type: 'bar', // or 'pie', 'scatter', 'line', etc.
        x: [...],
        y: [...],
        marker: {
          color: colorPalette.wildlife,
        },
      },
    ]
  }, [data, isDark])

  const layout = useMemo(
    () =>
      getLayout(isDark, {
        title: {
          text: 'Your Chart Title',
        },
        xaxis: {
          title: { text: 'X Axis Label' },
        },
        yaxis: {
          title: { text: 'Y Axis Label' },
        },
        height: 500,
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
```

### Steps to add a new chart:

1. Create new chart component in `src/components/charts/`
2. Import it in `chart-display.tsx`
3. Add conditional rendering in `ChartDisplay` component:
```typescript
if (chartType === 'your_chart_key') {
  return (
    <Card>
      <CardHeader>
        <CardTitle>{chartTitles[chartType]}</CardTitle>
      </CardHeader>
      <CardContent>
        <YourChart data={data} />
      </CardContent>
    </Card>
  )
}
```

## Available Chart Types

Plotly supports many chart types:
- `bar` - Bar charts
- `pie` - Pie charts
- `scatter` - Scatter plots
- `line` - Line charts
- `heatmap` - Heatmaps
- `box` - Box plots
- `histogram` - Histograms
- And many more...

## Color Palettes

Two palettes available in `plotly-config.ts`:
- `colorPalette.primary` - 10 vibrant colors
- `colorPalette.wildlife` - 10 darker shades for better contrast

## Theme Support

Charts automatically switch between light and dark themes using:
- `useTheme()` hook from next-themes
- Pre-configured layouts in `plotly-config.ts`
- Background colors, grid colors, and text colors adapt automatically

## Configuration

The `plotConfig` includes:
- Display mode bar (zoom, pan, download tools)
- Logo removed for cleaner look
- Image export settings (PNG, 1200x800, 2x scale)
- Responsive sizing enabled

## Next Steps

Implement remaining charts from `chart-selector.tsx`:
- [ ] Taluka Distribution (pie chart)
- [ ] Incident Types (grouped bar chart)
- [ ] Incident Frequency (line chart)
- [ ] Top Talukas (horizontal bar)
- [ ] Monthly Trend (line chart)
- [ ] Repeat Taluka (line chart)
- [ ] Wildlife Timeline (line chart)
- [ ] Monthly by Taluka (multi-line chart)
- [ ] Top Villages (horizontal bar)
- [ ] Frequent Callers (horizontal bar)
- [ ] Hourly Distribution (histogram)
- [ ] Heatmap (heatmap)
