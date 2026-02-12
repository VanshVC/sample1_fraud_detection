import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import Dashboard from './pages/Dashboard';
import Analytics from './pages/Analytics';
import ModelAnalysis from './pages/ModelAnalysis';

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-[#020617] font-sans selection:bg-indigo-500/30">

        <Navbar />
        <main>
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/analytics" element={<Analytics />} />
            <Route path="/analysis" element={<ModelAnalysis />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;
