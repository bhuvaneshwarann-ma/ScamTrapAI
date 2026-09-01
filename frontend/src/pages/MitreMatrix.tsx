import { useEffect, useState } from 'react'
import { Activity, Cpu } from 'lucide-react'

export default function MitreMatrix() {
  const [matrix, setMatrix] = useState<any>(null)

  useEffect(() => {
    fetch('/api/v1/cti/mitre-matrix')
      .then((res) => {
        if (res.ok) return res.json()
        throw new Error('Failed to fetch MITRE matrix')
      })
      .then((data) => setMatrix(data))
      .catch(console.error)
  }, [])

  return (
    <div className="animate-fade-in" style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
      <div className="section-header">
        <div>
          <h2 style={{ fontSize: '1.25rem', fontWeight: 700, display: 'flex', alignItems: 'center', gap: '8px' }}>
            <Activity style={{ color: 'var(--accent-400)' }} /> MITRE ATT&CK TTP Heatmap Matrix
          </h2>
          <div className="section-header__subtitle">
            Automated mapping of Scam DNA tactics to MITRE ATT&CK for Enterprise & Mobile threat frameworks
          </div>
        </div>
      </div>

      {matrix && (
        <div className="grid-stats">
          <div className="stat-card">
            <div className="stat-card__icon stat-card__icon--violet"><Activity size={22} /></div>
            <div className="stat-card__content">
              <div className="stat-card__label">Active Techniques Detected</div>
              <div className="stat-card__value">{matrix.total_techniques_detected}</div>
              <div className="stat-card__sub">Mapped across campaigns</div>
            </div>
          </div>

          <div className="stat-card">
            <div className="stat-card__icon stat-card__icon--amber"><Cpu size={22} /></div>
            <div className="stat-card__content">
              <div className="stat-card__label">Most Frequent Technique</div>
              <div className="stat-card__value" style={{ fontSize: '1.1rem' }}>{matrix.most_frequent_technique}</div>
              <div className="stat-card__sub">Primary vector</div>
            </div>
          </div>
        </div>
      )}

      {/* Heatmap Columns */}
      {matrix && matrix.tactics && (
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))', gap: '16px' }}>
          {Object.entries(matrix.tactics).map(([tacticName, techniques]: any) => (
            <div key={tacticName} className="glass-card" style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
              <div style={{ borderBottom: '1px solid var(--border-subtle)', paddingBottom: '8px' }}>
                <h3 style={{ fontSize: '0.9rem', fontWeight: 700, color: 'var(--primary-300)' }}>{tacticName}</h3>
              </div>

              <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
                {techniques.map((tech: any) => (
                  <div
                    key={tech.technique_id}
                    style={{
                      padding: '12px',
                      borderRadius: 'var(--radius-sm)',
                      background: 'var(--bg-primary)',
                      border: '1px solid rgba(239, 68, 68, 0.3)',
                    }}
                  >
                    <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '4px' }}>
                      <span className="mono badge badge--danger" style={{ fontSize: '0.75rem' }}>{tech.technique_id}</span>
                      <span style={{ fontSize: '0.7rem', color: 'var(--text-muted)' }}>{tech.observed_count} instances</span>
                    </div>
                    <div style={{ fontWeight: 600, fontSize: '0.85rem', color: 'var(--text-primary)', marginBottom: '4px' }}>
                      {tech.name}
                    </div>
                    <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', lineHeight: 1.4 }}>
                      {tech.description}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
