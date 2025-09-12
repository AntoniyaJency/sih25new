'use client'

import { useState, useEffect } from 'react'
import { 
  Plus, 
  Search, 
  MapPin, 
  Settings,
  AlertTriangle,
  Clock,
  Activity
} from 'lucide-react'

interface TrackSection {
  id: string
  name: string
  start_station: string
  end_station: string
  length: number
  max_speed: number
  capacity: number
  gradient: number
  signal_spacing: number
  current_trains: number
  utilization: number
}

export default function SectionManagement() {
  const [sections, setSections] = useState<TrackSection[]>([])
  const [searchTerm, setSearchTerm] = useState('')
  const [showAddModal, setShowAddModal] = useState(false)

  useEffect(() => {
    const sampleSections: TrackSection[] = [
      {
        id: '1',
        name: 'Mumbai-Delhi Main Line',
        start_station: 'Mumbai Central',
        end_station: 'Delhi',
        length: 1384,
        max_speed: 160,
        capacity: 8,
        gradient: 2.5,
        signal_spacing: 2.0,
        current_trains: 6,
        utilization: 75
      },
      {
        id: '2',
        name: 'Mumbai-Thane Suburban',
        start_station: 'Mumbai Central',
        end_station: 'Thane',
        length: 35,
        max_speed: 80,
        capacity: 12,
        gradient: 1.0,
        signal_spacing: 1.5,
        current_trains: 10,
        utilization: 83
      },
      {
        id: '3',
        name: 'Chennai-Bangalore Line',
        start_station: 'Chennai',
        end_station: 'Bangalore',
        length: 362,
        max_speed: 120,
        capacity: 6,
        gradient: 3.2,
        signal_spacing: 2.5,
        current_trains: 4,
        utilization: 67
      }
    ]
    setSections(sampleSections)
  }, [])

  const filteredSections = sections.filter(section =>
    section.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    section.start_station.toLowerCase().includes(searchTerm.toLowerCase()) ||
    section.end_station.toLowerCase().includes(searchTerm.toLowerCase())
  )

  const getUtilizationColor = (utilization: number) => {
    if (utilization >= 90) return 'text-red-600 bg-red-100'
    if (utilization >= 75) return 'text-yellow-600 bg-yellow-100'
    return 'text-green-600 bg-green-100'
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <h2 className="text-2xl font-bold text-gray-900">Section Management</h2>
        <button 
          onClick={() => setShowAddModal(true)}
          className="btn-primary"
        >
          <Plus className="w-4 h-4 mr-2" />
          Add Section
        </button>
      </div>

      {/* Search */}
      <div className="card">
        <div className="relative">
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
          <input
            type="text"
            placeholder="Search sections..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-railway-primary focus:border-transparent"
          />
        </div>
      </div>

      {/* Sections Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {filteredSections.map((section) => (
          <div key={section.id} className="card">
            <div className="flex items-start justify-between mb-4">
              <div>
                <h3 className="text-lg font-semibold text-gray-900">{section.name}</h3>
                <p className="text-sm text-gray-600">
                  {section.start_station} → {section.end_station}
                </p>
              </div>
              <button className="text-gray-400 hover:text-gray-600">
                <Settings className="w-4 h-4" />
              </button>
            </div>

            <div className="space-y-3">
              <div className="flex justify-between items-center">
                <span className="text-sm text-gray-600">Length</span>
                <span className="text-sm font-medium">{section.length} km</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-sm text-gray-600">Max Speed</span>
                <span className="text-sm font-medium">{section.max_speed} km/h</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-sm text-gray-600">Capacity</span>
                <span className="text-sm font-medium">{section.capacity} trains</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-sm text-gray-600">Current Trains</span>
                <span className="text-sm font-medium">{section.current_trains}</span>
              </div>
            </div>

            <div className="mt-4 pt-4 border-t border-gray-200">
              <div className="flex justify-between items-center mb-2">
                <span className="text-sm text-gray-600">Utilization</span>
                <span className={`text-sm font-medium ${getUtilizationColor(section.utilization).split(' ')[0]}`}>
                  {section.utilization}%
                </span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-2">
                <div 
                  className={`h-2 rounded-full transition-all duration-500 ${
                    section.utilization >= 90 ? 'bg-red-500' :
                    section.utilization >= 75 ? 'bg-yellow-500' : 'bg-green-500'
                  }`}
                  style={{ width: `${section.utilization}%` }}
                ></div>
              </div>
            </div>

            <div className="mt-4 flex space-x-2">
              <button className="flex-1 btn-secondary text-sm">
                <MapPin className="w-3 h-3 mr-1" />
                View Details
              </button>
              <button className="flex-1 btn-primary text-sm">
                <Activity className="w-3 h-3 mr-1" />
                Monitor
              </button>
            </div>
          </div>
        ))}
      </div>

      {/* Section Details Modal */}
      {showAddModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 w-full max-w-md">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Add New Section</h3>
            
            <form className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Section Name
                </label>
                <input
                  type="text"
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-railway-primary focus:border-transparent"
                  placeholder="Enter section name"
                />
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Start Station
                  </label>
                  <input
                    type="text"
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-railway-primary focus:border-transparent"
                    placeholder="Start station"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    End Station
                  </label>
                  <input
                    type="text"
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-railway-primary focus:border-transparent"
                    placeholder="End station"
                  />
                </div>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Length (km)
                  </label>
                  <input
                    type="number"
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-railway-primary focus:border-transparent"
                    placeholder="0"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Max Speed (km/h)
                  </label>
                  <input
                    type="number"
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-railway-primary focus:border-transparent"
                    placeholder="0"
                  />
                </div>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Capacity
                  </label>
                  <input
                    type="number"
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-railway-primary focus:border-transparent"
                    placeholder="0"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Gradient (%)
                  </label>
                  <input
                    type="number"
                    step="0.1"
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-railway-primary focus:border-transparent"
                    placeholder="0.0"
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
                  Add Section
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  )
}
