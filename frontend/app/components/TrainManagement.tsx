'use client'

import { useState, useEffect } from 'react'
import { 
  Plus, 
  Search, 
  Filter, 
  MoreVertical, 
  Clock, 
  MapPin,
  AlertTriangle,
  Play,
  Pause,
  Edit,
  Trash2
} from 'lucide-react'

interface Train {
  id: string
  train_number: string
  train_type: 'express' | 'local' | 'freight' | 'special'
  priority: number
  origin: string
  destination: string
  scheduled_departure: string
  scheduled_arrival: string
  current_location: string
  speed: number
  length: number
  weight: number
  status: 'scheduled' | 'running' | 'delayed' | 'cancelled' | 'maintenance'
}

export default function TrainManagement() {
  const [trains, setTrains] = useState<Train[]>([])
  const [filteredTrains, setFilteredTrains] = useState<Train[]>([])
  const [searchTerm, setSearchTerm] = useState('')
  const [filterType, setFilterType] = useState('all')
  const [filterStatus, setFilterStatus] = useState('all')
  const [showAddModal, setShowAddModal] = useState(false)
  const [selectedTrain, setSelectedTrain] = useState<Train | null>(null)

  // Sample data
  useEffect(() => {
    const sampleTrains: Train[] = [
      {
        id: '1',
        train_number: '12345',
        train_type: 'express',
        priority: 8,
        origin: 'Mumbai Central',
        destination: 'Delhi',
        scheduled_departure: '2024-01-15T08:00:00Z',
        scheduled_arrival: '2024-01-15T14:30:00Z',
        current_location: 'Mumbai Central',
        speed: 120,
        length: 450,
        weight: 1200,
        status: 'running'
      },
      {
        id: '2',
        train_number: '67890',
        train_type: 'local',
        priority: 5,
        origin: 'Mumbai Central',
        destination: 'Thane',
        scheduled_departure: '2024-01-15T09:15:00Z',
        scheduled_arrival: '2024-01-15T10:00:00Z',
        current_location: 'Kurla',
        speed: 60,
        length: 200,
        weight: 400,
        status: 'delayed'
      },
      {
        id: '3',
        train_number: '11111',
        train_type: 'freight',
        priority: 6,
        origin: 'Chennai',
        destination: 'Bangalore',
        scheduled_departure: '2024-01-15T10:30:00Z',
        scheduled_arrival: '2024-01-15T16:45:00Z',
        current_location: 'Chennai',
        speed: 80,
        length: 600,
        weight: 2000,
        status: 'scheduled'
      }
    ]
    setTrains(sampleTrains)
    setFilteredTrains(sampleTrains)
  }, [])

  // Filter trains
  useEffect(() => {
    let filtered = trains

    if (searchTerm) {
      filtered = filtered.filter(train =>
        train.train_number.toLowerCase().includes(searchTerm.toLowerCase()) ||
        train.origin.toLowerCase().includes(searchTerm.toLowerCase()) ||
        train.destination.toLowerCase().includes(searchTerm.toLowerCase())
      )
    }

    if (filterType !== 'all') {
      filtered = filtered.filter(train => train.train_type === filterType)
    }

    if (filterStatus !== 'all') {
      filtered = filtered.filter(train => train.status === filterStatus)
    }

    setFilteredTrains(filtered)
  }, [trains, searchTerm, filterType, filterStatus])

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'running': return 'status-running'
      case 'delayed': return 'status-delayed'
      case 'cancelled': return 'status-cancelled'
      case 'scheduled': return 'status-scheduled'
      default: return 'status-scheduled'
    }
  }

  const getTypeColor = (type: string) => {
    switch (type) {
      case 'express': return 'bg-blue-100 text-blue-800'
      case 'local': return 'bg-green-100 text-green-800'
      case 'freight': return 'bg-yellow-100 text-yellow-800'
      case 'special': return 'bg-purple-100 text-purple-800'
      default: return 'bg-gray-100 text-gray-800'
    }
  }

  const formatTime = (timeString: string) => {
    return new Date(timeString).toLocaleTimeString('en-US', {
      hour: '2-digit',
      minute: '2-digit'
    })
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <h2 className="text-2xl font-bold text-gray-900">Train Management</h2>
        <button 
          onClick={() => setShowAddModal(true)}
          className="btn-primary"
        >
          <Plus className="w-4 h-4 mr-2" />
          Add Train
        </button>
      </div>

      {/* Filters */}
      <div className="card">
        <div className="flex flex-wrap gap-4">
          <div className="flex-1 min-w-64">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
              <input
                type="text"
                placeholder="Search trains..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-railway-primary focus:border-transparent"
              />
            </div>
          </div>
          
          <select
            value={filterType}
            onChange={(e) => setFilterType(e.target.value)}
            className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-railway-primary focus:border-transparent"
          >
            <option value="all">All Types</option>
            <option value="express">Express</option>
            <option value="local">Local</option>
            <option value="freight">Freight</option>
            <option value="special">Special</option>
          </select>

          <select
            value={filterStatus}
            onChange={(e) => setFilterStatus(e.target.value)}
            className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-railway-primary focus:border-transparent"
          >
            <option value="all">All Status</option>
            <option value="scheduled">Scheduled</option>
            <option value="running">Running</option>
            <option value="delayed">Delayed</option>
            <option value="cancelled">Cancelled</option>
            <option value="maintenance">Maintenance</option>
          </select>
        </div>
      </div>

      {/* Trains Table */}
      <div className="card">
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="border-b border-gray-200">
                <th className="text-left py-3 px-4 font-medium text-gray-900">Train</th>
                <th className="text-left py-3 px-4 font-medium text-gray-900">Type</th>
                <th className="text-left py-3 px-4 font-medium text-gray-900">Route</th>
                <th className="text-left py-3 px-4 font-medium text-gray-900">Schedule</th>
                <th className="text-left py-3 px-4 font-medium text-gray-900">Status</th>
                <th className="text-left py-3 px-4 font-medium text-gray-900">Priority</th>
                <th className="text-left py-3 px-4 font-medium text-gray-900">Actions</th>
              </tr>
            </thead>
            <tbody>
              {filteredTrains.map((train) => (
                <tr key={train.id} className="border-b border-gray-100 hover:bg-gray-50">
                  <td className="py-4 px-4">
                    <div>
                      <div className="font-medium text-gray-900">{train.train_number}</div>
                      <div className="text-sm text-gray-600">{train.current_location}</div>
                    </div>
                  </td>
                  <td className="py-4 px-4">
                    <span className={`status-indicator ${getTypeColor(train.train_type)}`}>
                      {train.train_type}
                    </span>
                  </td>
                  <td className="py-4 px-4">
                    <div className="text-sm">
                      <div className="text-gray-900">{train.origin}</div>
                      <div className="text-gray-600">→ {train.destination}</div>
                    </div>
                  </td>
                  <td className="py-4 px-4">
                    <div className="text-sm">
                      <div className="text-gray-900">{formatTime(train.scheduled_departure)}</div>
                      <div className="text-gray-600">→ {formatTime(train.scheduled_arrival)}</div>
                    </div>
                  </td>
                  <td className="py-4 px-4">
                    <span className={`status-indicator ${getStatusColor(train.status)}`}>
                      {train.status}
                    </span>
                  </td>
                  <td className="py-4 px-4">
                    <div className="flex items-center">
                      <div className="w-16 bg-gray-200 rounded-full h-2 mr-2">
                        <div 
                          className="bg-railway-primary h-2 rounded-full"
                          style={{ width: `${train.priority * 10}%` }}
                        ></div>
                      </div>
                      <span className="text-sm text-gray-600">{train.priority}</span>
                    </div>
                  </td>
                  <td className="py-4 px-4">
                    <div className="flex items-center space-x-2">
                      <button 
                        onClick={() => setSelectedTrain(train)}
                        className="text-gray-400 hover:text-gray-600"
                      >
                        <Edit className="w-4 h-4" />
                      </button>
                      <button className="text-gray-400 hover:text-gray-600">
                        <MoreVertical className="w-4 h-4" />
                      </button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {filteredTrains.length === 0 && (
          <div className="text-center py-8 text-gray-500">
            No trains found matching your criteria
          </div>
        )}
      </div>

      {/* Add Train Modal */}
      {showAddModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 w-full max-w-md">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Add New Train</h3>
            
            <form className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Train Number
                </label>
                <input
                  type="text"
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-railway-primary focus:border-transparent"
                  placeholder="Enter train number"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Train Type
                </label>
                <select className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-railway-primary focus:border-transparent">
                  <option value="express">Express</option>
                  <option value="local">Local</option>
                  <option value="freight">Freight</option>
                  <option value="special">Special</option>
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Priority (1-10)
                </label>
                <input
                  type="number"
                  min="1"
                  max="10"
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-railway-primary focus:border-transparent"
                  placeholder="5"
                />
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Origin
                  </label>
                  <input
                    type="text"
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-railway-primary focus:border-transparent"
                    placeholder="Origin station"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Destination
                  </label>
                  <input
                    type="text"
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-railway-primary focus:border-transparent"
                    placeholder="Destination station"
                  />
                </div>
              </div>

              <div className="flex justify-end space-x-3 pt-4">
                <button
                  type="button"
                  onClick={() => setShowAddModal(false)}
                  className="btn-secondary"
                >
                  Cancel
                </button>
                <button type="submit" className="btn-primary">
                  Add Train
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  )
}
