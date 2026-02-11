# Credit Card Fraud Detection System

## 🎯 System Goal
Detect fraudulent transactions using machine learning models (Logistic Regression + Random Forest) on synthetic data.
**Primary Metric:** F1-Score.

## 🏗 Architecture
This is a full-stack system composed of:

1.  **Frontend (React Dashboard)**
    *   **Tech:** React (Vite), Axios, Recharts, TailwindCSS (for modern UI).
    *   **Role:** Visualization of transaction data, fraud alerts, and system metrics.
    *   **Communication:** REST API calls to the backend.

2.  **Backend (FastAPI)**
    *   **Tech:** FastAPI, Uvicorn, Pydantic.
    *   **Role:** 
        *   Serve ML predictions via API endoints.
        *   Manage database interactions.
        *   Process incoming transaction data.

3.  **ML Models**
    *   **Tech:** Scikit-learn, Pandas, NumPy.
    *   **Models:** Logistic Regression & Random Forest.
    *   **Task:** Binary Classification (0 = Legitimate, 1 = Fraud).

4.  **Database**
    *   **Tech:** PostgreSQL (Production), SQLite (Development).
    *   **Role:** Store transaction history and prediction logs.

## 📂 Project Structure
```
root/
├── backend/            # FastAPI Application & ML Models
│   ├── app/
│   │   ├── api/        # API Routes
│   │   ├── core/       # Config & Security
│   │   ├── db/         # Database Models & Session
│   │   ├── ml/         # ML Model Training & Inference Logic
│   │   └── main.py     # App Entrypoint
│   └── requirements.txt
├── frontend/           # React Dashboard (Vite)
│   ├── src/
│   │   ├── components/ # Reusable UI Components
│   │   ├── pages/      # Page Views
│   │   ├── services/   # API Service (Axios)
│   │   └── App.jsx
│   └── package.json
└── README.md
```

## 🚀 Phase 0: Setup & Design
*   Initialize Git repository.
*   Set up Backend environment (Python/FastAPI).
*   Set up Frontend environment (React/Vite).
*   Define initial database schema.
