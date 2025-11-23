import './App.css'
import { useState, useEffect } from 'react'
import AssistantBubble from './AssistantBubble'

function App() {
  const [systemStatus, setSystemStatus] = useState(null)
  const [logs, setLogs] = useState([])
  const [stardate, setStardate] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchSystemData()
  }, [])

  const fetchSystemData = async () => {
    try {
      // Fetch from ISS API
      const statusRes = await fetch('http://localhost:8000/api/status')
      const statusData = await statusRes.json()
      setSystemStatus(statusData)

      const stardateRes = await fetch('http://localhost:8000/api/stardate')
      const stardateData = await stardateRes.json()
      setStardate(stardateData)

      const logsRes = await fetch('http://localhost:8000/api/log/entries?limit=10')
      const logsData = await logsRes.json()
      setLogs(logsData)

      setLoading(false)
    } catch (error) {
      console.error('Failed to fetch system data:', error)
      setLoading(false)
    }
  }

  if (loading) {
    return <div className="loading">Loading Dual Core Caleon System...</div>
  }

  return (
    <div className="app">
      <header>
        <h1>Dual Core Caleon System Dashboard</h1>
        {stardate && <p className="stardate">Stardate: {stardate.stardate}</p>}
      </header>

      <main>
        <section className="system-status">
          <h2>System Status</h2>
          {systemStatus ? (
            <div className="status-grid">
              <div className="status-item">
                <strong>Status:</strong> {systemStatus.status}
              </div>
              <div className="status-item">
                <strong>Uptime:</strong> {systemStatus.uptime}
              </div>
              <div className="status-item">
                <strong>Active Modules:</strong> {systemStatus.active_modules.join(', ')}
              </div>
              <div className="status-item">
                <strong>Log Entries:</strong> {systemStatus.total_log_entries}
              </div>
            </div>
          ) : (
            <p>Unable to connect to ISS system</p>
          )}
        </section>

        <section className="recent-logs">
          <h2>Recent Log Entries</h2>
          {logs.length > 0 ? (
            <div className="logs-list">
              {logs.map((log, index) => (
                <div key={log.id || index} className="log-entry">
                  <div className="log-header">
                    <span className="log-category">{log.category}</span>
                    <span className="log-time">{new Date(log.timestamp * 1000).toLocaleString()}</span>
                  </div>
                  <p className="log-content">{log.content}</p>
                  {log.tags && log.tags.length > 0 && (
                    <div className="log-tags">
                      {log.tags.map(tag => <span key={tag} className="tag">{tag}</span>)}
                    </div>
                  )}
                </div>
              ))}
            </div>
          ) : (
            <p>No recent logs available</p>
          )}
        </section>

        <section className="modules">
          <h2>System Modules</h2>
          <div className="modules-grid">
            <div className="module-card">
              <h3>ISS Module</h3>
              <p>Integrated Systems Solution</p>
              <a href="http://localhost:8000" target="_blank" rel="noopener noreferrer">Access Dashboard</a>
            </div>
            <div className="module-card">
              <h3>Phonatory Output</h3>
              <p>Text-to-Speech System</p>
              <a href="http://localhost:8007" target="_blank" rel="noopener noreferrer">Access API</a>
            </div>
            <div className="module-card">
              <h3>Synaptic Resonators</h3>
              <p>Cognitive Processing Units</p>
              <p>Left & Right Hemispheres</p>
            </div>
          </div>
        </section>
      </main>

      {/* Nebula Core Assistant Bubble */}
      <AssistantBubble />
    </div>
  )
}

export default App
