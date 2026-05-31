# Kuta WasteSense AI - React + FastAPI Planning Document

| Field | Value |
| --- | --- |
| Document Version | 1.0 |
| Date | 31 May 2026 |
| Product | Kuta WasteSense AI |
| Scope | Migration plan from Streamlit prototype to React + FastAPI dashboard |
| Frontend | React, TypeScript, Vite |
| Backend | Python, FastAPI |
| Current Status | Planning |

## 1. Executive Summary

Kuta WasteSense AI saat ini berjalan sebagai prototype Streamlit dengan synthetic dataset, model Random Forest Regressor, dan rule-based recommendation engine. Untuk mencapai tampilan dashboard yang lebih polished, interaktif, dan mudah dikembangkan seperti referensi UI, frontend akan dipindahkan ke React + TypeScript + Vite, sedangkan backend tetap menggunakan Python melalui FastAPI.

Pendekatan ini mempertahankan keunggulan Python untuk machine learning dan data processing, sambil memberi fleksibilitas UI yang lebih baik melalui React. Streamlit tidak lagi menjadi frontend utama, tetapi tetap dapat dipertahankan sementara sebagai prototype/reference selama proses migrasi.

## 2. Goals

- Membangun dashboard web modern untuk Kuta WasteSense AI.
- Memisahkan frontend presentation layer dari backend prediction layer.
- Menyediakan API backend yang reusable untuk dashboard, simulator, analytics, dan integrasi masa depan.
- Mempertahankan model ML dan recommendation logic yang sudah ada.
- Menyiapkan struktur project yang scalable untuk multi-page dashboard di fase berikutnya.

## 3. Non-Goals For Initial MVP

- Tidak membangun aplikasi mobile native.
- Tidak melakukan integrasi data real-time DLH/DLHK pada fase awal.
- Tidak mengganti model ML utama kecuali dibutuhkan.
- Tidak membangun authentication kompleks pada fase awal.
- Tidak langsung membuat semua menu sidebar menjadi halaman terpisah.
- Tidak langsung memakai database produksi seperti PostgreSQL.

## 4. Current Project Baseline

Struktur project saat ini:

```text
kuta-wastesense/
├── app.py
├── README.md
├── prd.md
├── requirements.txt
├── data/
│   └── kuta_waste_synthetic_dataset.csv
├── models/
│   └── waste_model.pkl
└── src/
    ├── __init__.py
    ├── generate_dataset.py
    ├── recommender.py
    ├── train_model.py
    └── utils.py
```

Komponen yang akan dipakai ulang:

| Existing File | Usage In New Architecture |
| --- | --- |
| `src/generate_dataset.py` | Tetap digunakan untuk membuat synthetic dataset. |
| `src/train_model.py` | Tetap digunakan untuk training pipeline dan menyimpan model. |
| `src/recommender.py` | Dipakai ulang oleh backend service untuk recommendation output. |
| `src/utils.py` | Dipakai ulang sebagai sumber constants, feature columns, path, dan thresholds. |
| `models/waste_model.pkl` | Diload oleh FastAPI inference service. |
| `data/kuta_waste_synthetic_dataset.csv` | Dipakai backend sebagai data analytics awal. |
| `app.py` | Menjadi reference UI/prototype, bukan frontend final. |

## 5. Target Architecture

```text
Browser
  |
  | HTTP/JSON
  v
React + TypeScript + Vite Frontend
  |
  | REST API
  v
FastAPI Backend
  |
  | Python services
  v
ML Model + Recommendation Engine + Dataset
```

Responsibilities:

| Layer | Responsibility |
| --- | --- |
| Frontend | Render dashboard UI, charts, map, simulator form, state management, API consumption. |
| Backend API | Validate requests, expose REST endpoints, orchestrate prediction/recommendation/analytics. |
| ML Service | Load trained model, transform input, return predicted waste volume. |
| Recommendation Service | Convert prediction result into risk level, staff, bins, trucks, and schedule. |
| Data Service | Read synthetic dataset and generate dashboard metrics/trends. |

## 6. Recommended Tech Stack

### 6.1 Frontend

| Category | Recommendation | Notes |
| --- | --- | --- |
| Build Tool | Vite | Fast dev server and simple config. |
| Framework | React | Component-based dashboard UI. |
| Language | TypeScript | Safer contracts with backend responses. |
| Styling | TailwindCSS | Fast dashboard styling and responsive layout. |
| UI Components | shadcn/ui | Good for cards, buttons, form controls, dialogs, tabs. |
| Charts | Recharts | Simple React charting for line, area, and bar charts. |
| Map | Leaflet or Mapbox | Leaflet is simpler/free for MVP; Mapbox is better for polished satellite map. |
| API Client | Fetch or Axios | Fetch is enough for initial MVP. |
| Server State | TanStack Query | Recommended once API usage grows. Can be skipped initially. |

### 6.2 Backend

| Category | Recommendation | Notes |
| --- | --- | --- |
| Framework | FastAPI | Type-safe API, OpenAPI docs, async-ready. |
| Validation | Pydantic | Request/response schemas. |
| ML Runtime | scikit-learn + joblib | Load existing `.pkl` model. |
| Data Processing | pandas, numpy | Dataset analytics. |
| Storage Initial | CSV | Reuse current synthetic data. |
| Storage Later | SQLite/PostgreSQL | Add when persistence is needed. |
| API Docs | FastAPI OpenAPI | Available at `/docs`. |

## 7. MVP Dashboard Scope

Initial version is a single-page dashboard. Sidebar menu can be displayed visually, but navigation can remain inactive or anchor-based until multi-page implementation.

### 7.1 Dashboard Sections

| Section | Description | Data Source |
| --- | --- | --- |
| Top Bar | Greeting, date, weather summary, user profile placeholder. | Static/mock + API later. |
| Sidebar | Product branding and menu list. | Frontend static config. |
| KPI Cards | Predicted waste volume, low/medium/high risk zones. | `GET /dashboard/summary`. |
| Zone Heatmap | Visual zone risk overview on Kuta Beach. | `GET /dashboard/zones`. |
| Trend Cards | Visitor density, rainfall forecast, event impact, historical waste trends. | `GET /dashboard/trends`. |
| Operational Recommendations | Staff, bins, trucks, collection schedule. | `GET /dashboard/recommendations` or `POST /predict`. |
| Scenario Simulator | Input form for zone/date/weather/rainfall/event/visitors/season. | `POST /simulate`. |
| AI Insight | Plain-language insight based on prediction and risk. | Backend generated summary. |

### 7.2 Initial UI Components

```text
DashboardPage
├── AppSidebar
├── AppTopbar
├── DashboardKpiGrid
│   ├── PredictedWasteCard
│   ├── RiskZoneCard
│   └── RecommendationSummaryCard
├── ZoneHeatmapPanel
├── MetricTrendGrid
│   ├── VisitorDensityChart
│   ├── RainfallForecastChart
│   ├── EventImpactChart
│   └── HistoricalWasteTrendChart
├── OperationalRecommendationsPanel
├── ScenarioSimulatorPanel
└── AiInsightPanel
```

## 8. Proposed Folder Structure

The recommended structure is a monorepo because the frontend and backend belong to the same prototype product.

```text
kuta-wastesense/
├── README.md
├── prd.md
├── planning-react-fastapi.md
├── data/
│   └── kuta_waste_synthetic_dataset.csv
├── models/
│   └── waste_model.pkl
├── src/
│   ├── __init__.py
│   ├── generate_dataset.py
│   ├── recommender.py
│   ├── train_model.py
│   └── utils.py
├── backend/
│   ├── requirements.txt
│   ├── README.md
│   └── app/
│       ├── __init__.py
│       ├── main.py
│       ├── api/
│       │   ├── __init__.py
│       │   ├── routes_dashboard.py
│       │   ├── routes_prediction.py
│       │   └── routes_analytics.py
│       ├── core/
│       │   ├── __init__.py
│       │   ├── config.py
│       │   └── paths.py
│       ├── schemas/
│       │   ├── __init__.py
│       │   ├── common.py
│       │   ├── dashboard.py
│       │   └── prediction.py
│       ├── services/
│       │   ├── __init__.py
│       │   ├── analytics_service.py
│       │   ├── dashboard_service.py
│       │   ├── model_service.py
│       │   └── recommendation_service.py
│       └── utils/
│           ├── __init__.py
│           └── date_utils.py
└── frontend/
    ├── package.json
    ├── index.html
    ├── vite.config.ts
    ├── tsconfig.json
    ├── tailwind.config.ts
    ├── postcss.config.js
    ├── public/
    │   └── assets/
    └── src/
        ├── main.tsx
        ├── App.tsx
        ├── styles/
        │   └── globals.css
        ├── api/
        │   ├── client.ts
        │   ├── dashboard.ts
        │   └── prediction.ts
        ├── components/
        │   ├── layout/
        │   │   ├── AppSidebar.tsx
        │   │   └── AppTopbar.tsx
        │   ├── dashboard/
        │   │   ├── AiInsightPanel.tsx
        │   │   ├── DashboardKpiGrid.tsx
        │   │   ├── MetricTrendGrid.tsx
        │   │   ├── OperationalRecommendationsPanel.tsx
        │   │   ├── ScenarioSimulatorPanel.tsx
        │   │   └── ZoneHeatmapPanel.tsx
        │   └── ui/
        ├── hooks/
        │   ├── useDashboardSummary.ts
        │   └── useSimulation.ts
        ├── lib/
        │   ├── constants.ts
        │   ├── formatters.ts
        │   └── utils.ts
        ├── pages/
        │   └── DashboardPage.tsx
        └── types/
            ├── dashboard.ts
            └── prediction.ts
```

## 9. FastAPI API Contract

Base URL for local development:

```text
http://localhost:8000
```

API response format should be JSON. Dates should use ISO format: `YYYY-MM-DD`.

### 9.1 Health Check

```http
GET /health
```

Response:

```json
{
  "status": "ok",
  "service": "kuta-wastesense-api",
  "version": "1.0.0"
}
```

### 9.2 Dashboard Summary

```http
GET /dashboard/summary
```

Purpose:

Return top-level metrics for KPI cards.

Response:

```json
{
  "predicted_waste_tons": 18.7,
  "predicted_window_hours": 48,
  "waste_delta_percent": 12.4,
  "risk_zones": {
    "low": 4,
    "medium": 3,
    "high": 2
  },
  "risk_zone_percentages": {
    "low": 15.4,
    "medium": 46.2,
    "high": 38.4
  },
  "generated_at": "2026-05-31T10:00:00"
}
```

### 9.3 Dashboard Zones

```http
GET /dashboard/zones
```

Purpose:

Return zone risk data for map/heatmap.

Response:

```json
{
  "zones": [
    {
      "zone_id": "Z-01",
      "zone_name": "Beachwalk Area",
      "risk_level": "Medium",
      "predicted_waste_kg": 1850.5,
      "latitude": -8.7175,
      "longitude": 115.1686,
      "color": "#F59E0B"
    }
  ]
}
```

### 9.4 Dashboard Trends

```http
GET /dashboard/trends?days=30
```

Query params:

| Name | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `days` | integer | No | `30` | Number of historical days to return. |

Response:

```json
{
  "visitor_density": [
    { "hour": 0, "visitors": 16000 },
    { "hour": 12, "visitors": 26000 },
    { "hour": 24, "visitors": 42600 }
  ],
  "rainfall_forecast": [
    { "hour": 0, "rainfall_mm": 12.8 },
    { "hour": 12, "rainfall_mm": 8.2 },
    { "hour": 24, "rainfall_mm": 4.6 }
  ],
  "event_impact": [
    { "hour": 0, "impact_score": 35 },
    { "hour": 24, "impact_score": 75 },
    { "hour": 48, "impact_score": 68 }
  ],
  "historical_waste": [
    { "date": "2024-12-25", "waste_tons": 14.2 },
    { "date": "2024-12-26", "waste_tons": 16.2 }
  ]
}
```

### 9.5 Prediction

```http
POST /predict
```

Purpose:

Run ML prediction for a single scenario and return operational recommendation.

Request body:

```json
{
  "zone": "Beachwalk Area",
  "prediction_date": "2026-05-31",
  "day_type": "Weekend",
  "weather_condition": "Rainy",
  "rainfall_mm": 12.8,
  "event_type": "Beach Festival",
  "estimated_visitors": 45000,
  "season": "Peak Tourist Season",
  "bin_availability": 18,
  "previous_waste_kg": 1200.0
}
```

Validation rules:

| Field | Rule |
| --- | --- |
| `zone` | Must be one of configured zones. |
| `prediction_date` | Must be valid ISO date. |
| `day_type` | `Weekday`, `Weekend`, or `Public Holiday`. |
| `weather_condition` | `Sunny`, `Cloudy`, `Rainy`, or `Stormy`. |
| `rainfall_mm` | Number between `0` and `100`. |
| `event_type` | Must be one of configured event types. |
| `estimated_visitors` | Integer between `0` and `100000`. |
| `season` | Must be one of configured seasons. |
| `bin_availability` | Integer between `0` and `100`. |
| `previous_waste_kg` | Number between `0` and `20000`. |

Response:

```json
{
  "input": {
    "zone": "Beachwalk Area",
    "prediction_date": "2026-05-31",
    "day_type": "Weekend",
    "weather_condition": "Rainy",
    "rainfall_mm": 12.8,
    "event_type": "Beach Festival",
    "estimated_visitors": 45000,
    "season": "Peak Tourist Season",
    "bin_availability": 18,
    "previous_waste_kg": 1200.0
  },
  "prediction": {
    "predicted_waste_kg": 8500.0,
    "predicted_waste_tons": 8.5,
    "risk_level": "High"
  },
  "recommendation": {
    "recommended_staff": 29,
    "recommended_bins": 57,
    "recommended_trucks": 6,
    "collection_schedule": "3x per day (before event, during event, after event)"
  },
  "summary": "Beachwalk Area is predicted to generate high waste volume (8,500 kg) due to high visitor density, rainy weather conditions, and scheduled beach festival activity."
}
```

### 9.6 Scenario Simulation

```http
POST /simulate
```

Purpose:

Run scenario simulation from dashboard form. In MVP this can behave similarly to `/predict`, but the endpoint is separated so it can later support multi-scenario comparisons.

Request body:

```json
{
  "zone": "Beachwalk Area",
  "prediction_date": "2026-05-31",
  "weather_condition": "Cloudy",
  "rainfall_mm": 12.8,
  "holiday_status": true,
  "event_type": "Beach Festival",
  "estimated_visitors": 45000,
  "season": "Peak Tourist Season"
}
```

Response:

```json
{
  "scenario_id": "sim_20260531_beachwalk_area",
  "prediction": {
    "predicted_waste_kg": 8500.0,
    "predicted_waste_tons": 8.5,
    "risk_level": "High"
  },
  "recommendation": {
    "recommended_staff": 29,
    "recommended_bins": 57,
    "recommended_trucks": 6,
    "collection_schedule": "3x per day (before event, during event, after event)"
  },
  "insight": "High waste generation is expected in Beachwalk Area due to increased visitor density and upcoming event activity."
}
```

### 9.7 Operational Recommendations

```http
GET /dashboard/recommendations
```

Purpose:

Return default operational recommendation panel for dashboard load.

Response:

```json
{
  "sanitation_staff": {
    "required": 64,
    "delta_vs_normal": 12
  },
  "additional_bins": {
    "required": 48,
    "delta_vs_normal": 15
  },
  "collection_trucks": {
    "required": 8,
    "delta_vs_normal": 2
  },
  "collection_schedule": {
    "label": "Every 2 Hours",
    "time_range": "06:00 AM - 10:00 PM"
  }
}
```

### 9.8 Analytics Overview

```http
GET /analytics/overview
```

Purpose:

Return aggregate analytics from synthetic dataset.

Response:

```json
{
  "total_records": 2555,
  "date_range": {
    "start": "2024-01-01",
    "end": "2024-12-30"
  },
  "zones_count": 7,
  "average_waste_kg": 980.5,
  "max_waste_kg": 5200.3,
  "top_risk_zones": [
    {
      "zone": "Event Area",
      "average_waste_kg": 1450.5
    },
    {
      "zone": "Beachwalk Area",
      "average_waste_kg": 1320.7
    }
  ]
}
```

### 9.9 Error Response Format

All backend errors should use a consistent response format.

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid request payload.",
    "details": [
      {
        "field": "estimated_visitors",
        "message": "Value must be between 0 and 100000."
      }
    ]
  }
}
```

Common error codes:

| HTTP Status | Code | Description |
| --- | --- | --- |
| `400` | `BAD_REQUEST` | Request is malformed. |
| `422` | `VALIDATION_ERROR` | Request body/query failed validation. |
| `404` | `NOT_FOUND` | Resource does not exist. |
| `500` | `INTERNAL_ERROR` | Unexpected backend error. |
| `503` | `MODEL_UNAVAILABLE` | ML model cannot be loaded or used. |

## 10. Backend Schema Draft

### 10.1 PredictionRequest

```python
class PredictionRequest(BaseModel):
    zone: str
    prediction_date: date
    day_type: Literal["Weekday", "Weekend", "Public Holiday"]
    weather_condition: Literal["Sunny", "Cloudy", "Rainy", "Stormy"]
    rainfall_mm: float = Field(ge=0, le=100)
    event_type: str
    estimated_visitors: int = Field(ge=0, le=100000)
    season: Literal["Dry Season", "Wet Season", "Peak Tourist Season"]
    bin_availability: int = Field(ge=0, le=100)
    previous_waste_kg: float = Field(ge=0, le=20000)
```

### 10.2 PredictionResponse

```python
class PredictionResponse(BaseModel):
    input: PredictionRequest
    prediction: PredictionResult
    recommendation: RecommendationResult
    summary: str
```

### 10.3 RecommendationResult

```python
class RecommendationResult(BaseModel):
    recommended_staff: int
    recommended_bins: int
    recommended_trucks: int
    collection_schedule: str
```

## 11. Frontend Type Draft

```ts
export type RiskLevel = "Low" | "Medium" | "High";

export type PredictionRequest = {
  zone: string;
  predictionDate: string;
  dayType: "Weekday" | "Weekend" | "Public Holiday";
  weatherCondition: "Sunny" | "Cloudy" | "Rainy" | "Stormy";
  rainfallMm: number;
  eventType: string;
  estimatedVisitors: number;
  season: "Dry Season" | "Wet Season" | "Peak Tourist Season";
  binAvailability: number;
  previousWasteKg: number;
};

export type PredictionResponse = {
  input: PredictionRequest;
  prediction: {
    predictedWasteKg: number;
    predictedWasteTons: number;
    riskLevel: RiskLevel;
  };
  recommendation: {
    recommendedStaff: number;
    recommendedBins: number;
    recommendedTrucks: number;
    collectionSchedule: string;
  };
  summary: string;
};
```

Note: Backend JSON can use snake_case. Frontend can either consume snake_case directly or map to camelCase in the API client layer. Recommended approach: keep backend snake_case, convert to camelCase in frontend API functions if needed.

## 12. Data And Model Flow

### 12.1 Prediction Flow

```text
User fills scenario form
  -> React validates basic required fields
  -> POST /predict or POST /simulate
  -> FastAPI validates payload with Pydantic
  -> Backend transforms payload into model feature dataframe
  -> joblib model predicts waste_volume_kg
  -> recommendation service calculates risk/resources
  -> backend returns JSON
  -> React updates cards, recommendation panel, and AI insight
```

### 12.2 Dashboard Load Flow

```text
Dashboard page mounts
  -> GET /dashboard/summary
  -> GET /dashboard/zones
  -> GET /dashboard/trends
  -> GET /dashboard/recommendations
  -> React renders KPI cards, heatmap, charts, and recommendation panel
```

## 13. Migration Plan

### Phase 1 - Planning And Contract

- Finalize this planning document.
- Decide UI library and map library.
- Confirm API contract.
- Confirm monorepo structure.

### Phase 2 - Backend Foundation

- Create `backend/` folder.
- Set up FastAPI app.
- Add CORS for Vite dev server.
- Implement `/health`.
- Implement model loading service.
- Implement prediction endpoint using existing model and recommender.

### Phase 3 - Dashboard API

- Implement summary API from synthetic dataset.
- Implement zones API with mock coordinates and risk levels.
- Implement trends API from dataset and mock forecast where needed.
- Implement recommendations API.

### Phase 4 - Frontend Foundation

- Create Vite React TypeScript app under `frontend/`.
- Add TailwindCSS.
- Add UI component setup.
- Create dashboard layout with sidebar and topbar.
- Create static first version matching target dashboard direction.

### Phase 5 - API Integration

- Add frontend API client.
- Connect dashboard summary cards.
- Connect chart data.
- Connect simulator form to `/simulate`.
- Connect recommendations panel.

### Phase 6 - Visual Refinement

- Improve spacing, colors, typography, and responsive behavior.
- Add map/heatmap implementation.
- Add loading and error states.
- Add empty states for API failures.

### Phase 7 - Stabilization

- Add backend tests for prediction and recommendation services.
- Add basic frontend component tests if needed.
- Update README with setup instructions.
- Prepare demo run instructions.

## 14. Environment And Commands

### 14.1 Backend Local Development

Expected commands after backend setup:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r backend/requirements.txt
python -m uvicorn backend.app.main:app --reload --port 8000
```

Run the backend command from the project root to avoid conflict with the legacy Streamlit `app.py` file.

### 14.2 Frontend Local Development

Expected commands after frontend setup:

```bash
cd frontend
npm install
npm run dev
```

Frontend dev server default:

```text
http://localhost:5173
```

Backend dev server default:

```text
http://localhost:8000
```

## 15. Configuration

Backend `.env` draft:

```text
APP_NAME=Kuta WasteSense API
APP_ENV=development
API_VERSION=1.0.0
FRONTEND_ORIGIN=http://localhost:5173
DATASET_PATH=../data/kuta_waste_synthetic_dataset.csv
MODEL_PATH=../models/waste_model.pkl
```

Frontend `.env` draft:

```text
VITE_API_BASE_URL=http://localhost:8000
```

## 16. Testing Strategy

### 16.1 Backend

- Test `/health` returns status ok.
- Test `/predict` with valid scenario returns prediction and recommendation.
- Test `/predict` rejects invalid values.
- Test recommendation thresholds:
  - `< 1000 kg` returns `Low`.
  - `1000-3000 kg` returns `Medium`.
  - `> 3000 kg` returns `High`.
- Test dataset analytics endpoints return expected shape.

### 16.2 Frontend

- Test dashboard renders without API errors using mocked data.
- Test scenario form validation.
- Test simulator submit updates prediction UI.
- Test responsive layout for desktop and mobile widths.

## 17. Risks And Mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Synthetic data may not represent real operation | Medium | Keep disclaimer visible and document assumptions. |
| UI scope can grow too large | High | Start with one-page dashboard only. |
| Map/heatmap implementation may take time | Medium | Start with mock zone overlay or simplified Leaflet markers. |
| Model input mismatch between frontend and backend | High | Define Pydantic schema and shared frontend types. |
| Backend cannot load model due to path/runtime issue | Medium | Centralize paths and add `/health` model status later. |
| Dashboard API requires data not present in CSV | Medium | Use mock/derived data for MVP and mark fields clearly. |

## 18. Future Expansion

- Split dashboard into multiple pages:
  - Dashboard
  - Zone Monitoring
  - AI Predictions
  - Operations
  - Reports & Analytics
  - Alerts & Notifications
  - Data Management
  - Settings
- Add user authentication and role-based access.
- Add persistent database.
- Add official data ingestion pipeline.
- Add export PDF/CSV for reports.
- Add real weather API integration.
- Add better geospatial risk heatmap.
- Add model monitoring and model versioning.

## 19. Open Decisions

| Decision | Options | Recommendation |
| --- | --- | --- |
| UI component library | shadcn/ui, Mantine, custom Tailwind | shadcn/ui for polished dashboard components. |
| Map provider | Leaflet, Mapbox | Leaflet for MVP; Mapbox if satellite/polished map is required. |
| API state library | Fetch only, Axios, TanStack Query | Fetch initially; TanStack Query when calls grow. |
| Storage | CSV, SQLite, PostgreSQL | CSV for MVP; SQLite if persistence is needed. |
| Streamlit retention | Delete, archive, keep | Keep temporarily as prototype reference. |

## 20. Definition Of Done For MVP

- FastAPI backend runs locally at `localhost:8000`.
- React/Vite frontend runs locally at `localhost:5173`.
- Dashboard single page renders main layout similar to target reference.
- Dashboard loads summary, zones, trends, and recommendations from API.
- Scenario simulator calls backend and updates prediction result.
- Existing model `.pkl` is used for prediction.
- Existing recommendation rules are reused.
- README contains updated setup instructions.
- Synthetic data disclaimer remains visible in UI or documentation.
