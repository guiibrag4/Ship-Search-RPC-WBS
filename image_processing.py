import cv2 as cv
import numpy as np

# Para carregar o arquivo xml já treinado
carregaAlgoritmo = cv.CascadeClassifier('main-project/haarcascades/first_cascade.xml')

def process_image(image_path):
    imagem = cv.imread(image_path)
    if imagem is None:
        raise ValueError("Erro ao carregar a imagem")

    # Divide a imagem em 4 partes
    altura, largura = imagem.shape[:2]
    sub_imagens = [
        imagem[:altura//2, :largura//2], 
        imagem[:altura//2, largura//2:],
        imagem[altura//2:, :largura//2], 
        imagem[altura//2:, largura//2:]
    ]

    sub_imagens_processadas = []
    for sub_imagem in sub_imagens:
        sub_imagem_cinza = cv.cvtColor(sub_imagem, cv.COLOR_BGR2GRAY)
        boats = carregaAlgoritmo.detectMultiScale(sub_imagem_cinza, scaleFactor=1.4, minNeighbors=14, minSize=(150, 150), maxSize=(250, 250))
        for (x, y, l, a) in boats:
            cv.rectangle(sub_imagem, (x, y), (x + l, y + a), (0, 255, 0), 5)
        sub_imagens_processadas.append(sub_imagem)

    imagem_processada = np.concatenate(
        (
            np.concatenate(sub_imagens_processadas[:2], axis=1),
            np.concatenate(sub_imagens_processadas[2:], axis=1)
        ), 
        axis=0
    )
    
    return imagem_processada
