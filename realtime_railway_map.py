#!/usr/bin/env python3
"""
Real-time Railway Map System
Interactive map showing live train movements with paths
"""

import asyncio
import json
import time
import random
import math
from datetime import datetime, timedelta
from typing import Dict, List, Any, Tuple
import threading

# Real-time train tracking data
trains_data = {}
stations_data = {}
tracks_data = {}
live_positions = {}

class Station:
    def __init__(self, id: str, name: str, lat: float, lon: float, 
                 station_type: str, platforms: int):
        self.id = id
        self.name = name
        self.lat = lat
        self.lon = lon
        self.station_type = station_type
        self.platforms = platforms

class TrackSegment:
    def __init__(self, id: str, from_station: str, to_station: str, 
                 distance: float, max_speed: float, track_type: str):
        self.id = id
        self.from_station = from_station
        self.to_station = to_station
        self.distance = distance
        self.max_speed = max_speed
        self.track_type = track_type

class Train:
    def __init__(self, id: str, train_number: str, train_type: str, 
                 origin: str, destination: str, current_station: str,
                 next_station: str, speed: float, status: str):
        self.id = id
        self.train_number = train_number
        self.train_type = train_type
        self.origin = origin
        self.destination = destination
        self.current_station = current_station
        self.next_station = next_station
        self.speed = speed
        self.status = status
        self.progress = 0.0  # Progress along current track (0-1)
        self.delay_minutes = 0
        self.last_update = datetime.now()
        self.collision_risk = False
        self.rerouting_needed = False
        self.ai_message = ""
        self.voice_enabled = False
        self.lat = 0.0
        self.lon = 0.0
        self.current_track_id = None

class RailwayMapSystem:
    def __init__(self):
        self.trains = trains_data
        self.stations = stations_data
        self.tracks = tracks_data
        self.positions = live_positions
        self.initialize_railway_network()
        self.start_live_tracking()
    
    def initialize_railway_network(self):
        """Initialize the comprehensive Indian railway network with ALL major stations"""
        
        # ALL Major railway stations across India with real coordinates
        stations = [
            # Northern Railway Zone
            Station("DLI", "New Delhi", 28.6448, 77.2194, "terminal", 16),
            Station("NDLS", "New Delhi Railway Station", 28.6448, 77.2194, "terminal", 16),
            Station("AGR", "Agra Cantt", 27.1767, 78.0081, "junction", 8),
            Station("JHS", "Jhansi", 25.4484, 78.5685, "junction", 6),
            Station("GWL", "Gwalior", 26.2183, 78.1828, "junction", 6),
            Station("BPL", "Bhopal", 23.2599, 77.4126, "junction", 8),
            Station("UJN", "Ujjain", 23.1765, 75.7885, "junction", 4),
            Station("RTM", "Ratlam", 23.3315, 75.0367, "junction", 6),
            Station("KTA", "Kota", 25.2138, 75.8648, "junction", 8),
            Station("AII", "Ajmer", 26.4499, 74.6399, "junction", 6),
            Station("JP", "Jaipur", 26.9196, 75.7878, "junction", 8),
            Station("BIKANER", "Bikaner", 28.0229, 73.3119, "junction", 4),
            Station("JU", "Jodhpur", 26.2389, 73.0243, "junction", 6),
            
            # Western Railway Zone
            Station("BCT", "Mumbai Central", 19.0176, 72.8562, "terminal", 12),
            Station("CSMT", "Chhatrapati Shivaji Maharaj Terminus", 18.9398, 72.8355, "terminal", 18),
            Station("THA", "Thane", 19.1972, 72.9702, "junction", 8),
            Station("KYN", "Kalyan", 19.2437, 73.1305, "junction", 6),
            Station("PUNE", "Pune", 18.5204, 73.8567, "junction", 6),
            Station("PUNE_JN", "Pune Junction", 18.5204, 73.8567, "junction", 6),
            Station("SUR", "Solapur", 17.6599, 75.9064, "junction", 6),
            Station("UBL", "Hubli", 15.3647, 75.1240, "junction", 8),
            Station("BZA", "Vijayawada", 16.5062, 80.6480, "junction", 10),
            Station("MAS", "Chennai Central", 13.0827, 80.2707, "terminal", 12),
            Station("NAS", "Nashik Road", 19.9975, 73.7898, "junction", 4),
            Station("MMR", "Manmad", 20.2437, 74.4378, "junction", 6),
            Station("JL", "Jalgaon", 21.0077, 75.5626, "junction", 4),
            Station("BSL", "Bhusaval", 21.0542, 75.7849, "junction", 8),
            Station("AK", "Akola", 20.7002, 77.0082, "junction", 6),
            Station("BD", "Badnera", 20.7506, 77.7749, "junction", 4),
            Station("NGP", "Nagpur", 21.1458, 79.0882, "junction", 8),
            
            # Eastern Railway Zone
            Station("HWH", "Howrah", 22.5848, 88.3426, "terminal", 23),
            Station("KOAA", "Kolkata Airport", 22.6533, 88.4467, "junction", 4),
            Station("SRC", "Santragachi", 22.6033, 88.2667, "junction", 6),
            Station("KGP", "Kharagpur", 22.3460, 87.3197, "junction", 10),
            Station("BBS", "Bhubaneswar", 20.2961, 85.8245, "junction", 8),
            Station("CTC", "Cuttack", 20.4625, 85.8828, "junction", 6),
            Station("PURI", "Puri", 19.8135, 85.8312, "terminal", 6),
            Station("VZM", "Vizianagaram", 18.1124, 83.4116, "junction", 6),
            Station("VSKP", "Visakhapatnam", 17.7231, 83.3219, "junction", 8),
            Station("RJY", "Rajahmundry", 17.0005, 81.8040, "junction", 6),
            Station("ELR", "Eluru", 16.7107, 81.0953, "junction", 4),
            
            # Southern Railway Zone
            Station("MAS", "Chennai Central", 13.0827, 80.2707, "terminal", 12),
            Station("MSB", "Chennai Beach", 13.0878, 80.2785, "terminal", 8),
            Station("TBM", "Tambaram", 12.9249, 80.1000, "junction", 8),
            Station("CGL", "Chengalpattu", 12.6918, 79.9753, "junction", 6),
            Station("VM", "Villupuram", 11.9401, 79.4861, "junction", 8),
            Station("VRI", "Vriddhachalam", 11.5196, 79.3250, "junction", 4),
            Station("TPJ", "Tiruchirapalli", 10.7905, 78.7047, "junction", 8),
            Station("DG", "Dindigul", 10.3673, 77.9803, "junction", 6),
            Station("MDU", "Madurai", 9.9252, 78.1198, "junction", 8),
            Station("TEN", "Tirunelveli", 8.7139, 77.7567, "junction", 6),
            Station("NCJ", "Nagercoil", 8.1840, 77.4343, "junction", 4),
            Station("TVC", "Thiruvananthapuram Central", 8.4875, 76.9525, "terminal", 8),
            Station("QLN", "Kollam", 8.8932, 76.6141, "junction", 6),
            Station("ALLP", "Alappuzha", 9.4981, 76.3388, "junction", 4),
            Station("ERS", "Ernakulam South", 9.9718, 76.2847, "junction", 8),
            Station("TCR", "Thrissur", 10.5276, 76.2144, "junction", 6),
            Station("SRR", "Shoranur", 10.7614, 76.2711, "junction", 8),
            Station("PGT", "Palakkad", 10.7867, 76.6548, "junction", 6),
            Station("CBE", "Coimbatore", 11.0168, 76.9558, "junction", 6),
            Station("TUP", "Tiruppur", 11.1085, 77.3411, "junction", 4),
            Station("ED", "Erode", 11.3410, 77.7172, "junction", 8),
            Station("SA", "Salem", 11.6643, 78.1460, "junction", 6),
            Station("BWT", "Bangarapet", 12.9904, 78.1719, "junction", 4),
            Station("SBC", "Bangalore City", 12.9716, 77.5946, "terminal", 10),
            Station("YPR", "Yesvantpur", 13.0284, 77.5043, "junction", 8),
            Station("TK", "Tumkur", 13.3379, 77.1027, "junction", 4),
            Station("ASK", "Arsikere", 13.3147, 76.2567, "junction", 6),
            Station("DVG", "Davangere", 14.4644, 75.9167, "junction", 4),
            Station("UBL", "Hubli", 15.3647, 75.1240, "junction", 8),
            Station("BGM", "Belagavi", 15.8497, 74.4977, "junction", 6),
            
            # South Central Railway Zone
            Station("SC", "Secunderabad", 17.4399, 78.5010, "terminal", 10),
            Station("HYB", "Hyderabad Deccan", 17.3850, 78.4867, "junction", 8),
            Station("KCG", "Kacheguda", 17.3753, 78.4744, "junction", 6),
            Station("BMT", "Begumpet", 17.4399, 78.4399, "junction", 4),
            Station("WL", "Warangal", 17.9669, 79.5941, "junction", 8),
            Station("BZA", "Vijayawada", 16.5062, 80.6480, "junction", 10),
            Station("EE", "Eluru", 16.7107, 81.0953, "junction", 4),
            Station("RU", "Renigunta", 13.6288, 79.5130, "junction", 6),
            Station("TPTY", "Tirupati", 13.6288, 79.4192, "terminal", 6),
            Station("GDR", "Gudur", 14.1543, 79.8507, "junction", 4),
            Station("NLR", "Nellore", 14.4426, 79.9865, "junction", 6),
            Station("OGL", "Ongole", 15.5057, 80.0499, "junction", 4),
            Station("CLX", "Chirala", 15.8267, 80.3528, "junction", 2),
            Station("TEL", "Tenali", 16.2428, 80.6514, "junction", 4),
            Station("GNT", "Guntur", 16.3067, 80.4365, "junction", 8),
            
            # North Eastern Railway Zone
            Station("LKO", "Lucknow", 26.8393, 80.9231, "junction", 8),
            Station("GKP", "Gorakhpur", 26.7606, 83.3732, "junction", 8),
            Station("CPR", "Chhapra", 25.7890, 84.0174, "junction", 6),
            Station("SV", "Siwan", 26.2183, 84.3616, "junction", 4),
            Station("GD", "Gonda", 27.1404, 81.9784, "junction", 6),
            Station("FD", "Faizabad", 26.7751, 82.1382, "junction", 4),
            Station("AY", "Ayodhya", 26.7751, 82.1382, "junction", 4),
            Station("BSB", "Varanasi", 25.3176, 82.9739, "junction", 8),
            Station("MGS", "Mughal Sarai", 25.2916, 83.1216, "junction", 10),
            Station("ARJ", "Aunrihar", 25.4378, 83.6017, "junction", 4),
            Station("GCT", "Ghazipur City", 25.5881, 83.5775, "junction", 4),
            Station("MAU", "Mau", 25.9417, 83.5611, "junction", 4),
            Station("IAA", "Indara", 26.0394, 83.6281, "junction", 2),
            
            # East Coast Railway Zone
            Station("BBS", "Bhubaneswar", 20.2961, 85.8245, "junction", 8),
            Station("CTC", "Cuttack", 20.4625, 85.8828, "junction", 6),
            Station("BHC", "Bhadrakh", 21.0543, 86.5025, "junction", 4),
            Station("BLS", "Balasore", 21.4942, 86.9320, "junction", 6),
            Station("JER", "Jaleswar", 21.4017, 87.2211, "junction", 2),
            Station("HIJ", "Hijilli", 22.2833, 87.3000, "junction", 4),
            Station("MDN", "Midnapore", 22.4249, 87.3190, "junction", 6),
            Station("VSKP", "Visakhapatnam", 17.7231, 83.3219, "junction", 8),
            Station("DVD", "Duvvada", 17.6844, 83.2042, "junction", 4),
            Station("AKP", "Anakapalle", 17.6911, 83.0036, "junction", 4),
            Station("TUNI", "Tuni", 17.3500, 82.5500, "junction", 4),
            Station("RJY", "Rajahmundry", 17.0005, 81.8040, "junction", 6),
            
            # West Central Railway Zone
            Station("JBP", "Jabalpur", 23.1815, 79.9864, "junction", 8),
            Station("KTE", "Katni", 23.8367, 80.3942, "junction", 8),
            Station("STA", "Satna", 24.5667, 80.8167, "junction", 6),
            Station("MKP", "Manikpur", 25.2957, 81.0350, "junction", 4),
            Station("COI", "Chheoki", 25.1342, 81.8439, "junction", 6),
            Station("ALD", "Allahabad", 25.4358, 81.8463, "junction", 10),
            Station("SRJ", "Shankargarh", 25.1833, 81.6167, "junction", 2),
            Station("MZP", "Mirzapur", 25.1467, 82.5698, "junction", 4),
            Station("BDL", "Vindhyachal", 25.1667, 82.6500, "junction", 2),
            Station("MOF", "Mondh", 25.2000, 82.7000, "junction", 2),
            
            # North Central Railway Zone
            Station("ALJN", "Aligarh Junction", 27.8906, 78.0880, "junction", 8),
            Station("TDL", "Tundla", 27.2167, 78.2833, "junction", 6),
            Station("ETW", "Etawah", 26.7605, 79.0147, "junction", 6),
            Station("CNB", "Kanpur Central", 26.4499, 80.3319, "junction", 10),
            Station("ON", "Unnao", 26.5464, 80.4984, "junction", 4),
            Station("LJN", "Lucknow Junction", 26.8393, 80.9231, "junction", 8),
            Station("BE", "Bareilly", 28.3670, 79.4304, "junction", 8),
            Station("MB", "Moradabad", 28.8386, 78.7733, "junction", 8),
            Station("GZB", "Ghaziabad", 28.6692, 77.4538, "junction", 8),
            Station("MTC", "Meerut City", 28.9845, 77.7064, "junction", 6),
        ]
        
        for station in stations:
            self.stations[station.id] = station
        
        # Comprehensive track segments connecting ALL major stations
        tracks = [
            # Golden Quadrilateral - Main trunk routes
            # Delhi-Mumbai via Jaipur-Ajmer route
            TrackSegment("DLI-GZB", "DLI", "GZB", 25, 160, "main"),
            TrackSegment("GZB-MB", "GZB", "MB", 140, 130, "main"),
            TrackSegment("MB-BE", "MB", "BE", 90, 120, "main"),
            TrackSegment("BE-LKO", "BE", "LKO", 250, 110, "main"),
            TrackSegment("LKO-CNB", "LKO", "CNB", 75, 130, "main"),
            TrackSegment("CNB-JHS", "CNB", "JHS", 295, 130, "main"),
            TrackSegment("JHS-BPL", "JHS", "BPL", 180, 130, "main"),
            TrackSegment("BPL-NGP", "BPL", "NGP", 350, 120, "main"),
            TrackSegment("NGP-BSL", "NGP", "BSL", 140, 110, "main"),
            TrackSegment("BSL-MMR", "BSL", "MMR", 65, 100, "main"),
            TrackSegment("MMR-KYN", "MMR", "KYN", 180, 100, "main"),
            TrackSegment("KYN-BCT", "KYN", "BCT", 54, 80, "suburban"),
            
            # Delhi-Mumbai via Kota-Ratlam route  
            TrackSegment("DLI-JP", "DLI", "JP", 308, 130, "main"),
            TrackSegment("JP-AII", "JP", "AII", 135, 110, "main"),
            TrackSegment("AII-KTA", "AII", "KTA", 195, 130, "main"),
            TrackSegment("KTA-RTM", "KTA", "RTM", 108, 120, "main"),
            TrackSegment("RTM-UJN", "RTM", "UJN", 90, 100, "main"),
            TrackSegment("UJN-BPL", "UJN", "BPL", 185, 110, "main"),
            
            # Delhi-Chennai main line
            TrackSegment("DLI-AGR", "DLI", "AGR", 200, 160, "main"),
            TrackSegment("AGR-GWL", "AGR", "GWL", 120, 130, "main"),
            TrackSegment("GWL-JHS", "GWL", "JHS", 100, 130, "main"),
            TrackSegment("JHS-BPL", "JHS", "BPL", 180, 130, "main"),
            TrackSegment("BPL-JBP", "BPL", "JBP", 265, 110, "main"),
            TrackSegment("JBP-KTE", "JBP", "KTE", 25, 110, "main"),
            TrackSegment("KTE-STA", "KTE", "STA", 90, 110, "main"),
            TrackSegment("STA-ALD", "STA", "ALD", 130, 110, "main"),
            TrackSegment("ALD-MGS", "ALD", "MGS", 135, 110, "main"),
            TrackSegment("MGS-SC", "MGS", "SC", 800, 130, "main"),
            TrackSegment("SC-BZA", "SC", "BZA", 275, 130, "main"),
            TrackSegment("BZA-MAS", "BZA", "MAS", 350, 130, "main"),
            
            # Delhi-Kolkata main line
            TrackSegment("DLI-CNB", "DLI", "CNB", 440, 130, "main"),
            TrackSegment("CNB-ALD", "CNB", "ALD", 200, 130, "main"),
            TrackSegment("ALD-BSB", "ALD", "BSB", 135, 110, "main"),
            TrackSegment("BSB-MGS", "BSB", "MGS", 25, 110, "main"),
            TrackSegment("MGS-GKP", "MGS", "GKP", 130, 110, "main"),
            TrackSegment("GKP-CPR", "GKP", "CPR", 90, 100, "main"),
            TrackSegment("CPR-HWH", "CPR", "HWH", 140, 110, "main"),
            
            # Mumbai-Chennai via Pune
            TrackSegment("BCT-PUNE", "BCT", "PUNE", 150, 110, "main"),
            TrackSegment("PUNE-SUR", "PUNE", "SUR", 250, 110, "main"),
            TrackSegment("SUR-UBL", "SUR", "UBL", 230, 100, "main"),
            TrackSegment("UBL-SBC", "UBL", "SBC", 430, 110, "main"),
            TrackSegment("SBC-SA", "SBC", "SA", 190, 110, "main"),
            TrackSegment("SA-ED", "SA", "ED", 45, 100, "main"),
            TrackSegment("ED-CBE", "ED", "CBE", 100, 100, "main"),
            TrackSegment("CBE-TPJ", "CBE", "TPJ", 50, 100, "main"),
            TrackSegment("TPJ-MAS", "TPJ", "MAS", 470, 130, "main"),
            
            # Mumbai-Kolkata via Nagpur
            TrackSegment("BCT-NGP", "BCT", "NGP", 780, 120, "main"),
            TrackSegment("NGP-BZA", "NGP", "BZA", 590, 130, "main"),
            TrackSegment("BZA-VSKP", "BZA", "VSKP", 350, 130, "main"),
            TrackSegment("VSKP-BBS", "VSKP", "BBS", 440, 130, "main"),
            TrackSegment("BBS-HWH", "BBS", "HWH", 460, 130, "main"),
            
            # Southern Peninsula routes
            TrackSegment("MAS-SBC", "MAS", "SBC", 362, 130, "main"),
            TrackSegment("MAS-TVC", "MAS", "TVC", 695, 110, "main"),
            TrackSegment("TVC-ERS", "TVC", "ERS", 165, 100, "main"),
            TrackSegment("ERS-CBE", "ERS", "CBE", 195, 100, "main"),
            TrackSegment("SBC-HYB", "SBC", "HYB", 570, 130, "main"),
            TrackSegment("HYB-SC", "HYB", "SC", 8, 80, "suburban"),
            
            # Eastern routes
            TrackSegment("HWH-BBS", "HWH", "BBS", 460, 130, "main"),
            TrackSegment("BBS-PURI", "BBS", "PURI", 65, 100, "main"),
            TrackSegment("HWH-KGP", "HWH", "KGP", 120, 130, "main"),
            TrackSegment("KGP-VSKP", "KGP", "VSKP", 590, 130, "main"),
            
            # Western routes  
            TrackSegment("BCT-CSMT", "BCT", "CSMT", 15, 60, "suburban"),
            TrackSegment("CSMT-THA", "CSMT", "THA", 40, 80, "suburban"),
            TrackSegment("THA-KYN", "THA", "KYN", 15, 80, "suburban"),
            TrackSegment("BCT-AII", "BCT", "AII", 490, 110, "main"),
            TrackSegment("AII-JU", "AII", "JU", 185, 100, "main"),
            
            # Northern routes
            TrackSegment("DLI-BIKANER", "DLI", "BIKANER", 445, 110, "main"),
            TrackSegment("JP-BIKANER", "JP", "BIKANER", 250, 100, "main"),
            TrackSegment("DLI-LKO", "DLI", "LKO", 500, 130, "main"),
            TrackSegment("LKO-GKP", "LKO", "GKP", 270, 110, "main"),
            
            # North Eastern routes
            TrackSegment("GKP-GD", "GKP", "GD", 150, 100, "main"),
            TrackSegment("GD-LKO", "GD", "LKO", 125, 100, "main"),
            TrackSegment("LKO-FD", "LKO", "FD", 135, 100, "main"),
            TrackSegment("FD-BSB", "FD", "BSB", 165, 100, "main"),
            
            # South Central routes
            TrackSegment("SC-WL", "SC", "WL", 150, 130, "main"),
            TrackSegment("WL-BZA", "WL", "BZA", 140, 130, "main"),
            TrackSegment("BZA-RU", "BZA", "RU", 430, 130, "main"),
            TrackSegment("RU-TPTY", "RU", "TPTY", 15, 80, "branch"),
            TrackSegment("RU-MAS", "RU", "MAS", 150, 130, "main"),
            
            # Additional important connections
            TrackSegment("PUNE-SBC", "PUNE", "SBC", 840, 110, "main"),
            TrackSegment("NGP-HYB", "NGP", "HYB", 490, 120, "main"),
            TrackSegment("BPL-UJN", "BPL", "UJN", 185, 110, "main"),
            TrackSegment("CNB-LJN", "CNB", "LJN", 75, 130, "main"),
            TrackSegment("ALJN-CNB", "ALJN", "CNB", 190, 120, "main"),
            TrackSegment("AGR-ALJN", "AGR", "ALJN", 125, 120, "main"),
            TrackSegment("JBP-NGP", "JBP", "NGP", 265, 110, "main"),
            TrackSegment("KTE-NGP", "KTE", "NGP", 240, 110, "main"),
        ]
        
        for track in tracks:
            self.tracks[track.id] = track
        
        # Initialize comprehensive trains with realistic routes across India
        trains = [
            # Rajdhani Express trains (Premium trains connecting Delhi)
            Train("T001", "12951", "Rajdhani Express", "BCT", "DLI", "BCT", "KYN", 130, "running"),
            Train("T002", "12301", "Rajdhani Express", "HWH", "DLI", "HWH", "KGP", 140, "running"),
            Train("T003", "12431", "Rajdhani Express", "TVC", "DLI", "TVC", "ERS", 130, "running"),
            Train("T004", "12009", "Rajdhani Express", "SBC", "DLI", "SBC", "SA", 130, "running"),
            Train("T005", "12423", "Rajdhani Express", "DLI", "ALD", "DLI", "GZB", 140, "running"),
            
            # Shatabdi Express trains (Day trains)
            Train("T006", "12017", "Shatabdi Express", "DLI", "KTA", "DLI", "JP", 150, "running"),
            Train("T007", "12002", "Shatabdi Express", "BCT", "AII", "BCT", "PUNE", 140, "running"),
            Train("T008", "12008", "Shatabdi Express", "MAS", "SBC", "MAS", "SA", 130, "running"),
            Train("T009", "12004", "Shatabdi Express", "DLI", "LKO", "DLI", "CNB", 150, "running"),
            Train("T010", "12010", "Shatabdi Express", "HWH", "BBS", "HWH", "KGP", 130, "running"),
            
            # Duronto Express trains (Non-stop long distance)
            Train("T011", "12259", "Duronto Express", "SC", "DLI", "SC", "NGP", 140, "running"),
            Train("T012", "12274", "Duronto Express", "HWH", "DLI", "HWH", "MGS", 140, "running"),
            Train("T013", "12218", "Duronto Express", "CSMT", "SC", "CSMT", "PUNE", 120, "running"),
            Train("T014", "12290", "Duronto Express", "MAS", "DLI", "MAS", "BZA", 130, "running"),
            Train("T015", "12246", "Duronto Express", "YPR", "DLI", "YPR", "UBL", 130, "running"),
            
            # Superfast Express trains
            Train("T016", "12049", "Gatimaan Express", "DLI", "JHS", "DLI", "AGR", 160, "running"),
            Train("T017", "22691", "Rajdhani Express", "DLI", "KOL", "DLI", "CNB", 140, "running"),
            Train("T018", "12434", "Chennai Rajdhani", "MAS", "DLI", "MAS", "RU", 130, "running"),
            Train("T019", "12952", "Mumbai Rajdhani", "DLI", "BCT", "DLI", "KTA", 130, "running"),
            Train("T020", "22406", "Vande Bharat Express", "DLI", "KTA", "DLI", "JP", 160, "running"),
            
            # Long Distance Express trains  
            Train("T021", "12615", "Grand Trunk Express", "MAS", "DLI", "MAS", "GNT", 110, "running"),
            Train("T022", "12842", "Coromandel Express", "HWH", "MAS", "HWH", "BBS", 120, "running"),
            Train("T023", "12840", "Howrah Mail", "MAS", "HWH", "MAS", "VSKP", 110, "running"),
            Train("T024", "12321", "Howrah Mail", "HWH", "BCT", "HWH", "NGP", 110, "running"),
            Train("T025", "16031", "Andaman Express", "MAS", "VM", "MAS", "VM", 100, "running"),
            
            # Regional Express trains
            Train("T026", "11013", "Coimbatore Express", "MAS", "CBE", "MAS", "SA", 100, "running"),
            Train("T027", "12163", "Mumbai Express", "BCT", "PUNE", "BCT", "PUNE", 100, "running"),
            Train("T028", "12779", "Goa Express", "HWH", "VSKP", "HWH", "VSKP", 110, "running"),
            Train("T029", "12432", "Trivandrum Rajdhani", "DLI", "TVC", "DLI", "BPL", 130, "running"),
            Train("T030", "12269", "Chennai Duronto", "HWH", "MAS", "HWH", "BZA", 130, "running"),
            
            # Mail/Express trains
            Train("T031", "12651", "Sampark Kranti Express", "TVC", "DLI", "TVC", "CBE", 110, "running"),
            Train("T032", "12617", "Mangala Lakshadweep Express", "ERS", "DLI", "ERS", "SRR", 110, "running"),
            Train("T033", "12625", "Kerala Express", "TVC", "DLI", "TVC", "PGT", 110, "running"),
            Train("T034", "12484", "Punjab Express", "DLI", "CNB", "DLI", "GZB", 100, "running"),
            Train("T035", "12472", "Swaraj Express", "PUNE", "SUR", "PUNE", "SUR", 100, "running"),
            
            # Freight trains (cargo)
            Train("T036", "FG001", "Container Freight", "BCT", "PUNE", "BCT", "PUNE", 80, "running"),
            Train("T037", "FG002", "Coal Freight", "BBS", "HWH", "BBS", "HWH", 70, "running"),
            Train("T038", "FG003", "Iron Ore Freight", "BZA", "VSKP", "BZA", "VSKP", 75, "running"),
            Train("T039", "FG004", "Petroleum Freight", "JU", "AII", "JU", "AII", 70, "running"),
            Train("T040", "FG005", "Food Grains Freight", "DLI", "MAS", "DLI", "CNB", 80, "running"),
            
            # Suburban/Local trains
            Train("T041", "SL001", "Local Train", "CSMT", "KYN", "CSMT", "THA", 60, "running"),
            Train("T042", "SL002", "Local Train", "MAS", "TBM", "MAS", "CGL", 50, "running"),
            Train("T043", "SL003", "EMU Local", "HWH", "SRC", "HWH", "SRC", 45, "running"),
            Train("T044", "SL004", "MEMU Local", "DLI", "GZB", "DLI", "GZB", 55, "running"),
            Train("T045", "SL005", "Passenger Train", "BZA", "SC", "BZA", "WL", 40, "running"),
            
            # Special trains
            Train("T046", "SP001", "Palace on Wheels", "DLI", "JP", "DLI", "JP", 90, "running"),
            Train("T047", "SP002", "Deccan Odyssey", "BCT", "PUNE", "BCT", "PUNE", 80, "running"),
            Train("T048", "SP003", "Golden Chariot", "SBC", "YPR", "SBC", "YPR", 70, "running"),
            Train("T049", "SP004", "Maharaja Express", "DLI", "BCT", "DLI", "JP", 100, "running"),
            Train("T050", "SP005", "Buddhist Circuit Train", "DLI", "BSB", "DLI", "LKO", 90, "running"),
        ]
        
        for train in trains:
            self.trains[train.id] = train
            # Initialize random positions along their routes
            self.positions[train.id] = {
                "lat": self.stations[train.current_station].lat,
                "lon": self.stations[train.current_station].lon,
                "progress": random.uniform(0, 1),
                "speed": train.speed,
                "status": train.status
            }
    
    def calculate_position(self, train_id: str) -> Tuple[float, float]:
        """Calculate current position of train along its route"""
        train = self.trains[train_id]
        current_station = self.stations[train.current_station]
        next_station = self.stations[train.next_station]
        
        # Find the track segment
        track_id = f"{train.current_station}-{train.next_station}"
        if track_id not in self.tracks:
            track_id = f"{train.next_station}-{train.current_station}"
        
        if track_id not in self.tracks:
            return current_station.lat, current_station.lon
        
        # Interpolate position based on progress
        progress = self.positions[train_id]["progress"]
        
        lat = current_station.lat + (next_station.lat - current_station.lat) * progress
        lon = current_station.lon + (next_station.lon - current_station.lon) * progress
        
        return lat, lon
    
    def update_train_positions(self):
        """Update all train positions in real-time"""
        for train_id, train in self.trains.items():
            if train.status == "running":
                # Update progress along route
                track_id = f"{train.current_station}-{train.next_station}"
                if track_id not in self.tracks:
                    track_id = f"{train.next_station}-{train.current_station}"
                
                if track_id in self.tracks:
                    track = self.tracks[track_id]
                    # Calculate speed in progress units per second
                    speed_progress_per_sec = train.speed / (track.distance * 60)  # km/h to progress/sec
                    
                    # Update progress
                    self.positions[train_id]["progress"] += speed_progress_per_sec * 0.1  # Update every 0.1 seconds
                    
                    # If train reaches next station, move to next segment
                    if self.positions[train_id]["progress"] >= 1.0:
                        self.positions[train_id]["progress"] = 0.0
                        # Move to next station (simplified logic)
                        if train.next_station == train.destination:
                            train.status = "arrived"
                        else:
                            train.current_station = train.next_station
                            # Find next station (simplified)
                            for track_seg in self.tracks.values():
                                if track_seg.from_station == train.current_station:
                                    train.next_station = track_seg.to_station
                                    break
                
                # Update position coordinates
                lat, lon = self.calculate_position(train_id)
                self.positions[train_id]["lat"] = lat
                self.positions[train_id]["lon"] = lon
                self.positions[train_id]["speed"] = train.speed
                self.positions[train_id]["status"] = train.status
    
    def start_live_tracking(self):
        """Start the real-time tracking thread"""
        def tracking_loop():
            while True:
                self.update_train_positions()
                time.sleep(0.1)  # Update every 100ms for smooth movement
        
        tracking_thread = threading.Thread(target=tracking_loop, daemon=True)
        tracking_thread.start()
    
    def get_map_data(self) -> Dict[str, Any]:
        """Get all data needed for the map"""
        stations_list = []
        for station in self.stations.values():
            stations_list.append({
                "id": station.id,
                "name": station.name,
                "lat": station.lat,
                "lon": station.lon,
                "type": station.station_type,
                "platforms": station.platforms
            })
        
        tracks_list = []
        for track in self.tracks.values():
            from_station = self.stations[track.from_station]
            to_station = self.stations[track.to_station]
            tracks_list.append({
                "id": track.id,
                "from": {"lat": from_station.lat, "lon": from_station.lon},
                "to": {"lat": to_station.lat, "lon": to_station.lon},
                "distance": track.distance,
                "max_speed": track.max_speed,
                "type": track.track_type
            })
        
        trains_list = []
        for train_id, train in self.trains.items():
            position = self.positions[train_id]
            trains_list.append({
                "id": train_id,
                "train_number": train.train_number,
                "train_type": train.train_type,
                "origin": train.origin,
                "destination": train.destination,
                "current_station": train.current_station,
                "next_station": train.next_station,
                "lat": position["lat"],
                "lon": position["lon"],
                "speed": position["speed"],
                "status": position["status"],
                "progress": position["progress"],
                "collision_risk": position.get("collision_risk", False),
                "rerouting_needed": position.get("rerouting_needed", False),
                "ai_message": position.get("ai_message", ""),
                "section_id": self._get_section_id(train.current_station),
                "priority": self._get_train_priority(train.train_type),
                "delay_minutes": position.get("delay_minutes", 0)
            })
        
        return {
            "stations": stations_list,
            "tracks": tracks_list,
            "trains": trains_list,
            "collisions": self._get_collision_alerts(),
            "rerouting": self._get_rerouting_alerts(),
            "timestamp": datetime.now().isoformat()
        }
    
    def update_train_positions(self):
        """Update train positions with real movement"""
        for train_id, train in self.trains.items():
            self._move_train(train_id, train)
            self._check_collision_risk(train_id, train)
            self._check_rerouting_needed(train_id, train)
    
    def _move_train(self, train_id, train):
        """Move train along its current track"""
        if train_id in self.positions:
            position = self.positions[train_id]
            
            # Update progress based on speed
            speed_factor = position["speed"] / 100.0  # Normalize speed
            position["progress"] += speed_factor * 0.02  # Small increment
            
            if position["progress"] >= 1.0:
                # Train reached destination station
                position["progress"] = 0.0
                # Move to next station in route
                self._advance_to_next_station(train_id, train)
            
            # Update position based on current track
            self._update_train_coordinates(train_id, train, position)
    
    def _advance_to_next_station(self, train_id, train):
        """Move train to next station in route"""
        # Move train to next station
        train.current_station = train.next_station
        
        # Find next station in route
        available_tracks = [t for t in self.tracks.values() 
                          if t.from_station == train.current_station]
        if available_tracks:
            # Choose a track that leads towards destination
            destination = train.destination
            best_track = None
            
            # Try to find a track that gets closer to destination
            for track in available_tracks:
                if track.to_station == destination:
                    best_track = track
                    break
            
            # If no direct track to destination, choose first available track
            if not best_track:
                best_track = available_tracks[0]
            
            train.next_station = best_track.to_station
        else:
            # If no tracks available, stay at current station
            train.next_station = train.current_station
    
    def _update_train_coordinates(self, train_id, train, position):
        """Update train coordinates based on current track"""
        # Find current track
        current_track = None
        for track in self.tracks.values():
            if track.from_station == train.current_station and track.to_station == train.next_station:
                current_track = track
                break
        
        if current_track:
            from_station = self.stations[current_track.from_station]
            to_station = self.stations[current_track.to_station]
            
            # Calculate position based on progress
            progress = position["progress"]
            position["lat"] = from_station.lat + (to_station.lat - from_station.lat) * progress
            position["lon"] = from_station.lon + (to_station.lon - from_station.lon) * progress
    
    def _check_collision_risk(self, train_id, train):
        """Check if train is at risk of collision"""
        position = self.positions[train_id]
        
        # Check for trains on same track segment
        for other_id, other_train in self.trains.items():
            if other_id != train_id:
                other_position = self.positions[other_id]
                
                # Check if trains are on same track and too close
                if (train.current_station == other_train.current_station and 
                    train.next_station == other_train.next_station):
                    
                    distance = abs(position["progress"] - other_position["progress"])
                    if distance < 0.15:  # Within 15% of track
                        position["collision_risk"] = True
                        position["ai_message"] = f"⚠️ COLLISION RISK: Too close to {other_train.train_number}"
                        return
        
        position["collision_risk"] = False
        position["ai_message"] = ""
    
    def _check_rerouting_needed(self, train_id, train):
        """Check if train needs rerouting"""
        position = self.positions[train_id]
        
        # Check for delays
        if position.get("delay_minutes", 0) > 15:
            position["rerouting_needed"] = True
            position["ai_message"] = f"🔄 REROUTING NEEDED: {position['delay_minutes']} min delay"
            return
        
        # Check for track maintenance (random chance)
        if random.random() < 0.03:  # 3% chance
            position["rerouting_needed"] = True
            position["ai_message"] = "🚧 REROUTING NEEDED: Track maintenance ahead"
            return
        
        position["rerouting_needed"] = False
        if not position["collision_risk"]:
            position["ai_message"] = ""
    
    def _get_collision_alerts(self):
        """Get all collision alerts"""
        alerts = []
        for train_id, train in self.trains.items():
            position = self.positions[train_id]
            if position.get("collision_risk", False):
                alerts.append({
                    "train_id": train_id,
                    "train_number": train.train_number,
                    "message": position["ai_message"],
                    "severity": "high",
                    "timestamp": datetime.now().isoformat()
                })
        return alerts
    
    def _get_rerouting_alerts(self):
        """Get all rerouting alerts"""
        alerts = []
        for train_id, train in self.trains.items():
            position = self.positions[train_id]
            if position.get("rerouting_needed", False):
                alerts.append({
                    "train_id": train_id,
                    "train_number": train.train_number,
                    "message": position["ai_message"],
                    "severity": "medium",
                    "timestamp": datetime.now().isoformat()
                })
        return alerts
    
    def _get_section_id(self, station_id):
        """Get section ID for a station (simplified section mapping)"""
        # Map stations to railway sections
        section_mapping = {
            'NDLS': 'NORTH_DELHI', 'DLI': 'NORTH_DELHI', 'NZM': 'SOUTH_DELHI',
            'CSMT': 'MUMBAI_CENTRAL', 'BDTS': 'MUMBAI_WESTERN', 'LTT': 'MUMBAI_CENTRAL',
            'HWH': 'KOLKATA_HOWRAH', 'KOAA': 'KOLKATA_SEALDAH', 'SDAH': 'KOLKATA_SEALDAH',
            'MAS': 'CHENNAI_CENTRAL', 'MSB': 'CHENNAI_CENTRAL', 'TBM': 'CHENNAI_CENTRAL',
            'SBC': 'BANGALORE_CITY', 'YPR': 'BANGALORE_YESVANTPUR', 'KJM': 'BANGALORE_CITY',
            'GIMB': 'GUJARAT_NORTH', 'ADI': 'AHMEDABAD', 'BRC': 'VADODARA',
            'JP': 'JAIPUR', 'JU': 'JODHPUR', 'BIKANER': 'BIKANER',
            'LKO': 'LUCKNOW', 'CNB': 'KANPUR', 'GZB': 'GHAZIABAD',
            'PNBE': 'PATNA', 'GAY': 'GAYA', 'MFP': 'MUZAFFARPUR',
            'ASN': 'ASANSOL', 'DGR': 'DURGAPUR', 'BWN': 'BURDWAN',
            'PUNE': 'PUNE', 'KOP': 'KOLHAPUR', 'SUR': 'SURAT',
            'HYB': 'HYDERABAD', 'SC': 'SECUNDERABAD', 'KZJ': 'KAZIPET',
            'BZA': 'VIJAYAWADA', 'RJY': 'RAJAHMUNDRY', 'VSKP': 'VISAKHAPATNAM',
            'TVC': 'THIRUVANANTHAPURAM', 'QLN': 'KOLLAM', 'ALLP': 'ALLEPPEY',
            'CAN': 'KANNUR', 'CLT': 'KOZHIKODE', 'TCR': 'THRISSUR'
        }
        return section_mapping.get(station_id, 'UNKNOWN_SECTION')
    
    def _get_train_priority(self, train_type):
        """Get priority level for train type"""
        priority_mapping = {
            'Rajdhani Express': 1,  # Highest priority
            'Vande Bharat Express': 1,
            'Shatabdi Express': 2,
            'Duronto Express': 2,
            'Express': 3,
            'Mail': 4,
            'Freight': 5,
            'Local': 6  # Lowest priority
        }
        return priority_mapping.get(train_type, 3)
    
    def get_section_status(self):
        """Get status of all railway sections"""
        sections = {}
        for train_id, train in self.trains.items():
            section_id = self._get_section_id(train.current_station)
            if section_id not in sections:
                sections[section_id] = {
                    "section_id": section_id,
                    "trains": [],
                    "total_trains": 0,
                    "delayed_trains": 0,
                    "collision_risks": 0,
                    "rerouting_needed": 0,
                    "avg_delay": 0
                }
            
            position = self.positions[train_id]
            sections[section_id]["trains"].append({
                "train_number": train.train_number,
                "train_type": train.train_type,
                "current_station": train.current_station,
                "status": position["status"],
                "delay_minutes": position.get("delay_minutes", 0),
                "collision_risk": position.get("collision_risk", False),
                "rerouting_needed": position.get("rerouting_needed", False)
            })
            sections[section_id]["total_trains"] += 1
            
            if position.get("delay_minutes", 0) > 0:
                sections[section_id]["delayed_trains"] += 1
            
            if position.get("collision_risk", False):
                sections[section_id]["collision_risks"] += 1
            
            if position.get("rerouting_needed", False):
                sections[section_id]["rerouting_needed"] += 1
        
        # Calculate average delays
        for section_id, section in sections.items():
            if section["total_trains"] > 0:
                total_delay = sum(train["delay_minutes"] for train in section["trains"])
                section["avg_delay"] = round(total_delay / section["total_trains"], 1)
        
        return sections

# Global system instance
railway_map = RailwayMapSystem()

# Background thread for real-time updates
def update_positions_thread():
    """Background thread to update train positions"""
    while True:
        try:
            railway_map.update_train_positions()
            time.sleep(2)  # Update every 2 seconds
        except Exception as e:
            print(f"Error updating positions: {e}")
            time.sleep(5)

# Start background thread
position_thread = threading.Thread(target=update_positions_thread, daemon=True)
position_thread.start()

def create_realtime_map_html():
    """Create the real-time interactive railway map"""
    html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Real-time Railway Map - Live Train Tracking</title>
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
    <style>
        body {{
            margin: 0;
            padding: 0;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: #0a0a0a;
            color: white;
            overflow: hidden;
        }}
        
        .header {{
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            background: linear-gradient(90deg, #1a1a2e, #16213e, #0f3460);
            padding: 15px 20px;
            z-index: 1000;
            box-shadow: 0 2px 10px rgba(0,0,0,0.5);
        }}
        
        .header h1 {{
            margin: 0;
            font-size: 1.8rem;
            color: #ffd700;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.7);
        }}
        
        .header p {{
            margin: 5px 0 0 0;
            opacity: 0.9;
            font-size: 0.9rem;
        }}
        
        .map-container {{
            position: fixed;
            top: 80px;
            left: 0;
            right: 0;
            bottom: 0;
        }}
        
        #map {{
            width: 100%;
            height: 100%;
        }}
        
        .control-panel {{
            position: fixed;
            top: 80px;
            right: 20px;
            width: 300px;
            background: rgba(0,0,0,0.8);
            border-radius: 10px;
            padding: 15px;
            z-index: 1000;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255,255,255,0.1);
        }}
        
        .control-panel h3 {{
            margin: 0 0 15px 0;
            color: #ffd700;
            font-size: 1.1rem;
        }}
        
        .train-item {{
            background: rgba(255,255,255,0.1);
            border-radius: 8px;
            padding: 10px;
            margin: 8px 0;
            border-left: 4px solid #ffd700;
            cursor: pointer;
            transition: all 0.3s ease;
        }}
        
        .train-item:hover {{
            background: rgba(255,255,255,0.2);
            transform: translateX(5px);
        }}
        
        .train-item.selected {{
            background: rgba(255,215,0,0.2);
            border-left-color: #ff6b6b;
        }}
        
        .train-number {{
            font-weight: bold;
            color: #ffd700;
            font-size: 0.9rem;
        }}
        
        .train-route {{
            font-size: 0.8rem;
            opacity: 0.8;
            margin: 3px 0;
        }}
        
        .train-status {{
            font-size: 0.75rem;
            padding: 2px 8px;
            border-radius: 12px;
            display: inline-block;
            margin-top: 5px;
        }}
        
        .status-running {{ background: #4CAF50; }}
        .status-delayed {{ background: #FF9800; }}
        .status-arrived {{ background: #2196F3; }}
        .status-scheduled {{ background: #9C27B0; }}
        
        .stats {{
            position: fixed;
            bottom: 20px;
            left: 20px;
            background: rgba(0,0,0,0.8);
            border-radius: 10px;
            padding: 15px;
            z-index: 1000;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255,255,255,0.1);
        }}
        
        .stat-item {{
            display: flex;
            justify-content: space-between;
            margin: 5px 0;
            font-size: 0.9rem;
        }}
        
        .stat-value {{
            color: #ffd700;
            font-weight: bold;
        }}
        
        .legend {{
            position: fixed;
            bottom: 20px;
            right: 20px;
            background: rgba(0,0,0,0.8);
            border-radius: 10px;
            padding: 15px;
            z-index: 1000;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255,255,255,0.1);
        }}
        
        .legend h4 {{
            margin: 0 0 10px 0;
            color: #ffd700;
            font-size: 0.9rem;
        }}
        
        .legend-item {{
            display: flex;
            align-items: center;
            margin: 5px 0;
            font-size: 0.8rem;
        }}
        
        .legend-color {{
            width: 12px;
            height: 12px;
            border-radius: 50%;
            margin-right: 8px;
        }}
        
        .loading {{
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background: rgba(0,0,0,0.9);
            padding: 30px;
            border-radius: 15px;
            text-align: center;
            z-index: 2000;
        }}
        
        .spinner {{
            border: 3px solid rgba(255,255,255,0.3);
            border-top: 3px solid #ffd700;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            animation: spin 1s linear infinite;
            margin: 0 auto 15px;
        }}
        
        @keyframes spin {{
            0% {{ transform: rotate(0deg); }}
            100% {{ transform: rotate(360deg); }}
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🚂 Real-time Railway Map - Live Train Tracking</h1>
        <p>AI-Powered Train Traffic Control | Smart India Hackathon 2025 | Ministry of Railways</p>
    </div>
    
    <div class="loading" id="loading">
        <div class="spinner"></div>
        <p>Loading Railway Network...</p>
    </div>
    
    <div class="map-container">
        <div id="map"></div>
    </div>
    
    <div class="control-panel">
        <h3>🚂 Live Trains</h3>
        <div id="train-list">
            <!-- Train list will be populated here -->
        </div>
    </div>
    
    <div class="stats">
        <div class="stat-item">
            <span>Total Trains:</span>
            <span class="stat-value" id="total-trains">0</span>
        </div>
        <div class="stat-item">
            <span>Running:</span>
            <span class="stat-value" id="running-trains">0</span>
        </div>
        <div class="stat-item">
            <span>Average Speed:</span>
            <span class="stat-value" id="avg-speed">0 km/h</span>
        </div>
        <div class="stat-item">
            <span>Last Update:</span>
            <span class="stat-value" id="last-update">--:--:--</span>
        </div>
    </div>
    
    <div class="legend">
        <h4>Legend</h4>
        <div class="legend-item">
            <div class="legend-color" style="background: #ffd700;"></div>
            <span>Terminal Station</span>
        </div>
        <div class="legend-item">
            <div class="legend-color" style="background: #4CAF50;"></div>
            <span>Junction Station</span>
        </div>
        <div class="legend-item">
            <div class="legend-color" style="background: #2196F3;"></div>
            <span>Main Line</span>
        </div>
        <div class="legend-item">
            <div class="legend-color" style="background: #FF9800;"></div>
            <span>Suburban Line</span>
        </div>
    </div>

    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
    <script>
        // Initialize map centered on India
        const map = L.map('map').setView([20.5937, 78.9629], 5);
        
        // Add OpenStreetMap tiles
        L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png', {{
            attribution: '© OpenStreetMap contributors',
            maxZoom: 18
        }}).addTo(map);
        
        // Add dark theme tiles
        L.tileLayer('https://{{s}}.basemaps.cartocdn.com/dark_all/{{z}}/{{x}}/{{y}}{{r}}.png', {{
            attribution: '© CARTO',
            subdomains: 'abcd',
            maxZoom: 19
        }}).addTo(map);
        
        // Data storage
        let stations = [];
        let tracks = [];
        let trains = [];
        let trainMarkers = {{}};
        let trackLines = [];
        let stationMarkers = [];
        let selectedTrain = null;
        
        // Train icons
        const trainIcon = L.divIcon({{
            className: 'train-marker',
            html: '🚂',
            iconSize: [30, 30],
            iconAnchor: [15, 15]
        }});
        
        const selectedTrainIcon = L.divIcon({{
            className: 'selected-train-marker',
            html: '🚂',
            iconSize: [40, 40],
            iconAnchor: [20, 20]
        }});
        
        // Station icons
        const terminalIcon = L.divIcon({{
            className: 'terminal-marker',
            html: '🏢',
            iconSize: [25, 25],
            iconAnchor: [12, 12]
        }});
        
        const junctionIcon = L.divIcon({{
            className: 'junction-marker',
            html: '🚉',
            iconSize: [20, 20],
            iconAnchor: [10, 10]
        }});
        
        // Load initial data
        async function loadMapData() {{
            try {{
                const response = await fetch('/api/map-data');
                const data = await response.json();
                
                stations = data.stations;
                tracks = data.tracks;
                trains = data.trains;
                
                initializeMap();
                updateTrainList();
                updateStats();
                
                // Hide loading screen
                document.getElementById('loading').style.display = 'none';
                
            }} catch (error) {{
                console.error('Error loading map data:', error);
                // Use fallback data
                loadFallbackData();
            }}
        }}
        
        function loadFallbackData() {{
            // Fallback data if API is not available
            stations = [
                {{"id": "MUM", "name": "Mumbai Central", "lat": 19.0176, "lon": 72.8562, "type": "terminal", "platforms": 12}},
                {{"id": "DLI", "name": "Delhi", "lat": 28.6600, "lon": 77.2300, "type": "terminal", "platforms": 16}},
                {{"id": "MAS", "name": "Chennai Central", "lat": 13.0827, "lon": 80.2707, "type": "terminal", "platforms": 12}},
                {{"id": "SBC", "name": "Bangalore City", "lat": 12.9716, "lon": 77.5946, "type": "terminal", "platforms": 10}},
                {{"id": "THA", "name": "Thane", "lat": 19.1972, "lon": 72.9702, "type": "junction", "platforms": 8}},
                {{"id": "HYB", "name": "Hyderabad", "lat": 17.3850, "lon": 78.4867, "type": "junction", "platforms": 8}}
            ];
            
            tracks = [
                {{"id": "MUM-DLI", "from": {{"lat": 19.0176, "lon": 72.8562}}, "to": {{"lat": 28.6600, "lon": 77.2300}}, "distance": 1384, "max_speed": 160, "type": "main"}},
                {{"id": "MAS-SBC", "from": {{"lat": 13.0827, "lon": 80.2707}}, "to": {{"lat": 12.9716, "lon": 77.5946}}, "distance": 362, "max_speed": 120, "type": "main"}},
                {{"id": "MUM-THA", "from": {{"lat": 19.0176, "lon": 72.8562}}, "to": {{"lat": 19.1972, "lon": 72.9702}}, "distance": 35, "max_speed": 80, "type": "suburban"}}
            ];
            
            trains = [
                {{"id": "T001", "train_number": "12345", "train_type": "Rajdhani Express", "origin": "MUM", "destination": "DLI", "current_station": "MUM", "next_station": "THA", "lat": 19.0176, "lon": 72.8562, "speed": 120, "status": "running", "progress": 0.3}},
                {{"id": "T002", "train_number": "67890", "train_type": "Shatabdi Express", "origin": "MAS", "destination": "SBC", "current_station": "MAS", "next_station": "SBC", "lat": 13.0827, "lon": 80.2707, "speed": 130, "status": "running", "progress": 0.5}},
                {{"id": "T003", "train_number": "11111", "train_type": "Freight Train", "origin": "MUM", "destination": "THA", "current_station": "MUM", "next_station": "THA", "lat": 19.0176, "lon": 72.8562, "speed": 80, "status": "running", "progress": 0.7}}
            ];
            
            initializeMap();
            updateTrainList();
            updateStats();
            document.getElementById('loading').style.display = 'none';
        }}
        
        function initializeMap() {{
            // Clear existing markers
            stationMarkers.forEach(marker => map.removeLayer(marker));
            trackLines.forEach(line => map.removeLayer(line));
            Object.values(trainMarkers).forEach(marker => map.removeLayer(marker));
            
            stationMarkers = [];
            trackLines = [];
            trainMarkers = {{}};
            
            // Add stations
            stations.forEach(station => {{
                const icon = station.type === 'terminal' ? terminalIcon : junctionIcon;
                const marker = L.marker([station.lat, station.lon], {{icon: icon}})
                    .addTo(map)
                    .bindPopup(`
                        <div style="color: black;">
                            <h3>${{station.name}}</h3>
                            <p><strong>Type:</strong> ${{station.type}}</p>
                            <p><strong>Platforms:</strong> ${{station.platforms}}</p>
                            <p><strong>Code:</strong> ${{station.id}}</p>
                        </div>
                    `);
                stationMarkers.push(marker);
            }});
            
            // Add track lines
            tracks.forEach(track => {{
                const color = track.type === 'main' ? '#2196F3' : '#FF9800';
                const line = L.polyline([
                    [track.from.lat, track.from.lon],
                    [track.to.lat, track.to.lon]
                ], {{
                    color: color,
                    weight: 3,
                    opacity: 0.7
                }}).addTo(map);
                
                line.bindPopup(`
                    <div style="color: black;">
                        <h4>${{track.id}}</h4>
                        <p><strong>Distance:</strong> ${{track.distance}} km</p>
                        <p><strong>Max Speed:</strong> ${{track.max_speed}} km/h</p>
                        <p><strong>Type:</strong> ${{track.type}}</p>
                    </div>
                `);
                
                trackLines.push(line);
            }});
            
            // Add train markers
            trains.forEach(train => {{
                const marker = L.marker([train.lat, train.lon], {{icon: trainIcon}})
                    .addTo(map)
                    .bindPopup(`
                        <div style="color: black;">
                            <h3>${{train.train_number}}</h3>
                            <p><strong>Type:</strong> ${{train.train_type}}</p>
                            <p><strong>Route:</strong> ${{train.origin}} → ${{train.destination}}</p>
                            <p><strong>Speed:</strong> ${{train.speed}} km/h</p>
                            <p><strong>Status:</strong> ${{train.status}}</p>
                            <p><strong>Progress:</strong> ${{Math.round(train.progress * 100)}}%</p>
                        </div>
                    `);
                
                marker.on('click', () => selectTrain(train.id));
                trainMarkers[train.id] = marker;
            }});
        }}
        
        function updateTrainList() {{
            const trainList = document.getElementById('train-list');
            trainList.innerHTML = '';
            
            trains.forEach(train => {{
                const trainItem = document.createElement('div');
                trainItem.className = 'train-item';
                if (selectedTrain === train.id) {{
                    trainItem.classList.add('selected');
                }}
                
                trainItem.innerHTML = `
                    <div class="train-number">${{train.train_number}}</div>
                    <div class="train-route">${{train.train_type}}</div>
                    <div class="train-route">${{train.origin}} → ${{train.destination}}</div>
                    <div class="train-status status-${{train.status}}">${{train.status}}</div>
                `;
                
                trainItem.onclick = () => selectTrain(train.id);
                trainList.appendChild(trainItem);
            }});
        }}
        
        function selectTrain(trainId) {{
            selectedTrain = trainId;
            
            // Update train list selection
            document.querySelectorAll('.train-item').forEach(item => {{
                item.classList.remove('selected');
            }});
            
            // Update train markers
            Object.entries(trainMarkers).forEach(([id, marker]) => {{
                if (id === trainId) {{
                    marker.setIcon(selectedTrainIcon);
                    map.setView([trains.find(t => t.id === trainId).lat, trains.find(t => t.id === trainId).lon], 8);
                }} else {{
                    marker.setIcon(trainIcon);
                }}
            }});
            
            updateTrainList();
        }}
        
        function updateStats() {{
            const runningTrains = trains.filter(t => t.status === 'running').length;
            const avgSpeed = trains.length > 0 ? Math.round(trains.reduce((sum, t) => sum + t.speed, 0) / trains.length) : 0;
            
            document.getElementById('total-trains').textContent = trains.length;
            document.getElementById('running-trains').textContent = runningTrains;
            document.getElementById('avg-speed').textContent = avgSpeed + ' km/h';
            document.getElementById('last-update').textContent = new Date().toLocaleTimeString();
        }}
        
        // Simulate real-time updates
        function simulateRealTimeUpdates() {{
            trains.forEach(train => {{
                if (train.status === 'running') {{
                    // Simulate movement
                    const speedFactor = train.speed / 100;
                    train.progress += speedFactor * 0.01;
                    
                    if (train.progress > 1) {{
                        train.progress = 0;
                        // Simulate reaching destination
                        if (Math.random() < 0.1) {{
                            train.status = 'arrived';
                        }}
                    }}
                    
                    // Update position based on progress
                    const originStation = stations.find(s => s.id === train.origin);
                    const destStation = stations.find(s => s.id === train.destination);
                    
                    if (originStation && destStation) {{
                        train.lat = originStation.lat + (destStation.lat - originStation.lat) * train.progress;
                        train.lon = originStation.lon + (destStation.lon - originStation.lon) * train.progress;
                    }}
                }}
            }});
            
            // Update map
            Object.entries(trainMarkers).forEach(([id, marker]) => {{
                const train = trains.find(t => t.id === id);
                if (train) {{
                    marker.setLatLng([train.lat, train.lon]);
                }}
            }});
            
            updateStats();
        }}
        
        // Start the application
        loadMapData();
        
        // Update every 2 seconds
        setInterval(simulateRealTimeUpdates, 2000);
        
        // Update train list every 5 seconds
        setInterval(updateTrainList, 5000);
    </script>
</body>
</html>
    """
    
    with open('realtime_railway_map.html', 'w') as f:
        f.write(html_content)
    
    print(f"\n🗺️ Real-time Railway Map created: realtime_railway_map.html")
    return html_content

def create_map_api():
    """Create a simple API endpoint for map data"""
    from http.server import HTTPServer, BaseHTTPRequestHandler
    import json
    
    class MapAPIHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            if self.path == '/api/map-data':
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                
                map_data = railway_map.get_map_data()
                self.wfile.write(json.dumps(map_data).encode())
                
            elif self.path == '/api/section-status':
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                
                section_data = railway_map.get_section_status()
                self.wfile.write(json.dumps(section_data).encode())
                
            else:
                self.send_response(404)
                self.end_headers()
        
        def log_message(self, format, *args):
            pass  # Suppress log messages
    
    return MapAPIHandler

def run_realtime_demo():
    """Run the real-time railway map demonstration"""
    print("🗺️ REAL-TIME RAILWAY MAP SYSTEM")
    print("=" * 60)
    print("Interactive Map with Live Train Tracking")
    print("Smart India Hackathon 2025 - Ministry of Railways")
    print("=" * 60)
    
    # Create the HTML map
    create_realtime_map_html()
    
    # Start API server
    import threading
    from http.server import HTTPServer
    
    def start_api_server():
        handler = create_map_api()
        server = HTTPServer(('localhost', 8081), handler)
        print(f"🌐 API Server started on http://localhost:8081")
        server.serve_forever()
    
    api_thread = threading.Thread(target=start_api_server, daemon=True)
    api_thread.start()
    
    # Wait a moment for server to start
    time.sleep(1)
    
    print(f"\n✅ Real-time Railway Map System Ready!")
    print(f"🗺️ Map Interface: realtime_railway_map.html")
    print(f"🌐 API Endpoint: http://localhost:8081/api/map-data")
    print(f"📱 Open the map in your browser to see live train tracking!")
    
    # Show current system status
    map_data = railway_map.get_map_data()
    print(f"\n📊 Current System Status:")
    print(f"🚉 Stations: {len(map_data['stations'])}")
    print(f"🛤️ Track Segments: {len(map_data['tracks'])}")
    print(f"🚂 Active Trains: {len(map_data['trains'])}")
    
    running_trains = [t for t in map_data['trains'] if t['status'] == 'running']
    print(f"🏃 Running Trains: {len(running_trains)}")
    
    if running_trains:
        print(f"\n🚂 Live Train Positions:")
        for train in running_trains[:5]:  # Show first 5 trains
            print(f"   {train['train_number']} ({train['train_type']})")
            print(f"     Position: {train['lat']:.4f}, {train['lon']:.4f}")
            print(f"     Speed: {train['speed']} km/h")
            print(f"     Progress: {train['progress']:.1%}")
    
    return railway_map

if __name__ == "__main__":
    # Run the real-time railway map system
    system = run_realtime_demo()
    
    # Keep the system running
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print(f"\n🛑 Real-time Railway Map System stopped.")
