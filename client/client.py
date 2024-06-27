import socketio
import requests
import os
import base64
import logging

# Configurações de comunicação
RPC_URL = 'http://127.0.0.1:5000/detectar'
WEBSOCKET_URL = 'http://127.0.0.1:5001'
IMAGEM_SAIDA_PATH = 'imagem_processada.png'

# Inicialização do cliente WebSocket
sio = socketio.Client()

# Configuração do logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger()

@sio.event
def connect():
    logger.info('Conectado ao servidor WebSocket')
    sio.emit('mensagem', {'status': 'Cliente conectado'})

@sio.event
def disconnect():
    logger.info('Desconectado do servidor WebSocket')

@sio.event
def log(data):
    logger.info(f'Log recebido do WebSocket: {data["log"]}')

@sio.event
def resultado(data):
    logger.info(f'Resultado recebido do WebSocket: {data}')
    if 'image' in data:
        imagem_saida_path = os.path.join(os.path.dirname(__file__), IMAGEM_SAIDA_PATH)
        with open(imagem_saida_path, "wb") as f:
            f.write(base64.b64decode(data['image']))
        logger.info(f'Imagem processada salva como {imagem_saida_path}')

def enviar_imagem_para_rpc(imagem_base64):
    try:
        resposta = requests.post(RPC_URL, files={'file': base64.b64decode(imagem_base64)})
        if resposta.status_code == 200:
            resultado = resposta.json()
            logger.info(f'Resposta do RPC: {resultado}')
            sio.emit('resultado', resultado)
            sio.emit('mensagem', {'status': 'Imagem processada pelo RPC'})
        else:
            logger.error(f'Erro ao enviar imagem para o RPC: {resposta.json()}')
            sio.emit('mensagem', {'status': 'Erro ao processar imagem no RPC'})
    except Exception as e:
        logger.error(f'Erro ao enviar imagem para RPC: {e}')
        sio.emit('mensagem', {'status': f'Erro ao enviar imagem: {str(e)}'})

def main():
    # Conectar ao WebSocket
    sio.connect(WEBSOCKET_URL)

    sio.emit('mensagem', {'status': 'Cliente iniciado'})

    sio.wait()

if __name__ == '__main__':
    main()
