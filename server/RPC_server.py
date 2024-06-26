import eventlet
eventlet.monkey_patch()

from flask import Flask, request, jsonify
import cv2 as cv
import numpy as np
import base64
import os
import threading

app = Flask(__name__)
resultados_global = []

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
        imagem_data = base64.b64decode(request.json['imagem'])
        np_img = np.frombuffer(imagem_data, np.uint8)
        imagem = cv.imdecode(np_img, cv.IMREAD_COLOR)

        resultados, imagem_processada = dividir_e_processar_imagem(imagem)

        global resultados_global
        resultados_global = resultados

        # Codifica a imagem processada em base64
        _, buffer = cv.imencode('.png', imagem_processada)
        img_bytes = buffer.tobytes()
        img_base64 = base64.b64encode(img_bytes).decode('utf-8')

        response = {
            "resultados": resultados,
            "imagem_processada": img_base64
        }

        return jsonify(response)

    except Exception as e:
        return jsonify(error=str(e)), 500

if __name__ == '__main__':
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
    app.run(debug=True, port=5002)
