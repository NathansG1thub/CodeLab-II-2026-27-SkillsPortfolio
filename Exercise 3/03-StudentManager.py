import tkinter as tk
import os

# Get the script's folder path
script_dir = os.path.dirname(os.path.abspath(__file__))


def load_students():
    """Read student records from the external text file."""
    students = []

    file_path = os.path.join(script_dir, "studentmarks.txt")

    with open(file_path, "r") as file:
        number_of_students = int(file.readline().strip())

        for _ in range(number_of_students):
            line = file.readline().strip()
            data = line.split(",")

            student = {
                "number": data[0],
                "name": data[1],
                "coursework": [
                    int(data[2]),
                    int(data[3]),
                    int(data[4])
                ],
                "exam": int(data[5])
            }

            students.append(student)

    return students

def calculate_results(student):
    """Calculate total coursework, percentage and grade."""
    coursework_total = sum(student["coursework"])
    total_mark = coursework_total + student["exam"]
    percentage = (total_mark / 160) * 100

    if percentage >= 70:
        grade = "A"
    elif percentage >= 60:
        grade = "B"
    elif percentage >= 50:
        grade = "C"
    elif percentage >= 40:
        grade = "D"
    else:
        grade = "F"

    return coursework_total, percentage, grade

students = load_students()

# CREATE MAIN WINDOW

# COLOUR SETTINGS
BG_COLOR = "#D0ECFA"
BTN_COLOR = "#287C78"
FG_COLOR = "#FBDEDE"
TEXT_COLOR = "#263238"


# CREATE MAIN WINDOW
root = tk.Tk()
root.title("Student Manager")
root.geometry("600x550")
root.resizable(False, False)
root.configure(bg=BG_COLOR)


# VIEW ALL STUDENT RECORDS
def view_all_students():
    for widget in root.winfo_children():
        widget.destroy()

    title_label = tk.Label(
        root,
        text="All Student Records",
        font=("Arial", 20, "bold"),
        bg=BG_COLOR,
        fg=TEXT_COLOR
    )
    title_label.pack(pady=15)

    average_percentage = sum(
        calculate_results(student)[1] for student in students
    ) / len(students)

    summary_label = tk.Label(
        root,
        text=f"Number of Students: {len(students)}    "
             f"Average Percentage: {average_percentage:.2f}%",
        font=("Arial", 11, "bold"),
        bg=BG_COLOR,
        fg=TEXT_COLOR
    )
    summary_label.pack(pady=10)

    # RESULTS AREA
    results_frame = tk.Frame(root, bg=BG_COLOR)
    results_frame.pack(fill="both", expand=True, padx=15, pady=10)

    scrollbar = tk.Scrollbar(results_frame)
    scrollbar.pack(side="right", fill="y")

    results_text = tk.Text(
        results_frame,
        font=("Consolas", 10),
        yscrollcommand=scrollbar.set,
        wrap="word",
        bg="white",
        fg=TEXT_COLOR
    )
    results_text.pack(side="left", fill="both", expand=True)

    scrollbar.config(command=results_text.yview)

    # DISPLAY EACH STUDENT
    for student in students:
        coursework_total, percentage, grade = calculate_results(student)

        record = (
            f"Name: {student['name']}\n"
            f"Student Number: {student['number']}\n"
            f"Coursework Total: {coursework_total}/60\n"
            f"Exam Mark: {student['exam']}/100\n"
            f"Overall Percentage: {percentage:.2f}%\n"
            f"Grade: {grade}\n"
            f"{'-' * 40}\n"
        )

        results_text.insert(tk.END, record)

    results_text.config(state="disabled")

    back_button = tk.Button(
        root,
        text="Back to Menu",
        font=("Arial", 11),
        width=20,
        bg=BTN_COLOR,
        fg=FG_COLOR,
        command=show_menu
    )
    back_button.pack(pady=12)


# VIEW INDIVIDUAL STUDENT
def view_individual_student():
    for widget in root.winfo_children():
        widget.destroy()

    title_label = tk.Label(
        root,
        text="Find Individual Student",
        font=("Arial", 20, "bold"),
        bg=BG_COLOR,
        fg=TEXT_COLOR
    )
    title_label.pack(pady=25)

    instruction_label = tk.Label(
        root,
        text="Enter a student name or student number:",
        font=("Arial", 11),
        bg=BG_COLOR,
        fg=TEXT_COLOR
    )
    instruction_label.pack(pady=5)

    search_entry = tk.Entry(
        root,
        font=("Arial", 12),
        width=30
    )
    search_entry.pack(pady=10)

    result_label = tk.Label(
        root,
        text="",
        font=("Consolas", 11),
        bg=BG_COLOR,
        fg=TEXT_COLOR,
        justify="left"
    )
    result_label.pack(pady=20)

    def search_student():
        search_value = search_entry.get().strip().lower()

        if not search_value:
            result_label.config(text="Please enter a name or student number.")
            return

        found_student = None

        for student in students:
            if (search_value == student["number"] or
                    search_value == student["name"].lower()):
                found_student = student
                break

        if found_student:
            coursework_total, percentage, grade = calculate_results(found_student)

            result = (
                f"Name: {found_student['name']}\n\n"
                f"Student Number: {found_student['number']}\n\n"
                f"Coursework Total: {coursework_total}/60\n\n"
                f"Exam Mark: {found_student['exam']}/100\n\n"
                f"Overall Percentage: {percentage:.2f}%\n\n"
                f"Grade: {grade}"
            )

            result_label.config(text=result)
        else:
            result_label.config(text="No matching student found.")

    search_button = tk.Button(
        root,
        text="Search",
        font=("Arial", 11),
        width=20,
        bg=BTN_COLOR,
        fg=FG_COLOR,
        command=search_student
    )
    search_button.pack(pady=10)

    back_button = tk.Button(
        root,
        text="Back to Menu",
        font=("Arial", 11),
        width=20,
        bg=BTN_COLOR,
        fg=FG_COLOR,
        command=show_menu
    )
    back_button.pack(pady=10)

# MAIN MENU

# DISPLAY HIGHEST AND LOWEST SCORING STUDENTS
def show_top_student(highest=True):
    for widget in root.winfo_children():
        widget.destroy()

    if highest:
        title = "Highest Scoring Student"
        student = max(
            students,
            key=lambda student: sum(student["coursework"]) + student["exam"]
        )
    else:
        title = "Lowest Scoring Student"
        student = min(
            students,
            key=lambda student: sum(student["coursework"]) + student["exam"]
        )

    coursework_total, percentage, grade = calculate_results(student)

    title_label = tk.Label(
        root,
        text=title,
        font=("Arial", 20, "bold"),
        bg=BG_COLOR,
        fg=TEXT_COLOR
    )
    title_label.pack(pady=25)

    result = (
        f"Name: {student['name']}\n\n"
        f"Student Number: {student['number']}\n\n"
        f"Coursework Total: {coursework_total}/60\n\n"
        f"Exam Mark: {student['exam']}/100\n\n"
        f"Overall Percentage: {percentage:.2f}%\n\n"
        f"Grade: {grade}"
    )

    result_label = tk.Label(
        root,
        text=result,
        font=("Consolas", 11),
        bg=BG_COLOR,
        fg=TEXT_COLOR,
        justify="left"
    )
    result_label.pack(pady=20)

    back_button = tk.Button(
        root,
        text="Back to Menu",
        font=("Arial", 11),
        width=20,
        bg=BTN_COLOR,
        fg=FG_COLOR,
        command=show_menu
    )
    back_button.pack(pady=15)


def show_highest_student():
    show_top_student(True)


def show_lowest_student():
    show_top_student(False)


# SORT STUDENT RECORDS
def sort_students():
    for widget in root.winfo_children():
        widget.destroy()

    title_label = tk.Label(
        root,
        text="Sort Student Records",
        font=("Arial", 20, "bold"),
        bg=BG_COLOR,
        fg=TEXT_COLOR
    )
    title_label.pack(pady=15)

    tk.Label(
        root,
        text="Choose a sorting method:",
        font=("Arial", 11),
        bg=BG_COLOR,
        fg=TEXT_COLOR
    ).pack(pady=5)

    sort_options = [
        "Student Name",
        "Student Number",
        "Overall Percentage"
    ]

    sort_choice = tk.StringVar(value="Student Name")

    for option in sort_options:
        tk.Radiobutton(
            root,
            text=option,
            variable=sort_choice,
            value=option,
            font=("Arial", 11),
            bg=BG_COLOR,
            fg=TEXT_COLOR,
            selectcolor=BG_COLOR
        ).pack(anchor="w", padx=170)

    order_choice = tk.StringVar(value="Ascending")

    tk.Label(
        root,
        text="Choose sorting order:",
        font=("Arial", 11),
        bg=BG_COLOR,
        fg=TEXT_COLOR
    ).pack(pady=8)

    for option in ["Ascending", "Descending"]:
        tk.Radiobutton(
            root,
            text=option,
            variable=order_choice,
            value=option,
            font=("Arial", 11),
            bg=BG_COLOR,
            fg=TEXT_COLOR,
            selectcolor=BG_COLOR
        ).pack(anchor="w", padx=170)

    def display_sorted_records():
        selected = sort_choice.get()
        descending = order_choice.get() == "Descending"

        if selected == "Student Name":
            sorted_students = sorted(
                students,
                key=lambda student: student["name"].lower(),
                reverse=descending
            )
        elif selected == "Student Number":
            sorted_students = sorted(
                students,
                key=lambda student: int(student["number"]),
                reverse=descending
            )
        else:
            sorted_students = sorted(
                students,
                key=lambda student: sum(student["coursework"]) + student["exam"],
                reverse=descending
            )

        # DISPLAY SORTED RESULTS
        for widget in root.winfo_children():
            widget.destroy()

        title_label = tk.Label(
            root,
            text=f"Sorted by {selected} ({order_choice.get()})",
            font=("Arial", 18, "bold"),
            bg=BG_COLOR,
            fg=TEXT_COLOR
        )
        title_label.pack(pady=15)

        results_frame = tk.Frame(root, bg=BG_COLOR)
        results_frame.pack(fill="both", expand=True, padx=15, pady=5)

        scrollbar = tk.Scrollbar(results_frame)
        scrollbar.pack(side="right", fill="y")

        results_text = tk.Text(
            results_frame,
            font=("Consolas", 10),
            yscrollcommand=scrollbar.set,
            wrap="word",
            bg="white",
            fg=TEXT_COLOR
        )
        results_text.pack(side="left", fill="both", expand=True)

        scrollbar.config(command=results_text.yview)

        for student in sorted_students:
            coursework_total, percentage, grade = calculate_results(student)

            record = (
                f"Name: {student['name']}\n"
                f"Student Number: {student['number']}\n"
                f"Coursework Total: {coursework_total}/60\n"
                f"Exam Mark: {student['exam']}/100\n"
                f"Overall Percentage: {percentage:.2f}%\n"
                f"Grade: {grade}\n"
                f"{'-' * 40}\n"
            )

            results_text.insert(tk.END, record)

        results_text.config(state="disabled")

        back_button = tk.Button(
            root,
            text="Back to Menu",
            font=("Arial", 11),
            width=20,
            bg=BTN_COLOR,
            fg=FG_COLOR,
            command=show_menu
        )
        back_button.pack(pady=10)

    sort_button = tk.Button(
        root,
        text="Sort Records",
        font=("Arial", 11),
        width=20,
        bg=BTN_COLOR,
        fg=FG_COLOR,
        command=display_sorted_records
    )
    sort_button.pack(pady=12)

    back_button = tk.Button(
        root,
        text="Back to Menu",
        font=("Arial", 11),
        width=20,
        bg=BTN_COLOR,
        fg=FG_COLOR,
        command=show_menu
    )
    back_button.pack(pady=5)

def show_menu():
    for widget in root.winfo_children():
        widget.destroy()

    title_label = tk.Label(
        root,
        text="Student Manager",
        font=("Arial", 22, "bold"),
        bg=BG_COLOR,
        fg=TEXT_COLOR
    )
    title_label.pack(pady=25)

    menu_options = [
        "View All Student Records",
        "View Individual Student",
        "Show Highest Scoring Student",
        "Show Lowest Scoring Student",
        "Sort Student Records",
        "Add Student Record",
        "Delete Student Record",
        "Update Student Record"
    ]

    for index, option in enumerate(menu_options):
        button = tk.Button(
            root,
            text=option,
            font=("Arial", 11),
            width=30,
            bg=BTN_COLOR,
            fg=FG_COLOR,
            activebackground="#359A94",
            activeforeground=FG_COLOR,
            command=(
                view_all_students if index == 0
                else view_individual_student if index == 1
                else show_highest_student if index == 2
                else show_lowest_student if index == 3
                else sort_students if index == 4
                else None
            ))
        button.pack(pady=4)

    quit_button = tk.Button(
        root,
        text="Quit",
        font=("Arial", 11, "bold"),
        width=30,
        bg="#A94442",
        fg=FG_COLOR,
        command=root.destroy
    )
    quit_button.pack(pady=12)


# DISPLAY MAIN MENU
show_menu()

# RUN APPLICATION
root.mainloop()
