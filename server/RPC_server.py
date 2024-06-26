from flask import Flask, request, render_template, jsonify
import cv2 as cv
import numpy as np
import base64
import os
import re
import threading
import logging
import time

# Configuração do logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

app = Flask(__name__)
resultados_global = []

@app.route('/')
def index():
    return render_template('index.html', resultados=resultados_global)

def processar_segmento_imagem(segmento, resultados, idx):
    try:
        logger.info(f"Processando segmento {idx}")
        classificador_path = os.path.join('haarcascades', 'first_cascade.xml')
        if not os.path.exists(classificador_path):
            resultados[idx] = f"Erro: arquivo de classificador {classificador_path} não encontrado"
            logger.error(resultados[idx])
            return
        
        classificador = cv.CascadeClassifier(classificador_path)
        if classificador.empty():
            resultados[idx] = f"Erro ao carregar o classificador para o segmento {idx}"
            logger.error(resultados[idx])
            return

        imagem_cinza = cv.cvtColor(segmento, cv.COLOR_BGR2GRAY)
        
        # Verifica as dimensões da imagem
        altura, largura = segmento.shape[:2]
        if largura >= 5000 or altura >= 3000:
            scaleFactor = 1.4
            minNeighbors = 14
            minSize = (150, 150)
            maxSize = (250, 250)
        elif largura >= 3000 or altura >= 1000:
            # Defina aqui os parâmetros para imagens menores que 5000x3000
            scaleFactor = 1.2
            minNeighbors = 4
            minSize = (150, 150)
            maxSize = (250, 250)
        else:
            scaleFactor = 1.1
            minNeighbors = 2
            minSize = (30, 30)
            maxSize = (1000, 1000)

        barcos = classificador.detectMultiScale(imagem_cinza, scaleFactor=scaleFactor, minNeighbors=minNeighbors, minSize=minSize, maxSize=maxSize)
        for (x, y, l, a) in barcos:
            cv.rectangle(segmento, (x, y), (x + l, y + a), (0, 255, 0), 5)
        resultados[idx] = f"Segmento processado {idx} com {len(barcos)} barcos detectados"
        logger.info(resultados[idx])
    except Exception as e:
        resultados[idx] = f"Erro ao processar o segmento {idx}: {str(e)}"
        logger.error(resultados[idx])

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
            error_message = "Nenhum arquivo enviado"
            logger.error(error_message)
            return jsonify(error=error_message), 400

        file = request.files['file']
        if file.filename == '':
            error_message = "Nenhum arquivo selecionado"
            logger.error(error_message)
            return jsonify(error=error_message), 400

        # Salva o arquivo temporariamente
        file_path = os.path.join('uploads', file.filename)
        file.save(file_path)
        logger.info(f"Arquivo {file.filename} salvo em {file_path}")

        # Início da medição do tempo
        start_time = time.time()

        # Processa a imagem
        imagem = cv.imread(file_path)
        resultados, imagem_processada = dividir_e_processar_imagem(imagem)

        # Fim da medição do tempo
        end_time = time.time()
        elapsed_time = end_time - start_time
        formatted_time = time.strftime('%M:%S', time.gmtime(elapsed_time)) + f":{int((elapsed_time * 1000) % 1000):03d}"

        global resultados_global
        resultados_global = resultados

        # Salva a imagem processada
        imagem_processada_path = os.path.join('client', 'imagem_processada.png')
        cv.imwrite(imagem_processada_path, imagem_processada)
        logger.info(f"Imagem processada salva em {imagem_processada_path}")

        # Codifica a imagem processada em base64
        _, buffer = cv.imencode('.png', imagem_processada)
        img_bytes = buffer.tobytes()
        img_base64 = base64.b64encode(img_bytes).decode('utf-8')

        logger.info("Imagem processada e codificada para base64")

        # Correção: Usando expressão regular para extrair o número de barcos de forma segura
        total_boats = sum([int(re.search(r'(\d+) barcos detectados', result).group(1)) for result in resultados if 'barcos detectados' in result])

        response = {
            "tempo_decorrido": formatted_time,
            "num_boats": total_boats
        }

        return jsonify({"image": img_base64, "response": response})

    except Exception as e:
        logger.error(f"Erro no processamento: {str(e)}")
        return jsonify(error=str(e)), 500

if __name__ == '__main__':
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
    if not os.path.exists('client'):
        os.makedirs('client')
    app.run(debug=True, port=5000)
