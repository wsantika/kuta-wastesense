export type RiskLevel = 'Low' | 'Medium' | 'High'

export type DashboardSummary = {
  predicted_waste_tons: number
  predicted_window_hours: number
  waste_delta_percent: number
  risk_zones: {
    low: number
    medium: number
    high: number
  }
  risk_zone_percentages: {
    low: number
    medium: number
    high: number
  }
  generated_at: string
}

export type DashboardZone = {
  zone_id: string
  zone_name: string
  risk_level: RiskLevel
  predicted_waste_kg: number
  latitude: number
  longitude: number
  color: string
}

export type DashboardZonesResponse = {
  zones: DashboardZone[]
}

export type TrendPoint = {
  hour?: number
  date?: string
  visitors?: number
  rainfall_mm?: number
  impact_score?: number
  waste_tons?: number
}

export type DashboardTrends = {
  visitor_density: TrendPoint[]
  rainfall_forecast: TrendPoint[]
  event_impact: TrendPoint[]
  historical_waste: TrendPoint[]
}

export type DashboardRecommendations = {
  sanitation_staff: {
    required: number
    delta_vs_normal: number
  }
  additional_bins: {
    required: number
    delta_vs_normal: number
  }
  collection_trucks: {
    required: number
    delta_vs_normal: number
  }
  collection_schedule: {
    label: string
    time_range: string
  }
}
