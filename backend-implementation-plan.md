# Backend Implementation Plan - Kuta WasteSense AI

| Field | Value |
| --- | --- |
| Document Version | 1.0 |
| Date | 31 May 2026 |
| Scope | FastAPI backend implementation plan |
| Related Document | `planning-react-fastapi.md` |
| Status | Ready for implementation |

## 1. Objective

Backend FastAPI akan menjadi API layer untuk frontend React/Vite. Backend bertanggung jawab untuk load ML model, validasi input, menjalankan prediksi, menghitung rekomendasi operasional, menyediakan data analytics dari synthetic dataset, dan menyiapkan response JSON yang stabil untuk dashboard.

## 2. Implementation Strategy

Implementasi dilakukan bertahap supaya setiap fase bisa diuji sebelum lanjut ke fase berikutnya.

Urutan prioritas:

1. Setup struktur folder backend.
2. Setup FastAPI app minimal.
3. Implement health check.
4. Implement config dan path resolution.
5. Implement schemas Pydantic.
6. Implement model service untuk load `models/waste_model.pkl`.
7. Implement recommendation service dengan reuse logic dari `src/recommender.py`.
8. Implement prediction endpoint.
9. Implement dashboard summary/trends/zones endpoints.
10. Implement simulator endpoint.
11. Tambahkan CORS untuk frontend Vite.
12. Tambahkan dokumentasi local run.

## 3. Target Backend Folder Structure

```text
backend/
├── README.md
├── requirements.txt
└── app/
    ├── __init__.py
    ├── main.py
    ├── api/
    │   ├── __init__.py
    │   ├── routes_analytics.py
    │   ├── routes_dashboard.py
    │   └── routes_prediction.py
    ├── core/
    │   ├── __init__.py
    │   ├── config.py
    │   └── paths.py
    ├── schemas/
    │   ├── __init__.py
    │   ├── analytics.py
    │   ├── common.py
    │   ├── dashboard.py
    │   └── prediction.py
    ├── services/
    │   ├── __init__.py
    │   ├── analytics_service.py
    │   ├── dashboard_service.py
    │   ├── model_service.py
    │   ├── prediction_service.py
    │   └── recommendation_service.py
    └── utils/
        ├── __init__.py
        └── date_utils.py
```

## 4. Dependencies

Backend `requirements.txt` awal:

```text
fastapi>=0.110.0
uvicorn[standard]>=0.27.0
pydantic>=2.6.0
pydantic-settings>=2.2.0
pandas>=2.0.0
numpy>=1.24.0
scikit-learn>=1.3.0
joblib>=1.3.0
python-dotenv>=1.0.0
```

Catatan:

- `scikit-learn` dan `joblib` dibutuhkan karena model `.pkl` sekarang dibuat dari sklearn pipeline.
- `pandas` dipakai untuk membentuk dataframe input model dan analytics dataset.
- `pydantic-settings` dipakai untuk config berbasis environment.

## 5. Module Responsibilities

### 5.1 `app/main.py`

Tanggung jawab:

- Membuat instance `FastAPI`.
- Register CORS middleware.
- Register semua router.
- Menyediakan endpoint `/health`.

Endpoint minimal:

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

### 5.2 `app/core/config.py`

Tanggung jawab:

- Menyimpan setting aplikasi.
- Membaca env variables.
- Menyediakan default config untuk local development.

Config awal:

```python
APP_NAME = "Kuta WasteSense API"
APP_VERSION = "1.0.0"
APP_ENV = "development"
FRONTEND_ORIGIN = "http://localhost:5173"
```

### 5.3 `app/core/paths.py`

Tanggung jawab:

- Resolve path project root.
- Resolve dataset path.
- Resolve model path.
- Menghindari hardcoded path yang mudah rusak.

Path target:

```text
data/kuta_waste_synthetic_dataset.csv
models/waste_model.pkl
```

### 5.4 `app/schemas/prediction.py`

Tanggung jawab:

- Mendefinisikan request dan response schema untuk prediction/simulation.
- Menjaga kontrak API agar stabil untuk frontend.

Schema utama:

- `PredictionRequest`
- `PredictionResult`
- `RecommendationResult`
- `PredictionResponse`
- `SimulationRequest`
- `SimulationResponse`

### 5.5 `app/services/model_service.py`

Tanggung jawab:

- Load sklearn pipeline dari `models/waste_model.pkl`.
- Cache model agar tidak reload setiap request.
- Membuat input dataframe sesuai `FEATURE_COLS`.
- Menjalankan `model.predict()`.

Public functions:

```python
def get_model():
    ...

def predict_waste(input_data: PredictionRequest) -> float:
    ...
```

Important details:

- Gunakan `FEATURE_COLS` dari `src.utils` agar konsisten dengan training.
- `day_of_week` dihitung dari `prediction_date`.
- `is_weekend` dan `is_holiday` diambil dari `day_type` untuk match behavior prototype saat ini.
- Output prediction dipaksa minimum `0`.

### 5.6 `app/services/recommendation_service.py`

Tanggung jawab:

- Wrapper untuk recommendation logic.
- Reuse `get_recommendations()` dan `generate_executive_summary()` dari `src/recommender.py`.
- Menjaga response shape sesuai API contract.

Public functions:

```python
def build_recommendation(predicted_kg: float) -> RecommendationResult:
    ...

def build_summary(...):
    ...
```

### 5.7 `app/services/prediction_service.py`

Tanggung jawab:

- Orkestrasi prediction flow.
- Memanggil `model_service.predict_waste()`.
- Memanggil `recommendation_service`.
- Menghasilkan `PredictionResponse`.

Public functions:

```python
def run_prediction(request: PredictionRequest) -> PredictionResponse:
    ...
```

### 5.8 `app/services/analytics_service.py`

Tanggung jawab:

- Load synthetic dataset.
- Cache dataframe.
- Menghasilkan aggregate analytics.
- Menghasilkan trend data.

Public functions:

```python
def get_dataset() -> pd.DataFrame:
    ...

def get_analytics_overview() -> dict:
    ...

def get_historical_waste_trends(days: int = 30) -> list[dict]:
    ...
```

### 5.9 `app/services/dashboard_service.py`

Tanggung jawab:

- Menyediakan data dashboard-ready untuk frontend.
- Menggabungkan analytics, mock forecast, dan zone risk data.
- Pada MVP, sebagian data seperti coordinates/forecast boleh static/mock selama jelas.

Public functions:

```python
def get_dashboard_summary() -> dict:
    ...

def get_dashboard_zones() -> dict:
    ...

def get_dashboard_trends(days: int = 30) -> dict:
    ...

def get_dashboard_recommendations() -> dict:
    ...
```

## 6. API Routes Implementation Plan

### 6.1 `routes_prediction.py`

Endpoints:

```http
POST /predict
POST /simulate
```

Implementation notes:

- `/predict` menerima `PredictionRequest` lengkap.
- `/simulate` menerima form yang lebih dekat dengan dashboard UI.
- Untuk MVP, `/simulate` boleh mengisi default `day_type`, `bin_availability`, dan `previous_waste_kg` jika tidak dikirim frontend.
- Keduanya memakai service prediction yang sama.

### 6.2 `routes_dashboard.py`

Endpoints:

```http
GET /dashboard/summary
GET /dashboard/zones
GET /dashboard/trends
GET /dashboard/recommendations
```

Implementation notes:

- Endpoint ini mengembalikan data siap render untuk dashboard.
- Tidak perlu menerima input kompleks di fase awal.
- `days` query param hanya diperlukan untuk `/dashboard/trends`.

### 6.3 `routes_analytics.py`

Endpoints:

```http
GET /analytics/overview
```

Implementation notes:

- Menghasilkan statistik dataset.
- Berguna untuk debug, reports, dan dashboard analytics berikutnya.

## 7. Endpoint Priority

### Priority 1 - Must Have

- `GET /health`
- `POST /predict`
- `POST /simulate`

### Priority 2 - Dashboard Initial Load

- `GET /dashboard/summary`
- `GET /dashboard/recommendations`

### Priority 3 - Visualization Support

- `GET /dashboard/zones`
- `GET /dashboard/trends`
- `GET /analytics/overview`

## 8. Request/Response Shape

API contract detail tetap mengikuti `planning-react-fastapi.md`. Saat implementasi, backend response harus konsisten dengan contract berikut:

Prediction response top-level fields:

```json
{
  "input": {},
  "prediction": {},
  "recommendation": {},
  "summary": ""
}
```

Dashboard response top-level fields:

```json
{
  "predicted_waste_tons": 18.7,
  "risk_zones": {},
  "generated_at": "2026-05-31T10:00:00"
}
```

Error response target:

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid request payload.",
    "details": []
  }
}
```

Catatan: FastAPI default validation error boleh dipakai dulu untuk MVP. Custom error handler bisa ditambahkan setelah endpoint utama stabil.

## 9. Data Handling Plan

### 9.1 Dataset

Source:

```text
data/kuta_waste_synthetic_dataset.csv
```

Rules:

- Load dengan `pd.read_csv(..., parse_dates=["date"])`.
- Cache dataframe di service layer.
- Jika dataset tidak ditemukan, raise error yang jelas.

### 9.2 Model

Source:

```text
models/waste_model.pkl
```

Rules:

- Load dengan `joblib.load()`.
- Cache model di module-level variable atau `functools.lru_cache`.
- Jika model tidak ditemukan, endpoint prediction harus return error `503` atau `500` dengan pesan yang jelas.

### 9.3 Static Zone Coordinates

Dataset saat ini tidak punya latitude/longitude. Untuk endpoint `/dashboard/zones`, gunakan static coordinate map sementara.

Example:

```python
ZONE_COORDINATES = {
    "Beachwalk Area": {"lat": -8.7169, "lng": 115.1686},
    "Main Beach Gate": {"lat": -8.7182, "lng": 115.1681},
    "Food Vendor Area": {"lat": -8.7190, "lng": 115.1679},
    "Parking Area": {"lat": -8.7200, "lng": 115.1695},
    "Hotel Front Area": {"lat": -8.7158, "lng": 115.1690},
    "Event Area": {"lat": -8.7212, "lng": 115.1674},
    "Legian-side Beach Zone": {"lat": -8.7108, "lng": 115.1676},
}
```

## 10. Validation Rules

Prediction request validation:

| Field | Rule |
| --- | --- |
| `zone` | Must exist in `ZONES`. |
| `prediction_date` | Valid date. |
| `day_type` | `Weekday`, `Weekend`, or `Public Holiday`. |
| `weather_condition` | `Sunny`, `Cloudy`, `Rainy`, or `Stormy`. |
| `rainfall_mm` | `0 <= value <= 100`. |
| `event_type` | Must exist in `EVENT_TYPES`. |
| `estimated_visitors` | `0 <= value <= 100000`. |
| `season` | Must exist in `SEASONS`. |
| `bin_availability` | `0 <= value <= 100`. |
| `previous_waste_kg` | `0 <= value <= 20000`. |

## 11. CORS Plan

Allow frontend local dev origin:

```text
http://localhost:5173
```

FastAPI CORS middleware settings:

```python
allow_origins=[settings.frontend_origin]
allow_credentials=True
allow_methods=["*"]
allow_headers=["*"]
```

## 12. Local Run Plan

Backend setup:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r backend/requirements.txt
python -m uvicorn backend.app.main:app --reload --port 8000
```

Run this command from the project root to avoid conflict with the legacy Streamlit `app.py` file.

Health check:

```bash
curl http://localhost:8000/health
```

Open API docs:

```text
http://localhost:8000/docs
```

## 13. Verification Checklist

### 13.1 Backend Startup

- Backend starts without import error.
- `/health` returns `status: ok`.
- `/docs` loads OpenAPI docs.
- CORS allows frontend origin.

### 13.2 Model Prediction

- Backend can load `models/waste_model.pkl`.
- `/predict` returns non-negative predicted waste.
- `/predict` returns risk level.
- `/predict` returns staff, bins, trucks, and schedule.
- Invalid payload returns validation error.

### 13.3 Dashboard Data

- `/dashboard/summary` returns KPI-ready data.
- `/dashboard/zones` returns zone list with risk level and coordinates.
- `/dashboard/trends` returns arrays for charts.
- `/dashboard/recommendations` returns operational plan summary.
- `/analytics/overview` returns dataset stats.

## 14. Suggested Implementation Order By File

Step 1:

- `backend/requirements.txt`
- `backend/README.md`
- `backend/app/__init__.py`
- `backend/app/main.py`

Step 2:

- `backend/app/core/config.py`
- `backend/app/core/paths.py`

Step 3:

- `backend/app/schemas/common.py`
- `backend/app/schemas/prediction.py`
- `backend/app/schemas/dashboard.py`
- `backend/app/schemas/analytics.py`

Step 4:

- `backend/app/services/model_service.py`
- `backend/app/services/recommendation_service.py`
- `backend/app/services/prediction_service.py`

Step 5:

- `backend/app/api/routes_prediction.py`
- register router in `main.py`
- test `/predict` and `/simulate`

Step 6:

- `backend/app/services/analytics_service.py`
- `backend/app/services/dashboard_service.py`

Step 7:

- `backend/app/api/routes_dashboard.py`
- `backend/app/api/routes_analytics.py`
- register routers in `main.py`

Step 8:

- Manual endpoint test through `/docs` or curl.
- Update root `README.md` if backend setup is stable.

## 15. MVP Acceptance Criteria

Backend MVP is considered complete when:

- FastAPI app can run locally.
- API docs are available at `/docs`.
- `/health` works.
- `/predict` uses the existing sklearn model.
- `/simulate` returns prediction, recommendation, and insight.
- Dashboard endpoints return data in frontend-friendly shape.
- Dataset and model paths work from backend runtime.
- No Streamlit dependency is required for backend operation.

## 16. Known Technical Notes

- Existing model was trained with `FEATURE_COLS` from `src/utils.py`; backend must preserve the exact feature names.
- Existing `day_type` in Streamlit is manually selected, not inferred from date. Backend MVP should keep this behavior for compatibility.
- Synthetic dataset contains `day_type`, but model features do not use it directly. Model uses `day_of_week`, `is_weekend`, and `is_holiday`.
- Dashboard image shows 48-hour forecast style, but current dataset is daily. For MVP, 48-hour chart data can be generated as mock/derived data until real hourly data exists.
- Current zone names in dataset differ slightly from PRD zone IDs. Backend should return both `zone_id` and `zone_name` for frontend flexibility.
