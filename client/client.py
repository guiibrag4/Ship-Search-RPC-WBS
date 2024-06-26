import socketio
import requests
import os
import cv2 as cv
import base64
import time

# Configurações
RPC_URL = 'http://127.0.0.1:5000/detectar'
WEBSOCKET_URL = 'http://127.0.0.1:5001'

# Inicialização do cliente WebSocket
sio = socketio.Client()

@sio.event
def connect():
    print('Conectado ao servidor WebSocket')
    sio.emit('mensagem', {'status': 'Cliente conectado'})

@sio.event
def disconnect():
    print('Desconectado do servidor WebSocket')

@sio.event
def log(data):
    print(f'Log recebido do WebSocket: {data["log"]}')

@sio.event
def resultado(data):
    print(f'Resultado recebido do WebSocket: {data}')

def enviar_imagem_para_rpc(imagem_path):
    try:
        with open(imagem_path, 'rb') as imagem:
            files = {'file': imagem}
            resposta = requests.post(RPC_URL, files=files)
            if resposta.status_code == 200:
                resultado = resposta.json()
                print(f'Resposta do RPC: {resultado}')
                sio.emit('resultado', resultado)
                sio.emit('mensagem', {'status': 'Imagem processada pelo RPC'})
            else:
                print(f'Erro ao enviar imagem para o RPC: {resposta.json()}')
                sio.emit('mensagem', {'status': 'Erro ao processar imagem no RPC'})
    except Exception as e:
        print(f'Erro ao enviar imagem para RPC: {e}')
        sio.emit('mensagem', {'status': f'Erro ao enviar imagem: {str(e)}'})

def main():
    # Conectar ao WebSocket
    sio.connect(WEBSOCKET_URL)
    
    # Log inicial
    sio.emit('mensagem', {'status': 'Cliente iniciado'})

    # Exemplo: Enviar uma imagem para o RPC
    imagem_path = 'caminho/para/sua/imagem.png'
    if os.path.exists(imagem_path):
        print(f'Enviando imagem {imagem_path} para o RPC...')
        enviar_imagem_para_rpc(imagem_path)
    else:
        print(f'Arquivo de imagem não encontrado: {imagem_path}')
        sio.emit('mensagem', {'status': 'Arquivo de imagem não encontrado'})

    sio.wait()

if __name__ == '__main__':
    main()
