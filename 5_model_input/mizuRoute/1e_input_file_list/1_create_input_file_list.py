# Create input file list
# Populates a text file with the names of the SUMMA runoff files used as mizuRoute input.

# modules
import os
import glob
from pathlib import Path
from shutil import copyfile
from datetime import datetime


# --- Control file handling
# Easy access to control file folder
controlFolder = Path('../../../0_control_files')

# Store the name of the 'active' file in a variable
controlFile = 'control_active.txt'

# Function to extract a given setting from the control file
def read_from_control( file, setting ):
    
    # Open 'control_active.txt' and ...
    with open(file) as contents:
        for line in contents:
            
            # ... find the line with the requested setting
            if setting in line and not line.startswith('#'):
                break
    
    # Extract the setting's value
    substring = line.split('|',1)[1]      # Remove the setting's name (split into 2 based on '|', keep only 2nd part)
    substring = substring.split('#',1)[0] # Remove comments, does nothing if no '#' is found
    substring = substring.strip()         # Remove leading and trailing whitespace, tabs, newlines
       
    # Return this value    
    return substring
    
# Function to specify a default path
def make_default_path(suffix):
    
    # Get the root path
    rootPath = Path( read_from_control(controlFolder/controlFile,'root_path') )
    
    # Get the domain folder
    domainName = read_from_control(controlFolder/controlFile,'domain_name')
    domainFolder = 'domain_' + domainName
    
    # Specify the forcing path
    defaultPath = rootPath / domainFolder / suffix
    
    return defaultPath
    
    
# --- Find input location
path_to_input = read_from_control(controlFolder/controlFile,'settings_mizu_input_path')

# Specify default path if needed
if path_to_input == 'default':  
    experiment_id = read_from_control(controlFolder/controlFile,'experiment_id')
    path_to_input = make_default_path('simulations/' + experiment_id + '/SUMMA') # outputs a Path()
else:
    path_to_input = Path(path_to_input) # make sure a user-specified path is a Path()    
    
    
# --- Find where input file list needs to go
file_list_path = read_from_control(controlFolder/controlFile,'settings_mizu_path')
file_list_name = read_from_control(controlFolder/controlFile,'settings_mizu_input_list')

# Specify default path if needed
if file_list_path == 'default':
    file_list_path = make_default_path('settings/mizuRoute') # outputs a Path()
else:
    file_list_path = Path(file_list_path) # make sure a user-specified path is a Path()
    
# Make the folder if it doesn't exist
file_list_path.mkdir(parents=True, exist_ok=True)

# --- Find the search pattern for filenames
search_pattern = read_from_control(controlFolder/controlFile,'settings_mizu_input_pattern')

# --- Make the file
# Find a list of input files
input_files = glob.glob(str(path_to_input / search_pattern))

# Sort this list
input_files.sort()

# Create the file list
with open(file_list_path / file_list_name, 'w') as f:
    for input_file in input_files:
        file = os.path.basename(input_file)    
        f.write(str(file) + "\n")
        
        
# --- Code provenance
# Generates a basic log file in the domain folder and copies the control file and itself there.

# Set the log path and file name
logPath = file_list_path
log_suffix = '_make_input_file_list.txt'

# Create a log folder
logFolder = '_workflow_log'
Path( logPath / logFolder ).mkdir(parents=True, exist_ok=True)

# Copy this script
thisFile = '1_create_input_file_list.py'
copyfile(thisFile, logPath / logFolder / thisFile);

# Get current date and time
now = datetime.now()

# Create a log file 
logFile = now.strftime('%Y%m%d') + log_suffix
with open( logPath / logFolder / logFile, 'w') as file:
    
    lines = ['Log generated by ' + thisFile + ' on ' + now.strftime('%Y/%m/%d %H:%M:%S') + '\n',
             'Generated input file list.']
    for txt in lines:
        file.write(txt) 