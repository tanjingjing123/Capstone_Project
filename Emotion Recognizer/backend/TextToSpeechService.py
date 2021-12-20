from google.cloud import texttospeech
import os

def text_to_speech_service(path):
    """Synthesizes speech from the input file of text."""
    os.environ['GOOGLE_APPLICATION_CREDENTIALS']  ="./capstone.json"
    client = texttospeech.TextToSpeechClient()

    with open(path, "r") as f:
        text = f.read()
        input_text = texttospeech.types.SynthesisInput(text=text)

    voice = texttospeech.types.VoiceSelectionParams(language_code="en-US", ssml_gender=texttospeech.enums.SsmlVoiceGender.FEMALE)

    audio_config = texttospeech.types.AudioConfig(audio_encoding=texttospeech.enums.AudioEncoding.MP3)

    response = client.synthesize_speech(input_=input_text, voice=voice, audio_config=audio_config)

    with open("output.mp3", "wb") as out:
        out.write(response.audio_content)
        print('Audio content written to file "output.mp3')
