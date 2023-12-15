import tkinter as tk
from tkinter import simpledialog, messagebox


class ViewInventory(tk.Toplevel):
    def __init__(self, parent, saved_items_listbox):
        super().__init__(parent)
        self.title("Comic Keeper")
        self.parent = parent
        self.saved_items_listbox = saved_items_listbox

        self.geometry("400x400")
        self.create_widgets()

    def create_widgets(self):
        self.title_label = tk.Label(self, text="Inventory", font=("Helvetica", 20))
        self.title_label.pack(pady=10)

        self.search_label = tk.Label(self, text="Search:")
        self.search_label.pack()

        self.search_entry = tk.Entry(self)
        self.search_entry.pack()

        self.search_button = tk.Button(self, text="Search", command=self.search_inventory)
        self.search_button.pack()

        self.items_listbox = tk.Listbox(self, bg="white", fg="black")
        self.items_listbox.pack(side="bottom", fill="both", expand=True)

        self.mark_sold_button = tk.Button(self, text="Mark as Sold", command=self.mark_as_sold)
        self.mark_sold_button.pack()

        self.back_button = tk.Button(self, text="Back", command=self.destroy)
        self.back_button.pack()

        self.load_inventory()

    def load_inventory(self):
        with open("items.txt", "r") as f:
            items = f.readlines()
        for item in items:
            self.items_listbox.insert(tk.END, item.strip())

    def search_inventory(self):
        search_term = self.search_entry.get().lower()
        self.items_listbox.delete(0, tk.END)
        with open("items.txt", "r") as f:
            items = f.readlines()
        for item in items:
            if search_term in item.lower():
                self.items_listbox.insert(tk.END, item.strip())

    def mark_as_sold(self):
        selection = self.items_listbox.curselection()
        if not selection:
            messagebox.showwarning("Selection Error", "Please select an item to mark as sold.")
            return

        index = selection[0]
        item = self.items_listbox.get(index)

        with open("sold.txt", "a") as f:
            f.write(item + "\n")

        self.items_listbox.delete(index)

        with open("items.txt", "r") as f:
            items = f.readlines()

        with open("items.txt", "w") as f:
            for i in items:
                if i.strip() != item:
                    f.write(i)

        messagebox.showinfo("Success", "Item marked as sold.")


class Input_Window(tk.Toplevel):
    def __init__(self, parent, saved_items_listbox):
        super().__init__(parent)
        self.title("Comic Keeper")
        self.saved_items_listbox = saved_items_listbox
        self.configure(bg="#4169e1")
        self.geometry("401x500")
        self.title_label = tk.Label(self, text="Comic Keeper", font=("Helvetica", 20), bg="#CCE5FF")
        self.title_label.pack(pady=10)

        self.create_buttons()

    def create_buttons(self):
        button_frame = tk.Frame(self, bg="#4169e1")
        button_frame.pack(pady=10)

        buttons = [
            ("add new comic", self.open_profit_calculator),
            ("View Inventory", self.view_inventory),
            ("Pass Sold", self.pass_sold),
        ]

        for text, command in buttons:
            btn = tk.Button(button_frame, text=text, command=command, bg="#4CAF50", fg="white", width=15, height=3, font=(15))
            btn.grid(row=len(button_frame.winfo_children()) // 2, column=len(button_frame.winfo_children()) % 2, padx=10, pady=5)

        self.exit_button = tk.Button(self, text="Exit", command=self.master.quit, bg="red", fg="white")
        self.exit_button.pack(side="right")

    def view_inventory(self):
        view_inventory_window = ViewInventory(self, self.saved_items_listbox)
        view_inventory_window.grab_set()
        view_inventory_window.focus_set()

    def open_profit_calculator(self):
        profit_window = ProfitCalculator(self)
        profit_window.grab_set()
        profit_window.focus_set()
        profit_window.wait_window()

    def pass_sold(self):
        sold_window = Sold(self)
        sold_window.grab_set()
        sold_window.focus_set()
        sold_window.wait_window()



class ProfitCalculator(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("add new comic")
        self.parent = parent

        self.geometry("400x300")
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

        self.calculate_button = tk.Button(self, text="Calculate Profit", command=self.calculate_gross_profit)
        self.calculate_button.pack()

        self.save_button = tk.Button(self, text="Save to Inventory", command=self.save_item)
        self.save_button.pack()

        self.back_button = tk.Button(self, text="Back", command=self.destroy)
        self.back_button.pack()

        self.result_label = tk.Label(self, text="")
        self.result_label.pack()

    def calculate_gross_profit(self):
        try:
            purchase_price = float(self.purchase_entry.get())
            selling_price = float(self.sell_entry.get())
            gross_profit = selling_price - purchase_price
            self.result_label.config(text=f"Gross Profit: ${gross_profit:.2f}")
        except ValueError:
            messagebox.showwarning("Input Error", "Please enter valid numerical values for prices")

    def save_item(self):
        title = self.title_entry.get()
        issue_number = self.issue_entry.get()
        purchase_price = self.purchase_entry.get()
        selling_price = self.sell_entry.get()

        item = f"Title: {title}, Issue: {issue_number}, Purchase Price: ${purchase_price}, Selling Price: ${selling_price}"

        with open("items.txt", "a") as f:
            f.write(item + "\n")

        self.result_label.config(text="Item saved to inventory")


class Sold(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Sold items")
        self.parent = parent

        self.geometry("400x400")
        self.display_sold()
        self.create_delete_button()
        self.back()

    def display_sold(self):
        with open("sold.txt", "r") as f:
            sold_inventory = f.readlines()

        # Display the sold inventory in a Listbox
        self.sold_listbox = tk.Listbox(self, selectmode=tk.MULTIPLE)
        self.sold_listbox.pack(fill="both", expand=True)

        for item in sold_inventory:
            self.sold_listbox.insert(tk.END, item.strip())

    def create_delete_button(self):
        delete_button = tk.Button(self, text="Delete Selected", command=self.delete_selected)
        delete_button.pack()

    def delete_selected(self):
        selected_indices = self.sold_listbox.curselection()

        if not selected_indices:
            messagebox.showwarning("Selection Error", "Please select item(s) to delete.")
            return

        items_to_delete = [self.sold_listbox.get(index) for index in selected_indices]

        with open("sold.txt", "r") as f:
            sold_inventory = f.readlines()

        with open("sold.txt", "w") as f:
            for item in sold_inventory:
                if item.strip() not in items_to_delete:
                    f.write(item)

        self.sold_listbox.delete(0, tk.END)
        with open("sold.txt", "r") as f:
            updated_sold_inventory = f.readlines()
            for item in updated_sold_inventory:
                self.sold_listbox.insert(tk.END, item.strip())

        messagebox.showinfo("Delete Success", "Selected item(s) deleted.")

    def back(self):
        self.back_button = tk.Button(self, text="Back", command=self.destroy)
        self.back_button.pack()


root = tk.Tk()
root.title("Your Inventory")
root.configure(bg="green")
root.geometry("600x400")
root.state('withdrawn')

saved_items_listbox = tk.Listbox(root, bg="white", fg="black")
saved_items_listbox.pack(side="bottom", fill="both", expand=True)

input_window = Input_Window(root, saved_items_listbox)
root.mainloop()
