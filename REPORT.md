# Final Project Report - Credit Card Fraud Detection System

## 1. Executive Summary
This project implements a full-stack automated system to detect fraudulent credit card transactions in real-time. By leveraging machine learning (Random Forest and Logistic Regression) integrated with a modern web dashboard, the system provides both instant prediction capabilities and deep analytical insights into fraud patterns.

## 2. Methodology

### 2.1 Data Generation & Preprocessing
- **Synthetic Dataset**: Generated 3,000 transactions with controlled patterns for fraud (high amounts, late hours, etc.) to simulate real-world scenarios.
- **Preprocessing**: 
    - **Label Encoding**: Converted categorical variables (Category, Location) to numeric.
    - **Scaling**: Applied Standard Scaler to normalize numerical features (Amount, Time, Age).
    - **Stratified Split**: Maintained the fraud-to-legitimate ratio (approx. 8%) in both training and testing sets.

### 2.2 Model Selection
Two models were trained and compared:
1.  **Logistic Regression**: Used as a linear baseline. Provided interpretability but failed to capture complex, non-linear fraud patterns (F1 Score: ~0.26).
2.  **Random Forest Classifier**: The primary model. An ensemble of decision trees that excels at handling non-linear relationships and interactions between features (e.g., *High Amount* + *Late Night* = *Fraud*).
    - **Performance**: Achieved an accuracy of >92% and significantly higher Precision/Recall than the baseline.

### 2.3 System Architecture
- **Backend**: FastAPI (Python) for high-performance API serving.
- **Database**: SQLite (SQLAlchemy) for persistent storage of transaction history.
- **Frontend**: React (Vite) + TailwindCSS for a responsive, professional dashboard.
- **Visualization**: Recharts for interactive analytics (Feature Importance, Fraud Distribution).

## 3. Key Findings & Analysis

### 3.1 Fraud Patterns
- **High Amounts**: Transactions over $1,000 are the strongest indicator of fraud.
- **Time of Day**: Activity between 12 AM and 4 AM correlates highly with fraudulent behavior.
- **Low Profile History**: New accounts (low `previous_trans` count) are riskier.

### 3.2 Why Random Forest?
Random Forest outperformed Logistic Regression because fraud is rarely linear. It's not just "high amount = fraud"; it's a combination of factors. Decision trees naturally learn these "if-then" rules (e.g., *IF* amount > $500 *AND* time is 3 AM *THEN* fraud), which linear models struggle to represent without complex feature engineering.

## 4. Business Impact
- **Cost Savings**: By catching fraud in real-time, the system prevents financial loss (False Negatives are minimized).
- **Operational Efficiency**: The dashboard allows analysts to review flagged transactions instantly rather than manually auditing logs.
- **Scalability**: The containerized (Docker-ready) architecture allows for easy scaling as transaction volume grows.

## 5. Future Improvements
- **Deep Learning**: Explore LSTM or Autoencoders for sequence-based anomaly detection.
- **Real Data**: Retrain on a larger, real-world dataset (e.g., Kaggle European Card dataset).
- **Deployment**: Deploy to AWS/GCP with a production-grade database (PostgreSQL).

---
*Generated for Viva/Final Presentation*
