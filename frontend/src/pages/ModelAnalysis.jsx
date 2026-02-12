
import React, { useState, useEffect } from 'react';
import TransactionForm from '../components/TransactionForm';
import PredictionResult from '../components/PredictionResult';
import { predictFraud } from '../services/api';

const ModelAnalysis = () => {
    const [prediction, setPrediction] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [metrics, setMetrics] = useState(null);

    useEffect(() => {
        // Phase 5.1: Load Metrics
        fetch("/analysis/metrics.json")
            .then(res => res.json())
            .then(data => setMetrics(data))
            .catch(err => console.error("Error loading metrics:", err));
    }, []);

    const handlePredict = async (data) => {
        setLoading(true);
        setError(null);
        setPrediction(null);

        const sanitizedData = {
            ...data,
            amount: parseFloat(data.amount),
            time: parseInt(data.time),
            age: parseInt(data.age),
            previous_trans: parseInt(data.previous_trans)
        };

        try {
            const response = await predictFraud(sanitizedData);
            setPrediction(response.data);
        } catch (err) {
            setError('Failed to analyze transaction. Please check the backend connection.');
            console.error(err);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
            <div className="mb-12">
                <h1 className="text-4xl font-extrabold text-white mb-2 tracking-tight">
                    Analyze <span className="bg-clip-text text-transparent bg-gradient-to-r from-indigo-500 to-purple-500">Transaction</span>
                </h1>
                <p className="text-slate-400 text-lg">Predict fraud and view model performance insights.</p>
            </div>

            {/* LIVE PREDICTION SECTION */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 mb-20">
                <div className="space-y-6">
                    <div className="glass-card p-8 border-l-4 border-indigo-500 shadow-xl shadow-indigo-500/5">
                        <h2 className="text-xl font-bold text-white mb-6 flex items-center gap-2">
                            <div className="w-2 h-6 bg-indigo-500 rounded-full"></div>
                            1. Transaction Profiling
                        </h2>
                        <TransactionForm onPredict={handlePredict} loading={loading} />
                    </div>
                </div>

                <div className="space-y-6">
                    <div className="glass-card p-8 border-l-4 border-purple-500 shadow-xl shadow-purple-500/5 min-h-[400px]">
                        <h2 className="text-xl font-bold text-white mb-6 flex items-center gap-2">
                            <div className="w-2 h-6 bg-purple-500 rounded-full"></div>
                            2. Prediction Engine
                        </h2>
                        {error && (
                            <div className="bg-red-500/10 border border-red-500/20 text-red-400 px-6 py-4 rounded-xl mb-4">
                                {error}
                            </div>
                        )}

                        <PredictionResult result={prediction} />

                        {!prediction && !loading && !error && (
                            <div className="flex flex-col items-center justify-center h-full py-12 text-center text-slate-500">
                                <div className="text-6xl mb-4 opacity-20">🧠</div>
                                <p className="max-w-xs">Enter transaction details to trigger the Random Forest classifier.</p>
                            </div>
                        )}

                        {loading && (
                            <div className="flex flex-col items-center justify-center h-full py-12 text-center">
                                <div className="relative">
                                    <div className="w-16 h-16 border-4 border-indigo-500/10 rounded-full"></div>
                                    <div className="absolute top-0 left-0 w-16 h-16 border-4 border-indigo-500 border-t-transparent rounded-full animate-spin"></div>
                                </div>
                                <p className="mt-6 text-indigo-400 font-medium animate-pulse">Running Neural Inference...</p>
                            </div>
                        )}
                    </div>
                </div>
            </div>

            {/* MODEL EVALUATION SECTION */}
            <div className="space-y-12 bg-slate-900/40 p-10 rounded-[2.5rem] border border-slate-800/50">
                <div className="text-center mb-12">
                    <h2 className="text-3xl font-bold text-white mb-4">Model Evaluation Dashboard</h2>
                    <div className="w-24 h-1 bg-indigo-500 mx-auto rounded-full"></div>
                </div>

                {/* 5.2 Metrics Display */}
                {metrics && (
                    <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
                        <MetricCard label="Accuracy" value={metrics.accuracy} icon="🎯" color="text-emerald-400" />
                        <MetricCard label="Precision" value={metrics.precision} icon="🛡️" color="text-indigo-400" />
                        <MetricCard label="Recall" value={metrics.recall} icon="🔍" color="text-amber-400" />
                        <MetricCard label="F1 Score" value={metrics.f1_score} icon="⚡" color="text-purple-400" />
                    </div>
                )}

                {/* 5.3 Visuals Display */}
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                    <VisualCard title="Confusion Matrix" src="/analysis/confusion_matrix.png" description="Shows the ratio of True Positives, True Negatives, False Positives (False Alarms), and False Negatives (Misses)." />
                    <VisualCard title="ROC Curve" src="/analysis/roc_curve.png" description="The Receiver Operating Characteristic curve illustrates the diagnostic ability of our binary classifier." />
                </div>

                <div className="grid grid-cols-1 gap-8">
                    <VisualCard title="Feature Importance" src="/analysis/feature_importance.png" description="Identifies which transaction attributes (e.g., Amount, Time) most significantly influence the model's fraud prediction." wide />
                </div>
            </div>
        </div>
    );
};

const MetricCard = ({ label, value, icon, color }) => (
    <div className="glass-card p-6 flex flex-col items-center border border-white/5 hover:border-indigo-500/30 transition-all duration-300">
        <span className="text-3xl mb-2">{icon}</span>
        <h4 className="text-slate-500 text-sm font-medium uppercase tracking-wider">{label}</h4>
        <p className={`text-3xl font-bold mt-1 ${color}`}>{(value * 100).toFixed(1)}%</p>
    </div>
);

const VisualCard = ({ title, src, description, wide }) => (
    <div className={`glass-card p-8 border border-white/5 hover-glow ${wide ? 'col-span-full' : ''}`}>
        <h3 className="text-xl font-bold text-white mb-4">{title}</h3>
        <div className="bg-slate-950/50 rounded-2xl p-4 border border-slate-800/50">
            <img src={src} alt={title} className="w-full h-auto rounded-lg shadow-2xl" />
        </div>
        <p className="mt-4 text-slate-400 text-sm leading-relaxed">{description}</p>
    </div>
);

export default ModelAnalysis;
