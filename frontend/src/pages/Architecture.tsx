import { useState } from 'react'
import { Network, Cpu, ShieldCheck, Layers, GitFork, Lock, FileSearch } from 'lucide-react'

export default function Architecture() {
  const [selectedNode, setSelectedNode] = useState<string | null>(null)

  const architectureNodes = [
    {
      id: 'ingestion',
      name: '1. Multilingual Ingestion API',
      type: 'Gateway',
      icon: <FileSearch size={20} />,
      desc: 'Ingests SMS, WhatsApp, Email, and Voice transcripts in English, Tamil, Hindi, and code-switched text.',
      tech: 'FastAPI, Pydantic v2',
      security: 'Untrusted input sanitization (§4.1), prompt-injection defense.',
    },
    {
      id: 'pii',
      name: '2. PII Tokenization & Redaction',
      type: 'Security Layer',
      icon: <Lock size={20} />,
      desc: 'Hashes all raw phone numbers, UPI IDs, emails, and URLs using HMAC-SHA256 before log emission or persistence.',
      tech: 'HMAC-SHA256, structlog processor',
      security: 'Zero raw PII in logs (§4.2).',
    },
    {
      id: 'llm',
      name: '3. LLM Multilingual Extractor',
      type: 'AI Engine',
      icon: <Cpu size={20} />,
      desc: 'Extracts structured Scam DNA fingerprint and classifies tactics into locked taxonomy enums.',
      tech: 'Gemini Provider + 100% Offline Mock Provider',
      security: 'Closed-set enums prevent LLM hallucination.',
    },
    {
      id: 'scam_dna',
      name: '4. Structured Scam DNA',
      type: 'Data Model',
      icon: <Layers size={20} />,
      desc: 'Behavioral fingerprint containing urgency, fear, authority pressure, tactics, and infrastructure indicators.',
      tech: 'Pydantic v2 ScamDNA Schema (§3.4)',
      security: 'Provenance-tagged (OBSERVED / INFERRED / PREDICTED).',
    },
    {
      id: 'resolution',
      name: '5. Entity Resolution & Embeddings',
      type: 'Analytics',
      icon: <GitFork size={20} />,
      desc: 'Normalizes E.164 phones, UPI IDs, and domains; generates behavioral vector embeddings.',
      tech: 'EntityResolver, Cosine Similarity',
      security: 'Namespaced resolution_confidence (§3.2).',
    },
    {
      id: 'relationship',
      name: '6. Candidate Relationship Engine',
      type: 'Hybrid Engine',
      icon: <Network size={20} />,
      desc: 'Generates ML similarity probability and corroborates with deterministic infrastructure evidence.',
      tech: 'RelationshipEngine (ML + Deterministic)',
      security: 'HARD RULE: ML alone cannot produce high confidence without deterministic evidence.',
    },
    {
      id: 'graph',
      name: '7. NetworkX Campaign Graph',
      type: 'Graph Analytics',
      icon: <Network size={20} />,
      desc: 'Constructs heterogeneous multi-graph (Incidents, Phones, UPIs, URLs, Campaigns) and runs community detection.',
      tech: 'NetworkX, React Flow JSON',
      security: 'Graph connectivity backed by evidence chains.',
    },
    {
      id: 'copilot',
      name: '8. Evidence-Bounded Copilot',
      type: 'Investigator AI',
      icon: <ShieldCheck size={20} />,
      desc: 'Answers investigator Q&A with strict zero-hallucination guardrails and interactive citation badges.',
      tech: 'CopilotService, Evidence Engine',
      security: 'Replies "Insufficient evidence" when evidence is missing.',
    },
  ]

  return (
    <div className="animate-fade-in" style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
      <div className="section-header">
        <div>
          <h2 style={{ fontSize: '1.25rem', fontWeight: 700, display: 'flex', alignItems: 'center', gap: '8px' }}>
            <Layers style={{ color: 'var(--primary-400)' }} /> System Architecture & Data Flow Topology
          </h2>
          <div className="section-header__subtitle">
            End-to-end data pipeline from raw multilingual incident to campaign detection and evidence-bounded explainability
          </div>
        </div>
      </div>

      {/* Interactive Pipeline Diagram */}
      <div className="glass-card glass-card--accent">
        <h3 style={{ fontSize: '1rem', marginBottom: '16px', color: 'var(--primary-300)' }}>
          End-to-End Execution Pipeline
        </h3>

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))', gap: '12px' }}>
          {architectureNodes.map((node) => (
            <div
              key={node.id}
              onClick={() => setSelectedNode(node.id)}
              style={{
                padding: '16px',
                borderRadius: 'var(--radius-md)',
                background: selectedNode === node.id ? 'var(--primary-glow-strong)' : 'var(--bg-surface)',
                border: '1px solid ' + (selectedNode === node.id ? 'var(--primary-400)' : 'var(--border-subtle)'),
                cursor: 'pointer',
                transition: 'all var(--transition-fast)',
              }}
            >
              <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '8px' }}>
                <div style={{ color: 'var(--primary-400)' }}>{node.icon}</div>
                <span style={{ fontSize: '0.8rem', fontWeight: 600, color: 'var(--text-primary)' }}>
                  {node.name}
                </span>
              </div>
              <span className="badge badge--info" style={{ fontSize: '0.6rem', marginBottom: '8px' }}>
                {node.type}
              </span>
              <p style={{ fontSize: '0.75rem', color: 'var(--text-muted)', lineHeight: 1.4 }}>
                {node.desc}
              </p>
            </div>
          ))}
        </div>
      </div>

      {/* Selected Node Detailed Inspector */}
      {selectedNode && (
        <div className="glass-card animate-fade-in" style={{ borderLeft: '4px solid var(--primary-400)' }}>
          {(() => {
            const n = architectureNodes.find((x) => x.id === selectedNode)!
            return (
              <div>
                <h3 style={{ fontSize: '1.1rem', marginBottom: '8px', color: 'var(--primary-300)' }}>
                  {n.name} — Technical Details
                </h3>
                <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '16px', marginTop: '12px', fontSize: '0.85rem' }}>
                  <div>
                    <span style={{ color: 'var(--text-muted)' }}>Technology Stack:</span>
                    <div className="mono" style={{ color: 'var(--text-primary)', marginTop: '4px' }}>{n.tech}</div>
                  </div>
                  <div>
                    <span style={{ color: 'var(--text-muted)' }}>Security & Boundary Rules:</span>
                    <div style={{ color: 'var(--success-400)', marginTop: '4px' }}>{n.security}</div>
                  </div>
                </div>
              </div>
            )
          })()}
        </div>
      )}

      {/* Topology Mapping Table */}
      <div className="glass-card">
        <h3 style={{ fontSize: '1rem', marginBottom: '16px' }}>System Topology Component Mapping</h3>
        <div style={{ overflowX: 'auto' }}>
          <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '0.85rem', textAlign: 'left' }}>
            <thead>
              <tr style={{ borderBottom: '1px solid var(--border-default)', color: 'var(--text-muted)' }}>
                <th style={{ padding: '10px' }}>Architecture Component</th>
                <th style={{ padding: '10px' }}>Implementation Service</th>
                <th style={{ padding: '10px' }}>Provenance & Boundary Rule</th>
                <th style={{ padding: '10px' }}>Status</th>
              </tr>
            </thead>
            <tbody>
              <tr style={{ borderBottom: '1px solid var(--border-subtle)' }}>
                <td style={{ padding: '10px', fontWeight: 600 }}>API Gateway</td>
                <td style={{ padding: '10px' }} className="mono">backend/app/main.py</td>
                <td style={{ padding: '10px' }}>Request ID tracing, CORS, input sanitization</td>
                <td style={{ padding: '10px' }}><span className="badge badge--online">Active</span></td>
              </tr>
              <tr style={{ borderBottom: '1px solid var(--border-subtle)' }}>
                <td style={{ padding: '10px', fontWeight: 600 }}>PII Redaction</td>
                <td style={{ padding: '10px' }} className="mono">backend/app/core/security.py</td>
                <td style={{ padding: '10px' }}>HMAC-SHA256 hashing (§4.2)</td>
                <td style={{ padding: '10px' }}><span className="badge badge--online">Active</span></td>
              </tr>
              <tr style={{ borderBottom: '1px solid var(--border-subtle)' }}>
                <td style={{ padding: '10px', fontWeight: 600 }}>LLM Extractor</td>
                <td style={{ padding: '10px' }} className="mono">backend/app/services/llm_provider.py</td>
                <td style={{ padding: '10px' }}>Closed taxonomy enums, 100% offline fallback</td>
                <td style={{ padding: '10px' }}><span className="badge badge--online">Active</span></td>
              </tr>
              <tr style={{ borderBottom: '1px solid var(--border-subtle)' }}>
                <td style={{ padding: '10px', fontWeight: 600 }}>Entity Resolver</td>
                <td style={{ padding: '10px' }} className="mono">backend/app/services/entity_resolver.py</td>
                <td style={{ padding: '10px' }}>E.164 phone, UPI, domain normalization</td>
                <td style={{ padding: '10px' }}><span className="badge badge--online">Active</span></td>
              </tr>
              <tr style={{ borderBottom: '1px solid var(--border-subtle)' }}>
                <td style={{ padding: '10px', fontWeight: 600 }}>Relationship Engine</td>
                <td style={{ padding: '10px' }} className="mono">backend/app/services/relationship_engine.py</td>
                <td style={{ padding: '10px' }}>ML probability + deterministic corroboration rule</td>
                <td style={{ padding: '10px' }}><span className="badge badge--online">Active</span></td>
              </tr>
              <tr style={{ borderBottom: '1px solid var(--border-subtle)' }}>
                <td style={{ padding: '10px', fontWeight: 600 }}>Graph Builder</td>
                <td style={{ padding: '10px' }} className="mono">backend/app/services/graph_engine.py</td>
                <td style={{ padding: '10px' }}>NetworkX heterogeneous multi-graph</td>
                <td style={{ padding: '10px' }}><span className="badge badge--online">Active</span></td>
              </tr>
              <tr style={{ borderBottom: '1px solid var(--border-subtle)' }}>
                <td style={{ padding: '10px', fontWeight: 600 }}>Investigator Copilot</td>
                <td style={{ padding: '10px' }} className="mono">backend/app/services/copilot_service.py</td>
                <td style={{ padding: '10px' }}>Zero-hallucination citation Q&A</td>
                <td style={{ padding: '10px' }}><span className="badge badge--online">Active</span></td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  )
}
