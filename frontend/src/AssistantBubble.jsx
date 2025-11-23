import { useState, useEffect, useRef } from 'react'
import './AssistantBubble.css'

function AssistantBubble() {
  const [isExpanded, setIsExpanded] = useState(false)
  const [messages, setMessages] = useState([])
  const [inputValue, setInputValue] = useState('')
  const [isTyping, setIsTyping] = useState(false)
  const [stardate, setStardate] = useState(null)
  const [hemisphereStatus, setHemisphereStatus] = useState({ left: 'inactive', right: 'inactive' })
  const [resonanceLevel, setResonanceLevel] = useState(0)
  const [showEyes, setShowEyes] = useState(false)
  const messagesEndRef = useRef(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const [wsConnection, setWsConnection] = useState(null)
  const [platform, setPlatform] = useState('unknown')
  const [cognitiveLoad, setCognitiveLoad] = useState(0)
  const [activeConnections, setActiveConnections] = useState(0)
  const [isDirectPhi3, setIsDirectPhi3] = useState(false)
  const [isTextArticulation, setIsTextArticulation] = useState(false)

  useEffect(() => {
    // Fetch initial status and stardate
    fetchStatus()
    fetchStardate()

    // Establish WebSocket connection for real-time updates
    const ws = new WebSocket('ws://localhost:8000/ws/live')

    ws.onopen = () => {
      console.log('WebSocket connected')
      setWsConnection(ws)
    }

    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data)
        if (data.type === 'status_update') {
          setStardate(data.stardate)
          setPlatform(data.platform)
          setHemisphereStatus(data.hemisphere_status || { left: 'inactive', right: 'inactive' })
          setCognitiveLoad(data.cognitive_load || 0)
          setActiveConnections(data.active_connections || 0)
          setOllamaStatus(data.ollama_status || 'inactive')

          // Calculate resonance level based on active hemispheres
          const activeCount = Object.values(data.hemisphere_status || {}).filter(status => status === 'active').length
          setResonanceLevel(activeCount / 2) // 0, 0.5, or 1.0
        }
      } catch (error) {
        console.error('Failed to parse WebSocket message:', error)
      }
    }

    ws.onclose = () => {
      console.log('WebSocket disconnected')
      setWsConnection(null)
      // Fallback to polling if WebSocket fails
      const interval = setInterval(() => {
        fetchStatus()
        fetchStardate()
      }, 5000) // Less frequent polling as fallback

      return () => clearInterval(interval)
    }

    ws.onerror = (error) => {
      console.error('WebSocket error:', error)
    }

    return () => {
      if (ws) {
        ws.close()
      }
    }
  }, [])

  const fetchStatus = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/v1/status')
      const data = await response.json()
      setHemisphereStatus(data.hemisphere_status || { left: 'inactive', right: 'inactive' })

      // Calculate resonance level based on active hemispheres
      const activeCount = Object.values(data.hemisphere_status || {}).filter(status => status === 'active').length
      setResonanceLevel(activeCount / 2) // 0, 0.5, or 1.0
    } catch (error) {
      console.error('Failed to fetch status:', error)
    }
  }

  const fetchStardate = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/v1/pulse')
      const data = await response.json()
      setStardate(data.stardate)
    } catch (error) {
      console.error('Failed to fetch stardate:', error)
    }
  }

  const sendMessage = async (message) => {
    if (!message.trim()) return

    // Add user message
    const userMessage = { type: 'user', content: message, timestamp: new Date() }
    setMessages(prev => [...prev, userMessage])
    setInputValue('')
    setIsTyping(true)

    try {
      if (isTextArticulation) {
        // Text articulation mode - test Caleon's voice
        const response = await fetch('http://localhost:8000/api/v1/speak/text', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            left_verdict: `User input: ${message}`,
            right_verdict: "Analysis suggests thoughtful, protective response needed",
            distilled: {
              intent: "communicate_carefully",
              confidence: 0.88,
              context: "text_articulation_test"
            },
            context: { source: 'assistant_bubble', mode: 'text_articulation' }
          })
        })

        const data = await response.json()

        // Add articulated response
        const articulatedMessage = {
          type: 'articulated',
          content: data.text,
          voice_profile: data.voice_profile,
          pipeline_metadata: data.pipeline_metadata,
          timestamp: new Date()
        }
        setMessages(prev => [...prev, articulatedMessage])
      } else if (isDirectPhi3) {
        // Direct Phi-3 reasoning
        const response = await fetch('http://localhost:8000/api/v1/phi3', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            prompt: message,
            system: "You are Caleon, an advanced AI assistant with deep reasoning capabilities. Provide thoughtful, analytical responses.",
            context: { source: 'assistant_bubble', mode: 'direct_phi3' }
          })
        })

        const data = await response.json()

        // Add Phi-3 response
        const phi3Message = {
          type: 'phi3',
          content: data.response,
          model: data.model,
          performance: data.performance,
          timestamp: new Date()
        }
        setMessages(prev => [...prev, phi3Message])
      } else {
        // Full cognitive processing
        const response = await fetch('http://localhost:8000/api/v1/think', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            message: message,
            context: { source: 'assistant_bubble' },
            priority: 'normal'
          })
        })

        const data = await response.json()

        // Add Caleon response
        const caleonMessage = {
          type: 'caleon',
          content: data.final_verdict,
          reasoning: data.reasoning_chain,
          confidence: data.confidence,
          timestamp: new Date(),
          cycle_id: data.cycle_id,
          ollama_enhancement: data.ollama_enhancement
        }
        setMessages(prev => [...prev, caleonMessage])
      }

    } catch (error) {
      console.error('Failed to send message:', error)
      const errorMessage = { type: 'error', content: 'Connection failed. Please try again.', timestamp: new Date() }
      setMessages(prev => [...prev, errorMessage])
    } finally {
      setIsTyping(false)
    }
  }

  const handleSubmit = (e) => {
    e.preventDefault()
    sendMessage(inputValue)
  }

  const toggleEyes = () => {
    setShowEyes(!showEyes)
  }

  return (
    <>
      {/* Floating Nebula Core Bubble */}
      <div className={`assistant-bubble ${isExpanded ? 'expanded' : ''}`}>
        {!isExpanded ? (
          <div className="bubble-icon" onClick={() => setIsExpanded(true)}>
            <div className="pulse-ring" style={{
              animationDuration: `${3 - resonanceLevel * 2}s` // Faster pulsing when more active
            }}></div>
            <div className="bubble-content">
              <span className="brain-icon">🧠</span>
              <div className="status-indicators">
                <div className={`hemisphere left ${hemisphereStatus.left}`}></div>
                <div className={`hemisphere right ${hemisphereStatus.right}`}></div>
              </div>
            </div>
          </div>
        ) : (
          <div className="chat-window">
            <div className="chat-header">
              <div className="header-info">
                <div className="caleon-avatar">
                  <div className="avatar-circle">
                    <span className="avatar-icon">⚡</span>
                    {isTyping && <div className="spark-lines">
                      <div className="spark-line"></div>
                      <div className="spark-line"></div>
                      <div className="spark-line"></div>
                    </div>}
                  </div>
                  <div className="avatar-info">
                    <h3>Caleon</h3>
                    <span className="stardate">{stardate ? `SD: ${stardate}` : 'Connecting...'}</span>
                    <span className="platform">Platform: {platform}</span>
                  </div>
                </div>
              </div>
              <div className="header-controls">
                <div className="resonance-meter">
                  <div className="resonance-bar">
                    <div
                      className="resonance-fill"
                      style={{ width: `${resonanceLevel * 100}%` }}
                    ></div>
                  </div>
                  <span className="resonance-label">Resonance: {(resonanceLevel * 100).toFixed(0)}%</span>
                </div>
                <div className="system-info">
                  <span className="connections">Connections: {activeConnections}</span>
                  <span className="load">Load: {(cognitiveLoad * 100).toFixed(0)}%</span>
                  <span className={`ollama-status ${ollamaStatus}`}>Ollama: {ollamaStatus}</span>
                </div>
                <div className="mode-toggle">
                  <button
                    className={`mode-btn ${!isDirectPhi3 && !isTextArticulation ? 'active' : ''}`}
                    onClick={() => {
                      setIsDirectPhi3(false)
                      setIsTextArticulation(false)
                    }}
                  >
                    Dual-Core
                  </button>
                  <button
                    className={`mode-btn ${isDirectPhi3 ? 'active' : ''}`}
                    onClick={() => {
                      setIsDirectPhi3(true)
                      setIsTextArticulation(false)
                    }}
                  >
                    Phi-3 Direct
                  </button>
                  <button
                    className={`mode-btn ${isTextArticulation ? 'active' : ''}`}
                    onClick={() => {
                      setIsDirectPhi3(false)
                      setIsTextArticulation(true)
                    }}
                  >
                    Text Voice
                  </button>
                </div>
                <button className="eyes-toggle" onClick={toggleEyes}>
                  👁️
                </button>
                <button className="close-btn" onClick={() => setIsExpanded(false)}>
                  ✕
                </button>
              </div>
            </div>

            <div className="messages-container">
              {messages.map((msg, index) => (
                <div key={index} className={`message ${msg.type}`}>
                  <div className="message-content">
                    {msg.type === 'caleon' && (
                      <div className="message-meta">
                        <span className="confidence">Confidence: {(msg.confidence * 100).toFixed(1)}%</span>
                        {msg.cycle_id && <span className="cycle">Cycle: {msg.cycle_id}</span>}
                      </div>
                    )}
                    {msg.type === 'phi3' && (
                      <div className="message-meta">
                        <span className="model">Model: {msg.model}</span>
                        {msg.performance && <span className="tokens">Tokens: {msg.performance.eval_count}</span>}
                      </div>
                    )}
                    {msg.type === 'articulated' && (
                      <div className="message-meta">
                        <span className="voice-profile">Voice: {msg.voice_profile?.personality || 'grounded_guardian'}</span>
                        <span className="pipeline">Pipeline: {msg.pipeline_metadata?.pipeline_duration?.toFixed(2)}s</span>
                      </div>
                    )}
                    <p>{msg.content}</p>
                    {msg.reasoning && (
                      <details className="reasoning">
                        <summary>View Reasoning</summary>
                        <pre>{JSON.stringify(msg.reasoning, null, 2)}</pre>
                      </details>
                    )}
                    {msg.ollama_enhancement && (
                      <details className="ollama-enhancement">
                        <summary>🧠 Ollama Insights (Phi 3.5 Mini)</summary>
                        <div className="ollama-content">
                          <p>{msg.ollama_enhancement.enhancement?.insights}</p>
                          <div className="ollama-meta">
                            <span>Model: {msg.ollama_enhancement.enhancement?.model}</span>
                            <span>Tokens: {msg.ollama_enhancement.enhancement?.performance?.eval_count}</span>
                          </div>
                        </div>
                      </details>
                    )}
                  </div>
                  <span className="timestamp">
                    {msg.timestamp.toLocaleTimeString()}
                  </span>
                </div>
              ))}
              {isTyping && (
                <div className="message caleon typing">
                  <div className="typing-indicator">
                    <span></span>
                    <span></span>
                    <span></span>
                  </div>
                </div>
              )}
              <div ref={messagesEndRef} />
            </div>

            <form className="message-input" onSubmit={handleSubmit}>
              <input
                type="text"
                value={inputValue}
                onChange={(e) => setInputValue(e.target.value)}
                placeholder="Communicate with Caleon..."
                disabled={isTyping}
              />
              <button type="submit" disabled={isTyping || !inputValue.trim()}>
                Send
              </button>
            </form>
          </div>
        )}
      </div>

      {/* Caleon Eyes Animation */}
      {showEyes && (
        <div className="caleon-eyes-overlay">
          <div className="eyes-container">
            <div className="eye left-eye">
              <div className="pupil"></div>
            </div>
            <div className="eye right-eye">
              <div className="pupil"></div>
            </div>
          </div>
        </div>
      )}
    </>
  )
}

export default AssistantBubble