import cv2
from ultralytics import YOLO
import numpy as np
import time
import os

class Video(object):
    def __init__(self):
        # Set the input source (video file path or camera index)
        self.input_source = r'D:\DATA\Demo\demp.mp4'  
        #self.input_source = 0  # Uncomment this line to use webcam

        # Initialize video capture
        if isinstance(self.input_source, int):
            self.video = cv2.VideoCapture(self.input_source)  # For webcam
        else:
            self.video = cv2.VideoCapture(self.input_source)  # For video file
            if not self.video.isOpened():
                raise ValueError("Unable to open video file")
            
        # Load YOLO model
        self.model = YOLO('D:\\Flask_web\\runs\\detect\\train\\weights\\best.pt')  # Replace with your model path
        
        # Initialize variables for detections and processing
        self.detections = []  # Store current detections
        self.missing_items = []  # Store missing uniform items
        self.detection_count = 0  # Count of detections made
        self.last_detection_time = 0  # Timestamp of last detection
        self.previous_frame = None  # Store previous frame for motion detection
        self.motion_detected = False  # Flag for motion detection
        self.frame_count = 0  # Count of processed frames
        
        # Create directory for saving detection frames
        if not os.path.exists('static/detection_frames'):
            os.makedirs('static/detection_frames')

        # Define class names for the YOLO model
        self.class_names = ['Shirt', 'Pants', 'Shoes', 'Id', 'No_Id', 'No_shirt', 'No_pants', 'No_shoes', 'Bad_Id', 'Badge', 'Hat', 'Phone']

    def __del__(self):
        # Release the video capture object when the instance is deleted
        self.video.release()

    def set_video_source(self, source):
        # Method to change the video source
        self.video = cv2.VideoCapture(source)

    def get_detections(self):
        # Return current detections
        return self.detections

    def get_missing_items(self):
        # Return list of missing uniform items
        return self.missing_items

    def detect_motion(self, frame):
        # Convert frame to grayscale and apply Gaussian blur
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)
        
        # Initialize previous frame if it's the first frame
        if self.previous_frame is None:
            self.previous_frame = gray
            return False
        
        # Compute absolute difference between current and previous frame
        frame_delta = cv2.absdiff(self.previous_frame, gray)
        # Apply threshold to get binary image
        thresh = cv2.threshold(frame_delta, 25, 255, cv2.THRESH_BINARY)[1]
        # Dilate the thresholded image to fill in holes
        thresh = cv2.dilate(thresh, None, iterations=2)
        
        # Define region of interest (ROI) in the center of the frame
        height, width = thresh.shape
        center_roi = thresh[int(height*0.4):int(height*0.6), int(width*0.4):int(width*0.6)]
        
        # Detect motion if the sum of pixel values in ROI exceeds threshold
        if np.sum(center_roi) > 1000:
            self.motion_detected = True
        else:
            self.motion_detected = False
        
        # Update previous frame
        self.previous_frame = gray
        return self.motion_detected
    
    def get_frame(self):
        # Read a frame from the video
        ret, frame = self.video.read()
        self.frame_count += 1
        
        # Return None if no frame is captured
        if not ret:
            return None
        
        # Resize frame to 640x640 for consistency
        #frame = cv2.resize(frame, (640, 640))
        
        # Detect motion in the frame
        motion_detected = self.detect_motion(frame)
        
        # Process every 25th frame when motion is detected
        if motion_detected and self.frame_count % 25 == 0:
            # Perform object detection using YOLO
            results = self.model(frame)
            current_time = time.time()

            detected_items = set()
            self.detections = []
            
            # Process each detection
            for r in results:
                boxes = r.boxes
                for box in boxes:
                    # Extract bounding box coordinates
                    x1, y1, x2, y2 = box.xyxy[0]
                    x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                    # Get confidence and class label
                    conf = float(box.conf)
                    cls = int(box.cls)
                    label = self.class_names[cls]
                    
                    # Store detection information
                    self.detections.append({'label': label, 'confidence': conf})
                    detected_items.add(label)
                    
                    # Draw bounding box and label on the frame
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.putText(frame, f'{label} {conf:.2f}', (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                
            # Display detected items on the frame
            cv2.putText(frame, f'Detected: {detected_items}', (frame.shape[1] - 380, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 1)
            
            # Determine missing items
            required_items = {'Shirt', 'Pants', 'Shoes', 'Id'}
            self.missing_items = list(required_items - detected_items)
            cv2.putText(frame, f'Missing: {self.missing_items}', (frame.shape[1] - 380, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 1)

            # Save the frame if enough time has passed since last save
            if current_time - self.last_detection_time > 1:
                self.detection_count += 1
                cv2.imwrite(f'static/detection_frames/detection_{self.detection_count}.jpg', frame)
                self.last_detection_time = current_time

                # Print detection information
                print(f"Frame detected: {self.frame_count}")
                print("Detected items:", detected_items)
                for detection in self.detections:
                    print(f"  {detection['label']}: {detection['confidence']:.2f}")
                print("Missing items:", self.missing_items)
                print(f"Frame saved: detection_{self.detection_count}.jpg")
                print("---")

        # Encode the frame as JPEG
        ret, jpg = cv2.imencode('.jpg', frame)
        return jpg.tobytes()
