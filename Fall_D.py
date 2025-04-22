import cv2
import numpy as np
import time
import os

class FallDetector:
    def __init__(self):
        # Initialize background subtractor
        self.fgbg = cv2.createBackgroundSubtractorMOG2(history=500, varThreshold=16, detectShadows=False)
        
        # Fall detection parameters
        self.aspect_ratio_threshold = 0.6  # Lowered for better sensitivity
        self.min_contour_area = 2000       # Increased to ignore small movements
        self.stationary_time = 1.5         # Seconds of inactivity to confirm fall
        self.impact_threshold = 2.0        # Size change ratio for impact detection
        
        # State variables
        self.last_motion_time = time.time()
        self.last_aspect_ratio = None
        self.fall_detected = False
        self.alert_cooldown = 0

    def detect_fall(self, frame):
        # Preprocessing
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (7, 7), 0)
        
        # Background subtraction
        fgmask = self.fgbg.apply(blurred)
        _, fgmask = cv2.threshold(fgmask, 127, 255, cv2.THRESH_BINARY)
        
        # Noise removal
        kernel = np.ones((7,7), np.uint8)
        fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel)
        fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_CLOSE, kernel)
        
        # Find contours
        contours, _ = cv2.findContours(fgmask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        motion_detected = False
        fall_conditions_met = False
        current_aspect_ratio = None
        
        for contour in contours:
            if cv2.contourArea(contour) < self.min_contour_area:
                continue
                
            motion_detected = True
            self.last_motion_time = time.time()
            
            # Get bounding box
            x, y, w, h = cv2.boundingRect(contour)
            current_aspect_ratio = float(h)/w
            
            # Check for sudden change in aspect ratio (impact)
            if self.last_aspect_ratio and (self.last_aspect_ratio / current_aspect_ratio) > self.impact_threshold:
                print(f"Impact detected! Ratio change: {self.last_aspect_ratio:.2f} -> {current_aspect_ratio:.2f}")
                fall_conditions_met = True
            
            # Check if person is lying down
            if current_aspect_ratio < self.aspect_ratio_threshold:
                fall_conditions_met = True
            
            self.last_aspect_ratio = current_aspect_ratio
            cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), 2)
            cv2.putText(frame, f"Ratio: {current_aspect_ratio:.2f}", (x, y-10), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1)
        
        # Fall confirmation logic
        if fall_conditions_met:
            inactivity_duration = time.time() - self.last_motion_time
            print(f"Fall conditions met. Inactivity: {inactivity_duration:.2f}s")
            
            if inactivity_duration > self.stationary_time:
                if not self.fall_detected:
                    self.fall_detected = True
                    return True, frame
        else:
            self.fall_detected = False
        
        return False, frame

def process_video_file(video_path):
    detector = FallDetector()
    
    if not os.path.exists(video_path):
        print(f"Error: File not found at {video_path}")
        return
    
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Error: Could not open video file {video_path}")
        return
    
    fps = cap.get(cv2.CAP_PROP_FPS)
    delay = int(1000/fps) if fps > 0 else 30
    
    print("Processing video...")
    print("Press 'q' to quit")
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
            
        frame = cv2.resize(frame, (640, 480))  # Standardize size
        
        fall_detected, processed_frame = detector.detect_fall(frame)
        
        if fall_detected:
            cv2.putText(processed_frame, "FALL DETECTED!", (50, 50), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            print("ALERT: Fall detected!")
        
        cv2.imshow('Fall Detection', processed_frame)
        
        if cv2.waitKey(delay) & 0xFF == ord('q'):
            break
            
    cap.release()
    cv2.destroyAllWindows()
    print("Processing complete")

if __name__ == "__main__":
    video_file = "fall.mp4"  # Change to your video filename
    
    # List files in current directory to help debugging
    print("Files in current directory:")
    print(os.listdir('.'))
    
    process_video_file(video_file)