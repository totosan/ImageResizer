import io
from flask import Flask, request, Response
from PIL import Image
import base64
from werkzeug.datastructures import FileStorage

# logging
import logging
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

def ResizeImage(image, size=400):
    sizeConverted=(size,size)
    image.thumbnail(sizeConverted, Image.ANTIALIAS)
    return image

def ConvertImageToBytes(image):
    image_bytes = io.BytesIO()
    image.save(image_bytes, format='JPEG')
    image_bytes = image_bytes.getvalue()
    return image_bytes

@app.route("/", methods=["POST","GET"])
def index():
    try:
        if (request.method == "GET"):
            return "Image Resizer", 200
        
        payload=""
        if ('image' in request.files):
            logging.info("From files")
            imageData = request.files['image']
            payload = request.form["size"]
            logging.info(f'payload {payload} / image {imageData}')

        elif ('image' in request.form):
            logging.info("From form")
            imageData = request.form['image']
            payload = request.form["size"]
            logging.info (f'payload {payload} / image {imageData}')

        if isinstance(imageData, FileStorage):
            image_data = base64.b64decode(imageData.read())
            logging.debug(f'image_data {image_data}')
        else:
            image_data = base64.b64decode(imageData)

        # Create file object from image data
        file = io.BytesIO(image_data)

        # Reset file pointer to start of file
        file.seek(0)
        image = Image.open(file)
        
        image = ResizeImage(image, size=int(payload))    
        
        # convert image to bytes
        image_bytes = ConvertImageToBytes(image)

        # send image bytes to the client
        return Response(image_bytes, mimetype="image/jpeg", status=200)
    except Exception as e:
        logging.exception(e)
        return 'Error processing image', 500