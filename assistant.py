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

# Global to-do list
todo_list = []

# Initialize chat history in Streamlit session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# Speak function to output audio responses
def speak(text):
    tts = gTTS(text=text, lang='en')
    tts.save("temp.mp3")
    os.system("mpg321 temp.mp3")

# ... [All your existing functions remain unchanged here] ...

# 📧 Email sending function with fixed sender email and app password
def send_email(receiver_email, subject, message):
    from_email = "kotatejaswini0106@gmail.com"
    app_password = "ojepedhyhkfqfiyj"  # Use the exact app password without spaces
               # Your app password (no spaces)

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
        return f"Failed to send email. Error: {str(e)}"

# Command handler unchanged except removing 'send email' from command handling
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
    elif "send email" in command:
        return "To send an email, please use the Streamlit sidebar form."
    else:
        return "I'm sorry, I didn't understand that command."

# Streamlit UI
def chat():
    st.title("Personal Assistant")
    st.write("Hello! I am your personal assistant. How can I help you today?")

    user_input = st.text_input("You: ", "")

    if user_input:
        response = run_assistant(user_input.lower())
        st.session_state.chat_history.append(("You", user_input))
        st.session_state.chat_history.append(("Assistant", response))
        st.write(f"Assistant: {response}")

    if st.session_state.chat_history:
        st.write("### Chat History")
        for role, message in st.session_state.chat_history:
            st.write(f"{role}: {message}")

    if todo_list:
        st.write("### Current Tasks:")
        for idx, task in enumerate(todo_list, 1):
            st.write(f"{idx}. {task}")

    st.sidebar.title("Send an Email")
    with st.sidebar.form("email_form"):
        receiver = st.text_input("Recipient Email")
        subject = st.text_input("Subject")
        body = st.text_area("Message")
        send_btn = st.form_submit_button("Send")

        if send_btn:
            if receiver and subject and body:
                result = send_email(receiver, subject, body)
                st.sidebar.success(result)
            else:
                st.sidebar.error("Please fill all the fields.")

if __name__ == "__main__":
    chat()
