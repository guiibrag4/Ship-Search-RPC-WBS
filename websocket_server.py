from flask import Flask
from flask_socketio import SocketIO, emit
import requests
import json
import base64

app = Flask(__name__)
socketio = SocketIO(app)

RPC_SERVER_URL = "http://localhost:5001/rpc"

@app.route('/')
def index():
    return 'WebSocket server is running!'

@socketio.on('process_image')
def handle_process_image(data):
    image_path = data['image_path']
    rpc_request = json.dumps({
        "jsonrpc": "2.0",
        "method": "process_image_rpc",
        "params": {"image_path": image_path},
        "id": 1
    })

    try:
        response = requests.post(RPC_SERVER_URL, data=rpc_request, headers={"Content-Type": "application/json"})
        response_json = response.json()
        if "result" in response_json:
            img_bytes = response_json["result"].encode('latin1')
            img_base64 = base64.b64encode(img_bytes).decode('utf-8')
            emit('image_processed', {'image': img_base64})
        else:
            emit('error', {'message': response_json.get("error", "Unknown error")})
    except Exception as e:
        emit('error', {'message': str(e)})

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5002)
