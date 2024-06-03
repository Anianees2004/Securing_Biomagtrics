import speech_recognition as sr 
import datetime
import subprocess
import pywhatkit
import pyttsx3

# Define a dictionary to store user credentials and roles
users = {
    "Anees": {"password": "password1", "role": "admin"},
    "Gopi": {"password": "password2", "role": "user"}
}

# Initialize text-to-speech engine
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
recognizer = sr.Recognizer()

# Function to perform authentication
def authenticate():
    while True:
        username = input("Enter username: ")
        password = input("Enter password: ")
        if username in users and users[username]["password"] == password:
            return users[username]["role"]
        else:
            print("Invalid credentials. Please try again.")

# Authenticate user before starting the voice assistant
user_role = authenticate()
if user_role:
    print("Authentication successful. Starting voice assistant...")
else:
    print("Authentication failed. Exiting...")
    exit()

# Function to handle voice commands based on user role
def cmd():
    with sr.Microphone() as source:
        print("Clearing background noises...Please wait")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        print('Ask me anything..')
        recordedaudio = recognizer.listen(source)
    try:
        text = recognizer.recognize_google(recordedaudio, language='en_US')
        text = text.lower()
        print('Your message:', format(text))

        if user_role == "admin":
            if 'chrome' in text:
                a = 'Opening chrome..'
                engine.say(a)
                engine.runAndWait()
                programName = "C:\Program Files\Google\Chrome\Application\chrome.exe"
                subprocess.Popen([programName])
            if 'time' in text:
                current_time = datetime.datetime.now().strftime('%I:%M %p')
                print(current_time)
                engine.say(current_time)
                engine.runAndWait()
            if 'play' in text:
                a = 'opening youtube..'
                engine.say(a)
                engine.runAndWait()
                pywhatkit.playonyt(text)
        elif user_role == "user":  # Limit permissions for users
            if 'time' in text:
                current_time = datetime.datetime.now().strftime('%I:%M %p')
                print(current_time)
                engine.say(current_time)
                engine.runAndWait()
            if 'play' in text:
                a = 'opening youtube..'
                engine.say(a)
                engine.runAndWait()
                pywhatkit.playonyt(text)
            else:
                print("Sorry, you don't have permission to perform this action.")
    except sr.UnknownValueError:
        print("Sorry, I couldn't understand that.")
    except sr.RequestError as e:
        print("Sorry, there was an error processing your request:", e)

# Execute voice assistant commands
while True:
    cmd()
