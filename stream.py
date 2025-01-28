from flask import Flask, Response
from picamera2 import Picamera2
import cv2
import numpy as np

# Initialize the Flask application
app = Flask(__name__)

# Initialize the PiCamera2
picam2 = Picamera2()
picam2.configure(picam2.create_video_configuration(main={"size": (1920, 1080)}))
picam2.start()

@app.route('/')
def index():
    return "<h1>Raspberry Pi Camera Live Stream</h1><p>Visit <a href='/video'>/video</a> for live feed</p>"

@app.route('/video')
def video():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

def gen_frames():
    """Generate video frames for streaming."""
    while True:
        frame = picam2.capture_array()
        # Convert BGR to RGB to fix color inversion
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # Convert the frame to JPEG
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        # Yield frame data to be used in HTTP response
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)
    finally:
        picam2.stop()
