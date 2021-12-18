#import flask
import os, json
import base64
import flask
from flask import Flask, request, Response, send_file
from translate import Translator
from flask_cors import CORS, cross_origin
from werkzeug.utils import secure_filename
import music_recommendation_lib

import SpeechToTextService as stts
import TextToSpeechService as ttss

app = Flask(__name__)
CORS(app)

ch_to_en_translator = Translator(to_lang='en', from_lang='zh')
en_to_ch_translator = Translator(to_lang='zh', from_lang='en')


# API to translate text from: 1) English to Chinese 2) Chinese to English
@app.route('/translate_text')
def translate_ch():
    args = request.args
    print(args)  # For debugging
    word = args['word']
    language = args['language']

    if language == 'chinese':
        return en_to_ch_translator.translate(word)
    else:
        return ch_to_en_translator.translate(word)


# API to translate Speech to Text
@app.route("/Speech_to_text", methods=['GET', 'POST'])
def translate_speech_to_text():
    file = request.files["inputFile"]
    print(file)
    output_text = stts.get_large_audio_transcription(file)
    return output_text


# API to translate Text to Speech
@app.route("/Text_to_speech", methods=['GET', 'POST'])
@cross_origin()
def translate_text_to_speech():
    file = request.files["inputFile"]
    filename = secure_filename(file.filename)
    # filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    filepath = os.path.join("/home/sans/Downloads/Capstone-Project-main (1)/Emotion Recognizer/backend/UPLOADS", filename)
    file.save(filepath)
    print(filename, "-", filepath)
    ttss.text_to_speech_service(filepath)

    return flask.send_file('/home/sans/Downloads/Capstone-Project-main (1)/Emotion Recognizer/backend/output.mp3',
                               as_attachment=True, mimetype="audio/mp3")



@app.route("/Image_To_Emotion", methods=['GET', 'POST'])
@cross_origin()
def captureimage():
    if request.method == "POST":
        content = request.form['base64Image']	# should be base64 image = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAZAAAAFeCAYAAACrXUkIAAAAAXNSR0IArs4c6QAAIABJREFUe.......UmHWs/yaf0fFm2et73m9BcAAAAASUVORK5CYII="
        base64DecodedString = base64.b64decode(str(content.replace("data:image/png;base64,","")))

        saveToImage(base64DecodedString)

        from Google_Image_To_Emotions import detectEmotion
        detectedEmotion = detectEmotion(base64DecodedString)


        # Enable this block to send response in json format
        response = app.response_class(
                response=json.dumps({"emotion": detectedEmotion, "base64StringResend":content}),
                status=200,
                mimetype='application/json'
        )
        return response
    """	
        return render_template("captureImage.html", emotion = detectedEmotion, base64StringResend=content)
    else:
        return render_template("captureImage.html")
    """

def saveToImage(base64DecodedString):
    # print(base64DecodedString)
    with open("UPLOADS/imageToSave.png", "wb") as fh:
        fh.write(base64DecodedString)

@app.route('/get_music_rec', methods=['GET', 'POST'])
def get_music_rec():
    args = request.args
    keyword = args['keyword']

    return json.dumps(music_recommendation_lib.GetRecommendation(keyword))
