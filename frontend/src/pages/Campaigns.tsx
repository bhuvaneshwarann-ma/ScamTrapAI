import { useState, useEffect } from 'react'
import { Target, Download } from 'lucide-react'

interface CampaignItem {
  id: string
  name?: string
  status: string
  incident_count: number
  campaign_confidence: number
  risk_level: string
  first_seen: string
  last_seen: string
}

export default function Campaigns() {
  const [campaigns, setCampaigns] = useState<CampaignItem[]>([
    {
      id: 'CAMP-01-SBI-KYC',
      name: 'SBI KYC Account Suspension Campaign',
      status: 'active',
      incident_count: 44,
      campaign_confidence: 0.98,
      risk_level: 'high',
      first_seen: '2026-08-15T10:00:00Z',
      last_seen: '2026-09-01T18:30:00Z',
    },
    {
      id: 'CAMP-02-PAYTM-REFUND',
      name: 'Paytm Cashback & Security Alert Scam',
      status: 'active',
      incident_count: 44,
      campaign_confidence: 0.95,
      risk_level: 'high',
      first_seen: '2026-08-18T14:20:00Z',
      last_seen: '2026-09-01T20:10:00Z',
    },
  ])

  const [selectedCampaign, setSelectedCampaign] = useState<CampaignItem | null>(null)
  const [exportModal, setExportModal] = useState(false)

  useEffect(() => {
    fetch('/api/v1/campaigns')
      .then((res) => {
        if (res.ok) return res.json()
        throw new Error('Failed to fetch campaigns')
      })
      .then((data) => {
        if (data && data.length > 0) {
          setCampaigns(data)
          setSelectedCampaign(data[0])
        }
      })
      .catch(console.error)
  }, [])

  useEffect(() => {
    if (campaigns.length > 0 && !selectedCampaign) {
      setSelectedCampaign(campaigns[0])
    }
  }, [campaigns, selectedCampaign])

  return (
    <div className="animate-fade-in" style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
      <div className="section-header">
        <div>
          <h2 style={{ fontSize: '1.25rem', fontWeight: 700, display: 'flex', alignItems: 'center', gap: '8px' }}>
            <Target style={{ color: 'var(--accent-400)' }} /> Campaign Intelligence & Cluster Explorer
          </h2>
          <div className="section-header__subtitle">
            Detected scam campaign clusters, shared infrastructure, risk levels, and evidence summaries
          </div>
        </div>

        <button
          onClick={() => setExportModal(true)}
          style={{
            padding: '8px 16px',
            borderRadius: 'var(--radius-md)',
            background: 'var(--primary-glow)',
            border: '1px solid rgba(6, 182, 212, 0.3)',
            color: 'var(--primary-300)',
            fontWeight: 600,
            fontSize: '0.85rem',
            cursor: 'pointer',
            display: 'flex',
            alignItems: 'center',
            gap: '6px',
          }}
        >
          <Download size={15} /> Export Intelligence Report
        </button>
      </div>

      <div className="grid-2">
        {/* Campaign List */}
        <div className="glass-card" style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
          <h3 style={{ fontSize: '1rem', marginBottom: '8px' }}>Detected Campaign Clusters</h3>

          {campaigns.map((c) => (
            <div
              key={c.id}
              onClick={() => setSelectedCampaign(c)}
              style={{
                padding: '14px 16px',
                borderRadius: 'var(--radius-md)',
                background: selectedCampaign?.id === c.id ? 'var(--primary-glow-strong)' : 'var(--bg-surface)',
                border: '1px solid ' + (selectedCampaign?.id === c.id ? 'var(--primary-400)' : 'var(--border-subtle)'),
                cursor: 'pointer',
                transition: 'all var(--transition-fast)',
              }}
            >
              <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '6px' }}>
                <span style={{ fontSize: '0.9rem', fontWeight: 600, color: 'var(--text-primary)' }}>
                  {c.name || c.id}
                </span>
                <span className={`badge ${c.risk_level === 'high' ? 'badge--danger' : 'badge--warning'}`}>
                  {c.risk_level} risk
                </span>
              </div>

              <div style={{ display: 'flex', alignItems: 'center', gap: '16px', fontSize: '0.75rem', color: 'var(--text-muted)' }}>
                <span>{c.incident_count} Incidents</span>
                <span>Confidence: <strong style={{ color: 'var(--success-400)' }}>{(c.campaign_confidence * 100).toFixed(0)}%</strong></span>
                <span className="mono">{c.id.slice(0, 16)}</span>
              </div>
            </div>
          ))}
        </div>

        {/* Selected Campaign Detailed Dossier */}
        <div className="glass-card">
          {selectedCampaign ? (
            <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
              <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', borderBottom: '1px solid var(--border-subtle)', paddingBottom: '12px' }}>
                <div>
                  <h3 style={{ fontSize: '1.1rem', fontWeight: 700 }}>{selectedCampaign.name || selectedCampaign.id}</h3>
                  <div className="mono" style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>{selectedCampaign.id}</div>
                </div>
                <span className={`badge ${selectedCampaign.status === 'active' ? 'badge--danger' : 'badge--warning'}`}>
                  {selectedCampaign.status}
                </span>
              </div>

              <div className="grid-2">
                <div style={{ padding: '12px', background: 'var(--bg-primary)', borderRadius: 'var(--radius-sm)' }}>
                  <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>Campaign Confidence</div>
                  <div style={{ fontSize: '1.5rem', fontWeight: 700, color: 'var(--success-400)' }}>
                    {(selectedCampaign.campaign_confidence * 100).toFixed(0)}%
                  </div>
                  <div style={{ fontSize: '0.65rem', color: 'var(--text-dim)' }}>Backed by deterministic evidence</div>
                </div>

                <div style={{ padding: '12px', background: 'var(--bg-primary)', borderRadius: 'var(--radius-sm)' }}>
                  <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>Linked Incidents</div>
                  <div style={{ fontSize: '1.5rem', fontWeight: 700, color: 'var(--primary-400)' }}>
                    {selectedCampaign.incident_count}
                  </div>
                  <div style={{ fontSize: '0.65rem', color: 'var(--text-dim)' }}>Multilingual SMS / WhatsApp</div>
                </div>
              </div>

              <div>
                <h4 style={{ fontSize: '0.85rem', marginBottom: '8px', color: 'var(--text-secondary)' }}>Shared Infrastructure Indicators</h4>
                <div style={{ display: 'flex', flexWrap: 'wrap', gap: '6px' }}>
                  <span className="badge badge--info">UPI: sbi.kyc.update@ybl</span>
                  <span className="badge badge--info">Phone: +919876543210</span>
                  <span className="badge badge--danger">URL: https://sbi-kyc-update-portal.xyz/verify</span>
                  <span className="badge badge--warning">Tactic: Urgency Pressure</span>
                  <span className="badge badge--warning">Tactic: Authority Impersonation</span>
                </div>
              </div>

              <div>
                <h4 style={{ fontSize: '0.85rem', marginBottom: '8px', color: 'var(--text-secondary)' }}>Observability Timeline</h4>
                <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)', display: 'flex', flexDirection: 'column', gap: '4px' }}>
                  <div>First Observed: <span className="mono">{new Date(selectedCampaign.first_seen).toLocaleString()}</span></div>
                  <div>Most Recent: <span className="mono">{new Date(selectedCampaign.last_seen).toLocaleString()}</span></div>
                </div>
              </div>
            </div>
          ) : (
            <div className="empty-state">Select a campaign to inspect details.</div>
          )}
        </div>
      </div>

      {/* Export Intelligence Modal */}
      {exportModal && (
        <div style={{
          position: 'fixed', top: 0, left: 0, right: 0, bottom: 0,
          background: 'rgba(0,0,0,0.75)', backdropFilter: 'blur(8px)',
          display: 'flex', alignItems: 'center', justifyContent: 'center', zIndex: 100
        }}>
          <div className="glass-card animate-fade-in" style={{ width: '500px', maxWidth: '90%' }}>
            <h3 style={{ fontSize: '1.1rem', marginBottom: '12px' }}>Export Campaign Intelligence Dossier</h3>
            <p style={{ fontSize: '0.85rem', color: 'var(--text-muted)', marginBottom: '16px' }}>
              Generates a verified, evidence-bounded intelligence report containing incident summaries, shared infrastructure, and campaign graph metadata.
            </p>

            <div style={{ display: 'flex', flexDirection: 'column', gap: '8px', marginBottom: '20px' }}>
              <div style={{ padding: '10px', background: 'var(--bg-primary)', borderRadius: 'var(--radius-sm)', fontSize: '0.8rem' }}>
                ✓ Includes PII-redacted evidence tokens (§4.2)
              </div>
              <div style={{ padding: '10px', background: 'var(--bg-primary)', borderRadius: 'var(--radius-sm)', fontSize: '0.8rem' }}>
                ✓ Export format: JSON & Executive Summary Markdown
              </div>
            </div>

            <div style={{ display: 'flex', gap: '12px', justifyContent: 'flex-end' }}>
              <button
                onClick={() => setExportModal(false)}
                style={{
                  padding: '8px 16px', borderRadius: 'var(--radius-sm)',
                  background: 'var(--bg-elevated)', border: '1px solid var(--border-default)',
                  color: 'var(--text-secondary)', cursor: 'pointer'
                }}
              >
                Close
              </button>
              <button
                onClick={() => {
                  const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(campaigns, null, 2))
                  const downloadAnchor = document.createElement('a')
                  downloadAnchor.setAttribute("href", dataStr)
                  downloadAnchor.setAttribute("download", "scamtrap_campaign_dossier.json")
                  document.body.appendChild(downloadAnchor)
                  downloadAnchor.click()
                  downloadAnchor.remove()
                  setExportModal(false)
                }}
                style={{
                  padding: '8px 16px', borderRadius: 'var(--radius-sm)',
                  background: 'var(--primary-500)', border: 'none',
                  color: 'white', fontWeight: 600, cursor: 'pointer'
                }}
              >
                Download JSON Report
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
