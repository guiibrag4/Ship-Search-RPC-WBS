import eventlet
eventlet.monkey_patch()

from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import requests
import base64
import logging
import eventlet
import eventlet.wsgi

eventlet.monkey_patch()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'segredo!'
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')

logging.basicConfig(level=logging.DEBUG)

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def connect():
    logging.info('Cliente conectado')

@socketio.on('disconnect')
def disconnect():
    logging.info('Cliente desconectado')

@socketio.on('processar_imagem')
def processar_imagem(data):
    try:
        logging.debug('Recebendo imagem do cliente...')
        imagem_base64 = data['imagem']
        imagem_bytes = base64.b64decode(imagem_base64)

        response = requests.post('http://127.0.0.1:5002/detectar', files={'file': ('imagem.png', imagem_bytes, 'image/png')})
        
        if response.ok:
            resultado = response.json()
            logging.debug('Imagem processada com sucesso no servidor RPC.')
            socketio.emit('resultado_imagem', resultado)
        else:
            logging.error('Erro ao processar a imagem no servidor RPC.')
            socketio.emit('erro', {'error': 'Erro ao processar a imagem no servidor RPC.'})
    
    except Exception as e:
        logging.error(f'Erro: {str(e)}')
        socketio.emit('erro', {'error': str(e)})

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5001, debug=True)
