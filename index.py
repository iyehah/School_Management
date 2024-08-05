import sys
import tkinter as tk
from tkinter import ttk
import dashboard
import student_management
import subject_management
import teacher_management
import classroom_management

class SchoolManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("School Management System")
        self.root.geometry("900x700")

        # Configure the style for the notebook and tabs
        style = ttk.Style()
        style.configure('TNotebook.Tab', padding=[10, 5], font=('Arial', 12))
        style.configure('TNotebook', background='#f0f0f0')
        style.map('TNotebook.Tab',
                  background=[('selected', '#d0d0d0')],
                  foreground=[('selected', 'black')],
                  relief=[('selected', 'flat')],
                  )

        # Create a Notebook widget to hold the tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill='both')

        # Create frames for each tab
        self.dashboard_frame = ttk.Frame(self.notebook)
        self.student_management_frame = ttk.Frame(self.notebook)
        self.subject_management_frame = ttk.Frame(self.notebook)
        self.teacher_management_frame = ttk.Frame(self.notebook)
        self.classroom_management_frame = ttk.Frame(self.notebook)

        # Add frames as tabs to the notebook
        self.notebook.add(self.dashboard_frame, text="Dashboard")
        self.notebook.add(self.student_management_frame, text="Student Management")
        self.notebook.add(self.subject_management_frame, text="Subject Management")
        self.notebook.add(self.teacher_management_frame, text="Teacher Management")
        self.notebook.add(self.classroom_management_frame, text="Classroom Management")

        # Initialize the UI for each tab
        dashboard.Dashboard(self.dashboard_frame)
        student_management.StudentManagement(self.student_management_frame)
        subject_management.SubjectManagement(self.subject_management_frame)
        teacher_management.TeacherManagement(self.teacher_management_frame)
        classroom_management.ClassroomManagement(self.classroom_management_frame)

        # Bind the close event to the exit function
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def on_close(self):
        # Perform any cleanup tasks here
        print("Closing application...")  # For debugging
        self.root.destroy()
        sys.exit()  # Ensure the application exits completely

if __name__ == "__main__":
    window = tk.Tk()
    app = SchoolManagementSystem(window)
    window.mainloop()
