import tkinter as tk
import os
from tkinter import messagebox

# Get the script's folder path
script_dir = os.path.dirname(os.path.abspath(__file__))


def load_students():
    """Read student records from the external text file."""
    students = []

    file_path = os.path.join(script_dir, "03-studentmarks.txt")

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

def save_students():
    """Save all student records to the external text file."""
    file_path = os.path.join(script_dir, "studentmarks.txt")

    with open(file_path, "w") as file:
        file.write(str(len(students)) + "\n")

        for student in students:
            record = [
                student["number"],
                student["name"],
                *student["coursework"],
                student["exam"]
            ]

            file.write(",".join(map(str, record)) + "\n")

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

# Create main window and set its properties

# Color scheme
BG_COLOR = "#D0ECFA"
BTN_COLOR = "#287C78"
FG_COLOR = "#FBDEDE"
TEXT_COLOR = "#263238"


# Create the main application window
root = tk.Tk()
root.title("Student Manager")
root.geometry("600x550")
root.resizable(False, False)
root.configure(bg=BG_COLOR)

# Set the application icon
icon_path = os.path.join(script_dir, "03-student_cap.ico")
try:
    root.iconbitmap(icon_path)
except tk.TclError:
    print(f"Warning: Could not load icon at {icon_path}. Using default icon.")

# View All Students
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

    # Results Frame with Scrollbar
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

    # Display each student's record
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


# View Individual Student
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

# Main Menu

# Display Highest and Lowest Scoring Students
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


# Sort Student Records
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

        # Display the sorted records
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

# Add Student Record
def add_student():
    for widget in root.winfo_children():
        widget.destroy()

    title_label = tk.Label(
        root,
        text="Add Student Record",
        font=("Arial", 20, "bold"),
        bg=BG_COLOR,
        fg=TEXT_COLOR
    )
    title_label.pack(pady=15)

    form_frame = tk.Frame(root, bg=BG_COLOR)
    form_frame.pack(pady=10)

    fields = [
        ("Student Number", ""),
        ("Student Name", ""),
        ("Coursework 1", ""),
        ("Coursework 2", ""),
        ("Coursework 3", ""),
        ("Exam Mark", "")
    ]

    entries = {}

    for row, (field, default) in enumerate(fields):
        tk.Label(
            form_frame,
            text=field + ":",
            font=("Arial", 10),
            bg=BG_COLOR,
            fg=TEXT_COLOR
        ).grid(row=row, column=0, padx=10, pady=6, sticky="w")

        entry = tk.Entry(form_frame, font=("Arial", 10), width=25)
        entry.grid(row=row, column=1, padx=10, pady=6)
        entries[field] = entry

    def save_new_student():
        number = entries["Student Number"].get().strip()
        name = entries["Student Name"].get().strip()

        try:
            coursework = [
                int(entries["Coursework 1"].get()),
                int(entries["Coursework 2"].get()),
                int(entries["Coursework 3"].get())
            ]
            exam = int(entries["Exam Mark"].get())
        except ValueError:
            messagebox.showerror(
                "Invalid Input",
                "All marks must be whole numbers."
            )
            return

        if not number.isdigit() or len(number) != 4 or not 1000 <= int(number) <= 9999:
            messagebox.showerror(
                "Invalid Student Number",
                "Student number must be between 1000 and 9999."
            )
            return

        if any(student["number"] == number for student in students):
            messagebox.showerror(
                "Duplicate Student Number",
                "This student number already exists."
            )
            return

        if not name:
            messagebox.showerror(
                "Invalid Name",
                "Please enter the student's name."
            )
            return

        if any(mark < 0 or mark > 20 for mark in coursework):
            messagebox.showerror(
                "Invalid Coursework Mark",
                "Each coursework mark must be between 0 and 20."
            )
            return

        if exam < 0 or exam > 100:
            messagebox.showerror(
                "Invalid Exam Mark",
                "The exam mark must be between 0 and 100."
            )
            return

        new_student = {
            "number": number,
            "name": name,
            "coursework": coursework,
            "exam": exam
        }

        students.append(new_student)
        save_students()

        messagebox.showinfo(
            "Student Added",
            f"{name} was successfully added."
        )

        show_menu()

    save_button = tk.Button(
        root,
        text="Add Student",
        font=("Arial", 11),
        width=20,
        bg=BTN_COLOR,
        fg=FG_COLOR,
        command=save_new_student
    )
    save_button.pack(pady=8)

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

# Delete Student Record
def delete_student():
    for widget in root.winfo_children():
        widget.destroy()

    title_label = tk.Label(
        root,
        text="Delete Student Record",
        font=("Arial", 20, "bold"),
        bg=BG_COLOR,
        fg=TEXT_COLOR
    )
    title_label.pack(pady=25)

    tk.Label(
        root,
        text="Enter the student number to delete:",
        font=("Arial", 11),
        bg=BG_COLOR,
        fg=TEXT_COLOR
    ).pack(pady=5)

    number_entry = tk.Entry(root, font=("Arial", 12), width=25)
    number_entry.pack(pady=10)

    def confirm_delete():
        number = number_entry.get().strip()

        found_student = None

        for student in students:
            if student["number"] == number:
                found_student = student
                break

        if found_student is None:
            messagebox.showerror(
                "Student Not Found",
                "No student with that number exists."
            )
            return

        confirmation = messagebox.askyesno(
            "Confirm Deletion",
            f"Are you sure you want to delete "
            f"{found_student['name']}?"
        )

        if confirmation:
            students.remove(found_student)
            save_students()

            messagebox.showinfo(
                "Student Deleted",
                f"{found_student['name']} was successfully deleted."
            )

            show_menu()

    delete_button = tk.Button(
        root,
        text="Delete Student",
        font=("Arial", 11),
        width=20,
        bg="#A94442",
        fg=FG_COLOR,
        command=confirm_delete
    )
    delete_button.pack(pady=10)

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

# Update Student Record
def update_student():
    for widget in root.winfo_children():
        widget.destroy()

    title_label = tk.Label(
        root,
        text="Update Student Record",
        font=("Arial", 20, "bold"),
        bg=BG_COLOR,
        fg=TEXT_COLOR
    )
    title_label.pack(pady=20)

    tk.Label(
        root,
        text="Enter the student number to find:",
        font=("Arial", 11),
        bg=BG_COLOR,
        fg=TEXT_COLOR
    ).pack(pady=5)

    number_entry = tk.Entry(root, font=("Arial", 12), width=25)
    number_entry.pack(pady=10)

    def find_student():
        number = number_entry.get().strip()

        found_student = None

        for student in students:
            if student["number"] == number:
                found_student = student
                break

        if found_student is None:
            messagebox.showerror(
                "Student Not Found",
                "No student with that number exists."
            )
            return

        # Display the update form with current values
        for widget in root.winfo_children():
            widget.destroy()

        tk.Label(
            root,
            text=f"Updating: {found_student['name']}",
            font=("Arial", 18, "bold"),
            bg=BG_COLOR,
            fg=TEXT_COLOR
        ).pack(pady=15)

        form_frame = tk.Frame(root, bg=BG_COLOR)
        form_frame.pack(pady=5)

        current_values = [
            found_student["number"],
            found_student["name"],
            found_student["coursework"][0],
            found_student["coursework"][1],
            found_student["coursework"][2],
            found_student["exam"]
        ]

        field_names = [
            "Student Number",
            "Student Name",
            "Coursework 1",
            "Coursework 2",
            "Coursework 3",
            "Exam Mark"
        ]

        entries = {}

        for row, field in enumerate(field_names):
            tk.Label(
                form_frame,
                text=field + ":",
                font=("Arial", 10),
                bg=BG_COLOR,
                fg=TEXT_COLOR
            ).grid(row=row, column=0, padx=10, pady=5, sticky="w")

            entry = tk.Entry(form_frame, font=("Arial", 10), width=25)
            entry.insert(0, str(current_values[row]))
            entry.grid(row=row, column=1, padx=10, pady=5)

            entries[field] = entry

        def save_changes():
            new_number = entries["Student Number"].get().strip()
            new_name = entries["Student Name"].get().strip()

            try:
                coursework = [
                    int(entries["Coursework 1"].get()),
                    int(entries["Coursework 2"].get()),
                    int(entries["Coursework 3"].get())
                ]
                exam = int(entries["Exam Mark"].get())
            except ValueError:
                messagebox.showerror(
                    "Invalid Input",
                    "All marks must be whole numbers."
                )
                return

            if (not new_number.isdigit() or len(new_number) != 4
                    or not 1000 <= int(new_number) <= 9999):
                messagebox.showerror(
                    "Invalid Student Number",
                    "Student number must be between 1000 and 9999."
                )
                return

            if any(
                student["number"] == new_number and student is not found_student
                for student in students
            ):
                messagebox.showerror(
                    "Duplicate Student Number",
                    "This student number already belongs to another student."
                )
                return

            if not new_name:
                messagebox.showerror(
                    "Invalid Name",
                    "Please enter the student's name."
                )
                return

            if any(mark < 0 or mark > 20 for mark in coursework):
                messagebox.showerror(
                    "Invalid Coursework Mark",
                    "Each coursework mark must be between 0 and 20."
                )
                return

            if exam < 0 or exam > 100:
                messagebox.showerror(
                    "Invalid Exam Mark",
                    "The exam mark must be between 0 and 100."
                )
                return

            found_student["number"] = new_number
            found_student["name"] = new_name
            found_student["coursework"] = coursework
            found_student["exam"] = exam

            save_students()

            messagebox.showinfo(
                "Record Updated",
                f"{new_name}'s record was successfully updated."
            )

            show_menu()

        tk.Button(
            root,
            text="Save Changes",
            font=("Arial", 11),
            width=20,
            bg=BTN_COLOR,
            fg=FG_COLOR,
            command=save_changes
        ).pack(pady=8)

        tk.Button(
            root,
            text="Back to Menu",
            font=("Arial", 11),
            width=20,
            bg=BTN_COLOR,
            fg=FG_COLOR,
            command=show_menu
        ).pack(pady=5)

    tk.Button(
        root,
        text="Find Student",
        font=("Arial", 11),
        width=20,
        bg=BTN_COLOR,
        fg=FG_COLOR,
        command=find_student
    ).pack(pady=10)

    tk.Button(
        root,
        text="Back to Menu",
        font=("Arial", 11),
        width=20,
        bg=BTN_COLOR,
        fg=FG_COLOR,
        command=show_menu
    ).pack(pady=5)

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
                else add_student if index == 5
                else delete_student if index == 6
                else update_student if index == 7
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


# Display the main menu when the application starts
show_menu()

# Run the main event loop to keep the application running
root.mainloop()
