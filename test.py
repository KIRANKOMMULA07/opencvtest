from flask import Flask, Response, render_template
import cv2
import urllib.request

app = Flask(__name__)

# Function to generate frames from an external video source
def generate_frames():
    # Replace 'your_external_video_source_url' with the URL of your external video source
    url = 'https://vdo.ninja/?view=fFSDisK'

    # Open the video stream
    stream = urllib.request.urlopen(url)

    # Create a VideoCapture object to read frames from the video stream
    cap = cv2.VideoCapture()
    cap.open(stream)

    # Check if the video stream is opened correctly
    if not cap.isOpened():
        print("Error: Could not open video stream")
        return

    while True:
        # Read a frame from the video stream
        ret, frame = cap.read()
        if not ret:
            break

        # Encode the frame to JPEG format
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        # Yield the frame in a multipart response
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    # Release the video stream
    cap.release()

# Route to render the index.html template
@app.route('/')
def index():
    return render_template('index.html')

# Route to stream video frames
@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)
