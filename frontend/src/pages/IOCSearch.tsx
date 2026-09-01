import { useState, useEffect } from 'react'
import { Search, Target, Activity, Network } from 'lucide-react'
import { useNavigate } from 'react-router-dom'

export default function IOCSearch() {
  const [query, setQuery] = useState('sbi.kyc.update@ybl')
  const [result, setResult] = useState<any>(null)
  const [loading, setLoading] = useState(false)
  const navigate = useNavigate()

  useEffect(() => {
    handleSearch()
  }, [])

  const handleSearch = async (e?: React.FormEvent) => {
    if (e) e.preventDefault()
    if (!query.trim()) return

    setLoading(true)
    try {
      const res = await fetch(`/api/v1/cti/ioc-search?query=${encodeURIComponent(query.trim())}`)
      if (res.ok) {
        const data = await res.json()
        setResult(data)
      }
    } catch (err) {
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="animate-fade-in" style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
      <div className="section-header">
        <div>
          <h2 style={{ fontSize: '1.25rem', fontWeight: 700, display: 'flex', alignItems: 'center', gap: '8px' }}>
            <Search style={{ color: 'var(--primary-400)' }} /> Unified Global IOC Search Console
          </h2>
          <div className="section-header__subtitle">
            Cross-reference Indicators of Compromise (IPs, URLs, Domains, File Hashes, Emails, UPIs, Phone numbers) across database records and CTI feeds
          </div>
        </div>
      </div>

      {/* Search Input Box */}
      <div className="glass-card">
        <form onSubmit={handleSearch} style={{ display: 'flex', gap: '12px' }}>
          <div style={{ flex: 1, position: 'relative' }}>
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Search by IP, URL, UPI handle, Phone number, Email, or Hash..."
              style={{
                width: '100%',
                padding: '12px 16px 12px 42px',
                borderRadius: 'var(--radius-md)',
                background: 'var(--bg-primary)',
                border: '1px solid var(--border-default)',
                color: 'white',
                fontSize: '0.95rem',
                outline: 'none',
              }}
            />
            <Search size={18} style={{ position: 'absolute', left: '14px', top: '50%', transform: 'translateY(-50%)', color: 'var(--text-muted)' }} />
          </div>

          <button
            type="submit"
            disabled={loading}
            style={{
              padding: '12px 24px',
              borderRadius: 'var(--radius-md)',
              background: 'linear-gradient(135deg, var(--primary-500), var(--accent-500))',
              border: 'none',
              color: 'white',
              fontWeight: 600,
              cursor: 'pointer',
            }}
          >
            {loading ? 'Searching CTI...' : 'Search Threat Intel'}
          </button>
        </form>

        <div style={{ display: 'flex', gap: '8px', marginTop: '12px', fontSize: '0.75rem', color: 'var(--text-muted)', alignItems: 'center' }}>
          <span>Try quick queries:</span>
          <button type="button" onClick={() => { setQuery('sbi.kyc.update@ybl'); handleSearch(); }} className="badge badge--info" style={{ cursor: 'pointer', border: 'none' }}>UPI: sbi.kyc.update@ybl</button>
          <button type="button" onClick={() => { setQuery('+919876543210'); handleSearch(); }} className="badge badge--info" style={{ cursor: 'pointer', border: 'none' }}>Phone: +919876543210</button>
          <button type="button" onClick={() => { setQuery('https://sbi-kyc-update-portal.xyz/verify'); handleSearch(); }} className="badge badge--danger" style={{ cursor: 'pointer', border: 'none' }}>URL: sbi-kyc-update-portal.xyz</button>
        </div>
      </div>

      {/* Result Card */}
      {result && (
        <div className="glass-card animate-fade-in" style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', borderBottom: '1px solid var(--border-subtle)', paddingBottom: '16px' }}>
            <div>
              <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
                {result.ioc_type} INDICATOR
              </div>
              <div className="mono" style={{ fontSize: '1.25rem', fontWeight: 700, color: 'var(--text-primary)', marginTop: '2px' }}>
                {result.ioc_value}
              </div>
            </div>

            <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
              <div style={{ textAlign: 'right' }}>
                <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>Threat Score</div>
                <div style={{ fontSize: '1.5rem', fontWeight: 700, color: result.threat_score >= 80 ? 'var(--danger-400)' : 'var(--warning-400)' }}>
                  {result.threat_score}/100
                </div>
              </div>

              <span className={`badge ${result.verdict === 'MALICIOUS' ? 'badge--danger' : 'badge--warning'}`} style={{ fontSize: '0.9rem', padding: '8px 16px' }}>
                {result.verdict}
              </span>
            </div>
          </div>

          <div className="grid-2">
            <div style={{ padding: '14px', background: 'var(--bg-primary)', borderRadius: 'var(--radius-sm)', display: 'flex', flexDirection: 'column', gap: '8px' }}>
              <div style={{ fontWeight: 600, fontSize: '0.85rem', color: 'var(--text-secondary)', display: 'flex', alignItems: 'center', gap: '6px' }}>
                <Target size={16} /> Linked Campaign Clusters
              </div>
              <div style={{ display: 'flex', gap: '6px', flexWrap: 'wrap' }}>
                {result.associated_campaign_ids.map((cid: string) => (
                  <span key={cid} className="badge badge--danger mono">{cid}</span>
                ))}
              </div>
            </div>

            <div style={{ padding: '14px', background: 'var(--bg-primary)', borderRadius: 'var(--radius-sm)', display: 'flex', flexDirection: 'column', gap: '8px' }}>
              <div style={{ fontWeight: 600, fontSize: '0.85rem', color: 'var(--text-secondary)', display: 'flex', alignItems: 'center', gap: '6px' }}>
                <Activity size={16} /> MITRE ATT&CK Technique Mapping
              </div>
              <div style={{ display: 'flex', gap: '6px', flexWrap: 'wrap' }}>
                {result.mitre_techniques.map((t: string) => (
                  <span key={t} className="badge badge--info mono">{t}</span>
                ))}
              </div>
            </div>
          </div>

          <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '12px' }}>
            <button
              onClick={() => navigate('/graph')}
              style={{
                padding: '10px 18px',
                borderRadius: 'var(--radius-sm)',
                background: 'var(--primary-glow)',
                border: '1px solid rgba(6,182,212,0.3)',
                color: 'var(--primary-300)',
                fontWeight: 600,
                cursor: 'pointer',
                display: 'flex',
                alignItems: 'center',
                gap: '6px',
              }}
            >
              <Network size={16} /> Multi-Hop Pivot to Campaign Graph
            </button>
          </div>
        </div>
      )}
    </div>
  )
}
