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
os.environ['GOOGLE_APPLICATION_CREDENTIALS']  ="/home/sans/Desktop/TexttoSpeech/Google_API.json"

def detectEmotion(content):
    image = vision.Image(content=content)
    client = vision.ImageAnnotatorClient()
    response = client.face_detection(image=image)
    faces = response.face_annotations

    # Names of likelihood from google.cloud.vision.enums
    likelihood_name = ('UNKNOWN', 'VERY_UNLIKELY', 'UNLIKELY', 'POSSIBLE', 'LIKELY', 'VERY_LIKELY')

    detected_emotion = ""

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
            detected_emotion = very_likely
        elif likely != -1:
            detected_emotion = likely
        elif possible != -1:
            detected_emotion = possible
        else:
            detected_emotion = "Cannot determined"

        vertices = (['({},{})'.format(vertex.x, vertex.y)
                    for vertex in face.bounding_poly.vertices])

        print('face bounds: {}'.format(','.join(vertices)))

    if response.error.message:
        detected_emotion = (
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))
    return detected_emotion













    """
    print('anger: {}'.format(likelihood_name[face.anger_likelihood]))
    print('joy: {}'.format(likelihood_name[face.joy_likelihood]))
    print('surprise: {}'.format(likelihood_name[face.surprise_likelihood]))
    print('sorrow: {}'.format(likelihood_name[face.sorrow_likelihood]))
    print('blur: {}'.format(likelihood_name[face.blurred_likelihood]))
    print('headwear: {}'.format(likelihood_name[face.headwear_likelihood]))

    anger = '{}'.format(likelihood_name[face.anger_likelihood])
    joy = '{}'.format(likelihood_name[face.joy_likelihood])
    surprise = '{}'.format(likelihood_name[face.surprise_likelihood])
    sorrow = '{}'.format(likelihood_name[face.sorrow_likelihood])
    blur = '{}'.format(likelihood_name[face.blurred_likelihood])
    headwear = '{}'.format(likelihood_name[face.headwear_likelihood])

    list = [anger,joy,surprise,sorrow,blur,headwear]
    
    for value in list:
        if value == "VERY_LIKELY":
            print("The Person looks very sad", value)
"""