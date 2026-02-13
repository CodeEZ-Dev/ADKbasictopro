import React from 'react';

export default function ScoreBadge({ score }) {
  const getScoreLevel = (score) => {
    if (score >= 80) return 'high';
    if (score >= 60) return 'medium';
    return 'low';
  };

  const getScoreLabel = (score) => {
    if (score >= 80) return 'Excellent';
    if (score >= 60) return 'Good';
    if (score >= 40) return 'Fair';
    return 'Needs Improvement';
  };

  const level = getScoreLevel(score);
  const label = getScoreLabel(score);

  return (
    <div className="score-badge-container">
      <div className={`score-badge ${level}`}>
        {Math.round(score)}%
      </div>
      <p className="score-label">{label}</p>
      <div className="progress-bar">
        <div className="progress-fill" style={{ width: `${score}%` }}></div>
      </div>
    </div>
  );
}
