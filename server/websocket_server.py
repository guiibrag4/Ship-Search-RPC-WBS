from flask import Flask, render_template
from flask_socketio import SocketIO, send, emit
import requests
import base64

app = Flask(__name__)
app.config['SECRET_KEY'] = 'segredo!'
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('mensagem')
def lidar_com_mensagem(msg):
    print(f'Mensagem recebida: {msg}')
    send(f'Eco: {msg}')

@socketio.on('imagem')
def lidar_com_imagem(data):
    print('Imagem recebida pelo WebSocket')
    image_base64 = data['image']
    
    # Enviar imagem para o servidor RPC
    resposta = requests.post('http://127.0.0.1:5000/detectar', files={'file': base64.b64decode(image_base64)})
    if resposta.status_code == 200:
        resultado = resposta.json()
        socketio.emit('resultado', resultado)
    else:
        print(f'Erro ao processar imagem: {resposta.json()}')

if __name__ == '__main__':
    socketio.run(app, debug=True, port=5001)
