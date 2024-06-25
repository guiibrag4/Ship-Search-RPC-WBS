import socketio
import requests

# Cliente para o servidor RPC
url_rpc = 'http://127.0.0.1:5000/detectar'
resposta = requests.post(url_rpc, json={'dados': 'teste'})
print(f'Resposta RPC: {resposta.json()}')

# Cliente para o servidor WebSocket
sio = socketio.Client()

@sio.event
def conectar():
    print('Conectado ao servidor WebSocket')

@sio.event
def progresso(dados):
    print(f'Atualização de progresso: {dados}')

@sio.event
def resultado(dados):
    print(f'Resultado final: {dados}')

@sio.event
def desconectar():
    print('Desconectado do servidor WebSocket')

sio.connect('http://127.0.0.1:5001')
sio.send('Olá do cliente')
sio.wait()
