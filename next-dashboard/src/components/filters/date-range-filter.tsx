'use client'

import { useState, useEffect } from 'react'
import { Calendar } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Card, CardContent } from '@/components/ui/card'

interface DateRangeFilterProps {
  minDate: Date
  maxDate: Date
  value: [Date, Date]
  onChange: (range: [Date, Date]) => void
}

export function DateRangeFilter({ minDate, maxDate, value, onChange }: DateRangeFilterProps) {
  const [startDate, setStartDate] = useState(value[0])
  const [endDate, setEndDate] = useState(value[1])

  // Sync with parent when value prop changes (e.g., on reset)
  useEffect(() => {
    setStartDate(value[0])
    setEndDate(value[1])
  }, [value])

  const formatDate = (date: Date) => {
    return date.toISOString().split('T')[0]
  }

  const handleStartChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const newStart = new Date(e.target.value)
    setStartDate(newStart)
    onChange([newStart, endDate])
  }

  const handleEndChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const newEnd = new Date(e.target.value)
    setEndDate(newEnd)
    onChange([startDate, newEnd])
  }

  return (
    <div className="space-y-2">
      <label className="text-sm font-semibold text-gray-700 dark:text-slate-300 flex items-center gap-2">
        <Calendar className="h-4 w-4 text-emerald-600 dark:text-emerald-400" />
        Date Range
      </label>
      <div className="flex gap-2 items-center">
        <input
          type="date"
          value={formatDate(startDate)}
          min={formatDate(minDate)}
          max={formatDate(maxDate)}
          onChange={handleStartChange}
          className="flex h-10 w-full rounded-lg border border-gray-300 dark:border-slate-600 bg-white dark:bg-slate-800 px-3 py-2 text-sm text-gray-900 dark:text-slate-200 focus:border-emerald-500 dark:focus:border-emerald-600 focus:outline-none focus:ring-2 focus:ring-emerald-500/20"
        />
        <span className="text-gray-500 dark:text-slate-400">to</span>
        <input
          type="date"
          value={formatDate(endDate)}
          min={formatDate(minDate)}
          max={formatDate(maxDate)}
          onChange={handleEndChange}
          className="flex h-10 w-full rounded-lg border border-gray-300 dark:border-slate-600 bg-white dark:bg-slate-800 px-3 py-2 text-sm text-gray-900 dark:text-slate-200 focus:border-emerald-500 dark:focus:border-emerald-600 focus:outline-none focus:ring-2 focus:ring-emerald-500/20"
        />
      </div>
    </div>
  )
}
