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
import smtplib
from email.mime.text import MIMEText
import re

# Initialize session states
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'todo_list' not in st.session_state:
    st.session_state.todo_list = []

# Speak (Optional, for local use)
def speak(text):
    tts = gTTS(text=text, lang='en')
    tts.save("temp.mp3")
    os.system("start temp.mp3")  # Use 'start' for Windows


def search_wikipedia(query):
    query = " ".join(query.split())  # Normalize spaces in the query
    try:
        search_results = wikipedia.search(query)
        if not search_results:
            return "Sorry, no Wikipedia page matches your query."
        # Try first result title
        for title in search_results:
            try:
                summary = wikipedia.summary(title, sentences=2)
                return summary
            except wikipedia.exceptions.DisambiguationError as e:
                # If disambiguation page, try next option
                continue
            except wikipedia.exceptions.PageError:
                continue
        return "Sorry, no Wikipedia page matches your query."
    except Exception as e:
        return f"An error occurred: {str(e)}"



def tell_time():
    now = datetime.datetime.now()
    return "The current time is " + now.strftime("%I:%M %p")


def tell_date():
    today = datetime.date.today()
    return "Today's date is " + today.strftime("%B %d, %Y")


def open_website(website):
    if not website.startswith('http://') and not website.startswith('https://'):
        website = f"https://{website}" if '.' in website else f"https://www.{website}.com"
    webbrowser.open(website)
    return f"Opening {website}"


def google_search(query):
    url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
    webbrowser.open(url)
    return f"Searching Google for: {query}"


def play_youtube(query):
    try:
        kit.playonyt(query)
        return f"Playing {query} on YouTube."
    except Exception as e:
        return f"Could not play the video: {str(e)}"


def basic_calculator(command):
    try:
        expression = command.replace("calculate", "").strip()
        result = eval(expression)
        return f"The result is {result}."
    except Exception:
        return "Sorry, I couldn't calculate that."


def tell_joke():
    return pyjokes.get_joke()


def check_battery():
    battery = psutil.sensors_battery()
    return f"Battery is at {battery.percent}%."


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
        progress_bar = st.progress(0)
        timer_text = st.empty()

        for i in range(seconds):
            timer_text.text(f"Timer: {seconds - i} seconds remaining...")
            progress_bar.progress((i + 1) / seconds)
            time.sleep(1)

        timer_text.text("Timer completed!")
        return f"Timer for {seconds} seconds completed!"
    except ValueError:
        return "Please provide time in seconds."


def add_task(task):
    st.session_state.todo_list.append(task)
    return f"Task added: {task}"


def show_tasks():
    if not st.session_state.todo_list:
        return "You have no tasks."
    else:
        return "\n".join([f"{i + 1}. {task}" for i, task in enumerate(st.session_state.todo_list)])


def remove_task(task_number):
    try:
        index = int(task_number) - 1
        if 0 <= index < len(st.session_state.todo_list):
            removed = st.session_state.todo_list.pop(index)
            return f"Removed task: {removed}"
        else:
            return "Invalid task number."
    except ValueError:
        return "Provide a valid task number."


def clear_tasks():
    st.session_state.todo_list.clear()
    return "All tasks cleared."


def send_email(receiver_email, subject, message):
    from_email = "kotatejaswini0106@gmail.com"
    app_password = "ojepedhyhkfqfiyj"
    try:
        msg = MIMEText(message)
        msg['Subject'] = subject
        msg['From'] = from_email
        msg['To'] = receiver_email

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(from_email, app_password)
            server.send_message(msg)

        return f"Email sent to {receiver_email}."
    except Exception as e:
        return f"Failed to send email: {str(e)}"


def run_assistant(command):
    command = command.lower()
    if "search" in command:
        # Clean the query properly by removing the word 'search' and extra spaces
        query = re.sub(r'\bsearch\b', '', command).strip()
        return search_wikipedia(query)
    elif "timer" in command:
        return start_timer(re.sub(r'\btimer\b', '', command).strip())
    elif "time" in command:
        return tell_time()
    elif "date" in command:
        return tell_date()
    elif "open" in command:
        return open_website(re.sub(r'\bopen\b', '', command).strip())
    elif "google" in command:
        return google_search(re.sub(r'\bgoogle\b', '', command).strip())
    elif "play" in command:
        return play_youtube(re.sub(r'\bplay\b', '', command).strip())
    elif "calculate" in command or any(op in command for op in ['+', '-', '*', '/']):
        return basic_calculator(command)
    elif "joke" in command:
        return tell_joke()
    elif "battery" in command:
        return check_battery()
    elif "note" in command:
        return add_to_notes(re.sub(r'\bnote\b', '', command).strip())
    elif "remind me" in command:
        return set_reminder(re.sub(r'remind me', '', command).strip())
    elif "timer" in command:
        return start_timer(re.sub(r'\btimer\b', '', command).strip())
    elif "add task" in command:
        return add_task(re.sub(r'add task', '', command).strip())
    elif "show task" in command:
        return show_tasks()
    elif "remove task" in command:
        return remove_task(re.sub(r'remove task', '', command).strip())
    elif "clear tasks" in command:
        return clear_tasks()
    elif "send email" in command:
        return "Use the sidebar to send an email."
    else:
        return "Sorry, I didn't understand that."


# Streamlit app UI
def chat():
    st.title("Personal Assistant")

    user_input = st.text_input("You:", "")

    if user_input:
        response = run_assistant(user_input)
        st.session_state.chat_history.append(("You", user_input))
        st.session_state.chat_history.append(("Assistant", response))
        st.write(f"Assistant: {response}")

    if st.session_state.chat_history:
        st.write("### Chat History")
        for role, message in st.session_state.chat_history:
            st.write(f"{role}: {message}")

    if st.session_state.todo_list:
        st.write("### Your Tasks:")
        for i, task in enumerate(st.session_state.todo_list, 1):
            st.write(f"{i}. {task}")

    st.sidebar.title("Send an Email")
    with st.sidebar.form("email_form"):
        receiver = st.text_input("Recipient Email")
        subject = st.text_input("Subject")
        body = st.text_area("Message")
        send_btn = st.form_submit_button("Send")

        if send_btn:
            result = send_email(receiver, subject, body)
            st.sidebar.success(result)


if __name__ == "__main__":
    chat()
