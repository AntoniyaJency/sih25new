'use client'

import { useState, useEffect } from 'react'
import { 
  Play, 
  RefreshCw, 
  TrendingUp, 
  BarChart3,
  Clock,
  CheckCircle,
  AlertTriangle,
  Settings
} from 'lucide-react'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, BarChart, Bar } from 'recharts'

interface SimulationScenario {
  id: string
  name: string
  description: string
  modifications: Array<{
    type: string
    train_filter?: Record<string, any>
    delay_minutes?: number
    capacity_reduction?: number
    new_priority?: number
  }>
}

interface SimulationResult {
  scenario_name: string
  base_metrics: Record<string, any>
  modified_metrics: Record<string, any>
  improvement_percentage: number
  execution_time: number
}

export default function SimulationPanel() {
  const [scenarios, setScenarios] = useState<SimulationScenario[]>([])
  const [selectedScenario, setSelectedScenario] = useState<SimulationScenario | null>(null)
  const [isRunning, setIsRunning] = useState(false)
  const [results, setResults] = useState<SimulationResult[]>([])
  const [showScenarioModal, setShowScenarioModal] = useState(false)

  useEffect(() => {
    const sampleScenarios: SimulationScenario[] = [
      {
        id: 'delay_scenario',
        name: 'Train Delay Impact',
        description: 'Simulate impact of 30-minute delay on express train',
        modifications: [
          {
            type: 'delay_train',
            train_filter: { train_type: 'express' },
            delay_minutes: 30
          }
        ]
      },
      {
        id: 'cancellation_scenario',
        name: 'Train Cancellation',
        description: 'Simulate cancellation of local train',
        modifications: [
          {
            type: 'cancel_train',
            train_filter: { train_type: 'local' },
            limit: 1
          }
        ]
      },
      {
        id: 'maintenance_scenario',
        name: 'Track Maintenance',
        description: 'Simulate track maintenance reducing capacity',
        modifications: [
          {
            type: 'reduce_capacity',
            section_filter: { name: 'Main Line' },
            capacity_reduction: 0.5
          }
        ]
      },
      {
        id: 'priority_scenario',
        name: 'Priority Adjustment',
        description: 'Simulate increasing freight train priority',
        modifications: [
          {
            type: 'change_priority',
            train_filter: { train_type: 'freight' },
            new_priority: 8
          }
        ]
      }
    ]
    setScenarios(sampleScenarios)

    // Sample results
    const sampleResults: SimulationResult[] = [
      {
        scenario_name: 'Express Delay Impact',
        base_metrics: {
          punctuality_percentage: 84.4,
          average_delay_minutes: 8.5,
          throughput_efficiency: 87.2
        },
        modified_metrics: {
          punctuality_percentage: 78.2,
          average_delay_minutes: 12.3,
          throughput_efficiency: 82.1
        },
        improvement_percentage: -15.2,
        execution_time: 2.3
      },
      {
        scenario_name: 'Priority Adjustment',
        base_metrics: {
          punctuality_percentage: 84.4,
          average_delay_minutes: 8.5,
          throughput_efficiency: 87.2
        },
        modified_metrics: {
          punctuality_percentage: 88.7,
          average_delay_minutes: 6.8,
          throughput_efficiency: 91.3
        },
        improvement_percentage: 22.1,
        execution_time: 1.8
      }
    ]
    setResults(sampleResults)
  }, [])

  const runSimulation = async (scenario: SimulationScenario) => {
    setIsRunning(true)
    setSelectedScenario(scenario)

    // Simulate simulation process
    setTimeout(() => {
      const result: SimulationResult = {
        scenario_name: scenario.name,
        base_metrics: {
          punctuality_percentage: 84.4,
          average_delay_minutes: 8.5,
          throughput_efficiency: 87.2
        },
        modified_metrics: {
          punctuality_percentage: 84.4 + (Math.random() - 0.5) * 10,
          average_delay_minutes: 8.5 + (Math.random() - 0.5) * 5,
          throughput_efficiency: 87.2 + (Math.random() - 0.5) * 8
        },
        improvement_percentage: (Math.random() - 0.5) * 30,
        execution_time: Math.random() * 3 + 1
      }

      setResults(prev => [result, ...prev])
      setIsRunning(false)
      setSelectedScenario(null)
    }, 3000)
  }

  const getImprovementColor = (improvement: number) => {
    if (improvement > 0) return 'text-green-600 bg-green-100'
    if (improvement < -10) return 'text-red-600 bg-red-100'
    return 'text-yellow-600 bg-yellow-100'
  }

  const comparisonData = results.slice(0, 2).map(result => ({
    scenario: result.scenario_name,
    base_punctuality: result.base_metrics.punctuality_percentage,
    modified_punctuality: result.modified_metrics.punctuality_percentage,
    base_delay: result.base_metrics.average_delay_minutes,
    modified_delay: result.modified_metrics.average_delay_minutes
  }))

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <h2 className="text-2xl font-bold text-gray-900">Simulation Panel</h2>
        <button 
          onClick={() => setShowScenarioModal(true)}
          className="btn-primary"
        >
          <Settings className="w-4 h-4 mr-2" />
          Create Scenario
        </button>
      </div>

      {/* Available Scenarios */}
      <div className="card">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Available Scenarios</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {scenarios.map((scenario) => (
            <div key={scenario.id} className="border border-gray-200 rounded-lg p-4">
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <h4 className="font-medium text-gray-900">{scenario.name}</h4>
                  <p className="text-sm text-gray-600 mt-1">{scenario.description}</p>
                  <div className="mt-2">
                    <span className="text-xs text-gray-500">
                      {scenario.modifications.length} modification(s)
                    </span>
                  </div>
                </div>
                <button
                  onClick={() => runSimulation(scenario)}
                  disabled={isRunning}
                  className="btn-primary text-sm"
                >
                  {isRunning && selectedScenario?.id === scenario.id ? (
                    <>
                      <RefreshCw className="w-3 h-3 mr-1 animate-spin" />
                      Running...
                    </>
                  ) : (
                    <>
                      <Play className="w-3 h-3 mr-1" />
                      Run
                    </>
                  )}
                </button>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Simulation Results */}
      {results.length > 0 && (
        <div className="card">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Simulation Results</h3>
          <div className="space-y-4">
            {results.map((result, index) => (
              <div key={index} className="border border-gray-200 rounded-lg p-4">
                <div className="flex items-center justify-between mb-3">
                  <h4 className="font-medium text-gray-900">{result.scenario_name}</h4>
                  <span className={`status-indicator ${getImprovementColor(result.improvement_percentage)}`}>
                    {result.improvement_percentage > 0 ? '+' : ''}{result.improvement_percentage.toFixed(1)}%
                  </span>
                </div>
                
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  <div className="text-center">
                    <div className="text-sm text-gray-600">Punctuality</div>
                    <div className="text-lg font-semibold">
                      {result.base_metrics.punctuality_percentage.toFixed(1)}% → {result.modified_metrics.punctuality_percentage.toFixed(1)}%
                    </div>
                  </div>
                  <div className="text-center">
                    <div className="text-sm text-gray-600">Average Delay</div>
                    <div className="text-lg font-semibold">
                      {result.base_metrics.average_delay_minutes.toFixed(1)}m → {result.modified_metrics.average_delay_minutes.toFixed(1)}m
                    </div>
                  </div>
                  <div className="text-center">
                    <div className="text-sm text-gray-600">Throughput</div>
                    <div className="text-lg font-semibold">
                      {result.base_metrics.throughput_efficiency.toFixed(1)}% → {result.modified_metrics.throughput_efficiency.toFixed(1)}%
                    </div>
                  </div>
                </div>
                
                <div className="mt-3 text-sm text-gray-600">
                  Execution time: {result.execution_time.toFixed(2)}s
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Comparison Chart */}
      {comparisonData.length > 0 && (
        <div className="card">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Scenario Comparison</h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={comparisonData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="scenario" />
              <YAxis />
              <Tooltip />
              <Bar dataKey="base_punctuality" fill="#3b82f6" name="Base Punctuality" />
              <Bar dataKey="modified_punctuality" fill="#10b981" name="Modified Punctuality" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      )}

      {/* Performance Impact Analysis */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="card">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Performance Impact</h3>
          <div className="space-y-3">
            <div className="flex justify-between items-center">
              <span className="text-gray-600">Best Improvement</span>
              <span className="font-medium text-green-600">
                +{Math.max(...results.map(r => r.improvement_percentage)).toFixed(1)}%
              </span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-gray-600">Worst Impact</span>
              <span className="font-medium text-red-600">
                {Math.min(...results.map(r => r.improvement_percentage)).toFixed(1)}%
              </span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-gray-600">Average Execution Time</span>
              <span className="font-medium">
                {(results.reduce((sum, r) => sum + r.execution_time, 0) / results.length).toFixed(2)}s
              </span>
            </div>
          </div>
        </div>

        <div className="card">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Recommendations</h3>
          <div className="space-y-3">
            {results.length > 0 && (
              <>
                <div className="flex items-start space-x-2">
                  <CheckCircle className="w-4 h-4 text-green-500 mt-0.5" />
                  <span className="text-sm text-gray-700">
                    Priority adjustment scenarios show consistent improvements
                  </span>
                </div>
                <div className="flex items-start space-x-2">
                  <AlertTriangle className="w-4 h-4 text-yellow-500 mt-0.5" />
                  <span className="text-sm text-gray-700">
                    Delay scenarios require careful consideration of cascading effects
                  </span>
                </div>
                <div className="flex items-start space-x-2">
                  <TrendingUp className="w-4 h-4 text-blue-500 mt-0.5" />
                  <span className="text-sm text-gray-700">
                    Capacity reduction scenarios need alternative routing strategies
                  </span>
                </div>
              </>
            )}
          </div>
        </div>
      </div>

      {/* Create Scenario Modal */}
      {showScenarioModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 w-full max-w-lg">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Create New Scenario</h3>
            
            <form className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Scenario Name
                </label>
                <input
                  type="text"
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-railway-primary focus:border-transparent"
                  placeholder="Enter scenario name"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Description
                </label>
                <textarea
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-railway-primary focus:border-transparent"
                  rows={3}
                  placeholder="Describe the scenario"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Modification Type
                </label>
                <select className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-railway-primary focus:border-transparent">
                  <option value="delay_train">Delay Train</option>
                  <option value="cancel_train">Cancel Train</option>
                  <option value="reduce_capacity">Reduce Capacity</option>
                  <option value="change_priority">Change Priority</option>
                </select>
              </div>

              <div className="flex justify-end space-x-3 pt-4">
                <button
                  type="button"
                  onClick={() => setShowScenarioModal(false)}
                  className="btn-secondary"
                >
                  Cancel
                </button>
                <button type="submit" className="btn-primary">
                  Create Scenario
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  )
}
