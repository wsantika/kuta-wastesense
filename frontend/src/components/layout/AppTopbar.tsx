import { useEffect, useState } from "react";

type AppTopbarProps = {
  apiStatus: "loading" | "connected" | "fallback";
  onOpenSidebar: () => void;
};

export function AppTopbar({ apiStatus, onOpenSidebar }: AppTopbarProps) {
  const [now, setNow] = useState(() => new Date());
  const statusLabel = {
    loading: "Loading API",
    connected: "FastAPI connected",
    fallback: "Using fallback data",
  }[apiStatus];
  const hour = now.getHours();
  const greeting =
    hour < 12 ? "Good Morning" : hour < 18 ? "Good Afternoon" : "Good Evening";
  const formattedDate = new Intl.DateTimeFormat("en-US", {
    weekday: "long",
    day: "2-digit",
    month: "long",
    year: "numeric",
  }).format(now);
  const formattedTime = new Intl.DateTimeFormat("en-US", {
    hour: "2-digit",
    minute: "2-digit",
    second: "2-digit",
  }).format(now);

  useEffect(() => {
    const intervalId = window.setInterval(() => setNow(new Date()), 1000);
    return () => window.clearInterval(intervalId);
  }, []);

  return (
    <header className="topbar">
      <div className="topbar-left">
        <button
          className="menu-button"
          type="button"
          aria-label="Open sidebar"
          onClick={onOpenSidebar}
        >
          ☰
        </button>
        <div>
          <h1>{greeting}, Operator</h1>
          <p>
            {formattedDate} · {formattedTime}
          </p>
        </div>
      </div>
      <div className="topbar-right">
        <div className="weather-pill">
          <span>⛅</span>
          <strong>28°C</strong>
          <small>Partly Cloudy · Kuta Beach</small>
        </div>
        <div className={`api-pill ${apiStatus}`}>{statusLabel}</div>
        <div className="user-pill">
          <div className="avatar">KA</div>
          <div>
            <strong>Kevin Azaky</strong>
            <small>Waste Operations Admin</small>
          </div>
        </div>
      </div>
    </header>
  );
}
