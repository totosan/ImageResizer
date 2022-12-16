import io
from flask import Flask, request, Response
from PIL import Image

app = Flask(__name__)

@app.route("/resize", methods=["POST"])
def index():
    # get image from request and resize it
    image = Image.open(request.files["image"])
    image.thumbnail((400,400))
    
    # convert image to bytes
    image_bytes = io.BytesIO()
    image.save(image_bytes, format='JPEG')
    image_bytes = image_bytes.getvalue()

    # send image bytes to the client
    return Response(image_bytes, mimetype="image/jpeg")
