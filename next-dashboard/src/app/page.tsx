'use client'

import { useState, useEffect, useRef } from 'react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { fetchIncidentData } from './actions'
import { IncidentData } from '@/types'
import { DataTable } from '@/components/data-table'
import { ThemeToggle } from '@/components/theme-toggle'
import { FilterPanel } from '@/components/filters/filter-panel'
import { ChartSelector, ChartType } from '@/components/charts/chart-selector'
import { ChartDisplay } from '@/components/charts/chart-display'
import { BarChart3, Database, RefreshCw, Activity, MapPin, Users, TrendingUp, AlertCircle } from 'lucide-react'

export default function Home() {
  const [data, setData] = useState<IncidentData[]>([])
  const [filteredData, setFilteredData] = useState<IncidentData[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [activeChart, setActiveChart] = useState<ChartType>('heatmap')
  const chartDisplayRef = useRef<HTMLDivElement>(null)

  const loadData = async () => {
    setLoading(true)
    setError(null)
    try {
      const incidentData = await fetchIncidentData()
      console.log('Loaded incident data:', {
        total: incidentData.length,
        sample: incidentData[0],
        timestamps: incidentData.map(d => d.Timestamp).slice(0, 5)
      })
      setData(incidentData)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load data')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    loadData()
  }, [])

  // Initialize filtered data when data loads
  useEffect(() => {
    setFilteredData(data)
  }, [data])

  // Auto-scroll to chart when selection changes
  useEffect(() => {
    if (chartDisplayRef.current) {
      chartDisplayRef.current.scrollIntoView({ 
        behavior: 'smooth', 
        block: 'start'
      })
    }
  }, [activeChart])

  const stats = {
    totalIncidents: filteredData.length,
    uniqueWildlife: new Set(filteredData.map(d => d['कोणत्या वन्यप्राण्याची नोंद करू इच्छिता:'])).size,
    uniqueTalukas: new Set(filteredData.map(d => d['तालुका:'])).size,
    uniqueVillages: new Set(filteredData.map(d => d['गावाचे नाव:'])).size,
  }

  return (
    <div className="relative min-h-screen w-full overflow-x-hidden bg-gray-50 dark:bg-gradient-to-br dark:from-slate-900 dark:via-slate-800 dark:to-slate-900">
      {/* Animated Background Pattern */}
      <div className="absolute inset-0 bg-grid-pattern opacity-[0.015] dark:opacity-[0.03]"></div>
      <div className="absolute top-0 right-0 w-[500px] h-[500px] bg-emerald-100/40 dark:bg-emerald-500/5 rounded-full blur-3xl -z-10"></div>
      <div className="absolute bottom-0 left-0 w-[400px] h-[400px] bg-teal-100/30 dark:bg-teal-500/5 rounded-full blur-3xl -z-10"></div>
      
      <main className="relative flex flex-1 flex-col gap-8 p-6 lg:gap-10 lg:p-10 max-w-[1600px] mx-auto overflow-visible">
        {/* Enhanced Header */}
<div className="flex items-center justify-between">
          <div className="space-y-2">
            <div className="flex items-center gap-3">
              <div className="p-3 bg-emerald-600 dark:bg-gradient-to-br dark:from-emerald-600 dark:to-teal-700 rounded-2xl shadow-lg shadow-emerald-500/20 dark:shadow-emerald-500/20">
                <span className="text-3xl">🦁</span>
              </div>
              <div>
                <h1 className="text-4xl font-bold tracking-tight text-gray-900 dark:text-white">
                  Wildlife Incident Dashboard
                </h1>
                <p className="text-sm text-gray-600 dark:text-slate-400 font-medium mt-1">
                  Forest Department - Real-time Incident Management System
                </p>
              </div>
            </div>
          </div>
          <div className="flex items-center gap-3">
            <Button 
              onClick={loadData} 
              disabled={loading} 
              variant="outline" 
              size="lg"
              className="shadow-sm hover:shadow-md transition-all duration-300 border-gray-300 dark:border-slate-700 hover:border-emerald-500 dark:hover:border-emerald-600 dark:bg-slate-800 dark:text-slate-200"
            >
              <RefreshCw className={`mr-2 h-4 w-4 ${loading ? 'animate-spin' : ''}`} />
              Refresh
            </Button>
            <ThemeToggle />
          </div>
        </div>

        {/* Error Display with Better Styling */}
        {error && (
          <div className="rounded-xl border-2 border-red-200 dark:border-red-900 bg-gradient-to-r from-red-50 to-rose-50 dark:from-red-950/50 dark:to-rose-950/50 p-5 shadow-lg animate-shake">
            <div className="flex items-center gap-3">
              <AlertCircle className="h-5 w-5 text-red-600 dark:text-red-400" />
              <div>
                <div className="font-semibold text-red-700 dark:text-red-300">Error loading data</div>
                <p className="text-sm mt-1 text-red-600/80 dark:text-red-400/80">{error}</p>
              </div>
            </div>
          </div>
        )}

        {/* Filter Panel - Above KPI Cards */}
        {data.length > 0 && (
          <div className="relative z-40">
            <FilterPanel data={data} onFilterChange={setFilteredData} />
          </div>
        )}

        {/* Enhanced Stats Cards */}
        <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-4 relative z-10">
          <Card className="group relative overflow-hidden border border-gray-200 dark:border-slate-700 bg-white dark:bg-slate-800/50 dark:backdrop-blur-sm shadow-sm hover:shadow-lg transition-all duration-300 hover:border-emerald-500 dark:hover:border-emerald-600">
            <div className="absolute inset-0 bg-emerald-50 dark:bg-emerald-500/5 opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-3 relative z-10">
              <CardTitle className="text-sm font-semibold text-gray-700 dark:text-slate-300">
                Total Incidents
              </CardTitle>
              <div className="h-12 w-12 rounded-xl bg-emerald-600 dark:bg-gradient-to-br dark:from-emerald-600 dark:to-teal-700 flex items-center justify-center shadow-md group-hover:scale-110 transition-transform duration-300">
                <Database className="h-6 w-6 text-white" />
              </div>
            </CardHeader>
            <CardContent className="relative z-10">
              <div className="text-4xl font-bold text-gray-900 dark:text-emerald-400">
                {stats.totalIncidents.toLocaleString()}
              </div>
              <p className="text-xs text-gray-600 dark:text-slate-400 mt-2 flex items-center gap-1">
                <TrendingUp className="h-3 w-3" />
                Wildlife incident reports
              </p>
            </CardContent>
          </Card>

          <Card className="group relative overflow-hidden border border-gray-200 dark:border-slate-700 bg-white dark:bg-slate-800/50 dark:backdrop-blur-sm shadow-sm hover:shadow-lg transition-all duration-300 hover:border-blue-500 dark:hover:border-blue-600">
            <div className="absolute inset-0 bg-blue-50 dark:bg-blue-500/5 opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-3 relative z-10">
              <CardTitle className="text-sm font-semibold text-gray-700 dark:text-slate-300">
                Wildlife Types
              </CardTitle>
              <div className="h-12 w-12 rounded-xl bg-blue-600 dark:bg-gradient-to-br dark:from-blue-600 dark:to-cyan-700 flex items-center justify-center shadow-md group-hover:scale-110 transition-transform duration-300">
                <Activity className="h-6 w-6 text-white" />
              </div>
            </CardHeader>
            <CardContent className="relative z-10">
              <div className="text-4xl font-bold text-gray-900 dark:text-blue-400">
                {stats.uniqueWildlife}
              </div>
              <p className="text-xs text-gray-600 dark:text-slate-400 mt-2 flex items-center gap-1">
                <TrendingUp className="h-3 w-3" />
                Different species reported
              </p>
            </CardContent>
          </Card>

          <Card className="group relative overflow-hidden border border-gray-200 dark:border-slate-700 bg-white dark:bg-slate-800/50 dark:backdrop-blur-sm shadow-sm hover:shadow-lg transition-all duration-300 hover:border-purple-500 dark:hover:border-purple-600">
            <div className="absolute inset-0 bg-purple-50 dark:bg-purple-500/5 opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-3 relative z-10">
              <CardTitle className="text-sm font-semibold text-gray-700 dark:text-slate-300">
                Talukas Covered
              </CardTitle>
              <div className="h-12 w-12 rounded-xl bg-purple-600 dark:bg-gradient-to-br dark:from-purple-600 dark:to-pink-700 flex items-center justify-center shadow-md group-hover:scale-110 transition-transform duration-300">
                <MapPin className="h-6 w-6 text-white" />
              </div>
            </CardHeader>
            <CardContent className="relative z-10">
              <div className="text-4xl font-bold text-gray-900 dark:text-purple-400">
                {stats.uniqueTalukas}
              </div>
              <p className="text-xs text-gray-600 dark:text-slate-400 mt-2 flex items-center gap-1">
                <TrendingUp className="h-3 w-3" />
                Administrative divisions
              </p>
            </CardContent>
          </Card>

          <Card className="group relative overflow-hidden border border-gray-200 dark:border-slate-700 bg-white dark:bg-slate-800/50 dark:backdrop-blur-sm shadow-sm hover:shadow-lg transition-all duration-300 hover:border-orange-500 dark:hover:border-orange-600">
            <div className="absolute inset-0 bg-orange-50 dark:bg-orange-500/5 opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-3 relative z-10">
              <CardTitle className="text-sm font-semibold text-gray-700 dark:text-slate-300">
                Villages
              </CardTitle>
              <div className="h-12 w-12 rounded-xl bg-orange-600 dark:bg-gradient-to-br dark:from-orange-600 dark:to-amber-700 flex items-center justify-center shadow-md group-hover:scale-110 transition-transform duration-300">
                <Users className="h-6 w-6 text-white" />
              </div>
            </CardHeader>
            <CardContent className="relative z-10">
              <div className="text-4xl font-bold text-gray-900 dark:text-orange-400">
                {stats.uniqueVillages}
              </div>
              <p className="text-xs text-gray-600 dark:text-slate-400 mt-2 flex items-center gap-1">
                <TrendingUp className="h-3 w-3" />
                Locations affected
              </p>
            </CardContent>
          </Card>
        </div>

        {/* Enhanced Main Content Tabs */}
        <Tabs defaultValue="overview" className="space-y-6">
          <div className="flex items-center justify-center bg-white dark:bg-slate-800/50 dark:backdrop-blur-sm rounded-xl p-2 border border-gray-200 dark:border-slate-700 shadow-sm">
            <TabsList className="bg-gray-100 dark:bg-slate-700/50 h-12">
              <TabsTrigger 
                value="overview"
                className="data-[state=active]:bg-emerald-600 data-[state=active]:text-white data-[state=active]:shadow-md data-[state=active]:shadow-emerald-500/30 transition-all duration-300 px-6 rounded-lg text-gray-600 dark:text-slate-300 hover:text-gray-900 dark:hover:text-white"
              >
                <Activity className="h-4 w-4 mr-2" />
                Overview
              </TabsTrigger>
              <TabsTrigger 
                value="charts"
                className="data-[state=active]:bg-emerald-600 data-[state=active]:text-white data-[state=active]:shadow-md data-[state=active]:shadow-emerald-500/30 transition-all duration-300 px-6 rounded-lg text-gray-600 dark:text-slate-300 hover:text-gray-900 dark:hover:text-white"
              >
                <BarChart3 className="h-4 w-4 mr-2" />
                Charts
              </TabsTrigger>
              <TabsTrigger 
                value="raw-data"
                className="data-[state=active]:bg-emerald-600 data-[state=active]:text-white data-[state=active]:shadow-md data-[state=active]:shadow-emerald-500/30 transition-all duration-300 px-6 rounded-lg text-gray-600 dark:text-slate-300 hover:text-gray-900 dark:hover:text-white"
              >
                <Database className="h-4 w-4 mr-2" />
                Raw Data
              </TabsTrigger>
            </TabsList>
          </div>

          <TabsContent value="overview" className="space-y-6 mt-0">
            <Card className="border border-gray-200 dark:border-slate-700 bg-white dark:bg-slate-800/50 dark:backdrop-blur-sm shadow-md">
              <CardHeader className="bg-gray-50 dark:bg-slate-800/70 border-b border-gray-200 dark:border-slate-700">
                <CardTitle className="flex items-center gap-3 text-2xl">
                  <div className="p-2 bg-emerald-600 dark:bg-gradient-to-br dark:from-emerald-600 dark:to-teal-700 rounded-lg shadow-md">
                    <Activity className="h-6 w-6 text-white" />
                  </div>
                  <span className="text-gray-900 dark:text-white">
                    Dashboard Overview
                  </span>
                </CardTitle>
                <CardDescription className="text-base mt-2 dark:text-slate-400">
                  Welcome to the Wildlife Incident Management Dashboard. Use the tabs above to explore different views of the data.
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-6 p-8">
                <div className="grid gap-6 md:grid-cols-2">
                  <div className="group space-y-3 p-6 rounded-xl bg-emerald-50 dark:bg-slate-700/50 border border-emerald-200 dark:border-slate-600 hover:shadow-md transition-all duration-300">
                    <h4 className="font-bold flex items-center gap-2 text-gray-900 dark:text-white text-lg">
                      <div className="p-2 bg-emerald-600 dark:bg-gradient-to-br dark:from-emerald-600 dark:to-teal-700 rounded-lg shadow-sm">
                        <Database className="h-5 w-5 text-white" />
                      </div>
                      Data Status
                    </h4>
                    <p className="text-sm text-gray-700 dark:text-slate-300 leading-relaxed">
                      Successfully loaded <span className="font-bold text-emerald-600 dark:text-emerald-400">{data.length.toLocaleString()}</span> incident records from Google Sheets.
                      {filteredData.length < data.length && (
                        <span className="block mt-1 text-emerald-600 dark:text-emerald-400">
                          Showing {filteredData.length.toLocaleString()} filtered records.
                        </span>
                      )}
                    </p>
                  </div>
                  <div className="group space-y-3 p-6 rounded-xl bg-blue-50 dark:bg-slate-700/50 border border-blue-200 dark:border-slate-600 hover:shadow-md transition-all duration-300">
                    <h4 className="font-bold flex items-center gap-2 text-gray-900 dark:text-white text-lg">
                      <div className="p-2 bg-blue-600 dark:bg-gradient-to-br dark:from-blue-600 dark:to-cyan-700 rounded-lg shadow-sm">
                        <Activity className="h-5 w-5 text-white" />
                      </div>
                      Next Steps
                    </h4>
                    <p className="text-sm text-gray-700 dark:text-slate-300 leading-relaxed">
                      Navigate to <span className="font-bold text-blue-600 dark:text-blue-400">Charts</span> to explore visualizations or view <span className="font-bold text-blue-600 dark:text-blue-400">Raw Data</span> for detailed records.
                    </p>
                  </div>
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="charts" className="space-y-6 mt-0">
            {/* Chart Display */}
            <div ref={chartDisplayRef}>
              <ChartDisplay 
                chartType={activeChart} 
                data={filteredData} 
              />
            </div>

            {/* Chart Selector */}
            <ChartSelector 
              activeChart={activeChart} 
              onChartChange={setActiveChart} 
            />
          </TabsContent>

          <TabsContent value="raw-data" className="space-y-6 mt-0">
            <Card className="border border-gray-200 dark:border-slate-700 bg-white dark:bg-slate-800/50 dark:backdrop-blur-sm shadow-md">
              <CardHeader className="bg-gray-50 dark:bg-slate-800/70 border-b border-gray-200 dark:border-slate-700">
                <CardTitle className="flex items-center gap-3 text-2xl">
                  <div className="p-2 bg-emerald-600 dark:bg-gradient-to-br dark:from-emerald-600 dark:to-teal-700 rounded-lg shadow-md">
                    <Database className="h-6 w-6 text-white" />
                  </div>
                  <span className="text-gray-900 dark:text-white">
                    Raw Incident Data
                  </span>
                </CardTitle>
                <CardDescription className="text-base mt-2 dark:text-slate-400">
                  Complete dataset of wildlife incidents with pagination and search capabilities.
                </CardDescription>
              </CardHeader>
              <CardContent className="p-8">
                <DataTable data={filteredData} loading={loading} />
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>
      </main>
    </div>
  )
}
