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
        # Construct the WhatsApp Web URL with the phone number and message
        whatsapp_url = f"https://web.whatsapp.com/send?phone={phone_number}&text={message}"

        # Open WhatsApp Web in the default browser
        webbrowser.open(whatsapp_url)

        # Wait for WhatsApp Web to load
        time.sleep(8)  # Adjust based on your system's speed

        # Press "Enter" to send the message
        pyautogui.press('enter')

        print(f"Message sent successfully to {phone_number}!")

    except Exception as e:
        print(f"Failed to send message: {str(e)}")

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
            recipient_number = '918555874504'  # Example number
            alert_message = "Emergency alert"
            send_whatsapp_message(recipient_number, alert_message)

        
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

        elif "resume" in query:
            stopMusic()
        elif "diet plan" in query :
            voice_assistant()

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
