##PERSONAL ASSISTANT (Python)

A Python-based interactive personal assistant designed to perform a wide variety of tasks using natural language text commands. This assistant is built using rule-based logic and third-party APIs—not a Large Language Model (LLM) like ChatGPT. It focuses on functionality, productivity, and utility using lightweight libraries and predefined command patterns.


#Key Highlights

Not AI or ML-based — instead of learning or generating language, it uses predefined patterns to understand and execute commands.
Integrates multiple APIs and Python libraries (e.g., Wikipedia, PyDictionary, pyjokes, etc.) for rich and diverse features.
Ideal for beginners or developers looking to build assistant tools without the complexity of training models.
Runs locally — no internet-dependent backend or external AI API integration (except for online features like Google search or YouTube).
Offers hands-on experience with modules like nltk, psutil, pywhatkit, and more.


🚀 FEATURES
📚 General Knowledge
•	- search <query> – Search Wikipedia
•	- google <query> – Google Search
•	- play <query> – Play a YouTube video
•	- quote / inspire me – Show an inspirational quote
•	- joke – Tell a random joke
📏 Utilities
•	- time – Show current time
•	- date – Show today's date
•	- battery – Show battery status
•	- calculate <expression> – Evaluate mathematical expression
•	- timer <seconds> – Set a countdown timer
📝 Notes & Reminders
•	- note <text> – Add a note
•	- remind me <text> – Set a reminder
✅ Task Management
•	- add task <task> – Add a new task
•	- show task – Show all tasks
•	- remove task <number> – Remove a specific task
•	- clear tasks – Clear all tasks
📖 Dictionary
•	- meaning of <word> – Get meaning of the word
•	- synonym of <word> – Get synonyms
•	- antonym of <word> – Get antonyms
🌐 Web Utilities
•	- open <website> – Open a website (e.g., github.com)
•	- send email – Use sidebar to send email
🎲 Fun & Games
•	- roll a dice – Roll a six-sided dice
•	- flip a coin – Flip a coin (Heads/Tails)
•	- guess a number – Play number guessing game (if implemented)
⏲ Productivity
•	- start pomodoro – Start 25-min work session + 5-min break
•	- summary – Show today's time, tasks, notes, and reminders
💬 Small Talk
•	- hi / hello / hey
•	- how are you
•	- bye / goodnight / see you



🔧 SETUP INSTRUCTIONS

1. Clone the Repository:
   > git clone https://github.com/TejaswiniKota01/personal-assistant.git
   > cd personal-assistant

2. Create a Virtual Environment (optional):
   > python -m venv venv
   > venv\Scripts\activate  (Windows)

3. Install Dependencies:
   > pip install -r requirements.txt

4. Download NLTK Data (Run in Python shell):
   > import nltk
   > nltk.download('wordnet')
   > nltk.download('omw-1.4')

5. Run the Assistant:
   > python assistant.py


📁 PROJECT STRUCTURE
•	- assistant.py : Main assistant logic
•	- requirements.txt : Required Python packages
•	- README.docx : Project instructions (this file)


📦 DEPENDENCIES USED
•	- nltk
•	- wikipedia
•	- pyjokes
•	- psutil
•	- pywhatkit
•	- streamlit
•	- youtubesearchpython
•	- gtts
•	- speechrecognition
•	- pyaudio
•	- requests
•	- PyDictionary

