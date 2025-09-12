'use client'

import { useState, useEffect } from 'react'
import { 
  Train, 
  MapPin, 
  Clock, 
  AlertTriangle, 
  TrendingUp, 
  Activity,
  Settings,
  BarChart3,
  PlayCircle,
  PauseCircle
} from 'lucide-react'
import Dashboard from './components/Dashboard'
import TrainManagement from './components/TrainManagement'
import SectionManagement from './components/SectionManagement'
import OptimizationPanel from './components/OptimizationPanel'
import SimulationPanel from './components/SimulationPanel'
import MonitoringPanel from './components/MonitoringPanel'

export default function Home() {
  const [activeTab, setActiveTab] = useState('dashboard')
  const [systemStatus, setSystemStatus] = useState({
    status: 'operational',
    optimization_engine_active: true,
    websocket_connections: 0,
    active_conflicts: 0,
    system_load: 0
  })

  useEffect(() => {
    // Simulate real-time updates
    const interval = setInterval(() => {
      setSystemStatus(prev => ({
        ...prev,
        websocket_connections: Math.floor(Math.random() * 10) + 1,
        active_conflicts: Math.floor(Math.random() * 5),
        system_load: Math.random() * 0.8 + 0.1
      }))
    }, 5000)

    return () => clearInterval(interval)
  }, [])

  const tabs = [
    { id: 'dashboard', label: 'Dashboard', icon: BarChart3 },
    { id: 'trains', label: 'Trains', icon: Train },
    { id: 'sections', label: 'Sections', icon: MapPin },
    { id: 'optimization', label: 'Optimization', icon: TrendingUp },
    { id: 'simulation', label: 'Simulation', icon: PlayCircle },
    { id: 'monitoring', label: 'Monitoring', icon: Activity },
  ]

  const renderContent = () => {
    switch (activeTab) {
      case 'dashboard':
        return <Dashboard />
      case 'trains':
        return <TrainManagement />
      case 'sections':
        return <SectionManagement />
      case 'optimization':
        return <OptimizationPanel />
      case 'simulation':
        return <SimulationPanel />
      case 'monitoring':
        return <MonitoringPanel />
      default:
        return <Dashboard />
    }
  }

  return (
    <div className="flex h-screen bg-gray-50">
      {/* Sidebar */}
      <div className="w-64 bg-white shadow-lg">
        <div className="p-6">
          <h1 className="text-2xl font-bold text-gradient">
            Railway Control
          </h1>
          <p className="text-sm text-gray-600 mt-1">
            AI-Powered Traffic Control
          </p>
        </div>
        
        <nav className="mt-6">
          {tabs.map((tab) => {
            const Icon = tab.icon
            return (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`w-full flex items-center px-6 py-3 text-left transition-colors ${
                  activeTab === tab.id
                    ? 'bg-railway-primary text-white'
                    : 'text-gray-700 hover:bg-gray-100'
                }`}
              >
                <Icon className="w-5 h-5 mr-3" />
                {tab.label}
              </button>
            )
          })}
        </nav>

        {/* System Status */}
        <div className="mt-8 p-6 border-t border-gray-200">
          <h3 className="text-sm font-medium text-gray-900 mb-3">System Status</h3>
          <div className="space-y-2">
            <div className="flex items-center justify-between text-sm">
              <span className="text-gray-600">Status</span>
              <span className={`status-indicator ${
                systemStatus.status === 'operational' ? 'status-running' : 'status-delayed'
              }`}>
                {systemStatus.status}
              </span>
            </div>
            <div className="flex items-center justify-between text-sm">
              <span className="text-gray-600">Engine</span>
              <span className={`status-indicator ${
                systemStatus.optimization_engine_active ? 'status-running' : 'status-cancelled'
              }`}>
                {systemStatus.optimization_engine_active ? 'Active' : 'Inactive'}
              </span>
            </div>
            <div className="flex items-center justify-between text-sm">
              <span className="text-gray-600">Conflicts</span>
              <span className="text-gray-900">{systemStatus.active_conflicts}</span>
            </div>
            <div className="flex items-center justify-between text-sm">
              <span className="text-gray-600">Load</span>
              <span className="text-gray-900">
                {(systemStatus.system_load * 100).toFixed(1)}%
              </span>
            </div>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="flex-1 flex flex-col">
        {/* Header */}
        <header className="bg-white shadow-sm border-b border-gray-200">
          <div className="px-6 py-4">
            <div className="flex items-center justify-between">
              <h2 className="text-xl font-semibold text-gray-900 capitalize">
                {activeTab}
              </h2>
              <div className="flex items-center space-x-4">
                <div className="flex items-center space-x-2">
                  <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
                  <span className="text-sm text-gray-600">Live</span>
                </div>
                <button className="btn-secondary">
                  <Settings className="w-4 h-4 mr-2" />
                  Settings
                </button>
              </div>
            </div>
          </div>
        </header>

        {/* Content Area */}
        <main className="flex-1 overflow-auto p-6">
          {renderContent()}
        </main>
      </div>
    </div>
  )
}
