'use client'

import { useState, useEffect } from 'react'
import { Calendar, Leaf, MapPin, RotateCcw } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Card, CardContent } from '@/components/ui/card'
import { DateRangeFilter } from './date-range-filter'
import { MultiSelectFilter } from './multi-select-filter'
import { IncidentData } from '@/types'
import { parseIncidentDate } from '@/utils/date-parser'

interface FilterPanelProps {
  data: IncidentData[]
  onFilterChange: (filtered: IncidentData[]) => void
}

export function FilterPanel({ data, onFilterChange }: FilterPanelProps) {
  // Extract unique values and date range
  const allWildlifeTypes = [...new Set(data.map(d => d['कोणत्या वन्यप्राण्याची नोंद करू इच्छिता:']).filter(Boolean))]
  const allTalukas = [...new Set(data.map(d => d['तालुका:']).filter(Boolean))]
  
  // Parse dates properly using our date parser
  const dates = data
    .map(d => parseIncidentDate(d.Timestamp))
    .filter((d): d is Date => d !== null)
    .sort((a, b) => a.getTime() - b.getTime())
  
  const minDate = dates.length > 0 ? dates[0] : new Date()
  const maxDate = dates.length > 0 ? dates[dates.length - 1] : new Date()

  // Filter states
  const [dateRange, setDateRange] = useState<[Date, Date]>([minDate, maxDate])
  const [selectedWildlife, setSelectedWildlife] = useState<string[]>(allWildlifeTypes)
  const [selectedTalukas, setSelectedTalukas] = useState<string[]>(allTalukas)

  // Apply filters whenever they change
  useEffect(() => {
    const filtered = data.filter(row => {
      // Parse the row date
      const rowDate = parseIncidentDate(row.Timestamp)
      
      // Create end of day for the end date to include all times on that day
      const endOfDay = new Date(dateRange[1])
      endOfDay.setHours(23, 59, 59, 999)
      
      // Start of day for start date
      const startOfDay = new Date(dateRange[0])
      startOfDay.setHours(0, 0, 0, 0)
      
      // Check date match - include rows with valid dates OR if no date range filter is active
      const dateMatch = rowDate === null ? false : (
        rowDate >= startOfDay && rowDate <= endOfDay
      )
      
      const wildlifeMatch = selectedWildlife.includes(row['कोणत्या वन्यप्राण्याची नोंद करू इच्छिता:'])
      const talukaMatch = selectedTalukas.includes(row['तालुका:'])
      
      return dateMatch && wildlifeMatch && talukaMatch
    })
    
    console.log('Filter applied:', {
      dateRange: [dateRange[0].toISOString(), dateRange[1].toISOString()],
      totalData: data.length,
      filteredCount: filtered.length,
      wildlifeSelected: selectedWildlife.length,
      talukasSelected: selectedTalukas.length
    })
    
    onFilterChange(filtered)
  }, [dateRange, selectedWildlife, selectedTalukas, data, onFilterChange])

  const resetFilters = () => {
    setDateRange([minDate, maxDate])
    setSelectedWildlife(allWildlifeTypes)
    setSelectedTalukas(allTalukas)
  }

  const hasActiveFilters = 
    selectedWildlife.length < allWildlifeTypes.length ||
    selectedTalukas.length < allTalukas.length ||
    dateRange[0].getTime() !== minDate.getTime() ||
    dateRange[1].getTime() !== maxDate.getTime()

  return (
    <Card className="border border-gray-200 dark:border-slate-700 bg-white dark:bg-slate-800/50 dark:backdrop-blur-sm shadow-md relative z-50">
      <CardContent className="p-6 relative z-50">
        <div className="flex items-center justify-between mb-6">
          <h3 className="text-lg font-bold text-gray-900 dark:text-white flex items-center gap-2">
            🔎 Filter Data
          </h3>
          {hasActiveFilters && (
            <Button
              variant="outline"
              size="sm"
              onClick={resetFilters}
              className="text-xs"
            >
              <RotateCcw className="h-3 w-3 mr-1" />
              Reset Filters
            </Button>
          )}
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 relative z-50">
          <DateRangeFilter
            minDate={minDate}
            maxDate={maxDate}
            value={dateRange}
            onChange={setDateRange}
          />

          <MultiSelectFilter
            label="Type of Wildlife"
            icon={<Leaf className="h-4 w-4 text-emerald-600 dark:text-emerald-400" />}
            options={allWildlifeTypes}
            value={selectedWildlife}
            onChange={setSelectedWildlife}
            placeholder="Select wildlife types..."
          />

          <MultiSelectFilter
            label="Taluka"
            icon={<MapPin className="h-4 w-4 text-emerald-600 dark:text-emerald-400" />}
            options={allTalukas}
            value={selectedTalukas}
            onChange={setSelectedTalukas}
            placeholder="Select talukas..."
          />
        </div>

        {hasActiveFilters && (
          <div className="mt-4 pt-4 border-t border-gray-200 dark:border-slate-700">
            <div className="flex flex-col gap-2">
              <div className="flex items-center gap-2 text-sm text-gray-600 dark:text-slate-400">
                <span className="font-medium">Active filters:</span>
                {selectedWildlife.length < allWildlifeTypes.length && (
                  <span className="px-2 py-1 rounded-md bg-emerald-100 dark:bg-emerald-900/30 text-emerald-700 dark:text-emerald-300 text-xs">
                    {selectedWildlife.length}/{allWildlifeTypes.length} Wildlife
                  </span>
                )}
                {selectedTalukas.length < allTalukas.length && (
                  <span className="px-2 py-1 rounded-md bg-purple-100 dark:bg-purple-900/30 text-purple-700 dark:text-purple-300 text-xs">
                    {selectedTalukas.length}/{allTalukas.length} Talukas
                  </span>
                )}
                {(dateRange[0].getTime() !== minDate.getTime() || dateRange[1].getTime() !== maxDate.getTime()) && (
                  <span className="px-2 py-1 rounded-md bg-blue-100 dark:bg-blue-900/30 text-blue-700 dark:text-blue-300 text-xs">
                    Custom Date Range
                  </span>
                )}
              </div>
              <div className="text-xs text-gray-500 dark:text-slate-500">
                Data range: {minDate.toLocaleDateString()} to {maxDate.toLocaleDateString()} • 
                Total records: {data.length}
              </div>
            </div>
          </div>
        )}
      </CardContent>
    </Card>
  )
}
