import io
from flask import Flask, request, Response
from PIL import Image

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

@app.route("/resize", methods=["POST"])
def index():
    try:
        imageData = None
        payload=""
        if ('image' in request.files):
            print("From files")
            imageData = request.files['image']
            payload = request.form["size"]
            print (f'payload {payload} / image {imageData}')

        elif ('image' in request.form):
            print("From form")
            imageData = request.form['image']
            payload = request.form["size"]
            print (f'payload {payload} / image {imageData}')
        else:
            print("From get_data")
            imageData = io.BytesIO(request.get_data())

        image = Image.open(imageData)
        
        image = ResizeImage(image, size=int(payload))    
        
        # convert image to bytes
        image_bytes = ConvertImageToBytes(image)

        # send image bytes to the client
        return Response(image_bytes, mimetype="image/jpeg", status=200)
    except Exception as e:
        print('EXCEPTION:', str(e))
        return 'Error processing image', 500