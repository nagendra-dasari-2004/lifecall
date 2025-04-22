import subprocess
import datetime
import webbrowser
import os
import time
import requests
import json
import getpass

# Windows-specific imports with fallbacks
try:
    import pyttsx3
    import winshell
    import pyjokes
    import ctypes
    import wmi
    WINDOWS = True
except ImportError:
    WINDOWS = False
    print("Warning: Running in limited mode - some Windows-specific features disabled")

try:
    import wikipedia
except ImportError:
    wikipedia = None
from pathlib import Path
from bs4 import BeautifulSoup
import speech_recognition as sr
from urllib.request import urlopen
import wolframalpha
import pyautogui
import csv
import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from pywinauto import application
import geocoder
import random
from ambulance_service import book_ambulance, notify_nearby_hospitals, open_tracking_interface
from location_service import get_precise_location as get_current_location

# Initialize text-to-speech engine
# Initialize text-to-speech engine properly
engine = None
recognizer = None
if WINDOWS:
    try:
        engine = pyttsx3.init('sapi5')
        # Test voice immediately
        engine.say('Voice system initialized')
        engine.runAndWait()
        
        recognizer = sr.Recognizer()
        voices = engine.getProperty('voices')
        # Print available voices for debugging
        print("Available voices:")
        for voice in voices:
            print(f"- {voice.name} ({voice.id})")
        
        # Try different voice indices if needed
        engine.setProperty('voice', voices[1].id)  # Try 0 if 1 doesn't work
        engine.setProperty('rate', 150)  # Adjust speech rate
        
    except Exception as e:
        print(f"Speech initialization error: {e}")
        WINDOWS = False

def speak(audio):
    try:
        if engine:
            print(f"Speaking: {audio}")  # Debug output
            engine.say(audio)
            engine.runAndWait()
            time.sleep(0.5)  # Small pause after speaking
        else:
            print(f"[TTS Disabled] {audio}")
    except Exception as e:
        print(f"Speech error: {e}")
        # Fallback to system TTS
        os.system(f'powershell -Command "Add-Type -AssemblyName System.Speech; (New-Object System.Speech.Synthesis.SpeechSynthesizer).Speak(\'{audio}\');"')


def takeCommand():
    r = sr.Recognizer()
    r.energy_threshold = 4000  # Adjust based on your environment
    r.dynamic_energy_threshold = True
    
    with sr.Microphone() as source:
        print("Calibrating microphone...")
        r.adjust_for_ambient_noise(source, duration=1)
        print("Listening...")
        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=8)
            print("Recognizing...")
            query = r.recognize_google(audio, language='en-in')
            print(f"User said: {query}")
            return query.lower()
        except sr.WaitTimeoutError:
            print("No speech detected")
            return "None"
        except sr.UnknownValueError:
            print("Could not understand audio")
            return "None"
        except Exception as e:
            print(f"Error: {e}")
            return "None"

def handleEmergency():
    speak("Emergency detected! Please stay calm.")
    
    # Get location with timeout
    try:
        loc, address = get_current_location()
        if not loc:
            raise ValueError("No location")
            
        speak(f"Detected you near {address.split(',')[0]}")
        
        # Book ambulance
        booking = book_ambulance(*loc)
        if booking['success']:
            speak(f"Ambulance {booking['ambulance_id']} is coming in {booking['eta']} minutes")
            speak(f"Driver {booking['driver_name']} will contact you")
            
            # Show nearby hospitals
            hospitals = notify_nearby_hospitals(*loc)
            speak(f"Nearest is {hospitals[0]['name']} at {hospitals[0]['contact']}")
            
            # Open map
            open_tracking_interface(booking['tracking_url'])
        else:
            speak("Please call 108 or your local emergency number now!")
            
    except Exception as e:
        print(f"Emergency error: {e}")
        speak("Emergency services couldn't be contacted. Please call 108 manually!")

def open_website(url):
    webbrowser.open(url)
    speak(f"Opening {url}")

def main():
    print("Starting in debug mode...")
    while True:
        print("\nWaiting for command...")
        query = takeCommand().lower()
        print(f"Command received: {query}")
        
        if query == "none":
            continue
            
        if 'emergency' in query or 'ambulance' in query:
            handleEmergency()
        elif 'test' in query:
            speak("Microphone test successful!")
        elif 'exit' in query:
            speak("Goodbye!")
            break
        else:
            speak("I didn't understand that command")

if __name__ == "__main__":
    main()
