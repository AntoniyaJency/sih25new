'use client'

import { useState, useEffect } from 'react'
import { 
  Play, 
  RefreshCw, 
  AlertTriangle, 
  CheckCircle, 
  Clock,
  TrendingUp,
  Settings,
  Zap
} from 'lucide-react'

interface Conflict {
  train1_id: string
  train2_id: string
  section_id: string
  conflict_type: string
  severity: number
  resolution_options: Array<{
    action: string
    train_id: string
    delay_minutes?: number
  }>
}

interface OptimizationResult {
  status: string
  solution?: Record<string, any>
  total_delay?: number
  conflicts_resolved?: number
  execution_time: number
  message?: string
}

export default function OptimizationPanel() {
  const [isOptimizing, setIsOptimizing] = useState(false)
  const [lastResult, setLastResult] = useState<OptimizationResult | null>(null)
  const [conflicts, setConflicts] = useState<Conflict[]>([])
  const [selectedConflict, setSelectedConflict] = useState<Conflict | null>(null)
  const [optimizationSettings, setOptimizationSettings] = useState({
    timeHorizon: 60,
    includeConflictResolution: true,
    priorityWeights: {
      express: 1.0,
      local: 0.8,
      freight: 0.6,
      special: 1.2
    }
  })

  // Sample conflicts data
  useEffect(() => {
    const sampleConflicts: Conflict[] = [
      {
        train1_id: 'train_1',
        train2_id: 'train_2',
        section_id: 'section_1',
        conflict_type: 'headway',
        severity: 0.8,
        resolution_options: [
          { action: 'delay_train', train_id: 'train_1', delay_minutes: 10 },
          { action: 'delay_train', train_id: 'train_2', delay_minutes: 15 },
          { action: 'reroute_train', train_id: 'train_1' },
          { action: 'reroute_train', train_id: 'train_2' }
        ]
      },
      {
        train1_id: 'train_3',
        train2_id: 'train_4',
        section_id: 'section_2',
        conflict_type: 'platform',
        severity: 0.6,
        resolution_options: [
          { action: 'delay_train', train_id: 'train_3', delay_minutes: 5 },
          { action: 'delay_train', train_id: 'train_4', delay_minutes: 8 },
          { action: 'change_platform', train_id: 'train_3' },
          { action: 'change_platform', train_id: 'train_4' }
        ]
      }
    ]
    setConflicts(sampleConflicts)
  }, [])

  const runOptimization = async () => {
    setIsOptimizing(true)
    
    // Simulate optimization process
    setTimeout(() => {
      const result: OptimizationResult = {
        status: 'optimal',
        solution: {
          'train_1': { delay_minutes: 5 },
          'train_2': { delay_minutes: 0 },
          'train_3': { delay_minutes: 3 }
        },
        total_delay: 8,
        conflicts_resolved: 2,
        execution_time: 2.3,
        message: 'Optimization completed successfully'
      }
      
      setLastResult(result)
      setIsOptimizing(false)
    }, 3000)
  }

  const resolveConflict = (conflict: Conflict, resolution: any) => {
    // Simulate conflict resolution
    setConflicts(prev => prev.filter(c => c !== conflict))
    setSelectedConflict(null)
    
    // Re-run optimization after resolution
    setTimeout(() => {
      runOptimization()
    }, 1000)
  }

  const getSeverityColor = (severity: number) => {
    if (severity >= 0.8) return 'conflict-high'
    if (severity >= 0.5) return 'conflict-medium'
    return 'conflict-low'
  }

  const getSeverityText = (severity: number) => {
    if (severity >= 0.8) return 'High'
    if (severity >= 0.5) return 'Medium'
    return 'Low'
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <h2 className="text-2xl font-bold text-gray-900">Optimization Panel</h2>
        <div className="flex space-x-3">
          <button 
            onClick={() => setOptimizationSettings({...optimizationSettings})}
            className="btn-secondary"
          >
            <Settings className="w-4 h-4 mr-2" />
            Settings
          </button>
          <button 
            onClick={runOptimization}
            disabled={isOptimizing}
            className="btn-primary"
          >
            {isOptimizing ? (
              <>
                <RefreshCw className="w-4 h-4 mr-2 animate-spin" />
                Optimizing...
              </>
            ) : (
              <>
                <Play className="w-4 h-4 mr-2" />
                Run Optimization
              </>
            )}
          </button>
        </div>
      </div>

      {/* Optimization Settings */}
      <div className="card">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Optimization Settings</h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Time Horizon (minutes)
            </label>
            <input
              type="number"
              value={optimizationSettings.timeHorizon}
              onChange={(e) => setOptimizationSettings({
                ...optimizationSettings,
                timeHorizon: parseInt(e.target.value)
              })}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-railway-primary focus:border-transparent"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Include Conflict Resolution
            </label>
            <select
              value={optimizationSettings.includeConflictResolution ? 'true' : 'false'}
              onChange={(e) => setOptimizationSettings({
                ...optimizationSettings,
                includeConflictResolution: e.target.value === 'true'
              })}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-railway-primary focus:border-transparent"
            >
              <option value="true">Yes</option>
              <option value="false">No</option>
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Optimization Engine
            </label>
            <select className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-railway-primary focus:border-transparent">
              <option value="cp">Constraint Programming</option>
              <option value="linear">Linear Programming</option>
              <option value="genetic">Genetic Algorithm</option>
            </select>
          </div>
        </div>
      </div>

      {/* Last Optimization Result */}
      {lastResult && (
        <div className="card">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Last Optimization Result</h3>
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <div className="text-center">
              <div className="text-2xl font-bold text-gray-900">{lastResult.status}</div>
              <div className="text-sm text-gray-600">Status</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-gray-900">{lastResult.total_delay}m</div>
              <div className="text-sm text-gray-600">Total Delay</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-gray-900">{lastResult.conflicts_resolved}</div>
              <div className="text-sm text-gray-600">Conflicts Resolved</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-gray-900">{lastResult.execution_time}s</div>
              <div className="text-sm text-gray-600">Execution Time</div>
            </div>
          </div>
          {lastResult.message && (
            <div className="mt-4 p-3 bg-green-100 text-green-800 rounded-lg">
              <CheckCircle className="w-4 h-4 inline mr-2" />
              {lastResult.message}
            </div>
          )}
        </div>
      )}

      {/* Conflicts */}
      <div className="card">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Detected Conflicts</h3>
        {conflicts.length === 0 ? (
          <div className="text-center py-8 text-gray-500">
            <CheckCircle className="w-12 h-12 mx-auto mb-4 text-green-500" />
            <p>No conflicts detected</p>
          </div>
        ) : (
          <div className="space-y-4">
            {conflicts.map((conflict, index) => (
              <div 
                key={index}
                className={`p-4 rounded-lg border ${getSeverityColor(conflict.severity)}`}
              >
                <div className="flex items-center justify-between">
                  <div className="flex-1">
                    <div className="flex items-center space-x-3 mb-2">
                      <AlertTriangle className="w-5 h-5" />
                      <span className="font-medium">
                        {conflict.conflict_type.charAt(0).toUpperCase() + conflict.conflict_type.slice(1)} Conflict
                      </span>
                      <span className={`status-indicator ${getSeverityColor(conflict.severity)}`}>
                        {getSeverityText(conflict.severity)} Severity
                      </span>
                    </div>
                    <p className="text-sm text-gray-600">
                      Between Train {conflict.train1_id} and Train {conflict.train2_id} in Section {conflict.section_id}
                    </p>
                  </div>
                  <button 
                    onClick={() => setSelectedConflict(conflict)}
                    className="btn-primary text-sm"
                  >
                    Resolve
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Conflict Resolution Modal */}
      {selectedConflict && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 w-full max-w-md">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">
              Resolve Conflict
            </h3>
            
            <div className="mb-4">
              <p className="text-sm text-gray-600 mb-2">
                Conflict between Train {selectedConflict.train1_id} and Train {selectedConflict.train2_id}
              </p>
              <p className="text-sm text-gray-600">
                Type: {selectedConflict.conflict_type} | Severity: {getSeverityText(selectedConflict.severity)}
              </p>
            </div>

            <div className="space-y-3">
              <h4 className="font-medium text-gray-900">Resolution Options:</h4>
              {selectedConflict.resolution_options.map((option, index) => (
                <button
                  key={index}
                  onClick={() => resolveConflict(selectedConflict, option)}
                  className="w-full text-left p-3 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors"
                >
                  <div className="font-medium text-gray-900">
                    {option.action.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase())}
                  </div>
                  <div className="text-sm text-gray-600">
                    Train {option.train_id}
                    {option.delay_minutes && ` - Delay ${option.delay_minutes} minutes`}
                  </div>
                </button>
              ))}
            </div>

            <div className="flex justify-end space-x-3 pt-4">
              <button
                onClick={() => setSelectedConflict(null)}
                className="btn-secondary"
              >
                Cancel
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Optimization Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="card">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Performance Metrics</h3>
          <div className="space-y-3">
            <div className="flex justify-between">
              <span className="text-gray-600">Punctuality</span>
              <span className="font-medium">84.4%</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600">Average Delay</span>
              <span className="font-medium">8.5m</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600">Throughput</span>
              <span className="font-medium">87.2%</span>
            </div>
          </div>
        </div>

        <div className="card">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Optimization Stats</h3>
          <div className="space-y-3">
            <div className="flex justify-between">
              <span className="text-gray-600">Total Runs</span>
              <span className="font-medium">156</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600">Success Rate</span>
              <span className="font-medium">94.2%</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600">Avg. Time</span>
              <span className="font-medium">2.1s</span>
            </div>
          </div>
        </div>

        <div className="card">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">System Load</h3>
          <div className="space-y-3">
            <div className="flex justify-between">
              <span className="text-gray-600">CPU Usage</span>
              <span className="font-medium">23%</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600">Memory</span>
              <span className="font-medium">1.2GB</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600">Active Tasks</span>
              <span className="font-medium">3</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
