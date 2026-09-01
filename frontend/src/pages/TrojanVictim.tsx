import { useState, useEffect } from 'react'
import { ShieldAlert, Crosshair, FileText, Zap, Network } from 'lucide-react'

export default function TrojanVictim() {
  const [profile, setProfile] = useState<any>(null)
  const [stressResult, setStressResult] = useState<any>(null)
  const [playbook, setPlaybook] = useState<any>(null)
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    handleGenerateTrojan()
    handleRunStressTest('authority')
    handleLoadPlaybook()
  }, [])

  const handleGenerateTrojan = async () => {
    setLoading(true)
    try {
      const res = await fetch('/api/v1/trojan-victim/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ campaign_id: 'CAMP-01-SBI-KYC', impersonation: 'bank' }),
      })
      if (res.ok) {
        const data = await res.json()
        setProfile(data)
      }
    } catch (e) {
      console.error(e)
    } finally {
      setLoading(false)
    }
  }

  const handleRunStressTest = async (testType: string) => {
    try {
      const res = await fetch('/api/v1/trojan-victim/stress-test', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ test_type: testType }),
      })
      if (res.ok) {
        const data = await res.json()
        setStressResult(data)
      }
    } catch (e) {
      console.error(e)
    }
  }

  const handleLoadPlaybook = async () => {
    try {
      const res = await fetch('/api/v1/playbooks/CAMP-01-SBI-KYC')
      if (res.ok) {
        const data = await res.json()
        setPlaybook(data)
      }
    } catch (e) {
      console.error(e)
    }
  }

  return (
    <div className="animate-fade-in" style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
      <div className="section-header">
        <div>
          <h2 style={{ fontSize: '1.25rem', fontWeight: 700, display: 'flex', alignItems: 'center', gap: '8px' }}>
            <Crosshair style={{ color: 'var(--danger-400)' }} /> "The Trojan Victim" Protocol & Threat Playbooks
          </h2>
          <div className="section-header__subtitle">
            Autonomous Syndicate Reverse-Mapping via Weaponized Honey-Tokens, Adversarial Stress Testing, and Automated SOP Playbook Reverse-Engineering
          </div>
        </div>

        <button
          onClick={handleGenerateTrojan}
          disabled={loading}
          style={{
            padding: '10px 18px',
            borderRadius: 'var(--radius-md)',
            background: 'linear-gradient(135deg, var(--danger-500), var(--warning-500))',
            border: 'none',
            color: 'white',
            fontWeight: 600,
            cursor: 'pointer',
            display: 'flex',
            alignItems: 'center',
            gap: '8px',
          }}
        >
          <Zap size={16} /> Mint Trojan Victim Profile
        </button>
      </div>

      <div className="grid-2">
        {/* Section 1: Trojan Victim Profile & Honey-Token Beacon */}
        <div className="glass-card">
          <h3 style={{ fontSize: '1rem', marginBottom: '12px', display: 'flex', alignItems: 'center', gap: '8px' }}>
            <ShieldAlert size={18} style={{ color: 'var(--danger-400)' }} /> Trojan Victim Profile & Honey-Token Beacon
          </h3>

          {!profile ? (
            <div className="empty-state">
              <Crosshair className="empty-state__icon" />
              <div className="empty-state__title">No Profile Minted</div>
              <div className="empty-state__text">Click "Mint Trojan Victim Profile" to generate synthetic honey-tokens and tracked PDF beacon.</div>
            </div>
          ) : (
            <div style={{ display: 'flex', flexDirection: 'column', gap: '12px', fontSize: '0.85rem' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                <span style={{ color: 'var(--text-muted)' }}>Target Persona Name:</span>
                <span style={{ fontWeight: 600 }}>{profile.persona_name}</span>
              </div>
              <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                <span style={{ color: 'var(--text-muted)' }}>Synthetic Phone (Honey-Token):</span>
                <span className="mono badge badge--info">{profile.synthetic_phone}</span>
              </div>
              <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                <span style={{ color: 'var(--text-muted)' }}>Synthetic Email (Honey-Token):</span>
                <span className="mono badge badge--info">{profile.synthetic_email}</span>
              </div>
              <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                <span style={{ color: 'var(--text-muted)' }}>Weaponized Tracked File:</span>
                <span className="mono badge badge--danger">{profile.beacon_file_name}</span>
              </div>

              <div style={{ padding: '12px', background: 'var(--bg-primary)', borderRadius: 'var(--radius-sm)', border: '1px solid rgba(239, 68, 68, 0.3)' }}>
                <div style={{ fontWeight: 600, color: 'var(--danger-400)', marginBottom: '4px' }}>📡 Beacon Tracking Endpoint:</div>
                <div className="mono" style={{ fontSize: '0.75rem', wordBreak: 'break-all', color: 'var(--text-muted)' }}>
                  {profile.tracking_beacon_url}
                </div>
                <div style={{ fontSize: '0.7rem', color: 'var(--text-dim)', marginTop: '4px' }}>
                  pings back real syndicate IP, device fingerprints, & dark web resold victim lists.
                </div>
              </div>
            </div>
          )}
        </div>

        {/* Section 2: Adversarial Conversational Stress Testing */}
        <div className="glass-card">
          <h3 style={{ fontSize: '1rem', marginBottom: '12px', display: 'flex', alignItems: 'center', gap: '8px' }}>
            <Network size={18} style={{ color: 'var(--warning-400)' }} /> Adversarial Stress-Testing & Hierarchy Mapping
          </h3>

          <p style={{ fontSize: '0.85rem', color: 'var(--text-muted)', marginBottom: '12px' }}>
            Inject calculated conversational stressors into the simulation to test scammer sophistication and discover Tier 2 Supervisors.
          </p>

          <div style={{ display: 'flex', gap: '8px', marginBottom: '16px' }}>
            <button
              onClick={() => handleRunStressTest('authority')}
              className="badge badge--warning"
              style={{ padding: '8px 12px', cursor: 'pointer', border: 'none' }}
            >
              Authority Stress
            </button>
            <button
              onClick={() => handleRunStressTest('technical')}
              className="badge badge--info"
              style={{ padding: '8px 12px', cursor: 'pointer', border: 'none' }}
            >
              Technical Stress
            </button>
            <button
              onClick={() => handleRunStressTest('financial')}
              className="badge badge--online"
              style={{ padding: '8px 12px', cursor: 'pointer', border: 'none' }}
            >
              Financial Stress
            </button>
          </div>

          {stressResult && (
            <div style={{ padding: '12px', background: 'var(--bg-primary)', borderRadius: 'var(--radius-sm)', border: '1px solid var(--border-subtle)', fontSize: '0.8rem' }}>
              <div style={{ fontWeight: 600, color: 'var(--warning-400)', marginBottom: '4px' }}>
                Test: {stressResult.test_type.toUpperCase()} STRESS INJECTION
              </div>
              <div style={{ color: 'var(--text-muted)', marginBottom: '6px' }}>Prompt: "{stressResult.stress_prompt}"</div>
              <div style={{ color: 'var(--text-primary)', marginBottom: '8px' }}>Scammer Reaction: {stressResult.scammer_reaction}</div>
              <div style={{ display: 'flex', gap: '12px', alignItems: 'center' }}>
                <span className={`badge ${stressResult.escalated_to_supervisor ? 'badge--danger' : 'badge--info'}`}>
                  {stressResult.escalated_to_supervisor ? '⚡ Escalated to Tier 2 Supervisor' : 'Handled by Tier 1 Operator'}
                </span>
                <span style={{ color: 'var(--text-muted)' }}>
                  Sophistication Score: <strong style={{ color: 'var(--success-400)' }}>{(stressResult.syndicate_sophistication_score * 100).toFixed(0)}%</strong>
                </span>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Section 3: Reverse-Engineered Threat Playbook (SOP) */}
      <div className="glass-card">
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '16px' }}>
          <div>
            <h3 style={{ fontSize: '1rem', display: 'flex', alignItems: 'center', gap: '8px' }}>
              <FileText size={18} style={{ color: 'var(--primary-400)' }} /> Autonomous Threat Playbook (SOP) Reverse-Engineering
            </h3>
            <div className="section-header__subtitle">Reverse-engineered Standard Operating Procedure (SOP) training manual used by scam syndicate</div>
          </div>
          <button
            onClick={handleLoadPlaybook}
            style={{
              padding: '8px 14px', borderRadius: 'var(--radius-sm)',
              background: 'var(--primary-glow)', border: '1px solid rgba(6,182,212,0.3)',
              color: 'var(--primary-300)', fontWeight: 600, cursor: 'pointer', fontSize: '0.8rem'
            }}
          >
            Generate Playbook
          </button>
        </div>

        {playbook && (
          <div className="grid-2" style={{ gap: '16px', fontSize: '0.85rem' }}>
            <div style={{ padding: '12px', background: 'var(--bg-primary)', borderRadius: 'var(--radius-sm)' }}>
              <div style={{ fontWeight: 600, color: 'var(--primary-300)', marginBottom: '6px' }}>The Opening Hook</div>
              <div style={{ color: 'var(--text-primary)' }}>{playbook.the_hook}</div>
            </div>

            <div style={{ padding: '12px', background: 'var(--bg-primary)', borderRadius: 'var(--radius-sm)' }}>
              <div style={{ fontWeight: 600, color: 'var(--primary-300)', marginBottom: '6px' }}>Scammer Objection Handling Matrix (SOP)</div>
              <div style={{ display: 'flex', flexDirection: 'column', gap: '6px' }}>
                {Object.entries(playbook.objection_handling_matrix).map(([q, ans]: any) => (
                  <div key={q} style={{ fontSize: '0.75rem', padding: '6px', background: 'var(--bg-surface)', borderRadius: 'var(--radius-sm)' }}>
                    <div style={{ color: 'var(--warning-400)' }}>{q}</div>
                    <div style={{ color: 'var(--text-muted)' }}>↳ {ans}</div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}
