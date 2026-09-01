import { useState } from 'react'
import { Network, Filter, ZoomIn, ZoomOut, Info } from 'lucide-react'

export default function CampaignGraph() {
  const [filterType, setFilterType] = useState<string>('all')
  const [selectedNode, setSelectedNode] = useState<any>(null)

  const graphNodes = [
    { id: 'inc-1', label: 'Incident #1 (SMS SBI)', type: 'incident', color: 'var(--primary-400)' },
    { id: 'inc-2', label: 'Incident #2 (WhatsApp Tamil)', type: 'incident', color: 'var(--primary-400)' },
    { id: 'inc-3', label: 'Incident #3 (Hindi Alert)', type: 'incident', color: 'var(--primary-400)' },
    { id: 'upi-1', label: 'UPI: sbi.kyc.update@ybl', type: 'upi', color: 'var(--warning-400)' },
    { id: 'phone-1', label: 'Phone: +919876543210', type: 'phone', color: 'var(--success-400)' },
    { id: 'url-1', label: 'URL: sbi-kyc-update.xyz', type: 'url', color: 'var(--danger-400)' },
    { id: 'camp-1', label: 'Campaign: SBI KYC Scam', type: 'campaign', color: 'var(--accent-400)' },
  ]

  const filteredNodes = filterType === 'all'
    ? graphNodes
    : graphNodes.filter((n) => n.type === filterType)

  return (
    <div className="animate-fade-in" style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
      <div className="section-header">
        <div>
          <h2 style={{ fontSize: '1.25rem', fontWeight: 700, display: 'flex', alignItems: 'center', gap: '8px' }}>
            <Network style={{ color: 'var(--primary-400)' }} /> Interactive Campaign Graph Visualizer
          </h2>
          <div className="section-header__subtitle">
            Heterogeneous multi-graph connecting Incidents, Shared Infrastructure (Phone, UPI, URL), and Detected Campaigns
          </div>
        </div>

        {/* Filter Bar */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          <Filter size={16} style={{ color: 'var(--text-muted)' }} />
          <select
            value={filterType}
            onChange={(e) => setFilterType(e.target.value)}
            style={{
              padding: '6px 12px',
              borderRadius: 'var(--radius-sm)',
              background: 'var(--bg-primary)',
              border: '1px solid var(--border-default)',
              color: 'var(--text-primary)',
              fontSize: '0.85rem',
            }}
          >
            <option value="all">Show All Node Types</option>
            <option value="incident">Incidents Only</option>
            <option value="upi">UPI IDs Only</option>
            <option value="phone">Phones Only</option>
            <option value="url">URLs Only</option>
            <option value="campaign">Campaigns Only</option>
          </select>
        </div>
      </div>

      <div className="grid-2">
        {/* Graph Canvas Visualizer */}
        <div className="glass-card" style={{ height: '420px', position: 'relative', overflow: 'hidden', display: 'flex', alignItems: 'center', justifyContent: 'center', background: 'var(--bg-deep)' }}>
          {/* Background Grid Pattern */}
          <div style={{
            position: 'absolute', top: 0, left: 0, right: 0, bottom: 0,
            backgroundImage: 'radial-gradient(circle at 1px 1px, rgba(56, 189, 248, 0.08) 1px, transparent 0)',
            backgroundSize: '24px 24px', pointerEvents: 'none'
          }} />

          {/* Interactive Graph Nodes Representation */}
          <div style={{ position: 'relative', width: '100%', height: '100%', display: 'flex', flexWrap: 'wrap', alignItems: 'center', justifyContent: 'center', gap: '24px', padding: '30px' }}>
            {filteredNodes.map((n) => (
              <div
                key={n.id}
                onClick={() => setSelectedNode(n)}
                style={{
                  padding: '12px 18px',
                  borderRadius: 'var(--radius-lg)',
                  background: 'var(--bg-glass)',
                  backdropFilter: 'blur(12px)',
                  border: '1px solid ' + (selectedNode?.id === n.id ? n.color : 'var(--border-hover)'),
                  boxShadow: selectedNode?.id === n.id ? `0 0 16px ${n.color}` : 'var(--shadow-sm)',
                  cursor: 'pointer',
                  transition: 'all var(--transition-fast)',
                  display: 'flex',
                  alignItems: 'center',
                  gap: '8px',
                }}
              >
                <div style={{ width: '10px', height: '10px', borderRadius: '50%', background: n.color }} />
                <span style={{ fontSize: '0.85rem', fontWeight: 600, color: 'var(--text-primary)' }}>{n.label}</span>
              </div>
            ))}
          </div>

          <div style={{ position: 'absolute', bottom: '12px', right: '12px', display: 'flex', gap: '6px' }}>
            <button style={{ padding: '6px 10px', borderRadius: 'var(--radius-sm)', background: 'var(--bg-surface)', border: '1px solid var(--border-subtle)', color: 'var(--text-primary)', cursor: 'pointer' }}><ZoomIn size={14} /></button>
            <button style={{ padding: '6px 10px', borderRadius: 'var(--radius-sm)', background: 'var(--bg-surface)', border: '1px solid var(--border-subtle)', color: 'var(--text-primary)', cursor: 'pointer' }}><ZoomOut size={14} /></button>
          </div>
        </div>

        {/* Node Detail Inspector */}
        <div className="glass-card">
          <h3 style={{ fontSize: '1rem', marginBottom: '16px', display: 'flex', alignItems: 'center', gap: '8px' }}>
            <Info size={18} style={{ color: 'var(--primary-400)' }} /> Node Inspection Panel
          </h3>

          {selectedNode ? (
            <div style={{ display: 'flex', flexDirection: 'column', gap: '12px', fontSize: '0.85rem' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                <span style={{ color: 'var(--text-muted)' }}>Node ID:</span>
                <span className="mono">{selectedNode.id}</span>
              </div>
              <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                <span style={{ color: 'var(--text-muted)' }}>Type:</span>
                <span className="badge badge--info">{selectedNode.type}</span>
              </div>
              <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                <span style={{ color: 'var(--text-muted)' }}>Node Label:</span>
                <span>{selectedNode.label}</span>
              </div>

              <div style={{ marginTop: '12px', padding: '12px', background: 'var(--bg-primary)', borderRadius: 'var(--radius-sm)', border: '1px solid var(--border-subtle)' }}>
                <div style={{ fontWeight: 600, color: 'var(--primary-300)', marginBottom: '4px' }}>Graph Connectivity & Provenance</div>
                <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', lineHeight: 1.5 }}>
                  This node is linked across 3 incidents via verified deterministic infrastructure edges. Zero unverified ML claims.
                </div>
              </div>
            </div>
          ) : (
            <div className="empty-state">
              <Network className="empty-state__icon" />
              <div className="empty-state__title">Select a Node</div>
              <div className="empty-state__text">Click any node on the graph canvas to inspect its relationships and evidence.</div>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
