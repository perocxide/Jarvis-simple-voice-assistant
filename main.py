import speech_recognition as sr
import webbrowser as web
import pyttsx3 as pyt
import musiclibrary
import gc
import time

# Allow the system to stabilize before starting the program
time.sleep(1)

recognizer = sr.Recognizer()
engine = pyt.init()

def speak(text):
    """Convert text to speech."""
    engine.say(text)
    engine.runAndWait()
    
    # Collect garbage after text-to-speech to free memory
gc.collect()

def listen():
    """Listen for audio and return recognized text."""
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)  # Reduce background noise
        try:
            audio = recognizer.listen(source, timeout=3, phrase_time_limit=3)
            print("recognizing...")
            command = recognizer.recognize_google(audio).lower()
            print("Jarvis is active now")
            if "jarvis" in command:
                speak("Yes?")
                # Short sleep to prevent unnecessary CPU load after recognition
                time.sleep(1)
                return command
            return ""
        except sr.RequestError:
            print("Trouble connecting to the internet or API request error")
            return ""
        except sr.UnknownValueError:
            speak("Sorry, I didn't understand that.")
            return ""  # No speech detected
        except Exception as e:
            print(f"Error: {e}")
            return ""

def commandExecution(command):
    """Execute actions based on voice commands."""
    command = command.strip()

    if "terminate" in command:  # Termination condition
        print("It was nice assisting you, JARVIS signing off. Goodbye!")
        speak("It was nice assisting you, JARVIS signing off. Goodbye!")
        exit()

    if "open google" in command:
        web.open("https://google.com")
        speak("Opening Google.")
    
    elif "open youtube" in command:
        web.open("https://youtube.com")
        speak("Opening YouTube.")
    
    elif command.startswith("play"):
        words = command.split(" ")
        if len(words) > 1:  # Check if a song name is provided
            song = " ".join(words[1:])  # Get the full song name
            link = musiclibrary.music.get(song, None)
            
            if link:
                web.open(link)
                speak(f"Playing {song}.")
            else:
                speak(f"Sorry, I couldn't find {song} in your music library.")
        else:
            speak("Please specify a song name.")
    else:
        speak("showing results that match")
        search_url = f"https://www.google.com/search?q={command.replace(' ', '+')}"  # Correct Google search URL format
        web.open(search_url)

    
    # Garbage collection after executing a command to free up memory
gc.collect()
    
    # Short delay to prevent excessive CPU usage after executing a command
time.sleep(1)

if __name__ == "__main__":
    speak("This is Jarvis, signing in.")
    speak("How can I help you?")

    while True:
        # Run garbage collection periodically in the loop to free memory
        gc.collect()
        
        command = listen()
        
        if not command:
            print("Waiting for command...")
            # Reduce CPU load while waiting for a command
            time.sleep(1)
            continue
        
        else:
            command = command.replace("jarvis", "").strip()
            commandExecution(command)
