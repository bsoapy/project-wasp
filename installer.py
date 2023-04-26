import subprocess
import sys

# list of required modules
required_modules = ['tkinter', 'json', 'pandas']

# check if each module is installed, and install it if necessary
for module in required_modules:
    try:
        __import__(module)
        print(f"{module} is already installed")
    except ImportError:
        print(f"{module} is not installed, installing...")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', module])
        
