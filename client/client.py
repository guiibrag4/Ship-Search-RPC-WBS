import socketio
import logging

sio = socketio.Client(logger=True, engineio_logger=True)

@sio.event
def conectar():
    logging.info('Conectado ao servidor WebSocket')

@sio.event
def progresso(dados):
    logging.info(f'Atualização de progresso: {dados}')

@sio.event
def resultado(dados):
    logging.info(f'Resultado final: {dados}')

@sio.event
def erro(dados):
    logging.info(f'Erro: {dados["error"]}')

@sio.event
def desconectar():
    logging.info('Desconectado do servidor WebSocket')

logging.basicConfig(level=logging.DEBUG)

sio.connect('http://127.0.0.1:5001')
sio.send('Olá do cliente')
sio.wait()
