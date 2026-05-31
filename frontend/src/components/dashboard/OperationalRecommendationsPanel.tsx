import type { DashboardRecommendations } from '../../types/dashboard'
import type { SimulationResponse } from '../../types/prediction'

type OperationalRecommendationsPanelProps = {
  recommendations: DashboardRecommendations
  simulation: SimulationResponse | null
}

export function OperationalRecommendationsPanel({ recommendations, simulation }: OperationalRecommendationsPanelProps) {
  const staff = simulation?.recommendation.recommended_staff ?? recommendations.sanitation_staff.required
  const bins = simulation?.recommendation.recommended_bins ?? recommendations.additional_bins.required
  const trucks = simulation?.recommendation.recommended_trucks ?? recommendations.collection_trucks.required
  const schedule = simulation?.recommendation.collection_schedule ?? recommendations.collection_schedule.label
  const scheduleDetail = simulation ? 'Simulation result' : recommendations.collection_schedule.time_range

  return (
    <section className="panel side-panel">
      <div className="panel-heading compact"><h2>Operational Recommendations</h2></div>
      <RecommendationRow icon="ST" label="Sanitation Staff" value={staff} unit="Required" delta={recommendations.sanitation_staff.delta_vs_normal} />
      <RecommendationRow icon="BN" label="Additional Bins" value={bins} unit="Units" delta={recommendations.additional_bins.delta_vs_normal} />
      <RecommendationRow icon="TR" label="Collection Trucks" value={trucks} unit="Units" delta={recommendations.collection_trucks.delta_vs_normal} />
      <div className="recommendation-row">
        <span className="recommendation-icon">SC</span>
        <div><strong>Collection Schedule</strong><small>{scheduleDetail}</small></div>
        <b>{schedule}</b>
      </div>
      <button className="primary-button" type="button">View Detailed Plan →</button>
    </section>
  )
}

type RecommendationRowProps = {
  icon: string
  label: string
  value: number
  unit: string
  delta: number
}

function RecommendationRow({ icon, label, value, unit, delta }: RecommendationRowProps) {
  return (
    <div className="recommendation-row">
      <span className="recommendation-icon">{icon}</span>
      <div><strong>{label}</strong><small>{unit}</small></div>
      <b>{value}</b>
      <em>+{delta}</em>
    </div>
  )
}
