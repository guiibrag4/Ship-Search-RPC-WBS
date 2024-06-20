import socketio
import base64

# Crie uma instância de cliente SocketIO
sio = socketio.Client()

# Defina o evento para processar a resposta do servidor
@sio.event
def connect():
    print("Conexão estabelecida!")

@sio.event
def connect_error(data):
    print("Falha na conexão!")

@sio.event
def disconnect():
    print("Desconectado do servidor!")

@sio.on('image_processed')
def on_image_processed(data):
    image_base64 = data['image']
    with open("processed_image.png", "wb") as f:
        f.write(base64.b64decode(image_base64))
    print("Imagem processada recebida e salva como processed_image.png")

@sio.on('error')
def on_error(data):
    print("Erro: ", data['message'])

# Conecte ao servidor WebSocket
sio.connect('http://localhost:5002')

# Envie uma solicitação para processar uma imagem
sio.emit('process_image', {'image_path': 'main-project/assets/varios-barco18.tiff'})

# Mantenha o cliente ativo para aguardar as respostas
sio.wait()
