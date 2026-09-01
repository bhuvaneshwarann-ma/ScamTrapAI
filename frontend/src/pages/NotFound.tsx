import { useNavigate } from 'react-router-dom'
import { ShieldAlert, ArrowLeft } from 'lucide-react'

export default function NotFound() {
  const navigate = useNavigate()

  return (
    <div className="empty-state animate-fade-in" style={{ minHeight: '60vh' }}>
      <div style={{
        width: '80px',
        height: '80px',
        borderRadius: 'var(--radius-xl)',
        background: 'var(--danger-glow)',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        marginBottom: '24px',
      }}>
        <ShieldAlert size={40} style={{ color: 'var(--danger-400)' }} />
      </div>

      <h2 style={{
        fontSize: '3rem',
        fontWeight: 800,
        fontFamily: "'JetBrains Mono', monospace",
        background: 'linear-gradient(135deg, var(--danger-400), var(--warning-400))',
        WebkitBackgroundClip: 'text',
        WebkitTextFillColor: 'transparent',
        marginBottom: '8px',
      }}>
        404
      </h2>

      <div className="empty-state__title" style={{ fontSize: '1.2rem' }}>
        Sector Not Found
      </div>
      <div className="empty-state__text" style={{ marginBottom: '24px' }}>
        The investigation sector you're looking for doesn't exist or hasn't been
        activated yet. Some modules are still in development.
      </div>

      <button
        onClick={() => navigate('/')}
        style={{
          display: 'flex',
          alignItems: 'center',
          gap: '8px',
          padding: '10px 20px',
          borderRadius: 'var(--radius-md)',
          background: 'var(--primary-glow)',
          border: '1px solid rgba(6, 182, 212, 0.2)',
          color: 'var(--primary-300)',
          fontSize: '0.875rem',
          fontWeight: 600,
          cursor: 'pointer',
          transition: 'all var(--transition-fast)',
        }}
        onMouseEnter={(e) => {
          e.currentTarget.style.background = 'var(--primary-glow-strong)'
          e.currentTarget.style.borderColor = 'rgba(6, 182, 212, 0.4)'
        }}
        onMouseLeave={(e) => {
          e.currentTarget.style.background = 'var(--primary-glow)'
          e.currentTarget.style.borderColor = 'rgba(6, 182, 212, 0.2)'
        }}
      >
        <ArrowLeft size={16} />
        Return to Dashboard
      </button>
    </div>
  )
}
