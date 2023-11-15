#Owen Stackhouse This is an application built for a store to keep track of its inventory. 
#It will ask you for the year of the product, the name of the product, and the price of the 
#product. You will store this information, and whenever the product becomes outdated, you 
#can remove it from your records and repeat the process. Reduce, recycle, and repeat!


#This is where the import statements exist for the program to use them. 
import tkinter as tk
from PIL import ImageTk, Image
from tkinter import messagebox

#This is where it makes the window for the GUI application where it displays the input devices 
class Input_Window(tk.Toplevel):
    def __init__(self, parent, saved_items_listbox):
        super().__init__(parent)
        self.title("Megaventory")
        self.saved_items_listbox = saved_items_listbox
        self.text()

    
    #This is where it displays for one the image that's on there that also has the option for
    #  if the application can't get access over the ill say the name of the application. And 
    # this is where it has  all the input devices as entering the year, entering the title, 
    # entering the price, and all the buttons. 

    def text(self):
        try:
            img = Image.open("c:\\Users\\owen stacknouse\\Downloads\\Screenshot.jpg")
            img = img.resize((260, 140), Image.ANTIALIAS)
            photo = ImageTk.PhotoImage(img)
            self.img_label = tk.Label(self, image=photo)
            self.img_label.image = photo
            self.img_label.pack()
        except:
            self.img_label = tk.Label(self, text="Megaventory")
            self.img_label.pack()

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


    #This is when you fill out the input devices and per save this is where the information 
    # goes into will save those words into the items.txt file 
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


    # This is where it goes to delete it when you highlight the saved item and it goes into
    #  the text file and deletes it. 
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

    
    # this is what happens when you push the view button when you highlight over  it and push
    #  view it'll select that extracted from the txt file and let you examine it through a window.
    def view(self):
        
        selection = self.saved_items_listbox.curselection()
        
        index = selection[0]
        item = self.saved_items_listbox.get(index)
        if not selection:
            return
        
        messagebox.showinfo("View Item", item)


#This is where the list for where the items pop up exists and the image goes on top of that list 
# Same thing happens from up there if the file cannot be Founders not recognized it will display a 
# backup message saying your inventory because this is what I called your inventory.
root = tk.Tk()
container = tk.Frame(root)
container.pack(side="top", fill="both", expand=True)

try:
    image = Image.open("c:\\Users\\owen stacknouse\\Downloads\\screen.jpg")
    resized_image = image.resize((280 , 120), Image.ANTIALIAS)
    photo = ImageTk.PhotoImage(resized_image)
    image_label = tk.Label(container, image=photo)
    image_label.pack(side="top", fill="both")
except FileNotFoundError:
    image_label = tk.Label(container, text="your inventory")
    image_label.pack(side="top", fill="both")

saved_items_listbox = tk.Listbox(container)
saved_items_listbox.pack(side="bottom", fill="both", expand=True)

with open("items.txt") as f:
    for item in f:
        saved_items_listbox.insert(tk.END, item.strip())

input_window = Input_Window(root, saved_items_listbox)

root.mainloop()