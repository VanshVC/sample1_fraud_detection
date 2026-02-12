# 🛡️ Fraud Detection System

A complete end-to-end Machine Learning based Fraud Detection System. This project features a robust FastAPI backend serving real-time predictions and a modern React dashboard for monitoring transactions.

## 🚀 Features

-   **Real-time Fraud Detection**: ML models (Logistic Regression & Random Forest) classify transactions instantly.
-   **Interactive Dashboard**: Visualize transaction trends, fraud distribution, and model performance.
-   **Production-Ready Backend**: Built with FastAPI, PostgreSQL, SQLAlchemy, and Alembic.
-   **Comprehensive API**: Endpoints for single/batch predictions and analytics.
-   **Containerized**: Easy deployment with Docker Compose.

## 🛠️ Tech Stack

-   **Backend**: Python, FastAPI, Uvicorn, SQLAlchemy, Alembic
-   **Database**: PostgreSQL
-   **ML**: Scikit-Learn, Pandas, NumPy
-   **Frontend**: React (Vite), TailwindCSS, Recharts
-   **DevOps**: Docker, Docker Compose

## ⚡ Quick Start

### Prerequisites
-   Docker & Docker Compose OR
-   Python 3.9+ and Node.js 18+ and PostgreSQL

### Option 1: Docker (Testing Only)
```bash
docker-compose up --build
```
Access the dashboard at `http://localhost:5173` and API docs at `http://localhost:8000/docs`.

### Option 2: Local Development

1.  **Backend Setup**
    ```bash
    cd backend
    python -m venv .venv
    source .venv/bin/activate  # Windows: .venv\Scripts\activate
    pip install -r requirements.txt
    
    # Configure Database (PostgreSQL must be running)
    # Update .env or ensure default credentials work
    
    # Run Migrations/Init DB
    python init_db.py  # Or 'alembic upgrade head'

    uvicorn app.main:app --reload
    ```

2.  **Frontend Setup**
    ```bash
    cd frontend
    npm install
    npm run dev
    ```

## 📂 Project Structure

```
root/
├── backend/            # FastAPI Application & Migrations
│   ├── app/            # Source Code
│   │   ├── api/        # Routes (Predict, Analytics)
│   │   ├── core/       # Configuration
│   │   ├── db/         # Models & Database Logic
│   │   └── ml/         # ML Pipelines
│   └── tests/          # Pytest Suite
├── frontend/           # React Dashboard
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   └── services/
└── docker-compose.yml
```

## 🔍 API Endpoints

-   `POST /api/predict`: Classify a transaction.
-   `GET /api/analytics`: Get fraud statistics (From PostgreSQL).
-   `GET /docs`: Interactive Swagger UI.

## 📝 License

This project is open-source and available under the MIT License.
