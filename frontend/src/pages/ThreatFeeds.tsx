import { useEffect, useState } from 'react'
import { Radio, ShieldAlert, RefreshCw } from 'lucide-react'

export default function ThreatFeeds() {
  const [feeds, setFeeds] = useState<any[]>([])

  useEffect(() => {
    fetch('/api/v1/cti/threat-feeds')
      .then((res) => {
        if (res.ok) return res.json()
        throw new Error('Failed to fetch threat feeds')
      })
      .then((data) => setFeeds(data))
      .catch(console.error)
  }, [])

  return (
    <div className="animate-fade-in" style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
      <div className="section-header">
        <div>
          <h2 style={{ fontSize: '1.25rem', fontWeight: 700, display: 'flex', alignItems: 'center', gap: '8px' }}>
            <Radio style={{ color: 'var(--danger-400)' }} /> Real-Time CTI Threat Feed & OSINT Monitoring Hub
          </h2>
          <div className="section-header__subtitle">
            Aggregated Cyber Threat Intelligence feeds, dark web leaks, phishing domain blocklists, and OSINT alerts
          </div>
        </div>

        <button
          onClick={() => {
            fetch('/api/v1/cti/threat-feeds')
              .then((res) => res.json())
              .then((data) => setFeeds(data))
          }}
          style={{
            padding: '8px 16px',
            borderRadius: 'var(--radius-md)',
            background: 'var(--bg-elevated)',
            border: '1px solid var(--border-default)',
            color: 'var(--text-secondary)',
            fontWeight: 600,
            fontSize: '0.85rem',
            cursor: 'pointer',
            display: 'flex',
            alignItems: 'center',
            gap: '6px',
          }}
        >
          <RefreshCw size={14} /> Refresh Feeds
        </button>
      </div>

      <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
        {feeds.map((feed) => (
          <div
            key={feed.feed_id}
            className="glass-card"
            style={{
              padding: '16px 20px',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'space-between',
              gap: '16px',
            }}
          >
            <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
              <div
                style={{
                  width: '40px',
                  height: '40px',
                  borderRadius: 'var(--radius-md)',
                  background: feed.threat_level === 'CRITICAL' ? 'rgba(239,68,68,0.2)' : 'rgba(245,158,11,0.2)',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                }}
              >
                <ShieldAlert size={20} color={feed.threat_level === 'CRITICAL' ? 'var(--danger-400)' : 'var(--warning-400)'} />
              </div>

              <div>
                <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '4px' }}>
                  <h3 style={{ fontSize: '0.95rem', fontWeight: 600 }}>{feed.title}</h3>
                  <span className={`badge ${feed.threat_level === 'CRITICAL' ? 'badge--danger' : 'badge--warning'}`}>
                    {feed.threat_level}
                  </span>
                </div>

                <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)', marginBottom: '4px' }}>
                  {feed.description}
                </div>

                <div style={{ fontSize: '0.75rem', color: 'var(--text-dim)', display: 'flex', gap: '16px' }}>
                  <span>Source: <strong style={{ color: 'var(--primary-300)' }}>{feed.source}</strong></span>
                  <span>Indicator: <strong className="mono" style={{ color: 'var(--danger-400)' }}>{feed.indicator}</strong></span>
                  <span>Time: <strong className="mono">{new Date(feed.timestamp).toLocaleString()}</strong></span>
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
