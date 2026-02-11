import React from 'react';
import { Link } from 'react-router-dom';

const Navbar = () => {
    return (
        <nav className="sticky top-0 z-50 bg-[#020617]/80 backdrop-blur-xl border-b border-white/5">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                <div className="flex justify-between h-20">
                    <div className="flex items-center gap-3 group cursor-pointer">
                        <div className="w-10 h-10 bg-gradient-to-br from-indigo-500 to-purple-600 rounded-xl flex items-center justify-center shadow-lg shadow-indigo-500/20 group-hover:scale-110 transition-transform duration-300">
                            <span className="text-xl">🛡️</span>
                        </div>
                        <span className="text-2xl font-black bg-clip-text text-transparent bg-gradient-to-r from-white to-slate-400 tracking-tight">
                            FraudGuard
                        </span>
                    </div>

                    <div className="flex items-center space-x-2">
                        <Link to="/" className="nav-link active">Dashboard</Link>
                        <Link to="/analytics" className="nav-link">Analytics</Link>
                        <div className="ml-6 pl-6 border-l border-white/10 flex items-center">
                            <div className="flex items-center px-4 py-2 bg-emerald-500/10 border border-emerald-500/20 rounded-full animate-pulse-glow">
                                <div className="h-2 w-2 bg-emerald-500 rounded-full mr-2"></div>
                                <span className="text-[10px] font-bold text-emerald-400 uppercase tracking-widest">System Active</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </nav>

    );
};


export default Navbar;
