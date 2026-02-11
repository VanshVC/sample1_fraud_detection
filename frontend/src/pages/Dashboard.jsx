import React, { useState } from 'react';
import TransactionForm from '../components/TransactionForm';
import PredictionResult from '../components/PredictionResult';
import { predictFraud } from '../services/api';

const Dashboard = () => {
    const [prediction, setPrediction] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    const handlePredict = async (data) => {
        setLoading(true);
        setError(null);
        setPrediction(null);

        // Ensure numeric fields are numbers
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
                <h1 className="text-4xl font-extrabold text-white mb-2">Real-time Fraud Analysis</h1>
                <p className="text-slate-400 text-lg">Deploying advanced ML models to safeguard your transactions.</p>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-12">
                <div className="space-y-6 animate-stealth">
                    <TransactionForm onPredict={handlePredict} loading={loading} />
                </div>

                <div className="space-y-6">
                    {error && (
                        <div className="bg-red-500/5 border border-red-500/20 text-red-400 px-6 py-4 rounded-2xl animate-stealth" role="alert">
                            <span className="block sm:inline">{error}</span>
                        </div>
                    )}

                    <PredictionResult result={prediction} />

                    {!prediction && !loading && !error && (
                        <div className="glass-card p-12 text-center flex flex-col items-center justify-center h-full min-h-[400px]">
                            <div className="w-20 h-20 bg-slate-700/30 rounded-full flex items-center justify-center mb-6">
                                <span className="text-4xl text-slate-500">🔍</span>
                            </div>
                            <h3 className="text-xl font-semibold text-slate-300 mb-2">Ready for Analysis</h3>
                            <p className="text-slate-500 max-w-xs">Input a transaction profile on the left to generate an instant risk score.</p>
                        </div>
                    )}

                    {loading && (
                        <div className="glass-card p-12 text-center flex flex-col items-center justify-center h-full min-h-[400px] animate-stealth">
                            <div className="relative">
                                <div className="w-20 h-20 border-4 border-indigo-500/10 rounded-full"></div>
                                <div className="absolute top-0 left-0 w-20 h-20 border-4 border-indigo-500 border-t-transparent rounded-full animate-spin"></div>
                                <div className="absolute inset-0 bg-indigo-500/10 blur-2xl rounded-full"></div>
                            </div>
                            <h3 className="mt-8 text-2xl font-bold text-white tracking-tight">Scanning Global Network</h3>
                            <p className="text-slate-500 mt-2 max-w-xs">Cross-referencing transaction metadata with deep-learning nodes.</p>
                        </div>
                    )}

                </div>
            </div>
        </div>
    );
};


export default Dashboard;
