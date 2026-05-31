import type { DashboardTrends, TrendPoint } from '../../types/dashboard'
import { formatCompact, formatNumber } from '../../lib/formatters'
import {
  Area,
  AreaChart,
  CartesianGrid,
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from 'recharts'

type MetricTrendGridProps = {
  trends: DashboardTrends
}

export function MetricTrendGrid({ trends }: MetricTrendGridProps) {
  return (
    <section className="trend-grid">
      <TrendCard title="Visitor Density" value={`${formatCompact(lastValue(trends.visitor_density, 'visitors'))} Visitors`} points={trends.visitor_density} field="visitors" tone="green" chart="area" />
      <TrendCard title="Rainfall Forecast" value={`${formatNumber(lastValue(trends.rainfall_forecast, 'rainfall_mm'))} mm`} points={trends.rainfall_forecast} field="rainfall_mm" tone="blue" chart="line" />
      <TrendCard title="Event Impact" value="High" subvalue="Impact Level" points={trends.event_impact} field="impact_score" tone="red" chart="area" />
      <TrendCard title="Historical Waste Trends" value={`${formatNumber(lastValue(trends.historical_waste, 'waste_tons'))} Tons`} subvalue="Average" points={trends.historical_waste} field="waste_tons" tone="green" chart="line" />
    </section>
  )
}

function lastValue(points: TrendPoint[], field: keyof TrendPoint) {
  const value = points.at(-1)?.[field]
  return typeof value === 'number' ? value : 0
}

type TrendCardProps = {
  title: string
  value: string
  subvalue?: string
  points: TrendPoint[]
  field: keyof TrendPoint
  tone: 'green' | 'blue' | 'red'
  chart: 'area' | 'line'
}

function TrendCard({ title, value, subvalue, points, field, tone, chart }: TrendCardProps) {
  const color = { green: '#16864f', blue: '#2d9cdb', red: '#e85656' }[tone]
  const chartData = points.map((point, index) => ({
    label: point.hour !== undefined ? `${point.hour}h` : point.date?.slice(5) ?? String(index + 1),
    value: typeof point[field] === 'number' ? point[field] : 0,
  }))

  return (
    <article className="trend-card">
      <h3>{title}</h3>
      <strong>{value}</strong>
      {subvalue ? <span>{subvalue}</span> : null}
      <div className="trend-chart">
        <ResponsiveContainer width="100%" height="100%">
          {chart === 'area' ? (
            <AreaChart data={chartData} margin={{ top: 8, right: 4, bottom: 0, left: -18 }}>
              <defs>
                <linearGradient id={`fill-${tone}-${title.replace(/\s+/g, '-')}`} x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor={color} stopOpacity={0.25} />
                  <stop offset="95%" stopColor={color} stopOpacity={0} />
                </linearGradient>
              </defs>
              <CartesianGrid vertical={false} stroke="#edf2ef" />
              <XAxis dataKey="label" tick={{ fontSize: 10 }} tickLine={false} axisLine={false} />
              <YAxis hide />
              <Tooltip contentStyle={{ borderRadius: 12, border: '1px solid #e5ede9' }} />
              <Area type="monotone" dataKey="value" stroke={color} fill={`url(#fill-${tone}-${title.replace(/\s+/g, '-')})`} strokeWidth={2.5} />
            </AreaChart>
          ) : (
            <LineChart data={chartData} margin={{ top: 8, right: 4, bottom: 0, left: -18 }}>
              <CartesianGrid vertical={false} stroke="#edf2ef" />
              <XAxis dataKey="label" tick={{ fontSize: 10 }} tickLine={false} axisLine={false} />
              <YAxis hide />
              <Tooltip contentStyle={{ borderRadius: 12, border: '1px solid #e5ede9' }} />
              <Line type="monotone" dataKey="value" stroke={color} strokeWidth={2.5} dot={false} />
            </LineChart>
          )}
        </ResponsiveContainer>
      </div>
    </article>
  )
}
