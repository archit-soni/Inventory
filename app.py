from flask import Flask
import os


app = Flask(__name__)


@app.route("/")
def index():
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'C:\\Users\\archi\\Documents\\GitHub\\inventory\\Inventory\\Inventory-43cc8f010091.json'
    scrapURL("https://www.allrecipes.com/recipe/17481/simple-white-cake/")
    textFromPath(
        "C:\\Users\\archi\\Documents\\GitHub\\inventory\\Inventory\\Untitled.png")
    textFromURI("https://i.imgur.com/pCkrQky.png")
    textFromURI(
        "http://sunnymoney.weebly.com/uploads/1/9/6/4/19645963/veggie-grocery-receipt_orig.jpeg")
    return "Hello"


def scrapURL(url):
    import requests
    from bs4 import BeautifulSoup
    ings = {}
    ings["Ingredients"] = []
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    for s in soup.findAll('span', {'class': 'ingredients-item-name'}):
        ings["Ingredients"].append(s.contents[0])
    print(ings)
    return ings


def textFromURI(uri):
    """Detects text in the file located in Google Cloud Storage or on the Web.
    """
    from google.cloud import vision
    client = vision.ImageAnnotatorClient()
    image = vision.Image()
    image.source.image_uri = uri

    response = client.text_detection(image=image)
    texts = response.text_annotations
    print('Texts:')

    for text in texts:
        print('\n"{}"'.format(text.description))

        vertices = (['({},{})'.format(vertex.x, vertex.y)
                     for vertex in text.bounding_poly.vertices])

        print('bounds: {}'.format(','.join(vertices)))

    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))
    print(texts)
    return texts


def textFromPath(path):
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
    print(texts)
    return texts
