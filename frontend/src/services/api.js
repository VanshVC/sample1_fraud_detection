import axios from 'axios';

const api = axios.create({
    baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000/api',
});

export const predictFraud = async (data) => {
    return await api.post('predict', data);
};

export const getAnalytics = async () => {
    return await api.get('analytics');
};

export const getModelMetrics = async () => {
    return await api.get('model-metrics');
};

export const getFeatureImportance = async () => {
    return await api.get('visualizations/feature-importance');
};

export const getFraudDistribution = async () => {
    return await api.get('visualizations/fraud-distribution');
};

export const getAmountVsFraud = async () => {
    return await api.get('visualizations/amount-vs-fraud');
};

export default api;
