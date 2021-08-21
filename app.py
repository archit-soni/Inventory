from flask import Flask
import os

app = Flask(__name__)


@app.route("/")
def index():
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'C:\\Users\\archi\\Documents\\GitHub\\inventory\\Inventory\\Inventory-43cc8f010091.json'
    path = "C:\\Users\\archi\\Documents\\GitHub\\inventory\\Inventory\\Untitled.png"
    from google.cloud import vision
    import io
    textInImage = ""
    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations
    print('Texts:')

    for text in texts:
        textInImage = textInImage+'\n"{}"'.format(text.description)
        print('\n"{}"'.format(text.description))

        vertices = (['({},{})'.format(vertex.x, vertex.y)
                     for vertex in text.bounding_poly.vertices])

        print('bounds: {}'.format(','.join(vertices)))

    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))
    return textInImage
