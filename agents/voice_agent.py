import whisper
import pyttsx3
import os



os.environ["XDG_CACHE_HOME"] = "/tmp"

whisper_model = whisper.load_model("base")

def convert_audio_to_text(file_path):
    result = whisper_model.transcribe(file_path)
    return result['text']

def speak_text(text):
    speaker = pyttsx3.init()
    speaker.say(text)
    speaker.runAndWait()
