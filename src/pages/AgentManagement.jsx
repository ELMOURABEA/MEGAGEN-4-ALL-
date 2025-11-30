import React, { useState } from 'react'
import './AgentManagement.css'

function AgentManagement() {
  const [agents] = useState([
    {
      id: 1,
      name: 'Research Agent',
      type: 'Research',
      status: 'active',
      tasks: 24,
      successRate: 98,
      lastActive: '2 min ago',
    },
    {
      id: 2,
      name: 'Code Agent',
      type: 'Development',
      status: 'active',
      tasks: 156,
      successRate: 95,
      lastActive: '5 min ago',
    },
    {
      id: 3,
      name: 'Data Agent',
      type: 'Analytics',
      status: 'active',
      tasks: 89,
      successRate: 99,
      lastActive: '12 min ago',
    },
    {
      id: 4,
      name: 'Content Agent',
      type: 'Writing',
      status: 'idle',
      tasks: 45,
      successRate: 97,
      lastActive: '1 hour ago',
    },
    {
      id: 5,
      name: 'Analytics Agent',
      type: 'Analytics',
      status: 'active',
      tasks: 67,
      successRate: 96,
      lastActive: '8 min ago',
    },
    {
      id: 6,
      name: 'Communication Agent',
      type: 'Communication',
      status: 'idle',
      tasks: 34,
      successRate: 94,
      lastActive: '3 hours ago',
    },
  ])

  const [filter, setFilter] = useState('all')

  const filteredAgents = agents.filter((agent) => {
    if (filter === 'all') return true
    return agent.status === filter
  })

  const getStatusColor = (status) => {
    switch (status) {
      case 'active':
        return 'status-active'
      case 'idle':
        return 'status-idle'
      default:
        return 'status-offline'
    }
  }

  return (
    <div className="agent-management">
      <div className="management-header">
        <div>
          <h2>Agent Management</h2>
          <p className="management-subtitle">Monitor and control your AI agents</p>
        </div>
        <button className="btn-primary">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <circle cx="12" cy="12" r="10" />
            <line x1="12" y1="8" x2="12" y2="16" />
            <line x1="8" y1="12" x2="16" y2="12" />
          </svg>
          Create New Agent
        </button>
      </div>

      <div className="filter-tabs">
        <button
          className={`filter-tab ${filter === 'all' ? 'active' : ''}`}
          onClick={() => setFilter('all')}
        >
          All Agents
          <span className="filter-count">{agents.length}</span>
        </button>
        <button
          className={`filter-tab ${filter === 'active' ? 'active' : ''}`}
          onClick={() => setFilter('active')}
        >
          Active
          <span className="filter-count">
            {agents.filter((a) => a.status === 'active').length}
          </span>
        </button>
        <button
          className={`filter-tab ${filter === 'idle' ? 'active' : ''}`}
          onClick={() => setFilter('idle')}
        >
          Idle
          <span className="filter-count">
            {agents.filter((a) => a.status === 'idle').length}
          </span>
        </button>
      </div>

      <div className="agents-grid">
        {filteredAgents.map((agent) => (
          <div key={agent.id} className="agent-card">
            <div className="agent-card-header">
              <div className="agent-card-title">
                <div className="agent-card-icon">
                  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <path d="M12 2L2 7l10 5 10-5-10-5z" />
                    <path d="M2 17l10 5 10-5M2 12l10 5 10-5" />
                  </svg>
                </div>
                <div>
                  <h3>{agent.name}</h3>
                  <span className="agent-type">{agent.type}</span>
                </div>
              </div>
              <div className={`agent-status ${getStatusColor(agent.status)}`}>
                <span className="status-dot"></span>
                {agent.status}
              </div>
            </div>

            <div className="agent-stats">
              <div className="agent-stat">
                <span className="stat-label">Tasks</span>
                <span className="stat-value">{agent.tasks}</span>
              </div>
              <div className="agent-stat">
                <span className="stat-label">Success Rate</span>
                <span className="stat-value">{agent.successRate}%</span>
              </div>
            </div>

            <div className="agent-card-footer">
              <span className="last-active">Last active: {agent.lastActive}</span>
              <div className="agent-actions">
                <button className="icon-button">
                  <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7" />
                    <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z" />
                  </svg>
                </button>
                <button className="icon-button">
                  <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <polyline points="9 11 12 14 22 4" />
                    <path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11" />
                  </svg>
                </button>
                <button className="icon-button delete">
                  <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <polyline points="3 6 5 6 21 6" />
                    <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2" />
                  </svg>
                </button>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}

export default AgentManagement
