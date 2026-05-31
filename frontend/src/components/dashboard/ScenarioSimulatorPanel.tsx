import { useState } from 'react'
import type { FormEvent } from 'react'
import { EVENT_TYPES, SEASONS, WEATHER_CONDITIONS, ZONES } from '../../lib/constants'
import type { SimulationRequest } from '../../types/prediction'

type ScenarioSimulatorPanelProps = {
  onSubmit: (payload: SimulationRequest) => Promise<void>
}

export function ScenarioSimulatorPanel({ onSubmit }: ScenarioSimulatorPanelProps) {
  const [form, setForm] = useState<SimulationRequest>({
    zone: 'Beachwalk Area',
    prediction_date: '2026-05-31',
    weather_condition: 'Cloudy',
    rainfall_mm: 12.8,
    holiday_status: true,
    event_type: 'Beach Festival',
    estimated_visitors: 45000,
    season: 'Peak Tourist Season',
    bin_availability: 18,
    previous_waste_kg: 500,
  })
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [error, setError] = useState<string | null>(null)

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    setIsSubmitting(true)
    setError(null)
    try {
      await onSubmit(form)
    } catch {
      setError('Simulation failed. Make sure the FastAPI backend is running.')
    } finally {
      setIsSubmitting(false)
    }
  }

  return (
    <section className="panel simulator-panel">
      <div className="panel-heading compact"><h2>Scenario Simulator</h2></div>
      <form className="simulator-form" onSubmit={handleSubmit}>
        <label>Zone<select value={form.zone} onChange={(event) => setForm({ ...form, zone: event.target.value })}>{ZONES.map((zone) => <option key={zone}>{zone}</option>)}</select></label>
        <label>Date<input type="date" value={form.prediction_date} onChange={(event) => setForm({ ...form, prediction_date: event.target.value })} /></label>
        <label>Weather<select value={form.weather_condition} onChange={(event) => setForm({ ...form, weather_condition: event.target.value as SimulationRequest['weather_condition'] })}>{WEATHER_CONDITIONS.map((weather) => <option key={weather}>{weather}</option>)}</select></label>
        <label>Rainfall (mm)<input type="number" min="0" max="100" value={form.rainfall_mm} onChange={(event) => setForm({ ...form, rainfall_mm: Number(event.target.value) })} /></label>
        <label>Holiday Status<select value={form.holiday_status ? 'yes' : 'no'} onChange={(event) => setForm({ ...form, holiday_status: event.target.value === 'yes' })}><option value="yes">Yes</option><option value="no">No</option></select></label>
        <label>Event Type<select value={form.event_type} onChange={(event) => setForm({ ...form, event_type: event.target.value })}>{EVENT_TYPES.map((eventType) => <option key={eventType}>{eventType}</option>)}</select></label>
        <label>Estimated Visitors<input type="number" min="0" value={form.estimated_visitors} onChange={(event) => setForm({ ...form, estimated_visitors: Number(event.target.value) })} /></label>
        <label>Season<select value={form.season} onChange={(event) => setForm({ ...form, season: event.target.value as SimulationRequest['season'] })}>{SEASONS.map((season) => <option key={season}>{season}</option>)}</select></label>
        {error ? <p className="form-error">{error}</p> : null}
        <button className="primary-button wide" type="submit" disabled={isSubmitting}>{isSubmitting ? 'Running...' : 'Run Simulation ▶'}</button>
      </form>
    </section>
  )
}
