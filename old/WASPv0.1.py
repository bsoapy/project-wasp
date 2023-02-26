import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
import traceback
import os

""" TODO Find out what buttons we need. """

def upload():
    try:
        result = findFile(root)
        filepathBox.delete("1.0", "end")
        filepathBox.insert("1.0", result)
    except Exception as e:
        messagebox.showerror(title="Error Uploading File.", message="Sorry, there was an error uploading file.")
        return False

def findFile(root):
    """ A function that allows the user to select files from anywhere
on there computer system."""
    #root.withdraw() # Hide the main window
    file_path = filedialog.askopenfilename(
        initialdir = "/",
        title = "Select file",
        filetypes = (("Excel files", "*.xlsx"), ("all files", "*.*")))
    return file_path

def calculate():
    print("calculating")

def quitProg():
    """Quitting the program."""
    if messagebox.askyesno(title="Quit Program", message="Are you sure wish to quit?\nUnsaved changes will be lost."):   
        root.quit()
        print("Program closed...")
        os.sys.exit()
    else:
        return False
        
root = tk.Tk() # Create a window.
width=725
height=500
root.geometry(f"{width}x{height}") # Window size.
root.title("WASP Statistic Tool") # Window title.

# Title of the software tool.
labelTitle = tk.Label(root,
                 text="WASP Statistic Tool",
                 font=("Helvetica", 36, "bold"))
labelTitle.pack(pady=20)

# Description of the software tool.
labelDesc = tk.Label(root,
                text="Designed by Ben Sohanpal, Alex Read, Tony Dalziel, Jeremy Roy, Maksim Sics, Yosef Berezovskiy",
                font=("Helvetica", 14))
labelDesc.pack(pady=50)

# Upload stw file button.
uploadButton = tk.Button(root, text="Upload STW", command=upload)
uploadButton.pack()
# Entry box.
filepathBox = tk.Text(root, width=20, height=1)
filepathBox.pack()

# Calculate button for PE, DWF and FFT.
calculateButton = tk.Button(root, text="Calculate", command=calculate)
calculateButton.pack()
# Quit program button.
quitButton = tk.Button(root, text="Quit Program", command=quitProg)
quitButton.pack()

try:
    print("Program started...")
    root.mainloop()
    print("Program closed...")
except Exception as e:
    print(f"Failed... Error generated:\n{e}\n{traceback.print_exc()}")
        
