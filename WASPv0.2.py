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
width=800
height=650
root.geometry(f"{width}x{height}") # Window size.
root.title("WASP Statistic Tool") # Window title.

# Title of the software tool.
labelTitle = tk.Label(root,
                 text="WASP Statistic Tool",
                 font=("Helvetica", 36, "bold"))
labelTitle.grid(row=0, column=0, columnspan=2, pady=15)

# Description of the software tool.
labelDesc = tk.Label(root,
                text="Designed by Ben Sohanpal, Alex Read, Tony Dalziel, Jeremy Roy, Maksim Sics, Yosef Berezovskiy",
                font=("Helvetica", 14))
labelDesc.grid(row=1, column=0, columnspan=2, padx=15, pady=30)

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

# A sub panel to house metrics
metricPanel = tk.Frame(rightPanel)
metricPanel.grid(row=8, column=0)

""" Edit metrics """
idwfVal = StringVar(metricPanel)
idwfVal.set("")
idwfLabel = tk.Label(metricPanel,
    text="IDWF:",
    font=("Helvetica", 14, "bold"))
idwfLabel.grid(row=0, column=0)
idwfEntry = tk.Entry(metricPanel, textvariable=idwfVal)
idwfEntry.grid(row=0, column=1)

mirVal = StringVar(metricPanel)
mirVal.set("")
mirLabel = tk.Label(metricPanel,
    text="Max Infiltration Rate:",
    font=("Helvetica", 14, "bold"))
mirLabel.grid(row=1, column=0)
mirEntry = tk.Entry(metricPanel, textvariable=mirVal)
mirEntry.grid(row=1, column=1)

tradeEffVal = StringVar(metricPanel)
tradeEffVal.set("")
tradeEffLabel = tk.Label(metricPanel,
    text="Trade Effluent:",
    font=("Helvetica", 14, "bold"))
tradeEffLabel.grid(row=2, column=0)
tradeEffEntry = tk.Entry(metricPanel, textvariable=tradeEffVal)
tradeEffEntry.grid(row=2, column=1)

perCapitaVal = StringVar(metricPanel)
perCapitaVal.set("")
perCapitaLabel = tk.Label(metricPanel,
    text="Per Capita Domestic Flow:",
    font=("Helvetica", 14, "bold"))
perCapitaLabel.grid(row=3, column=0)
perCapitaEntry = tk.Entry(metricPanel, textvariable=perCapitaVal)
perCapitaEntry.grid(row=3, column=1)

popCatchVal = StringVar(metricPanel)
popCatchVal.set("")
popCatchLabel = tk.Label(metricPanel,
    text="Population Catchment:",
    font=("Helvetica", 14, "bold"))
popCatchLabel.grid(row=4, column=0)
popCatchEntry = tk.Entry(metricPanel, textvariable=popCatchVal)
popCatchEntry.grid(row=4, column=1)

bodVal = StringVar(metricPanel)
bodVal.set("")
bodLabel = tk.Label(metricPanel,
    text="BOD:",
    font=("Helvetica", 14, "bold"))
bodLabel.grid(row=5, column=0)
bodEntry = tk.Entry(metricPanel, textvariable=bodVal)
bodEntry.grid(row=5, column=1)

""" FUNCTIONALITY OUTPUT -- Left Panel """
leftPanel = tk.Frame(root)
leftPanel.grid(row=2, column=1)

outputLabel = tk.Label(leftPanel,
    text="Output Results:",
    font=("Helvetica", 28, "bold"))
outputLabel.grid(row=1, column=0)
outputMon = tk.Text(leftPanel, height=30, width=30, yscrollcommand=True)
outputMon.grid(row=2, column=0)

# Quit program button.
quitButton = tk.Button(root, text="Quit Program", command=quitProg)
quitButton.grid(row=3, column=0)

try:
    print("Program started...")
    root.mainloop()
    print("Program closed...")
except Exception as e:
    print(f"Failed... Error generated:\n{e}\n{traceback.print_exc()}")
        
