import React from 'react';
import { ShieldAlert, AlertTriangle, Code, Globe, Server, CheckCircle2 } from 'lucide-react';

const SEVERITY_MAP = {
  HIGH: { cls: 'error', label: 'High Severity' },
  MEDIUM: { cls: 'warning', label: 'Medium Severity' },
  LOW: { cls: 'success', label: 'Low Severity' },
};

const AGENT_ICON = {
  'AI Security Agent': <Code size={16} />,
  'API Security Agent': <Globe size={16} />,
  'Code Review Agent': <ShieldAlert size={16} />,
  'Infrastructure Agent': <Server size={16} />,
};

export default function LiveResultsPanel({ data }) {
  if (!data) return null;

  const { overall_score, findings, target_url } = data;

  const scoreColor =
    overall_score >= 80
      ? 'var(--success)'
      : overall_score >= 60
      ? 'var(--warning)'
      : 'var(--error)';

  const scoreLabel =
    overall_score >= 80 ? 'Good' : overall_score >= 60 ? 'Fair' : 'Poor';

  return (
    <div className="animate-fade-in">
      {/* Header Stats */}
      <div className="dashboard-grid" style={{ marginBottom: '2rem' }}>
        <div className="glass-card">
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
            <div className="text-muted">Overall Security Score</div>
            <ShieldAlert size={22} color={scoreColor} />
          </div>
          <div className="stat-value" style={{ color: scoreColor }}>
            {overall_score}
            <span style={{ fontSize: '1rem', color: 'var(--text-secondary)' }}>/100</span>
          </div>
          <span className={`badge ${SEVERITY_MAP[overall_score >= 80 ? 'LOW' : overall_score >= 60 ? 'MEDIUM' : 'HIGH'].cls}`} style={{ marginTop: '1rem', display: 'inline-block' }}>
            {scoreLabel} Posture
          </span>
        </div>

        <div className="glass-card">
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
            <div className="text-muted">Target Application</div>
            <Globe size={22} color="var(--accent-secondary)" />
          </div>
          <div style={{ marginTop: '0.75rem', fontWeight: 600, wordBreak: 'break-all', color: 'var(--accent-primary)', fontSize: '0.95rem' }}>
            {target_url}
          </div>
          <span className="badge success" style={{ marginTop: '1rem', display: 'inline-block' }}>
            <CheckCircle2 size={12} style={{ marginRight: '0.25rem' }} />
            Assessment Complete
          </span>
        </div>

        <div className="glass-card">
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
            <div className="text-muted">Vulnerabilities Found</div>
            <AlertTriangle size={22} color="var(--error)" />
          </div>
          <div className="stat-value">{findings?.length ?? 0}</div>
          <div style={{ marginTop: '1rem', display: 'flex', gap: '0.5rem', flexWrap: 'wrap' }}>
            {['HIGH', 'MEDIUM', 'LOW'].map((sev) => {
              const count = findings?.filter((f) => f.severity === sev).length ?? 0;
              return count > 0 ? (
                <span key={sev} className={`badge ${SEVERITY_MAP[sev].cls}`}>
                  {count} {sev.charAt(0) + sev.slice(1).toLowerCase()}
                </span>
              ) : null;
            })}
          </div>
        </div>
      </div>

      {/* Findings List */}
      <div className="glass-panel" style={{ padding: '2rem' }}>
        <h2 className="heading-2">Detailed Findings</h2>
        <div className="finding-list">
          {findings?.length > 0 ? (
            findings.map((f, i) => {
              const sev = SEVERITY_MAP[f.severity] || SEVERITY_MAP.LOW;
              return (
                <div key={i} className={`finding-item ${sev.cls === 'error' ? 'high' : sev.cls === 'warning' ? 'medium' : 'low'}`}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '0.5rem' }}>
                    <h3 style={{ fontSize: '1rem', fontWeight: 600 }}>{f.description}</h3>
                    <span className={`badge ${sev.cls}`}>{sev.label}</span>
                  </div>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }} className="text-muted">
                    {AGENT_ICON[f.agent_name] ?? <Code size={16} />}
                    {f.agent_name}
                  </div>
                  {f.remediation && (
                    <div style={{ marginTop: '0.5rem', padding: '0.75rem', background: 'rgba(0,0,0,0.2)', borderRadius: '6px', fontSize: '0.9rem', lineHeight: 1.5 }}>
                      <strong style={{ color: 'var(--text-primary)' }}>Remediation: </strong>
                      <span className="text-muted">{f.remediation}</span>
                    </div>
                  )}
                </div>
              );
            })
          ) : (
            <p className="text-muted" style={{ textAlign: 'center', padding: '2rem' }}>
              No findings reported.
            </p>
          )}
        </div>
      </div>
    </div>
  );
}
