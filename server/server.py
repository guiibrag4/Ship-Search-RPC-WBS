from flask import Flask, request, render_template, jsonify
import cv2 as cv
import numpy as np
import time
import base64
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/detect', methods=['POST'])
def detect_boats():
    try:
        # Carregar o arquivo xml já treinado
        carregaAlgoritmo = cv.CascadeClassifier('haarcascades/first_cascade.xml')
        
        # Verificar se o arquivo XML foi carregado corretamente
        if carregaAlgoritmo.empty():
            return jsonify(error="Erro ao carregar o classificador"), 500

        # Pegando a imagem
        imagem = cv.imread('assets/varios-barco18.tiff')
        
        # Verificar se a imagem foi carregada corretamente
        if imagem is None:
            return jsonify(error="Erro ao carregar a imagem"), 400

        # Deixando a imagem cinza para maior eficiência do opencv
        imagem_cinza = cv.cvtColor(imagem, cv.COLOR_BGR2GRAY)
        
        # Processa a imagem
        num_boats = 0
        start_time = time.time()  # Inicia o contador de tempo
        boats = carregaAlgoritmo.detectMultiScale(imagem_cinza, scaleFactor=1.4, minNeighbors=14, minSize=(150, 150), maxSize=(250, 250))
        num_boats += len(boats)  # Incrementa o contador de navios
        for (x, y, l, a) in boats:
            cv.rectangle(imagem, (x, y), (x + l, y + a), (0, 255, 0), 5)
        end_time = time.time()  # Finaliza o contador de tempo

        # Calcula o tempo decorrido em segundos
        tempo_decorrido = end_time - start_time

        # Convertendo o tempo decorrido para hh:mm:ss:ms
        tempo_restante = time.strftime("%H:%M:%S:", time.gmtime(tempo_decorrido))
        milissegundos = int((tempo_decorrido - int(tempo_decorrido)) * 1000)
        tempo_restante += f"{milissegundos:03d}"

        # Redimensiona a imagem processada apenas para visualização ou salvamento
        largura_visualizacao = 1400
        altura_visualizacao = 720
        imagem_processada = cv.resize(imagem, (largura_visualizacao, altura_visualizacao))

        # Salvando a imagem em memória
        _, buffer = cv.imencode('.png', imagem_processada)
        img_bytes = buffer.tobytes()
        img_base64 = base64.b64encode(img_bytes).decode('utf-8')

        # Enviar resposta
        response = {
            "tempo_decorrido": tempo_restante,
            "num_boats": num_boats
        }

        return jsonify({"image": img_base64, "response": response})

    except Exception as e:
        return jsonify(error=str(e)), 500

if __name__ == '__main__':
    app.run(debug=True)
