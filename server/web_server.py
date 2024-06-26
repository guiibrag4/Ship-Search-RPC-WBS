from flask import Flask, render_template, request, jsonify
import requests
import base64

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    try:
        file = request.files['file']
        image = file.read()

        # Codificar a imagem para base64
        image_base64 = base64.b64encode(image).decode('utf-8')

        # Enviar a imagem para o servidor RPC
        response = requests.post('http://127.0.0.1:5002/process_image', json={'image': image_base64})
        response_data = response.json()

        if 'error' in response_data:
            return jsonify({'error': response_data['error']}), 500

        processed_image_base64 = response_data['image']
        return jsonify({'image': processed_image_base64})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
