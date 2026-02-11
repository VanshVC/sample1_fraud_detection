import React, { useEffect, useState } from 'react';
import { getAnalytics, getModelMetrics, getFeatureImportance, getFraudDistribution, getAmountVsFraud } from '../services/api';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';

const Analytics = () => {
    const [analytics, setAnalytics] = useState(null);
    const [metrics, setMetrics] = useState(null);
    const [features, setFeatures] = useState([]);
    const [distribution, setDistribution] = useState([]);
    const [amountStats, setAmountStats] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const [analyticsRes, metricsRes, featuresRes, distRes, amountRes] = await Promise.all([
                    getAnalytics(),
                    getModelMetrics(),
                    getFeatureImportance(),
                    getFraudDistribution(),
                    getAmountVsFraud()
                ]);
                setAnalytics(analyticsRes.data);
                setMetrics(metricsRes.data);
                setFeatures(featuresRes.data);
                setDistribution(distRes.data);
                setAmountStats(amountRes.data);
            } catch (err) {
                console.error("Error fetching analytics", err);
            } finally {
                setLoading(false);
            }
        };

        fetchData();
    }, []);

    if (loading) return <div className="text-center py-10">Loading analytics...</div>;

    // Colors
    const COLORS = ['#10B981', '#EF4444']; // Green, Red

    // Confusion Matrix Data
    const confusionData = metrics?.confusion_matrix ? [
        { name: 'True Negative', value: metrics.confusion_matrix.tn, fill: '#10B981' },
        { name: 'False Positive', value: metrics.confusion_matrix.fp, fill: '#EF4444' },
        { name: 'False Negative', value: metrics.confusion_matrix.fn, fill: '#F59E0B' },
        { name: 'True Positive', value: metrics.confusion_matrix.tp, fill: '#3B82F6' },
    ] : [];

    return (
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
            <div className="mb-12">
                <h1 className="text-4xl font-extrabold text-white mb-2">System Analytics</h1>
                <p className="text-slate-400 text-lg">Comprehensive overview of model performance and transaction trends.</p>
            </div>

            {/* Quick Stats */}
            <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-12">
                {[
                    { label: 'Total Transactions', value: analytics?.total_transactions, icon: '📊', color: 'text-indigo-400' },
                    { label: 'Fraud Cases', value: analytics?.fraud_count, icon: '🚨', color: 'text-red-400' },
                    { label: 'Fraud Percentage', value: `${analytics?.fraud_percentage}%`, icon: '📉', color: 'text-pink-400' },
                    { label: 'Random Forest F1', value: metrics?.f1_score?.toFixed(4), icon: '🤖', color: 'text-green-400' }
                ].map((stat, i) => (
                    <div key={i} className="glass-card px-8 py-8 animate-stealth" style={{ animationDelay: `${i * 100}ms` }}>
                        <div className="flex items-center justify-between mb-4">
                            <span className="w-10 h-10 rounded-xl bg-white/5 flex items-center justify-center text-xl">{stat.icon}</span>
                            <span className="text-[10px] font-bold uppercase tracking-widest text-slate-500">{stat.label}</span>
                        </div>
                        <dd className={`text-4xl font-black ${stat.color} tracking-tighter`}>{stat.value}</dd>
                    </div>
                ))}
            </div>


            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">

                {/* Feature Importance */}
                <div className="glass-card p-8 animate-stealth" style={{ animationDelay: '400ms' }}>
                    <h3 className="text-xl font-bold text-white mb-8 flex items-center">
                        <span className="w-8 h-8 rounded-lg bg-indigo-500/20 flex items-center justify-center mr-3 text-lg">🔑</span>
                        Key Predictors
                    </h3>
                    <div className="h-80 w-full">
                        <ResponsiveContainer width="100%" height="100%">
                            <BarChart layout="vertical" data={features}>
                                <XAxis type="number" hide />
                                <YAxis dataKey="feature" type="category" width={100} stroke="#475569" fontSize={11} />
                                <Tooltip
                                    contentStyle={{ backgroundColor: '#0f172a', border: '1px solid #1e293b', borderRadius: '12px', color: '#f8fafc' }}
                                    itemStyle={{ color: '#818cf8' }}
                                    cursor={{ fill: 'rgba(255,255,255,0.02)' }}
                                />
                                <Bar dataKey="importance" fill="url(#colorImportance)" radius={[0, 4, 4, 0]} />
                                <defs>
                                    <linearGradient id="colorImportance" x1="0" y1="0" x2="1" y2="0">
                                        <stop offset="5%" stopColor="#6366f1" stopOpacity={0.8} />
                                        <stop offset="95%" stopColor="#a855f7" stopOpacity={0.8} />
                                    </linearGradient>
                                </defs>
                            </BarChart>
                        </ResponsiveContainer>
                    </div>
                </div>


                {/* Fraud Distribution Pie Chart */}
                <div className="glass-card p-8 animate-stealth" style={{ animationDelay: '500ms' }}>
                    <h3 className="text-xl font-bold text-white mb-8 flex items-center">
                        <span className="w-8 h-8 rounded-lg bg-indigo-500/20 flex items-center justify-center mr-3 text-lg">🎯</span>
                        Traffic Composition
                    </h3>
                    <div className="h-80 w-full">
                        <ResponsiveContainer width="100%" height="100%">
                            <PieChart>
                                <Pie
                                    data={distribution}
                                    cx="50%"
                                    cy="50%"
                                    labelLine={false}
                                    label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                                    outerRadius={100}
                                    innerRadius={70}
                                    paddingAngle={8}
                                    dataKey="value"
                                >
                                    {distribution.map((entry, index) => (
                                        <Cell
                                            key={`cell-${index}`}
                                            fill={index === 0 ? '#6366f1' : '#f43f5e'}
                                            fillOpacity={0.9}
                                            stroke="none"
                                        />
                                    ))}
                                </Pie>
                                <Tooltip
                                    contentStyle={{ backgroundColor: '#0f172a', border: '1px solid #1e293b', borderRadius: '12px', color: '#f8fafc' }}
                                />
                            </PieChart>
                        </ResponsiveContainer>
                    </div>
                </div>

            </div>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                {/* Transaction Amount vs Fraud */}
                <div className="glass-card p-8 animate-stealth" style={{ animationDelay: '600ms' }}>
                    <h3 className="text-xl font-bold text-white mb-8 flex items-center">
                        <span className="w-8 h-8 rounded-lg bg-indigo-500/20 flex items-center justify-center mr-3 text-lg">💰</span>
                        Risk by Volume
                    </h3>
                    <div className="h-80 w-full">
                        <ResponsiveContainer width="100%" height="100%">
                            <BarChart data={amountStats}>
                                <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" vertical={false} />
                                <XAxis dataKey="range" stroke="#475569" fontSize={11} />
                                <YAxis stroke="#475569" fontSize={11} />
                                <Tooltip
                                    contentStyle={{ backgroundColor: '#0f172a', border: '1px solid #1e293b', borderRadius: '12px', color: '#f8fafc' }}
                                />
                                <Legend verticalAlign="top" height={36} />
                                <Bar dataKey="legitimate" name="Legitimate" fill="#6366f1" fillOpacity={0.4} radius={[4, 4, 0, 0]} />
                                <Bar dataKey="fraud" name="Fraud" fill="#f43f5e" fillOpacity={0.8} radius={[4, 4, 0, 0]} />
                            </BarChart>
                        </ResponsiveContainer>
                    </div>
                </div>

                {/* Confusion Matrix */}
                <div className="glass-card p-8 animate-stealth" style={{ animationDelay: '700ms' }}>
                    <h3 className="text-xl font-bold text-white mb-8 flex items-center">
                        <span className="w-8 h-8 rounded-lg bg-indigo-500/20 flex items-center justify-center mr-3 text-lg">📐</span>
                        Confusion Matrix
                    </h3>
                    <div className="h-80 w-full">
                        <ResponsiveContainer width="100%" height="100%">
                            <BarChart data={confusionData}>
                                <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" vertical={false} />
                                <XAxis dataKey="name" stroke="#475569" fontSize={10} />
                                <YAxis stroke="#475569" fontSize={11} />
                                <Tooltip
                                    contentStyle={{ backgroundColor: '#0f172a', border: '1px solid #1e293b', borderRadius: '12px', color: '#f8fafc' }}
                                />
                                <Bar dataKey="value" radius={[4, 4, 0, 0]}>
                                    {confusionData.map((entry, index) => (
                                        <Cell key={`cell-${index}`} fill={entry.fill} fillOpacity={0.6} stroke={entry.fill} strokeWidth={1} />
                                    ))}
                                </Bar>
                            </BarChart>
                        </ResponsiveContainer>
                    </div>
                </div>
            </div>

        </div>
    );
};


export default Analytics;
