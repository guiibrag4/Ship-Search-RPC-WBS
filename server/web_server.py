from flask import Flask, render_template, request, jsonify
import base64
import socketio

app = Flask(__name__)
sio = socketio.Client()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    try:
        file = request.files['file']
        image = file.read()

        # Codificar a imagem para base64
        image_base64 = base64.b64encode(image).decode('utf-8')

        # Enviar a imagem para o servidor RPC através do WebSocket
        sio.connect('http://127.0.0.1:5001')
        sio.emit('imagem', {'image': image_base64})
        sio.disconnect()

        return jsonify({'status': 'Imagem enviada com sucesso'})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
