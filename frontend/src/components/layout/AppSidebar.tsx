const menuItems = [
  ['Dashboard', 'grid'],
  ['Zone Monitoring', 'pin'],
  ['AI Predictions', 'brain'],
  ['Operations', 'truck'],
  ['Reports & Analytics', 'chart'],
  ['Alerts & Notifications', 'bell'],
  ['Data Management', 'database'],
  ['Settings', 'gear'],
]

type AppSidebarProps = {
  isOpen: boolean
  onClose: () => void
}

export function AppSidebar({ isOpen, onClose }: AppSidebarProps) {
  return (
    <>
      <button
        aria-label="Close sidebar"
        className={`sidebar-backdrop ${isOpen ? 'show' : ''}`}
        onClick={onClose}
        type="button"
      />
      <aside className={`sidebar ${isOpen ? 'open' : ''}`}>
        <div className="brand-block">
          <div className="brand-mark">K</div>
          <div>
            <strong>Kuta WasteSense AI</strong>
            <span>AI-Powered Waste Prediction & Operational Readiness</span>
          </div>
          <button className="sidebar-close" type="button" aria-label="Close sidebar" onClick={onClose}>×</button>
        </div>
        <nav className="sidebar-nav" aria-label="Main navigation">
          {menuItems.map(([label, icon], index) => (
            <button className={`nav-item ${index === 0 ? 'active' : ''}`} type="button" key={label} onClick={onClose}>
              <span className="nav-icon">{icon.slice(0, 2).toUpperCase()}</span>
              {label}
              {label === 'Alerts & Notifications' ? <span className="nav-badge">3</span> : null}
            </button>
          ))}
        </nav>
        <div className="sidebar-photo">
          <div className="photo-overlay">
            <strong>2025 Kuta WasteSense AI</strong>
            <span>Prototype with synthetic data</span>
          </div>
        </div>
      </aside>
    </>
  )
}
