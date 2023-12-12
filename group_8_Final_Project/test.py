import tkinter as tk
#from PIL import ImageTk, Image
from tkinter import messagebox

class Input_Window(tk.Toplevel):
    def __init__(self, parent, saved_items_listbox):
        super().__init__(parent)
        self.title("Megaventory")
        self.saved_items_listbox = saved_items_listbox
        self.configure(bg="#4169e1")  # Set background color to very light blue
        self.geometry("400x500")  # Set window size
        self.title_label = tk.Label(self, text="Your Inventory", font=("Helvetica", 20), bg="#CCE5FF")
        self.title_label.pack(pady=10)
        # Uncomment and replace the following line with your actual image code when you have the image
        # self.image_label = tk.Label(self, image=your_image, bg="#CCE5FF", borderwidth=2, relief="solid")
        # self.image_label.pack(pady=10)

        self.create_buttons()

    def create_buttons(self):
            button_frame = tk.Frame(self, bg="#4169e1")
            button_frame.pack(pady=10)

            buttons = [
                ("Profit Calculator", self.open_profit_calculator),
                ("View Inventory", self.view),
                ("Pass Sold", self.pass_sold),
                ("Need Something", self.need_something)
            ]

            for text, command in buttons:
                btn = tk.Button(button_frame, text=text, command=command, bg="#4CAF50", fg="white", width=15, height=3, font=(15))
                btn.grid(row=len(button_frame.winfo_children()) // 2, column=len(button_frame.winfo_children()) % 2, padx=10, pady=5)

            self.exit_button = tk.Button(self, text="Exit", command=self.master.quit, bg="red", fg="white")
            self.exit_button.pack(side="right")





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

        with open("sold.txt", "w") as f:
            for i in items:
                if i.strip() != item:
                    f.write(i)

    def view(self):
        profit_window = ProfitCalculator(self)
        profit_window.grab_set()
        profit_window.focus_set()
        profit_window.wait_window()

    def open_profit_calculator(self):
        profit_window = ProfitCalculator(self)
        profit_window.grab_set()
        profit_window.focus_set()
        profit_window.wait_window()

    def pass_sold(self):
        # Add functionality for "Pass Sold" button
        pass
        sold_window = Sold(self)
        sold_window.grab_set()
        sold_window.focus_set()
        sold_window.wait_window()

    def need_something(self):
        # Add functionality for "Need Something" button
        pass

class Sold(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Sold items")
        self.parent = parent
         
        self.geometry("400x400")
        self.display_sold()  
        self.back()
    
    def display_sold(self):
        with open("sold.txt","r") as f:
            sold_inventory = f.readlines()
        
    
    def back(self):
        self.back_button = tk.Button(self, text="Return to home screen", command=Input_Window)
        self.back_button.pack()
    


class ProfitCalculator(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Profit Calculator")
        self.parent = parent
        self.configure(bg="#4169e1")  # Set background color to very light blue
        self.geometry("400x300")  # Set window size
        self.create_widgets()

    def create_widgets(self):
        self.title_label = tk.Label(self, text="Comic Title:")
        self.title_label.pack()

        self.title_entry = tk.Entry(self)
        self.title_entry.pack()

        self.issue_label = tk.Label(self, text="Issue Number:")
        self.issue_label.pack()

        self.issue_entry = tk.Entry(self)
        self.issue_entry.pack()

        self.purchase_label = tk.Label(self, text="Purchase Price:")
        self.purchase_label.pack()

        self.purchase_entry = tk.Entry(self)
        self.purchase_entry.pack()

        self.sell_label = tk.Label(self, text="Selling Price:")
        self.sell_label.pack()

        self.sell_entry = tk.Entry(self)
        self.sell_entry.pack()

        self.calculate_button = tk.Button(self, text="Calculate Profit", command=self.calculate_profit_and_save)
        self.calculate_button.pack()

        self.result_label = tk.Label(self, text="")
        self.result_label.pack()

    def calculate_profit_and_save(self):
        try:
            title = self.title_entry.get()
            issue_number = int(self.issue_entry.get())
            purchase_price = float(self.purchase_entry.get())
            selling_price = float(self.sell_entry.get())
            profit = selling_price - purchase_price

            # Save the information


            item = f"Title: {title}, Issue: {issue_number}, Purchase Price: ${purchase_price:.2f}, Selling Price: ${selling_price:.2f}, Profit: ${profit:.2f}"

            with open("items.txt", "a") as f:
                f.write(item + "\n")

            # Display the profit
            self.result_label.config(text=f"Profit: ${profit:.2f}")
        except ValueError:
            messagebox.showwarning("Input Error", "Please enter valid numerical values for prices")



root = tk.Tk()
root.title("Your Inventory")
root.configure(bg="green")  # Set background color to blue
root.geometry("600x400")  # Set window size
root.state('withdrawn')

saved_items_listbox = tk.Listbox(root, bg="white", fg="black")
saved_items_listbox.pack(side="bottom", fill="both", expand=True)

with open("items.txt") as f:
    for item in f:
        saved_items_listbox.insert(tk.END, item.strip())

input_window = Input_Window(root, saved_items_listbox)
root.mainloop()
