import cv2
import os
from datetime import datetime
from django.utils import timezone
from django.contrib.gis.geos import Point
from ...models import CCTVAnalysis
from ..ai_analyzer import CCTVAnalyzer

class CCTVProcessor:
    def __init__(self, model_path='yolov8n.pt'):
        self.analyzer = CCTVAnalyzer(model_path)
    
    def process_video_file(self, video_path, location=None, output_dir=None, frame_interval=30):
        """Process a single video file and store analysis results"""
        try:
            if not os.path.exists(video_path):
                print(f"Video file not found: {video_path}")
                return 0
            
            cap = cv2.VideoCapture(video_path)
            frame_count = 0
            processed_count = 0
            
            # Create output directory if specified
            if output_dir and not os.path.exists(output_dir):
                os.makedirs(output_dir)
            
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break
                
                # Process every nth frame
                if frame_count % frame_interval == 0:
                    # Save frame temporarily
                    temp_frame_path = f"temp_frame_{frame_count}.jpg"
                    cv2.imwrite(temp_frame_path, frame)
                    
                    # Analyze frame
                    analysis_result = self.analyzer.analyze_video_frame(temp_frame_path)
                    
                    if analysis_result and analysis_result['anomaly_detected']:
                        # Save frame image if output directory specified
                        frame_filename = None
                        if output_dir:
                            frame_filename = f"frame_{frame_count}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
                            frame_path = os.path.join(output_dir, frame_filename)
                            cv2.imwrite(frame_path, frame)
                            frame_filename = f"cctv_frames/{os.path.basename(frame_path)}"
                        
                        # Create CCTV analysis record
                        cctv_analysis = CCTVAnalysis(
                            video_path=video_path,
                            frame_image=frame_filename or '',
                            timestamp=timezone.now(),
                            location=location,
                            crowd_density=analysis_result['crowd_density'],
                            anomaly_detected=analysis_result['anomaly_detected'],
                            detected_objects=analysis_result['detections'],
                            threat_level=analysis_result['threat_level']
                        )
                        cctv_analysis.save()
                        processed_count += 1
                    
                    # Clean up temp file
                    if os.path.exists(temp_frame_path):
                        os.remove(temp_frame_path)
                
                frame_count += 1
            
            cap.release()
            print(f"Processed {processed_count} anomalous frames from {video_path}")
            return processed_count
            
        except Exception as e:
            print(f"Error processing video file {video_path}: {e}")
            return 0
    
    def process_directory(self, directory_path, location=None, output_dir=None):
        """Process all video files in a directory"""
        video_extensions = ['.mp4', '.avi', '.mov', '.mkv', '.webm']
        processed_files = 0
        
        for filename in os.listdir(directory_path):
            file_path = os.path.join(directory_path, filename)
            if any(filename.lower().endswith(ext) for ext in video_extensions):
                print(f"Processing {filename}...")
                count = self.process_video_file(file_path, location, output_dir)
                processed_files += count
        
        print(f"Completed processing directory. Processed {processed_files} anomalous frames.")
        return processed_files
    
    def process_single_frame(self, image_path, location=None):
        """Process a single image frame"""
        try:
            analysis_result = self.analyzer.analyze_video_frame(image_path)
            
            if analysis_result:
                cctv_analysis = CCTVAnalysis(
                    video_path=image_path,
                    frame_image=image_path,
                    timestamp=timezone.now(),
                    location=location,
                    crowd_density=analysis_result['crowd_density'],
                    anomaly_detected=analysis_result['anomaly_detected'],
                    detected_objects=analysis_result['detections'],
                    threat_level=analysis_result['threat_level']
                )
                cctv_analysis.save()
                return cctv_analysis
            
            return None
            
        except Exception as e:
            print(f"Error processing single frame {image_path}: {e}")
            return None