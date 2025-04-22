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
import wmi
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
import cv2
import numpy as np
from pprint import pprint
import geocoder


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
        print("Good Morning ")
        speak("Good Morning ")
    elif 12 <= hour < 18:
        print("Good Afternoon ")
        speak("Good Afternoon ")
    else:
        print("Good Evening ")
        speak("Good Evening ")
    
    print("I am your Assistant, divya")
    speak("I am your Assistant, divya")
    
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
    return query

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
        # Open WhatsApp Web
        whatsapp_url = f"https://web.whatsapp.com/send?phone={phone_number}&text={message}"
        webbrowser.open(whatsapp_url)

        # Wait for WhatsApp Web to load and for user to scan QR code
        print("Please scan the QR code to log in.")
        time.sleep(20)  # Increase if needed

        # Use pywinauto to focus on the browser window
        app = application.Application().connect(title_re=".*WhatsApp.*")
        app_window = app.window(title_re=".*WhatsApp.*")
        app_window.set_focus()

        # Simulate pressing 'Enter' to send the message
        time.sleep(2)  # Wait for the message box to be focused
        pyautogui.press('enter')

        print(f"Message sent successfully to {phone_number}!")

    except Exception as e:
        print(f"Failed to send message: {str(e)}")

# Example usage
def trigger_alert():
    recipient_number = '918555874504'  # The recipient's phone number in international format without "+"
    alert_message = "emergency"  # The alert message

    send_whatsapp_message(recipient_number, alert_message)


def playMusic():
    print("which song you want to search")
    speak("which song you want to search")
    search = takeCommand()
    url = f"https://www.youtube.com/search?q={search}"
    webbrowser.open(url)
    time.sleep(5)  # Wait for YouTube to load
    pyautogui.press('enter')
    pyautogui.press('enter')

def pauseMusic():
    """ Pause the currently playing music """
    print("Pausing music")
    speak("Pausing music")
    pyautogui.press('space')  # Press space to pause

def resumeMusic():
    """ Resume the currently playing music """
    speak("Resuming music")
    pyautogui.press('space')  # Press space to resume

def stopMusic():
    """ Stop the music and close YouTube """
    speak("Stopping the music and closing YouTube")
    pyautogui.hotkey('ctrl', 'w')  # Close the current tab
    time.sleep(1)
    pyautogui.hotkey('ctrl', 'w')  # Close the tab if it is still open


def get_current_time():
    now = datetime.datetime.now()
    current_hour = now.hour
    current_minute = now.minute
    print(f"Current time is {current_hour:02d}:{current_minute:02d}")
    return current_hour, current_minute

def set_alarm(alarm_hour, alarm_minute, medication_name):
    while True:
        current_hour, current_minute = get_current_time()

        # Check if current time matches the alarm time
        if current_hour == alarm_hour and current_minute == alarm_minute:
            print("Reminder take "+ medication_name)
            speak("Reminder take "+ medication_name)
            break
        # Wait for 1 minute before checking the time again
        time.sleep(60)

# List of general jokes
general_jokes = [
    "Why don't skeletons fight each other? They don't have the guts.",
    "What do you call fake spaghetti? An impasta!",
    "Why don't scientists trust atoms? Because they make up everything!",
    "I'm reading a book about anti-gravity. It's impossible to put down.",
    "Why did the scarecrow win an award? Because he was outstanding in his field!"
]

def speak(text):
    engine.say(text)
    engine.runAndWait()

def listen():
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(audio)
            print(f"You said: {command}")
            return command.lower()
        except sr.UnknownValueError:
            speak("Sorry, I did not understand that.")
        except sr.RequestError:
            speak("Sorry, I am having trouble connecting to the service.")
        return ""

def tell_joke():
    import random
    # Select a random general joke from the list
    joke = random.choice(general_jokes)
    speak(joke)
    print(joke)

def main():
    speak("Hello! How can I assist you today?")
    while True:
        command = listen()
        if 'joke' in command:
            tell_joke()
        elif 'one more' in command:
            tell_joke()
        
        elif 'exit' in command:
            speak("Goodbye!")
            break


# Load the CSV file
data = pd.read_csv('d.csv')

# Preprocess data to create a lookup table for diseases
disease_dict = {}
for i, row in data.iterrows():
    disease = row['disease'].lower()
    symptoms = row['symptoms'].lower()
    food_items = row['food_items']
    nutritional_values = row['nutritional_values']
    health_benefits = row['health_benefits']
    disease_dict[disease] = {
        'food_items': food_items,
        'nutritional_values': nutritional_values,
        'health_benefits': health_benefits,
        'symptoms': symptoms
    }

# Function to recognize speech input
def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Please say the disease or symptoms:")
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio)
            print(f"You said: {text}")
            return text.lower()
        except sr.UnknownValueError:
            engine.say("Sorry, I did not understand that.")
            engine.runAndWait()
            return None

# Function to find the diet plan based on input
def find_diet_plan(input_text):
    for disease, info in disease_dict.items():
        if disease in input_text or any(symptom in input_text for symptom in info['symptoms'].split(',')):
            return info
    return None

# Main function to run the voice assistant
def voice_assistant():
    while True:
        user_input = recognize_speech()
        if user_input:
            diet_plan = find_diet_plan(user_input)
            if diet_plan:
                response = f"For {user_input}, consider consuming {diet_plan['food_items']}. These foods are beneficial because {diet_plan['health_benefits']}."
                print(response)
                engine.say(response)
                engine.runAndWait()
            elif user_input == 'exit' :
                break
                
            else:
                engine.say("Sorry, I couldn't find a specific diet plan for your symptoms. Please consult a doctor for a personalized diet.")
                engine.runSAndWait()
            
def ambulance():
    GEOAPIFY_API_KEY = "7e3060986bbd458daad681f933b6d6f7"  # Get from geoapify.com

    def get_precise_location():
        """Get precise location using Geoapify without area-specific logic"""
        try:
            # Step 1: Get coordinates (IP-based)
            ip_data = requests.get('https://ipapi.co/json/', timeout=3).json()
            lat, lng = ip_data.get('latitude'), ip_data.get('longitude')
            
            if not lat or not lng:
                return None, "Could not get coordinates"
            
            # Step 2: Get precise address using Geoapify
            url = f"https://api.geoapify.com/v1/geocode/reverse?lat={lat}&lon={lng}&apiKey={GEOAPIFY_API_KEY}"
            response = requests.get(url).json()
            
            if not response['features']:
                return (lat, lng), "Address not found"
            
            # Extract complete address components
            properties = response['features'][0]['properties']
            address = {
                'road': properties.get('street'),
                'neighborhood': properties.get('suburb'),
                'city': properties.get('city'),
                'state': properties.get('state'),
                'postcode': properties.get('postcode'),
                'country': properties.get('country')
            }
            
            # Format address string
            address_parts = [
                address['road'],
                address['neighborhood'],
                f"{address['city']}, {address['state']}",
                address['postcode'],
                address['country']
            ]
            formatted_address = ", ".join(filter(None, address_parts))
            
            return (lat, lng), formatted_address
            
        except requests.exceptions.RequestException as e:
            print(f"Network error: {e}")
            return None, "Network error"
        except Exception as e:
            print(f"Unexpected error: {e}")
            return None, "Location service error"

    # Usage Example
    if __name__ == "__main__":
        print("Detecting location...")
        coords, address = get_precise_location()
        
        if coords:
            print(f"\nCoordinates: {coords}")
            print("Full Address Details:")
            pprint(address)  # Pretty print full address
        else:
            print(f"\nError: {address}")

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


def falldetect():

    class FallDetector:
        def __init__(self):
            # Initialize background subtractor
            self.fgbg = cv2.createBackgroundSubtractorMOG2(history=500, varThreshold=16, detectShadows=False)
            
            # Fall detection parameters
            self.aspect_ratio_threshold = 0.6  # Lowered for better sensitivity
            self.min_contour_area = 2000       # Increased to ignore small movements
            self.stationary_time = 1.5         # Seconds of inactivity to confirm fall
            self.impact_threshold = 2.0        # Size change ratio for impact detection
            
            # State variables
            self.last_motion_time = time.time()
            self.last_aspect_ratio = None
            self.fall_detected = False
            self.alert_cooldown = 0

        def detect_fall(self, frame):
            # Preprocessing
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            blurred = cv2.GaussianBlur(gray, (7, 7), 0)
            
            # Background subtraction
            fgmask = self.fgbg.apply(blurred)
            _, fgmask = cv2.threshold(fgmask, 127, 255, cv2.THRESH_BINARY)
            
            # Noise removal
            kernel = np.ones((7,7), np.uint8)
            fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel)
            fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_CLOSE, kernel)
            
            # Find contours
            contours, _ = cv2.findContours(fgmask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            motion_detected = False
            fall_conditions_met = False
            current_aspect_ratio = None
            
            for contour in contours:
                if cv2.contourArea(contour) < self.min_contour_area:
                    continue
                    
                motion_detected = True
                self.last_motion_time = time.time()
                
                # Get bounding box
                x, y, w, h = cv2.boundingRect(contour)
                current_aspect_ratio = float(h)/w
                
                # Check for sudden change in aspect ratio (impact)
                if self.last_aspect_ratio and (self.last_aspect_ratio / current_aspect_ratio) > self.impact_threshold:
                    print(f"Impact detected! Ratio change: {self.last_aspect_ratio:.2f} -> {current_aspect_ratio:.2f}")
                    fall_conditions_met = True
                
                # Check if person is lying down
                if current_aspect_ratio < self.aspect_ratio_threshold:
                    fall_conditions_met = True
                
                self.last_aspect_ratio = current_aspect_ratio
                cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), 2)
                cv2.putText(frame, f"Ratio: {current_aspect_ratio:.2f}", (x, y-10), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1)
            
            # Fall confirmation logic
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

    def process_video_file(video_path):
        detector = FallDetector()
        
        if not os.path.exists(video_path):
            print(f"Error: File not found at {video_path}")
            return
        
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            print(f"Error: Could not open video file {video_path}")
            return
        
        fps = cap.get(cv2.CAP_PROP_FPS)
        delay = int(1000/fps) if fps > 0 else 30
        
        print("Processing video...")
        print("Press 'q' to quit")
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
                
            frame = cv2.resize(frame, (640, 480))  # Standardize size
            
            fall_detected, processed_frame = detector.detect_fall(frame)
            
            if fall_detected:
                cv2.putText(processed_frame, "FALL DETECTED!", (50, 50), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                print("ALERT: Fall detected!")
            
            cv2.imshow('Fall Detection', processed_frame)
            
            if cv2.waitKey(delay) & 0xFF == ord('q'):
                break
                
        cap.release()
        cv2.destroyAllWindows()
        print("Processing complete")

    if __name__ == "__main__":
        video_file = "fall.mp4"  # Change to your video filename
        
        # List files in current directory to help debugging
        print("Files in current directory:")
        print(os.listdir('.'))
        
        process_video_file(video_file)
def fetch_medicine_info(medicine_name):
    with open('c.csv', mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['medicine_name'].lower() == medicine_name.lower():
                description = row['description']
                uses = row['uses']
                dosage = row['dosage']
                return description, uses, dosage
    return None, None, None

        
def handleCommands():
    wishMe() 
    while True:
        query = takeCommand().lower()

        if "hello" in query:
            print("Hello, how are you ?")
            speak("Hello, how are you ?")
        elif "i am fine" in query:
            print("that's great,")
            speak("that's great,")
        elif "how are you" in query:
            print("I am doing great")
            speak("I am doing great")
        elif "thank you" in query:
            print("you are welcome,")
            speak("you are welcome,")

        elif 'open youtube' in query:
            webbrowser.open("youtube.com")

        elif 'open google' in query:
            webbrowser.open("google.com")

        elif 'time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            print(f"Sir, the time is {strTime}")
            speak(f"Sir, the time is {strTime}")

        elif 'medicine' in query or 'tablet' in query:
            print("Please tell me the name of the medicine.")
            speak("Please tell me the name of the medicine.")
            medicine_name = takeCommand()

            if medicine_name != "None":
                description, uses, dosage = fetch_medicine_info(medicine_name)
                
                if description and uses and dosage:
                    print("Here is the information I found.")
                    speak("Here is the information I found.")
                    print(f"Description: {description}")
                    speak(f"Description: {description}")
                    print(f"Uses: {uses}")
                    speak(f"Uses: {uses}")
                    print(f"Dosage: {dosage}")
                    speak(f"Dosage: {dosage}")
                    print('thanks for your time')
                    speak('thanks for your time')
                else:
                    speak("Sorry, I couldn't find information on that medicine.")
        elif 'alert' in query:
            print("Sure,I will send an alert as soon as possible.")
            speak("Sure,I will send an alert as soon as possible.")
            trigger_alert()

        
        elif "set alarm" in query:
            speak("set the alarm hour in 24-hour format.")
            alarm_hour = takeCommand()
            if alarm_hour:
                alarm_hour = int(alarm_hour)
            speak("Please set the alarm minute.")
            alarm_minute = takeCommand()
            if alarm_minute:
                alarm_minute = int(alarm_minute)
            
            if alarm_hour is not None and alarm_minute is not None:
                print("medication_name")
                speak("medication_name")
                medication_name = takeCommand()
                print(f"Alarm is set for {alarm_hour:02d}:{alarm_minute:02d}.")
                speak(f"Alarm is set for {alarm_hour:02d}:{alarm_minute:02d}.")
                set_alarm(alarm_hour, alarm_minute, medication_name)

        elif 'tell me a joke' in query:
            main()

        elif "play music" in query:
            playMusic()

        elif "pause" in query:
            pauseMusic()

        elif "play" in query:
            resumeMusic()
        if ambulance():
            handleEmergency()
        elif "resume" in query:
            stopMusic()
        elif "diet plan" in query :
            voice_assistant()
        elif "detect" in query:
            falldetect()
            query = takeCommand().lower()
            if "exit" in query:
                break
        elif "weather" in query:
            speak("give a comand to search")
            search = takeCommand()
            url = f"https://www.google.com/search?q={search}"
            r  = requests.get(url)
            data = BeautifulSoup(r.text,"html.parser")
            temp = data.find("div", class_ = "BNeawe").text
            speak(f"current{search} is {temp}")

        elif 'exit' in query:
            print("Thanks for giving me your time")
            speak("Thanks for giving me your time")
            break


if __name__ == '__main__':
    handleCommands()
