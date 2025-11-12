import cv2
import numpy as np
from ultralytics import YOLO
import os

class CCTVAnalyzer:
    def __init__(self, model_path='yolov8n.pt'):
        self.model = YOLO(model_path)
        self.anomaly_threshold = 0.5
        
        # Object weights for threat calculation
        self.object_weights = {
            'person': 0.1,
            'car': 0.05,
            'truck': 0.1,
            'bus': 0.1,
            'motorcycle': 0.08,
            'bicycle': 0.03,
            'fire': 0.9,
            'knife': 0.8,
            'gun': 0.9,
        }
    
    def analyze_video_frame(self, frame_path):
        """Analyze a single frame for anomalies and threats"""
        try:
            # Check if file exists
            if not os.path.exists(frame_path):
                print(f"Frame path does not exist: {frame_path}")
                return None
            
            # Run YOLO inference
            results = self.model(frame_path)
            result = results[0]
            
            detections = {
                'people': 0,
                'vehicles': 0,
                'weapons': 0,
                'fire': 0,
                'objects': []
            }
            
            threat_score = 0
            
            for box in result.boxes:
                class_id = int(box.cls[0])
                class_name = result.names[class_id]
                confidence = float(box.conf[0])
                
                # Count specific object types
                if class_name == 'person':
                    detections['people'] += 1
                    threat_score += self.object_weights.get('person', 0.1) * confidence
                elif class_name in ['car', 'truck', 'bus', 'motorcycle', 'bicycle']:
                    detections['vehicles'] += 1
                    threat_score += self.object_weights.get(class_name, 0.05) * confidence
                elif class_name in ['knife', 'gun']:
                    detections['weapons'] += 1
                    threat_score += self.object_weights.get(class_name, 0.8) * confidence
                elif class_name == 'fire':
                    detections['fire'] += 1
                    threat_score += self.object_weights.get('fire', 0.9) * confidence
                
                detections['objects'].append({
                    'class': class_name,
                    'confidence': confidence,
                    'bbox': box.xyxy[0].tolist()
                })
            
            # Adjust threat score based on crowd density
            if detections['people'] > 20:
                threat_score += 0.3
            if detections['people'] > 50:
                threat_score += 0.5
            
            # Calculate threat level
            threat_level = self._calculate_threat_level(threat_score)
            
            return {
                'detections': detections,
                'threat_level': threat_level,
                'threat_score': threat_score,
                'crowd_density': detections['people'],
                'anomaly_detected': threat_level != 'LOW'
            }
            
        except Exception as e:
            print(f"Error analyzing frame {frame_path}: {e}")
            return None
    
    def _calculate_threat_level(self, threat_score):
        """Calculate threat level based on threat score"""
        if threat_score > 1.5:
            return "HIGH"
        elif threat_score > 0.8:
            return "MEDIUM"
        else:
            return "LOW"
    
    def process_video(self, video_path, output_dir=None, frame_interval=10):
        """Process entire video and extract key frames"""
        try:
            cap = cv2.VideoCapture(video_path)
            frame_count = 0
            analysis_results = []
            
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break
                
                if frame_count % frame_interval == 0:
                    # Save frame temporarily
                    temp_frame_path = f"temp_frame_{frame_count}.jpg"
                    cv2.imwrite(temp_frame_path, frame)
                    
                    # Analyze frame
                    result = self.analyze_video_frame(temp_frame_path)
                    if result:
                        analysis_results.append(result)
                    
                    # Clean up
                    os.remove(temp_frame_path)
                
                frame_count += 1
            
            cap.release()
            return analysis_results
            
        except Exception as e:
            print(f"Error processing video: {e}")
            return []