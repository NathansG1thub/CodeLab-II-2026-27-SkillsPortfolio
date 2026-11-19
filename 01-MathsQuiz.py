from random import random
from sys import implementation
import tkinter as tk
root = tk.Tk()

# Develop a GUI using Tkinter that presents the user with quiz of arithmetic problems. 
# Each "play" of the quiz should be 10 questions. 
# The user should initially be presented with a short menu of options to select a difficulty level. 

root.title("Maths Quiz")

root.geometry("400x300")

# need to create a variable to store the selected difficulty level

button_easy = tk.Button(root, text="Easy", command=lambda: select_difficulty("easy"))
button_medium = tk.Button(root, text="Medium", command=lambda: select_difficulty("medium"))
button_hard = tk.Button(root, text="Hard", command=lambda: select_difficulty("hard"))
button_easy.pack()
button_medium.pack()
button_hard.pack()

start_quiz_button = tk.Button(root, text="Start Quiz", command=lambda: start_quiz(selected_difficulty.get()))
start_quiz_button.pack()

def select_difficulty(difficulty):
    global selected_difficulty
    selected_difficulty = difficulty

def check_answer(question, answer_entry):
    user_answer = answer_entry.get()
    if user_answer == str(question["answer"]):
        result_label = tk.Label(root, text="Correct!")
    else:
        result_label = tk.Label(root, text=f"Incorrect! The correct answer was {question['answer']}.")
    result_label.pack()


def generate_questions(difficulty):
    questions = []
    for _ in range(10):
        if difficulty == "easy":
            num1 = random.randint(1, 10)
            num2 = random.randint(1, 10)
            operation = random.choice(["+", "-"])
        elif difficulty == "medium":
            num1 = random.randint(10, 50)
            num2 = random.randint(10, 50)
            operation = random.choice(["+", "-", "*"])
        else:  # hard
            num1 = random.randint(50, 100)
            num2 = random.randint(50, 100)
            operation = random.choice(["+", "-", "*", "/"])

        question_text = f"{num1} {operation} {num2}"
        answer = eval(question_text)
        questions.append({"question": question_text, "answer": answer})
    return questions
    
def start_quiz(difficulty):
    # Clear the window
    for widget in root.winfo_children():
        widget.destroy()

    # Generate 10 questions based on the selected difficulty
    questions = generate_questions(difficulty)
    score = 0

    for i, question in enumerate(questions):
        question_label = tk.Label(root, text=f"Question {i + 1}: {question['question']}")
        question_label.pack()

        answer_entry = tk.Entry(root)
        answer_entry.pack()

        submit_button = tk.Button(root, text="Submit", command=lambda q=question, a=answer_entry: check_answer(q, a))
        submit_button.pack()



root.mainloop()