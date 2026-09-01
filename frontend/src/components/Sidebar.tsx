import { NavLink, useLocation } from 'react-router-dom'
import {
  LayoutDashboard,
  FileSearch,
  Target,
  MessageSquare,
  BarChart3,
  Shield,
  Layers,
  Network,
} from 'lucide-react'

const navItems = [
  {
    section: 'Investigation',
    items: [
      { to: '/', label: 'Dashboard', icon: LayoutDashboard },
      { to: '/incidents', label: 'Incidents', icon: FileSearch },
      { to: '/campaigns', label: 'Campaign Clusters', icon: Target },
      { to: '/graph', label: 'Campaign Graph', icon: Network },
      { to: '/architecture', label: 'System Architecture', icon: Layers },
      { to: '/demo', label: 'Killer Demo Mode', icon: Shield },
    ],
  },
  {
    section: 'Intelligence',
    items: [
      { to: '/copilot', label: 'Investigator Copilot', icon: MessageSquare },
      { to: '/evaluation', label: 'Evaluation Scorecard', icon: BarChart3 },
      { to: '/security', label: 'Security & PII Sandbox', icon: Shield },
    ],
  },
]

export default function Sidebar() {
  const location = useLocation()

  return (
    <aside className="app-sidebar">
      {/* Logo */}
      <div className="sidebar-logo">
        <div className="sidebar-logo__icon">
          <Shield size={20} />
        </div>
        <div>
          <div className="sidebar-logo__text">ScamTrap AI</div>
          <div className="sidebar-logo__version">v1.0.0 Production</div>
        </div>
      </div>

      {/* Navigation */}
      {navItems.map((section) => (
        <div className="sidebar-section" key={section.section}>
          <div className="sidebar-section__title">{section.section}</div>
          <nav className="sidebar-nav">
            {section.items.map((item) => {
              const Icon = item.icon
              const isActive = location.pathname === item.to

              return (
                <NavLink
                  key={item.to}
                  to={item.to}
                  className={`sidebar-link ${isActive ? 'sidebar-link--active' : ''}`}
                >
                  <Icon className="sidebar-link__icon" size={18} />
                  <span>{item.label}</span>
                </NavLink>
              )
            })}
          </nav>
        </div>
      ))}

      {/* Footer */}
      <div className="sidebar-footer">
        <div className="synthetic-banner">
          ⚠ Demo — Synthetic Data Only
        </div>
      </div>
    </aside>
  )
}
