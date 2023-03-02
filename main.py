# Modules
import tkinter as tk
from tkinter import messagebox
from tkinter import StringVar
import traceback
import os
import json
from stw_calc import *
import pandas as pd

def refresh():
    """Refresh the list of STWs."""
    STWS = []
    data = json.load(open('stw_data.json'))
    for i in data:
        STWS.append(data[i]["name"])

#load STW data from JSON file
data = json.load(open('stw_data.json'))
global  STWS
STWS = []
refresh()


for i in data:
    STWS.append(data[i]["name"])

def quitProg():
    """Quitting the program."""
    if messagebox.askyesno(title="Quit Program", message="Are you sure wish to quit?\nUnsaved changes will be lost."):   
        root.quit()
        print("Program closed...")
        os.sys.exit()
    else:
        return False

def recallSTW(name):
    #get all vaues for the STW from JSON file
    data = json.load(open('stw_data.json'))
    STW_data = {}
    for i in data:
        
        if data[i]["name"] == name:
            STW_data = data[i]
            break

    if STW_data == {}:
        messagebox.showerror(title="Error Viewing STW", message="Sorry, there was a problem loading this STW.")
        return None
    
    return STW_data
    
def report(name):
    #get data from JSON file with STW name
    data = recallSTW(name)

    #load data into seperate variables 

    #dry weather infiltration
    try:
        i_dwf = data["IDWF"]
    except:
        i_dwf = "Not Input"

    #max infiltration rate
    try:
        i_max = data["MIR"]
    except:
        i_max = "Not Input"


    #trade eff flow
    try:
        e = data["TE"]
    except:
        e = "Not Input"
  

    #per capita domestc flow 
    try:
        g = data["PCDF"]
    except:
        g = "Not Input"

    #catchment population
    try:
        p = data["POPC"]
    except:
        p = "Not Input"
    
    old_pe = data["O_PE"]
    old_dwf = data["O_DWF"]
    old_fft = data["O_FFT"]

    

    #calculate the values
    try:
        fft = calculate_fft(p,g,i_max,e)
    
    except:
        fft = "Could not calculate (need more metrics)"
    try:
        dwf = calculate_dwf(p,g,i_dwf,e)
    except:
        dwf = "Could not calculate (need more metrics)"

    try:
        pe = calculate_pe(fft)
    except:
        pe = "Could not calculate (need more metrics)"


    

        

    #create a popup that displays the values, the old values and the difference

    #it should also have a save to excel button

    popup = tk.Toplevel(root)
    popup.resizable(False, False)
    width=600
    height=350
    popup.geometry(f"{width}x{height}") # Window size.
    popup.title(f"Report for {name}") # Window title.

    #create a label for each metric
    labelFFT = tk.Label(popup,
                        text="Calculated FFT",
                        font=("Helvetica", 12, "bold"))
    labelFFT.grid(row=1, column=0, padx=10, pady=10)

    labelDWF = tk.Label(popup,
                        text="Calculated DWF",
                        font=("Helvetica", 12, "bold"))
    labelDWF.grid(row=2, column=0, padx=10, pady=10)

    labelPE = tk.Label(popup,
                        text="Calculated PE",
                        font=("Helvetica", 12, "bold"))
    labelPE.grid(row=3, column=0, padx=10, pady=10)

    #create a label for each old value
    labelOldFFT = tk.Label(popup,
                        text="FFT Provided",
                        font=("Helvetica", 12, "bold"))
    labelOldFFT.grid(row=1, column=2, padx=10, pady=10)

    labelOldDWF = tk.Label(popup,
                        text="DWF Provided",
                        font=("Helvetica", 12, "bold"))
    labelOldDWF.grid(row=2, column=2, padx=10, pady=10)

    labelOldPE = tk.Label(popup,
                        text="PE Provided",
                        font=("Helvetica", 12, "bold"))
    labelOldPE.grid(row=3, column=2, padx=10, pady=10)


    #create a label for each value
    labelFFTValue = tk.Label(popup,
                        text=fft,
                        font=("Helvetica", 12, "bold"))
    labelFFTValue.grid(row=1, column=1, padx=10, pady=10)
    
    labelDWFValue = tk.Label(popup,
                        text=dwf,
                        font=("Helvetica", 12, "bold"))
    labelDWFValue.grid(row=2, column=1, padx=10, pady=10)

    labelPEValue = tk.Label(popup,
                        text=pe,

                        font=("Helvetica", 12, "bold"))
    
    labelPEValue.grid(row=3, column=1, padx=10, pady=10)

    #create a label for each old value
    labelOldFFTValue = tk.Label(popup,
                        text=old_fft,
                        font=("Helvetica", 12, "bold"))
    labelOldFFTValue.grid(row=1, column=3, padx=10, pady=10)

    labelOldDWFValue = tk.Label(popup,
                        text=old_dwf,
                        font=("Helvetica", 12, "bold"))

    labelOldDWFValue.grid(row=2, column=3, padx=10, pady=10)

    labelOldPEValue = tk.Label(popup,
                        text=old_pe,
                        font=("Helvetica", 12, "bold"))
    labelOldPEValue.grid(row=3, column=3, padx=10, pady=10)

    #create a button to save to excel
    saveButton = tk.Button(popup,
                        text="Save to Excel",
                        font=("Helvetica", 12, "bold"),
                        command=lambda: saveToExcel(name, fft, dwf, pe, old_fft, old_dwf, old_pe))
    saveButton.grid(row=4, column=0, padx=10, pady=10)

def saveToExcel(name, fft, dwf, pe, old_fft, old_dwf, old_pe):
    #create pandas dataframe with the values, save it to a excel file, if successful, show a message box
    df = pd.DataFrame({"FFT": [fft], "DWF": [dwf], "PE": [pe], "Given FFT": [old_fft], "Given DWF": [old_dwf], "Given PE": [old_pe]})
    #remove index
    
    try:
        df.to_excel(f"{name}.xlsx", index=False)
        # An info box to indicate the report has been saved.
        messagebox.showinfo(title="Success", message="Saved to Excel")
    except:
        # An error box to indicate the report was not able to save.
        messagebox.showerror(title="Error", message="Sorry, there was a problem saving to Excel")

    return None
    
def viewSTW(name):
    """Viewing an STWs Metrics"""
    #Create a new window that displays the STW's metrics.
    viewWindow = tk.Toplevel(root)
    viewWindow.resizable(False, False)
    width=300
    height=400
    viewWindow.geometry(f"{width}x{height}") # Window size.
    viewWindow.title(f"Viewing {name}") # Window title.

    STW_data = recallSTW(name)

    if STW_data == None: return None

    #create a label for each metric
    labelIDWF = tk.Label(viewWindow,
                        text="IDWF",
                        font=("Helvetica", 12, "bold"))
    labelIDWF.grid(row=1, column=0, padx=10, pady=10)
    #thus each label has a corresponding text box.
    labelMIR = tk.Label(viewWindow,
                        text="Max Infiltration Rate",
                        font=("Helvetica", 12, "bold"))
    labelMIR.grid(row=2, column=0, padx=10, pady=10)

    labelTE = tk.Label(viewWindow,
                        text="Trade Effluent",

                        font=("Helvetica", 12, "bold"))
    labelTE.grid(row=3, column=0, padx=10, pady=10)

    labelPCDF = tk.Label(viewWindow,
                        text="Per Capita Domestic Flow",
                        font=("Helvetica", 12, "bold"))
    labelPCDF.grid(row=4, column=0, padx=10, pady=10)

    labelPC = tk.Label(viewWindow,
                        text="Population Catchment",
                        font=("Helvetica", 12, "bold"))

    labelPC.grid(row=5, column=0, padx=10, pady=10)

    labelBOD = tk.Label(viewWindow, text= "BOD", font=("Helvetica", 12, "bold"))

    labelBOD.grid(row=6, column=0, padx=10, pady=10)

    labelKnownFFT = tk.Label(viewWindow, text= "Known FFT", font=("Helvetica", 12, "bold"))

    labelKnownFFT.grid(row=7, column=0, padx=10, pady=10)

    labelKnownDWF = tk.Label(viewWindow, text= "Known DWF", font=("Helvetica", 12, "bold"))

    labelKnownDWF.grid(row=8, column=0, padx=10, pady=10)

    labelKnownPE = tk.Label(viewWindow, text= "Known PE", font=("Helvetica", 12, "bold"))

    labelKnownPE.grid(row=9, column=0, padx=10, pady=10)


    #put in data next to each metric - make them text labels
    idwfVal = tk.Label(viewWindow, text=STW_data["IDWF"], font=("Helvetica", 12))
    idwfVal.grid(row=1, column=1, padx=10, pady=10)

    mirVal = tk.Label(viewWindow, text=STW_data["MIR"], font=("Helvetica", 12))
    mirVal.grid(row=2, column=1, padx=10, pady=10)

    tradeEffVal = tk.Label(viewWindow, text=STW_data["TE"], font=("Helvetica", 12))
    tradeEffVal.grid(row=3, column=1, padx=10, pady=10)

    perCapitaVal = tk.Label(viewWindow, text=STW_data["PCDF"], font=("Helvetica", 12))
    perCapitaVal.grid(row=4, column=1, padx=10, pady=10)

    popCatchVal = tk.Label(viewWindow, text=STW_data["POPC"], font=("Helvetica", 12))
    popCatchVal.grid(row=5, column=1, padx=10, pady=10)   


    bodVal = tk.Label(viewWindow, text=STW_data["BOD"], font=("Helvetica", 12))

    bodVal.grid(row=6, column=1, padx=10, pady=10)

    known_fft = tk.Label(viewWindow, text=STW_data["O_FFT"], font=("Helvetica", 12))

    known_fft.grid(row=7, column=1, padx=10, pady=10)

    known_dwf = tk.Label(viewWindow, text=STW_data["O_DWF"], font=("Helvetica", 12))

    known_dwf.grid(row=8, column=1, padx=10, pady=10)

    known_pe = tk.Label(viewWindow, text=STW_data["O_PE"], font=("Helvetica", 12))

    known_pe.grid(row=9, column=1, padx=10, pady=10)

    


               
    #Show all the metrics for a the STW

def updateSTW():
    """Updating an STWs Metrics"""
    if messagebox.askyesno(title="Save Changes", message="Are you sure wish to update these metrics?\nResults for PE, FFT and DWF may change."):   
        info = { # Retrieve information.
            "name": nameVal.get(),
            "IDWF":idwfVal.get(),
            "MIR":mirVal.get(),
            "TE":tradeEffVal.get(),
            "PCDF:":perCapitaVal.get(),
            "POPC:":popCatchVal.get(),
            "BOD":bodVal.get(),
            "O_FFT":known_fft.get(),
            "O_DWF":known_dwf.get(),
            "O_PE":known_pe.get(),
        }
        
        #check if any values are empty
        for value in info.values():
            if value == "" or value == " ":
                messagebox.showerror(title="Error", message="Please fill in all the fields. (With correct values)")
                return None

        name = info["name"]

        with open("STW_data.json", "r") as f:
            data = json.load(f)
        #update the data
        update = False
        for object in data:      
            if data[object]["name"] == name:
                messagebox.showinfo(title="Updating Entry", message="This entry already exists,so the current STW's data will be updated.")

                data[object] = info
                update = True
        if not update:
            messagebox.showinfo(title="Adding Entry", message="This entry does not exist, so a new entry will be created.")
            
            last_entry = int(list(data.keys())[-1])
            last_entry += 1
            data[str(last_entry)] = info
            
        #save the data
        with open("STW_data.json", "w") as f:
            json.dump(data, f, indent=4)
    else:
        return False

root = tk.Tk() # 
root.resizable(False, False)
width=665
height=750
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

""" BUTTONS & FUNCTIONALITY """
rightPanel = tk.Frame(root)
rightPanel.grid(row=2, column=0)

# Label to for STW drop down.
STWlabel = tk.Label(rightPanel,
                    text="Select a loaded STW:",
                    font=("Helvetica", 14, "bold"))
STWlabel.grid(row=0, column=0)

# STW Dropdown list.
chosenSTW = StringVar(rightPanel) # Default & selected STW.
chosenSTW.set(STWS[0])
STWdropdown = tk.OptionMenu(rightPanel, chosenSTW, *STWS)
STWdropdown.grid(row=1, column=0)

#create a refresj button next to it 
refreshButton = tk.Button(rightPanel, text="Refresh", command=lambda: refresh())

# Simply a line break
_blank = tk.Label(rightPanel,
                  text="-------------------------------",
                  font=("Helvetica", 14))
_blank.grid(row=2, column=0)

# View STW button.
viewButton = tk.Button(rightPanel, text="View STW", command=lambda: viewSTW(chosenSTW.get()))
viewButton.grid(row=3, column=0)

# Generate report button.
reportButton = tk.Button(rightPanel, text="Generate Report", command=lambda: report(chosenSTW.get()))
reportButton.grid(row=4, column=0)

_blank = tk.Label(rightPanel,
                  text="-------------------------------",
                  font=("Helvetica", 14))
_blank.grid(row=5, column=0)

# Label to show editing metrics.
STWlabel = tk.Label(rightPanel,
                    text="Edit STW metrics:",
                    font=("Helvetica", 14, "bold"))
STWlabel.grid(row=6, column=0)

# A sub panel to house metrics
metricPanel = tk.Frame(rightPanel)
metricPanel.grid(row=7, column=0)

""" Edit metrics """
nameVal = StringVar(metricPanel)
nameVal.set("Example STW")
nameLbl = tk.Label(metricPanel,
    text="Name:",
    font=("Helvetica", 14, "bold"))
nameLbl.grid(row=0, column=0)
nameEntry = tk.Entry(metricPanel, textvariable=nameVal)
nameEntry.grid(row=0, column=1)
# A text and label widget for the name of the STW.


idwfVal = StringVar(metricPanel)
idwfVal.set("")
idwfLabel = tk.Label(metricPanel,
    text="IDWF:",
    font=("Helvetica", 14, "bold"))
idwfLabel.grid(row=1, column=0)
idwfEntry = tk.Entry(metricPanel, textvariable=idwfVal)
idwfEntry.grid(row=1, column=1)
# A text and label widget for the 'idwf' of the STW.


mirVal = StringVar(metricPanel)
mirVal.set("")
mirLabel = tk.Label(metricPanel,
    text="Max Infiltration Rate:",
    font=("Helvetica", 14, "bold"))
mirLabel.grid(row=2, column=0)
mirEntry = tk.Entry(metricPanel, textvariable=mirVal)
mirEntry.grid(row=2, column=1)
# A text and label widget for the 'mir' of the STW.


tradeEffVal = StringVar(metricPanel)
tradeEffVal.set("")
tradeEffLabel = tk.Label(metricPanel,
    text="Trade Effluent:",
    font=("Helvetica", 14, "bold"))
tradeEffLabel.grid(row=3, column=0)
tradeEffEntry = tk.Entry(metricPanel, textvariable=tradeEffVal)
tradeEffEntry.grid(row=3, column=1)
# A text and label widget for the 'trade effluent' of the STW.


perCapitaVal = StringVar(metricPanel)
perCapitaVal.set("")
perCapitaLabel = tk.Label(metricPanel,
    text="Per Capita Domestic Flow:",
    font=("Helvetica", 14, "bold"))
perCapitaLabel.grid(row=4, column=0)
perCapitaEntry = tk.Entry(metricPanel, textvariable=perCapitaVal)
perCapitaEntry.grid(row=4, column=1)
# A text and label widget for the 'per capita domestic flow' of the STW.


popCatchVal = StringVar(metricPanel)
popCatchVal.set("")
popCatchLabel = tk.Label(metricPanel,
    text="Population Catchment:",
    font=("Helvetica", 14, "bold"))
popCatchLabel.grid(row=5, column=0)
popCatchEntry = tk.Entry(metricPanel, textvariable=popCatchVal)
popCatchEntry.grid(row=5, column=1)
# A text and label widget for the 'population catchment' of the STW.


bodVal = StringVar(metricPanel)
bodVal.set("")
bodLabel = tk.Label(metricPanel,
    text="BOD:",
    font=("Helvetica", 14, "bold"))
bodLabel.grid(row=6, column=0)
bodEntry = tk.Entry(metricPanel, textvariable=bodVal)
bodEntry.grid(row=6, column=1)
# A text and label widget for the 'bod' of the STW.


known_fft = StringVar(metricPanel)
known_fft.set("")
known_fftLabel = tk.Label(metricPanel,
    text="Known FFT:",
    font=("Helvetica", 14, "bold"))
known_fftLabel.grid(row=7, column=0)
known_fftEntry = tk.Entry(metricPanel, textvariable=known_fft)
known_fftEntry.grid(row=7, column=1)
# A text and label widget for the known fft of the STW.

known_dwf = StringVar(metricPanel)
known_dwf.set("")
known_dwfLabel = tk.Label(metricPanel,
    text="Known DWF:",
    font=("Helvetica", 14, "bold"))
known_dwfLabel.grid(row=8, column=0)
known_dwfEntry = tk.Entry(metricPanel, textvariable=known_dwf)
known_dwfEntry.grid(row=8, column=1)
# A text and label widget for the known dwf of the STW.

known_pe = StringVar(metricPanel)
known_pe.set("")
known_peLabel = tk.Label(metricPanel,
    text="Known PE:",
    font=("Helvetica", 14, "bold"))
known_peLabel.grid(row=9, column=0)
known_peEntry = tk.Entry(metricPanel, textvariable=known_pe)
known_peEntry.grid(row=9, column=1)
# A text and label widget for the known pe of the STW.


# Button to update the metrics of the STW.
viewButton = tk.Button(metricPanel, text="Update STW", command=lambda: updateSTW())
viewButton.grid(row=10, column=0)    

# Quit program button.
quitButton = tk.Button(root, text="Quit Program", command=quitProg)
quitButton.grid(row=3, column=0)

try:
    print("Program started...")
    root.mainloop()
    print("Program closed...")
except Exception as e:
    print(f"Failed... Error generated:\n{e}\n{traceback.print_exc()}")
        
