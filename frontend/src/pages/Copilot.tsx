import React, { useState } from 'react'
import { Send, FileText } from 'lucide-react'

interface Message {
  id: string
  sender: 'user' | 'copilot'
  text: string
  citations?: string[]
  insufficient?: boolean
}

export default function Copilot() {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: 'm1',
      sender: 'copilot',
      text: 'Greetings. I am the Evidence-Bounded Investigator Copilot. I answer queries strictly using verified incident evidence and graph relationships. Ask me why incidents are connected or what tactics were observed.',
    },
  ])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)

  const handleSend = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!input.trim()) return

    const userMsg: Message = { id: String(Date.now()), sender: 'user', text: input }
    setMessages((prev) => [...prev, userMsg])
    const question = input
    setInput('')
    setLoading(true)

    try {
      const res = await fetch('/api/v1/investigations/copilot', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question }),
      })
      if (res.ok) {
        const data = await res.json()
        setMessages((prev) => [
          ...prev,
          {
            id: String(Date.now() + 1),
            sender: 'copilot',
            text: data.answer,
            citations: data.cited_incident_ids,
            insufficient: data.insufficient_evidence,
          },
        ])
      }
    } catch {
      setMessages((prev) => [
        ...prev,
        {
          id: String(Date.now() + 1),
          sender: 'copilot',
          text: 'Insufficient evidence.',
          insufficient: true,
        },
      ])
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="animate-fade-in" style={{ display: 'flex', flexDirection: 'column', height: 'calc(100vh - 120px)' }}>
      <div className="section-header" style={{ marginBottom: '16px' }}>
        <div>
          <h2 style={{ fontSize: '1.25rem', fontWeight: 700 }}>Evidence-Bounded Investigator Copilot</h2>
          <div className="section-header__subtitle">Strict zero-hallucination Q&A grounded in verified evidence</div>
        </div>
      </div>

      {/* Chat messages container */}
      <div className="glass-card" style={{ flex: 1, display: 'flex', flexDirection: 'column', overflow: 'hidden', padding: 0 }}>
        <div style={{ flex: 1, overflowY: 'auto', padding: '20px', display: 'flex', flexDirection: 'column', gap: '16px' }}>
          {messages.map((m) => (
            <div
              key={m.id}
              style={{
                display: 'flex',
                flexDirection: 'column',
                alignItems: m.sender === 'user' ? 'flex-end' : 'flex-start',
              }}
            >
              <div
                style={{
                  maxWidth: '75%',
                  padding: '12px 16px',
                  borderRadius: 'var(--radius-md)',
                  background: m.sender === 'user' ? 'linear-gradient(135deg, var(--primary-600), var(--accent-600))' : 'var(--bg-secondary)',
                  border: '1px solid ' + (m.sender === 'user' ? 'transparent' : 'var(--border-default)'),
                  color: 'var(--text-primary)',
                  fontSize: '0.9rem',
                  lineHeight: 1.5,
                }}
              >
                {m.text}

                {/* Citation Badges */}
                {m.citations && m.citations.length > 0 && (
                  <div style={{ marginTop: '10px', paddingTop: '8px', borderTop: '1px solid var(--border-subtle)', display: 'flex', flexWrap: 'wrap', gap: '6px' }}>
                    <span style={{ fontSize: '0.7rem', color: 'var(--text-muted)' }}>Citations:</span>
                    {m.citations.map((c) => (
                      <span key={c} className="badge badge--info" style={{ fontSize: '0.65rem' }}>
                        <FileText size={10} /> Incident {c.slice(0, 8)}
                      </span>
                    ))}
                  </div>
                )}
              </div>
            </div>
          ))}
          {loading && (
            <div style={{ color: 'var(--text-muted)', fontSize: '0.85rem' }}>Copilot analyzing evidence...</div>
          )}
        </div>

        {/* Input bar */}
        <form onSubmit={handleSend} style={{ padding: '16px', borderTop: '1px solid var(--border-subtle)', display: 'flex', gap: '12px', background: 'var(--bg-glass)' }}>
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask a question about the evidence (e.g. 'Why are these incidents connected?')..."
            style={{
              flex: 1,
              padding: '12px 16px',
              borderRadius: 'var(--radius-md)',
              background: 'var(--bg-primary)',
              border: '1px solid var(--border-default)',
              color: 'var(--text-primary)',
              fontSize: '0.9rem',
            }}
          />
          <button
            type="submit"
            disabled={loading}
            style={{
              padding: '12px 20px',
              borderRadius: 'var(--radius-md)',
              background: 'var(--primary-500)',
              border: 'none',
              color: 'white',
              cursor: 'pointer',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
            }}
          >
            <Send size={18} />
          </button>
        </form>
      </div>
    </div>
  )
}
