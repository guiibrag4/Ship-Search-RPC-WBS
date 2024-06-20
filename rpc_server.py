from flask import Flask, request, jsonify
from jsonrpcserver import method, dispatch
import cv2 as cv
from image_processing import process_image

app = Flask(__name__)

@method
def process_image_rpc(image_path: str):
    try:
        processed_image = process_image(image_path)
        _, img_encoded = cv.imencode('.png', processed_image)
        return img_encoded.tobytes().decode('latin1')  # Converta para uma string usando latin1
    except Exception as e:
        return str(e)

@app.route('/rpc', methods=['POST'])
def rpc():
    response = dispatch(request.get_data().decode())
    return jsonify(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)