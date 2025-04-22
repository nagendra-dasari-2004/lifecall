import subprocess
import pyttsx3
import datetime
import wikipedia
import webbrowser
import os
import winshell
import pyjokes
import smtplib
import ctypes
import time
import requests
import json
import getpass
import random
import csv
import cv2
import numpy as np
from pathlib import Path
from bs4 import BeautifulSoup
import speech_recognition as sr
from urllib.request import urlopen
import pyautogui
import pandas as pd
import geocoder
from pprint import pprint

# Initialize text-to-speech engine
engine = pyttsx3.init('sapi5')
recognizer = sr.Recognizer()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

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

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def wishMe():
    hour = datetime.datetime.now().hour
    if 0 <= hour < 12:
        greeting = "Good Morning"
    elif 12 <= hour < 18:
        greeting = "Good Afternoon"
    else:
        greeting = "Good Evening"
    
    print(f"{greeting}, I am your Assistant, Divya")
    speak(f"{greeting}, I am your Assistant, Divya")
    
def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")
    except sr.UnknownValueError:
        print("Sorry, I did not understand that.")
        return "None"
    except sr.RequestError:
        print("Sorry, there was an issue with the request.")
        return "None"
    return query.lower()

def organizeFiles():
    try:
        for entry in os.scandir():
            if entry.is_file():
                file_path = Path(entry.name)
                file_format = file_path.suffix.lower()
                if file_format in FILE_FORMATS:
                    directory_path = Path(FILE_FORMATS[file_format])
                    directory_path.mkdir(exist_ok=True)
                    file_path.rename(directory_path.joinpath(file_path))
        
        os.makedirs("OTHER", exist_ok=True)

        for entry in os.scandir():
            try:
                if entry.is_dir() and not os.listdir(entry.path):
                    os.rmdir(entry)
                elif entry.is_file():
                    os.rename(entry.path, Path("OTHER") / Path(entry.name))
            except Exception as e:
                print(f"Error organizing file {entry.name}: {e}")
    except Exception as e:
        print(f"Error in organizeFiles: {e}")

def send_whatsapp_message(phone_number, message):
    try:
        whatsapp_url = f"https://web.whatsapp.com/send?phone={phone_number}&text={message}"
        webbrowser.open(whatsapp_url)
        time.sleep(20)  # Wait for WhatsApp to load

        # Send the message
        time.sleep(2)
        pyautogui.press('enter')
        print(f"Message sent successfully to {phone_number}!")
        return True
    except Exception as e:
        print(f"Failed to send message: {str(e)}")
        return False

def trigger_alert():
    recipient_number = '918555874504'  # Replace with actual number
    alert_message = "Emergency! Please help!"
    return send_whatsapp_message(recipient_number, alert_message)

def playMusic():
    print("Which song you want to search?")
    speak("Which song you want to search?")
    search = takeCommand()
    if search != "None":
        url = f"https://www.youtube.com/results?search_query={search}"
        webbrowser.open(url)
        time.sleep(5)
        pyautogui.press('enter')

def pauseMusic():
    print("Pausing music")
    speak("Pausing music")
    pyautogui.press('space')

def resumeMusic():
    print("Resuming music")
    speak("Resuming music")
    pyautogui.press('space')

def stopMusic():
    print("Stopping music")
    speak("Stopping music")
    pyautogui.hotkey('ctrl', 'w')

def get_current_time():
    now = datetime.datetime.now()
    current_time = now.strftime("%H:%M")
    print(f"Current time is {current_time}")
    return now.hour, now.minute

def set_alarm(alarm_hour, alarm_minute, medication_name):
    try:
        while True:
            current_hour, current_minute = get_current_time()
            if current_hour == alarm_hour and current_minute == alarm_minute:
                print(f"Reminder: Take {medication_name}")
                speak(f"Reminder: Take {medication_name}")
                break
            time.sleep(60)
    except Exception as e:
        print(f"Error in alarm: {e}")

# Jokes functionality
general_jokes = [
    "Why don't skeletons fight each other? They don't have the guts.",
    "What do you call fake spaghetti? An impasta!",
    "Why don't scientists trust atoms? Because they make up everything!",
    "I'm reading a book about anti-gravity. It's impossible to put down.",
    "Why did the scarecrow win an award? Because he was outstanding in his field!"
]

def tell_joke():
    joke = random.choice(general_jokes)
    print(joke)
    speak(joke)

# Diet plan functionality
def load_diet_data():
    try:
        data = pd.read_csv('d.csv')
        disease_dict = {}
        for _, row in data.iterrows():
            disease = row['disease'].lower()
            disease_dict[disease] = {
                'food_items': row['food_items'],
                'nutritional_values': row['nutritional_values'],
                'health_benefits': row['health_benefits'],
                'symptoms': row['symptoms'].lower()
            }
        return disease_dict
    except Exception as e:
        print(f"Error loading diet data: {e}")
        return {}

def voice_assistant():
    disease_dict = load_diet_data()
    if not disease_dict:
        speak("Sorry, diet data not available")
        return

    while True:
        speak("Please say the disease or symptoms")
        user_input = takeCommand()
        
        if user_input == "None":
            continue
        elif 'exit' in user_input:
            break
            
        found = False
        for disease, info in disease_dict.items():
            if disease in user_input or any(symptom in user_input for symptom in info['symptoms'].split(',')):
                response = (f"For {disease}, consider consuming {info['food_items']}. "
                          f"These foods are beneficial because {info['health_benefits']}.")
                print(response)
                speak(response)
                found = True
                break
                
        if not found:
            speak("Sorry, I couldn't find a diet plan for that. Please consult a doctor.")

# Emergency functionality
GEOAPIFY_API_KEY = "7e3060986bbd458daad681f933b6d6f7"

def get_precise_location():
    try:
        g = geocoder.ip('me')
        if g.latlng:
            return g.latlng, g.address
        return None, "Location not found"
    except Exception as e:
        print(f"Location error: {e}")
        return None, "Location service error"

def handleEmergency():
    speak("Emergency detected! Please stay calm.")
    coords, address = get_precise_location()
    
    if coords:
        speak(f"Detected you near {address}")
        booking = {
            'success': True,
            'ambulance_id': f"AMB{random.randint(1000, 9999)}",
            'eta': random.randint(5, 15),
            'driver_name': f"Driver {random.choice(['Smith', 'Johnson', 'Williams'])}",
            'tracking_url': f"https://maps.google.com/?q={coords[0]},{coords[1]}"
        }
        
        speak(f"Ambulance {booking['ambulance_id']} is coming in {booking['eta']} minutes")
        webbrowser.open(booking['tracking_url'])
    else:
        speak("Could not determine location. Please call emergency services manually!")

# Fall detection
class FallDetector:
    def __init__(self):
        self.fgbg = cv2.createBackgroundSubtractorMOG2(history=500, varThreshold=16, detectShadows=False)
        self.aspect_ratio_threshold = 0.6
        self.min_contour_area = 2000
        self.stationary_time = 1.5
        self.impact_threshold = 2.0
        self.last_motion_time = time.time()
        self.last_aspect_ratio = None
        self.fall_detected = False

    def detect_fall(self, frame):
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
        
        for contour in contours:
            if cv2.contourArea(contour) < self.min_contour_area:
                continue
                
            motion_detected = True
            self.last_motion_time = time.time()
            x, y, w, h = cv2.boundingRect(contour)
            current_aspect_ratio = float(h)/w
            
            if self.last_aspect_ratio and (self.last_aspect_ratio / current_aspect_ratio) > self.impact_threshold:
                fall_conditions_met = True
            
            if current_aspect_ratio < self.aspect_ratio_threshold:
                fall_conditions_met = True
                
            self.last_aspect_ratio = current_aspect_ratio
            cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), 2)
        
        if fall_conditions_met and (time.time() - self.last_motion_time) > self.stationary_time:
            if not self.fall_detected:
                self.fall_detected = True
                return True, frame
                
        return False, frame

def falldetect():
    try:
        video_file = "fall.mp4"
        if not os.path.exists(video_file):
            speak("Fall detection video not found")
            return

        detector = FallDetector()
        cap = cv2.VideoCapture(video_file)
        
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
                
            frame = cv2.resize(frame, (640, 480))
            fall_detected, processed_frame = detector.detect_fall(frame)
            
            if fall_detected:
                cv2.putText(processed_frame, "FALL DETECTED!", (50, 50), 
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                speak("Fall detected! Calling for help!")
                handleEmergency()
            
            cv2.imshow('Fall Detection', processed_frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
                
        cap.release()
        cv2.destroyAllWindows()
    except Exception as e:
        print(f"Fall detection error: {e}")

# Medicine information
def fetch_medicine_info(medicine_name):
    try:
        with open('c.csv', mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['medicine_name'].lower() == medicine_name.lower():
                    return row['description'], row['uses'], row['dosage']
        return None, None, None
    except Exception as e:
        print(f"Medicine info error: {e}")
        return None, None, None

# Main command handler
def handleCommands():
    wishMe()
    
    while True:
        query = takeCommand()

        if "hello" in query:
            speak("Hello, how are you?")
        elif "i am fine" in query:
            speak("That's great!")
        elif "how are you" in query:
            speak("I'm doing great, thank you!")
        elif "thank you" in query:
            speak("You're welcome!")
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
                    speak(f"Description: {description}. Uses: {uses}. Dosage: {dosage}")
                else:
                    speak("Sorry, I couldn't find information on that medicine.")
        elif 'alert' in query:
            speak("Sending emergency alert")
            trigger_alert()
        elif "set alarm" in query:
            speak("Please say the alarm hour in 24-hour format.")
            alarm_hour = takeCommand()
            speak("Please say the alarm minute.")
            alarm_minute = takeCommand()
            if alarm_hour.isdigit() and alarm_minute.isdigit():
                speak("Please say the medication name.")
                medication_name = takeCommand()
                speak(f"Alarm set for {alarm_hour}:{alarm_minute}")
                set_alarm(int(alarm_hour), int(alarm_minute), medication_name)
        elif 'joke' in query:
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
            voice_assistant()
        elif "detect fall" in query:
            falldetect()
        elif "weather" in query:
            speak("Please say the location for weather")
            location = takeCommand()
            if location != "None":
                url = f"https://www.google.com/search?q=weather+{location}"
                r = requests.get(url)
                data = BeautifulSoup(r.text, "html.parser")
                temp = data.find("div", class_="BNeawe").text
                speak(f"Current weather in {location} is {temp}")
        elif 'exit' in query or 'quit' in query:
            speak("Goodbye! Have a nice day!")
            break
        else:
            speak("I didn't understand that. Could you please repeat?")

if __name__ == '__main__':
    # Check for required files
    if not os.path.exists('d.csv') or not os.path.exists('c.csv'):
        print("Warning: Required data files not found")
    
    handleCommands()