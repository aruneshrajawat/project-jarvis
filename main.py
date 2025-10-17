import speech_recognition as sr
import webbrowser
import pyttsx3
import requests
import time
import musiclibrary

# Initialize text-to-speech engine
engine = pyttsx3.init()

# Gemini Pro API key
GEMINI_API_KEY = "AIzaSyCb52Oq6d3gwnlX_nm_ZPIauoraY5uojnQ"
GEMINI_API_URL =  "https://generativelanguage.googleapis.com/v1beta2/models/gemini-1.5-turbo:generateText"

# News API key
newsapi = "705caaf6c57845bfa09f5e8872556e15"

# Function to speak text
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Gemini Pro AI processing using REST API
def aiProcess(command):
    headers = {
        "Authorization": f"Bearer {GEMINI_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "prompt": f"You are a virtual assistant named Jarvis. User: {command}",
        "maxOutputTokens": 300
    }

    try:
        response = requests.post(GEMINI_API_URL, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()
        # Gemini Pro response is in candidates[0]['output']
        return result['candidates'][0]['output']
    except Exception as e:
        print(f"AI Error: {e}")
        return "Sorry, I couldn't process that."

# Process user command
def processcommand(c):
    c_lower = c.lower()

    if "open google" in c_lower:
        webbrowser.open("https://google.com")
    elif "open facebook" in c_lower:
        webbrowser.open("https://facebook.com")
    elif "open youtube" in c_lower:
        webbrowser.open("https://youtube.com")
    elif "open linkedin" in c_lower:
        webbrowser.open("https://linkedin.com")
    elif c_lower.startswith("play"):
        song = c_lower.split(" ")[1]
        link = musiclibrary.music.get(song, "")
        if link:
            webbrowser.open(link)
        else:
            speak(f"Sorry, {song} not found in music library.")
    elif "news" in c_lower:
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={newsapi}")
        if r.status_code == 200:
            data = r.json()
            articles = data.get('articles', [])
            if not articles:
                speak("No news found.")
            for article in articles:
                speak(article['title'])
        else:
            speak("Sorry, I couldn't fetch the news.")
    else:
        output = aiProcess(c)
        speak(output)

# Main loop
if __name__ == "__main__":
    speak("Initializing Jarvis...")
    recognizer = sr.Recognizer()
    
    while True:
        try:
            with sr.Microphone() as source:
                print("Listening for wake word...")
                audio = recognizer.listen(source, timeout=6, phrase_time_limit=6)
            word = recognizer.recognize_google(audio)
            
            if word.lower() == "jarvis":
                speak("Yes?")
                time.sleep(0.5)
                
                with sr.Microphone() as source:
                    print("Jarvis Active...")
                    audio = recognizer.listen(source)
                    command = recognizer.recognize_google(audio)
                    processcommand(command)
        except Exception as e:
            print(f"Error: {e}")
