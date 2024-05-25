import tkinter as tk
from tkinter import messagebox
import sqlite3

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Pet Service App")
        self.geometry("400x300")
        self.create_database()
        self.show_login_register_window()

    def create_database(self):
        self.conn = sqlite3.connect("users.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                user_type TEXT NOT NULL
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
        self.conn.commit()

    def show_login_register_window(self):
        self.clear_window()
        tk.Label(self, text="Welcome to Pet Service App", font=("Helvetica", 16)).pack(pady=20)
        
        tk.Button(self, text="Login", command=self.show_login_window).pack(pady=10)
        tk.Button(self, text="Register", command=self.show_register_window).pack(pady=10)

    def show_login_window(self):
        self.clear_window()
        tk.Label(self, text="Login", font=("Helvetica", 16)).pack(pady=20)

        tk.Label(self, text="Username").pack()
        self.username_entry = tk.Entry(self)
        self.username_entry.pack()

        tk.Label(self, text="Password").pack()
        self.password_entry = tk.Entry(self, show='*')
        self.password_entry.pack()

        tk.Button(self, text="Login", command=self.login).pack(pady=10)
        tk.Button(self, text="Back", command=self.show_login_register_window).pack(pady=10)

    def show_register_window(self):
        self.clear_window()
        tk.Label(self, text="Register", font=("Helvetica", 16)).pack(pady=20)

        tk.Label(self, text="Username").pack()
        self.reg_username_entry = tk.Entry(self)
        self.reg_username_entry.pack()

        tk.Label(self, text="Password").pack()
        self.reg_password_entry = tk.Entry(self, show='*')
        self.reg_password_entry.pack()

        tk.Label(self, text="Select User Type").pack()
        self.user_type = tk.StringVar()
        user_types = ["Ordinary User", "Veterinarian", "Pet Sitter", "Trainer"]
        for user_type in user_types:
            tk.Radiobutton(self, text=user_type, variable=self.user_type, value=user_type).pack()

        tk.Button(self, text="Register", command=self.register).pack(pady=10)
        tk.Button(self, text="Back", command=self.show_login_register_window).pack(pady=10)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        self.cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
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
        user_type = self.user_type.get()  # Get selected user type
        try:
            self.cursor.execute("INSERT INTO users (username, password, user_type) VALUES (?, ?, ?)",
                                (username, password, user_type))
            self.conn.commit()
            messagebox.showinfo("Registration Successful", "User registered successfully.")
            if user_type == "Ordinary User":
                self.show_ordinary_user_profile()
            else:
                self.show_user_type_selection(user_type)
        except sqlite3.IntegrityError:
            messagebox.showerror("Registration Error", "Username already exists.")

    def show_user_type_selection(self, user_type):
        self.clear_window()
        tk.Label(self, text="Select User Type", font=("Helvetica", 16)).pack(pady=20)

        tk.Label(self, text=f"Logged in as: {user_type}").pack()

    def show_ordinary_user_profile(self):
        self.clear_window()
        tk.Label(self, text="Ordinary User Profile", font=("Helvetica", 16)).pack(pady=20)
        tk.Label(self, text="Welcome, Ordinary User!").pack(pady=10)
        
        tk.Button(self, text="My Profile", command=self.show_user_profile).pack(pady=10)

    def show_user_profile(self):
        self.clear_window()
        tk.Label(self, text="My Profile", font=("Helvetica", 16)).pack(pady=20)

        # Show My Pets section
        tk.Label(self, text="My Pets", font=("Helvetica", 14)).pack(pady=10)
        self.pet_name_entry = tk.Entry(self)
        self.pet_name_entry.pack()
        tk.Button(self, text="Add Pet", command=self.add_pet).pack(pady=5)
        tk.Button(self, text="Back", command=self.show_login_register_window).pack(pady=10)
        # List of pets
        self.pet_listbox = tk.Listbox(self)
        self.pet_listbox.pack(pady=10)
        self.populate_pet_list()  # Populate list with user's pets

        

    def add_pet(self):
        pet_name = self.pet_name_entry.get()
        if pet_name:
            self.cursor.execute("INSERT INTO pets (user_id, pet_name) VALUES (?, ?)", (self.logged_in_user_id, pet_name))
            self.conn.commit()
            self.populate_pet_list()
        tk.Button(self, text="Back", command=self.show_login_register_window).pack(pady=10)

    def populate_pet_list(self):
        self.pet_listbox.delete(0, tk.END)
        self.cursor.execute("SELECT pet_name FROM pets WHERE user_id=?", (self.logged_in_user_id,))
        pets = self.cursor.fetchall()
        for pet in pets:
            self.pet_listbox.insert(tk.END, pet[0])
        tk.Button(self, text="Back", command=self.show_login_register_window).pack(pady=10)
            
    def clear_window(self):
        for widget in self.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    app = Application()
    app.mainloop()
