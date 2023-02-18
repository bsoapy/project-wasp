# Declarations and constants
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from tkinter import StringVar
import traceback
import os

STWs = [
    "Ampney St Peter",
    "Chipping Norton"
]

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

def quitProg():
    """Quitting the program."""
    if messagebox.askyesno(title="Quit Program", message="Are you sure wish to quit?\nUnsaved changes will be lost."):   
        root.quit()
        print("Program closed...")
        os.sys.exit()
    else:
        return False
        
def recallSTW(chosen):
    print(f"Chosen STW is {chosen.get()}.")
    # TODO Database functionality to recall STW info.
    
def report(chosen):
    recallSTW(chosen)
    print("Report generated.")
    # TODO Functionality to generate excel report.
    
root = tk.Tk() # Create a window.
width=670
height=500
root.geometry(f"{width}x{height}") # Window size.
root.title("WASP Statistic Tool") # Window title.

# Title of the software tool.
labelTitle = tk.Label(root,
                 text="WASP Statistic Tool",
                 font=("Helvetica", 36, "bold"))
labelTitle.grid(row=0, column=0, columnspan=2, pady=20)

# Description of the software tool.
labelDesc = tk.Label(root,
                text="Designed by Ben Sohanpal, Alex Read, Tony Dalziel, Jeremy Roy, Maksim Sics, Yosef Berezovskiy",
                font=("Helvetica", 14))
labelDesc.grid(row=1, column=0, columnspan=2, padx=15, pady=50)

""" BUTTONS & FUNCTIONALITY -- Right Panel """
rightPanel = tk.Frame(root)
rightPanel.grid(row=2, column=0)

# Upload stw file button.
uploadButton = tk.Button(rightPanel, text="Upload STW", command=upload)
uploadButton.grid(row=0, column=0, padx=10)

# Entry box.
filepathBox = tk.Text(rightPanel, width=20, height=1)
filepathBox.grid(row=0, column=1, padx=10)

orLabel = tk.Label(rightPanel,
                    text="OR",
                    font=("Helvetica", 14, "bold"))
orLabel.grid(row=1, column=0)

# Label to for STW drop down.
STWlabel = tk.Label(rightPanel,
                    text="Select a loaded STW:",
                    font=("Helvetica", 14, "bold"))
STWlabel.grid(row=2, column=0)

# STW Dropdown list.
chosenSTW = StringVar(rightPanel) # Default & selected STW.
chosenSTW.set(STWs[0])
STWdropdown = tk.OptionMenu(rightPanel, chosenSTW, *STWs)
STWdropdown.grid(row=2, column=1)

# Simply a line break
_blank = tk.Label(rightPanel,
                  text="-------------------------------",
                  font=("Helvetica", 14))
_blank.grid(row=3, column=0)

# View STW button.
viewButton = tk.Button(rightPanel, text="View STW", command=lambda: recallSTW(chosenSTW))
viewButton.grid(row=4, column=0)

# Generate report button.
reportButton = tk.Button(rightPanel, text="Generate Report", command=lambda: report(chosenSTW))
reportButton.grid(row=5, column=0)

_blank = tk.Label(rightPanel,
                  text="-------------------------------",
                  font=("Helvetica", 14))
_blank.grid(row=6, column=0)

# Label to show editing metrics.
STWlabel = tk.Label(rightPanel,
                    text="Edit STW metrics:",
                    font=("Helvetica", 14, "bold"))
STWlabel.grid(row=7, column=0)

# A sub panel to house 
rightSubPanel = tk.Frame(rightPanel)



""" FUNCTIONALITY OUTPUT -- Left Panel """

# Quit program button.
quitButton = tk.Button(root, text="Quit Program", command=quitProg)
#quitButton.pack()

try:
    print("Program started...")
    root.mainloop()
    print("Program closed...")
except Exception as e:
    print(f"Failed... Error generated:\n{e}\n{traceback.print_exc()}")
        
