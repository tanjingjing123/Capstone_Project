from google.cloud import texttospeech
import os
import io

"""Synthesizes speech from the input file of text."""
os.environ['GOOGLE_APPLICATION_CREDENTIALS']  ="D:/Classes/Sem3/CApstone/Project_Stuff/Google_API.json"
client = texttospeech.TextToSpeechClient()

# Full path of the audio file, Replace with your file name
text_file = os.path.join(os.path.dirname(__file__),"sample2.txt")

with open(text_file, "r") as f:
    text = f.read()
    input_text = texttospeech.SynthesisInput(text=text)

# Note: the voice can also be specified by name.
# Names of voices can be retrieved with client.list_voices().
voice = texttospeech.VoiceSelectionParams(language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.FEMALE)

audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)

response = client.synthesize_speech(request={"input": input_text, "voice": voice, "audio_config": audio_config})

# The response's audio_content is binary.
with open("output.mp3", "wb") as out:
    out.write(response.audio_content)
    print('Audio content written to file "output.mp3"')