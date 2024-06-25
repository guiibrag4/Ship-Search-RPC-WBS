from flask import Flask, request, render_template
from flask_socketio import SocketIO, send, emit

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

@app.route('/resultado', methods=['POST'])
def receber_resultado():
    dados = request.json
    print(f'Resultado final recebido: {dados}')
    socketio.emit('resultado', dados)
    return '', 200

def enviar_atualizacao_progresso(progresso):
    socketio.emit('progresso', {'progresso': progresso})

def enviar_resultado_final(resultado):
    socketio.emit('resultado', {'resultado': resultado})

if __name__ == '__main__':
    socketio.run(app, debug=True, port=5001)
