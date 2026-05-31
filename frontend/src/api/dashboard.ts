import { apiGet } from './client'
import type {
  DashboardRecommendations,
  DashboardSummary,
  DashboardTrends,
  DashboardZonesResponse,
} from '../types/dashboard'

export function getDashboardSummary() {
  return apiGet<DashboardSummary>('/dashboard/summary')
}

export function getDashboardZones() {
  return apiGet<DashboardZonesResponse>('/dashboard/zones')
}

export function getDashboardTrends() {
  return apiGet<DashboardTrends>('/dashboard/trends')
}

export function getDashboardRecommendations() {
  return apiGet<DashboardRecommendations>('/dashboard/recommendations')
}
