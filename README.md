# ♻️ Kuta WasteSense AI

> **From Reactive Cleanup to Predictive Waste Planning**
>
> 🏗️ _MVP Prototype — Synthetic Data_

Kuta WasteSense AI is an AI-powered waste volume prediction and operational readiness dashboard for **Kuta Beach, Bali**. It predicts daily waste volume per zone using historical waste patterns, weather conditions, holidays, events, visitor estimates, and zone characteristics, then recommends sanitation staff, additional bins, collection trucks, and optimized collection schedules.

---

## 📁 Project Structure

```
kuta-wastesense-ai/
├── app.py                                  # Streamlit dashboard
├── requirements.txt                        # Python dependencies
├── README.md
├── data/
│   └── kuta_waste_synthetic_dataset.csv    # Generated synthetic dataset
├── models/
│   └── waste_model.pkl                     # Trained Random Forest model
└── src/
    ├── __init__.py
    ├── generate_dataset.py                 # Synthetic data generator
    ├── train_model.py                      # ML model training script
    ├── recommender.py                      # Rule-based recommendation engine
    └── utils.py                            # Constants & helpers
```

---

Recommended Demo: Streamlit MVP Prototype <br>
Advanced/Experimental: React + FastAPI Dashboard

---

## ⚙️ Installation

```bash
# 1. Clone or navigate to the project folder
cd kuta-wastesense-ai

# 2. (Optional) Create a virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS / Linux

# 3. Install dependencies
pip install -r requirements.txt
```

---

## 🚀 Usage

### Option A — New React + FastAPI Dashboard

Run the FastAPI backend:

```bash
pip install -r backend/requirements.txt
python -m uvicorn backend.app.main:app --reload --port 8000
```

Run the command above from the project root. Do not target the top-level `app` module from the root folder because it resolves to the legacy Streamlit `app.py` file.

Open the backend API docs at `http://localhost:8000/docs`.

Run the React/Vite frontend in a separate terminal:

```bash
cd frontend
npm install
npm run dev
```

Open the frontend URL shown in the terminal, usually `http://localhost:5173`.

### Option B — Legacy Streamlit Prototype

### Step 1 — Generate Synthetic Dataset

```bash
python src/generate_dataset.py
```

This creates `data/kuta_waste_synthetic_dataset.csv` with ~2,555 rows (365 days x 7 zones).

### Step 2 — Train the ML Model

```bash
python src/train_model.py
```

Trains a **Random Forest Regressor** (and prints Linear Regression baseline metrics). The trained pipeline is saved to `models/waste_model.pkl`.

### Step 3 — Run the Dashboard

```bash
streamlit run app.py
```

Open the URL shown in your terminal (usually `http://localhost:8501`).

---

## 🖥️ Dashboard Features

| Feature                         | Description                                             |
| ------------------------------- | ------------------------------------------------------- |
| **Prediction Input**            | Select zone, date, weather, event type, visitors, etc.  |
| **Predicted Waste Volume**      | AI-predicted waste in kg for the given scenario         |
| **Risk Level**                  | 🟢 Low / 🟡 Medium / 🔴 High                            |
| **Operational Recommendations** | Staff, bins, trucks, and collection schedule            |
| **Executive Summary**           | Plain-English summary paragraph                         |
| **Zone Analytics**              | Bar chart of average waste volume per zone              |
| **7-Day Trend**                 | Area chart showing recent daily totals                  |
| **Scenario Comparison**         | Side-by-side table for Normal / Rainy / Event scenarios |

---

## 🧠 Model Details

- **Algorithm**: Random Forest Regressor (200 trees, max depth 18)
- **Preprocessing**: OneHotEncoder for categoricals, StandardScaler for numerics
- **Target**: `waste_volume_kg`
- **Features**: zone, day_of_week, is_weekend, is_holiday, weather_condition, rainfall_mm, event_type, estimated_visitors, season, bin_availability, previous_waste_kg

---

## ⚠️ Disclaimer

> This MVP uses **synthetic data** generated for demonstration purposes.
> It is **not** official DLH/DLHK Badung operational data and should not be used for real operational decisions.

---

## 📜 License

Built for hackathon / academic prototype purposes.
