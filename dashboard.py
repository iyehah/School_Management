import tkinter as tk
from tkinter import ttk
import sqlite3
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class Dashboard:
    def __init__(self, frame):
        self.frame = frame

        # Configure styles for cards
        self.configure_styles()

        # Create and place content cards
        self.create_content_cards()
        
        # Create and place graphics
        self.create_graphics()

    def configure_styles(self):
        style = ttk.Style()
        
        # Define custom styles for each card with different background colors
        style.configure('Card1.TFrame', background='lightblue')
        style.configure('Card2.TFrame', background='lightgreen')
        style.configure('Card3.TFrame', background='lightcoral')
        style.configure('Card4.TFrame', background='lightgoldenrodyellow')
        style.configure('Card5.TFrame', background='lightpink')
        style.configure('Card6.TFrame', background='lightgray')

    def create_content_cards(self):
        # Frame for content cards
        card_frame = ttk.Frame(self.frame, padding="10")
        card_frame.pack(fill='x')

        # Create cards with different styles
        self.create_card(card_frame, "Total Students", self.get_total_students(), 'Card1.TFrame')
        self.create_card(card_frame, "Total Teachers", self.get_total_teachers(), 'Card2.TFrame')
        self.create_card(card_frame, "Total Classrooms", self.get_total_classrooms(), 'Card3.TFrame')
        self.create_card(card_frame, "Unpaid Students", self.get_unpaid_students(), 'Card4.TFrame')
        self.create_card(card_frame, "Total Money", self.get_total_price(), 'Card5.TFrame')
        self.create_card(card_frame, "Total Salary", self.get_total_salary(), 'Card6.TFrame')

    def create_card(self, parent_frame, title, value, style):
        card = ttk.Frame(parent_frame, relief='solid', padding="10", style=style)
        card.pack(side='left', padx=10, pady=10, fill='both', expand=True)

        title_label = ttk.Label(card, text=title, font=('Arial', 14))
        title_label.pack()

        value_label = ttk.Label(card, text=value, font=('Arial', 18, 'bold'))
        value_label.pack()

    def create_graphics(self):
        # Frame for graphics and controls
        graph_frame = ttk.Frame(self.frame, padding="10")
        graph_frame.pack(fill='both', expand=True)

        # Create a frame for controls on the left side
        control_frame = ttk.LabelFrame(graph_frame, text="Controls", padding="10")
        control_frame.pack(side='left', fill='y', padx=10)

        # Create a frame for graphics on the center side
        graphics_frame_center = ttk.Frame(graph_frame, padding="10")
        graphics_frame_center.pack(side='left', fill='both', expand=True)

        # Create a frame for graphics on the right side
        graphics_frame_right = ttk.Frame(graph_frame, padding="10")
        graphics_frame_right.pack(side='right', fill='y')

        # Create and place input fields for student and teacher updates
        self.create_control_inputs(control_frame)

        # Create the graphics
        self.create_student_graph(graphics_frame_center)
        self.create_classroom_graph(graphics_frame_right)
        self.create_payment_graph(graphics_frame_right)

    def create_control_inputs(self, parent_frame):
        # Create input fields for students
        student_frame = ttk.LabelFrame(parent_frame, text="Student Controls", padding="10")
        student_frame.pack(pady=10, fill='x')

        ttk.Label(student_frame, text="Student Code Rim:").pack(anchor='w')
        self.student_code_entry = ttk.Entry(student_frame)
        self.student_code_entry.pack(fill='x')

        ttk.Label(student_frame, text="New Price:").pack(anchor='w')
        self.student_price_entry = ttk.Entry(student_frame)
        self.student_price_entry.pack(fill='x')

        ttk.Button(student_frame, text="Update Student Price", command=self.update_student_price).pack(pady=5)

        # Create input fields for teachers
        teacher_frame = ttk.LabelFrame(parent_frame, text="Teacher Controls", padding="10")
        teacher_frame.pack(pady=10, fill='x')

        ttk.Label(teacher_frame, text="Teacher Number:").pack(anchor='w')
        self.teacher_number_entry = ttk.Entry(teacher_frame)
        self.teacher_number_entry.pack(fill='x')

        ttk.Label(teacher_frame, text="New Salary:").pack(anchor='w')
        self.teacher_salary_entry = ttk.Entry(teacher_frame)
        self.teacher_salary_entry.pack(fill='x')

        ttk.Button(teacher_frame, text="Update Teacher Salary", command=self.update_teacher_salary).pack(pady=5)

    def create_student_graph(self, parent_frame):
        # Retrieve student data
        data = self.get_student_data()

        # Prepare data for plotting
        dates, counts = zip(*data.items())

        # Create figure and axis
        fig, ax = plt.subplots(figsize=(5, 4))
        bars = ax.bar(dates, counts, color='skyblue', width=0.4)  # Adjust width here

        # Add border to the bottom of the graph
        for spine in ax.spines.values():
            spine.set_visible(False)
        ax.spines['bottom'].set_visible(True)
        ax.spines['bottom'].set_linewidth(2)  # Set the width of the bottom border
        ax.spines['bottom'].set_color('black')  # Set the color of the bottom border
        ax.spines['bottom'].set_position(('outward', 10))  # Move the border outward

        ax.set_xlabel('Date')
        ax.set_ylabel('Number of Students')
        ax.set_title('Students Registered by Date')
        ax.tick_params(axis='x', rotation=45 )

        # Embed the plot in the Tkinter window
        canvas = FigureCanvasTkAgg(fig, master=parent_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side='top', fill='both', expand=True)

    def create_payment_graph(self, parent_frame):
        # Retrieve payment data
        data = self.get_payment_data()

        # Prepare data for plotting
        labels, values = zip(*data.items())

        # Create figure and axis
        fig, ax = plt.subplots(figsize=(3, 2))
        ax.pie(values, labels=labels, autopct='%1.1f%%', colors=plt.cm.Paired(range(len(labels))))
        ax.set_title('Payment Status')

        # Embed the plot in the Tkinter window
        canvas = FigureCanvasTkAgg(fig, master=parent_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side='top', fill='both', expand=True)

    def create_classroom_graph(self, parent_frame):
        # Retrieve classroom data
        data = self.get_classroom_data()

        # Prepare data for plotting
        classrooms, percentages = zip(*data.items())

        # Create figure and axis
        fig, ax = plt.subplots(figsize=(4, 3))
        ax.pie(percentages, labels=classrooms, autopct='%1.1f%%', colors=plt.cm.Paired(range(len(classrooms))))
        ax.set_title('Percentage of Students in Each Classroom')

        # Embed the plot in the Tkinter window
        canvas = FigureCanvasTkAgg(fig, master=parent_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side='top', fill='both', expand=True)

    def get_total_students(self):
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM students")
        count = cursor.fetchone()[0]
        conn.close()
        return count

    def get_total_teachers(self):
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM teachers")
        count = cursor.fetchone()[0]
        conn.close()
        return count

    def get_total_classrooms(self):
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM classrooms")
        count = cursor.fetchone()[0]
        conn.close()
        return count

    def get_unpaid_students(self):
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM students WHERE price <= 0")
        count = cursor.fetchone()[0]
        conn.close()
        return count

    def get_total_price(self):
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT SUM(price) FROM students")
        total = cursor.fetchone()[0]
        conn.close()
        return f"${total:,.2f}"

    def get_total_salary(self):
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT SUM(salary) FROM teachers")
        total = cursor.fetchone()[0]
        conn.close()
        return f"${total:,.2f}"

    def get_student_data(self):
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT date_of_register, COUNT(*) FROM students GROUP BY date_of_register")
        data = dict(cursor.fetchall())
        conn.close()
        return data

    def get_payment_data(self):
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT CASE WHEN price <= 0 THEN 'Unpaid' ELSE 'Paid' END AS status, COUNT(*) FROM students GROUP BY status")
        data = cursor.fetchall()
        conn.close()
        return dict(data)

    def get_classroom_data(self):
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT classroom, COUNT(*) FROM students GROUP BY classroom")
        data = cursor.fetchall()
        total_students = sum(count for _, count in data)
        classroom_data = {classroom: (count / total_students * 100) for classroom, count in data}
        conn.close()
        return classroom_data

    def update_student_price(self):
        code_rim = self.student_code_entry.get()
        new_price = self.student_price_entry.get()

        if code_rim and new_price:
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            cursor.execute("UPDATE students SET price = ? WHERE code_rim = ?", (new_price, code_rim))
            conn.commit()
            conn.close()

            # Clear input fields
            self.student_code_entry.delete(0, tk.END)
            self.student_price_entry.delete(0, tk.END)

            # Refresh data
            self.create_graphics()

    def update_teacher_salary(self):
        teacher_number = self.teacher_number_entry.get()
        new_salary = self.teacher_salary_entry.get()

        if teacher_number and new_salary:
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            cursor.execute("UPDATE teachers SET salary = ? WHERE number_of_teachers = ?", (new_salary, teacher_number))
            conn.commit()
            conn.close()

            # Clear input fields
            self.teacher_number_entry.delete(0, tk.END)
            self.teacher_salary_entry.delete(0, tk.END)

            # Refresh data
            self.create_graphics()

if __name__ == "__main__":
    root = tk.Tk()
    dashboard = Dashboard(root)
    root.mainloop()
