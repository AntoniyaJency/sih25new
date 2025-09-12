#!/usr/bin/env python3
"""
Railway Monitoring System - Static Server
This script serves the railway monitoring system as a static website.
"""

import http.server
import socketserver
import json
import threading
import time
import random
import math
from datetime import datetime
import os

# Port configuration
PORT = int(os.environ.get('PORT', 8080))

# Sample railway data
stations = [
    {"id": "NDLS", "name": "New Delhi", "lat": 28.644800, "lon": 77.216721},
    {"id": "CSMT", "name": "Mumbai CST", "lat": 18.939800, "lon": 72.835500},
    {"id": "HWH", "name": "Howrah", "lat": 22.585320, "lon": 88.346790},
    {"id": "MAS", "name": "Chennai Central", "lat": 13.082700, "lon": 80.270721},
    {"id": "SBC", "name": "Bangalore City", "lat": 12.976750, "lon": 77.575279},
    {"id": "HYB", "name": "Hyderabad Deccan", "lat": 17.385044, "lon": 78.486671},
    {"id": "PUNE", "name": "Pune", "lat": 18.531400, "lon": 73.874359},
    {"id": "JP", "name": "Jaipur", "lat": 26.922070, "lon": 75.778885},
    {"id": "ADI", "name": "Ahmedabad", "lat": 23.022505, "lon": 72.571365},
    {"id": "LKO", "name": "Lucknow", "lat": 26.846510, "lon": 80.946166},
    {"id": "PNBE", "name": "Patna", "lat": 25.594095, "lon": 85.137565},
    {"id": "KGP", "name": "Kharagpur", "lat": 22.314930, "lon": 87.310532},
    {"id": "BZA", "name": "Vijayawada", "lat": 16.506174, "lon": 80.648018},
    {"id": "GTL", "name": "Guntakal", "lat": 15.170280, "lon": 77.364441},
    {"id": "KPD", "name": "Katpadi", "lat": 12.976750, "lon": 79.128365}
]

tracks = [
    {"from": {"id": "NDLS", "lat": 28.644800, "lon": 77.216721}, "to": {"id": "HWH", "lat": 22.585320, "lon": 88.346790}},
    {"from": {"id": "NDLS", "lat": 28.644800, "lon": 77.216721}, "to": {"id": "CSMT", "lat": 18.939800, "lon": 72.835500}},
    {"from": {"id": "CSMT", "lat": 18.939800, "lon": 72.835500}, "to": {"id": "MAS", "lat": 13.082700, "lon": 80.270721}},
    {"from": {"id": "MAS", "lat": 13.082700, "lon": 80.270721}, "to": {"id": "SBC", "lat": 12.976750, "lon": 77.575279}},
    {"from": {"id": "SBC", "lat": 12.976750, "lon": 77.575279}, "to": {"id": "HYB", "lat": 17.385044, "lon": 78.486671}},
    {"from": {"id": "HYB", "lat": 17.385044, "lon": 78.486671}, "to": {"id": "PUNE", "lat": 18.531400, "lon": 73.874359}},
    {"from": {"id": "NDLS", "lat": 28.644800, "lon": 77.216721}, "to": {"id": "JP", "lat": 26.922070, "lon": 75.778885}},
    {"from": {"id": "JP", "lat": 26.922070, "lon": 75.778885}, "to": {"id": "ADI", "lat": 23.022505, "lon": 72.571365}},
    {"from": {"id": "NDLS", "lat": 28.644800, "lon": 77.216721}, "to": {"id": "LKO", "lat": 26.846510, "lon": 80.946166}},
    {"from": {"id": "LKO", "lat": 26.846510, "lon": 80.946166}, "to": {"id": "PNBE", "lat": 25.594095, "lon": 85.137565}}
]

# Global train data
trains = []
collisions = []

class RailwayHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/api/map-data':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            response = {
                "stations": stations,
                "tracks": tracks,
                "trains": trains,
                "collisions": collisions,
                "timestamp": datetime.now().isoformat()
            }
            self.wfile.write(json.dumps(response).encode())
            return
        elif self.path == '/api/section-status':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            # Generate section data
            sections = {}
            for train in trains:
                section_key = f"{train['origin']}-{train['destination']}"
                if section_key not in sections:
                    sections[section_key] = {
                        "id": section_key,
                        "name": f"{train['origin']} to {train['destination']}",
                        "trains": [],
                        "status": "normal",
                        "priority": 3 if "Rajdhani" in train['train_type'] else 2 if "Shatabdi" in train['train_type'] else 1,
                        "throughput": 0,
                        "delays": 0
                    }
                sections[section_key]["trains"].append(train)
                if train.get('delay_minutes', 0) > 0:
                    sections[section_key]["delays"] += 1
            
            for section in sections.values():
                section["throughput"] = len(section["trains"])
                section["status"] = "delayed" if section["delays"] > len(section["trains"]) / 2 else "normal"
            
            response = {
                "sections": sections,
                "alerts": collisions,
                "timestamp": datetime.now().isoformat()
            }
            self.wfile.write(json.dumps(response).encode())
            return
        else:
            # Serve static files
            super().do_GET()

def generate_train_data():
    global trains, collisions
    
    train_types = ["Rajdhani Express", "Shatabdi Express", "Mail Express", "Superfast", "Passenger"]
    origins = [s["id"] for s in stations]
    
    trains = []
    for i in range(15):
        origin = random.choice(origins)
        destination = random.choice([s["id"] for s in stations if s["id"] != origin])
        
        train = {
            "train_number": f"12{i:03d}",
            "train_name": f"Express {i+1}",
            "train_type": random.choice(train_types),
            "origin": origin,
            "destination": destination,
            "current_station": origin,
            "next_station": destination,
            "status": random.choice(["running", "stopped", "in_transit"]),
            "speed": random.randint(60, 120),
            "delay_minutes": random.randint(0, 30) if random.random() < 0.3 else 0,
            "progress": random.uniform(0, 1),
            "lat": random.uniform(20, 30),
            "lon": random.uniform(75, 85),
            "collision_risk": random.random() < 0.1,
            "rerouting_needed": random.random() < 0.05
        }
        trains.append(train)
    
    collisions = []
    for train in trains:
        if train["collision_risk"]:
            collisions.append({
                "train_number": train["train_number"],
                "message": "Potential collision risk detected",
                "severity": "high",
                "timestamp": datetime.now().isoformat()
            })

def update_train_positions():
    """Update train positions and simulate movement"""
    global trains
    
    for train in trains:
        if train["status"] == "running":
            # Update progress
            train["progress"] += random.uniform(0.01, 0.03)
            if train["progress"] >= 1.0:
                train["progress"] = 0.0
                # Move to next station
                current_idx = next(i for i, s in enumerate(stations) if s["id"] == train["current_station"])
                next_idx = (current_idx + 1) % len(stations)
                train["current_station"] = stations[next_idx]["id"]
                train["next_station"] = stations[(next_idx + 1) % len(stations)]["id"]
            
            # Update coordinates based on progress
            origin_station = next(s for s in stations if s["id"] == train["origin"])
            dest_station = next(s for s in stations if s["id"] == train["destination"])
            
            progress = train["progress"]
            train["lat"] = origin_station["lat"] + (dest_station["lat"] - origin_station["lat"]) * progress
            train["lon"] = origin_station["lon"] + (dest_station["lon"] - origin_station["lon"]) * progress
            
            # Random status changes
            if random.random() < 0.01:
                train["collision_risk"] = random.random() < 0.1
            if random.random() < 0.005:
                train["rerouting_needed"] = random.random() < 0.05
            if random.random() < 0.02:
                train["delay_minutes"] = max(0, train["delay_minutes"] + random.randint(-5, 10))

def background_updater():
    """Background thread to update train data"""
    while True:
        try:
            update_train_positions()
            time.sleep(2)  # Update every 2 seconds
        except Exception as e:
            print(f"Background update error: {e}")
            time.sleep(5)

if __name__ == "__main__":
    # Generate initial data
    generate_train_data()
    
    # Start background updater
    updater_thread = threading.Thread(target=background_updater, daemon=True)
    updater_thread.start()
    
    # Start server
    with socketserver.TCPServer(("", PORT), RailwayHandler) as httpd:
        print(f"🚂 Railway Monitoring System Server")
        print(f"📍 Server running at http://localhost:{PORT}")
        print(f"🌐 Map API available at http://localhost:{PORT}/api/map-data")
        print(f"📊 Section API available at http://localhost:{PORT}/api/section-status")
        print(f"🔄 Auto-updating train positions every 2 seconds")
        print("Press Ctrl+C to stop the server")
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n🛑 Server stopped")
