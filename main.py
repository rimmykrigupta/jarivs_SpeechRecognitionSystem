import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
import requests
from openai import OpenAI
from gtts import gTTS
import pygame
import os

# Initialize recognizer and text-to-speech engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()
newsapi="69f70b98655043b890c873e89115cbef"

def speak(text):
    """Function to make the text-to-speech engine say the given text using gTTS and Pygame."""
    try:
        # Convert text to speech using gTTS and save it as an MP3 file
        tts = gTTS(text)
        tts.save('temp.mp3')

        # Initialize Pygame
        pygame.init()

        # Try initializing the mixer
        try:
            pygame.mixer.quit()  # Quit any existing mixers
            pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=4096)
        except pygame.error as e:
            print(f"Pygame mixer initialization failed: {e}")
            return

        # Load the MP3 file
        pygame.mixer.music.load("temp.mp3")

        # Play the MP3 file
        pygame.mixer.music.play()

        # Keep the program running until the music stops playing
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

        # Clean up after playing
        pygame.mixer.music.unload()
        os.remove("temp.mp3")
    
    except pygame.error as e:
        print(f"Pygame error: {e}")
    except Exception as e:
        print(f"An error occurred in the speak function: {e}")

def aiProcess(command):
    try:
        client = OpenAI(
            api_key="sk-b42nysr4Y8iNheTQTbOtkqJY13tXykQcvkU4JFKthoT3BlbkFJgK7Og00sbKMtioHCbudAzJZUoIQpAf7RFnNi8TgPoA",
        )
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a virtual assistant named Jarvis skilled in general tasks like Alexa and Google Cloud. Give short responses, please."},
                {"role": "user", "content": command}
            ]
        )
        return completion.choices[0].message['content']
    except Exception as e:
        print(f"Error with OpenAI API: {e}")
        return "Sorry, I couldn't process your request."

def processCommand(c):
    if "open google" in c.lower():
        webbrowser.open("https://google.com")
    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")
    elif "open facebook" in c.lower():
        webbrowser.open("https://facebook.com")
    elif "open linkedin" in c.lower():
        webbrowser.open("https://linkedin.com")
    elif c.lower().startswith("play"):
        song = c.lower().split(" ", 1)[1]
        link = musicLibrary.music.get(song, "")
        if link:
            webbrowser.open(link)
        else:
            speak("Song not found in the music library.")
    elif "news" in c.lower():
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={newsapi}")
        if r.status_code == 200:
            data = r.json()
            articles = data.get('articles', [])
            for article in articles:
                speak(article['title'])
        else:
            speak("Failed to retrieve news. Please try again later.")
    else:
        output = aiProcess(c)
        speak(output)

if __name__ == "__main__":
    # Announce that Jarvis is initializing
    speak("Initializing Jarvis......")
    while True:
        try:
            with sr.Microphone() as source:
                print("Listening for 'Jarvis'...")
                audio = recognizer.listen(source, timeout=3, phrase_time_limit=5)
                word = recognizer.recognize_google(audio)
                if word.lower() == "jarvis":
                    speak("Yes, I can Listen you .")
                    with sr.Microphone() as source:
                        print("Jarvis Active...")
                        audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
                        command = recognizer.recognize_google(audio)
                        processCommand(command)
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand the audio.")
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
        except Exception as e:
            print(f"Error: {e}")
