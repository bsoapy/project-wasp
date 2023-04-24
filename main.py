import tkinter as tk
from tkinter import messagebox, StringVar
import os
import json
import pandas as pd
from idlelib.tooltip import Hovertip
from formulae import *

from formulae import *


# =====================================================================================================================================================================================
# FUNCTIONS
# =====================================================================================================================================================================================

# Refresh the status of STWs
def refresh():
    stws = []
    data = json.load(open("stw_data.json"))
    for i in data:
        stws.append(data[i]["name"])

# Closes the program
def quitProg():
    if messagebox.askyesno(title="Quit", message="Are you sure you want to quit?\nUnsaved changes will be lost."):
        root.quit()
        os.sys.exit()
    else:
        return False

# Retrieve the data of a selected STW
def callSTW(name):
    data = json.load(open("stw_data.json"))
    stw_data = {}
    for i in data:
        if data[i]["name"] == name:
            stw_data = data[i]
            break
    if stw_data == {}:
        messagebox.showerror(title="Error Viewing STW", message="There was a problem loading this STW")
    return stw_data

def viewSTW(name):
    data = callSTW(name)
    if data == None: return None

    # =====================================================================================================================================================================================
    # POPUP TO DISPLAY STORED METRICS
    # =====================================================================================================================================================================================

    popup = tk.Toplevel(root)
    popup.resizable(True, True)
    popup.geometry("400x400")
    popup.title(f"Viewing {name}")

    # Create a Label for each stored metric
    labelIDWF = tk.Label(popup, text="IDWF (I/d) = "+str(data["IDWF"]), font=("Helvetica", 12, "bold"))
    labelIDWF.grid(row=1, column=0, padx=10, pady=10)

    labelMIR = tk.Label(popup, text="Max Infiltration Rate (I/d) = "+str(data["MIR"]), font=("Helvetica", 12, "bold"))
    labelMIR.grid(row=2, column=0, padx=10, pady=10)

    labelTE = tk.Label(popup, text="Trade Effluent (I/d) = "+str(data["TE"]), font=("Helvetica", 12, "bold"))
    labelTE.grid(row=3, column=0, padx=10, pady=10)

    labelPCDF = tk.Label(popup, text="Per Capita Domestic Flow (I/d) = "+str(data["PCDF"]), font=("Helvetica", 12, "bold"))
    labelPCDF.grid(row=4, column=0, padx=10, pady=10)

    labelPC = tk.Label(popup, text="Population Catchment = "+str(data["POPC"]), font=("Helvetica", 12, "bold"))
    labelPC.grid(row=5, column=0, padx=10, pady=10)

    labelBOD = tk.Label(popup, text= "BOD = "+str(data["BOD"]), font=("Helvetica", 12, "bold"))
    labelBOD.grid(row=6, column=0, padx=10, pady=10)

    labelKnownFFT = tk.Label(popup, text= "Published FFT (I/s) = "+str(data["O_FFT"]), font=("Helvetica", 12, "bold"))
    labelKnownFFT.grid(row=7, column=0, padx=10, pady=10)

    labelKnownDWF = tk.Label(popup, text= "Published DWF (I/d) = "+str(data["O_DWF"]), font=("Helvetica", 12, "bold"))
    labelKnownDWF.grid(row=8, column=0, padx=10, pady=10)

    labelKnownPE = tk.Label(popup, text= "Published PE = "+str(data["O_PE"]), font=("Helvetica", 12, "bold"))
    labelKnownPE.grid(row=9, column=0, padx=10, pady=10)

def updateSTW(passphrase, nameVal, idwfVal, mirVal, tradeEffVal, perCapitaVal, popCatchVal, bodVal, known_fft, known_dwf, known_pe):
    if messagebox.askyesno(title="Save Changes", message="Are you sure wish to update these metrics?\nResults for PE, FFT and DWF may change.") and passphrase.get() == "password":
        info = { 
            "name": nameVal.get(),
            "IDWF":idwfVal.get(),
            "MIR":mirVal.get(),
            "TE":tradeEffVal.get(),
            "PCDF":perCapitaVal.get(),
            "POPC":popCatchVal.get(),
            "BOD":bodVal.get(),
            "O_FFT":known_fft.get(),
            "O_DWF":known_dwf.get(),
            "O_PE":known_pe.get(),
        }
        
        for value in info.values():
            if value == "" or value == " ":
                messagebox.showerror(title="Error", message="Please fill in all the fields. (With correct values)")
                return None

        name = info["name"]

        with open("STW_data.json", "r") as f:
            data = json.load(f)
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

        with open("STW_data.json", "w") as f:
            json.dump(data, f, indent=4)
    elif passphrase.get() != "password":
        messagebox.showerror(title="Error", message="Incorrect passphrase")
    else:
        return False
    
def saveToExcel(name, fft, dwf, pe, o_fft, o_dwf, o_pe):
    df = pd.DataFrame({"FFT": [fft], "DWF": [dwf], "PE": [pe], "Given FFT": [o_fft], "Given DWF": [o_dwf], "Given PE": [o_pe]})

    try:
        df.to_excel(f"{name}.xlsx", index=False)
        messagebox.showinfo(title="Success", message="Saved to Excel")
    except: messagebox.showerror(title="Error", message="Sorry, there was a problem saving to Excel")

    return None

def generateReport(name):
    data = callSTW(name)

    # Retrieve data to be used for calculations
    try: i_dwf = float(data["IDWF"])
    except: i_dwf = "No Input"

    try: i_max = float(data["MIR"])
    except: i_max = "No Input"

    try: e = float(data["TE"])
    except: e = "No Input"

    try: g = float(data["PCDF"])
    except: g = "No Input"

    try: p = float(data["POPC"])
    except: p = "No Input"

    try: bod = float(data["BOD"])
    except: bod = "No Input"

    o_pe = data["O_PE"]
    o_dwf = data["O_DWF"]
    o_fft = data["O_FFT"]

  

    # Calculate PE, DWF and FFT
    try: 
        fft = calculate_fft(p,g,i_max,e)
    except: 
        fft = "Could not calculate (need more metrics)"

    try: 
        dwf = calculate_dwf(p,g,i_dwf,e)
    except: 
        dwf = "Could not calculate (need more metrics)"

    try: 
        pe = calculate_pe(bod, p)
    except: 
        pe = "Could not calculate (need more metrics)"
    
    # =====================================================================================================================================================================================
    # POPUP TO DISPLAY PUBLISHED AND CALCULATED METRICS
    # =====================================================================================================================================================================================
    
    popup = tk.Toplevel(root)
    popup.resizable(True, True)
    popup.geometry("500x200")
    popup.title(f"Report for {name}")

    # Create a Label for each calculate metric
    labelFFT = tk.Label(popup, text=f"Calculated FFT = {fft}", font=("Helvetica", 12, "bold"))
    labelFFT.grid(row=1, column=0, padx=10, pady=10)

    labelDWF = tk.Label(popup, text=f"Calculated DWF = {dwf}", font=("Helvetica", 12, "bold"))
    labelDWF.grid(row=2, column=0, padx=10, pady=10)

    labelPE = tk.Label(popup, text=f"Calculated PE = {pe}", font=("Helvetica", 12, "bold"))
    labelPE.grid(row=3, column=0, padx=10, pady=10)

    # Create a Label for each published metric
    labelOldFFT = tk.Label(popup, text=f"FFT Published = {o_fft}", font=("Helvetica", 12, "bold"))
    labelOldFFT.grid(row=1, column=2, padx=10, pady=10)

    labelOldDWF = tk.Label(popup, text=f"DWF Published = {o_dwf}", font=("Helvetica", 12, "bold"))
    labelOldDWF.grid(row=2, column=2, padx=10, pady=10)

    labelOldPE = tk.Label(popup, text=f"PE Published = {o_pe}", font=("Helvetica", 12, "bold"))
    labelOldPE.grid(row=3, column=2, padx=10, pady=10)

    # Create a button to save to Excel
    saveBtn = tk.Button(popup, text="Save to Excel", command=lambda: saveToExcel(name, fft, dwf, pe, o_fft, o_dwf, o_pe))
    saveBtn.grid(row=4, column=0, padx=10, pady=10)

def updateEntries(chosenSTW):
    data = callSTW(chosenSTW)
    nameVal.set(f"{data['name']}")
    idwfVal.set(f"{data['IDWF']}")
    mirVal.set(f"{data['MIR']}")
    tradeEffVal.set(f"{data['TE']}")
    perCapitaVal.set(f"{data['PCDF']}")
    popCatchVal.set(f"{data['POPC']}")
    bodVal.set(f"{data['BOD']}")
    known_fft.set(f"{data['O_FFT']}")
    known_dwf.set(f"{data['O_DWF']}")
    known_pe.set(f"{data['O_PE']}")

# =====================================================================================================================================================================================
# LOAD STW DATA
# =====================================================================================================================================================================================

data = json.load(open("stw_data.json"))
stws = []
refresh()
for i in data:
    stws.append(data[i]["name"])

# =====================================================================================================================================================================================
# ROOT WINDOW
# =====================================================================================================================================================================================

root = tk.Tk() # create root window
root.resizable(True, True)
root.title("SoftEng Project")

# =====================================================================================================================================================================================
# HEADER SECTION
# =====================================================================================================================================================================================

# Create Header widget
header_frame = tk.Frame(root, width=400, height=100)
header_frame.grid(row=1, column=0, padx=10, pady=(5,0))

# Create Title in Header widget
title_frame = tk.Frame(header_frame, width=170, height=50)
title_frame.grid(row=1, column=1, padx=(10,5), pady=10)
labelTitle = tk.Label(title_frame, text="WASP TOOL", font=("Arial", 28, "bold"))
labelTitle.grid(row=0, column=0, columnspan=1, pady=(5,0))

# Create Descriptor in Header widget
desc_frame = tk.Frame(header_frame, width=200, height=50)
desc_frame.grid(row=1, column=2, padx=(5,10), pady=10)
labelDesc = tk.Label(desc_frame, text="This tool allows you to view and update metrics\nfor each STW and generate reports to validate\npublished PE, DWF and FFT figures. ", font=("Arial", 10), justify="left")
labelDesc.grid(row=1, column=0, columnspan=2, padx=15, pady=(5,0))

_blank = tk.Label(root, text="- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -", font=("Arial", 14))
_blank.grid(row=2, column=0)

# =====================================================================================================================================================================================
# BODY SECTION
# =====================================================================================================================================================================================

# Create Body widget
body_frame = tk.Frame(root, width=400, height=300)
body_frame.grid(row=3, column=0, padx=10, pady=0)

# Create Selector in Body widget
selector_frame = tk.Frame(body_frame, width=160, height=30)
selector_frame.grid(row=1, column=1, padx=(10,5), pady=10)
chosenSTW = StringVar(selector_frame)
chosenSTW.set(stws[0])
labelSelect = tk.Label(selector_frame, text="Select a STW: ", font=("Arial", 11, "bold"))
labelSelect.grid(row=0, column=0, padx=0, pady=5)
selectSTW = tk.OptionMenu(selector_frame, chosenSTW, *stws, command=lambda x:updateEntries(chosenSTW.get()))
selectSTW.grid(row=0, column=1, padx=(0,5), pady=5)

# Create View Button in Body widget
view_btn_frame = tk.Frame(body_frame, width=100, height=30)
view_btn_frame.grid(row=1, column=2, padx=(5,5), pady=10)
view_btn = tk.Button(view_btn_frame, text="View Statistics", command=lambda: viewSTW(chosenSTW.get()))
view_btn.grid(row=0, column=0, padx=5, pady=5)
viewTip = tk.Button(view_btn_frame, text="?", state="disabled")
viewTip.grid(row=0, column=1, padx=5)
view_ttp = Hovertip(viewTip, "This button shows the current statistics for the selected STW.")

# Create Report Button in Body widget
report_btn_frame = tk.Frame(body_frame, width=100, height=30)
report_btn_frame.grid(row=1, column=3, padx=(5,10), pady=10)
report_btn = tk.Button(report_btn_frame, text="Generate Report", command=lambda: generateReport(chosenSTW.get()))
report_btn.grid(row=0, column=0, padx=5, pady=5)
reportTip = tk.Button(report_btn_frame, text="?", state="disabled")
reportTip.grid(row=0, column=1, padx=5)
report_ttp = Hovertip(reportTip, "This button generates a report that compares the published PE, DWF\nand FFT figures with raw data for the selected STW.")

# Create Edit widget
edit_frame = tk.Frame(root, width=400, height=300)
edit_frame.grid(row=4, column=0, padx=10, pady=0)

# Create first columns for Edit entries in Edit widget
edit_frame_1 = tk.Frame(edit_frame, width=185, height=150)
edit_frame_1.grid(row=0, column=1, padx=(10,5), pady=5)

nameVal = StringVar(edit_frame_1)
nameLbl = tk.Label(edit_frame_1,text="Name:",font=("Arial", 11), justify="left")
nameLbl.grid(row=0, column=0)
nameEntry = tk.Entry(edit_frame_1, textvariable=nameVal)
nameEntry.grid(row=0, column=1)

idwfVal = StringVar(edit_frame_1)
idwfLabel = tk.Label(edit_frame_1, text="IDWF:", font=("Arial", 11), justify="left")
idwfLabel.grid(row=1, column=0)
idwfEntry = tk.Entry(edit_frame_1, textvariable=idwfVal)
idwfEntry.grid(row=1, column=1)

mirVal = StringVar(edit_frame_1)
mirLabel = tk.Label(edit_frame_1, text="Max Infiltration Rate:", font=("Arial", 11), justify="left")
mirLabel.grid(row=2, column=0)
mirEntry = tk.Entry(edit_frame_1, textvariable=mirVal)
mirEntry.grid(row=2, column=1)

tradeEffVal = StringVar(edit_frame_1)
tradeEffLabel = tk.Label(edit_frame_1, text="Trade Effluent:", font=("Arial", 11), justify="left")
tradeEffLabel.grid(row=3, column=0)
tradeEffEntry = tk.Entry(edit_frame_1, textvariable=tradeEffVal)
tradeEffEntry.grid(row=3, column=1)

perCapitaVal = StringVar(edit_frame_1)
perCapitaLabel = tk.Label(edit_frame_1, text="Per Capita Domestic Flow:", font=("Arial", 11), justify="left")
perCapitaLabel.grid(row=4, column=0)
perCapitaEntry = tk.Entry(edit_frame_1, textvariable=perCapitaVal)
perCapitaEntry.grid(row=4, column=1)

# Create second columns for Edit entries in Edit widget
edit_frame_2 = tk.Frame(edit_frame, width=185, height=150,)
edit_frame_2.grid(row=0, column=2, padx=(5,10), pady=5)

popCatchVal = StringVar(edit_frame_2)
popCatchLabel = tk.Label(edit_frame_2, text="Population Catchment:", font=("Arial", 11), justify="left")
popCatchLabel.grid(row=5, column=0)
popCatchEntry = tk.Entry(edit_frame_2, textvariable=popCatchVal)
popCatchEntry.grid(row=5, column=1)

bodVal = StringVar(edit_frame_2)
bodLabel = tk.Label(edit_frame_2, text="BOD:", font=("Arial", 11), justify="left")
bodLabel.grid(row=6, column=0)
bodEntry = tk.Entry(edit_frame_2, textvariable=bodVal)
bodEntry.grid(row=6, column=1)

known_fft = StringVar(edit_frame_2)
known_fftLabel = tk.Label(edit_frame_2, text="Published FFT:", font=("Arial", 11), justify="left")
known_fftLabel.grid(row=7, column=0)
known_fftEntry = tk.Entry(edit_frame_2, textvariable=known_fft)
known_fftEntry.grid(row=7, column=1)

known_dwf = StringVar(edit_frame_2)
known_dwfLabel = tk.Label(edit_frame_2, text="Published DWF:", font=("Arial", 11), justify="left")
known_dwfLabel.grid(row=8, column=0)
known_dwfEntry = tk.Entry(edit_frame_2, textvariable=known_dwf)
known_dwfEntry.grid(row=8, column=1)

known_pe = StringVar(edit_frame_2)
known_peLabel = tk.Label(edit_frame_2, text="Published PE:", font=("Arial", 11), justify="left")
known_peLabel.grid(row=9, column=0)
known_peEntry = tk.Entry(edit_frame_2, textvariable=known_pe)
known_peEntry.grid(row=9, column=1)

updateEntries(chosenSTW.get())

# Create passphrase button in Edit widget
submission_frame = tk.Frame(root, width=400, height=300)
submission_frame.grid(row=5, column=0, padx=10, pady=0)
passphrase_frame = tk.Frame(submission_frame, width=185, height=30)
passphrase_frame.grid(row=1, column=1, padx=10, pady=10)
passphrase = StringVar(passphrase_frame)
passphrase.set("")
passphraseLabel = tk.Label(passphrase_frame, text="Admin Passphrase:", font=("Arial", 11, "bold"), justify="left")
passphraseLabel.grid(row=2, column=0)
passphraseEntry = tk.Entry(passphrase_frame, textvariable=passphrase, show="*")
passphraseEntry.grid(row=2, column=1)
adminTip = tk.Button(passphrase_frame, text="?", state="disabled")
adminTip.grid(row=2, column=2, padx=5)
admin_ttp = Hovertip(adminTip, "Please enter the administrator passphrase\nto commit changes to the database.")

# Create submit button in Edit widget
submit_btn_frame = tk.Frame(submission_frame, width=185, height=30)
submit_btn_frame.grid(row=2, column=1, padx=10, pady=(5,0))
submit_btn = tk.Button(submit_btn_frame, text="Update STW", command=lambda: updateSTW(passphrase, nameVal, idwfVal, mirVal, tradeEffVal, perCapitaVal, popCatchVal, bodVal, known_fft, known_dwf, known_pe))
submit_btn.grid(row=1, column=1, padx=0, pady=0)

_blank = tk.Label(root, text="- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -", font=("Arial", 14))
_blank.grid(row=6, column=0, pady=(10,0))

# =====================================================================================================================================================================================
# FOOTER SECTION
# =====================================================================================================================================================================================

# Create Footer widget
footer_frame = tk.Frame(root, width=500, height=50)
footer_frame.grid(row=7, column=0, padx=10, pady=0)

# Create T&C's in Footer widget
terms_frame = tk.Frame(footer_frame, width=350, height=30)
terms_frame.grid(row=0, column=1, padx=(10,5), pady=5)
link_var = StringVar()
link_var.set("© 2022 - 2023, All Rights Reserved. See the user manual for contact details.")
terms = tk.Label(terms_frame, textvariable=link_var, font=("Arial", 9), justify="left", anchor="w", cursor="hand2")
terms.grid(row=0, column=1, padx=10)


# Create Quit Button in Footer widget
quit_btn_frame = tk.Frame(footer_frame, width=100, height=30)
quit_btn_frame.grid(row=0, column=2, padx=(5,10), pady=(10))
quitBtn = tk.Button(quit_btn_frame, text="Quit Program", command=quitProg)
quitBtn.grid(row=0, column=0, padx=5, pady=5)

# =====================================================================================================================================================================================
# RUN PROGRAM
# =====================================================================================================================================================================================

try: root.mainloop()
except Exception as e: print("Error: ", e)