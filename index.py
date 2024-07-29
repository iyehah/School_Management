from tkinter import ttk
from tkinter import *
import sqlite3

class SchoolManagement:
    db_name = 'database.db'  # Ensure this is the correct path

    def __init__(self, window):
        self.wind = window
        self.wind.title('School Management System')
        self.wind.geometry('900x700')
        self.wind.config(bg='#f0f0f0')

        style = ttk.Style()
        style.configure('TLabel', font=('Arial', 12))
        style.configure('TButton', font=('Arial', 12), padding=6)
        style.configure('TEntry', font=('Arial', 12))

        frame = ttk.LabelFrame(self.wind, text='Register new Student', padding=20)
        frame.grid(row=0, column=0, columnspan=3, pady=30, padx=40)

        # Name
        ttk.Label(frame, text='Name: ').grid(row=1, column=0, padx=5, pady=5)
        self.name = ttk.Entry(frame, width=30)
        self.name.focus()
        self.name.grid(row=1, column=1, padx=5, pady=5)

        # Code Rim
        ttk.Label(frame, text='Code Rim: ').grid(row=2, column=0, padx=5, pady=5)
        self.code_rim = ttk.Entry(frame, width=30)
        self.code_rim.grid(row=2, column=1, padx=5, pady=5)

        # Gender
        ttk.Label(frame, text='Gender: ').grid(row=3, column=0, padx=5, pady=5)
        self.gender = ttk.Entry(frame, width=30)
        self.gender.grid(row=3, column=1, padx=5, pady=5)

        # Date of Register
        ttk.Label(frame, text='Date of Register: ').grid(row=4, column=0, padx=5, pady=5)
        self.date_of_register = ttk.Entry(frame, width=30)
        self.date_of_register.grid(row=4, column=1, padx=5, pady=5)

        # Classroom
        ttk.Label(frame, text='Classroom: ').grid(row=5, column=0, padx=5, pady=5)
        self.classroom = ttk.Entry(frame, width=30)
        self.classroom.grid(row=5, column=1, padx=5, pady=5)

        # Price
        ttk.Label(frame, text='Price: ').grid(row=6, column=0, padx=5, pady=5)
        self.price = ttk.Entry(frame, width=30)
        self.price.grid(row=6, column=1, padx=5, pady=5)

        # Number of Agent
        ttk.Label(frame, text='Number of Agent: ').grid(row=7, column=0, padx=5, pady=5)
        self.number_of_agent = ttk.Entry(frame, width=30)
        self.number_of_agent.grid(row=7, column=1, padx=5, pady=5)

        ttk.Button(frame, text='Save Student', command=self.add_student).grid(row=8, columnspan=2, sticky=W+E, pady=10)

        self.message = ttk.Label(text='', foreground='red')
        self.message.grid(row=9, column=0, columnspan=2, sticky=W+E, pady=10)

        self.tree = ttk.Treeview(height=10, columns=('code_rim', 'gender', 'date_of_register', 'classroom', 'price', 'number_of_agent'), show='headings')
        self.tree.grid(row=0, column=40, columnspan=2, pady=20, padx=20)
        self.tree.heading('code_rim', text='Code Rim', anchor=CENTER)
        self.tree.heading('gender', text='Gender', anchor=CENTER)
        self.tree.heading('date_of_register', text='Date of Register', anchor=CENTER)
        self.tree.heading('classroom', text='Classroom', anchor=CENTER)
        self.tree.heading('price', text='Price', anchor=CENTER)
        self.tree.heading('number_of_agent', text='Number of Agent', anchor=CENTER)

        self.tree.column('code_rim', anchor=CENTER, width=100)
        self.tree.column('gender', anchor=CENTER, width=100)
        self.tree.column('date_of_register', anchor=CENTER, width=100)
        self.tree.column('classroom', anchor=CENTER, width=100)
        self.tree.column('price', anchor=CENTER, width=100)
        self.tree.column('number_of_agent', anchor=CENTER, width=100)

        self.get_students()

        # Add DELETE and EDIT buttons below the Treeview widget
        button_frame = Frame(self.wind)
        button_frame.grid(row=11, column=0, columnspan=2, pady=20)

        ttk.Button(button_frame, text='DELETE', command=self.delete_student).grid(row=0, column=0, padx=10)
        ttk.Button(button_frame, text='EDIT', command=self.edit_student).grid(row=0, column=1, padx=10)

    def run_query(self, query, parameters=()):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            result = cursor.execute(query, parameters)
            conn.commit()
        return result

    def get_students(self):
        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)
        query = 'SELECT * FROM students ORDER BY name DESC'
        db_rows = self.run_query(query)
        for row in db_rows:
            self.tree.insert('', 'end', values=(row[1], row[2], row[3], row[4], row[5], row[6], row[7]))

    def add_student(self):
        if self.validate():
            query = 'INSERT INTO students VALUES(NULL, ?, ?, ?, ?, ?, ?, ?)'
            parameters = (self.name.get(), self.code_rim.get(), self.gender.get(), self.date_of_register.get(), self.classroom.get(), self.price.get(), self.number_of_agent.get())
            self.run_query(query, parameters)
            self.message['text'] = f'Student {self.name.get()} added successfully'
            self.clear_fields()
        else:
            self.message['text'] = 'All fields are required'
        self.get_students()

    def delete_student(self):
        self.message['text'] = ''
        try:
            self.tree.item(self.tree.selection())['values'][0]
        except IndexError as e:
            self.message['text'] = 'Please, select a Record'
            return
        name = self.tree.item(self.tree.selection())['values'][0]
        query = 'DELETE FROM students WHERE name = ?'
        self.run_query(query, (name,))
        self.message['text'] = f'Record {name} deleted successfully'
        self.get_students()

    def edit_student(self):
        self.message['text'] = ''
        try:
            self.tree.item(self.tree.selection())['values'][0]
        except IndexError as e:
            self.message['text'] = 'Please, select a Record'
            return
        name = self.tree.item(self.tree.selection())['values'][0]
        code_rim = self.tree.item(self.tree.selection())['values'][1]
        gender = self.tree.item(self.tree.selection())['values'][2]
        date_of_register = self.tree.item(self.tree.selection())['values'][3]
        classroom = self.tree.item(self.tree.selection())['values'][4]
        price = self.tree.item(self.tree.selection())['values'][5]
        number_of_agent = self.tree.item(self.tree.selection())['values'][6]

        self.edit_wind = Toplevel()
        self.edit_wind.title('Edit Student')

        frame = ttk.LabelFrame(self.edit_wind, text='Edit the following fields', padding=20)
        frame.grid(row=0, column=1, pady=20, padx=20)

        ttk.Label(frame, text='Name: ').grid(row=0, column=1, padx=5, pady=5)
        new_name = ttk.Entry(frame, textvariable=StringVar(self.edit_wind, value=name), width=30)
        new_name.grid(row=0, column=2, padx=5, pady=5)

        ttk.Label(frame, text='Code Rim: ').grid(row=1, column=1, padx=5, pady=5)
        new_code_rim = ttk.Entry(frame, textvariable=StringVar(self.edit_wind, value=code_rim), width=30)
        new_code_rim.grid(row=1, column=2, padx=5, pady=5)

        ttk.Label(frame, text='Gender: ').grid(row=2, column=1, padx=5, pady=5)
        new_gender = ttk.Entry(frame, textvariable=StringVar(self.edit_wind, value=gender), width=30)
        new_gender.grid(row=2, column=2, padx=5, pady=5)

        ttk.Label(frame, text='Date of Register: ').grid(row=3, column=1, padx=5, pady=5)
        new_date_of_register = ttk.Entry(frame, textvariable=StringVar(self.edit_wind, value=date_of_register), width=30)
        new_date_of_register.grid(row=3, column=2, padx=5, pady=5)

        ttk.Label(frame, text='Classroom: ').grid(row=4, column=1, padx=5, pady=5)
        new_classroom = ttk.Entry(frame, textvariable=StringVar(self.edit_wind, value=classroom), width=30)
        new_classroom.grid(row=4, column=2, padx=5, pady=5)

        ttk.Label(frame, text='Price: ').grid(row=5, column=1, padx=5, pady=5)
        new_price = ttk.Entry(frame, textvariable=StringVar(self.edit_wind, value=price), width=30)
        new_price.grid(row=5, column=2, padx=5, pady=5)

        ttk.Label(frame, text='Number of Agent: ').grid(row=6, column=1, padx=5, pady=5)
        new_number_of_agent = ttk.Entry(frame, textvariable=StringVar(self.edit_wind, value=number_of_agent), width=30)
        new_number_of_agent.grid(row=6, column=2, padx=5, pady=5)

        ttk.Button(frame, text='Update', command=lambda: self.edit_records(new_name.get(), name, new_code_rim.get(), code_rim, new_gender.get(), gender, new_date_of_register.get(), date_of_register, new_classroom.get(), classroom, new_price.get(), price, new_number_of_agent.get(), number_of_agent)).grid(row=7, column=2, sticky=W, pady=10)
        self.edit_wind.mainloop()

    def edit_records(self, new_name, name, new_code_rim, code_rim, new_gender, gender, new_date_of_register, date_of_register, new_classroom, classroom, new_price, price, new_number_of_agent, number_of_agent):
        query = 'UPDATE students SET name = ?, code_rim = ?, gender = ?, date_of_register = ?, classroom = ?, price = ?, number_of_agent = ? WHERE name = ? AND code_rim = ? AND gender = ? AND date_of_register = ? AND classroom = ? AND price = ? AND number_of_agent = ?'
        parameters = (new_name, new_code_rim, new_gender, new_date_of_register, new_classroom, new_price, new_number_of_agent, name, code_rim, gender, date_of_register, classroom, price, number_of_agent)
        self.run_query(query, parameters)
        self.edit_wind.destroy()
        self.message['text'] = f'Record {name} updated successfully'
        self.get_students()

    def validate(self):
        return (len(self.name.get()) != 0 and len(self.code_rim.get()) != 0 and len(self.gender.get()) != 0 and len(self.date_of_register.get()) != 0 and len(self.classroom.get()) != 0 and len(self.price.get()) != 0 and len(self.number_of_agent.get()) != 0)

    def clear_fields(self):
        self.name.delete(0, END)
        self.code_rim.delete(0, END)
        self.gender.delete(0, END)
        self.date_of_register.delete(0, END)
        self.classroom.delete(0, END)
        self.price.delete(0, END)
        self.number_of_agent.delete(0, END)

if __name__ == '__main__':
    window = Tk()
    application = SchoolManagement(window)
    window.mainloop()
