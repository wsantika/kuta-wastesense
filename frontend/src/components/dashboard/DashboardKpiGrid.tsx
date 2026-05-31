import type { DashboardSummary } from '../../types/dashboard'
import { formatNumber } from '../../lib/formatters'

type DashboardKpiGridProps = {
  summary: DashboardSummary
}

export function DashboardKpiGrid({ summary }: DashboardKpiGridProps) {
  return (
    <section className="kpi-grid">
      <article className="kpi-card hero-kpi">
        <div>
          <span>Predicted Waste Volume</span>
          <small>Next {summary.predicted_window_hours} Hours</small>
        </div>
        <strong>{formatNumber(summary.predicted_waste_tons)}<em>tons</em></strong>
        <p>↑ {formatNumber(summary.waste_delta_percent)}% vs previous period</p>
      </article>
      <RiskCard title="Low Risk Zones" count={summary.risk_zones.low} percent={summary.risk_zone_percentages.low} tone="low" />
      <RiskCard title="Medium Risk Zones" count={summary.risk_zones.medium} percent={summary.risk_zone_percentages.medium} tone="medium" />
      <RiskCard title="High Risk Zones" count={summary.risk_zones.high} percent={summary.risk_zone_percentages.high} tone="high" />
    </section>
  )
}

type RiskCardProps = {
  title: string
  count: number
  percent: number
  tone: 'low' | 'medium' | 'high'
}

function RiskCard({ title, count, percent, tone }: RiskCardProps) {
  return (
    <article className={`kpi-card risk-card ${tone}`}>
      <h3>{title}</h3>
      <strong>{count}<em>Zones</em></strong>
      <p>{formatNumber(percent)}% of total area</p>
    </article>
  )
}
