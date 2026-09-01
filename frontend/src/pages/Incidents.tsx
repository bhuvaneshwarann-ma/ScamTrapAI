import React, { useState } from 'react'
import { FileSearch, Cpu, Lock } from 'lucide-react'

export default function Incidents() {
  const [rawText, setRawText] = useState('')
  const [channel, setChannel] = useState('sms')
  const [analyzed, setAnalyzed] = useState<any>(null)
  const [loading, setLoading] = useState(false)

  const handleIngest = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!rawText.trim()) return

    setLoading(true)
    try {
      const res = await fetch('/api/v1/incidents', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ raw_text: rawText, channel }),
      })
      if (res.ok) {
        const data = await res.json()
        setAnalyzed(data)
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
          <h2 style={{ fontSize: '1.25rem', fontWeight: 700 }}>Incident Ingestion & Scam DNA Analyzer</h2>
          <div className="section-header__subtitle">Submit raw multilingual incident text for closed-taxonomy extraction</div>
        </div>
      </div>

      <div className="grid-2">
        {/* Ingestion Form */}
        <div className="glass-card">
          <h3 style={{ fontSize: '1rem', marginBottom: '16px', display: 'flex', alignItems: 'center', gap: '8px' }}>
            <FileSearch size={18} style={{ color: 'var(--primary-400)' }} /> Ingest Raw Transcript
          </h3>

          <form onSubmit={handleIngest} style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
            <div>
              <label style={{ display: 'block', fontSize: '0.8rem', color: 'var(--text-muted)', marginBottom: '6px' }}>
                Channel
              </label>
              <select
                value={channel}
                onChange={(e) => setChannel(e.target.value)}
                style={{
                  width: '100%',
                  padding: '8px 12px',
                  borderRadius: 'var(--radius-sm)',
                  background: 'var(--bg-primary)',
                  border: '1px solid var(--border-default)',
                  color: 'var(--text-primary)',
                }}
              >
                <option value="sms">SMS</option>
                <option value="whatsapp">WhatsApp</option>
                <option value="email">Email</option>
                <option value="voice">Voice Transcript</option>
              </select>
            </div>

            <div>
              <label style={{ display: 'block', fontSize: '0.8rem', color: 'var(--text-muted)', marginBottom: '6px' }}>
                Pre-loaded Multilingual Test Samples (1-Click Test)
              </label>
              <div style={{ display: 'flex', flexWrap: 'wrap', gap: '6px', marginBottom: '12px' }}>
                <button
                  type="button"
                  onClick={() => setRawText('SBI ALERT: Your netbanking blocked. Update PAN card immediately: https://sbi-kyc-update-portal.xyz/verify. Pay Rs 1 fee to sbi.kyc.update@ybl. Call +919876543210.')}
                  className="badge badge--info"
                  style={{ cursor: 'pointer', border: 'none' }}
                >
                  English SBI KYC
                </button>
                <button
                  type="button"
                  onClick={() => setRawText('வணக்கம், உங்கள் SBI கணக்கு முடக்கப்படும். உடனடியாக KYC புதுப்பிக்கவும்: https://sbi-kyc-update-portal.xyz/verify. தொடர்புக்கு: +919876543210.')}
                  className="badge badge--warning"
                  style={{ cursor: 'pointer', border: 'none' }}
                >
                  Tamil SBI KYC
                </button>
                <button
                  type="button"
                  onClick={() => setRawText('प्रिय ग्राहक, आपका SBI बैंक खाता ब्लॉक हो गया है। तुरंत KYC अपडेट करें https://sbi-kyc-update-portal.xyz/verify या कॉल करें +919876543210।')}
                  className="badge badge--warning"
                  style={{ cursor: 'pointer', border: 'none' }}
                >
                  Hindi SBI KYC
                </button>
                <button
                  type="button"
                  onClick={() => setRawText('FedEx Alert: Parcel AWB-8821 held by Mumbai Customs containing illegal goods. Pay clearance fee Rs 14,500 to customs.duty.tax@oksbi or call +919000111222.')}
                  className="badge badge--danger"
                  style={{ cursor: 'pointer', border: 'none' }}
                >
                  FedEx Customs
                </button>
                <button
                  type="button"
                  onClick={() => setRawText('Dear customer, your monthly SBI bank statement for August is ready. View it safely in your YONO app. SBI will never ask for your OTP.')}
                  className="badge badge--online"
                  style={{ cursor: 'pointer', border: 'none' }}
                >
                  Negative Control (Legit)
                </button>
              </div>

              <label style={{ display: 'block', fontSize: '0.8rem', color: 'var(--text-muted)', marginBottom: '6px' }}>
                Transcript / Message Text (Multilingual / Untrusted Input)
              </label>
              <textarea
                rows={5}
                value={rawText}
                onChange={(e) => setRawText(e.target.value)}
                placeholder="e.g. SBI ALERT: Your account is blocked. Update PAN card at https://sbi-kyc.xyz or pay Rs 1 to sbi@ybl..."
                style={{
                  width: '100%',
                  padding: '12px',
                  borderRadius: 'var(--radius-md)',
                  background: 'var(--bg-primary)',
                  border: '1px solid var(--border-default)',
                  color: 'var(--text-primary)',
                  fontFamily: 'inherit',
                  resize: 'vertical',
                }}
              />
            </div>

            <button
              type="submit"
              disabled={loading}
              style={{
                padding: '10px 18px',
                borderRadius: 'var(--radius-md)',
                background: 'linear-gradient(135deg, var(--primary-500), var(--accent-500))',
                border: 'none',
                color: 'white',
                fontWeight: 600,
                cursor: 'pointer',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                gap: '8px',
              }}
            >
              {loading ? 'Extracting Scam DNA...' : 'Analyze Incident'}
            </button>
          </form>
        </div>

        {/* Extraction Output */}
        <div className="glass-card">
          <h3 style={{ fontSize: '1rem', marginBottom: '16px', display: 'flex', alignItems: 'center', gap: '8px' }}>
            <Cpu size={18} style={{ color: 'var(--accent-400)' }} /> Extracted Scam DNA Fingerprint
          </h3>

          {!analyzed ? (
            <div className="empty-state">
              <FileSearch className="empty-state__icon" />
              <div className="empty-state__title">No Incident Loaded</div>
              <div className="empty-state__text">Submit a transcript to see structured Scam DNA extraction.</div>
            </div>
          ) : (
            <div style={{ display: 'flex', flexDirection: 'column', gap: '12px', fontSize: '0.85rem' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                <span style={{ color: 'var(--text-muted)' }}>Incident ID:</span>
                <span className="mono">{analyzed.id}</span>
              </div>
              <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                <span style={{ color: 'var(--text-muted)' }}>Target Impersonation:</span>
                <span className="badge badge--info">{analyzed.scam_dna?.impersonation_target}</span>
              </div>
              <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                <span style={{ color: 'var(--text-muted)' }}>Payment Method:</span>
                <span className="badge badge--warning">{analyzed.scam_dna?.payment_method}</span>
              </div>
              <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                <span style={{ color: 'var(--text-muted)' }}>Urgency Level:</span>
                <span>{((analyzed.scam_dna?.urgency || 0) * 100).toFixed(0)}%</span>
              </div>
              <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                <span style={{ color: 'var(--text-muted)' }}>Fear Pressure:</span>
                <span>{((analyzed.scam_dna?.fear || 0) * 100).toFixed(0)}%</span>
              </div>

              <div style={{ marginTop: '8px' }}>
                <div style={{ color: 'var(--text-muted)', marginBottom: '4px' }}>Extracted Entities:</div>
                <div style={{ display: 'flex', flexWrap: 'wrap', gap: '6px' }}>
                  {analyzed.scam_dna?.phone_numbers?.map((p: string) => (
                    <span key={p} className="badge badge--info">Phone: {p}</span>
                  ))}
                  {analyzed.scam_dna?.upi_ids?.map((u: string) => (
                    <span key={u} className="badge badge--warning">UPI: {u}</span>
                  ))}
                  {analyzed.scam_dna?.urls?.map((url: string) => (
                    <span key={url} className="badge badge--danger">URL: {url}</span>
                  ))}
                </div>
              </div>

              <div style={{ marginTop: '8px', padding: '8px 12px', background: 'var(--bg-primary)', borderRadius: 'var(--radius-sm)', border: '1px solid var(--border-subtle)', display: 'flex', alignItems: 'center', gap: '8px' }}>
                <Lock size={14} style={{ color: 'var(--success-400)' }} />
                <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>
                  All extracted identifiers are PII-hashed in system logs (§4.2).
                </span>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
