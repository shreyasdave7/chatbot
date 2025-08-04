import tkinter as tk
from tkinter import messagebox, scrolledtext
import nltk
from nltk.chat.util import Chat, reflections
import time
import threading

# Download required NLTK data
nltk.download('punkt')

# Chatbot configuration
BOT_NAME = "Aira"
pairs = [
    [r"(hi|hello|hey)", [f"Hello! I'm {BOT_NAME}. How can I assist you today?"]],
    [r"how are you\??", ["I'm doing great, thanks for asking!", "All systems operational. 😊"]],
    [r"what is your name\??", [f"My name is {BOT_NAME}, your virtual assistant."]],
    [r"who created you\??", ["I was created by Shreyas Dave."]],
    [r"what can you do\??", [
        "I can chat with you, answer simple questions, tell jokes, and keep you company!"
    ]],
    [r"tell me a joke", [
        "Why don't programmers like nature? It has too many bugs. 🐛",
        "Why did the computer get cold? It left its Windows open. 💻❄"
    ]],
    [r"what is python\??", [
        "Python is a high-level, interpreted programming language known for its simplicity and versatility."
    ]],
    [r"what is AI\??", [
        "AI stands for Artificial Intelligence, the simulation of human intelligence in machines."
    ]],
    [r"what is machine learning\??", [
        "Machine learning is a subset of AI that enables systems to learn from data and improve over time."
    ]],
    [r"what's your favorite language\??", [
        "Definitely Python! 🐍 It's clean and powerful."
    ]],
    [r"do you have feelings\??", [
        "I'm a bot, so I don't feel emotions like humans do, but I’m here to help you!"
    ]],
    [r"what's the time\??", [
        time.strftime("It's %I:%M %p right now."), 
        time.strftime("The current time is %H:%M.")
    ]],
    [r"what day is it\??", [
        time.strftime("Today is %A, %B %d, %Y.")
    ]],
    [r"bye|goodbye|see you", [
        "Goodbye! It was lovely chatting with you. 😊",
        "See you later! 👋"
    ]],
    [r"(.*)", [
        "Hmm, I didn't quite get that. Could you rephrase it?",
        "I'm still learning. Could you try asking that differently?"
    ]]
]

chatbot = Chat(pairs, reflections)

# --- Functions --- #
def send_message():
    user_input = user_entry.get().strip()
    if not user_input:
        return
    chat_area.config(state=tk.NORMAL)
    chat_area.insert(tk.END, f"You: {user_input}\n", "user")
    chat_area.config(state=tk.DISABLED)
    chat_area.yview(tk.END)
    user_entry.delete(0, tk.END)
    threading.Thread(target=bot_response, args=(user_input,), daemon=True).start()

def bot_response(user_input):
    time.sleep(0.4)
    response = chatbot.respond(user_input)
    chat_area.config(state=tk.NORMAL)
    chat_area.insert(tk.END, f"{BOT_NAME}: {response}\n", "bot")
    chat_area.config(state=tk.DISABLED)
    chat_area.yview(tk.END)

def clear_chat():
    if messagebox.askyesno("Clear Chat", "Are you sure you want to clear the conversation?"):
        chat_area.config(state=tk.NORMAL)
        chat_area.delete('1.0', tk.END)
        chat_area.config(state=tk.DISABLED)

def on_closing():
    if messagebox.askokcancel("Exit", "Do you really want to exit?"):
        root.destroy()

# --- GUI Setup --- #
root = tk.Tk()
root.title(f"{BOT_NAME} - AI Chat Assistant")
root.configure(bg="#e9f1f7")
root.geometry("600x640")
root.resizable(False, False)

# --- Chat Display Area --- #
chat_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=70, height=25, font=("Segoe UI", 11), bg="#ffffff", fg="#333")
chat_area.tag_config("user", foreground="#005b96", font=("Segoe UI", 11, "bold"))
chat_area.tag_config("bot", foreground="#2e8b57", font=("Segoe UI", 11))
chat_area.config(state=tk.DISABLED)
chat_area.pack(padx=10, pady=(10, 5), fill=tk.BOTH, expand=True)

# --- Entry and Buttons Frame --- #
input_frame = tk.Frame(root, bg="#e9f1f7")
input_frame.pack(pady=(0, 10), padx=10, fill=tk.X)

user_entry = tk.Entry(input_frame, font=("Segoe UI", 12), width=50, bd=2, relief=tk.GROOVE)
user_entry.pack(side=tk.LEFT, padx=(0, 10), ipady=6, expand=True, fill=tk.X)
user_entry.focus_set()
user_entry.bind("<Return>", lambda event: send_message())

def create_button(parent, text, command, bg, hover_bg):
    def on_enter(e): btn.config(bg=hover_bg)
    def on_leave(e): btn.config(bg=bg)
    btn = tk.Button(parent, text=text, command=command, bg=bg, fg="white", font=("Segoe UI", 10, "bold"), width=10, relief=tk.FLAT, cursor="hand2")
    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)
    btn.pack(side=tk.LEFT, padx=(0, 10))
    return btn

send_button = create_button(input_frame, "Send", send_message, "#4CAF50", "#45a049")
clear_button = create_button(input_frame, "Clear", clear_chat, "#f44336", "#e53935")

# --- Exit Protocol --- #
root.protocol("WM_DELETE_WINDOW", on_closing)

# --- Run GUI --- #
root.mainloop()