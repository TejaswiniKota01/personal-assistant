from gtts import gTTS
import os
import speech_recognition as sr
import wikipedia
import datetime
import pyjokes
import psutil
import webbrowser
import streamlit as st
import time
import pywhatkit as kit
from youtubesearchpython import VideosSearch

# Global to-do list
todo_list = []

def speak(text):
    tts = gTTS(text=text, lang='en')
    tts.save("temp.mp3")
    os.system("mpg321 temp.mp3")

def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.write("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        command = recognizer.recognize_google(audio)
        st.write("You said:", command)
        return command.lower()
    except sr.UnknownValueError:
        speak("Sorry, I did not understand that.")
        return ""

def search_wikipedia(query):
    try:
        result = wikipedia.summary(query, sentences=1)
        return result
    except wikipedia.exceptions.DisambiguationError:
        return "I found multiple results. Please be more specific."

def tell_time():
    now = datetime.datetime.now()
    return "The current time is " + now.strftime("%I:%M %p")

def tell_date():
    today = datetime.date.today()
    return "Today's date is " + today.strftime("%B %d, %Y")

def open_website(website):
    if not website.startswith('http://') and not website.startswith('https://'):
        if '.' in website:
            website = 'https://' + website
        else:
            website = 'https://www.' + website + '.com'
    try:
        webbrowser.open(website)
        speak(f"Opening {website}")
    except Exception as e:
        speak(f"Sorry, I couldn't open the website. Error: {str(e)}")

def google_search(query):
    url = "https://www.google.com/search?q=" + query.replace(" ", "+")
    webbrowser.open(url)
    return f"Searching Google for: {query}"

def play_youtube(query):
    try:
        kit.playonyt(query)
        return f"Playing {query} on YouTube."
    except Exception as e:
        return f"Sorry, could not play the video. Error: {str(e)}"

def basic_calculator(command):
    try:
        expression = command.replace("calculate", "").strip()
        result = eval(expression)
        return f"The result is {result}."
    except:
        return "Sorry, I couldn't calculate that."

def tell_joke():
    return pyjokes.get_joke()

def check_battery():
    battery = psutil.sensors_battery()
    return f"Your battery is at {battery.percent} percent."

def add_to_notes(note):
    with open("notes.txt", "a") as file:
        file.write(note + "\n")
    return "Note saved."

def set_reminder(reminder_text):
    with open("reminders.txt", "a") as f:
        f.write(reminder_text + "\n")
    return f"Reminder saved: {reminder_text}"

def start_timer(seconds):
    try:
        seconds = int(seconds)
        time.sleep(seconds)
        return f"Timer for {seconds} seconds completed!"
    except:
        return "Please provide time in seconds."

def add_task(task):
    if not task:
        return "Please specify the task."
    todo_list.append(task)
    return f"Task added: {task}"

def show_tasks():
    if not todo_list:
        return "You have no tasks."
    else:
        tasks = "Here are your tasks:\n"
        for idx, task in enumerate(todo_list, 1):
            tasks += f"{idx}. {task}\n"
        return tasks

def remove_task(task_number):
    try:
        index = int(task_number) - 1
        if 0 <= index < len(todo_list):
            removed = todo_list.pop(index)
            return f"Removed task: {removed}"
        else:
            return "Invalid task number."
    except ValueError:
        return "Please provide a valid task number."

def clear_tasks():
    todo_list.clear()
    return "All tasks have been cleared."

def run_assistant(command):
    if "search" in command:
        query = command.replace("search", "").strip()
        return search_wikipedia(query)
    elif "time" in command:
        return tell_time()
    elif "date" in command:
        return tell_date()
    elif "open" in command:
        website = command.replace("open", "").strip()
        return open_website(website)
    elif "google" in command:
        query = command.replace("google", "").strip()
        return google_search(query)
    elif "play" in command:
        query = command.replace("play", "").strip()
        return play_youtube(query)
    elif "calculate" in command or any(op in command for op in ['+', '-', '*', '/']):
        return basic_calculator(command)
    elif "joke" in command:
        return tell_joke()
    elif "battery" in command:
        return check_battery()
    elif "note" in command:
        note = command.replace("note", "").strip()
        return add_to_notes(note)
    elif "remind me" in command:
        reminder = command.replace("remind me", "").strip()
        return set_reminder(reminder)
    elif "timer" in command:
        seconds = command.replace("timer", "").strip()
        return start_timer(seconds)
    elif "add task" in command:
        task = command.replace("add task", "").strip()
        return add_task(task)
    elif "show task" in command:
        return show_tasks()
    elif "remove task" in command:
        number = command.replace("remove task", "").strip()
        return remove_task(number)
    elif "clear tasks" in command:
        return clear_tasks()
    else:
        return "I'm sorry, I didn't understand that command."

# Streamlit Interface
def chat():
    st.title("Personal Assistant")
    st.write("Hello! I am your personal assistant. How can I help you today?")

    user_input = st.text_input("You: ", "")

    if user_input:
        response = run_assistant(user_input.lower())
        st.write(f"Assistant: {response}")

    if todo_list:
        st.write("### Current Tasks:")
        for idx, task in enumerate(todo_list, 1):
            st.write(f"{idx}. {task}")

if __name__ == "__main__":
    chat()
