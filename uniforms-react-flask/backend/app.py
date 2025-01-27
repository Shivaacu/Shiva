from flask import Flask, jsonify, request, send_from_directory, Response
from flask_cors import CORS
from werkzeug.utils import secure_filename
from camera import Video
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Configure upload folder
app.config['UPLOAD_FOLDER'] = 'uploads'

video = Video()

@app.route('/api/video_feed')
def video_feed():
    return Response(gen(video),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/api/get_detection_frames')
def get_detection_frames():
    warning_frames = [f for f in os.listdir('static/detection_frames') if f.endswith('.jpg')]
    return jsonify({"frames": warning_frames})

@app.route('/api/get_detections')
def get_detections():
    return jsonify(video.get_detections())

@app.route('/api/get_missing_items')
def get_missing_items():
    return jsonify(video.get_missing_items())

@app.route('/api/upload_video', methods=['POST'])
def upload_video():
    if 'video' not in request.files:
        return jsonify({"message": "No video file uploaded"}), 400
    
    video_file = request.files['video']
    if video_file.filename == '':
        return jsonify({"message": "No video file selected"}), 400
    
    if video_file and allowed_file(video_file.filename):
        filename = secure_filename(video_file.filename)
        video_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        video.set_video_source(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return jsonify({"message": "Video uploaded successfully"}), 200
    
    return jsonify({"message": "Invalid file type"}), 400

@app.route('/static/detection_frames/<path:filename>')
def serve_detection_frame(filename):
    return send_from_directory('static/detection_frames', filename)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'mp4', 'avi', 'mov', 'mkv'}

def gen(camera):
    while True:
        frame = camera.get_frame()
        if frame is None:
            break
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

if __name__ == '__main__':
    app.run(debug=True)
