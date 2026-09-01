import { BrowserRouter, Routes, Route } from 'react-router-dom'
import AppLayout from './layouts/AppLayout'
import Dashboard from './pages/Dashboard'
import Incidents from './pages/Incidents'
import Campaigns from './pages/Campaigns'
import CampaignGraph from './pages/CampaignGraph'
import SecurityAudit from './pages/SecurityAudit'
import TrojanVictim from './pages/TrojanVictim'
import IOCSearch from './pages/IOCSearch'
import MitreMatrix from './pages/MitreMatrix'
import ThreatFeeds from './pages/ThreatFeeds'
import Copilot from './pages/Copilot'
import Evaluation from './pages/Evaluation'
import Architecture from './pages/Architecture'
import DemoMode from './pages/DemoMode'
import NotFound from './pages/NotFound'
import './index.css'

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route element={<AppLayout />}>
          <Route path="/" element={<Dashboard />} />
          <Route path="/incidents" element={<Incidents />} />
          <Route path="/campaigns" element={<Campaigns />} />
          <Route path="/graph" element={<CampaignGraph />} />
          <Route path="/trojan-victim" element={<TrojanVictim />} />
          <Route path="/ioc-search" element={<IOCSearch />} />
          <Route path="/mitre-matrix" element={<MitreMatrix />} />
          <Route path="/threat-feeds" element={<ThreatFeeds />} />
          <Route path="/architecture" element={<Architecture />} />
          <Route path="/copilot" element={<Copilot />} />
          <Route path="/evaluation" element={<Evaluation />} />
          <Route path="/security" element={<SecurityAudit />} />
          <Route path="/demo" element={<DemoMode />} />
          <Route path="*" element={<NotFound />} />
        </Route>
      </Routes>
    </BrowserRouter>
  )
}

export default App
