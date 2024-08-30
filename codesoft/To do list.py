from tkinter import *
from tkinter import messagebox
import sqlite3 as sql

class Task:
    def __init__(self, title):
        self.title = title
        self.completed = False

class TaskList:
    def __init__(self, master):
        self.master = master
        self.tasks = []
        self.task_field = Entry(master, width=40)
        self.task_listbox = Listbox(master, width=70, height=9)
        self.init_ui()

    def init_ui(self):
        Label(self.master, text="TO-DO LIST\nEnter Task Title:").grid(row=0, column=0, padx=20, pady=10)
        self.task_field.grid(row=0, column=1, padx=10, pady=10)

        Button(self.master, text="Add", width=10, command=self.add_task).grid(row=1, column=0, padx=10, pady=10)
        Button(self.master, text="Remove", width=10, command=self.remove_task).grid(row=1, column=2, padx=10, pady=10)
        Button(self.master, text="Mark as Complete", width=15, command=self.mark_as_complete).grid(row=1, column=1, padx=10, pady=10)
        
        self.task_listbox.grid(row=3, column=0, columnspan=3, padx=20, pady=10)

    def add_task(self):
        task_string = self.task_field.get().strip()
        if task_string:
            task = Task(task_string)
            self.tasks.append(task)
            self.update_listbox()
            self.task_field.delete(0, 'end')
        else:
            messagebox.showinfo('Error', 'Task field is empty.')

    def mark_as_complete(self):
        try:
            index = self.task_listbox.curselection()[0]
            task = self.tasks[index]
            task.completed = True
            self.update_listbox()
        except IndexError:
            messagebox.showinfo('Error', 'No task selected.')

    def remove_task(self):
        try:
            index = self.task_listbox.curselection()[0]
            self.tasks.pop(index)
            self.update_listbox()
        except IndexError:
            messagebox.showinfo('Error', 'No task selected.')

    def update_listbox(self):
        self.task_listbox.delete(0, 'end')
        for task in self.tasks:
            self.task_listbox.insert('end', task.title)
            if task.completed:
                self.task_listbox.itemconfig('end', {'fg': 'green'})

if __name__ == "__main__":
    guiWindow = Tk()
    guiWindow.title("To-Do List")
    guiWindow.geometry("550x350+550+275")
    guiWindow.resizable(0, 0)

    task_list = TaskList(guiWindow)
    guiWindow.mainloop()