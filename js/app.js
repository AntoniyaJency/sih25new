// Railway Traffic Control System - Main Application JavaScript

class RailwayApp {
    constructor() {
        this.currentPage = 'home';
        this.map = null;
        this.mapData = null;
        this.refreshInterval = null;
        this.init();
    }

    init() {
        this.setupNavigation();
        this.setupEventListeners();
        this.loadInitialData();
        this.startAutoRefresh();
    }

    setupNavigation() {
        // Add click event listeners to navigation links
        document.querySelectorAll('.nav-link').forEach(link => {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                const pageId = this.getPageIdFromElement(e.target);
                this.showPage(pageId);
            });
        });

        // Mobile menu toggle
        const mobileToggle = document.querySelector('.mobile-menu-toggle');
        if (mobileToggle) {
            mobileToggle.addEventListener('click', () => {
                const navLinks = document.querySelector('.nav-links');
                navLinks.classList.toggle('active');
            });
        }
    }

    setupEventListeners() {
        // Add keyboard navigation
        document.addEventListener('keydown', (e) => {
            if (e.altKey) {
                switch(e.key) {
                    case '1': this.showPage('home'); break;
                    case '2': this.showPage('dashboard'); break;
                    case '3': this.showPage('map'); break;
                    case '4': this.showPage('trains'); break;
                    case '5': this.showPage('analytics'); break;
                    case '6': this.showPage('about'); break;
                }
            }
        });

        // Add window resize handler
        window.addEventListener('resize', () => {
            if (this.map) {
                setTimeout(() => this.map.invalidateSize(), 100);
            }
        });
    }

    getPageIdFromElement(element) {
        return element.getAttribute('data-page') || element.closest('[data-page]')?.getAttribute('data-page');
    }

    showPage(pageId) {
        // Hide all pages
        document.querySelectorAll('.page').forEach(page => {
            page.classList.remove('active');
        });
        
        // Remove active class from all nav links
        document.querySelectorAll('.nav-link').forEach(link => {
            link.classList.remove('active');
        });
        
        // Show selected page
        const targetPage = document.getElementById(pageId);
        if (targetPage) {
            targetPage.classList.add('active');
            this.currentPage = pageId;
            
            // Add active class to clicked nav link
            const activeLink = document.querySelector(`[data-page="${pageId}"]`);
            if (activeLink) {
                activeLink.classList.add('active');
            }
            
            // Load page-specific data
            this.loadPageData(pageId);
            
            // Close mobile menu if open
            const navLinks = document.querySelector('.nav-links');
            if (navLinks) {
                navLinks.classList.remove('active');
            }
        }
    }

    async loadPageData(pageId) {
        switch(pageId) {
            case 'dashboard':
                await this.loadDashboardData();
                break;
            case 'map':
                this.initMap();
                break;
            case 'trains':
                await this.loadTrainsData();
                break;
            case 'analytics':
                await this.loadAnalyticsData();
                break;
        }
    }

    async loadInitialData() {
        try {
            const response = await fetch('http://localhost:8081/api/map-data');
            this.mapData = await response.json();
            console.log('Initial data loaded:', this.mapData);
        } catch (error) {
            console.error('Failed to load initial data:', error);
            this.showError('Failed to connect to the railway system. Please check if the backend is running.');
        }
    }

    async loadDashboardData() {
        if (!this.mapData) {
            await this.loadInitialData();
        }

        if (this.mapData) {
            this.updateDashboardStats();
            this.updateRecentTrains();
        }
    }

    updateDashboardStats() {
        const stats = {
            'total-stations': this.mapData.stations.length,
            'total-trains': this.mapData.trains.length,
            'total-tracks': this.mapData.tracks.length,
            'system-efficiency': this.calculateSystemEfficiency()
        };

        Object.entries(stats).forEach(([id, value]) => {
            const element = document.getElementById(id);
            if (element) {
                this.animateNumber(element, value);
            }
        });
    }

    calculateSystemEfficiency() {
        // Simulate efficiency calculation based on train status
        const runningTrains = this.mapData.trains.filter(train => train.status === 'running').length;
        const totalTrains = this.mapData.trains.length;
        const baseEfficiency = (runningTrains / totalTrains) * 100;
        return Math.round(baseEfficiency + Math.random() * 10); // Add some variance
    }

    animateNumber(element, targetValue) {
        const startValue = parseInt(element.textContent) || 0;
        const duration = 1000;
        const startTime = performance.now();

        const animate = (currentTime) => {
            const elapsed = currentTime - startTime;
            const progress = Math.min(elapsed / duration, 1);
            const currentValue = Math.round(startValue + (targetValue - startValue) * progress);
            
            element.textContent = typeof targetValue === 'string' ? targetValue : currentValue;
            
            if (progress < 1) {
                requestAnimationFrame(animate);
            }
        };

        requestAnimationFrame(animate);
    }

    updateRecentTrains() {
        const recentTrainsContainer = document.getElementById('recent-trains');
        if (!recentTrainsContainer) return;

        const recentTrains = this.mapData.trains.slice(0, 5);
        const trainsHtml = recentTrains.map(train => this.createTrainItemHtml(train)).join('');
        
        recentTrainsContainer.innerHTML = trainsHtml;
    }

    createTrainItemHtml(train) {
        const statusClass = this.getStatusClass(train.status);
        const statusText = this.getStatusText(train.status);
        
        return `
            <div class="train-item">
                <div class="train-info">
                    <h4>${train.train_number} - ${train.train_type}</h4>
                    <p>${train.origin} → ${train.destination}</p>
                    <p>Current: ${train.current_station} | Speed: ${train.speed} km/h</p>
                </div>
                <div class="train-status ${statusClass}">${statusText}</div>
            </div>
        `;
    }

    getStatusClass(status) {
        const statusMap = {
            'running': 'status-running',
            'delayed': 'status-delayed',
            'on-time': 'status-on-time',
            'maintenance': 'status-maintenance'
        };
        return statusMap[status] || 'status-running';
    }

    getStatusText(status) {
        const statusMap = {
            'running': 'Running',
            'delayed': 'Delayed',
            'on-time': 'On Time',
            'maintenance': 'Maintenance'
        };
        return statusMap[status] || 'Running';
    }

    initMap() {
        if (this.map) return; // Map already initialized
        
        const mapContainer = document.getElementById('railway-map');
        if (!mapContainer) return;

        this.map = L.map('railway-map').setView([20.5937, 78.9629], 5);
        
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '© OpenStreetMap contributors'
        }).addTo(this.map);
        
        this.loadMapData();
    }

    async loadMapData() {
        if (!this.mapData) {
            await this.loadInitialData();
        }

        if (this.mapData && this.map) {
            this.addStationsToMap();
            this.addTracksToMap();
            this.addTrainsToMap();
        }
    }

    addStationsToMap() {
        this.mapData.stations.forEach(station => {
            const marker = L.marker([station.lat, station.lon]).addTo(this.map);
            marker.bindPopup(`
                <div style="min-width: 200px;">
                    <h3 style="margin: 0 0 10px 0; color: #2c3e50;">${station.name}</h3>
                    <p style="margin: 5px 0;"><strong>Type:</strong> ${station.type}</p>
                    <p style="margin: 5px 0;"><strong>Platforms:</strong> ${station.platforms}</p>
                    <p style="margin: 5px 0;"><strong>ID:</strong> ${station.id}</p>
                </div>
            `);
        });
    }

    addTracksToMap() {
        this.mapData.tracks.forEach(track => {
            const fromStation = this.mapData.stations.find(s => s.id === track.from_station);
            const toStation = this.mapData.stations.find(s => s.id === track.to_station);
            
            if (fromStation && toStation) {
                const polyline = L.polyline([
                    [fromStation.lat, fromStation.lon],
                    [toStation.lat, toStation.lon]
                ], {
                    color: this.getTrackColor(track.track_type),
                    weight: this.getTrackWeight(track.track_type),
                    opacity: 0.8
                }).addTo(this.map);
                
                polyline.bindPopup(`
                    <div style="min-width: 200px;">
                        <h4 style="margin: 0 0 10px 0;">Track Segment</h4>
                        <p style="margin: 5px 0;"><strong>From:</strong> ${fromStation.name}</p>
                        <p style="margin: 5px 0;"><strong>To:</strong> ${toStation.name}</p>
                        <p style="margin: 5px 0;"><strong>Distance:</strong> ${track.distance} km</p>
                        <p style="margin: 5px 0;"><strong>Max Speed:</strong> ${track.max_speed} km/h</p>
                        <p style="margin: 5px 0;"><strong>Type:</strong> ${track.track_type}</p>
                    </div>
                `);
            }
        });
    }

    addTrainsToMap() {
        this.mapData.trains.forEach(train => {
            const currentStation = this.mapData.stations.find(s => s.id === train.current_station);
            if (currentStation) {
                const trainIcon = L.divIcon({
                    className: 'train-marker',
                    html: this.getTrainIcon(train.train_type),
                    iconSize: [25, 25],
                    iconAnchor: [12, 12]
                });
                
                const trainMarker = L.marker([currentStation.lat, currentStation.lon], {
                    icon: trainIcon
                }).addTo(this.map);
                
                trainMarker.bindPopup(`
                    <div style="min-width: 250px;">
                        <h3 style="margin: 0 0 10px 0; color: #2c3e50;">${train.train_number}</h3>
                        <p style="margin: 5px 0;"><strong>Type:</strong> ${train.train_type}</p>
                        <p style="margin: 5px 0;"><strong>Route:</strong> ${train.origin} → ${train.destination}</p>
                        <p style="margin: 5px 0;"><strong>Current:</strong> ${train.current_station}</p>
                        <p style="margin: 5px 0;"><strong>Next:</strong> ${train.next_station}</p>
                        <p style="margin: 5px 0;"><strong>Speed:</strong> ${train.speed} km/h</p>
                        <p style="margin: 5px 0;"><strong>Status:</strong> ${train.status}</p>
                    </div>
                `);
            }
        });
    }

    getTrackColor(trackType) {
        const colors = {
            'main': '#3498db',
            'suburban': '#e74c3c',
            'branch': '#f39c12',
            'freight': '#95a5a6'
        };
        return colors[trackType] || '#3498db';
    }

    getTrackWeight(trackType) {
        const weights = {
            'main': 4,
            'suburban': 3,
            'branch': 2,
            'freight': 2
        };
        return weights[trackType] || 3;
    }

    getTrainIcon(trainType) {
        const icons = {
            'Rajdhani Express': '🚄',
            'Shatabdi Express': '🚅',
            'Duronto Express': '🚆',
            'Vande Bharat Express': '🚈',
            'Express': '🚂',
            'Mail': '🚃',
            'Freight': '🚛',
            'Local': '🚋'
        };
        return icons[trainType] || '🚂';
    }

    async loadTrainsData() {
        if (!this.mapData) {
            await this.loadInitialData();
        }

        const allTrainsContainer = document.getElementById('all-trains');
        if (!allTrainsContainer) return;

        const trainsHtml = this.mapData.trains.map(train => this.createTrainItemHtml(train)).join('');
        allTrainsContainer.innerHTML = trainsHtml;
    }

    async loadAnalyticsData() {
        // Simulate analytics data loading
        const analyticsCards = document.querySelectorAll('#analytics .stat-card .stat-number');
        if (analyticsCards.length > 0) {
            const analyticsData = {
                0: '95.2%', // Punctuality Rate
                1: '87.5%', // Throughput Efficiency
                2: '12',     // Conflicts Resolved
                3: '2.3 min' // Average Delay
            };

            analyticsCards.forEach((card, index) => {
                if (analyticsData[index]) {
                    this.animateNumber(card, analyticsData[index]);
                }
            });
        }
    }

    startAutoRefresh() {
        // Refresh data every 30 seconds
        this.refreshInterval = setInterval(() => {
            if (this.currentPage === 'dashboard' || this.currentPage === 'map' || this.currentPage === 'trains') {
                this.loadInitialData().then(() => {
                    this.loadPageData(this.currentPage);
                });
            }
        }, 30000);
    }

    showError(message) {
        // Create error notification
        const errorDiv = document.createElement('div');
        errorDiv.className = 'error';
        errorDiv.textContent = message;
        errorDiv.style.position = 'fixed';
        errorDiv.style.top = '100px';
        errorDiv.style.right = '20px';
        errorDiv.style.zIndex = '10000';
        errorDiv.style.maxWidth = '300px';
        
        document.body.appendChild(errorDiv);
        
        // Remove after 5 seconds
        setTimeout(() => {
            if (errorDiv.parentNode) {
                errorDiv.parentNode.removeChild(errorDiv);
            }
        }, 5000);
    }

    destroy() {
        if (this.refreshInterval) {
            clearInterval(this.refreshInterval);
        }
        if (this.map) {
            this.map.remove();
        }
    }
}

// Initialize the application when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.railwayApp = new RailwayApp();
});

// Handle page visibility changes
document.addEventListener('visibilitychange', () => {
    if (document.hidden) {
        // Page is hidden, pause updates
        if (window.railwayApp && window.railwayApp.refreshInterval) {
            clearInterval(window.railwayApp.refreshInterval);
        }
    } else {
        // Page is visible, resume updates
        if (window.railwayApp) {
            window.railwayApp.startAutoRefresh();
        }
    }
});

// Handle page unload
window.addEventListener('beforeunload', () => {
    if (window.railwayApp) {
        window.railwayApp.destroy();
    }
});
