import speech_recognition as sr
import webbrowser
import pyttsx3
import os
import datetime
import musiclibrary
import requests 

recognizer = sr.Recognizer()
engine = pyttsx3.init()
newsapi = "0f8c1818fae645ffb632113d9d04aa74"
def speak(text):
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
    speak("How can I assist you today?")
greet_user() 

import google.generativeai as genai

def aiprocess(command):
    genai.configure(api_key="AIzaSyBTuIrqC--YeFH-55YqURCmIXRI3ROA7DI")
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(
        command,
        generation_config={"max_output_tokens": 50}  # Adjust this value for shorter responses
    )
    speak(response.text)
    print(response.text)

def processcommand(c):
    if "open google" in c.lower():
        webbrowser.open("https://google.com")
    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")
    elif "open facebook" in c.lower():
        webbrowser.open("https://facebook.com")
    elif "open opera" in c.lower():
        webbrowser.open("https://opera.com")
    elif "open whatsapp" in c.lower():
        webbrowser.open("https://web.whatsapp.com")
    elif c.lower().startswith("play"):
        song = c.lower().split(" ")[1]
        link = musiclibrary.music[song]
        webbrowser.open(link)
    elif "tell me news" in c.lower():
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={newsapi}")
        if r.status_code == 200:
            data = r.json()  # Corrected variable name
            articles = data.get("articles", [])
            if articles:
                speak("Here are the latest news headlines.")
                for article in articles[:5]: 
                    speak(article['title'])
            else:
                speak("Sorry, I couldn't find any news at the moment.")
        else:
            speak("Sorry, I am unable to fetch news right now.")
    elif "tell me weather" in c.lower():
        api_key = "a93488f223194895ac045648250402" 
        city = "Lahore"  
        url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={city}&aqi=no"
        response = requests.get(url)
        if response.status_code == 200:
            weather_data = response.json()
            temp = weather_data["current"]["temp_c"]
            description = weather_data["current"]["condition"]["text"]
            speak(f"The current temperature in {city} is {temp} degrees Celsius with {description}.")

    else:
        aiprocess(c)
        speak(output)
        #let openai handle the request
        pass
        
if __name__ == "__main__":
    while True:
        #listen for the word "jarvis" only 
        r = sr.Recognizer()
        print("Listening...")
                   
        # recognize speech using Sphinx
        try:
            with sr.Microphone() as source:
                print("Recognizing...")
                audio = r.listen(source, timeout=2,phrase_time_limit=2)
            word = r.recognize_google(audio)
            if(word.lower()== "orion"):
                speak("Ya")
                #listen for command
                with sr.Microphone() as source:
                    print("Orion Active...")
                    audio = r.listen(source)
                    command = r.recognize_google(audio)
                    processcommand(command)
        except Exception as e:
            print("Error; {0}".format(e))
# AIzaSyBX6r9tX8Kmsjph68lmb1uD8FU8FD9rSNE
