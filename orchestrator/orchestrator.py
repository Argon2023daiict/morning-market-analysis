from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import pyttsx3
import os
import tempfile
import base64
import re


app = FastAPI()


app.mount("/frontend", StaticFiles(directory="frontend"), name="frontend")

@app.get("/")
def home():
    return FileResponse("frontend/index.html")


try:
    from agents.voice_agent import convert_audio_to_text, speak_text
    from agents.language_agent import generate_narrative
    from agents.retriever_agent import initialize_retriever
    HAVE_AGENTS = True
except ImportError:
    HAVE_AGENTS = False

if not HAVE_AGENTS:
    print(" Agents not found. Using stub functions.")

    def convert_audio_to_text(filepath: str) -> str:
        print(f"Converting audio at {filepath} to text... [STUB]")
        return "Hello world"

    def initialize_retriever():
        return None

    def generate_narrative(text: str, retriever) -> str:
        print(f"Generating narrative for text: {text} [STUB]")
        return f"This is a summary for: {text}"
def clean_text_for_speech(text: str) -> str:
    
    
    
    cleaned = re.sub(r"[^a-zA-Z0-9\s,.!?'-]", '', text)
    
    
    cleaned = re.sub(r'\s+', ' ', cleaned).strip()
    
    return cleaned

def synthesize_speech(text: str) -> bytes:
    try:
        speaker = pyttsx3.init()
        speaker.setProperty('rate', 150)
        speaker.setProperty('volume', 1.0)

        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tf:
            temp_path = tf.name

        speaker.save_to_file(text, temp_path)
        speaker.runAndWait()

        with open(temp_path, "rb") as f:
            audio_bytes = f.read()

        os.remove(temp_path)
        return audio_bytes
    except Exception as e:
        print("TTS Error:", e)
        return b""

@app.post("/respond/")
async def handle_voice(file: UploadFile = File(...)):
    try:
        suffix = os.path.splitext(file.filename)[-1] if file.filename else ".wav"
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tf:
            temp_audio_path = tf.name
            content = await file.read()
            tf.write(content)

        print(f" Saved audio to {temp_audio_path}")

        text = convert_audio_to_text(temp_audio_path)
        print(f" Transcribed Text: {text}")

        retriever = initialize_retriever()
        summary = generate_narrative(text, retriever)
        print(f" Final Summary: {summary}")

        
        cleaned_summary = clean_text_for_speech(summary)
        print(f" Cleaned Summary for TTS: {cleaned_summary}")

        audio_bytes = synthesize_speech(cleaned_summary)

        os.remove(temp_audio_path)

        audio_b64 = base64.b64encode(audio_bytes).decode("utf-8")

        return {"answer": summary, "audio_b64": audio_b64}

    except Exception as e:
        print(" Error in /respond/:", str(e))
        return JSONResponse(status_code=500, content={"error": str(e)})
