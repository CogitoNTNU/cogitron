import cv2
from flask import Flask, Response, render_template_string
from cogitron.camera import get_camera_config

camera_config = get_camera_config()

app = Flask(__name__)

# HTML template for simple homepage
HTML_PAGE = """
<html>
  <head>
    <title>Live Video Stream</title>
  </head>
  <body>
    <h1>Live Camera Feed</h1>
    <img src="/video_feed" width="640" height="480">
  </body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_PAGE)

def generate_frames():
    camera = cv2.VideoCapture(camera_config.index_or_path)
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            _, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=True)