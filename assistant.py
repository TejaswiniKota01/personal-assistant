import os
import wikipedia
import datetime
import pyjokes
import psutil
import webbrowser
from nltk.corpus import wordnet
import nltk
import streamlit as st
import time
import pywhatkit as kit
from PyDictionary import PyDictionary
from youtubesearchpython import VideosSearch
import smtplib
import random
import re
import requests 
from email.mime.text import MIMEText


dictionary = PyDictionary()

# Initialize session states
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'todo_list' not in st.session_state:
    st.session_state.todo_list = []
if 'reminders' not in st.session_state:
    st.session_state.reminders = []
if 'notes' not in st.session_state:
    st.session_state.notes = []



def show_help():
    return """Here are some commands you can try:

General Knowledge:
- search <query>          : Search Wikipedia
- google <query>          : Google search
- play <query>            : Play YouTube video
- joke                    : Tell a joke
- quote / inspire me      : Show an inspirational quote

Utilities:
- time                    : Get current time
- date                    : Get today's date
- battery                 : Check battery status
- calculate <expression>  : Calculate math expression
- timer <seconds>         : Start a timer

Notes & Reminders:
- note <text>             : Add a note
- remind me <text>        : Set a reminder

Task Management:
- add task <task>         : Add a task
- show task               : Show all tasks
- remove task <number>    : Remove a specific task
- clear tasks             : Clear all tasks

Email:
- send email              : Use sidebar to send an email

Websites:
- open <website>          : Open a website (e.g., open github)

Unit Conversion:
- <value> cm to inches    : Convert cm to inches
- <value> inches to cm    : Convert inches to cm

Small Talk & Greetings:
- hi / hello / hey
- how are you
- what's up
- bye / goodnight / see you

- start pomodoro          : Begin a 25-minute Pomodoro session followed by a 5-minute break

- summary                 : Show daily summary (time, tasks, reminders, notes)

- roll a dice             : Simulate rolling a six-sided dice
- flip a coin             : Simulate flipping a coin

-Dictionary & Language:
- meaning of <word>       : Get meaning/definitions of a word
- synonym of <word>       : Get synonyms of a word
- antonym of <word>       : Get antonyms of a word


Help:
- help / commands / what can you do  : Show this help message
"""




from nltk.corpus import wordnet

def get_meaning(word):
    synsets = wordnet.synsets(word)
    if synsets:
        meanings = [syn.definition() for syn in synsets[:3]]
        return "\n".join(meanings)
    else:
        return f"No meaning found for '{word}'."


# Function to get synonyms
def get_synonyms(word):
    synonyms = set()
    for syn in wordnet.synsets(word):
        for lemma in syn.lemmas():
            synonyms.add(lemma.name().replace("_", " "))
    if synonyms:
        return f"Synonyms of '{word}': " + ", ".join(sorted(synonyms)[:10])
    else:
        return f"No synonyms found for '{word}'."

# Function to get antonyms
def get_antonyms(word):
    antonyms = set()
    for syn in wordnet.synsets(word):
        for lemma in syn.lemmas():
            for ant in lemma.antonyms():
                antonyms.add(ant.name().replace("_", " "))
    if antonyms:
        return f"Antonyms of '{word}': " + ", ".join(sorted(antonyms))
    else:
        return f"No antonyms found for '{word}'."

    

# Wikipedia search
def search_wikipedia(query):
    try:
        result = wikipedia.summary(query, sentences=1)
        return result
    except wikipedia.exceptions.DisambiguationError:
        return "I found multiple results. Please be more specific."
    except wikipedia.exceptions.HTTPTimeoutError:
        return "The Wikipedia service is currently unavailable. Please try again later."
def get_quote():
    try:
        response = requests.get("https://api.quotable.io/random")
        data = response.json()
        return f"Quote: \"{data['content']}\" — {data['author']}"
    except Exception as e:
        return f"Could not fetch quote. Error: {str(e)}"

def start_pomodoro():
    work_duration = 25 * 60  # 25 minutes
    break_duration = 5 * 60  # 5 minutes

    st.success("Pomodoro started! Focus for 25 minutes.")
    work_bar = st.progress(0)
    work_text = st.empty()

    for i in range(work_duration):
        remaining = work_duration - i
        mins, secs = divmod(remaining, 60)
        work_text.text(f"Work Time: {mins:02d}:{secs:02d} remaining")
        work_bar.progress((i + 1) / work_duration)
        time.sleep(1)

    work_text.text("Work session complete! Time for a 5-minute break.")
    st.balloons()

    break_bar = st.progress(0)
    break_text = st.empty()

    for i in range(break_duration):
        remaining = break_duration - i
        mins, secs = divmod(remaining, 60)
        break_text.text(f"Break Time: {mins:02d}:{secs:02d} remaining")
        break_bar.progress((i + 1) / break_duration)
        time.sleep(1)

    break_text.text("🎉 Break complete! Ready for your next Pomodoro session?")
    return "Pomodoro session completed!"


def roll_dice():
    return f"🎲 You rolled a {random.randint(1, 6)}."


def flip_coin():
    return f"🪙 It's {'Heads' if random.choice([True, False]) else 'Tails'}."




def unit_conversion(command):
    # Convert cm to inches
    if "cm to inches" in command:
        try:
            value = float(command.split("cm to inches")[-1].strip())
            inches = value / 2.54
            return f"{value} cm is {inches:.2f} inches."
        except:
            return "Please provide a valid number for conversion."
    # Convert inches to cm
    elif "inches to cm" in command:
        try:
            value = float(command.split("inches to cm")[-1].strip())
            cm = value * 2.54
            return f"{value} inches is {cm:.2f} cm."
        except:
            return "Please provide a valid number for conversion."
    return None

def small_talk(command):
    command = command.lower()
    greetings = ['hi', 'hello', 'hey', 'good morning', 'good afternoon', 'good evening']
    how_are_you = ['how are you', 'how r u', 'how do you do', 'how is it going', 'how are things']
    farewells = ['bye', 'goodbye', 'see you', 'talk to you later']
    thanks = ['thank you', 'thanks', 'thx', 'thank u']

    if any(greet in command for greet in greetings):
        return "Hello! How can I assist you today?"
    elif any(phrase in command for phrase in how_are_you):
        return "I'm just a program, but I'm here to help you! How can I assist?"
    elif any(farewell in command for farewell in farewells):
        return "Goodbye! Have a great day!"
    elif any(thank in command for thank in thanks):
        return "You're welcome! If you need anything else, just ask."
    elif "what is your name" in command or "who are you" in command:
        return "I'm your personal assistant. How can I help you?"
    elif "thank" in command:
        return "You're welcome!"
    return None



def tell_time():
    now = datetime.datetime.now()
    return "The current time is " + now.strftime("%I:%M %p")

def tell_date():
    today = datetime.date.today()
    return "Today's date is " + today.strftime("%B %d, %Y")

def open_website(website):
    if not website.startswith('http://') and not website.startswith('https://'):
        website = f"https://{website}" if '.' in website else f"https://www.{website}.com"
    try:
        webbrowser.open(website)
        return f"Opening {website}"
    except Exception as e:
        return f"Sorry, I couldn't open the website. Error: {str(e)}"

def google_search(query):
    url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
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
    except Exception:
        return "Sorry, I couldn't calculate that."

def tell_joke():
    return pyjokes.get_joke()

def check_battery():
    battery = psutil.sensors_battery()
    if battery:
        return f"Your battery is at {battery.percent}%."
    else:
        return "Cannot retrieve battery information."

def add_to_notes(note):
    st.session_state.notes.append(note)
    with open("notes.txt", "a") as file:
        file.write(note + "\n")
    return "Note saved."

def set_reminder(reminder_text):
    st.session_state.reminders.append(reminder_text)
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

def get_summary():
    time_now = tell_time()
    tasks = show_tasks()
    reminders = "\n".join(st.session_state.reminders) if st.session_state.reminders else "No reminders."
    notes = "\n".join(st.session_state.notes) if st.session_state.notes else "No notes."
    return f"{time_now}\n\nTasks:\n{tasks}\n\nReminders:\n{reminders}\n\nNotes:\n{notes}"



def run_assistant(command):
    import re
    import random

    command = command.lower().strip()

    # Small talk
    small_talk_response = small_talk(command)
    if small_talk_response:
        return small_talk_response

    # Help / commands
    if command in ["help", "commands", "what can you do"]:
        return show_help()

    # Quotes
    if "quote" in command or "inspire me" in command:
        quotes = [
            "The best way to predict the future is to invent it. – Alan Kay",
            "Success is not the key to happiness. Happiness is the key to success. – Albert Schweitzer",
            "Do something today that your future self will thank you for.",
            "Your time is limited, so don’t waste it living someone else’s life. – Steve Jobs"
        ]
        return random.choice(quotes)

    # Dictionary
    if command.startswith("meaning of "):
        word = command.replace("meaning of ", "").strip()
        return get_meaning(word)

    elif command.startswith("synonym of "):
        word = command.replace("synonym of ", "").strip()
        return get_synonyms(word)

    elif command.startswith("antonym of "):
        word = command.replace("antonym of ", "").strip()
        return get_antonyms(word)

    # Dice & coin
    elif "roll dice" in command or "roll a dice" in command:
        return roll_dice()

    elif "flip coin" in command or "flip a coin" in command:
        return flip_coin()

    # Unit conversion
    if "cm to inches" in command:
        match = re.search(r'(\d+\.?\d*)\s*cm', command)
        if match:
            cm = float(match.group(1))
            inches = cm / 2.54
            return f"{cm} cm is {round(inches, 2)} inches."

    elif "inches to cm" in command or "inch to cm" in command:
        match = re.search(r'(\d+\.?\d*)\s*inch', command)
        if match:
            inch = float(match.group(1))
            cm = inch * 2.54
            return f"{inch} inches is {round(cm, 2)} cm."

    # Knowledge
    if "search" in command:
        query = command.replace("search", "").strip()
        return search_wikipedia(query)

    elif "google" in command:
        query = command.replace("google", "").strip()
        return google_search(query)

    elif "play" in command:
        query = command.replace("play", "").strip()
        return play_youtube(query)

    # Utilities
    elif "time" in command:
        return tell_time()

    elif "date" in command:
        return tell_date()

    elif "calculate" in command or any(op in command for op in ['+', '-', '*', '/']):
        return basic_calculator(command)

    elif "joke" in command:
        return tell_joke()

    elif "battery" in command:
        return check_battery()

    elif "timer" in command:
        seconds = command.replace("timer", "").strip()
        return start_timer(seconds)

    # Notes & reminders
    elif "note" in command:
        note = command.replace("note", "").strip()
        return add_to_notes(note)

    elif "remind me" in command:
        reminder = command.replace("remind me", "").strip()
        return set_reminder(reminder)

    # Tasks
    elif "add task" in command:
        return add_task(command.replace("add task", "").strip())

    elif "show task" in command:
        return show_tasks()

    elif "remove task" in command:
        return remove_task(command.replace("remove task", "").strip())

    elif "clear tasks" in command:
        return clear_tasks()

    # Email
    elif "send email" in command:
        return "Use the sidebar to send an email."

    # Websites
    elif "open" in command:
        website = command.replace("open", "").strip()
        return open_website(website)

    # Productivity
    elif command == "start pomodoro":
        return start_pomodoro()

    elif command == "summary":
        return get_summary()

    # Greetings
    elif command in ["hi", "hello", "hey"]:
        return "Hello! How can I assist you today?"

    elif command in ["how are you", "how are you?"]:
        return "I'm just a program, but thanks for asking! How can I help?"

    elif command in ["bye", "goodnight", "see you"]:
        return "Goodbye! Have a great day!"

    else:
        return "I'm sorry, I didn't understand that command."


def chat():
    st.title("Personal Assistant")
    st.write("Hello! I am your personal assistant. How can I help you today?")

    user_input = st.text_input("You: ", "")

    if user_input.strip():  # Only process if user input is not empty
        if "timer" in user_input.lower():
            seconds = user_input.lower().replace("timer", "").strip()
            try:
                seconds = int(seconds)
                progress_bar = st.progress(0)
                timer_text = st.empty()

                for i in range(seconds):
                    timer_text.text(f"Timer: {seconds - i} seconds remaining...")
                    progress_bar.progress((i + 1) / seconds)
                    time.sleep(1)

                timer_text.text("Timer completed!")
                response = f"Timer for {seconds} seconds completed!"
            except ValueError:
                response = "Please provide time in seconds."
        else:
            response = run_assistant(user_input.lower())

        st.session_state.chat_history.append(("You", user_input))
        st.session_state.chat_history.append(("Assistant", response))
        st.write(f"Assistant: {response}")

    # Show chat history only if at least one user input is present
    if st.session_state.chat_history and any(role == "You" and message.strip() != "" for role, message in st.session_state.chat_history):
        st.write("### Chat History")
        for role, message in st.session_state.chat_history:
            st.write(f"{role}: {message}")

    if st.session_state.todo_list:
        st.write("### Your Tasks:")
        for i, task in enumerate(st.session_state.todo_list, 1):
            st.write(f"{i}. {task}")

    if st.session_state.reminders:
        st.write("### Your Reminders:")
        for i, reminder in enumerate(st.session_state.reminders, 1):
            st.write(f"{i}. {reminder}")

    if st.session_state.notes:
        st.write("### Your Notes:")
        for i, note in enumerate(st.session_state.notes, 1):
            st.write(f"{i}. {note}")

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
