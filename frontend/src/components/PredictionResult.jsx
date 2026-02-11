import React from 'react';

const PredictionResult = ({ result }) => {
    if (!result) return null;

    const isFraud = result.is_fraud;
    const probability = (result.probability * 100).toFixed(2);
    const borderColor = isFraud ? 'border-red-500/50' : 'border-green-500/50';
    const textColor = isFraud ? 'text-red-400' : 'text-green-400';
    const bgColor = isFraud ? 'bg-red-500/10' : 'bg-green-500/10';

    return (
        <div className={`glass-card overflow-hidden border-l-4 ${borderColor} ${bgColor} animate-fade-in`}>
            <div className="px-6 py-5">
                <div className="flex items-center justify-between mb-4">
                    <h3 className={`text-xl font-bold ${textColor}`}>
                        {isFraud ? '🚫 HIGH RISK DETECTED' : '✅ LOW RISK TRANSACTION'}
                    </h3>
                    <div className={`px-3 py-1 rounded-full text-xs font-bold border ${isFraud ? 'border-red-500/30 text-red-400' : 'border-green-500/30 text-green-400'}`}>
                        {result.model_used}
                    </div>
                </div>

                <div className="space-y-4">
                    <div>
                        <div className="flex justify-between text-sm mb-1">
                            <span className="text-slate-400">Fraud Probability</span>
                            <span className={`font-mono ${textColor}`}>{probability}%</span>
                        </div>
                        <div className="w-full bg-slate-700 rounded-full h-2 overflow-hidden">
                            <div
                                className={`h-full transition-all duration-1000 ${isFraud ? 'bg-red-500' : 'bg-green-500'}`}
                                style={{ width: `${probability}%` }}
                            ></div>
                        </div>
                    </div>

                    <p className="text-sm text-slate-400 italic">
                        {isFraud
                            ? "Warning: This transaction exhibits patterns highly consistent with historical fraud cases."
                            : "System scan complete: No significant anomalies detected in this transaction profile."
                        }
                    </p>
                </div>
            </div>
        </div>
    );
};


export default PredictionResult;
