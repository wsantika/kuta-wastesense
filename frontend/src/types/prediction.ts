import type { RiskLevel } from './dashboard'

export type PredictionRequest = {
  zone: string
  prediction_date: string
  day_type: 'Weekday' | 'Weekend' | 'Public Holiday'
  weather_condition: 'Sunny' | 'Cloudy' | 'Rainy' | 'Stormy'
  rainfall_mm: number
  event_type: string
  estimated_visitors: number
  season: 'Dry Season' | 'Wet Season' | 'Peak Tourist Season'
  bin_availability: number
  previous_waste_kg: number
}

export type SimulationRequest = {
  zone: string
  prediction_date: string
  weather_condition: 'Sunny' | 'Cloudy' | 'Rainy' | 'Stormy'
  rainfall_mm: number
  holiday_status: boolean
  event_type: string
  estimated_visitors: number
  season: 'Dry Season' | 'Wet Season' | 'Peak Tourist Season'
  bin_availability?: number
  previous_waste_kg?: number
}

export type PredictionResult = {
  predicted_waste_kg: number
  predicted_waste_tons: number
  risk_level: RiskLevel
}

export type RecommendationResult = {
  recommended_staff: number
  recommended_bins: number
  recommended_trucks: number
  collection_schedule: string
}

export type SimulationResponse = {
  scenario_id: string
  prediction: PredictionResult
  recommendation: RecommendationResult
  insight: string
}
