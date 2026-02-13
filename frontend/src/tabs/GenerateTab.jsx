import React, { useState, useRef } from 'react';
import { templateAPI, jiraAPI } from '../api';
import '../styles/GenerateTab.css';

export default function GenerateTab() {
  const [jiraInput, setJiraInput] = useState('');
  const [contextInput, setContextInput] = useState('');
  const [useJiraAPI, setUseJiraAPI] = useState(false);
  const [template, setTemplate] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [jiraConfigured, setJiraConfigured] = useState(false);
  const textareaRef = useRef(null);

  React.useEffect(() => {
    checkJiraConfig();
  }, []);

  const checkJiraConfig = async () => {
    try {
      const response = await jiraAPI.checkConfig();
      setJiraConfigured(response.data.configured);
    } catch (err) {
      setJiraConfigured(false);
    }
  };

  const generateTemplate = async () => {
    try {
      setLoading(true);
      setError(null);
      
      if (!jiraInput.trim()) {
        throw new Error('Please enter a JIRA ticket ID (e.g., PROJ-123)');
      }

      const result = await templateAPI.generateFromJIRA(
        jiraInput,
        contextInput,
        useJiraAPI && jiraConfigured
      );

      setTemplate(result.data.template);
    } catch (err) {
      setError(err.message || 'Failed to generate template');
    } finally {
      setLoading(false);
    }
  };

  const copyToClipboard = () => {
    if (textareaRef.current) {
      textareaRef.current.select();
      document.execCommand('copy');
      alert('Template copied to clipboard!');
    }
  };

  const downloadTemplate = () => {
    if (!template) return;
    
    const element = document.createElement('a');
    const file = new Blob([template], { type: 'text/markdown' });
    element.href = URL.createObjectURL(file);
    element.download = `ADR-${jiraInput.replace(/-/g, '_')}.md`;
    document.body.appendChild(element);
    element.click();
    document.body.removeChild(element);
  };

  return (
    <div className="generate-tab">
      <div className="generate-container">
        {!template ? (
          <div className="generate-form-section">
            <h2>Generate ADR Template from JIRA</h2>

            <div className="form-group">
              <label htmlFor="jira-id">JIRA Ticket ID *</label>
              <input
                id="jira-id"
                type="text"
                placeholder="e.g., PROJ-123 or https://jira.example.com/browse/PROJ-123"
                value={jiraInput}
                onChange={(e) => setJiraInput(e.target.value)}
                className="form-input"
              />
              <small>Enter the JIRA ticket ID or full URL</small>
            </div>

            {jiraConfigured && (
              <div className="form-group checkbox-group">
                <label>
                  <input
                    type="checkbox"
                    checked={useJiraAPI}
                    onChange={(e) => setUseJiraAPI(e.target.checked)}
                  />
                  Fetch from JIRA API (requires configuration)
                </label>
              </div>
            )}

            <div className="form-group">
              <label htmlFor="context">Additional Context (Optional)</label>
              <textarea
                id="context"
                placeholder="Add any additional information about this decision that should be included in the template..."
                value={contextInput}
                onChange={(e) => setContextInput(e.target.value)}
                rows="8"
                className="form-textarea"
              />
            </div>

            {error && <div className="error-message">{error}</div>}

            <button
              className="generate-button"
              onClick={generateTemplate}
              disabled={loading || !jiraInput.trim()}
            >
              {loading ? '⏳ Generating...' : '✨ Generate Template'}
            </button>

            {!jiraConfigured && (
              <div className="info-box">
                <p>
                  💡 <strong>JIRA API not configured</strong> - You can still use manual input.
                  To enable JIRA API integration, configure the JIRA credentials in your .env file.
                </p>
              </div>
            )}
          </div>
        ) : (
          <div className="template-result-section">
            <div className="template-header">
              <h2>Generated ADR Template</h2>
              <p className="ticket-id">JIRA: {jiraInput}</p>
            </div>

            <div className="template-actions">
              <button className="action-button copy-btn" onClick={copyToClipboard}>
                📋 Copy to Clipboard
              </button>
              <button className="action-button download-btn" onClick={downloadTemplate}>
                ⬇️ Download as .md
              </button>
              <button
                className="action-button new-btn"
                onClick={() => {
                  setTemplate(null);
                  setJiraInput('');
                  setContextInput('');
                }}
              >
                ➕ Generate Another
              </button>
            </div>

            <textarea
              ref={textareaRef}
              className="template-textarea"
              value={template}
              readOnly
              rows="30"
            />
          </div>
        )}
      </div>
    </div>
  );
}
