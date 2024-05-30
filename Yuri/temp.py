# https://github.com/GoogleCloudPlatform/python-docs-samples/blob/main/texttospeech/snippets/quickstart.py
import os
import google
from google.cloud import texttospeech
from playsound import playsound
import keys

def tts(message):
    client = texttospeech.TextToSpeechClient(client_options={"api_key": keys.GOOGLE_API_KEY})
    input = texttospeech.SynthesisInput(text=message)
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-GB", name="en-GB-Wavenet-A", ssml_gender=texttospeech.SsmlVoiceGender.FEMALE
    )
    audio = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )
    response = client.synthesize_speech(
        input=input, voice=voice, audio_config=audio
    )
    current_dir = os.getcwd()
    path = current_dir + '\output.mp3'
    with open(path, "wb+") as out:
        # Write the response to the output file.
        out.write(response.audio_content)
        #print('Audio content written to file "output.mp3"')
    out.close()
    playsound(path)
    os.remove(path)
    path = current_dir + '\output.txt'
    #os.remove(path)

tts("Text-to-Speech provides the following voices. The list includes Neural2, Studio, Standard, and WaveNet voices. Studio, Neural2 and WaveNet voices are higher quality voices with different pricing")