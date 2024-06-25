from flask import Flask, request, render_template, jsonify
import cv2 as cv
import numpy as np
import time
import base64
import os
import threading

app = Flask(__name__)
resultados_global = []

@app.route('/')
def index():
    return render_template('index.html', resultados=resultados_global)

def processar_segmento_imagem(segmento, resultados, idx):
    try:
        classificador = cv.CascadeClassifier('haarcascades/first_cascade.xml')
        if classificador.empty():
            resultados[idx] = f"Erro ao carregar o classificador para o segmento {idx}"
            return
        imagem_cinza = cv.cvtColor(segmento, cv.COLOR_BGR2GRAY)
        barcos = classificador.detectMultiScale(imagem_cinza, scaleFactor=1.4, minNeighbors=14, minSize=(150, 150), maxSize=(250, 250))
        for (x, y, l, a) in barcos:
            cv.rectangle(segmento, (x, y), (x + l, y + a), (0, 255, 0), 5)
        resultados[idx] = f"Segmento processado {idx} com {len(barcos)} barcos detectados"
    except Exception as e:
        resultados[idx] = f"Erro ao processar o segmento {idx}: {str(e)}"

def dividir_e_processar_imagem(imagem):
    altura, largura = imagem.shape[:2]
    segmentos = [(0, 0, largura // 2, altura // 2), (largura // 2, 0, largura, altura // 2),
                 (0, altura // 2, largura // 2, altura), (largura // 2, altura // 2, largura, altura)]

    threads = []
    resultados = [None] * len(segmentos)

    for idx, (x1, y1, x2, y2) in enumerate(segmentos):
        segmento = imagem[y1:y2, x1:x2]
        thread = threading.Thread(target=processar_segmento_imagem, args=(segmento, resultados, idx))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    return resultados, imagem

@app.route('/detectar', methods=['POST'])
def detectar_barcos():
    try:
        if 'file' not in request.files:
            return jsonify(error="Nenhum arquivo enviado"), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify(error="Nenhum arquivo selecionado"), 400

        # Salva o arquivo temporariamente
        file_path = os.path.join('uploads', file.filename)
        file.save(file_path)

        # Processa a imagem
        imagem = cv.imread(file_path)
        resultados, imagem_processada = dividir_e_processar_imagem(imagem)

        global resultados_global
        resultados_global = resultados

        # Redimensiona a imagem para largura de 350 pixels
        altura, largura = imagem_processada.shape[:2]
        nova_largura = 350
        nova_altura = int(altura * (nova_largura / largura))
        imagem_redimensionada = cv.resize(imagem_processada, (nova_largura, nova_altura))

        # Codifica a imagem processada em base64
        _, buffer = cv.imencode('.png', imagem_redimensionada)
        img_bytes = buffer.tobytes()
        img_base64 = base64.b64encode(img_bytes).decode('utf-8')

        # Calcula o tempo decorrido como uma soma fictícia dos resultados
        tempo_decorrido = sum([result.count('detectados') for result in resultados])

        response = {
            "tempo_decorrido": tempo_decorrido,
            "num_boats": len(resultados)
        }

        return jsonify({"image": img_base64, "response": response})

    except Exception as e:
        return jsonify(error=str(e)), 500

if __name__ == '__main__':
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
    app.run(debug=True, port=5000)
