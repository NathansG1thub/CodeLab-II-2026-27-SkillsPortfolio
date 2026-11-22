import tkinter as tk
import random
from PIL import Image, ImageTk

current_joke = None
joke_history = []
history_position = -1

def load_jokes():
    """Read jokes from the external text file."""
    jokes = []

    try:
        with open("02-randomJokes.txt", "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()

                if "?" in line:
                    setup, punchline = line.split("?", 1)
                    jokes.append((setup + "?", punchline))

    except FileNotFoundError:
        print("Error: 02-randomJokes.txt could not be found.")

    return jokes


jokes = load_jokes()


def show_menu():
    """Display the welcome page."""
    joke_frame.pack_forget()
    menu_frame.pack(fill="both", expand=True)


def show_joke_page():
    """Display the joke page."""
    menu_frame.pack_forget()
    joke_frame.pack(fill="both", expand=True)


def tell_joke():
    """Select the first random joke and open the joke page."""
    global current_joke, joke_history, history_position

    if not jokes:
        setup_label.config(text="No jokes available.")
        show_joke_page()
        return

    joke_index = random.randrange(len(jokes))

    current_joke = jokes[joke_index]
    joke_history = [joke_index]
    history_position = 0

    setup_label.config(text=current_joke[0])
    punchline_label.config(text="")

    show_joke_page()


def next_joke():
    """Select another random joke."""
    global current_joke, history_position

    if len(jokes) == 0:
        return

    if len(jokes) == 1:
        return

    current_index = joke_history[history_position]

    available_indices = [
        i for i in range(len(jokes))
        if i != current_index
    ]

    new_index = random.choice(available_indices)

    # Remove any forward history when selecting a new joke
    del joke_history[history_position + 1:]

    joke_history.append(new_index)
    history_position += 1

    current_joke = jokes[new_index]

    setup_label.config(text=current_joke[0])
    punchline_label.config(text="")


def previous_joke():
    """Return to the previously viewed joke."""
    global current_joke, history_position

    if history_position > 0:
        history_position -= 1

        joke_index = joke_history[history_position]
        current_joke = jokes[joke_index]

        setup_label.config(text=current_joke[0])
        punchline_label.config(text="")


def show_punchline():
    """Reveal the current joke's punchline."""
    if current_joke:
        punchline_label.config(text=current_joke[1])


# Create the main application window
root = tk.Tk()
root.title("Random Jokes")
root.geometry("500x350")
root.resizable(False, False)
root.iconbitmap("02-clown.ico")

# Colors to match the background image
BG_COLOR = "#1b0a5e"  # Dark blue from the background
BTN_COLOR = "#5B4B8A" # Purple from your button frame
FG_COLOR = "white"    # Text color

# Page 1: Welcome screen
menu_frame = tk.Frame(root)

menu_background_image = Image.open("02-joke_background.jpg")
menu_background_image = menu_background_image.resize((500, 350))
menu_background_photo = ImageTk.PhotoImage(menu_background_image)

menu_background_label = tk.Label(
    menu_frame,
    image=menu_background_photo
)
menu_background_label.place(x=0, y=0, relwidth=1, relheight=1)

# FIX: Added bg and fg
heading_label = tk.Label(
    menu_frame,
    text="Random Jokes",
    font=("Arial", 20, "bold"),
    bg=BG_COLOR,
    fg=FG_COLOR
)
heading_label.pack(pady=50)

# FIX: Added bg and fg
welcome_label = tk.Label(
    menu_frame,
    text="Ready for a laugh?",
    font=("Arial", 12),
    bg=BG_COLOR,
    fg=FG_COLOR
)
welcome_label.pack(pady=10)

# FIX: Styled the button
tell_joke_button = tk.Button(
    menu_frame,
    text="Tell Me a Joke",
    font=("Arial", 12),
    bg=BTN_COLOR,
    fg=FG_COLOR,
    activebackground="#4a3c70",
    activeforeground=FG_COLOR,
    command=tell_joke
)
tell_joke_button.pack(pady=20)


# Page 2: Joke screen
joke_frame = tk.Frame(root)

joke_background_image = Image.open("02-joke_background.jpg")
joke_background_image = joke_background_image.resize((500, 350))
joke_background_photo = ImageTk.PhotoImage(joke_background_image)

joke_background_label = tk.Label(
    joke_frame,
    image=joke_background_photo
)
joke_background_label.place(x=0, y=0, relwidth=1, relheight=1)

# FIX: Added bg and fg
joke_heading = tk.Label(
    joke_frame,
    text="Random Jokes",
    font=("Arial", 20, "bold"),
    bg=BG_COLOR,
    fg=FG_COLOR
)
joke_heading.pack(pady=20)

# FIX: Added bg and fg
setup_label = tk.Label(
    joke_frame,
    text="",
    font=("Arial", 12),
    wraplength=400,
    bg=BG_COLOR,
    fg=FG_COLOR
)
setup_label.pack(pady=15)

# FIX: Added bg and fg
punchline_label = tk.Label(
    joke_frame,
    text="",
    font=("Arial", 12, "italic"),
    wraplength=400,
    bg=BG_COLOR,
    fg=FG_COLOR
)
punchline_label.pack(pady=10)


# FIX: Matched the frame background to the button color
button_frame = tk.Frame(joke_frame, bg=BTN_COLOR)
button_frame.pack(pady=15)

# FIX: Styled all buttons to match
show_punchline_button = tk.Button(
    button_frame,
    text="Show Punchline",
    font=("Arial", 11),
    width=16,
    bg=BTN_COLOR,
    fg=FG_COLOR,
    activebackground="#4a3c70",
    activeforeground=FG_COLOR,
    command=show_punchline
)
show_punchline_button.grid(row=0, column=0, padx=5, pady=5)

next_button = tk.Button(
    button_frame,
    text="Next Joke",
    font=("Arial", 11),
    width=16,
    bg=BTN_COLOR,
    fg=FG_COLOR,
    activebackground="#4a3c70",
    activeforeground=FG_COLOR,
    command=next_joke
)
next_button.grid(row=0, column=1, padx=5, pady=5)

previous_button = tk.Button(
    button_frame,
    text="Previous Joke",
    font=("Arial", 11),
    width=16,
    bg=BTN_COLOR,
    fg=FG_COLOR,
    activebackground="#4a3c70",
    activeforeground=FG_COLOR,
    command=previous_joke
)
previous_button.grid(row=1, column=0, padx=5, pady=5)

quit_button = tk.Button(
    button_frame,
    text="Quit",
    font=("Arial", 11),
    width=16,
    bg=BTN_COLOR,
    fg=FG_COLOR,
    activebackground="#4a3c70",
    activeforeground=FG_COLOR,
    command=show_menu
)
quit_button.grid(row=1, column=1, padx=5, pady=5)

# Display the welcome page initially
show_menu()

# Start the application
root.mainloop()