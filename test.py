import cv2
from flask import Flask, render_template, Response
import urllib.request

app = Flask(__name__)

# URL of the online video stream
video_url = "https://vdo.ninja/?view=t5mGjyH"

# Function to fetch frames from the video stream
def get_frames():
    stream = urllib.request.urlopen(video_url)
    bytes = bytes()
    while True:
        bytes += stream.read(1024)
        a = bytes.find(b'\xff\xd8')
        b = bytes.find(b'\xff\xd9')
        if a != -1 and b != -1:
            jpg = bytes[a:b + 2]
            bytes = bytes[b + 2:]
            frame = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
            yield frame

# Function to generate video frames
def generate_frames():
    for frame in get_frames():
        # Encode the frame in JPEG format
        ret, buffer = cv2.imencode('.jpg', frame)
        # Convert the frame into bytes
        frame_bytes = buffer.tobytes()
        # Yield the frame in byte format
        yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

# Route to the home page
@app.route('/')
def index():
    return render_template('index.html')

# Route to video feed
@app.route('/video_feed')
def video_feed():
    # Return the response generated along with the specific media type (mime type)
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(debug=True)
