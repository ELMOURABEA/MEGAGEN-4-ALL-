import React, { useState } from 'react'
import { AuthProvider, useAuth } from './contexts/AuthContext'
import Header from './components/Header'
import Sidebar from './components/Sidebar'
import Dashboard from './pages/Dashboard'
import AgentChat from './pages/AgentChat'
import AgentManagement from './pages/AgentManagement'
import OctogenDashboard from './pages/OctogenDashboard'
import Login from './pages/auth/Login'
import SignUp from './pages/auth/SignUp'
import './styles/App.css'

function AuthenticatedApp() {
  const [currentPage, setCurrentPage] = useState('octogen')
  const [sidebarOpen, setSidebarOpen] = useState(true)

  const renderPage = () => {
    switch (currentPage) {
      case 'octogen':
        return <OctogenDashboard />
      case 'dashboard':
        return <Dashboard />
      case 'chat':
        return <AgentChat />
      case 'agents':
        return <AgentManagement />
      default:
        return <OctogenDashboard />
    }
  }

  return (
    <div className="app">
      <Header onMenuClick={() => setSidebarOpen(!sidebarOpen)} />
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

function AppContent() {
  const { user, loading } = useAuth()
  const [showLogin, setShowLogin] = useState(true)

  if (loading) {
    return (
      <div style={{
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        minHeight: '100vh',
        fontSize: '1.25rem',
        color: 'var(--text-secondary)',
      }}>
        Loading...
      </div>
    )
  }

  if (!user) {
    return showLogin ? (
      <Login onToggle={() => setShowLogin(false)} />
    ) : (
      <SignUp onToggle={() => setShowLogin(true)} />
    )
  }

  return <AuthenticatedApp />
}

function App() {
  return (
    <AuthProvider>
      <AppContent />
    </AuthProvider>
  )
}

export default App
