import { useEffect, useState } from 'react'
import { Activity } from 'lucide-react'

interface HealthStatus {
  status: string
  app_name: string
  version: string
  uptime_seconds: number
  llm_provider: string
  embedding_provider: string
}

export default function TopBar() {
  const [health, setHealth] = useState<HealthStatus | null>(null)
  const [isOnline, setIsOnline] = useState(false)

  useEffect(() => {
    const checkHealth = async () => {
      try {
        const res = await fetch('/api/v1/health')
        if (res.ok) {
          const data = await res.json()
          setHealth(data)
          setIsOnline(true)
        } else {
          setIsOnline(false)
        }
      } catch {
        setIsOnline(false)
      }
    }

    checkHealth()
    const interval = setInterval(checkHealth, 30000) // Poll every 30s
    return () => clearInterval(interval)
  }, [])

  return (
    <div className="app-topbar">
      <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
        <h1 style={{
          fontSize: '1rem',
          fontWeight: 600,
          color: 'var(--text-primary)',
        }}>
          Dashboard
        </h1>
      </div>

      <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
        {/* LLM Provider */}
        {health && (
          <div className="badge badge--info" style={{ fontSize: '0.65rem' }}>
            LLM: {health.llm_provider.toUpperCase()}
          </div>
        )}

        {/* System Status */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          <Activity size={14} style={{ color: isOnline ? 'var(--success-400)' : 'var(--danger-400)' }} />
          <span className={`badge ${isOnline ? 'badge--online' : 'badge--danger'}`}>
            {isOnline ? 'System Online' : 'Backend Offline'}
          </span>
        </div>
      </div>
    </div>
  )
}
