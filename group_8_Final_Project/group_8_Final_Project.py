# Import Statements
import tkinter as tk
from tkinter import messagebox

# Input_Window Class
class Input_Window(tk.Toplevel):
    def __init__(self, parent, saved_items_listbox):
        super().__init__(parent)
        self.title("Megaventory")
        self.saved_items_listbox = saved_items_listbox
        self.text()

    def text(self):
        self.year_label = tk.Label(self, text="Enter the year:")
        self.year_label.pack()

        self.year_entry = tk.Entry(self)
        self.year_entry.pack()

        self.name_label = tk.Label(self, text="Enter the name:")
        self.name_label.pack()

        self.name_entry = tk.Entry(self)
        self.name_entry.pack()

        self.description_label = tk.Label(self, text="Enter the price:")
        self.description_label.pack()

        self.description_entry = tk.Entry(self)
        self.description_entry.pack()

        self.exit_button = tk.Button(self, text="Exit", command=self.master.quit)
        self.exit_button.pack(side="right")

        self.save_button = tk.Button(self, text="Save", command=self.save)
        self.save_button.pack()

        self.delete_button = tk.Button(self, text="Delete", command=self.delete)
        self.delete_button.pack()

        self.view_button = tk.Button(self, text="View", command=self.view)
        self.view_button.pack()

    def save(self):
        year_input = self.year_entry.get()
        name_input = self.name_entry.get()
        description_input = self.description_entry.get()

        if not all((year_input, name_input, description_input)):
            messagebox.showwarning("Empty Input", "Please enter a year, name, and price")
            return

        try:
            year = int(year_input)
        except:
            messagebox.showwarning("Input Error", "Please enter a valid year")
            return

        try:
            price = float(description_input)
        except:
            messagebox.showwarning("Input Error", "Please enter a valid price")
            return

        item = f"{year} {name_input} ${price:.2f}"

        with open("items.txt", "a") as f:
            f.write(item + "\n")
        self.saved_items_listbox.insert(tk.END, item)
        self.year_entry.delete(0, tk.END)
        self.name_entry.delete(0, tk.END)
        self.description_entry.delete(0, tk.END)

        self.destroy()

    def delete(self):
        selection = self.saved_items_listbox.curselection()
        if not selection:
            return

        index = selection[0]
        item = self.saved_items_listbox.get(index)

        self.saved_items_listbox.delete(index)

        with open("items.txt", "r") as f:
            items = f.readlines()

        with open("items.txt", "w") as f:
            for i in items:
                if i.strip() != item:
                    f.write(i)

    def view(self):
        selection = self.saved_items_listbox.curselection()
        if not selection:
            return

        index = selection[0]
        item = self.saved_items_listbox.get(index)
        messagebox.showinfo("View Item", item)

# Main Application (root)
root = tk.Tk()
container = tk.Frame(root)
container.pack(side="top", fill="both", expand=True)

saved_items_listbox = tk.Listbox(container)
saved_items_listbox.pack(side="bottom", fill="both", expand=True)

with open("items.txt") as f:
    for item in f:
        saved_items_listbox.insert(tk.END, item.strip())

input_window = Input_Window(root, saved_items_listbox)

root.mainloop()
