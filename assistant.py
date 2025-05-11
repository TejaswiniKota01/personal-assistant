import pyttsx3
import speech_recognition as sr
import wikipedia
import datetime
import pyjokes
import psutil
import webbrowser
import streamlit as st

# Initialize Text-to-Speech Engine
engine = pyttsx3.init()
todo_list = []  # Global to-do list

def speak(text):
    print("Assistant:", text)
    engine.say(text)
    engine.runAndWait()

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

def open_website(website):
    # Check if the user has typed a simple domain name like 'youtube'
    if not website.startswith('http://') and not website.startswith('https://'):
        if '.' in website:  # Looks like a domain (e.g., youtube.com)
            website = 'https://' + website
        else:
            website = 'https://www.' + website + '.com'  # Adding 'www' and '.com' to basic domains

    try:
        webbrowser.open(website)
        speak(f"Opening {website}")
    except Exception as e:
        speak(f"Sorry, I couldn't open the website. Error: {str(e)}")

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

def clear_tasks():
    todo_list.clear()
    return "All tasks have been cleared."

def run_assistant(command):
    if "search" in command:
        query = command.replace("search", "").strip()
        return search_wikipedia(query)
    elif "time" in command:
        return tell_time()
    elif "open" in command:
        website = command.replace("open", "").strip()
        return open_website(website)
    elif "calculate" in command or any(op in command for op in ['+', '-', '*', '/']):
        return basic_calculator(command)
    elif "joke" in command:
        return tell_joke()
    elif "battery" in command:
        return check_battery()
    elif "note" in command:
        note = command.replace("note", "").strip()
        return add_to_notes(note)
    elif "add task" in command:
        task = command.replace("add task", "").strip()
        return add_task(task)
    elif "show task" in command:
        return show_tasks()
    elif "clear tasks" in command:
        return clear_tasks()
    else:
        return "I'm sorry, I didn't understand that command."

# Streamlit Interface
def chat():
    st.title("Personal Assistant")
    st.write("Hello! I am your personal assistant. How can I help you today?")
    
    # Text input for the user to type a command
    user_input = st.text_input("You: ", "")

    if user_input:
        response = run_assistant(user_input.lower())
        st.write(f"Assistant: {response}")

    # Displaying the current tasks in the todo list
    if todo_list:
        st.write("### Current Tasks:")
        for idx, task in enumerate(todo_list, 1):
            st.write(f"{idx}. {task}")

if __name__ == "__main__":
    chat()
