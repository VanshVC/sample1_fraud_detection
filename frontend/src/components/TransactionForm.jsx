import React, { useState } from 'react';

const TransactionForm = ({ onPredict, loading }) => {
    // Default values for quick testing
    const [formData, setFormData] = useState({
        amount: 150.00,
        time: 14,
        category: 'electronics',
        age: 35,
        location: 'New York',
        previous_trans: 10
    });

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData(prev => ({ ...prev, [name]: value }));
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        onPredict(formData);
    };

    return (
        <div className="glass-card overflow-hidden animate-fade-in">
            <div className="px-6 py-5 border-b border-slate-700/50 bg-slate-800/30">
                <h3 className="text-xl font-bold text-white flex items-center">
                    <span className="mr-2">📝</span> Transaction Details
                </h3>
                <p className="mt-1 text-sm text-slate-400">Enter transaction information for real-time risk assessment.</p>
            </div>
            <div className="px-6 py-6">
                <form onSubmit={handleSubmit} className="grid grid-cols-1 gap-y-6 gap-x-4 sm:grid-cols-6">

                    <div className="sm:col-span-3">
                        <label htmlFor="amount" className="block text-sm font-medium text-slate-300 mb-1">Amount ($)</label>
                        <input type="number" name="amount" id="amount" value={formData.amount} onChange={handleChange} step="0.01" className="input-field w-full" required />
                    </div>

                    <div className="sm:col-span-3">
                        <label htmlFor="time" className="block text-sm font-medium text-slate-300 mb-1">Time (Hour 0-23)</label>
                        <input type="number" name="time" id="time" value={formData.time} onChange={handleChange} min="0" max="23" className="input-field w-full" required />
                    </div>

                    <div className="sm:col-span-3">
                        <label htmlFor="category" className="block text-sm font-medium text-slate-300 mb-1">Category</label>
                        <select name="category" id="category" value={formData.category} onChange={handleChange} className="input-field w-full">
                            <option value="groceries">Groceries</option>
                            <option value="electronics">Electronics</option>
                            <option value="utilities">Utilities</option>
                            <option value="entertainment">Entertainment</option>
                            <option value="travel">Travel</option>
                            <option value="dining">Dining</option>
                            <option value="gas">Gas</option>
                        </select>
                    </div>

                    <div className="sm:col-span-3">
                        <label htmlFor="age" className="block text-sm font-medium text-slate-300 mb-1">Age</label>
                        <input type="number" name="age" id="age" value={formData.age} onChange={handleChange} min="18" max="100" className="input-field w-full" required />
                    </div>

                    <div className="sm:col-span-3">
                        <label htmlFor="location" className="block text-sm font-medium text-slate-300 mb-1">Location</label>
                        <input type="text" name="location" id="location" value={formData.location} onChange={handleChange} className="input-field w-full" required />
                    </div>

                    <div className="sm:col-span-3">
                        <label htmlFor="previous_trans" className="block text-sm font-medium text-slate-300 mb-1">Previous Transactions</label>
                        <input type="number" name="previous_trans" id="previous_trans" value={formData.previous_trans} onChange={handleChange} min="0" className="input-field w-full" required />
                    </div>

                    <div className="sm:col-span-6 mt-2">
                        <button type="submit" disabled={loading} className="btn-primary w-full flex items-center justify-center space-x-2">
                            {loading ? (
                                <>
                                    <svg className="animate-spin h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                                        <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                                        <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                                    </svg>
                                    <span>Analyzing Risk Profile...</span>
                                </>
                            ) : (
                                <>
                                    <span>🔍 Analyze Transaction</span>
                                </>
                            )}
                        </button>
                    </div>
                </form>
            </div>
        </div>
    );
};


export default TransactionForm;
