import tkinter as tk
import random
import os

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

print("Number of jokes loaded:", len(jokes))
print("First joke:", jokes[0])