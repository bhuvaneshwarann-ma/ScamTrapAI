import { useState } from 'react'
import { Play, ShieldAlert, CheckCircle, Sparkles } from 'lucide-react'

export default function DemoMode() {
  const [step, setStep] = useState(0)

  const steps = [
    {
      title: 'Step 1: View Suspicious Incidents',
      desc: 'Three incidents arrive from different channels (SMS, WhatsApp, Email). On the surface, they look unrelated.',
    },
    {
      title: 'Step 2: Multilingual Scam DNA Extraction',
      desc: 'AI extracts Scam DNA: SBI Bank Impersonation, Urgency Pressure, UPI Payment request.',
    },
    {
      title: 'Step 3: Entity Normalization & Relationship Engine',
      desc: 'Shared UPI (sbi.kyc.update@ybl) and phone (+919876543210) identified across incidents.',
    },
    {
      title: 'Step 4: Emerging Campaign Alert',
      desc: 'Campaign Detector announces: EMERGING CAMPAIGN DETECTED (Confidence: 98%).',
    },
    {
      title: 'Step 5: False Similarity Rejection',
      desc: 'Incident D (legitimate SBI statement) introduced. Hybrid engine rejects false similarity!',
    },
    {
      title: 'Step 6: Evidence-Bounded Copilot Query',
      desc: 'Investigator asks "Why connected?" -> Copilot answers with exact cited evidence.',
    },
  ]

  return (
    <div className="animate-fade-in" style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
      <div className="section-header">
        <div>
          <h2 style={{ fontSize: '1.25rem', fontWeight: 700, display: 'flex', alignItems: 'center', gap: '8px' }}>
            <Sparkles style={{ color: 'var(--primary-400)' }} /> Deterministic Live Presentation Engine
          </h2>
          <div className="section-header__subtitle">3-minute zero-failure hackathon presentation scenario</div>
        </div>
        <button
          onClick={() => setStep((s) => (s + 1) % steps.length)}
          style={{
            padding: '10px 20px',
            borderRadius: 'var(--radius-md)',
            background: 'linear-gradient(135deg, var(--primary-500), var(--accent-500))',
            border: 'none',
            color: 'white',
            fontWeight: 600,
            cursor: 'pointer',
            display: 'flex',
            alignItems: 'center',
            gap: '8px',
          }}
        >
          <Play size={16} /> Advance Demo Step ({step + 1}/{steps.length})
        </button>
      </div>

      <div className="glass-card glass-card--accent">
        <h3 style={{ fontSize: '1.1rem', marginBottom: '8px', color: 'var(--primary-300)' }}>
          {steps[step].title}
        </h3>
        <p style={{ fontSize: '0.9rem', color: 'var(--text-secondary)' }}>
          {steps[step].desc}
        </p>
      </div>

      {step >= 3 && (
        <div style={{ padding: '20px', borderRadius: 'var(--radius-lg)', background: 'var(--danger-glow)', border: '1px solid rgba(239, 68, 68, 0.3)', display: 'flex', alignItems: 'center', gap: '16px' }}>
          <ShieldAlert size={36} style={{ color: 'var(--danger-400)' }} />
          <div>
            <div style={{ fontSize: '1.1rem', fontWeight: 700, color: 'var(--danger-400)' }}>
              ⚠️ EMERGING CAMPAIGN DETECTED
            </div>
            <div style={{ fontSize: '0.85rem', color: 'var(--text-primary)' }}>
              Campaign: SBI KYC Account Suspension Campaign | 3 Incidents Linked | Shared Infrastructure: sbi.kyc.update@ybl | Confidence: 98%
            </div>
          </div>
        </div>
      )}

      {step >= 4 && (
        <div style={{ padding: '20px', borderRadius: 'var(--radius-lg)', background: 'var(--success-glow)', border: '1px solid rgba(16, 185, 129, 0.3)', display: 'flex', alignItems: 'center', gap: '16px' }}>
          <CheckCircle size={36} style={{ color: 'var(--success-400)' }} />
          <div>
            <div style={{ fontSize: '1.1rem', fontWeight: 700, color: 'var(--success-400)' }}>
              ✓ False Similarity Rejected
            </div>
            <div style={{ fontSize: '0.85rem', color: 'var(--text-primary)' }}>
              Incident D (Legitimate Bank Statement) shared keywords 'SBI' but lacked infrastructure corroboration. System correctly prevented false clustering.
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
