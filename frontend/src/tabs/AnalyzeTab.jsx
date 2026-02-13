import React, { useState, useEffect } from 'react';
import { analysisAPI } from '../api';
import ScoreBadge from '../components/ScoreBadge';
import AnalysisResults from '../components/AnalysisResults';
import '../styles/AnalyzeTab.css';

export default function AnalyzeTab() {
  const [inputMethod, setInputMethod] = useState('text'); // text, file
  const [textInput, setTextInput] = useState('');
  const [uploadedFile, setUploadedFile] = useState(null);
  const [analysisId, setAnalysisId] = useState(null);
  const [analysis, setAnalysis] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [thinking, setThinking] = useState(false);

  useEffect(() => {
    if (analysisId) {
      loadAnalysis(analysisId);
    }
  }, [analysisId]);

  const handleFileUpload = (event) => {
    const file = event.target.files[0];
    if (file) {
      setUploadedFile(file);
      setError(null);
    }
  };

  const analyzeContent = async () => {
    try {
      setLoading(true);
      setThinking(true);
      setError(null);
      setAnalysis(null);

      let result;
      if (inputMethod === 'text') {
        if (!textInput.trim()) {
          throw new Error('Please enter some ADR content to analyze');
        }
        result = await analysisAPI.analyzeText(textInput);
      } else {
        if (!uploadedFile) {
          throw new Error('Please select a file to analyze');
        }
        
        if (uploadedFile.name.endsWith('.pdf')) {
          result = await analysisAPI.analyzePDF(uploadedFile);
        } else if (uploadedFile.name.endsWith('.md') || uploadedFile.type === 'text/plain') {
          result = await analysisAPI.analyzeMarkdown(uploadedFile);
        } else {
          throw new Error('Please upload a PDF or Markdown file');
        }
      }

      setAnalysisId(result.data.id);
    } catch (err) {
      setError(err.message || 'Analysis failed');
      setLoading(false);
      setThinking(false);
    }
  };

  const loadAnalysis = async (id) => {
    try {
      const response = await analysisAPI.getAnalysis(id);
      setAnalysis(response.data);
      setLoading(false);
      setThinking(false);
    } catch (err) {
      setError('Failed to load analysis');
      setLoading(false);
      setThinking(false);
    }
  };

  return (
    <div className="analyze-tab">
      <div className="analyze-container">
        {/* Input Section */}
        {!analysis && (
          <div className="input-section">
            <h2>Analyze Architecture Decision Record</h2>
            
            <div className="input-method-selector">
              <button
                className={`method-btn ${inputMethod === 'text' ? 'active' : ''}`}
                onClick={() => {
                  setInputMethod('text');
                  setUploadedFile(null);
                }}
              >
                📝 Paste Text
              </button>
              <button
                className={`method-btn ${inputMethod === 'file' ? 'active' : ''}`}
                onClick={() => {
                  setInputMethod('file');
                  setTextInput('');
                }}
              >
                📁 Upload File
              </button>
            </div>

            {inputMethod === 'text' && (
              <div className="text-input-group">
                <textarea
                  className="content-textarea"
                  placeholder="Paste your ADR content here (markdown format)..."
                  value={textInput}
                  onChange={(e) => setTextInput(e.target.value)}
                  rows="15"
                />
                <div className="char-count">{textInput.length} characters</div>
              </div>
            )}

            {inputMethod === 'file' && (
              <div className="file-input-group">
                <label className="file-upload-label">
                  <input
                    type="file"
                    onChange={handleFileUpload}
                    accept=".pdf,.md,.txt"
                    className="file-input"
                  />
                  <span className="file-upload-placeholder">
                    {uploadedFile ? (
                      <>✓ {uploadedFile.name}</>
                    ) : (
                      <>📎 Click to select PDF, Markdown, or text file</>
                    )}
                  </span>
                </label>
              </div>
            )}

            {error && <div className="error-message">{error}</div>}

            <button
              className="analyze-button"
              onClick={analyzeContent}
              disabled={loading || (!textInput.trim() && !uploadedFile)}
            >
              {loading ? '⏳ Analyzing...' : '🚀 Analyze ADR'}
            </button>
          </div>
        )}

        {/* Thinking Process */}
        {thinking && (
          <div className="thinking-process">
            <h3>🧠 Analysis In Progress</h3>
            <div className="thinking-steps">
              <div className="thinking-step">
                <span className="spinner"></span>
                <span>Phase 1: Structural Analysis</span>
              </div>
              <div className="thinking-step">
                <span className="spinner"></span>
                <span>Phase 2: Quality Assessment</span>
              </div>
              <div className="thinking-step">
                <span className="spinner"></span>
                <span>Phase 3: LLM Detection</span>
              </div>
              <div className="thinking-step">
                <span className="spinner"></span>
                <span>Phases 4-9: Advanced Analysis</span>
              </div>
            </div>
          </div>
        )}

        {/* Results Section */}
        {analysis && (
          <div className="results-section">
            <div className="results-header">
              <h2>Analysis Results</h2>
              <button
                className="new-analysis-button"
                onClick={() => {
                  setAnalysis(null);
                  setAnalysisId(null);
                  setTextInput('');
                  setUploadedFile(null);
                }}
              >
                ← New Analysis
              </button>
            </div>

            <div className="results-summary">
              <div className="summary-card">
                <h3>Overall Quality Score</h3>
                <ScoreBadge score={analysis.overall_quality_score} />
              </div>
              <div className="summary-card">
                <h3>Architecture Maturity</h3>
                <ScoreBadge score={analysis.overall_maturity_score} />
              </div>
              <div className="summary-card">
                <h3>Standards Compliance</h3>
                <ScoreBadge score={analysis.compliance_percentage} />
              </div>
            </div>

            <AnalysisResults data={analysis} />
          </div>
        )}
      </div>
    </div>
  );
}
