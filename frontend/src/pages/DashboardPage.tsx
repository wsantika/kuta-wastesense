import { useEffect, useState } from 'react'
import {
  getDashboardRecommendations,
  getDashboardSummary,
  getDashboardTrends,
  getDashboardZones,
} from '../api/dashboard'
import { runSimulation } from '../api/prediction'
import { AppSidebar } from '../components/layout/AppSidebar'
import { AppTopbar } from '../components/layout/AppTopbar'
import { AiInsightPanel } from '../components/dashboard/AiInsightPanel'
import { DashboardKpiGrid } from '../components/dashboard/DashboardKpiGrid'
import { MetricTrendGrid } from '../components/dashboard/MetricTrendGrid'
import { OperationalRecommendationsPanel } from '../components/dashboard/OperationalRecommendationsPanel'
import { ScenarioSimulatorPanel } from '../components/dashboard/ScenarioSimulatorPanel'
import { ZoneHeatmapPanel } from '../components/dashboard/ZoneHeatmapPanel'
import type {
  DashboardRecommendations,
  DashboardSummary,
  DashboardTrends,
  DashboardZone,
} from '../types/dashboard'
import type { SimulationRequest, SimulationResponse } from '../types/prediction'

const fallbackSummary: DashboardSummary = {
  predicted_waste_tons: 18.7,
  predicted_window_hours: 48,
  waste_delta_percent: 12.4,
  risk_zones: { low: 4, medium: 3, high: 2 },
  risk_zone_percentages: { low: 15.4, medium: 46.2, high: 38.4 },
  generated_at: new Date().toISOString(),
}

const fallbackZones: DashboardZone[] = [
  { zone_id: 'Z-01', zone_name: 'Legian-side Beach Zone', risk_level: 'Low', predicted_waste_kg: 720, latitude: -8.7108, longitude: 115.1676, color: '#22C55E' },
  { zone_id: 'Z-02', zone_name: 'Main Beach Gate', risk_level: 'Medium', predicted_waste_kg: 1850, latitude: -8.7182, longitude: 115.1681, color: '#F59E0B' },
  { zone_id: 'Z-03', zone_name: 'Beachwalk Area', risk_level: 'Medium', predicted_waste_kg: 2240, latitude: -8.7169, longitude: 115.1686, color: '#F59E0B' },
  { zone_id: 'Z-04', zone_name: 'Food Vendor Area', risk_level: 'High', predicted_waste_kg: 3250, latitude: -8.7190, longitude: 115.1679, color: '#EF4444' },
  { zone_id: 'Z-05', zone_name: 'Event Area', risk_level: 'High', predicted_waste_kg: 4100, latitude: -8.7212, longitude: 115.1674, color: '#EF4444' },
  { zone_id: 'Z-06', zone_name: 'Parking Area', risk_level: 'Low', predicted_waste_kg: 680, latitude: -8.7200, longitude: 115.1695, color: '#22C55E' },
]

const fallbackTrends: DashboardTrends = {
  visitor_density: [
    { hour: 0, visitors: 16000 },
    { hour: 12, visitors: 22000 },
    { hour: 24, visitors: 42600 },
    { hour: 36, visitors: 31000 },
    { hour: 48, visitors: 35000 },
  ],
  rainfall_forecast: [
    { hour: 0, rainfall_mm: 12.8 },
    { hour: 12, rainfall_mm: 8.2 },
    { hour: 24, rainfall_mm: 4.6 },
    { hour: 36, rainfall_mm: 10.3 },
    { hour: 48, rainfall_mm: 7.4 },
  ],
  event_impact: [
    { hour: 0, impact_score: 35 },
    { hour: 12, impact_score: 52 },
    { hour: 24, impact_score: 75 },
    { hour: 36, impact_score: 68 },
    { hour: 48, impact_score: 59 },
  ],
  historical_waste: [
    { date: '2024-12-26', waste_tons: 14.2 },
    { date: '2024-12-27', waste_tons: 16.2 },
    { date: '2024-12-28', waste_tons: 12.9 },
    { date: '2024-12-29', waste_tons: 20.1 },
    { date: '2024-12-30', waste_tons: 16.7 },
  ],
}

const fallbackRecommendations: DashboardRecommendations = {
  sanitation_staff: { required: 64, delta_vs_normal: 12 },
  additional_bins: { required: 48, delta_vs_normal: 15 },
  collection_trucks: { required: 8, delta_vs_normal: 2 },
  collection_schedule: { label: 'Every 2 Hours', time_range: '06:00 AM - 10:00 PM' },
}

export function DashboardPage() {
  const [summary, setSummary] = useState(fallbackSummary)
  const [zones, setZones] = useState(fallbackZones)
  const [trends, setTrends] = useState(fallbackTrends)
  const [recommendations, setRecommendations] = useState(fallbackRecommendations)
  const [simulation, setSimulation] = useState<SimulationResponse | null>(null)
  const [apiStatus, setApiStatus] = useState<'loading' | 'connected' | 'fallback'>('loading')
  const [apiMessage, setApiMessage] = useState('Connecting to FastAPI backend...')
  const [isSidebarOpen, setIsSidebarOpen] = useState(false)

  useEffect(() => {
    let cancelled = false

    async function loadDashboard() {
      try {
        const [summaryData, zonesData, trendsData, recommendationsData] = await Promise.all([
          getDashboardSummary(),
          getDashboardZones(),
          getDashboardTrends(),
          getDashboardRecommendations(),
        ])

        if (cancelled) return
        setSummary(summaryData)
        setZones(zonesData.zones)
        setTrends(trendsData)
        setRecommendations(recommendationsData)
        setApiStatus('connected')
        setApiMessage('Live backend data loaded successfully.')
      } catch (error) {
        if (!cancelled) {
          setApiStatus('fallback')
          setApiMessage(error instanceof Error ? error.message : 'Backend unavailable. Showing fallback demo data.')
        }
      }
    }

    loadDashboard()

    return () => {
      cancelled = true
    }
  }, [])

  async function handleRunSimulation(payload: SimulationRequest) {
    const result = await runSimulation(payload)
    setSimulation(result)
  }

  return (
    <div className="app-shell">
      <AppSidebar isOpen={isSidebarOpen} onClose={() => setIsSidebarOpen(false)} />
      <main className="dashboard-main">
        <AppTopbar apiStatus={apiStatus} onOpenSidebar={() => setIsSidebarOpen(true)} />
        <div className="dashboard-content">
          <div className={`status-banner ${apiStatus}`}>
            <strong>{apiStatus === 'connected' ? 'Live mode' : apiStatus === 'loading' ? 'Loading' : 'Fallback mode'}</strong>
            <span>{apiMessage}</span>
          </div>
          <section className="main-grid">
            <div className="main-column">
              <DashboardKpiGrid summary={summary} />
              <ZoneHeatmapPanel zones={zones} />
              <MetricTrendGrid trends={trends} />
              <AiInsightPanel simulation={simulation} />
            </div>
            <aside className="side-column">
              <OperationalRecommendationsPanel recommendations={recommendations} simulation={simulation} />
              {simulation ? <SimulationResultPanel simulation={simulation} /> : null}
              <ScenarioSimulatorPanel onSubmit={handleRunSimulation} />
            </aside>
          </section>
        </div>
      </main>
    </div>
  )
}

function SimulationResultPanel({ simulation }: { simulation: SimulationResponse }) {
  return (
    <section className={`panel simulation-result ${simulation.prediction.risk_level.toLowerCase()}`}>
      <div className="panel-heading compact"><h2>Latest Simulation Result</h2></div>
      <div className="simulation-metric">
        <span>Predicted Waste</span>
        <strong>{simulation.prediction.predicted_waste_tons.toFixed(2)} tons</strong>
      </div>
      <div className="simulation-result-grid">
        <div><small>Risk</small><b>{simulation.prediction.risk_level}</b></div>
        <div><small>Staff</small><b>{simulation.recommendation.recommended_staff}</b></div>
        <div><small>Bins</small><b>{simulation.recommendation.recommended_bins}</b></div>
        <div><small>Trucks</small><b>{simulation.recommendation.recommended_trucks}</b></div>
      </div>
      <p>{simulation.recommendation.collection_schedule}</p>
    </section>
  )
}
