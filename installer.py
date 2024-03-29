import os
import sys
import urllib

""" An installer file that ensures all required modules for the program are installed.
    It also installs all missing modules so that the program can run."""

requiredModules = [
    "pandas",
    "tkinter",
    "traceback",
    "os",
    "numpy",
    "json",
    "openpyxl"
]

# First ensure pip is installed on the machine.
try:
    import pip
    print("pip found.")
except ModuleNotFoundError:
    # if pip is not installed, download get-pip.py
    url = "https://bootstrap.pypa.io/get-pip.py"
    urllib.request.urlretrieve(url, "get-pip.py")
    
   # run get-pip.py using os.system()
    os.system(f"{sys.executable} get-pip.py")
    
    
# Start installing any modules that are missing.
for module in requiredModules:
    try:
        import module
    except ImportError:
        print(f"{module} module not found. Installing {module}.")
        os.system(f"pip3.10 install {module}")
        
