import type { SimulationResponse } from '../../types/prediction'

type AiInsightPanelProps = {
  simulation: SimulationResponse | null
}

export function AiInsightPanel({ simulation }: AiInsightPanelProps) {
  return (
    <section className="ai-insight">
      <div>
        <h2>AI Insight</h2>
        <p>{simulation?.insight ?? 'High waste generation expected in South Kuta and Airport Area due to increased visitor density and upcoming events.'}</p>
      </div>
      <div className="ai-chip">AI</div>
    </section>
  )
}
