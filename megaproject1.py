import speech_recognition as sr
import webbrowser
import pyttsx3
import os
import sys
import time
import datetime
import musiclibrary
import requests  
import google.generativeai as genai

# Initialize recognizer & text-to-speech engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()

# API Keys
newsapi = "api key"  
weather_api = "api key"
genai_key = "api key"  # Updated API Key

# Configure AI Model
genai.configure(api_key=genai_key)
model = genai.GenerativeModel("gemini-1.5-flash")

def speak(text):
    """Speak the given text."""
    engine.say(text)
    engine.runAndWait()

def greet_user():
    """Greets the user based on the time of day."""
    hour = datetime.datetime.now().hour
    if hour < 12:
        speak("Good morning!")
    elif 12 <= hour < 18:
        speak("Good afternoon!")
    else:
        speak("Good evening!")
    speak("Orion is now active. How can I assist you?")

def aiprocess(command):
    """Processes AI-based commands using Gemini API."""
    response = model.generate_content(
        command,
        generation_config={"max_output_tokens": 50}
    )
    if response.text:
        speak(response.text)
        print(response.text)
    else:
        speak("I couldn't process that. Please try again.")

def process_command(command):
    """Handles user commands."""
    command = command.lower()

    if "open google" in command:
        webbrowser.open("https://google.com")
    elif "open youtube" in command:
        webbrowser.open("https://youtube.com")
    elif "open facebook" in command:
        webbrowser.open("https://facebook.com")
    elif "open opera" in command:
        webbrowser.open("https://opera.com")
    elif "open whatsapp" in command:
        webbrowser.open("https://web.whatsapp.com")
    elif command.startswith("play"):
        song = command.split(" ")[1]
        link = musiclibrary.music.get(song, "No link found")
        webbrowser.open(link)
    elif "tell me news" in command:
        fetch_news()
    elif "tell me weather" in command:
        fetch_weather()
    elif "restart" in command:
        speak("Restarting the system now.")
        print("Restarting...")
        time.sleep(2)  # Give some time before restart
        os.system("shutdown /r /t 1")  # Windows restart command
        # For Linux/Mac, use: os.system("sudo reboot")
    elif "shutdown" in command:
        speak("Shutting down the system now.")
        print("Shutting down...")
        time.sleep(2)  # Give some time before shutdown
        os.system("shutdown /s /t 1")  # Windows shutdown command

    else:
        aiprocess(command)

def fetch_news():
    """Fetches and reads out the latest news headlines."""
    r = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={newsapi}")
    if r.status_code == 200:
        data = r.json()
        articles = data.get("articles", [])
        if articles:
            speak("Here are the latest news headlines.")
            for article in articles[:5]:  
                speak(article['title'])
        else:
            speak("Sorry, I couldn't find any news at the moment.")
    else:
        speak("Sorry, I am unable to fetch news right now.")

def fetch_weather(city="Lahore"):
    """Fetches current weather conditions."""
    url = f"http://api.weatherapi.com/v1/current.json?key={weather_api}&q={city}&aqi=no"
    response = requests.get(url)
    if response.status_code == 200:
        weather_data = response.json()
        temp = weather_data["current"]["temp_c"]
        description = weather_data["current"]["condition"]["text"]
        speak(f"The current temperature in {city} is {temp} degrees Celsius with {description}.")
    else:
        speak("Unable to retrieve weather data.")

if __name__ == "__main__":
    greet_user()
    while True:
        try:
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source)  # Reduce background noise
                print("Listening for commands...")
                audio = recognizer.listen(source, timeout=5)

            command = recognizer.recognize_google(audio)
            print(f"You said: {command}")
            process_command(command)

        except sr.UnknownValueError:
            print("Sorry, I couldn't understand that.")
        except sr.RequestError:
            print("Could not request results, please check your internet connection.")
        except Exception as e:
            print(f"Error: {e}")
