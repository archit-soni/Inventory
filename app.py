<<<<<<< HEAD
from flask import Flask, send_file, request, jsonify, make_response, redirect, url_for
from firebase_admin import credentials, firestore, initialize_app
=======
from flask import Flask, send_file, jsonify
>>>>>>> 7ff0ea6ef115c5f9a2e7d58eb1600fb989ed90ae
from dotenv import load_dotenv          # Ask Jason for the dotenv file details!
import os
import requests
import shutil                           # Used to save the photos locally
from google.cloud import vision

load_dotenv()

app = Flask(__name__)

# Initialize Firestore DB
cred = credentials.Certificate("./key.json")
default_app = initialize_app(cred)
db = firestore.client()
ingredients_db = db.collection("ingredients")

# Configuration for spoonacular API
API_KEY = os.getenv("API_KEY")
SPOON_BASEURL = os.getenv("SPOON_BASEURL")
SPOON_IMGURL = os.getenv("SPOON_IMGURL")
IMAGE_SIZE = "250x250"


@app.route("/")
def index():
    # os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'C:\\Users\\archi\\Documents\\GitHub\\inventory\\Inventory\\Inventory-43cc8f010091.json'
    # scrapURL("https://www.allrecipes.com/recipe/17481/simple-white-cake/")
    # textFromPath(
    #     "C:\\Users\\archi\\Documents\\GitHub\\inventory\\Inventory\\Untitled.png")
    # textFromURI("https://i.imgur.com/pCkrQky.png")
    # textFromURI(
    #     "http://sunnymoney.weebly.com/uploads/1/9/6/4/19645963/veggie-grocery-receipt_orig.jpeg")
    return "Hello"

@app.route("/api/ingredient_image")
def get_ingredient():
    '''Query Spoonacular API using requests and Display an Image of the Ingredient'''
    ingredient_name = request.args.get("food")
    # Parameters we want to provide in our ingredient search
    payload = {
        "query": ingredient_name,
        "number": 1,
        "apiKey": API_KEY,
    }
    try: 
        INGREDIENT_URL = f"{SPOON_BASEURL}/food/ingredients/search"
        response = requests.get(INGREDIENT_URL, params=payload).json()

    except requests.exceptions.HTTPError as errh:
        print(errh)
        return f"There was an error querying Spoonacular's API for {ingredient_name}!" 
    
    # Create a URL that represents the ingredient image 
    image_route = get_image_url(response['results'][0]['image'])
    try:
        '''Heads to the route of the ingredient and saves it locally'''
        img_response = requests.get(image_route, stream = True)
        if img_response.status_code == 200:
            img_response.raw.decode_content = True

            # Make sure you have a photos directory or this will crash!
            filename = f"./photos/{ingredient_name}.jpg"
            with open(filename, "wb") as f:
                '''Saves the image to your local directory'''
                shutil.copyfileobj(img_response.raw, f)

    except requests.exceptions.HTTPError as errh:
        print(errh)
        return f"There was an error trying to get the image for a {ingredient_name}"

    return send_file(filename, mimetype="image")
    

@app.route("/api/ingredients", methods=["GET", "POST"])
def get_add_ingredients():
    if request.method == "POST":
        ingredient_name = request.form.get("ingredient_name")
        if not ingredient_name:
            return make_response(jsonify({"message": "That ingredient name is invalid."}), 400)
        new_ingredient = {
            "name": ingredient_name,
            "img_url": get_image_url(ingredient_name),
            "amount": 1
        }
        ingredients_db.add(new_ingredient)
        print(f"Successfully added {ingredient_name} to FireStore.")
        return redirect("/api/ingredients")
    # Default to GET Request since we know POST was used
    else:
        try:
            all_ingredients = []
            ingredient_iterator = ingredients_db.stream()
            for ingredient in ingredient_iterator:
                all_ingredients.append(ingredient.to_dict())
            return make_response(jsonify({"message": f"Successfully Grabbed all ingredients from FireStore.", "ingredients": f"{all_ingredients}"}), 200)

        except Exception as e:
            return f"An error occurred: {e}"

# @app.route("/api/ingredients/<ingredient>", methods=["PATCH"])
# def update_ingredients(ingredient):
#     '''Updates the ingredient'''
#     req = request.get_json()
#     print(req)
#     current_ingredient = ingredients_db.where(u'name', u'==', ingredient['name']).stream()

#     print(current_ingredient)

#     return redirect("/api/ingredients")

@app.route("/uri/")
def textFromURI():
    uri = request.args.get('uri')
    """Detects text in the file located in Google Cloud Storage or on the Web.
    """
    client = vision.ImageAnnotatorClient()
    image = vision.Image()
    image.source.image_uri = uri
    response = client.text_detection(image=image)
    texts = response.text_annotations
    data = {}
    data["ings"] = []
    data["filter"] = []
    print('Texts:')
    for text in texts:
        print('\n"{}"'.format(text.description))
        data["ings"].append(text.description)

        vertices = (['({},{})'.format(vertex.x, vertex.y)
                    for vertex in text.bounding_poly.vertices])

        print('bounds: {}'.format(','.join(vertices)))

    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))
    print()
    splt = data['ings'][0].split('\n')
    for ing in splt:
        if '$' not in ing:
            if len(ing)>5:
                if '.' not in ing:
                    data['filter'].append(ing)
    print(data['filter'])
    return jsonify(data)
<<<<<<< HEAD

def get_image_url(ingredient_name):
    return f"{SPOON_IMGURL}{IMAGE_SIZE}/{ingredient_name}"
=======
>>>>>>> 7ff0ea6ef115c5f9a2e7d58eb1600fb989ed90ae

# def scrapURL(url):
#     import requests
#     from bs4 import BeautifulSoup
#     ings = {}
#     ings["Ingredients"] = []
#     page = requests.get(url)
#     soup = BeautifulSoup(page.content, 'html.parser')
#     for s in soup.findAll('span', {'class': 'ingredients-item-name'}):
#         ings["Ingredients"].append(s.contents[0])
#     print(ings)
#     return ings


# def textFromURI(uri):
#     """Detects text in the file located in Google Cloud Storage or on the Web.
#     """
#     from google.cloud import vision
#     client = vision.ImageAnnotatorClient()
#     image = vision.Image()
#     image.source.image_uri = uri

#     response = client.text_detection(image=image)
#     texts = response.text_annotations
#     print('Texts:')

#     for text in texts:
#         print('\n"{}"'.format(text.description))

#         vertices = (['({},{})'.format(vertex.x, vertex.y)
#                      for vertex in text.bounding_poly.vertices])

#         print('bounds: {}'.format(','.join(vertices)))

#     if response.error.message:
#         raise Exception(
#             '{}\nFor more info on error messages, check: '
#             'https://cloud.google.com/apis/design/errors'.format(
#                 response.error.message))
#     print(texts)
#     return texts


# def textFromPath(path):
#     from google.cloud import vision
#     import io
#     textInImage = ""
#     client = vision.ImageAnnotatorClient()

#     with io.open(path, 'rb') as image_file:
#         content = image_file.read()

#     image = vision.Image(content=content)

#     response = client.text_detection(image=image)
#     texts = response.text_annotations
#     print('Texts:')

#     for text in texts:
#         textInImage = textInImage+'\n"{}"'.format(text.description)
#         print('\n"{}"'.format(text.description))

#         vertices = (['({},{})'.format(vertex.x, vertex.y)
#                      for vertex in text.bounding_poly.vertices])

#         print('bounds: {}'.format(','.join(vertices)))

#     if response.error.message:
#         raise Exception(
#             '{}\nFor more info on error messages, check: '
#             'https://cloud.google.com/apis/design/errors'.format(
#                 response.error.message))
#     print(texts)
#     return texts
