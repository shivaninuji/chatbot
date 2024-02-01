import json
import re                  #regular expression- for text processing
import random_responses
import tkinter as tk        #tkinter- for building gui(standard package in python for gui)
from tkinter import Scrollbar, Text, Entry, Frame

# Load JSON data
def load_json(file):
    with open(file) as bot_responses:
        print(f"Loaded '{file}' successfully!")
        return json.load(bot_responses)

# Store JSON data
response_data = load_json("bot.json")

# Function to get bot response
def get_response(input_string):
    split_message = re.split(r'\s+|[,;?!.-]\s*', input_string.lower())
    score_list = []

    # Check all the responses
    for response in response_data:
        response_score = 0
        required_score = 0
        required_words = response["required_words"]

        # Check if there are any required words
        if required_words:
            for word in split_message:
                if word in required_words:
                    required_score += 1

        # Amount of required words should match the required score
        if required_score == len(required_words):
            # Check each word the user has typed
            for word in split_message:
                # If the word is in the response, add to the score
                if word in response["user_input"]:
                    response_score += 1

        # Add score to list
        score_list.append(response_score)

    # Find the best response and return it if they're not all 0
    best_response = max(score_list)
    response_index = score_list.index(best_response)

    # If there is no good response, return a random one.
    if best_response != 0:
        return response_data[response_index]["bot_response"]

    return random_responses.random_string()

# Function to handle user input
def on_send():                          #retrieves user input, updates the chat display, and clears the input field.
    user_input = input_entry.get()
    if user_input:
        chat_box.config(state=tk.NORMAL)
        chat_box.insert(tk.END, f"You: {user_input}\n")
        chat_box.insert(tk.END, f"Bot: {get_response(user_input)}\n")
        chat_box.config(state=tk.DISABLED)
        input_entry.delete(0, tk.END)

#for creating gui
# Create the main window
root = tk.Tk()                  
root.title("Chatbot")

# Create frames
chat_frame = Frame(root)        #displaying the chat
input_frame = Frame(root)       #user input

# Create text widget for chat
chat_box = Text(chat_frame, wrap="word", state=tk.DISABLED)
scrollbar = Scrollbar(chat_frame, command=chat_box.yview)
chat_box.config(yscrollcommand=scrollbar.set)
chat_box.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Create entry widget for user input
input_entry = Entry(input_frame, width=50)
send_button = tk.Button(input_frame, text="Send", command=on_send)

# Pack widgets
input_entry.pack(side=tk.LEFT, padx=5)                  #Organizes and packs widgets into the frames, specifying their layout.
send_button.pack(side=tk.RIGHT, padx=5)
chat_frame.pack(fill=tk.BOTH, expand=True)
input_frame.pack(fill=tk.BOTH)

# Start the main loop
root.mainloop()             #Initiates the main event loop, allowing the GUI to respond to user interactions.
