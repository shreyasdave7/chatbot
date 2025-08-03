from tkinter import *
from tkinter import messagebox, scrolledtext
import threading
import time
import nltk
import json
from nltk.chat.util import Chat, reflections

# Download NLTK punkt once
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

BOT_NAME = "Aira"

# Load chat data from JSON
def load_chat_data(file_path="chat_data.json"):
    try:
        with open(file_path, "r") as file:
            data = json.load(file)
            return [[entry["pattern"], entry["responses"]] for entry in data]
    except Exception as e:
        print(f"Error loading chat data: {e}")
        return []

pairs = load_chat_data()
chatbot = Chat(pairs, reflections)

# GUI Application
class ChatbotApp:
    def __init__(self, root):
        self.root = root
        self.root.title(f"{BOT_NAME} - Chat Assistant")
        self.root.geometry("700x600")
        self.root.configure(bg="#e0f7fa")

        self.build_widgets()

    def build_widgets(self):
        Label(self.root, text=f"{BOT_NAME}", font=("Arial", 24, "bold"), bg="#00897b", fg="white", pady=10).pack(fill=X)

        self.chat_area = scrolledtext.ScrolledText(self.root, wrap=WORD, font=("Segoe UI", 12), bg="white", fg="black")
        self.chat_area.tag_config("user", foreground="#0d47a1", font=("Segoe UI", 12, "bold"))
        self.chat_area.tag_config("bot", foreground="#1b5e20", font=("Segoe UI", 12))
        self.chat_area.config(state=DISABLED)
        self.chat_area.pack(padx=15, pady=10, fill=BOTH, expand=True)

        self.entry_frame = Frame(self.root, bg="#e0f7fa")
        self.entry_frame.pack(fill=X, padx=15)

        self.user_input = Entry(self.entry_frame, font=("Segoe UI", 12))
        self.user_input.pack(side=LEFT, fill=X, expand=True, padx=(0, 10))
        self.user_input.bind("<Return>", lambda event: self.send_message())

        Button(self.entry_frame, text="Send", bg="#00796b", fg="white", font=("Segoe UI", 11), width=10, command=self.send_message).pack(side=LEFT)

        Button(self.root, text="Clear Chat", bg="#c62828", fg="white", font=("Segoe UI", 11), width=12, command=self.clear_chat).pack(pady=10)

        self.root.protocol("WM_DELETE_WINDOW", self.close_app)

    def send_message(self):
        user_msg = self.user_input.get().strip()
        if not user_msg:
            return

        self.display_message(f"You: {user_msg}", "user")
        self.user_input.delete(0, END)
        threading.Thread(target=self.reply, args=(user_msg,)).start()

    def reply(self, user_msg):
        time.sleep(0.4)
        response = chatbot.respond(user_msg)
        if not response:
            response = "Sorry, I don't understand that yet."
        self.display_message(f"{BOT_NAME}: {response}", "bot")

    def display_message(self, message, tag):
        self.chat_area.config(state=NORMAL)
        self.chat_area.insert(END, message + "\n", tag)
        self.chat_area.config(state=DISABLED)
        self.chat_area.yview(END)

    def clear_chat(self):
        if messagebox.askyesno("Clear", "Are you sure you want to clear chat?"):
            self.chat_area.config(state=NORMAL)
            self.chat_area.delete('1.0', END)
            self.chat_area.config(state=DISABLED)

    def close_app(self):
        if messagebox.askokcancel("Exit", "Close the chatbot?"):
            self.root.destroy()

if __name__ == "__main__":
    root = Tk()
    app = ChatbotApp(root)
    root.mainloop()
