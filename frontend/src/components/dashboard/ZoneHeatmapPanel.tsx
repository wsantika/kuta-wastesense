import { CircleMarker, MapContainer, Popup, TileLayer } from 'react-leaflet'
import type { DashboardZone } from '../../types/dashboard'
import { formatNumber } from '../../lib/formatters'

type ZoneHeatmapPanelProps = {
  zones: DashboardZone[]
}

export function ZoneHeatmapPanel({ zones }: ZoneHeatmapPanelProps) {
  const center: [number, number] = [-8.7172, 115.1684]

  return (
    <section className="panel heatmap-panel">
      <div className="panel-heading">
        <h2>Kuta Beach Zone Heatmap</h2>
        <div className="risk-legend"><span /> Low <span /> Medium <span /> High</div>
      </div>
      <div className="leaflet-shell">
        <MapContainer center={center} zoom={15} scrollWheelZoom={false} className="leaflet-map">
          <TileLayer
            attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          />
          {zones.map((zone) => (
            <CircleMarker
              center={[zone.latitude, zone.longitude]}
              key={zone.zone_id}
              pathOptions={{ color: zone.color, fillColor: zone.color, fillOpacity: 0.55, weight: 2 }}
              radius={riskRadius(zone.risk_level)}
            >
              <Popup>
                <strong>{zone.zone_name}</strong>
                <br />
                Risk: {zone.risk_level}
                <br />
                Predicted: {formatNumber(zone.predicted_waste_kg, 0)} kg
              </Popup>
            </CircleMarker>
          ))}
        </MapContainer>
        <div className="zone-strip">
          {zones.map((zone) => (
            <div className="zone-chip" key={zone.zone_id} style={{ borderColor: zone.color }}>
              <span style={{ background: zone.color }} />
              <strong>{zone.zone_id}</strong>
              <small>{zone.zone_name}</small>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}

function riskRadius(riskLevel: DashboardZone['risk_level']) {
  if (riskLevel === 'High') return 22
  if (riskLevel === 'Medium') return 17
  return 12
}
