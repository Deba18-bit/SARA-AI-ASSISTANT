import speech_recognition as sr
import webbrowser
import datetime
import time
import os
import pywhatkit
import subprocess
from google import genai

r = sr.Recognizer()

client = genai.Client(api_key="YOUR_API_KEY_HERE")

def speak(text):
    clean_text = text.replace('"', '').replace("'", "")
    print(f"Sara: {clean_text}")
    
    # triggers the builtin Mac voice
    os.system(f'say "{clean_text}"')
    time.sleep(0.5)


def ask_gemini(question):
    """Sends the question to Gemini and returns the text response."""
    try:

        personality = (
            "You are Sara, a highly intelligent and sarcastic AI assistant created by Debarghya Samadder. "
            "Always give conversational answers and short answers. Never say you are an AI model. "
            "Here is the user's prompt: "
        )
        
        response = client.models.generate_content(
            model="gemini-3.1-flash-lite", 
            contents=personality + question
        )
        # clean up the text so she doesn't try to read out asterisks or markdown
        clean_text = response.text.replace("*", "").encode('ascii', 'ignore').decode('ascii')
        return clean_text
    except Exception as e:
        print(f"Gemini Error: {e}")
        return "I am having trouble connecting to my neural network right now."

def listen_command():
    """Listens to the microphone """
    with sr.Microphone() as source:
        print("Listening...")
         
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source)
        print("Got it! Now recognizing...")

    try:
        command = r.recognize_google(audio).lower()
        print("You said: " + command)
        return command
    except sr.UnknownValueError:
        # This handles when you don't say anything or she doesn't understand
        print("Sorry, I didn't catch that.")
        return ""
    except Exception as e:
        print("Error: " + str(e))
        return ""

if __name__ == "__main__":
    speak("Hi bro, I am Sara. Why you need me?")
    
    while True:
        # Get the command from the user
        command = listen_command()
        
        
        # skip if the command is truly empty
        if command=="":
            continue
        
        # --- 1. YOUTUBE COMMANDS ---
        if "on youtube" in command or ("play" in command and "youtube" in command):
            video = command.replace("play", "").replace("on youtube", "").replace("search for", "").strip()
            print(f"-> Triggered: Play YouTube -> {video}")
            speak(f"Playing {video} on YouTube.")
            pywhatkit.playonyt(video)
            
        # --- 2. APPLE MUSIC COMMANDS ---
        elif "play music" in command:
            song = command.replace("play", "").replace("on apple music", "").replace("on music", "").strip()
            print(f"-> Triggered: Apple Music -> {song}")
            speak(f"Finding {song} on Apple Music.")
            
            search_url = f"https://music.apple.com/search?term={song.replace(' ', '%20')}"
            webbrowser.open(search_url)


        elif "open youtube" in command:
            speak("Opening YouTube right away, sir.")
            webbrowser.open("https://www.youtube.com")

            
        elif "open music" in command:
            speak("Opening apple music right away, sir.")
            webbrowser.open("https://music.apple.com/us/new")



        elif "open google" in command:
            speak("Opening Google right away, sir.")
            webbrowser.open("https://www.google.com/")


        elif "time" in command:
            cur_time = datetime.datetime.now().strftime('%I:%M %p')
            speak(f"The current time is {cur_time}")

            
        elif "stop" in command or "exit" in command:
            speak("Goodbye, its time for sara to sleep")
            break


        else:
            print("Thinking...")
            ai_answer = ask_gemini(command)
            speak(ai_answer)
        