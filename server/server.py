from flask import Flask, request, jsonify, Response, render_template_string
import base64
import threading
import queue

app = Flask(__name__)

MAX_QUEUE_SIZE = 30
CLEAR_INTERVAL = 120
image_queue = queue.Queue(MAX_QUEUE_SIZE)
lock = threading.Lock()

@app.route('/api/upload_image', methods=['POST'])
def upload_image():
    data = request.json
    image_data = base64.b64decode(data['image'])
    with lock:
        if image_queue.full():
            image_queue.get()  # Drop the oldest image
        image_queue.put(image_data)
    return jsonify({'status': 'success'}), 200

def generate():
    while True:
        frame = None
        with lock:
            if not image_queue.empty():
                frame = image_queue.get()
        if frame:
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


def clear_queue_periodically():
    while True:
        time.sleep(CLEAR_INTERVAL)
        with lock:
            while not image_queue.empty():
                image_queue.get()
        print("Cleared the image queue.")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)