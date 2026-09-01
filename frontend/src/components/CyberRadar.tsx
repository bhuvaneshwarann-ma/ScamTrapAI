import { useState, useEffect } from 'react'
import { Radar } from 'lucide-react'

export default function CyberRadar() {
  const [angle, setAngle] = useState(0)

  useEffect(() => {
    const interval = setInterval(() => {
      setAngle((prev) => (prev + 3) % 360)
    }, 30)
    return () => clearInterval(interval)
  }, [])

  return (
    <div className="glass-card glass-card--accent" style={{ position: 'relative', overflow: 'hidden', minHeight: '260px', display: 'flex', flexDirection: 'column', justifyContent: 'space-between' }}>
      {/* Background Radar Circle Canvas */}
      <div style={{ position: 'absolute', top: '50%', left: '50%', transform: 'translate(-50%, -50%)', width: '220px', height: '220px', pointerEvents: 'none' }}>
        {/* Concentric Circles */}
        <div style={{ position: 'absolute', inset: 0, border: '1px solid rgba(0, 242, 254, 0.25)', borderRadius: '50%' }} />
        <div style={{ position: 'absolute', inset: '25%', border: '1px solid rgba(0, 242, 254, 0.2)', borderRadius: '50%' }} />
        <div style={{ position: 'absolute', inset: '50%', border: '1px solid rgba(0, 242, 254, 0.15)', borderRadius: '50%' }} />
        
        {/* Crosshair lines */}
        <div style={{ position: 'absolute', top: '50%', left: 0, right: 0, height: '1px', background: 'rgba(0, 242, 254, 0.15)' }} />
        <div style={{ position: 'absolute', left: '50%', top: 0, bottom: 0, width: '1px', background: 'rgba(0, 242, 254, 0.15)' }} />

        {/* Rotating Radar Sweeper */}
        <div
          style={{
            position: 'absolute',
            inset: 0,
            borderRadius: '50%',
            background: 'conic-gradient(from ' + angle + 'deg at 50% 50%, rgba(0, 242, 254, 0.3) 0deg, transparent 60deg, transparent 360deg)',
          }}
        />

        {/* Radar Threat Ping Blips */}
        <div style={{ position: 'absolute', top: '25%', left: '65%', width: '8px', height: '8px', borderRadius: '50%', background: '#ff007f', boxShadow: '0 0 12px #ff007f', animation: 'pulse 1.5s infinite' }} />
        <div style={{ position: 'absolute', top: '70%', left: '30%', width: '8px', height: '8px', borderRadius: '50%', background: '#fbbf24', boxShadow: '0 0 12px #fbbf24', animation: 'pulse 2s infinite' }} />
        <div style={{ position: 'absolute', top: '40%', left: '20%', width: '8px', height: '8px', borderRadius: '50%', background: '#ff007f', boxShadow: '0 0 12px #ff007f', animation: 'pulse 1.2s infinite' }} />
      </div>

      {/* Foreground Header */}
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', zIndex: 2 }}>
        <div>
          <h3 style={{ fontSize: '1.1rem', fontWeight: 800, display: 'flex', alignItems: 'center', gap: '8px', color: 'white' }}>
            <Radar style={{ color: '#00f2fe' }} /> Global Cyber Threat Radar & Syndicate Sweeper
          </h3>
          <div className="section-header__subtitle">Real-time telemetry tracking active scam call centers, malicious UPI vectors, & Trojan Victim pings</div>
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          <span className="pulse-dot" />
          <span className="badge badge--danger mono">5 ACTIVE CLUSTERS DETECTED</span>
        </div>
      </div>

      {/* Stats overlay */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '12px', zIndex: 2, marginTop: 'auto', background: 'rgba(10, 11, 20, 0.85)', padding: '12px 16px', borderRadius: 'var(--radius-md)', backdropFilter: 'blur(10px)', border: '1px solid rgba(255,255,255,0.08)' }}>
        <div>
          <div style={{ fontSize: '0.7rem', color: 'var(--text-dim)' }}>Radar Sweep Latency</div>
          <div className="mono" style={{ fontSize: '1rem', fontWeight: 700, color: '#00ff9d' }}>12ms</div>
        </div>
        <div>
          <div style={{ fontSize: '0.7rem', color: 'var(--text-dim)' }}>Active Call Center IPs</div>
          <div className="mono" style={{ fontSize: '1rem', fontWeight: 700, color: '#00f2fe' }}>18 nodes</div>
        </div>
        <div>
          <div style={{ fontSize: '0.7rem', color: 'var(--text-dim)' }}>Honey-Token Beacons</div>
          <div className="mono" style={{ fontSize: '1rem', fontWeight: 700, color: '#ff007f' }}>3 armed</div>
        </div>
        <div>
          <div style={{ fontSize: '0.7rem', color: 'var(--text-dim)' }}>Syndicate Risk Level</div>
          <div className="mono" style={{ fontSize: '1rem', fontWeight: 700, color: '#fbbf24' }}>HIGH (88/100)</div>
        </div>
      </div>
    </div>
  )
}
