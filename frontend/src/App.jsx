import React from 'react';
import AnalyzeTab from './tabs/AnalyzeTab';
import GenerateTab from './tabs/GenerateTab';
import './styles/App.css';

export default function App() {
  const [activeTab, setActiveTab] = React.useState('analyze');

  return (
    <div className="app">
      <header className="app-header">
        <div className="app-header-content">
          <h1>🏗️ ADR Analysis Engine</h1>
          <p>Comprehensive Architecture Decision Records Analysis & Template Generation</p>
        </div>
      </header>

      <div className="tabs-container">
        <div className="tabs-navigation">
          <button
            className={`tab-button ${activeTab === 'analyze' ? 'active' : ''}`}
            onClick={() => setActiveTab('analyze')}
          >
            📊 Analyze ADR
          </button>
          <button
            className={`tab-button ${activeTab === 'generate' ? 'active' : ''}`}
            onClick={() => setActiveTab('generate')}
          >
            ✨ Generate ADR Template
          </button>
        </div>

        <div className="tabs-content">
          {activeTab === 'analyze' && <AnalyzeTab />}
          {activeTab === 'generate' && <GenerateTab />}
        </div>
      </div>

      <footer className="app-footer">
        <p>ADR Analysis Engine v1.0.0 | Enterprise Architecture Tools</p>
      </footer>
    </div>
  );
}
