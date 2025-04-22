import subprocess
import datetime
import webbrowser
import os
import time
import requests
import json
import getpass
import random
import csv
import pandas as pd
from pathlib import Path
from bs4 import BeautifulSoup
from urllib.request import urlopen
import pyautogui
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import geocoder

# Windows-specific imports with fallbacks
try:
    import pyttsx3
    import winshell
    import pyjokes
    import ctypes
    import wmi
    from pywinauto import application
    WINDOWS = True
except ImportError:
    WINDOWS = False
    print("Warning: Running in limited mode - some Windows-specific features disabled")

try:
    import wikipedia
except ImportError:
    wikipedia = None

try:
    import speech_recognition as sr
except ImportError:
    sr = None

try:
    import wolframalpha
except ImportError:
    wolframalpha = None

try:
    import cv2
    import numpy as np
except ImportError:
    cv2 = None
    np = None

# Initialize text-to-speech engine
engine = None
recognizer = None
if WINDOWS:
    try:
        engine = pyttsx3.init('sapi5')
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[1].id)
        engine.setProperty('rate', 150)
    except Exception as e:
        print(f"Speech initialization error: {e}")
        WINDOWS = False

if sr:
    recognizer = sr.Recognizer()

# Define directories and file formats
DIRECTORIES = {
    "HTML": [".html", ".htm", ".xhtml"],
    "IMAGES": [".jpeg", ".jpg", ".tiff", ".gif", ".bmp", ".png", ".svg"],
    "VIDEOS": [".avi", ".flv", ".wmv", ".mov", ".mp4", ".webm", ".vob", ".mkv"],
    "DOCUMENTS": [".docx", ".doc", ".pdf", ".xls", ".xlsx", ".pptx"],
    "ARCHIVES": [".zip", ".rar", ".tar", ".gz"],
    "AUDIO": [".mp3", ".wav", ".aac"],
    "PLAINTEXT": [".txt"],
    "PYTHON": [".py"],
    "XML": [".xml"],
    "EXE": [".exe"],
    "SHELL": [".sh"]
}
FILE_FORMATS = {file_format: directory for directory, file_formats in DIRECTORIES.items() for file_format in file_formats}

# List of general jokes
general_jokes = [
    "Why don't skeletons fight each other? They don't have the guts.",
    "What do you call fake spaghetti? An impasta!",
    "Why don't scientists trust atoms? Because they make up everything!",
    "I'm reading a book about anti-gravity. It's impossible to put down.",
    "Why did the scarecrow win an award? Because he was outstanding in his field!"
]

def speak(audio):
    try:
        if engine:
            engine.say(audio)
            engine.runAndWait()
        else:
            print(f"[TTS Disabled] {audio}")
    except Exception as e:
        print(f"Speech error: {e}")

def takeCommand():
    if not recognizer:
        print("Speech recognition not available")
        return "None"
    
    r = recognizer
    r.energy_threshold = 4000
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

def wishMe():
    hour = datetime.datetime.now().hour
    if 0 <= hour < 12:
        speak("Good Morning")
    elif 12 <= hour < 18:
        speak("Good Afternoon")
    else:
        speak("Good Evening")
    speak("I am your Assistant, Divya")

def organizeFiles():
    for entry in os.scandir():
        if entry.is_file():
            file_path = Path(entry.name)
            file_format = file_path.suffix.lower()
            if file_format in FILE_FORMATS:
                directory_path = Path(FILE_FORMATS[file_format])
                directory_path.mkdir(exist_ok=True)
                file_path.rename(directory_path.joinpath(file_path))
    
    try:
        os.mkdir("OTHER")
    except FileExistsError:
        pass

    for entry in os.scandir():
        try:
            if entry.is_dir():
                os.rmdir(entry)
            else:
                os.rename(entry.path, Path("OTHER") / Path(entry.name))
        except Exception as e:
            print(f"Error organizing file {entry.name}: {e}")

def send_whatsapp_message(phone_number, message):
    try:
        whatsapp_url = f"https://web.whatsapp.com/send?phone={phone_number}&text={message}"
        webbrowser.open(whatsapp_url)
        time.sleep(20)
        
        if WINDOWS:
            app = application.Application().connect(title_re=".*WhatsApp.*")
            app_window = app.window(title_re=".*WhatsApp.*")
            app_window.set_focus()
        
        time.sleep(2)
        pyautogui.press('enter')
        speak(f"Message sent successfully to {phone_number}!")
    except Exception as e:
        speak(f"Failed to send message: {str(e)}")

def trigger_alert():
    recipient_number = '918555874504'
    alert_message = "emergency"
    send_whatsapp_message(recipient_number, alert_message)

def playMusic():
    speak("Which song you want to search")
    search = takeCommand()
    if search != "None":
        url = f"https://www.youtube.com/search?q={search}"
        webbrowser.open(url)
        time.sleep(5)
        pyautogui.press('enter')
        pyautogui.press('enter')

def pauseMusic():
    speak("Pausing music")
    pyautogui.press('space')

def resumeMusic():
    speak("Resuming music")
    pyautogui.press('space')

def stopMusic():
    speak("Stopping the music and closing YouTube")
    pyautogui.hotkey('ctrl', 'w')
    time.sleep(1)
    pyautogui.hotkey('ctrl', 'w')

def get_current_time():
    now = datetime.datetime.now()
    current_hour = now.hour
    current_minute = now.minute
    speak(f"Current time is {current_hour:02d}:{current_minute:02d}")
    return current_hour, current_minute

def set_alarm(alarm_hour, alarm_minute, medication_name):
    while True:
        current_hour, current_minute = get_current_time()
        if current_hour == alarm_hour and current_minute == alarm_minute:
            speak(f"Reminder take {medication_name}")
            break
        time.sleep(60)

def tell_joke():
    joke = random.choice(general_jokes)
    speak(joke)
    print(joke)

def joke_mode():
    speak("Hello! How can I assist you today?")
    while True:
        command = takeCommand()
        if 'joke' in command:
            tell_joke()
        elif 'one more' in command:
            tell_joke()
        elif 'exit' in command:
            speak("Goodbye!")
            break

# Load the CSV files
def load_data():
    try:
        diet_data = pd.read_csv('d.csv')
        medicine_data = pd.read_csv('c.csv')
        return diet_data, medicine_data
    except Exception as e:
        print(f"Error loading data files: {e}")
        return None, None

diet_data, medicine_data = load_data()

def find_diet_plan(input_text):
    if diet_data is None:
        return None
        
    for i, row in diet_data.iterrows():
        disease = row['disease'].lower()
        symptoms = row['symptoms'].lower()
        if disease in input_text or any(symptom in input_text for symptom in symptoms.split(',')):
            return {
                'food_items': row['food_items'],
                'nutritional_values': row['nutritional_values'],
                'health_benefits': row['health_benefits'],
                'symptoms': symptoms
            }
    return None

def fetch_medicine_info(medicine_name):
    if medicine_data is None:
        return None, None, None
        
    for i, row in medicine_data.iterrows():
        if row['medicine_name'].lower() == medicine_name.lower():
            return row['description'], row['uses'], row['dosage']
    return None, None, None

class FallDetector:
    def __init__(self):
        if cv2 is None:
            return
            
        self.fgbg = cv2.createBackgroundSubtractorMOG2(history=500, varThreshold=16, detectShadows=False)
        self.aspect_ratio_threshold = 0.6
        self.min_contour_area = 2000
        self.stationary_time = 1.5
        self.impact_threshold = 2.0
        self.last_motion_time = time.time()
        self.last_aspect_ratio = None
        self.fall_detected = False
        self.alert_cooldown = 0

    def detect_fall(self, frame):
        if cv2 is None:
            return False, frame
            
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (7, 7), 0)
        fgmask = self.fgbg.apply(blurred)
        _, fgmask = cv2.threshold(fgmask, 127, 255, cv2.THRESH_BINARY)
        kernel = np.ones((7,7), np.uint8)
        fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel)
        fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_CLOSE, kernel)
        contours, _ = cv2.findContours(fgmask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        motion_detected = False
        fall_conditions_met = False
        current_aspect_ratio = None
        
        for contour in contours:
            if cv2.contourArea(contour) < self.min_contour_area:
                continue
                
            motion_detected = True
            self.last_motion_time = time.time()
            x, y, w, h = cv2.boundingRect(contour)
            current_aspect_ratio = float(h)/w
            
            if self.last_aspect_ratio and (self.last_aspect_ratio / current_aspect_ratio) > self.impact_threshold:
                print(f"Impact detected! Ratio change: {self.last_aspect_ratio:.2f} -> {current_aspect_ratio:.2f}")
                fall_conditions_met = True
            
            if current_aspect_ratio < self.aspect_ratio_threshold:
                fall_conditions_met = True
            
            self.last_aspect_ratio = current_aspect_ratio
            cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), 2)
            cv2.putText(frame, f"Ratio: {current_aspect_ratio:.2f}", (x, y-10), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1)
        
        if fall_conditions_met:
            inactivity_duration = time.time() - self.last_motion_time
            print(f"Fall conditions met. Inactivity: {inactivity_duration:.2f}s")
            
            if inactivity_duration > self.stationary_time:
                if not self.fall_detected:
                    self.fall_detected = True
                    return True, frame
        else:
            self.fall_detected = False
        
        return False, frame

def falldetect():
    if cv2 is None:
        speak("OpenCV is not installed. Fall detection disabled.")
        return
        
    video_file = "fall.mp4"
    detector = FallDetector()
    
    if not os.path.exists(video_file):
        speak(f"Error: Video file {video_file} not found")
        return
    
    cap = cv2.VideoCapture(video_file)
    if not cap.isOpened():
        speak(f"Error: Could not open video file {video_file}")
        return
    
    fps = cap.get(cv2.CAP_PROP_FPS)
    delay = int(1000/fps) if fps > 0 else 30
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
            
        frame = cv2.resize(frame, (640, 480))
        fall_detected, processed_frame = detector.detect_fall(frame)
        
        if fall_detected:
            cv2.putText(processed_frame, "FALL DETECTED!", (50, 50), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            speak("ALERT: Fall detected!")
            trigger_alert()
        
        cv2.imshow('Fall Detection', processed_frame)
        
        if cv2.waitKey(delay) & 0xFF == ord('q'):
            break
            
    cap.release()
    cv2.destroyAllWindows()

def get_weather():
    speak("Which location's weather would you like to know?")
    location = takeCommand()
    if location != "None":
        url = f"https://www.google.com/search?q=weather+{location}"
        r = requests.get(url)
        data = BeautifulSoup(r.text, "html.parser")
        temp = data.find("div", class_="BNeawe").text
        speak(f"Current weather in {location} is {temp}")

def handleEmergency():
    speak("Emergency detected! Please stay calm.")
    try:
        # Try to get precise location
        g = geocoder.ip('me')
        if g.latlng:
            lat, lng = g.latlng
            address = g.address
            speak(f"Detected you near {address}")
            
            # Simulate ambulance booking
            booking = {
                'success': True,
                'ambulance_id': f"AMB{random.randint(1000, 9999)}",
                'eta': random.randint(5, 15),
                'driver_name': f"Driver {random.choice(['Smith', 'Johnson', 'Williams'])}",
                'tracking_url': f"https://maps.google.com/?q={lat},{lng}"
            }
            
            speak(f"Ambulance {booking['ambulance_id']} is coming in {booking['eta']} minutes")
            speak(f"Driver {booking['driver_name']} will contact you")
            webbrowser.open(booking['tracking_url'])
        else:
            speak("Could not determine location. Please call 108 manually!")
    except Exception as e:
        print(f"Emergency error: {e}")
        speak("Emergency services couldn't be contacted. Please call 108 manually!")

def handleCommands():
    wishMe()
    while True:
        query = takeCommand().lower()

        if query == "none":
            continue
            
        if "hello" in query:
            speak("Hello, how are you?")
        elif "i am fine" in query:
            speak("That's great!")
        elif "how are you" in query:
            speak("I am doing great")
        elif "thank you" in query:
            speak("You are welcome")
        elif 'open youtube' in query:
            webbrowser.open("youtube.com")
        elif 'open google' in query:
            webbrowser.open("google.com")
        elif 'time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"The time is {strTime}")
        elif 'medicine' in query or 'tablet' in query:
            speak("Please tell me the name of the medicine.")
            medicine_name = takeCommand()
            if medicine_name != "None":
                description, uses, dosage = fetch_medicine_info(medicine_name)
                if description and uses and dosage:
                    speak(f"Here's information about {medicine_name}")
                    speak(f"Description: {description}")
                    speak(f"Uses: {uses}")
                    speak(f"Dosage: {dosage}")
                else:
                    speak("Sorry, I couldn't find information on that medicine.")
        elif 'alert' in query or 'emergency' in query:
            speak("Activating emergency protocol!")
            handleEmergency()
        elif "set alarm" in query:
            speak("Set the alarm hour in 24-hour format.")
            alarm_hour = takeCommand()
            speak("Set the alarm minute.")
            alarm_minute = takeCommand()
            if alarm_hour.isdigit() and alarm_minute.isdigit():
                speak("What medication should I remind you about?")
                medication_name = takeCommand()
                speak(f"Alarm set for {alarm_hour}:{alarm_minute} for {medication_name}")
                set_alarm(int(alarm_hour), int(alarm_minute), medication_name)
        elif 'tell me a joke' in query or 'joke' in query:
            tell_joke()
        elif "play music" in query:
            playMusic()
        elif "pause" in query:
            pauseMusic()
        elif "resume" in query or "play" in query:
            resumeMusic()
        elif "stop music" in query:
            stopMusic()
        elif "diet plan" in query:
            speak("Please describe your symptoms or condition")
            symptoms = takeCommand()
            if symptoms != "None":
                plan = find_diet_plan(symptoms)
                if plan:
                    speak(f"For your condition, consider eating {plan['food_items']}")
                    speak(f"These foods provide {plan['nutritional_values']}")
                    speak(f"Health benefits include {plan['health_benefits']}")
                else:
                    speak("I couldn't find a specific diet plan for your symptoms")
        elif "detect fall" in query and cv2:
            falldetect()
        elif "weather" in query:
            get_weather()
        elif "organize files" in query:
            organizeFiles()
            speak("Files organized successfully")
        elif 'exit' in query or 'quit' in query:
            speak("Goodbye! Have a nice day.")
            break
        else:
            speak("I didn't understand that command. Please try again.")

if __name__ == '__main__':
    handleCommands()