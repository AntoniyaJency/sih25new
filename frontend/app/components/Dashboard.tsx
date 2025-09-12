'use client'

import { useState, useEffect } from 'react'
import { 
  Train, 
  Clock, 
  AlertTriangle, 
  TrendingUp, 
  Activity,
  MapPin,
  Users,
  Zap
} from 'lucide-react'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, BarChart, Bar, PieChart, Pie, Cell } from 'recharts'

export default function Dashboard() {
  const [metrics, setMetrics] = useState({
    total_trains: 45,
    running_trains: 38,
    delayed_trains: 5,
    cancelled_trains: 2,
    average_delay_minutes: 8.5,
    punctuality_percentage: 84.4,
    conflicts_detected: 3,
    throughput_efficiency: 87.2
  })

  const [recentAlerts, setRecentAlerts] = useState([
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
      severity: 'success',
      message: 'Optimization completed successfully',
      timestamp: '2024-01-15T10:00:00Z',
      acknowledged: true
    }
  ])

  // Sample data for charts
  const punctualityData = [
    { time: '00:00', punctuality: 92 },
    { time: '04:00', punctuality: 88 },
    { time: '08:00', punctuality: 85 },
    { time: '12:00', punctuality: 84 },
    { time: '16:00', punctuality: 87 },
    { time: '20:00', punctuality: 90 }
  ]

  const delayData = [
    { time: '00:00', delay: 3.2 },
    { time: '04:00', delay: 5.8 },
    { time: '08:00', delay: 8.5 },
    { time: '12:00', delay: 7.2 },
    { time: '16:00', delay: 6.1 },
    { time: '20:00', delay: 4.3 }
  ]

  const trainTypeData = [
    { name: 'Express', value: 15, color: '#3b82f6' },
    { name: 'Local', value: 20, color: '#10b981' },
    { name: 'Freight', value: 8, color: '#f59e0b' },
    { name: 'Special', value: 2, color: '#ef4444' }
  ]

  const conflictData = [
    { type: 'Headway', count: 2 },
    { type: 'Platform', count: 1 },
    { type: 'Crossing', count: 0 },
    { type: 'Signal', count: 0 }
  ]

  useEffect(() => {
    // Simulate real-time updates
    const interval = setInterval(() => {
      setMetrics(prev => ({
        ...prev,
        average_delay_minutes: prev.average_delay_minutes + (Math.random() - 0.5) * 2,
        punctuality_percentage: Math.max(70, Math.min(95, prev.punctuality_percentage + (Math.random() - 0.5) * 5)),
        conflicts_detected: Math.floor(Math.random() * 6)
      }))
    }, 10000)

    return () => clearInterval(interval)
  }, [])

  const metricCards = [
    {
      title: 'Total Trains',
      value: metrics.total_trains,
      icon: Train,
      color: 'text-blue-600',
      bgColor: 'bg-blue-100'
    },
    {
      title: 'Running Trains',
      value: metrics.running_trains,
      icon: Activity,
      color: 'text-green-600',
      bgColor: 'bg-green-100'
    },
    {
      title: 'Delayed Trains',
      value: metrics.delayed_trains,
      icon: Clock,
      color: 'text-yellow-600',
      bgColor: 'bg-yellow-100'
    },
    {
      title: 'Active Conflicts',
      value: metrics.conflicts_detected,
      icon: AlertTriangle,
      color: 'text-red-600',
      bgColor: 'bg-red-100'
    }
  ]

  return (
    <div className="space-y-6">
      {/* Key Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {metricCards.map((card, index) => {
          const Icon = card.icon
          return (
            <div key={index} className="metric-card">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-gray-600">{card.title}</p>
                  <p className="text-2xl font-bold text-gray-900">{card.value}</p>
                </div>
                <div className={`p-3 rounded-full ${card.bgColor}`}>
                  <Icon className={`w-6 h-6 ${card.color}`} />
                </div>
              </div>
            </div>
          )
        })}
      </div>

      {/* Performance Metrics */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="card">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Punctuality Trend</h3>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={punctualityData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="time" />
              <YAxis domain={[70, 100]} />
              <Tooltip />
              <Line type="monotone" dataKey="punctuality" stroke="#3b82f6" strokeWidth={2} />
            </LineChart>
          </ResponsiveContainer>
        </div>

        <div className="card">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Average Delay Trend</h3>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={delayData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="time" />
              <YAxis />
              <Tooltip />
              <Line type="monotone" dataKey="delay" stroke="#ef4444" strokeWidth={2} />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Charts Row */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="card">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Train Types Distribution</h3>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={trainTypeData}
                cx="50%"
                cy="50%"
                outerRadius={80}
                dataKey="value"
                label={({ name, value }) => `${name}: ${value}`}
              >
                {trainTypeData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.color} />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </div>

        <div className="card">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Conflict Types</h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={conflictData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="type" />
              <YAxis />
              <Tooltip />
              <Bar dataKey="count" fill="#f59e0b" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Performance Indicators */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="card">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Punctuality</h3>
          <div className="text-center">
            <div className="text-4xl font-bold text-gray-900 mb-2">
              {metrics.punctuality_percentage.toFixed(1)}%
            </div>
            <div className="w-full bg-gray-200 rounded-full h-2">
              <div 
                className="bg-green-500 h-2 rounded-full transition-all duration-500"
                style={{ width: `${metrics.punctuality_percentage}%` }}
              ></div>
            </div>
            <p className="text-sm text-gray-600 mt-2">Target: 95%</p>
          </div>
        </div>

        <div className="card">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Average Delay</h3>
          <div className="text-center">
            <div className="text-4xl font-bold text-gray-900 mb-2">
              {metrics.average_delay_minutes.toFixed(1)}m
            </div>
            <div className="w-full bg-gray-200 rounded-full h-2">
              <div 
                className="bg-yellow-500 h-2 rounded-full transition-all duration-500"
                style={{ width: `${Math.min(100, (metrics.average_delay_minutes / 15) * 100)}%` }}
              ></div>
            </div>
            <p className="text-sm text-gray-600 mt-2">Target: &lt;5m</p>
          </div>
        </div>

        <div className="card">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Throughput Efficiency</h3>
          <div className="text-center">
            <div className="text-4xl font-bold text-gray-900 mb-2">
              {metrics.throughput_efficiency.toFixed(1)}%
            </div>
            <div className="w-full bg-gray-200 rounded-full h-2">
              <div 
                className="bg-blue-500 h-2 rounded-full transition-all duration-500"
                style={{ width: `${metrics.throughput_efficiency}%` }}
              ></div>
            </div>
            <p className="text-sm text-gray-600 mt-2">Target: 90%</p>
          </div>
        </div>
      </div>

      {/* Recent Alerts */}
      <div className="card">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Recent Alerts</h3>
        <div className="space-y-3">
          {recentAlerts.map((alert) => (
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
                  <p className="text-sm font-medium text-gray-900">{alert.message}</p>
                  <p className="text-xs text-gray-600 mt-1">
                    {new Date(alert.timestamp).toLocaleString()}
                  </p>
                </div>
                <div className="flex items-center space-x-2">
                  <span className={`status-indicator ${
                    alert.severity === 'critical' ? 'status-cancelled' :
                    alert.severity === 'warning' ? 'status-delayed' :
                    'status-running'
                  }`}>
                    {alert.severity}
                  </span>
                  {!alert.acknowledged && (
                    <button className="btn-primary text-xs px-2 py-1">
                      Acknowledge
                    </button>
                  )}
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}
