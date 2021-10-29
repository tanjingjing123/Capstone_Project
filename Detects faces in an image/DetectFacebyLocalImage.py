#"""Detects faces in an image."""
from google.cloud import vision
import os
import io

def findInMap(visions, prob):
    try:
        return list(visions.keys())[list(visions.values()).index(prob)]
    except ValueError:
        return -1

# Creates google client
os.environ['GOOGLE_APPLICATION_CREDENTIALS']  ="D:/Classes/Sem3/CApstone/Project_Stuff/Google_API.json"
client = vision.ImageAnnotatorClient()

path = r"D:\Classes\Sem3\CApstone\Project_Stuff\Images\facial_emotions.png"

with io.open(path, 'rb') as image_file:
    content = image_file.read()

image = vision.Image(content=content)

response = client.face_detection(image=image)
faces = response.face_annotations

# Names of likelihood from google.cloud.vision.enums
likelihood_name = ('UNKNOWN', 'VERY_UNLIKELY', 'UNLIKELY', 'POSSIBLE',
                       'LIKELY', 'VERY_LIKELY')
print('Faces:')

for face in faces:
    visions = {"anger":likelihood_name[face.anger_likelihood], 
    "Happy":likelihood_name[face.joy_likelihood],
    "surprise":likelihood_name[face.surprise_likelihood],
    "sorrow":likelihood_name[face.sorrow_likelihood],
    "blur":likelihood_name[face.blurred_likelihood],
    "headwear":likelihood_name[face.headwear_likelihood]}

    very_likely = findInMap(visions, "VERY_LIKELY")
    likely = findInMap(visions, "LIKELY")
    possible = findInMap(visions, "POSSIBLE")

    if very_likely != -1:
        print("The Person looks", very_likely)
    elif likely != -1:
        print("The Person looks partially", likely)
    elif possible != -1:
        print("The Person looks may be", possible)
    else:
        print("The Person expression can not be determined")

    vertices = (['({},{})'.format(vertex.x, vertex.y)
                for vertex in face.bounding_poly.vertices])

    print('face bounds: {}'.format(','.join(vertices)))

if response.error.message:
    raise Exception(
        '{}\nFor more info on error messages, check: '
        'https://cloud.google.com/apis/design/errors'.format(
            response.error.message))












