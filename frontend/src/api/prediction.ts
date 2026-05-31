import { apiPost } from './client'
import type { SimulationRequest, SimulationResponse } from '../types/prediction'

export function runSimulation(payload: SimulationRequest) {
  return apiPost<SimulationResponse, SimulationRequest>('/simulate', payload)
}
