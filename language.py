import speech_recognition as sr
import pyttsx3
from googletrans import Translator
from faster_whisper import WhisperModel

# Load Whisper model (use "large-v2" for better accuracy)
model = WhisperModel("small", compute_type="int8")

# Initialize translator and TTS engine
translator = Translator()
tts = pyttsx3.init()

# Adjust speaking rate
tts.setProperty('rate', 150)

def recognize_and_respond():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 Speak something...")
        audio = r.listen(source)

        try:
            print("🔍 Recognizing using Whisper...")
            # Save audio to a file
            with open("temp.wav", "wb") as f:
                f.write(audio.get_wav_data())

            segments, info = model.transcribe("temp.wav", beam_size=5, language=None)
            text = "".join(segment.text for segment in segments)
            detected_lang = info.language

            print(f"🧠 You said ({detected_lang}): {text}")

            # Translate back to the same language just for demo
            translated = translator.translate(text, dest=detected_lang).text
            print(f"🗣 Responding in {detected_lang}: {translated}")

            tts.say(translated)
            tts.runAndWait()

        except Exception as e:
            print("❌ Error:", str(e))

if __name__ == "__main__":
    while True:
        recognize_and_respond()
