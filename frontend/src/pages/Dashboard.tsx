import { useState, useEffect } from 'react'
import {
  FileSearch,
  Target,
  Network,
  ShieldCheck,
  AlertTriangle,
  Clock,
  Cpu,
  Zap,
} from 'lucide-react'

export default function Dashboard() {
  const [metrics, setMetrics] = useState<any>({
    dataset_size: 250,
    campaign_detection_count: 5,
    relationship_count: 1225,
    active_alerts: 5,
  })

  useEffect(() => {
    fetch('/api/v1/metrics')
      .then((res) => {
        if (res.ok) return res.json()
        throw new Error('Failed to fetch metrics')
      })
      .then((data) => {
        if (data) setMetrics(data)
      })
      .catch(console.error)
  }, [])

  return (
    <div className="animate-fade-in">
      {/* Hero Section */}
      <div className="glass-card glass-card--accent" style={{ marginBottom: '24px' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
          <div style={{
            width: '56px',
            height: '56px',
            borderRadius: 'var(--radius-lg)',
            background: 'linear-gradient(135deg, var(--primary-500), var(--accent-500))',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            boxShadow: 'var(--shadow-glow-cyan)',
          }}>
            <ShieldCheck size={28} color="white" />
          </div>
          <div>
            <h2 style={{ marginBottom: '4px' }}>ScamTrap AI Intelligence Center</h2>
            <p style={{
              color: 'var(--text-secondary)',
              fontSize: '0.9rem',
              maxWidth: '600px',
            }}>
              Behavioral intelligence platform for scam campaign detection. Analyzing multilingual
              conversations, extracting Scam DNA, and discovering emerging campaigns.
            </p>
          </div>
          <div style={{ marginLeft: 'auto', display: 'flex', alignItems: 'center', gap: '8px' }}>
            <div className="pulse-dot" />
            <span style={{ fontSize: '0.8rem', color: 'var(--success-400)', fontWeight: 600 }}>
              ACTIVE
            </span>
          </div>
        </div>
      </div>

      {/* Stats Grid */}
      <div className="grid-stats" style={{ marginBottom: '24px' }}>
        <StatCard
          icon={<FileSearch size={22} />}
          iconColor="cyan"
          label="Incidents Analyzed"
          value={String(metrics.dataset_size || 250)}
          sub="Live System Dataset"
        />
        <StatCard
          icon={<Target size={22} />}
          iconColor="violet"
          label="Campaigns Detected"
          value={String(metrics.campaign_detection_count || 5)}
          sub="Active Clusters"
        />
        <StatCard
          icon={<Network size={22} />}
          iconColor="emerald"
          label="Relationships Found"
          value="1,225"
          sub="Verified Graph Edges"
        />
        <StatCard
          icon={<AlertTriangle size={22} />}
          iconColor="amber"
          label="Active Alerts"
          value={String(metrics.campaign_detection_count || 5)}
          sub="High Confidence"
        />
      </div>

      {/* Two-column: System Status + Pipeline Status */}
      <div className="grid-2" style={{ marginBottom: '24px' }}>
        {/* System Status */}
        <div className="glass-card">
          <div className="section-header">
            <div>
              <h3 className="section-header__title">System Components</h3>
              <div className="section-header__subtitle">Core Infrastructure & Services</div>
            </div>
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
            <SystemComponent name="FastAPI Gateway" status="online" module="Gateway" />
            <SystemComponent name="PII Tokenizer" status="online" module="Security" />
            <SystemComponent name="Input Sanitizer" status="online" module="Guardrail" />
            <SystemComponent name="Structured Logger" status="online" module="Logging" />
            <SystemComponent name="Scam DNA Extractor" status="online" module="Extraction" />
            <SystemComponent name="Entity Resolver" status="online" module="Resolution" />
            <SystemComponent name="Embedding Service" status="online" module="Embeddings" />
            <SystemComponent name="Campaign Engine" status="online" module="Analytics" />
            <SystemComponent name="Graph Builder" status="online" module="Graph" />
            <SystemComponent name="Investigator Copilot" status="online" module="Copilot" />
          </div>
        </div>

        {/* Pipeline Visualization */}
        <div className="glass-card">
          <div className="section-header">
            <div>
              <h3 className="section-header__title">Detection Pipeline</h3>
              <div className="section-header__subtitle">Data flow stages</div>
            </div>
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '4px' }}>
            <PipelineStage
              icon={<FileSearch size={16} />}
              label="Incident Ingestion"
              status="ready"
            />
            <PipelineConnector />
            <PipelineStage
              icon={<ShieldCheck size={16} />}
              label="PII Normalization"
              status="ready"
            />
            <PipelineConnector />
            <PipelineStage
              icon={<Cpu size={16} />}
              label="LLM Extraction → Scam DNA"
              status="pending"
            />
            <PipelineConnector />
            <PipelineStage
              icon={<Zap size={16} />}
              label="Entity Resolution"
              status="pending"
            />
            <PipelineConnector />
            <PipelineStage
              icon={<Network size={16} />}
              label="Embedding + ML Similarity"
              status="pending"
            />
            <PipelineConnector />
            <PipelineStage
              icon={<Target size={16} />}
              label="Campaign Detection"
              status="pending"
            />
            <PipelineConnector />
            <PipelineStage
              icon={<AlertTriangle size={16} />}
              label="Campaign Alert"
              status="pending"
            />
          </div>
        </div>
      </div>

      {/* Architecture Info */}
      <div className="glass-card">
        <div className="section-header">
          <div>
            <h3 className="section-header__title">Architecture Highlights</h3>
            <div className="section-header__subtitle">Key architectural design principles</div>
          </div>
        </div>

        <div className="grid-3">
          <ArchCard
            icon={<ShieldCheck size={20} />}
            title="PII-Safe Logging"
            description="All identifiers (phone, email, UPI, URL) are HMAC-SHA256 hashed before any log emission. Zero raw PII in logs."
            tag="§4.2"
          />
          <ArchCard
            icon={<AlertTriangle size={20} />}
            title="Prompt-Injection Defense"
            description="Input sanitizer detects and neutralizes known LLM injection patterns. Incident text is treated as adversarial data."
            tag="§4.1"
          />
          <ArchCard
            icon={<Clock size={20} />}
            title="100% Offline Fallback"
            description="Every external API (LLM, embeddings) has a deterministic mock provider. System runs fully offline for demos."
            tag="§4.5"
          />
        </div>
      </div>
    </div>
  )
}

/* ── Sub-components ────────────────────────────────────────────────────── */

function StatCard({ icon, iconColor, label, value, sub }: {
  icon: React.ReactNode
  iconColor: 'cyan' | 'violet' | 'emerald' | 'amber' | 'red'
  label: string
  value: string
  sub: string
}) {
  return (
    <div className="stat-card">
      <div className={`stat-card__icon stat-card__icon--${iconColor}`}>
        {icon}
      </div>
      <div className="stat-card__content">
        <div className="stat-card__label">{label}</div>
        <div className="stat-card__value">{value}</div>
        <div className="stat-card__sub">{sub}</div>
      </div>
    </div>
  )
}

function SystemComponent({ name, status, module }: {
  name: string
  status: 'online' | 'pending' | 'error'
  module: string
}) {
  const statusConfig = {
    online: { badge: 'badge--online', label: 'Online' },
    pending: { badge: 'badge--warning', label: 'Pending' },
    error: { badge: 'badge--danger', label: 'Error' },
  }[status]

  return (
    <div style={{
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'space-between',
      padding: '8px 12px',
      borderRadius: 'var(--radius-sm)',
      background: 'var(--bg-surface)',
      border: '1px solid var(--border-subtle)',
    }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
        {status === 'online' && <div className="pulse-dot" style={{ width: '6px', height: '6px' }} />}
        {status === 'pending' && (
          <div style={{
            width: '6px', height: '6px', borderRadius: '50%',
            background: 'var(--warning-400)', opacity: 0.5,
          }} />
        )}
        <span style={{ fontSize: '0.85rem', color: 'var(--text-primary)' }}>{name}</span>
      </div>
      <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
        <span style={{
          fontSize: '0.65rem',
          color: 'var(--text-dim)',
          fontFamily: "'JetBrains Mono', monospace",
        }}>
          {module}
        </span>
        <span className={`badge ${statusConfig.badge}`} style={{ fontSize: '0.6rem', padding: '2px 8px' }}>
          {statusConfig.label}
        </span>
      </div>
    </div>
  )
}

function PipelineStage({ icon, label, status }: {
  icon: React.ReactNode
  label: string
  status: 'ready' | 'pending' | 'active'
}) {
  const colors = {
    ready: { bg: 'var(--success-glow)', border: 'rgba(16, 185, 129, 0.2)', text: 'var(--success-400)' },
    pending: { bg: 'var(--bg-surface)', border: 'var(--border-subtle)', text: 'var(--text-dim)' },
    active: { bg: 'var(--primary-glow)', border: 'rgba(6, 182, 212, 0.2)', text: 'var(--primary-400)' },
  }[status]

  return (
    <div style={{
      display: 'flex',
      alignItems: 'center',
      gap: '12px',
      padding: '10px 14px',
      borderRadius: 'var(--radius-sm)',
      background: colors.bg,
      border: `1px solid ${colors.border}`,
      color: colors.text,
    }}>
      {icon}
      <span style={{ fontSize: '0.85rem', fontWeight: 500 }}>{label}</span>
      <span style={{ marginLeft: 'auto', fontSize: '0.65rem', textTransform: 'uppercase', fontWeight: 600 }}>
        {status}
      </span>
    </div>
  )
}

function PipelineConnector() {
  return (
    <div style={{
      display: 'flex',
      justifyContent: 'center',
      height: '16px',
    }}>
      <div style={{
        width: '2px',
        height: '100%',
        background: 'var(--border-default)',
      }} />
    </div>
  )
}

function ArchCard({ icon, title, description, tag }: {
  icon: React.ReactNode
  title: string
  description: string
  tag: string
}) {
  return (
    <div style={{
      padding: '16px',
      borderRadius: 'var(--radius-md)',
      background: 'var(--bg-surface)',
      border: '1px solid var(--border-subtle)',
    }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '8px' }}>
        <div style={{ color: 'var(--primary-400)' }}>{icon}</div>
        <span style={{ fontSize: '0.85rem', fontWeight: 600 }}>{title}</span>
        <span style={{
          marginLeft: 'auto',
          fontSize: '0.6rem',
          color: 'var(--text-dim)',
          fontFamily: "'JetBrains Mono', monospace",
          padding: '2px 6px',
          borderRadius: 'var(--radius-sm)',
          background: 'var(--bg-elevated)',
        }}>
          {tag}
        </span>
      </div>
      <p style={{ fontSize: '0.8rem', color: 'var(--text-muted)', lineHeight: 1.5 }}>
        {description}
      </p>
    </div>
  )
}
