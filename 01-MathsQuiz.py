import tkinter as tk
from tkinter import messagebox
import random


# Global variables
selected_difficulty = None
questions = []
question_number = 0
score = 0
attempt = 1


# Utility functions
def clear_window():
    """Remove all widgets from the main window."""
    for widget in root.winfo_children():
        widget.destroy()


# Assessment functions
def displayMenu():
    """Display the difficulty selection menu."""
    clear_window()

    title_label = tk.Label(
        root,
        text="Maths Quiz",
        font=("Arial", 20, "bold")
    )
    title_label.pack(pady=20)

    instruction_label = tk.Label(
        root,
        text="Choose a difficulty level:"
    )
    instruction_label.pack(pady=5)

    tk.Button(
        root,
        text="Easy",
        width=15,
        command=lambda: select_difficulty("Easy")
    ).pack(pady=5)

    tk.Button(
        root,
        text="Moderate",
        width=15,
        command=lambda: select_difficulty("Moderate")
    ).pack(pady=5)

    tk.Button(
        root,
        text="Advanced",
        width=15,
        command=lambda: select_difficulty("Advanced")
    ).pack(pady=5)


def select_difficulty(difficulty):
    """Store the selected difficulty and begin the quiz."""
    global selected_difficulty

    selected_difficulty = difficulty
    start_quiz()


def randomInt():
    """
    Generate two random integers based on the
    selected difficulty level.
    """
    if selected_difficulty == "Easy":
        minimum = 1
        maximum = 9

    elif selected_difficulty == "Moderate":
        minimum = 10
        maximum = 99

    else:
        minimum = 1000
        maximum = 9999

    number1 = random.randint(minimum, maximum)
    number2 = random.randint(minimum, maximum)

    return number1, number2


def decideOperation():
    """Randomly choose either addition or subtraction."""
    return random.choice(["+", "-"])


def create_question():
    """Create one random maths question and calculate its answer."""
    number1, number2 = randomInt()
    operation = decideOperation()

    if operation == "+":
        answer = number1 + number2
    else:
        answer = number1 - number2

    return {
        "text": f"{number1} {operation} {number2}",
        "answer": answer
    }


def displayProblem():
    """Display the current question and allow the user to enter an answer."""
    clear_window()

    question_label = tk.Label(
        root,
        text=f"Question {question_number + 1} of 10",
        font=("Arial", 14, "bold")
    )
    question_label.pack(pady=15)

    question_text = tk.Label(
        root,
        text=f"{questions[question_number]['text']} =",
        font=("Arial", 18)
    )
    question_text.pack(pady=15)

    attempt_label = tk.Label(
        root,
        text=f"Attempt {attempt} of 2"
    )
    attempt_label.pack(pady=5)

    answer_entry = tk.Entry(
        root,
        width=15,
        justify="center",
        font=("Arial", 14)
    )
    answer_entry.pack(pady=10)
    answer_entry.focus()

    submit_button = tk.Button(
        root,
        text="Submit Answer",
        command=lambda: isCorrect(answer_entry)
    )
    submit_button.pack(pady=10)

    root.bind(
        "<Return>",
        lambda event: isCorrect(answer_entry)
    )


def isCorrect(answer_entry):
    """
    Check the user's answer.

    A correct first attempt awards 10 points.
    A correct second attempt awards 5 points.
    An incorrect second attempt awards 0 points.
    """
    global question_number
    global score
    global attempt

    try:
        user_answer = int(answer_entry.get())
    except ValueError:
        messagebox.showerror(
            "Invalid Answer",
            "Please enter a whole number."
        )
        return

    correct_answer = questions[question_number]["answer"]

    if user_answer == correct_answer:

        if attempt == 1:
            score += 10
            messagebox.showinfo(
                "Correct",
                "Correct! You earned 10 points."
            )
        else:
            score += 5
            messagebox.showinfo(
                "Correct",
                "Correct on your second attempt! You earned 5 points."
            )

        move_to_next_question()

    else:

        if attempt == 1:
            attempt = 2

            messagebox.showwarning(
                "Incorrect",
                "That answer is incorrect.\n\n"
                "You have one more attempt."
            )

            displayProblem()

        else:
            messagebox.showerror(
                "Incorrect",
                f"Incorrect again.\n\n"
                f"The correct answer was {correct_answer}."
            )

            move_to_next_question()


def move_to_next_question():
    """Move to the next question or display the final results."""
    global question_number
    global attempt

    question_number += 1
    attempt = 1

    if question_number < 10:
        displayProblem()
    else:
        displayResults()


def displayResults():
    """Display the final score and performance ranking."""
    clear_window()

    if score > 90:
        rank = "A+"
    elif score >= 80:
        rank = "A"
    elif score >= 70:
        rank = "B"
    elif score >= 60:
        rank = "C"
    elif score >= 50:
        rank = "D"
    else:
        rank = "F"

    result_label = tk.Label(
        root,
        text="Quiz Complete!",
        font=("Arial", 20, "bold")
    )
    result_label.pack(pady=20)

    score_label = tk.Label(
        root,
        text=f"Your score: {score} out of 100",
        font=("Arial", 16)
    )
    score_label.pack(pady=10)

    rank_label = tk.Label(
        root,
        text=f"Rank: {rank}",
        font=("Arial", 16, "bold")
    )
    rank_label.pack(pady=10)

    tk.Button(
        root,
        text="Play Again",
        width=15,
        command=displayMenu
    ).pack(pady=10)

    tk.Button(
        root,
        text="Quit",
        width=15,
        command=root.destroy
    ).pack(pady=5)


def start_quiz():
    """Generate ten questions and start the quiz."""
    global questions
    global question_number
    global score
    global attempt

    questions = []
    question_number = 0
    score = 0
    attempt = 1

    for _ in range(10):
        questions.append(create_question())

    displayProblem()


# Main program
root = tk.Tk()
root.title("Maths Quiz")
root.geometry("400x350")
root.resizable(False, False)

displayMenu()

root.mainloop()