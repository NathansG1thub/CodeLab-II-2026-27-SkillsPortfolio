import tkinter as tk
import random

root = tk.Tk()
root.title("Maths Quiz")
root.geometry("400x300")

selected_difficulty = None
questions = []
question_number = 0
score = 0


def clear_window():
    for widget in root.winfo_children():
        widget.destroy()


def select_difficulty(difficulty):
    global selected_difficulty
    selected_difficulty = difficulty


def generate_questions(difficulty):
    generated_questions = []

    for _ in range(10):
        if difficulty == "Easy":
            num1 = random.randint(1, 10)
            num2 = random.randint(1, 10)
            operation = random.choice(["+", "-"])
        elif difficulty == "Medium":
            num1 = random.randint(10, 50)
            num2 = random.randint(10, 50)
            operation = random.choice(["+", "-", "*"])
        else:
            num1 = random.randint(50, 100)
            num2 = random.randint(50, 100)
            operation = random.choice(["+", "-", "*", "/"])

        if operation == "+":
            answer = num1 + num2
        elif operation == "-":
            answer = num1 - num2
        elif operation == "*":
            answer = num1 * num2
        else:
            num1 = num2 * random.randint(1, 10)
            answer = num1 // num2

        generated_questions.append({
            "text": f"{num1} {operation} {num2}",
            "answer": answer
        })

    return generated_questions


def show_difficulty_menu():
    clear_window()

    tk.Label(root, text="Choose a difficulty level", font=("Arial", 14)).pack(pady=20)
    tk.Button(root, text="Easy", width=15,
              command=lambda: select_difficulty("Easy")).pack(pady=5)
    tk.Button(root, text="Medium", width=15,
              command=lambda: select_difficulty("Medium")).pack(pady=5)
    tk.Button(root, text="Hard", width=15,
              command=lambda: select_difficulty("Hard")).pack(pady=5)
    tk.Button(root, text="Start Quiz", width=15,
              command=start_quiz).pack(pady=15)


def start_quiz():
    global questions, question_number, score

    if selected_difficulty is None:
        tk.Label(root, text="Please select a difficulty level.", fg="red").pack()
        return

    questions = generate_questions(selected_difficulty)
    question_number = 0
    score = 0
    show_question()


def show_question():
    clear_window()

    question = questions[question_number]
    tk.Label(root, text=f"Question {question_number + 1} of 10",
             font=("Arial", 12)).pack(pady=10)
    tk.Label(root, text=question["text"], font=("Arial", 18)).pack(pady=10)

    answer_entry = tk.Entry(root, width=10)
    answer_entry.pack(pady=10)
    answer_entry.focus()

    tk.Button(root, text="Submit",
              command=lambda: check_answer(answer_entry)).pack(pady=10)


def check_answer(answer_entry):
    global question_number, score

    try:
        user_answer = int(answer_entry.get())
    except ValueError:
        tk.Label(root, text="Please enter a whole number.", fg="red").pack()
        return

    if user_answer == questions[question_number]["answer"]:
        score += 1

    question_number += 1
    if question_number < 10:
        show_question()
    else:
        show_result()


def show_result():
    clear_window()

    tk.Label(root, text="Quiz Complete", font=("Arial", 16)).pack(pady=20)
    tk.Label(root, text=f"Your score: {score} out of 10",
             font=("Arial", 14)).pack(pady=10)

    if score == 10:
        message = "Excellent!"
    elif score >= 7:
        message = "Good job!"
    elif score >= 4:
        message = "Not bad!"
    else:
        message = "Keep practising!"

    tk.Label(root, text=message).pack(pady=10)
    tk.Button(root, text="Play Again",
              command=show_difficulty_menu).pack(pady=10)


show_difficulty_menu()
root.mainloop()
