'use client'

import { useState, useEffect } from 'react'
import { 
  Activity, 
  AlertTriangle, 
  CheckCircle, 
  Clock,
  TrendingUp,
  TrendingDown,
  RefreshCw,
  Bell,
  Download
} from 'lucide-react'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, AreaChart, Area } from 'recharts'

interface Alert {
  id: string
  type: string
  severity: 'info' | 'warning' | 'critical'
  message: string
  timestamp: string
  acknowledged: boolean
}

interface PerformanceMetrics {
  timestamp: string
  total_trains: number
  running_trains: number
  delayed_trains: number
  cancelled_trains: number
  average_delay_minutes: number
  punctuality_percentage: number
  conflicts_detected: number
  throughput_efficiency: number
}

export default function MonitoringPanel() {
  const [metrics, setMetrics] = useState<PerformanceMetrics | null>(null)
  const [alerts, setAlerts] = useState<Alert[]>([])
  const [historicalData, setHistoricalData] = useState<PerformanceMetrics[]>([])
  const [systemStatus, setSystemStatus] = useState({
    status: 'operational',
    optimization_engine_active: true,
    websocket_connections: 0,
    active_conflicts: 0,
    system_load: 0
  })

  useEffect(() => {
    // Sample metrics
    const sampleMetrics: PerformanceMetrics = {
      timestamp: new Date().toISOString(),
      total_trains: 45,
      running_trains: 38,
      delayed_trains: 5,
      cancelled_trains: 2,
      average_delay_minutes: 8.5,
      punctuality_percentage: 84.4,
      conflicts_detected: 3,
      throughput_efficiency: 87.2
    }
    setMetrics(sampleMetrics)

    // Sample alerts
    const sampleAlerts: Alert[] = [
      {
        id: '1',
        type: 'conflict',
        severity: 'warning',
        message: 'Headway conflict detected between Train 12345 and Train 67890',
        timestamp: '2024-01-15T10:30:00Z',
        acknowledged: false
      },
      {
        id: '2',
        type: 'performance',
        severity: 'info',
        message: 'Punctuality dropped below 85% threshold',
        timestamp: '2024-01-15T10:15:00Z',
        acknowledged: true
      },
      {
        id: '3',
        type: 'system',
        severity: 'critical',
        message: 'Optimization engine connection lost',
        timestamp: '2024-01-15T10:00:00Z',
        acknowledged: false
      }
    ]
    setAlerts(sampleAlerts)

    // Sample historical data
    const sampleHistoricalData: PerformanceMetrics[] = Array.from({ length: 24 }, (_, i) => ({
      timestamp: new Date(Date.now() - (23 - i) * 60 * 60 * 1000).toISOString(),
      total_trains: 45 + Math.floor(Math.random() * 10 - 5),
      running_trains: 38 + Math.floor(Math.random() * 8 - 4),
      delayed_trains: 5 + Math.floor(Math.random() * 4 - 2),
      cancelled_trains: 2 + Math.floor(Math.random() * 2),
      average_delay_minutes: 8.5 + (Math.random() - 0.5) * 4,
      punctuality_percentage: 84.4 + (Math.random() - 0.5) * 10,
      conflicts_detected: 3 + Math.floor(Math.random() * 4 - 2),
      throughput_efficiency: 87.2 + (Math.random() - 0.5) * 8
    }))
    setHistoricalData(sampleHistoricalData)

    // Simulate real-time updates
    const interval = setInterval(() => {
      setMetrics(prev => prev ? {
        ...prev,
        average_delay_minutes: prev.average_delay_minutes + (Math.random() - 0.5) * 2,
        punctuality_percentage: Math.max(70, Math.min(95, prev.punctuality_percentage + (Math.random() - 0.5) * 5)),
        conflicts_detected: Math.floor(Math.random() * 6)
      } : null)

      setSystemStatus(prev => ({
        ...prev,
        websocket_connections: Math.floor(Math.random() * 10) + 1,
        active_conflicts: Math.floor(Math.random() * 5),
        system_load: Math.random() * 0.8 + 0.1
      }))
    }, 5000)

    return () => clearInterval(interval)
  }, [])

  const acknowledgeAlert = (alertId: string) => {
    setAlerts(prev => prev.map(alert => 
      alert.id === alertId ? { ...alert, acknowledged: true } : alert
    ))
  }

  const getSeverityColor = (severity: string) => {
    switch (severity) {
      case 'critical': return 'text-red-600 bg-red-100'
      case 'warning': return 'text-yellow-600 bg-yellow-100'
      case 'info': return 'text-blue-600 bg-blue-100'
      default: return 'text-gray-600 bg-gray-100'
    }
  }

  const unacknowledgedAlerts = alerts.filter(alert => !alert.acknowledged)

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <h2 className="text-2xl font-bold text-gray-900">System Monitoring</h2>
        <div className="flex space-x-3">
          <button className="btn-secondary">
            <Download className="w-4 h-4 mr-2" />
            Export Report
          </button>
          <button className="btn-primary">
            <RefreshCw className="w-4 h-4 mr-2" />
            Refresh
          </button>
        </div>
      </div>

      {/* System Status */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <div className="card">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600">System Status</p>
              <p className="text-2xl font-bold text-gray-900 capitalize">{systemStatus.status}</p>
            </div>
            <div className={`p-3 rounded-full ${
              systemStatus.status === 'operational' ? 'bg-green-100' : 'bg-red-100'
            }`}>
              <Activity className={`w-6 h-6 ${
                systemStatus.status === 'operational' ? 'text-green-600' : 'text-red-600'
              }`} />
            </div>
          </div>
        </div>

        <div className="card">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600">Optimization Engine</p>
              <p className="text-2xl font-bold text-gray-900">
                {systemStatus.optimization_engine_active ? 'Active' : 'Inactive'}
              </p>
            </div>
            <div className={`p-3 rounded-full ${
              systemStatus.optimization_engine_active ? 'bg-green-100' : 'bg-red-100'
            }`}>
              <CheckCircle className={`w-6 h-6 ${
                systemStatus.optimization_engine_active ? 'text-green-600' : 'text-red-600'
              }`} />
            </div>
          </div>
        </div>

        <div className="card">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600">Active Conflicts</p>
              <p className="text-2xl font-bold text-gray-900">{systemStatus.active_conflicts}</p>
            </div>
            <div className="p-3 rounded-full bg-yellow-100">
              <AlertTriangle className="w-6 h-6 text-yellow-600" />
            </div>
          </div>
        </div>

        <div className="card">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600">System Load</p>
              <p className="text-2xl font-bold text-gray-900">
                {(systemStatus.system_load * 100).toFixed(1)}%
              </p>
            </div>
            <div className="p-3 rounded-full bg-blue-100">
              <TrendingUp className="w-6 h-6 text-blue-600" />
            </div>
          </div>
        </div>
      </div>

      {/* Performance Metrics */}
      {metrics && (
        <div className="card">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Current Performance Metrics</h3>
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
            <div className="text-center">
              <div className="text-3xl font-bold text-gray-900 mb-2">
                {metrics.punctuality_percentage.toFixed(1)}%
              </div>
              <div className="text-sm text-gray-600">Punctuality</div>
              <div className="w-full bg-gray-200 rounded-full h-2 mt-2">
                <div 
                  className="bg-green-500 h-2 rounded-full transition-all duration-500"
                  style={{ width: `${metrics.punctuality_percentage}%` }}
                ></div>
              </div>
            </div>

            <div className="text-center">
              <div className="text-3xl font-bold text-gray-900 mb-2">
                {metrics.average_delay_minutes.toFixed(1)}m
              </div>
              <div className="text-sm text-gray-600">Average Delay</div>
              <div className="w-full bg-gray-200 rounded-full h-2 mt-2">
                <div 
                  className="bg-yellow-500 h-2 rounded-full transition-all duration-500"
                  style={{ width: `${Math.min(100, (metrics.average_delay_minutes / 15) * 100)}%` }}
                ></div>
              </div>
            </div>

            <div className="text-center">
              <div className="text-3xl font-bold text-gray-900 mb-2">
                {metrics.throughput_efficiency.toFixed(1)}%
              </div>
              <div className="text-sm text-gray-600">Throughput Efficiency</div>
              <div className="w-full bg-gray-200 rounded-full h-2 mt-2">
                <div 
                  className="bg-blue-500 h-2 rounded-full transition-all duration-500"
                  style={{ width: `${metrics.throughput_efficiency}%` }}
                ></div>
              </div>
            </div>

            <div className="text-center">
              <div className="text-3xl font-bold text-gray-900 mb-2">
                {metrics.conflicts_detected}
              </div>
              <div className="text-sm text-gray-600">Active Conflicts</div>
              <div className="w-full bg-gray-200 rounded-full h-2 mt-2">
                <div 
                  className="bg-red-500 h-2 rounded-full transition-all duration-500"
                  style={{ width: `${Math.min(100, (metrics.conflicts_detected / 10) * 100)}%` }}
                ></div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Historical Trends */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="card">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Punctuality Trend (24h)</h3>
          <ResponsiveContainer width="100%" height={300}>
            <AreaChart data={historicalData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis 
                dataKey="timestamp" 
                tickFormatter={(value) => new Date(value).toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' })}
              />
              <YAxis domain={[70, 100]} />
              <Tooltip 
                labelFormatter={(value) => new Date(value).toLocaleString()}
                formatter={(value) => [`${value}%`, 'Punctuality']}
              />
              <Area type="monotone" dataKey="punctuality_percentage" stroke="#10b981" fill="#10b981" fillOpacity={0.3} />
            </AreaChart>
          </ResponsiveContainer>
        </div>

        <div className="card">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Delay Trend (24h)</h3>
          <ResponsiveContainer width="100%" height={300}>
            <AreaChart data={historicalData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis 
                dataKey="timestamp" 
                tickFormatter={(value) => new Date(value).toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' })}
              />
              <YAxis />
              <Tooltip 
                labelFormatter={(value) => new Date(value).toLocaleString()}
                formatter={(value) => [`${value}m`, 'Average Delay']}
              />
              <Area type="monotone" dataKey="average_delay_minutes" stroke="#f59e0b" fill="#f59e0b" fillOpacity={0.3} />
            </AreaChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Alerts */}
      <div className="card">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-semibold text-gray-900">System Alerts</h3>
          <div className="flex items-center space-x-2">
            <Bell className="w-4 h-4 text-gray-400" />
            <span className="text-sm text-gray-600">
              {unacknowledgedAlerts.length} unacknowledged
            </span>
          </div>
        </div>

        <div className="space-y-3">
          {alerts.map((alert) => (
            <div 
              key={alert.id}
              className={`p-4 rounded-lg border ${
                alert.severity === 'critical' ? 'conflict-high' :
                alert.severity === 'warning' ? 'conflict-medium' :
                'conflict-low'
              }`}
            >
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <div className="flex items-center space-x-2 mb-1">
                    <span className={`status-indicator ${getSeverityColor(alert.severity)}`}>
                      {alert.severity}
                    </span>
                    <span className="text-sm text-gray-600">{alert.type}</span>
                  </div>
                  <p className="text-sm font-medium text-gray-900">{alert.message}</p>
                  <p className="text-xs text-gray-600 mt-1">
                    {new Date(alert.timestamp).toLocaleString()}
                  </p>
                </div>
                {!alert.acknowledged && (
                  <button 
                    onClick={() => acknowledgeAlert(alert.id)}
                    className="btn-primary text-xs px-3 py-1"
                  >
                    Acknowledge
                  </button>
                )}
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* System Health */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="card">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Train Status Distribution</h3>
          <div className="space-y-3">
            <div className="flex justify-between items-center">
              <span className="text-gray-600">Running</span>
              <span className="font-medium text-green-600">{metrics?.running_trains}</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-gray-600">Delayed</span>
              <span className="font-medium text-yellow-600">{metrics?.delayed_trains}</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-gray-600">Cancelled</span>
              <span className="font-medium text-red-600">{metrics?.cancelled_trains}</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-gray-600">Total</span>
              <span className="font-medium text-gray-900">{metrics?.total_trains}</span>
            </div>
          </div>
        </div>

        <div className="card">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">System Resources</h3>
          <div className="space-y-3">
            <div className="flex justify-between items-center">
              <span className="text-gray-600">CPU Usage</span>
              <span className="font-medium">23%</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-gray-600">Memory</span>
              <span className="font-medium">1.2GB / 4GB</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-gray-600">Disk Space</span>
              <span className="font-medium">45GB / 100GB</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-gray-600">Network</span>
              <span className="font-medium">125 Mbps</span>
            </div>
          </div>
        </div>

        <div className="card">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Performance KPIs</h3>
          <div className="space-y-3">
            <div className="flex justify-between items-center">
              <span className="text-gray-600">Target Punctuality</span>
              <span className="font-medium">95%</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-gray-600">Target Delay</span>
              <span className="font-medium">&lt;5m</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-gray-600">Target Throughput</span>
              <span className="font-medium">90%</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-gray-600">Uptime</span>
              <span className="font-medium text-green-600">99.8%</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
