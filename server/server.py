from flask import Flask, request, jsonify, Response, render_template_string
import base64
import threading

app = Flask(__name__)

latest_image = None
lock = threading.Lock()

@app.route('/api/upload_image', methods=['POST'])
def upload_image():
    global latest_image
    data = request.json
    with lock:
        latest_image = base64.b64decode(data['image'])
    return jsonify({'status': 'success'}), 200

def generate():
    global latest_image
    while True:
        with lock:
            if latest_image:
                frame = latest_image
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template_string('''
    <html>
        <head>
            <title>Video Stream</title>
        </head>
        <body>
            <h1>Video Stream</h1>
            <img src="/video_feed" width="640" height="480">
        </body>
    </html>
    ''')

@app.route('/video_feed')
def video_feed():
    return Response(generate(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)