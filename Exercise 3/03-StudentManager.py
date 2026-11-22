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


students = load_students()

print(students)