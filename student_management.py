from tkinter import ttk, Tk, Frame, StringVar, Toplevel, END
import sqlite3

class StudentManagement:
    def __init__(self, frame):
        self.frame = frame

        # Create main frame with grid layout
        self.main_frame = Frame(self.frame)
        self.main_frame.grid(row=0, column=0, sticky='nsew')
        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)

        # Create two blocks
        self.first_block = Frame(self.main_frame)
        self.first_block.grid(row=0, column=0, sticky='ns')
        self.second_block = Frame(self.main_frame)
        self.second_block.grid(row=0, column=1, sticky='nsew')

        # Configure column weight to make the second block expand
        self.main_frame.grid_columnconfigure(0, weight=0)
        self.main_frame.grid_columnconfigure(1, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=1)

        # Registration frame
        self.registration_frame = Frame(self.first_block, padx=10, pady=10)
        self.registration_frame.pack(side='top', fill='x')
        self.registration_frame.grid_rowconfigure(7, weight=1)
        
        # Control buttons frame
        self.control_buttons_frame = Frame(self.first_block, padx=10, pady=10)
        self.control_buttons_frame.pack(side='bottom', fill='x')
        
        # Input fields and save button in registration frame
        ttk.Label(self.registration_frame, text='Name: ').grid(row=1, column=0, padx=5, pady=5, sticky='w')
        self.name = ttk.Entry(self.registration_frame, width=30)
        self.name.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(self.registration_frame, text='Code Rim: ').grid(row=2, column=0, padx=5, pady=5, sticky='w')
        self.code_rim = ttk.Entry(self.registration_frame, width=30)
        self.code_rim.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(self.registration_frame, text='Gender: ').grid(row=3, column=0, padx=5, pady=5, sticky='w')
        self.gender = ttk.Combobox(self.registration_frame, values=['Male', 'Female'], width=27)
        self.gender.grid(row=3, column=1, padx=5, pady=5)

        ttk.Label(self.registration_frame, text='Date of Register: ').grid(row=4, column=0, padx=5, pady=5, sticky='w')
        self.date_of_register = ttk.Entry(self.registration_frame, width=30)
        self.date_of_register.grid(row=4, column=1, padx=5, pady=5)

        ttk.Label(self.registration_frame, text='Classroom: ').grid(row=5, column=0, padx=5, pady=5, sticky='w')
        self.classroom = ttk.Combobox(self.registration_frame, values=['1As', '2As', '3As', '4As', '5C', '5D', '6C', '6D', '7C', '7D', '5O', '5A', '6O', '6A', '7O', '7A'], width=27)
        self.classroom.grid(row=5, column=1, padx=5, pady=5)

        ttk.Label(self.registration_frame, text='Price: ').grid(row=6, column=0, padx=5, pady=5, sticky='w')
        self.price = ttk.Entry(self.registration_frame, width=30)
        self.price.grid(row=6, column=1, padx=5, pady=5)

        ttk.Label(self.registration_frame, text='Number of Agent: ').grid(row=7, column=0, padx=5, pady=5, sticky='w')
        self.number_of_agent = ttk.Entry(self.registration_frame, width=30)
        self.number_of_agent.grid(row=7, column=1, padx=5, pady=5)

        # Add button
        ttk.Button(self.registration_frame, text='Add', command=self.add_student).grid(row=8, columnspan=2, pady=10, sticky='we')

        # Treeview and control buttons in second block
        self.search_frame = Frame(self.second_block, padx=10, pady=10)
        self.search_frame.pack(side='top', fill='x')

        ttk.Label(self.search_frame, text='Search by Code Rim: ').pack(side='left', padx=5)
        self.search_entry = ttk.Entry(self.search_frame, width=30)
        self.search_entry.pack(side='left', padx=5)
        ttk.Button(self.search_frame, text='Search', command=self.search_student).pack(side='left', padx=5)

        self.tree = ttk.Treeview(self.second_block, height=15, columns=('id', 'name', 'code_rim', 'gender', 'date_of_register', 'classroom', 'price', 'number_of_agent'), show='headings')
        self.tree.pack(side='top', fill='both', expand=True)
        self.tree.heading('id', text='ID')
        self.tree.heading('name', text='Name')
        self.tree.heading('code_rim', text='Code Rim')
        self.tree.heading('gender', text='Gender')
        self.tree.heading('date_of_register', text='Date of Register')
        self.tree.heading('classroom', text='Classroom')
        self.tree.heading('price', text='Price')
        self.tree.heading('number_of_agent', text='Number of Agent')

        self.tree.column('id', width=50)
        self.tree.column('name', width=100)
        self.tree.column('code_rim', width=100)
        self.tree.column('gender', width=100)
        self.tree.column('date_of_register', width=100)
        self.tree.column('classroom', width=100)
        self.tree.column('price', width=100)
        self.tree.column('number_of_agent', width=100)

        # Buttons below the Treeview
        self.control_buttons_frame = Frame(self.second_block, padx=10, pady=10)
        self.control_buttons_frame.pack(side='bottom', fill='x')
        
        ttk.Button(self.control_buttons_frame, text='Edit', command=self.edit_student).pack(side='left', padx=5)
        ttk.Button(self.control_buttons_frame, text='Delete', command=self.delete_student).pack(side='left', padx=5)
        ttk.Button(self.control_buttons_frame, text='View', command=self.view_student).pack(side='left', padx=5)

        self.message = ttk.Label(self.second_block, text='', foreground='red')
        self.message.pack(pady=10)

        self.get_students()

    def run_query(self, query, parameters=()):
        with sqlite3.connect('database.db') as conn:
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
            self.tree.insert('', 'end', values=row)

    def search_student(self):
        search_query = self.search_entry.get()
        query = 'SELECT * FROM students WHERE code_rim LIKE ?'
        parameters = (f'%{search_query}%',)
        db_rows = self.run_query(query, parameters)
        self.tree.delete(*self.tree.get_children())
        for row in db_rows:
            self.tree.insert('', 'end', values=row)

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
            student_id = self.tree.item(self.tree.selection())['values'][0]
        except IndexError:
            self.message['text'] = 'Please, select a record'
            return
        query = 'DELETE FROM students WHERE id = ?'
        self.run_query(query, (student_id,))
        self.message['text'] = f'Record {student_id} deleted successfully'
        self.get_students()

    def edit_student(self):
        self.message['text'] = ''
        try:
            selected_item = self.tree.item(self.tree.selection())
            student_id = selected_item['values'][0]
            name = selected_item['values'][1]
            code_rim = selected_item['values'][2]
            gender = selected_item['values'][3]
            date_of_register = selected_item['values'][4]
            classroom = selected_item['values'][5]
            price = selected_item['values'][6]
            number_of_agent = selected_item['values'][7]
        except IndexError:
            self.message['text'] = 'Please, select a record'
            return

        self.edit_wind = Toplevel()
        self.edit_wind.title(f'Edit Student {student_id}')
        
        # Creating and positioning input fields and save button
        ttk.Label(self.edit_wind, text='Name: ').grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.edit_name = ttk.Entry(self.edit_wind, width=30)
        self.edit_name.grid(row=0, column=1, padx=5, pady=5)
        self.edit_name.insert(0, name)

        ttk.Label(self.edit_wind, text='Code Rim: ').grid(row=1, column=0, padx=5, pady=5, sticky='w')
        self.edit_code_rim = ttk.Entry(self.edit_wind, width=30)
        self.edit_code_rim.grid(row=1, column=1, padx=5, pady=5)
        self.edit_code_rim.insert(0, code_rim)

        ttk.Label(self.edit_wind, text='Gender: ').grid(row=2, column=0, padx=5, pady=5, sticky='w')
        self.edit_gender = ttk.Combobox(self.edit_wind, values=['Male', 'Female'], width=27)
        self.edit_gender.grid(row=2, column=1, padx=5, pady=5)
        self.edit_gender.set(gender)

        ttk.Label(self.edit_wind, text='Date of Register: ').grid(row=3, column=0, padx=5, pady=5, sticky='w')
        self.edit_date_of_register = ttk.Entry(self.edit_wind, width=30)
        self.edit_date_of_register.grid(row=3, column=1, padx=5, pady=5)
        self.edit_date_of_register.insert(0, date_of_register)

        ttk.Label(self.edit_wind, text='Classroom: ').grid(row=4, column=0, padx=5, pady=5, sticky='w')
        self.edit_classroom = ttk.Combobox(self.edit_wind, values=['1As', '2As', '3As', '4As', '5C', '5D', '6C', '6D', '7C', '7D', '5O', '5A', '6O', '6A', '7O', '7A'], width=27)
        self.edit_classroom.grid(row=4, column=1, padx=5, pady=5)
        self.edit_classroom.set(classroom)

        ttk.Label(self.edit_wind, text='Price: ').grid(row=5, column=0, padx=5, pady=5, sticky='w')
        self.edit_price = ttk.Entry(self.edit_wind, width=30)
        self.edit_price.grid(row=5, column=1, padx=5, pady=5)
        self.edit_price.insert(0, price)

        ttk.Label(self.edit_wind, text='Number of Agent: ').grid(row=6, column=0, padx=5, pady=5, sticky='w')
        self.edit_number_of_agent = ttk.Entry(self.edit_wind, width=30)
        self.edit_number_of_agent.grid(row=6, column=1, padx=5, pady=5)
        self.edit_number_of_agent.insert(0, number_of_agent)

        # Save button
        ttk.Button(self.edit_wind, text='Save Changes', command=lambda: self.save_changes(student_id)).grid(row=7, columnspan=2, pady=10)

    def save_changes(self, student_id):
        query = '''
        UPDATE students SET name = ?, code_rim = ?, gender = ?, date_of_register = ?, classroom = ?, price = ?, number_of_agent = ?
        WHERE id = ?
        '''
        parameters = (
            self.edit_name.get(),
            self.edit_code_rim.get(),
            self.edit_gender.get(),
            self.edit_date_of_register.get(),
            self.edit_classroom.get(),
            self.edit_price.get(),
            self.edit_number_of_agent.get(),
            student_id
        )
        self.run_query(query, parameters)
        self.edit_wind.destroy()
        self.message['text'] = f'Record {student_id} updated successfully'
        self.get_students()

    def view_student(self):
        self.message['text'] = ''
        try:
            student_id = self.tree.item(self.tree.selection())['values'][0]
        except IndexError:
            self.message['text'] = 'Please, select a record'
            return

        # Create a new window to display the student details
        self.view_wind = Toplevel()
        self.view_wind.title(f'View Student {student_id}')

        # Query to fetch the student details
        query = 'SELECT * FROM students WHERE id = ?'
        student = self.run_query(query, (student_id,)).fetchone()

        if student:
            ttk.Label(self.view_wind, text=f'Name: {student[1]}').pack(padx=5, pady=5)
            ttk.Label(self.view_wind, text=f'Code Rim: {student[2]}').pack(padx=5, pady=5)
            ttk.Label(self.view_wind, text=f'Gender: {student[3]}').pack(padx=5, pady=5)
            ttk.Label(self.view_wind, text=f'Date of Register: {student[4]}').pack(padx=5, pady=5)
            ttk.Label(self.view_wind, text=f'Classroom: {student[5]}').pack(padx=5, pady=5)
            ttk.Label(self.view_wind, text=f'Price: {student[6]}').pack(padx=5, pady=5)
            ttk.Label(self.view_wind, text=f'Number of Agent: {student[7]}').pack(padx=5, pady=5)
        else:
            ttk.Label(self.view_wind, text='Student not found').pack(padx=5, pady=5)

    def validate(self):
        return all([
            self.name.get(),
            self.code_rim.get(),
            self.gender.get(),
            self.date_of_register.get(),
            self.classroom.get(),
            self.price.get(),
            self.number_of_agent.get()
        ])

    def clear_fields(self):
        self.name.delete(0, END)
        self.code_rim.delete(0, END)
        self.gender.set('')
        self.date_of_register.delete(0, END)
        self.classroom.set('')
        self.price.delete(0, END)
        self.number_of_agent.delete(0, END)

if __name__ == '__main__':
    window = Tk()
    window.title('School Management System')
    app = StudentManagement(window)
    window.mainloop()
