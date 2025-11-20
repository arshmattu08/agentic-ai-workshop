# agentic-ai-workshop

## Useful Commands:

## MacOS

### Creating venv
python3.11 -m venv <your_venv_name>

### Activating venv
source <your_venv_name>/bin/activate

### Command to select interpreter
shift+cmd+P then choose 'Python: select interpreter'

(Sometimes you need to manually enter interpreter path. For that, right click your venv, copy path, paste into enter interpreter path and enter).

### Installing packages into your venv
pip install -r requirements.txt

## Windows

### Creating venv
py -3.11 -m venv <your_venv_name> OR  
python -m venv <your_venv_name> OR  
for python 3.11 use <path-to-python311>\python.exe" -m venv <your_venv_name>  
path to python can be found using "where python"  

### Activating venv

.\<your_venv_name>\Scripts\Activate (Powershell)

### Command to select interpreter
Press: Ctrl + Shift + P  
Type: Python: Select Interpreter  
Pick the one from your venv   
If not detected: right click venv on left pane, copy path and paste into interpreter path and enter.  

### Installing packages into your venv
pip install -r requirements.txt

