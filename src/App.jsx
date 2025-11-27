import React, { useState } from 'react'
import Header from './components/Header'
import Sidebar from './components/Sidebar'
import Dashboard from './pages/Dashboard'
import AgentChat from './pages/AgentChat'
import AgentManagement from './pages/AgentManagement'
import './styles/App.css'

function App() {
  const [currentPage, setCurrentPage] = useState('dashboard')
  const [sidebarOpen, setSidebarOpen] = useState(true)

  const renderPage = () => {
    switch (currentPage) {
      case 'dashboard':
        return <Dashboard />
      case 'chat':
        return <AgentChat />
      case 'agents':
        return <AgentManagement />
      default:
        return <Dashboard />
    }
  }

  return (
    <div className="app">
      <Header
        onMenuClick={() => setSidebarOpen(!sidebarOpen)}
      />
      <div className="app-container">
        <Sidebar
          currentPage={currentPage}
          setCurrentPage={setCurrentPage}
          isOpen={sidebarOpen}
        />
        <main className={`main-content ${sidebarOpen ? 'sidebar-open' : ''}`}>
          {renderPage()}
        </main>
      </div>
    </div>
  )
}

export default App
