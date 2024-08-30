import string
import secrets
import sqlite3
from tkinter import *
from tkinter import messagebox

class PasswordGenerator:
    def __init__(self):
        self.chars = string.ascii_letters + string.digits + string.punctuation

    def generate_password(self, length):
        return ''.join(secrets.choice(self.chars) for _ in range(length))

class GUI:
    def __init__(self, root):
        self.root = root
        self.root.title('Password Generator')
        self.root.geometry('500x350')
        self.root.resizable(False, False)

        self.password_generator = PasswordGenerator()
        self.create_widgets()

    def create_widgets(self):
        Label(self.root, text="Enter User Name:", font='Arial 12 bold', bg='white', fg='darkred').grid(row=0, column=0, padx=10, pady=10, sticky=W)
        self.username_entry = Entry(self.root, font='Arial 12', bd=3, relief='ridge')
        self.username_entry.grid(row=0, column=1, padx=10, pady=10, sticky=W+E)

        Label(self.root, text="Enter Password Length:", font='Arial 12 bold', bg='white', fg='darkred').grid(row=1, column=0, padx=10, pady=10, sticky=W)
        self.length_entry = Entry(self.root, font='Arial 12', bd=3, relief='ridge')
        self.length_entry.grid(row=1, column=1, padx=10, pady=10, sticky=W+E)

        Button(self.root, text="GENERATE PASSWORD", bd=3, padx=10, pady=5, font='Arial 12 bold', fg='yellow', bg='green', command=self.generate_password).grid(row=2, column=1, padx=10, pady=10, sticky=W+E)

        Label(self.root, text="Generated Password:", font='Arial 12 bold', bg='white', fg='darkblue').grid(row=3, column=0, padx=10, pady=10, sticky=W)
        self.generated_password_entry = Entry(self.root, font='Arial 12', bd=3, relief='ridge', fg='black')
        self.generated_password_entry.grid(row=3, column=1, padx=10, pady=10, sticky=W+E)

        Button(self.root, text="ACCEPT", bd=3, padx=10, pady=5, font='Arial 12 bold italic', fg='green', bg='white', command=self.accept_password).grid(row=4, column=1, padx=10, pady=10, sticky=W+E)

        Button(self.root, text="RESET", bd=3, padx=10, pady=5, font='Arial 12 bold italic', fg='red', bg='white', command=self.reset_fields).grid(row=5, column=1, padx=10, pady=10, sticky=W+E)

    def generate_password(self):
        try:
            length = int(self.length_entry.get())
            if length < 4:
                messagebox.showerror("Error", "Password must be at least 4 characters long")
                return

            password = self.password_generator.generate_password(length)
            self.generated_password_entry.delete(0, END)
            self.generated_password_entry.insert(0, password)

        except ValueError:
            messagebox.showerror("Error", "Invalid password length")

    def accept_password(self):
        username = self.username_entry.get()
        password = self.generated_password_entry.get()

        if not username:
            messagebox.showerror("Error", "Username cannot be empty")
            return

        try:
            with sqlite3.connect("users.db") as db:
                cursor = db.cursor()
                cursor.execute("CREATE TABLE IF NOT EXISTS users (Username TEXT PRIMARY KEY, GeneratedPassword TEXT)")

                cursor.execute("INSERT INTO users (Username, GeneratedPassword) VALUES (?, ?)", (username, password))
                db.commit()
                messagebox.showinfo("Success", "Password generated and stored successfully.")

        except sqlite3.Error as e:
            messagebox.showerror("Error", str(e))

    def reset_fields(self):
        self.username_entry.delete(0, END)
        self.length_entry.delete(0, END)
        self.generated_password_entry.delete(0, END)

if __name__ == '__main__':
    root = Tk()
    app = GUI(root)
    root.mainloop()