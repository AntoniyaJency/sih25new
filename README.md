# Railway Traffic Control System
## Smart India Hackathon 2025 - Ministry of Railways

### 🚂 **AI-Powered Decision Support System for Railway Traffic Control**

A comprehensive web application that maximizes section throughput using intelligent decision support for railway traffic controllers across India's vast railway network.

---

## 🌟 **Key Features**

### **Real-time Monitoring & Control**
- **Live Railway Map**: Interactive map showing all trains, stations, and tracks across India
- **Real-time Tracking**: Live train position updates with movement simulation
- **Comprehensive Network**: 124+ major stations and 86+ track segments covering all railway zones

### **AI-Powered Optimization**
- **Conflict Detection**: Advanced algorithms for identifying and resolving train conflicts
- **Route Optimization**: Multi-objective optimization for maximum throughput
- **Dynamic Re-optimization**: Rapid response to disruptions and schedule changes

### **Professional Dashboard**
- **System Overview**: Real-time statistics and KPIs
- **Train Management**: Complete train information and status tracking
- **Performance Analytics**: Punctuality rates, efficiency metrics, and delay analysis

### **Advanced Features**
- **What-if Simulation**: Scenario analysis and disruption handling
- **Predictive Analytics**: Machine learning for proactive management
- **Audit Trails**: Complete logging and performance tracking

---

## 🚀 **Quick Start**

### **Prerequisites**
- Python 3.8+
- Node.js (for frontend development)
- Modern web browser

### **Installation**

1. **Clone the repository**
   ```bash
   git clone https://github.com/AntoniyaJency/sih25new.git
   cd sih25new
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Start the backend server**
   ```bash
   python3 realtime_railway_map.py &
   ```

4. **Start the web server**
   ```bash
   python3 -m http.server 8084 --bind 127.0.0.1 &
   ```

5. **Open the application**
   ```
   http://localhost:8084/index.html
   ```

---

## 📱 **Website Navigation**

### **Complete Navigation Flow**

The website features a comprehensive navigation system with the following pages:

#### **🏠 Home Page**
- Hero section with system overview
- Feature highlights and capabilities
- Quick access buttons to main sections

#### **📊 Dashboard**
- Real-time system statistics
- Active train count and status
- Recent train activity feed
- System efficiency metrics

#### **🗺️ Live Map**
- Interactive railway network map
- Real-time train positions
- Station and track information
- Clickable markers with detailed popups

#### **🚂 Trains**
- Complete train management interface
- Train status and route information
- Speed and location tracking
- Status indicators (Running, Delayed, On-time, Maintenance)

#### **📈 Analytics**
- Performance metrics and KPIs
- Punctuality rates and efficiency data
- Conflict resolution statistics
- Average delay calculations

#### **ℹ️ About**
- System mission and technology overview
- Impact and future roadmap
- Technical specifications

---

## 🛠️ **Technical Architecture**

### **Backend (Python)**
- **FastAPI**: High-performance web framework
- **Google OR-Tools**: Advanced optimization algorithms
- **SQLAlchemy**: Database ORM and management
- **WebSockets**: Real-time communication
- **Redis**: Caching and session management

### **Frontend (HTML/CSS/JavaScript)**
- **Responsive Design**: Mobile-first approach
- **Leaflet.js**: Interactive mapping
- **Modern CSS**: Advanced styling with animations
- **Vanilla JavaScript**: Clean, efficient code
- **Auto-refresh**: Real-time data updates

### **Data Management**
- **PostgreSQL**: Robust data storage
- **Pydantic**: Data validation and serialization
- **Real-time Updates**: Live data synchronization

---

## 🎯 **Key Capabilities**

### **Comprehensive Indian Railway Network**
- **124 Major Stations** across all railway zones
- **86 Track Segments** covering Golden Quadrilateral routes
- **50+ Realistic Trains** including Rajdhani, Shatabdi, Duronto, Vande Bharat

### **Real-time Features**
- **Live Train Tracking**: Real-time position updates
- **Interactive Map**: Clickable stations and trains
- **Status Monitoring**: Real-time status updates
- **Auto-refresh**: Data updates every 30 seconds

### **Professional Interface**
- **Responsive Design**: Works on all devices
- **Smooth Animations**: Enhanced user experience
- **Mobile Navigation**: Hamburger menu for mobile
- **Keyboard Shortcuts**: Alt+1-6 for quick navigation

---

## 📊 **System Statistics**

- **Stations**: 124+ major Indian railway stations
- **Tracks**: 86+ track segments
- **Trains**: 50+ active trains
- **Coverage**: All major railway zones
- **Routes**: Golden Quadrilateral and regional routes

---

## 🔧 **Development**

### **File Structure**
```
sih25new/
├── index.html              # Main website
├── css/
│   └── styles.css          # Main stylesheet
├── js/
│   └── app.js              # Application logic
├── realtime_railway_map.py # Backend server
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

### **Customization**
- Modify `css/styles.css` for styling changes
- Update `js/app.js` for functionality enhancements
- Edit `realtime_railway_map.py` for backend modifications

---

## 🌐 **Access Information**

- **Main Website**: http://localhost:8084/index.html
- **Backend API**: http://localhost:8081/api/map-data
- **Map Data**: Real-time railway network information

---

## 🏆 **Smart India Hackathon 2025**

This project was developed for the **Smart India Hackathon 2025** under the **Ministry of Railways** theme:

> **"Maximizing Section Throughput Using AI-Powered Precise Train Traffic Control"**

### **Problem Statement**
Develop an intelligent decision-support system for section controllers that leverages operations research and AI to model constraints, train priorities, and operational rules for conflict-free, feasible schedules.

### **Solution**
A comprehensive web application with real-time monitoring, AI-powered optimization, and professional user interface for railway traffic control across India's vast network.

---

## 📞 **Support**

For technical support or questions about the Railway Traffic Control System:

- **GitHub**: https://github.com/AntoniyaJency/sih25new
- **Documentation**: See inline code comments
- **Issues**: Report via GitHub Issues

---

## 📄 **License**

This project is developed for the Smart India Hackathon 2025 and is intended for educational and demonstration purposes.

---

**🚂 Railway Traffic Control System - Revolutionizing Indian Railways with AI-Powered Intelligence**