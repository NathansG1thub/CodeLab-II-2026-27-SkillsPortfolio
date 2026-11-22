import tkinter as tk
import random
import os

current_joke = None

def load_jokes():
    """Read jokes from the external text file."""
    jokes = []

    try:
        file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "02-randomJokes.txt")
        with open(file_path, "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()

                if "?" in line:
                    setup, punchline = line.split("?", 1)
                    jokes.append((setup + "?", punchline))

    except FileNotFoundError:
        print("Error: 02-randomJokes.txt could not be found.")

    return jokes

jokes = load_jokes()

def tell_joke():
    """Select and display a random joke."""
    if not jokes:
        setup_label.config(text="No jokes available.")
        return
    global current_joke
    current_joke = random.choice(jokes)

    setup_label.config(text=current_joke[0])
    punchline_label.config(text="")

def show_punchline():
    """Reveal the current joke's punchline."""
    global current_joke
    if not current_joke:
        return
    punchline_label.config(text=current_joke[1])

# Create the main application window
root = tk.Tk()
root.title("Random Jokes")
root.geometry("500x350")
root.resizable(False, False)

# Application heading
heading_label = tk.Label(
    root,
    text="Random Jokes",
    font=("Arial", 20, "bold")
)
heading_label.pack(pady=20)

# Joke setup display
setup_label = tk.Label(
    root,
    text="Your joke will appear here!",
    font=("Arial", 12),
    wraplength=400
)
setup_label.pack(pady=20)

# Punchline display
punchline_label = tk.Label(
    root,
    text="",
    font=("Arial", 12, "italic"),
    wraplength=400
)
punchline_label.pack(pady=10)

tell_joke_button = tk.Button(
    root,
    text="Tell Me a Joke",
    font=("Arial", 11),
    command=tell_joke
)
tell_joke_button.pack(pady=15)

show_punchline_button = tk.Button(
    root,
    text="Show Punchline",
    font=("Arial", 11),
    command=show_punchline
)
show_punchline_button.pack(pady=15)

# Start the application
root.mainloop()