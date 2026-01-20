import React, { useState, useEffect } from 'react'
import { octogenService } from '../services/octogenService'
import './OctogenDashboard.css'

function OctogenDashboard() {
  const [tentacles, setTentacles] = useState([])
  const [subscription, setSubscription] = useState(null)
  const [stats, setStats] = useState(null)
  const [loading, setLoading] = useState(true)
  const [activeTab, setActiveTab] = useState('overview')

  useEffect(() => {
    loadData()
  }, [])

  const loadData = async () => {
    try {
      const [tentaclesData, statsData] = await Promise.all([
        octogenService.getTentacles(),
        octogenService.getUsageStats(),
      ])
      setTentacles(tentaclesData)
      setStats(statsData)
      setSubscription(statsData.subscription)
    } catch (error) {
      console.error('Failed to load data:', error)
    } finally {
      setLoading(false)
    }
  }

  const getTierInfo = (tier) => {
    const tiers = {
      free: { name: 'Free', color: '#64748b', queries: '10/day', research: '5/day' },
      pro: { name: 'Pro', color: '#2563eb', queries: 'Unlimited', research: 'Unlimited' },
      enterprise: { name: 'Enterprise', color: '#10b981', queries: 'Unlimited', research: 'Unlimited' },
    }
    return tiers[tier] || tiers.free
  }

  const getStatusColor = (status) => {
    const colors = {
      active: '#10b981',
      idle: '#f59e0b',
      busy: '#3b82f6',
      offline: '#64748b',
    }
    return colors[status] || colors.offline
  }

  if (loading) {
    return <div className="octogen-loading">Loading MeGaOcToOoN System...</div>
  }

  const tierInfo = getTierInfo(subscription?.tier || 'free')

  return (
    <div className="octogen-dashboard">
      <div className="octogen-header">
        <div className="octogen-title-section">
          <h1 className="octogen-title">MeGaOcToOoN</h1>
          <p className="octogen-subtitle">Unleash Octopodal Intelligence - AI-Agent x10</p>
        </div>
        <div className="tier-badge" style={{ borderColor: tierInfo.color }}>
          <div className="tier-dot" style={{ backgroundColor: tierInfo.color }}></div>
          {tierInfo.name} Tier
        </div>
      </div>

      <div className="tab-navigation">
        <button
          className={`tab-button ${activeTab === 'overview' ? 'active' : ''}`}
          onClick={() => setActiveTab('overview')}
        >
          Overview
        </button>
        <button
          className={`tab-button ${activeTab === 'tentacles' ? 'active' : ''}`}
          onClick={() => setActiveTab('tentacles')}
        >
          AI Tentacles
        </button>
        <button
          className={`tab-button ${activeTab === 'usage' ? 'active' : ''}`}
          onClick={() => setActiveTab('usage')}
        >
          Usage & Limits
        </button>
      </div>

      {activeTab === 'overview' && (
        <div className="overview-section">
          <div className="stats-row">
            <div className="stat-box">
              <div className="stat-icon octopus">🐙</div>
              <div className="stat-info">
                <div className="stat-value">{tentacles.length}</div>
                <div className="stat-label">AI Tentacles</div>
              </div>
            </div>
            <div className="stat-box">
              <div className="stat-icon">⚡</div>
              <div className="stat-info">
                <div className="stat-value">{stats?.totalTasks || 0}</div>
                <div className="stat-label">Tasks Completed</div>
              </div>
            </div>
            <div className="stat-box">
              <div className="stat-icon">✨</div>
              <div className="stat-info">
                <div className="stat-value">{stats?.totalDreams || 0}</div>
                <div className="stat-label">Dreams Achieved</div>
              </div>
            </div>
            <div className="stat-box">
              <div className="stat-icon">🔬</div>
              <div className="stat-info">
                <div className="stat-value">{stats?.totalResearch || 0}</div>
                <div className="stat-label">Research Operations</div>
              </div>
            </div>
          </div>

          <div className="capabilities-grid">
            <div className="capability-card">
              <h3>🔗 Self-Connect</h3>
              <p>Automatically connects to all systems</p>
            </div>
            <div className="capability-card">
              <h3>⚡ Instant Builder</h3>
              <p>Build anything in 3-5 minutes</p>
            </div>
            <div className="capability-card">
              <h3>✨ Dream Achievement</h3>
              <p>95% success rate in achieving goals</p>
            </div>
            <div className="capability-card">
              <h3>🔬 Deep Research</h3>
              <p>Unlimited depth with petabyte databases</p>
            </div>
            <div className="capability-card">
              <h3>💼 Business Plans</h3>
              <p>Complete executive strategies</p>
            </div>
            <div className="capability-card">
              <h3>🔄 Auto-Update</h3>
              <p>Updates everything automatically</p>
            </div>
          </div>
        </div>
      )}

      {activeTab === 'tentacles' && (
        <div className="tentacles-section">
          <div className="tentacles-grid">
            {tentacles.map((tentacle) => (
              <div key={tentacle.id} className="tentacle-card">
                <div className="tentacle-header">
                  <div className="tentacle-name">
                    <div
                      className="tentacle-status-dot"
                      style={{ backgroundColor: getStatusColor(tentacle.status) }}
                    ></div>
                    <h4>{tentacle.name}</h4>
                  </div>
                  <span className="tentacle-platform">{tentacle.platform}</span>
                </div>
                <div className="tentacle-type">{tentacle.type}</div>
                <div className="tentacle-stats">
                  <div className="tentacle-stat">
                    <span className="label">Tasks</span>
                    <span className="value">{tentacle.tasks_completed}</span>
                  </div>
                  <div className="tentacle-stat">
                    <span className="label">Success</span>
                    <span className="value">{tentacle.success_rate}%</span>
                  </div>
                  <div className="tentacle-stat">
                    <span className="label">Speed</span>
                    <span className="value">{tentacle.response_time_ms}ms</span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {activeTab === 'usage' && (
        <div className="usage-section">
          <div className="usage-card">
            <h3>Current Plan: {tierInfo.name}</h3>
            <div className="usage-details">
              <div className="usage-item">
                <span className="usage-label">Queries Today</span>
                <span className="usage-value">
                  {subscription?.queries_today || 0} / {tierInfo.queries}
                </span>
              </div>
              <div className="usage-item">
                <span className="usage-label">Research Today</span>
                <span className="usage-value">
                  {subscription?.research_today || 0} / {tierInfo.research}
                </span>
              </div>
            </div>
          </div>

          <div className="tier-comparison">
            <div className="tier-card">
              <h4>Free</h4>
              <div className="tier-price">$0/month</div>
              <ul className="tier-features">
                <li>10 queries per day</li>
                <li>5 research operations per day</li>
                <li>2 concurrent tasks</li>
                <li>Basic caching</li>
              </ul>
            </div>
            <div className="tier-card pro">
              <h4>Pro</h4>
              <div className="tier-price">$9.99/month</div>
              <ul className="tier-features">
                <li>Unlimited queries</li>
                <li>Unlimited research</li>
                <li>10 concurrent tasks</li>
                <li>Advanced caching</li>
                <li>Auto-updates</li>
              </ul>
              <button className="upgrade-button">Upgrade to Pro</button>
            </div>
            <div className="tier-card enterprise">
              <h4>Enterprise</h4>
              <div className="tier-price">$29.99/month</div>
              <ul className="tier-features">
                <li>Everything in Pro</li>
                <li>20 concurrent tasks</li>
                <li>Priority support</li>
                <li>Early access features</li>
                <li>Premium integrations</li>
              </ul>
              <button className="upgrade-button">Upgrade to Enterprise</button>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

export default OctogenDashboard
