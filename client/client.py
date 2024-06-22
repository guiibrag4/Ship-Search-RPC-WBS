import requests
import base64

def detect_boats():
    url = "http://localhost:5000/detect"
    response = requests.post(url)
    if response.status_code == 200:
        result = response.json()
        tempo_decorrido = result['response']['tempo_decorrido']
        num_boats = result['response']['num_boats']
        print(f"Tempo decorrido: {tempo_decorrido} segundos")
        print(f"Número de navios detectados: {num_boats}")
        img_base64 = result['image']
        img_bytes = base64.b64decode(img_base64)
        with open("Imagem_Detectada.png", "wb") as img_file:
            img_file.write(img_bytes)
    else:
        error_message = response.json().get('error', 'Sem mensagem de erro')
        print(f"Erro: {response.status_code}, Mensagem: {error_message}")

if __name__ == "__main__":
    detect_boats()
