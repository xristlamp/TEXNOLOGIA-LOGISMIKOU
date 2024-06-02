import tkinter as tk
from tkinter import messagebox, simpledialog
import sqlite3
import hashlib
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os



class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Pet Service App")
        self.geometry("600x400")
        self.create_database()
        self.show_login_register_window()
        self.logged_in_user_location = None  # Initialize the location
        self.custom_questions = {}

    def create_database(self):
        db_file_path = os.path.join(os.getcwd(), "users.db")  # Database file in the current working directory
        self.conn = sqlite3.connect(db_file_path)
        self.cursor = self.conn.cursor()
        
        # Remove the DROP TABLE IF EXISTS users statement
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                user_type TEXT NOT NULL,
                email TEXT NOT NULL,
                location TEXT NOT NULL
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS pets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                pet_name TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS services (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                vet_id INTEGER NOT NULL,
                service_name TEXT NOT NULL,
                service_description TEXT,
                FOREIGN KEY (vet_id) REFERENCES users(id)
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS appointments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pet_id INTEGER NOT NULL,
                vet_id INTEGER NOT NULL,
                appointment_date TEXT NOT NULL,
                appointment_time TEXT NOT NULL,
                description TEXT,
                notes TEXT,
                FOREIGN KEY (pet_id) REFERENCES pets(id),
                FOREIGN KEY (vet_id) REFERENCES users(id)
            )
        """)
           # Check if the 'location' column exists, and if not, add it
        self.cursor.execute("PRAGMA table_info(users)")
        columns = [info[1] for info in self.cursor.fetchall()]
        if 'location' not in columns:
            self.cursor.execute("ALTER TABLE users ADD COLUMN location TEXT")
            self.conn.commit()

        self.conn.commit()

    def open_ai_chat(self):
        self.show_ai_chat_help()

    def show_login_register_window(self):
        self.clear_window()
        tk.Label(self, text="Welcome to Pet Service App", font=("Helvetica", 20), bg='lightblue').pack(pady=20)
        
        tk.Button(self, text="Login", command=self.show_login_window, bg='green', fg='white').pack(pady=10)
        tk.Button(self, text="Register", command=self.show_register_window, bg='blue', fg='white').pack(pady=10)
        tk.Button(self, text="Live Chat", command=self.open_ai_chat, bg='grey', fg='white').pack(pady=10)

    def show_login_window(self):
        self.clear_window()
        tk.Label(self, text="Login", font=("Helvetica", 20), bg='lightblue').pack(pady=20)

        tk.Label(self, text="Username").pack()
        self.username_entry = tk.Entry(self)
        self.username_entry.pack()

        tk.Label(self, text="Password").pack()
        self.password_entry = tk.Entry(self, show='*')
        self.password_entry.pack()

        tk.Button(self, text="Login", command=self.login, bg='green', fg='white').pack(pady=10)
        tk.Button(self, text="Back", command=self.show_login_register_window, bg='red', fg='white').pack(pady=10)
        tk.Button(self, text="Live Chat", command=self.show_ai_chat_help, bg='grey', fg='white').pack(pady=10)

    def show_register_window(self):
        self.clear_window()
        tk.Label(self, text="Register", font=("Helvetica", 20), bg='lightblue').pack(pady=20)

        tk.Label(self, text="Username").pack()
        self.reg_username_entry = tk.Entry(self)
        self.reg_username_entry.pack()

        tk.Label(self, text="Password").pack()
        self.reg_password_entry = tk.Entry(self, show='*')
        self.reg_password_entry.pack()

        tk.Label(self, text="Emaiil").pack()
        self.reg_email_entry = tk.Entry(self)
        self.reg_email_entry.pack()

        tk.Label(self, text="Select User Type").pack()
        self.user_type = tk.StringVar()
        user_types = ["Ordinary User", "Veterinarian", "Pet Sitter", "Trainer"]
        for user_type in user_types:
            tk.Radiobutton(self, text=user_type, variable=self.user_type, value=user_type).pack()

        # Add Location Selection
        tk.Label(self, text="Location").pack()
        self.location_var = tk.StringVar()
        self.location_var.set("Athens")  # default value
        cities = ["Patras", "Athens", "Thessaloniki", "Heraklion", "Larissa", "Volos", "Ioannina", "Chania", "Rhodes", "Kalamata"]
        tk.OptionMenu(self, self.location_var, *cities).pack()

        tk.Button(self, text="Register", command=self.register, bg='blue', fg='white').pack(pady=10)
        tk.Button(self, text="Back", command=self.show_login_register_window, bg='red', fg='white').pack(pady=10)
        tk.Button(self, text="Live Chat", command=self.show_ai_chat_help, bg='grey', fg='white').pack(pady=10)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        self.cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, hashed_password))
        user = self.cursor.fetchone()
        if user:
            self.logged_in_user_id = user[0]  # Store the user's ID
            user_type = user[3]
            if user_type == "Ordinary User":
                self.show_ordinary_user_profile()
            elif user_type == "Veterinarian":
                self.show_veterinarian_profile()
            elif user_type == "Pet Sitter":
                self.show_pet_sitter_profile()
            elif user_type == "Trainer":
                self.show_trainer_profile()
        else:
            messagebox.showerror("Login Error", "Invalid username or password.")

    def register(self):
        username = self.reg_username_entry.get()
        password = self.reg_password_entry.get()
        email = self.reg_email_entry.get()
        user_type = self.user_type.get()  # Get selected user type
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        location = self.location_var.get()  # Get the selected location

        try:
            self.cursor.execute("INSERT INTO users (username, password, user_type, email, location) VALUES (?, ?, ?, ?, ?)",
                                (username, hashed_password, user_type, email,location))
            self.conn.commit()
            messagebox.showinfo("Registration Successful", "User registered successfully.")
            if user_type == "Ordinary User":
                self.show_ordinary_user_profile()
            elif user_type == "Veterinarian":
                self.show_veterinarian_profile()
            elif user_type == "Pet Sitter":
                self.show_pet_sitter_profile()
            elif user_type == "Trainer":
                self.show_trainer_profile()
        except sqlite3.IntegrityError:
            messagebox.showerror("Registration Error", "Username already exists.")

    def show_ordinary_user_profile(self):
        self.clear_window()
        tk.Label(self, text="Ordinary User Profile", font=("Helvetica", 20), bg='lightblue').pack(pady=20)
        tk.Label(self, text="Welcome, Ordinary User!").pack(pady=10)
        
        tk.Button(self, text="Add Pet", command=self.show_add_pet_window, bg='green', fg='white').pack(pady=10)
        tk.Button(self, text="My Pets", command=self.show_user_profile, bg='blue', fg='white').pack(pady=10)
        tk.Button(self, text="Book Appointment", command=self.show_book_appointment_window, bg='purple', fg='white').pack(pady=10)
        tk.Button(self, text="Back", command=self.show_login_register_window, bg='red', fg='white').pack(pady=10)
        tk.Button(self, text="Live Chat", command=self.show_ai_chat_help, bg='grey', fg='white').pack(pady=10)

    def show_veterinarian_profile(self):
        self.clear_window()
        tk.Label(self, text="Veterinarian Profile", font=("Helvetica", 20), bg='lightblue').pack(pady=20)
        tk.Label(self, text="Welcome, Veterinarian!").pack(pady=10)
        
        tk.Button(self, text="Manage Services", command=self.show_manage_services_window, bg='green', fg='white').pack(pady=10)
        tk.Button(self, text="Appointments", command=self.show_appointments_window, bg='blue', fg='white').pack(pady=10)
        tk.Button(self, text="Back", command=self.show_login_register_window, bg='red', fg='white').pack(pady=10)
        tk.Button(self, text="Live Chat", command=self.show_ai_chat_help, bg='grey', fg='white').pack(pady=10)

    def show_manage_services_window(self):
        self.clear_window()
        tk.Label(self, text="Manage Services", font=("Helvetica", 20), bg='lightblue').pack(pady=20)

        tk.Label(self, text="Service Name").pack()
        self.service_name_entry = tk.Entry(self)
        self.service_name_entry.pack()

        tk.Label(self, text="Description").pack()
        self.service_description_entry = tk.Entry(self)
        self.service_description_entry.pack()

        tk.Button(self, text="Add Service", command=self.add_service, bg='green', fg='white').pack(pady=10)
        tk.Button(self, text="Back", command=self.show_veterinarian_profile, bg='red', fg='white').pack(pady=10)
        tk.Button(self, text="Live Chat", command=self.show_ai_chat_help, bg='grey', fg='white').pack(pady=10)

    def add_service(self):
        service_name = self.service_name_entry.get()
        service_description = self.service_description_entry.get()
        if service_name and service_description:
            try:
                self.cursor.execute("INSERT INTO services (vet_id, service_name, service_description) VALUES (?, ?, ?)",
                                    (self.logged_in_user_id, service_name, service_description))
                self.conn.commit()
                messagebox.showinfo("Add Service", "Service added successfully.")
            except sqlite3.Error as e:
                messagebox.showerror("Add Service Error", str(e))
        else:
            messagebox.showerror("Add Service Error", "Please enter service name and description.")

    def show_appointments_window(self):
        self.clear_window()
        tk.Label(self, text="Appointments", font=("Helvetica", 20), bg='lightblue').pack(pady=20)
        self.appointment_listbox = tk.Listbox(self)
        self.appointment_listbox.pack(pady=10)
        self.populate_appointment_list()
        tk.Button(self, text="Add Note", command=self.add_note_to_appointment, bg='green', fg='white').pack(pady=10)
        tk.Button(self, text="Send Email", command=self.send_email_to_patient, bg='blue', fg='white').pack(pady=10)
        tk.Button(self, text="Back", command=self.show_veterinarian_profile, bg='red', fg='white').pack(pady=10)
        tk.Button(self, text="Live Chat", command=self.show_ai_chat_help, bg='grey', fg='white').pack(pady=10)

    def populate_appointment_list(self):
        self.appointment_listbox.delete(0, tk.END)
        try:
            self.cursor.execute("""
                SELECT a.id, p.pet_name, a.appointment_date, a.appointment_time, a.description
                FROM appointments a
                JOIN pets p ON a.pet_id = p.id
                WHERE a.vet_id=?
            """, (self.logged_in_user_id,))
            appointments = self.cursor.fetchall()
            for appt in appointments:
                self.appointment_listbox.insert(tk.END, f"{appt[1]} - {appt[2]} {appt[3]}: {appt[4]}")
        except sqlite3.Error as e:
            messagebox.showerror("Fetch Appointments Error", str(e))

    def add_note_to_appointment(self):
        selected_appointment = self.appointment_listbox.curselection()
        if selected_appointment:
            appointment_id = self.appointment_listbox.get(selected_appointment).split('-')[0].strip()
            note = simpledialog.askstring("Add Note", "Enter your note:")
            if note:
                try:
                    self.cursor.execute("UPDATE appointments SET notes = ? WHERE id = ?", (note, appointment_id))
                    self.conn.commit()
                    messagebox.showinfo("Add Note", "Note added successfully.")
                except sqlite3.Error as e:
                    messagebox.showerror("Add Note Error", str(e))
        else:
            messagebox.showwarning("Selection Error", "Please select an appointment to add a note.")

    def send_email_to_patient(self):
        selected_appointment = self.appointment_listbox.curselection()
        if selected_appointment:
            appointment_id = self.appointment_listbox.get(selected_appointment).split('-')[0].strip()
            self.cursor.execute("""
                SELECT u.email
                FROM appointments a
                JOIN pets p ON a.pet_id = p.id
                JOIN users u ON p.user_id = u.id
                WHERE a.id = ?
            """, (appointment_id,))
            email = self.cursor.fetchone()
            if email:
                email = email[0]
                subject = simpledialog.askstring("Send Email", "Enter the email subject:")
                body = simpledialog.askstring("Send Email", "Enter the email body:")
                if subject and body:
                    try:
                        self.send_email(email, subject, body)
                        messagebox.showinfo("Send Email", "Email sent successfully.")
                    except Exception as e:
                        messagebox.showerror("Send Email Error", str(e))
                else:
                    messagebox.showwarning("Input Error", "Please enter both subject and body.")
            else:
                messagebox.showerror("Email Error", "Could not find patient's email.")
        else:
            messagebox.showwarning("Selection Error", "Please select an appointment to send an email.")

    def send_email(self, to_email, subject, body):
        from_email = "your_email@example.com"
        from_password = "your_password"

        msg = MIMEMultipart()
        msg['From'] = from_email
        msg['To'] = to_email
        msg['Subject'] = subject

        msg.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP('smtp.example.com', 587)
        server.starttls()
        server.login(from_email, from_password)
        text = msg.as_string()
        server.sendmail(from_email, to_email, text)
        server.quit()

    def show_user_profile(self):
        self.clear_window()
        tk.Label(self, text="My Pets", font=("Helvetica", 20), bg='lightblue').pack(pady=20)

        # List of pets
        self.pet_listbox = tk.Listbox(self)
        self.pet_listbox.pack(pady=10)
        self.populate_pet_list()  # Populate list with user's pets

        tk.Button(self, text="Back", command=self.show_ordinary_user_profile, bg='red', fg='white').pack(pady=10)

    def show_add_pet_window(self):
        self.clear_window()
        tk.Label(self, text="Add Pet", font=("Helvetica", 20), bg='lightblue').pack(pady=20)

        tk.Label(self, text="Pet Name").pack()
        self.pet_name_entry = tk.Entry(self)
        self.pet_name_entry.pack()

        tk.Button(self, text="Add Pet", command=self.add_pet, bg='green', fg='white').pack(pady=10)
        tk.Button(self, text="Back", command=self.show_ordinary_user_profile, bg='red', fg='white').pack(pady=10)
    def show_pet_sitter_profile(self):
        self.clear_window()
        tk.Label(self, text="Pet Sitter Profile", font=("Helvetica", 20), bg='lightblue').pack(pady=20)
        tk.Label(self, text="Welcome, Pet Sitter!").pack(pady=10)
        
        tk.Button(self, text="Manage Services", command=self.show_manage_services_window, bg='green', fg='white').pack(pady=10)
        tk.Button(self, text="Appointments", command=self.show_appointments_window, bg='blue', fg='white').pack(pady=10)
        tk.Button(self, text="Back", command=self.show_login_register_window, bg='red', fg='white').pack(pady=10)

    def show_trainer_profile(self):
        self.clear_window()
        tk.Label(self, text="Trainer Profile", font=("Helvetica", 20), bg='lightblue').pack(pady=20)
        tk.Label(self, text="Welcome, Trainer!").pack(pady=10)
        
        tk.Button(self, text="Manage Services", command=self.show_manage_services_window, bg='green', fg='white').pack(pady=10)
        tk.Button(self, text="Appointments", command=self.show_appointments_window, bg='blue', fg='white').pack(pady=10)
        tk.Button(self, text="Back", command=self.show_login_register_window, bg='red', fg='white').pack(pady=10)


    def add_pet(self):
        pet_name = self.pet_name_entry.get()
        if pet_name:
            try:
                self.cursor.execute("INSERT INTO pets (user_id, pet_name) VALUES (?, ?)", (self.logged_in_user_id, pet_name))
                self.conn.commit()
                messagebox.showinfo("Add Pet", "Pet added successfully.")
            except sqlite3.Error as e:
                messagebox.showerror("Add Pet Error", str(e))
        else:
            messagebox.showerror("Add Pet Error", "Please enter a pet name.")
        tk.Button(self, text="Back", command=self.show_ordinary_user_profile, bg='red', fg='white').pack(pady=10)

    def show_book_appointment_window(self):
        self.clear_window()
        tk.Label(self, text="Book Appointment", font=("Helvetica", 20), bg='lightblue').pack(pady=20)

        tk.Label(self, text="Select Pet").pack()
        self.pet_var = tk.StringVar(self)
        pets = self.get_user_pets()
        if pets:
            self.pet_var.set(pets[0])
            tk.OptionMenu(self, self.pet_var, *pets).pack()

            tk.Label(self, text="Select Service Provider").pack()
            self.provider_var = tk.StringVar(self)
            providers = self.get_service_providers()
            if providers:
                self.provider_var.set(providers[0])
                tk.OptionMenu(self, self.provider_var, *providers).pack()

                tk.Label(self, text="Appointment Date (YYYY-MM-DD)").pack()
                self.appointment_date_entry = tk.Entry(self)
                self.appointment_date_entry.pack()

                tk.Label(self, text="Appointment Time (HH:MM)").pack()
                self.appointment_time_entry = tk.Entry(self)
                self.appointment_time_entry.pack()

                tk.Label(self, text="Description").pack()
                self.appointment_description_entry = tk.Entry(self)
                self.appointment_description_entry.pack()

                tk.Button(self, text="Book Appointment", command=self.book_appointment, bg='green', fg='white').pack(pady=10)
            else:
                tk.Label(self, text="No service providers available.").pack()
        else:
            tk.Label(self, text="No pets available.").pack()

        tk.Button(self, text="Back", command=self.show_ordinary_user_profile, bg='red', fg='white').pack(pady=10)

    def get_user_pets(self):
        self.cursor.execute("SELECT pet_name FROM pets WHERE user_id=?", (self.logged_in_user_id,))
        pets = self.cursor.fetchall()
        return [pet[0] for pet in pets]

    def get_veterinarians(self):
        self.cursor.execute("SELECT username FROM users WHERE user_type='Veterinarian'")
        vets = self.cursor.fetchall()
        return [vet[0] for vet in vets]

    def get_service_providers(self):
        self.cursor.execute("SELECT username, user_type FROM users WHERE user_type IN ('Veterinarian', 'Pet Sitter', 'Trainer')")
        providers = self.cursor.fetchall()
        return [f"{provider[0]} ({provider[1]})" for provider in providers]

    def book_appointment(self):
        pet_name = self.pet_var.get()
        provider_info = self.provider_var.get()
        appointment_date = self.appointment_date_entry.get()
        appointment_time = self.appointment_time_entry.get()
        description = self.appointment_description_entry.get()

        self.cursor.execute("SELECT id FROM pets WHERE pet_name=? AND user_id=?", (pet_name, self.logged_in_user_id))
        pet_id = self.cursor.fetchone()[0]
        
        provider_name = provider_info.split(' (')[0]  # Extract the provider's username
        self.cursor.execute("SELECT id FROM users WHERE username=?", (provider_name,))
        provider_id = self.cursor.fetchone()[0]

        try:
            self.cursor.execute("INSERT INTO appointments (pet_id, vet_id, appointment_date, appointment_time, description) VALUES (?, ?, ?, ?, ?)",
                                (pet_id, provider_id, appointment_date, appointment_time, description))
            self.conn.commit()
            messagebox.showinfo("Book Appointment", "Appointment booked successfully.")
            self.show_ordinary_user_profile()
        except sqlite3.Error as e:
            messagebox.showerror("Book Appointment Error", str(e))

        tk.Button(self, text="Back", command=self.show_ordinary_user_profile, bg='red', fg='white').pack(pady=10)

    def populate_pet_list(self):
        self.pet_listbox.delete(0, tk.END)
        try:
            self.cursor.execute("SELECT pet_name FROM pets WHERE user_id=?", (self.logged_in_user_id,))
            pets = self.cursor.fetchall()
            for pet in pets:
                self.pet_listbox.insert(tk.END, pet[0])
        except sqlite3.Error as e:
            messagebox.showerror("Fetch Pets Error", str(e))

    def clear_window(self):
        for widget in self.winfo_children():
            widget.destroy()

    def show_ai_chat_help(self):
        chat_window = tk.Toplevel(self)
        chat_window.title("AI Chat Help")
        chat_window.geometry("400x400")

        chat_display = tk.Text(chat_window, height=15, width=50)
        chat_display.pack(pady=10)

        chat_entry = tk.Entry(chat_window, width=40)
        chat_entry.pack(pady=10)

        predefined_questions = {
            "How can I book an appointment?": "You can book an appointment by going to the 'Book Appointment' section.",
            "Where are you located?": "We are located in Athens, Greece.",
            "What services do you offer?": "We offer a variety of services including veterinary care, pet sitting, and training.",
            "How to contact support?": "You can contact support by calling our hotline at 123-456-7890 or emailing support@example.com.",
            "What are your working hours?": "Our working hours are Monday to Friday, 9:00 AM to 5:00 PM.",
            "How can I cancel an appointment?": "To cancel an appointment, please contact us via phone or email at least 24 hours in advance.",
            "Do you offer emergency services?": "Yes, we offer emergency services. Please call our emergency hotline for assistance.",
            "How can I add a pet?": "You can add a pet by navigating to the 'Add Pet' section and entering the required details.",
            "How to find nearby veterinarians?": "You can find nearby veterinarians by using the 'Find Vets Near Me' feature.",
            "How to search for trainers?": "Use the 'Find Trainers Near Me' feature to search for trainers based on your location."
        }

        keywords = {
            "appointment": "How can I book an appointment?",
            "location": "Where are you located?",
            "services": "What services do you offer?",
            "support": "How to contact support?",
            "hours": "What are your working hours?",
            "cancel": "How can I cancel an appointment?",
            "emergency": "Do you offer emergency services?",
            "add pet": "How can I add a pet?",
            "veterinarians": "How to find nearby veterinarians?",
            "trainers": "How to search for trainers?"
        }

        def handle_predefined_question(question):
            chat_display.insert(tk.END, f"You: {question}\n")
            response = predefined_questions.get(question, "I'm sorry, I don't understand that question.")
            chat_display.insert(tk.END, f"AI: {response}\n")

        for question in predefined_questions.keys():
            tk.Button(chat_window, text=question, command=lambda q=question: handle_predefined_question(q)).pack(pady=5)

        def send_message():
            message = chat_entry.get()
            if message:
                chat_display.insert(tk.END, f"You: {message}\n")
                response = None
                if message in predefined_questions:
                    response = predefined_questions[message]
                else:
                    for keyword, question in keywords.items():
                        if keyword in message.lower():
                            response = predefined_questions[question]
                            break
                if not response:
                    response = "Sorry, I don't understand that question."
                chat_display.insert(tk.END, f"AI: {response}\n")
                chat_entry.delete(0, tk.END)

        send_button = tk.Button(chat_window, text="Send", command=send_message)
        send_button.pack(pady=10)

if __name__ == "__main__":
    app = Application()
    app.mainloop()
