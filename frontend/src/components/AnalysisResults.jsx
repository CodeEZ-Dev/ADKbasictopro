import React, { useState } from 'react';
import ScoreBadge from './ScoreBadge';
import '../styles/AnalysisResults.css';

export default function AnalysisResults({ data }) {
  const [expandedPhase, setExpandedPhase] = useState('phase_1');

  const phases = [
    { key: 'phase_1_structural_analysis', title: '📐 Phase 1: Structural Analysis' },
    { key: 'phase_2_quality_assessment', title: '⭐ Phase 2: Quality Assessment' },
    { key: 'phase_3_llm_detection', title: '🤖 Phase 3: LLM Detection' },
    { key: 'phase_4_improvements', title: '💡 Phase 4: Improvement Suggestions' },
    { key: 'phase_5_enterprise', title: '🏛️ Phase 5: Enterprise Architecture' },
    { key: 'phase_6_design_patterns', title: '🎯 Phase 6: Design Patterns' },
    { key: 'phase_7_technical_debt', title: '⚠️ Phase 7: Technical Debt' },
    { key: 'phase_8_maturity', title: '📈 Phase 8: Maturity Scoring' },
    { key: 'phase_9_compliance', title: '✅ Phase 9: Standards Compliance' },
  ];

  const renderPhase1 = (data) => (
    <div className="phase-details">
      <div className="metrics-grid">
        <div className="metric">
          <div className="metric-label">Mandatory Sections Present</div>
          <div className="metric-value">{data.mandatory_sections_count}/{data.mandatory_sections_count + data.mandatory_sections_missing.length}</div>
        </div>
        <div className="metric">
          <div className="metric-label">Structure Quality</div>
          <div className="metric-value">{Math.round(data.structure_quality_score)}%</div>
        </div>
      </div>

      <div className="section-details">
        <h4>✓ Present Sections</h4>
        <ul>
          {data.mandatory_sections_present.map(section => (
            <li key={section} className="present-item">{section}</li>
          ))}
        </ul>

        {data.mandatory_sections_missing.length > 0 && (
          <>
            <h4>✗ Missing Sections</h4>
            <ul>
              {data.mandatory_sections_missing.map(section => (
                <li key={section} className="missing-item">{section}</li>
              ))}
            </ul>
          </>
        )}

        {data.optional_sections_found.length > 0 && (
          <>
            <h4>+ Optional Sections Found</h4>
            <ul>
              {data.optional_sections_found.map(section => (
                <li key={section} className="optional-item">{section}</li>
              ))}
            </ul>
          </>
        )}
      </div>

      <p className="findings">{data.detailed_findings}</p>
    </div>
  );

  const renderPhase2 = (data) => (
    <div className="phase-details">
      <div className="quality-dimensions">
        {Object.entries(data.quality_dimensions).map(([key, value]) => (
          <div key={key} className="quality-item">
            <div className="quality-label">{key.charAt(0).toUpperCase() + key.slice(1)}</div>
            <ScoreBadge score={value} />
          </div>
        ))}
      </div>
      <div className="overall-quality">
        <h4>Overall Quality Score</h4>
        <ScoreBadge score={data.overall_quality_score} />
      </div>
    </div>
  );

  const renderPhase3 = (data) => (
    <div className="phase-details">
      <div className="llm-confidence">
        <h4>AI Generation Confidence</h4>
        <ScoreBadge score={data.confidence} />
        <p>{data.is_likely_ai_generated ? '⚠️ Likely AI-generated content detected' : '✓ Appears to be human-written'}</p>
      </div>

      {data.ai_indicators.length > 0 && (
        <div className="ai-indicators">
          <h4>AI-like Indicators Found ({data.ai_indicators.length})</h4>
          <ul>
            {data.ai_indicators.map((indicator, idx) => (
              <li key={idx}>{indicator}</li>
            ))}
          </ul>
        </div>
      )}

      <p className="llm-analysis">{data.analysis_text}</p>
    </div>
  );

  const renderPhase4 = (improvements) => (
    <div className="phase-details">
      <div className="improvements-list">
        {improvements.map((sugg, idx) => (
          <div key={idx} className={`suggestion-item ${sugg.priority.toLowerCase()}`}>
            <div className="suggestion-priority">{sugg.priority} Priority</div>
            <h4>{sugg.category}</h4>
            <p>{sugg.description}</p>
            <div className="suggestion-box">
              <strong>Example:</strong> {sugg.specific_example}
            </div>
            <div className="guidance">
              <strong>Guidance:</strong> {sugg.implementation_guidance}
            </div>
          </div>
        ))}
      </div>
    </div>
  );

  const renderPhase5 = (suggestions) => (
    <div className="phase-details">
      <div className="enterprise-suggestions">
        {suggestions.map((sugg, idx) => (
          <div key={idx} className="enterprise-card">
            <div className="enterprise-header">
              <h4>{sugg.category}</h4>
              <span className={`priority-badge ${sugg.priority.toLowerCase()}`}>{sugg.priority}</span>
            </div>
            <p className="description">{sugg.description}</p>
            <div className="details">
              <p><strong>Rationale:</strong> {sugg.rationale}</p>
              <p><strong>Implementation:</strong> {sugg.implementation_guidance}</p>
              <p><strong>Impact:</strong> {sugg.impact_assessment}</p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );

  const renderPhase6 = (patterns) => (
    <div className="phase-details">
      <div className="patterns-grid">
        {patterns.map((pattern, idx) => (
          <div key={idx} className="pattern-card">
            <h4>{pattern.name}</h4>
            <p className="category">Category: {pattern.category}</p>
            <p className="applicability">Applicability: {pattern.applicability}</p>
            
            <div className="pattern-section">
              <strong>Benefits:</strong>
              <ul>
                {pattern.benefits.map((benefit, bidx) => (
                  <li key={bidx}>{benefit}</li>
                ))}
              </ul>
            </div>

            <div className="pattern-section">
              <strong>Considerations:</strong>
              <ul>
                {pattern.considerations.map((consideration, cidx) => (
                  <li key={cidx}>{consideration}</li>
                ))}
              </ul>
            </div>

            <p className="hints"><strong>Implementation Hints:</strong> {pattern.implementation_hints}</p>
          </div>
        ))}
      </div>
    </div>
  );

  const renderPhase7 = (debts) => (
    <div className="phase-details">
      <div className="debt-list">
        {debts.map((debt, idx) => (
          <div key={idx} className={`debt-item ${debt.severity.toLowerCase()}`}>
            <div className="debt-header">
              <h4>{debt.type} Debt</h4>
              <span className="severity">{debt.severity}</span>
            </div>
            <p className="description">{debt.description}</p>
            <p><strong>Impact:</strong> {debt.impact}</p>
            <p><strong>Remediation:</strong> {debt.remediation_strategy}</p>
            <p><strong>Effort:</strong> {debt.estimated_effort}</p>
          </div>
        ))}
      </div>
    </div>
  );

  const renderPhase8 = (maturity) => (
    <div className="phase-details">
      <div className="maturity-overview">
        <div className="maturity-main">
          <h4>Overall Maturity Score</h4>
          <ScoreBadge score={maturity.overall_maturity_score} />
          <p className="maturity-level">Level: <strong>{maturity.maturity_level}</strong></p>
        </div>

        <div className="maturity-dimensions">
          <h4>Dimensions</h4>
          <div className="dimension-item">
            <span>Documentation Quality</span>
            <ScoreBadge score={maturity.documentation_quality} />
          </div>
          <div className="dimension-item">
            <span>Decision Rationale</span>
            <ScoreBadge score={maturity.decision_rationale} />
          </div>
          <div className="dimension-item">
            <span>Risk Assessment</span>
            <ScoreBadge score={maturity.risk_assessment} />
          </div>
          <div className="dimension-item">
            <span>Alternative Analysis</span>
            <ScoreBadge score={maturity.alternative_analysis} />
          </div>
        </div>
      </div>

      <div className="improvement-pathway">
        <h4>Improvement Pathway</h4>
        <ol>
          {maturity.improvement_pathway.map((step, idx) => (
            <li key={idx}>{step}</li>
          ))}
        </ol>
      </div>
    </div>
  );

  const renderPhase9 = (compliance) => (
    <div className="phase-details">
      <div className="compliance-summary">
        <div className="compliance-metric">
          <h4>Compliance Score</h4>
          <ScoreBadge score={compliance.compliance_percentage} />
        </div>
        <div className="compliance-stats">
          <p>Present: <strong>{compliance.present_topics_count}</strong> / {compliance.total_topics}</p>
          <p>Missing: <strong>{compliance.missing_topics_count}</strong> / {compliance.total_topics}</p>
        </div>
      </div>

      {compliance.priority_improvements.length > 0 && (
        <div className="priority-improvements">
          <h4>🎯 Priority Improvements</h4>
          <ol>
            {compliance.priority_improvements.map((improvement, idx) => (
              <li key={idx}>{improvement}</li>
            ))}
          </ol>
        </div>
      )}

      <div className="compliance-topics">
        <h4>Topic Status</h4>
        <div className="topics-list">
          {compliance.topics.map((topic, idx) => (
            <div key={idx} className="topic-row">
              <span className="topic-name">{topic.topic_name}</span>
              <span className={`status-badge ${topic.status.toLowerCase()}`}>{topic.status}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );

  const renderPhaseContent = (phaseKey, phaseData) => {
    switch (phaseKey) {
      case 'phase_1_structural_analysis':
        return renderPhase1(phaseData);
      case 'phase_2_quality_assessment':
        return renderPhase2(phaseData);
      case 'phase_3_llm_detection':
        return renderPhase3(phaseData);
      case 'phase_4_improvements':
        return renderPhase4(phaseData);
      case 'phase_5_enterprise':
        return renderPhase5(phaseData);
      case 'phase_6_design_patterns':
        return renderPhase6(phaseData);
      case 'phase_7_technical_debt':
        return renderPhase7(phaseData);
      case 'phase_8_maturity':
        return renderPhase8(phaseData);
      case 'phase_9_compliance':
        return renderPhase9(phaseData);
      default:
        return null;
    }
  };

  return (
    <div className="analysis-results">
      <div className="phases-container">
        {phases.map((phase) => (
          <div key={phase.key} className="phase-card">
            <button
              className="phase-header"
              onClick={() => setExpandedPhase(expandedPhase === phase.key ? null : phase.key)}
            >
              <span className="phase-title">{phase.title}</span>
              <span className="expand-icon">{expandedPhase === phase.key ? '▼' : '▶'}</span>
            </button>

            {expandedPhase === phase.key && (
              <div className="phase-content">
                {renderPhaseContent(phase.key, data[phase.key])}
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}
