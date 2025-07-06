import datetime
import speech_recognition as sr
import wikipedia
import webbrowser
import pywhatkit
import pyttsx3
import os
import smtplib
import random
import json
import requests
import pyautogui
import time

# Initialize the text-to-speech engine
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
engine.setProperty('rate', 180)  # Adjust speaking rate

# Declare global variable for input method
current_input_method = '1'  # Default to voice

def speak(audio):
    """Function to make the assistant speak and also print the response"""
    print(f"Jarvis: {audio}")
    engine.say(audio)
    engine.runAndWait()

def wishMe():
    """Function to greet the user based on time of day"""
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Good Morning! Mister Ravi")
    elif hour >= 12 and hour < 18:
        speak("Good Afternoon! Mister Ravi")
    else:
        speak("Good Evening! Mister Ravi")
    speak("I am Jarvis. Please tell me how may I assist you.")

def takeVoiceCommand():
    """Function to take voice command from the user"""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("\nListening...")
        r.pause_threshold = 1
        r.energy_threshold = 300  # Adjust based on your microphone sensitivity
        audio = r.listen(source)
        
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"You said: {query}")
        return query.lower()
    except Exception as e:
        print("Say that again please...")
        return "None"

def takeTextCommand():
    """Function to take text command from the user"""
    query = input("\nEnter your command: ")
    print(f"You typed: {query}")
    return query.lower()

def get_weather(city):
    """Function to get weather information"""
    api_key = "YOUR_API_KEY"  # Replace with your OpenWeatherMap API key
    base_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    
    try:
        response = requests.get(base_url)
        data = response.json()
        
        if data["cod"] != "404":
            weather_info = data["main"]
            temperature = weather_info["temp"]
            humidity = weather_info["humidity"]
            weather_description = data["weather"][0]["description"]
            
            weather_report = f"The weather in {city} is {weather_description}. The temperature is {temperature} degrees Celsius, and the humidity is {humidity} percent."
            return weather_report
        else:
            return f"Sorry, I couldn't find weather information for {city}."
    except:
        return "I'm having trouble connecting to the weather service right now."

def send_email(to, content):
    """Function to send email"""
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        # You'll need to set up app password for your Google account
        server.login('your_email@gmail.com', 'your_app_password')
        server.sendmail('your_email@gmail.com', to, content)
        server.close()
        return True
    except Exception as e:
        print(e)
        return False

def take_screenshot():
    """Function to take a screenshot"""
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    screenshot_path = f"screenshot_{timestamp}.png"
    pyautogui.screenshot(screenshot_path)
    return screenshot_path

def get_news():
    """Function to get top news headlines"""
    api_key = "YOUR_API_KEY"  # Replace with your NewsAPI key
    url = f"https://newsapi.org/v2/top-headlines?country=in&apiKey={api_key}"
    
    try:
        response = requests.get(url)
        data = response.json()
        
        if data["status"] == "ok":
            articles = data["articles"][:5]  # Get top 5 news
            news_headlines = "Here are today's top headlines:\n"
            
            for i, article in enumerate(articles, 1):
                news_headlines += f"{i}. {article['title']}\n"
                
            return news_headlines
        else:
            return "Sorry, I couldn't fetch the news at the moment."
    except:
        return "I'm having trouble connecting to the news service right now."

def processCommand(query):
    """Function to process the command and execute appropriate action"""
    global current_input_method
    
    if 'wikipedia' in query:
        speak('Searching Wikipedia...')
        query = query.replace("wikipedia", "").strip()
        try:
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia")
            speak(results)
        except:
            speak("Sorry, I couldn't find information about that on Wikipedia.")
        
    elif 'open youtube' in query:
        speak("Opening YouTube")
        webbrowser.open("youtube.com")
        
    elif 'open google' in query:
        speak("Opening Google")
        webbrowser.open("google.com")
        
    elif 'open gmail' in query or 'open mail' in query:
        speak("Opening Gmail")
        webbrowser.open("gmail.com")
        
    elif 'time' in query:
        strTime = datetime.datetime.now().strftime("%H:%M:%S")
        speak(f"Sir, the time is {strTime}")
        
    elif 'date' in query:
        strDate = datetime.datetime.now().strftime("%d %B, %Y")
        speak(f"Today's date is {strDate}")
        
    elif 'play' in query:
        song = query.replace("play", "").strip()
        speak(f"Playing {song} on YouTube")
        pywhatkit.playonyt(song)
        
    elif 'weather' in query:
        speak("Which city would you like to know the weather for?")
        if current_input_method == '1':  # Voice
            city = takeVoiceCommand()
        else:  # Text
            city = takeTextCommand()
            
        if city != "None":
            weather_report = get_weather(city)
            speak(weather_report)
            
    elif 'send email' in query or 'send mail' in query:
        try:
            speak("Who should I send the email to?")
            if current_input_method == '1':  # Voice
                to = takeVoiceCommand()
            else:  # Text
                to = takeTextCommand()
                
            speak("What should I say in the email?")
            if current_input_method == '1':  # Voice
                content = takeVoiceCommand()
            else:  # Text
                content = takeTextCommand()
                
            if to != "None" and content != "None":
                if send_email(to, content):
                    speak("Email has been sent!")
                else:
                    speak("Sorry, I couldn't send the email.")
        except:
            speak("Sorry, I couldn't send the email.")
            
    elif 'screenshot' in query:
        speak("Taking screenshot...")
        screenshot_path = take_screenshot()
        speak(f"Screenshot saved as {screenshot_path}")
        
    elif 'news' in query:
        news = get_news()
        speak(news)
        
    elif 'joke' in query:
        jokes = [
            "Why don't scientists trust atoms? Because they make up everything!",
            "Did you hear about the mathematician who's afraid of negative numbers? He'll stop at nothing to avoid them!",
            "Why don't we tell secrets on a farm? Because the potatoes have eyes, the corn has ears, and the beans stalk.",
            "I told my wife she was drawing her eyebrows too high. She looked surprised.",
            "What do you call a fake noodle? An impasta!"
        ]
        joke = random.choice(jokes)
        speak(joke)
        
    elif 'open notepad' in query:
        speak("Opening Notepad")
        os.system("notepad")
        
    elif 'calculator' in query:
        speak("Opening Calculator")
        os.system("calc")
        
    elif 'change input' in query or 'switch input' in query:
        if current_input_method == '1':
            speak("Switching to text input")
            current_input_method = '2'
        else:
            speak("Switching to voice input")
            current_input_method = '1'
        
    elif 'quit' in query or 'bye' in query or 'exit' in query:
        speak("Goodbye Ravi! Have a nice day")
        return False
    
    # Handle general knowledge questions
    elif 'who is' in query or 'what is' in query or 'how to' in query:
        try:
            # Try to search Wikipedia for the answer
            results = wikipedia.summary(query, sentences=2)
            speak("Here's what I found")
            speak(results)
        except:
            speak("I'm sorry, I don't have information about that. Would you like me to search Google for you?")
            if current_input_method == '1':  # Voice
                response = takeVoiceCommand()
            else:  # Text
                response = takeTextCommand()
                
            if "yes" in response.lower():
                query = query.replace("search", "").strip()
                speak(f"Searching Google for {query}")
                pywhatkit.search(query)
    
    else:
        speak("I'm not sure how to help with that. You can ask me to search Wikipedia, open websites, play songs, check weather, take screenshots, or tell the time.")
    
    return True

if __name__ == "__main__":
    wishMe()
    running = True
    
    # Ask for input method at the beginning
    print("\nHow would you like to give commands?")
    print("1. Voice")
    print("2. Text")
    current_input_method = input("Enter 1 or 2: ")
    
    # Display commands guide
    print("\n=== JARVIS COMMAND GUIDE ===")
    print("• 'wikipedia [query]' - Search Wikipedia")
    print("• 'play [song name]' - Play a song on YouTube")
    print("• 'open youtube/google/gmail' - Open websites")
    print("• 'time' - Get current time")
    print("• 'date' - Get current date")
    print("• 'screenshot' - Take a screenshot")
    print("• 'joke' - Tell a joke")
    print("• 'open notepad/calculator' - Open applications")
    print("• 'who is/what is/how to [query]' - General knowledge questions")
    print("• 'change input' or 'switch input' - Switch between voice and text")
    print("• 'quit', 'bye', or 'exit' - End the session")
    print("=============================\n")
    
    while running:
        if current_input_method == '1':  # Voice
            query = takeVoiceCommand()
        else:  # Text
            query = takeTextCommand()
            
        if query != "None":
            running = processCommand(query)
