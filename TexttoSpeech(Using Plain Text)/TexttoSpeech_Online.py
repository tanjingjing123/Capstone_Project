import gtts
from playsound import playsound


# make request to google to get synthesis
tts = gtts.gTTS("Hi ,Greetings for the day , i hope you will enjoy this tutorial Please let me know if you have any question or concern")

# save the audio file
tts.save("hello.mp3")

# play the audio file
playsound("hello.mp3")



































"""

tts = gtts.gTTS('sample2.txt', -file='sample2.txt')

# in telugu
tts = gtts.gTTS("పేరు", lang="te")
tts.save("telugu.mp3")
playsound("telugu.mp3")
"""