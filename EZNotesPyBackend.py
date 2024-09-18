"""
This file will be in charge of all "upfront" operations that is needed to get the
software launched on the clients computer/phone.. presumably.

The actions of this file include, but are not limited to, checking if the user logged into the software,
fixing any sort of bugs that may come about in regards to the sign-up/log-in operation,
getting the users categories and adding categoreis.
"""

import yaml
import sys
import win32com.client
import os

if len(sys.argv) < 2:
    sys.exit(0)

#print(os.path.expanduser('~'))

# The location `C:\\EZNotes_Data` is temporary.
PATH = 'C:\\EZNotes_Data\\eznotes_data.yaml'

def open_eznotes_data():
    with open(PATH, 'rb') as file:
        yaml_data = yaml.safe_load(file)
        file.close()
    
    return yaml_data

# Ran after user signs up, or if user created an account via the website and logs in on the software
if sys.argv[1] == '--add_user':
    pass

if sys.argv[1] == '--add_account_id':
    try:
        with open(PATH, 'w') as file:
            yaml.safe_dump(
                {
                    'account_id': str(sys.argv[2])
                },
                file
            )
            file.flush()
            file.close()
        
        sys.stdout.write('saved_aid\0')
    except:
        sys.stdout.write('error_saving_aid\0')

    sys.exit(0)

if sys.argv[1] == '--AID_exists':
    if os.path.isfile(PATH):
        eznotes_data = yaml.safe_load(open(PATH, 'r').read())
        sys.stdout.write('exists\0' if 'account_id' in eznotes_data else 'not_exists\0')
    else:
        sys.stdout.write('not_exists\0')
    
    sys.exit(0)

# If `--AID_exists` returns `exists`, the below command will be invoked
if sys.argv[1] == '--get_AID':
    AID = yaml.safe_load(open(PATH, 'r').read())
    sys.stdout.write(AID['account_id'] + '\0')
    sys.exit(0)

if sys.argv[1] == '--set_max_code_tries_exceeded':
    try:
        eznotes_data = yaml.safe_load(open(PATH, 'r').read())
        eznotes_data['max_code_tries_reached'] = True

        with open(PATH, 'w') as file:
            yaml.safe_dump(eznotes_data, file)
            file.flush()
            file.close()
        
        sys.stdout.write('done\0')
    except:
        sys.stdout.write('error\0')
    
    sys.exit(0)

if sys.argv[1] == '--has_exceeded_code_attempts':
    eznotes_data = yaml.safe_load(open(PATH, 'r').read())

    if 'max_code_tries_reached' in eznotes_data and eznotes_data['max_code_tries_reached']:
        sys.stdout.write('reached\0')
    else:
        sys.stdout.write('not_reached\0')
    
    sys.exit(0)

if sys.argv[1] == '--remove_eznotes_data':
    if os.path.isfile(PATH):
        os.remove(PATH)

    sys.stdout.write('good\0')
    sys.exit(0)

# We should probably try and do this via the C++ backend in QT instead of via Python..
# TODO: Make the above statement possible lol
if sys.argv[1] == '--rerun':
    os.system('C:\qt_apps\\build-EZNotesSoftware-Desktop_Qt_6_6_1_MinGW_64_bit-Debug\\appEZNotesSoftware.exe')
    sys.exit(0)

# Ran if user deletes their account
if sys.argv[1] == '--remove_user':
    os.remove(PATH)
    
    sys.exit(0)

# The below checks are ran in `main.cpp`
# They check if `PATH` (`eznotes_data.yaml`) exists. If it does, `--check_user_logged_in` gets ran.
#   `--check_user_logged_in` checks if `logged_in` is `true` in `PATH` (`eznotes_data.yaml`).
if sys.argv[1] == '--check_for_user_yaml':
    if os.path.isfile(PATH):
        sys.stdout.write('exists\0')
    else:
        sys.stdout.write('does_not_exist\0')
    
    sys.exit(0)

if sys.argv[1] == '--log_user_in':
    try:
        eznotes_data = yaml.safe_load(open(PATH, 'r').read())
        eznotes_data['logged_in'] = True

        with open(PATH, 'w') as file:
            yaml.safe_dump(eznotes_data, file)
            file.flush()
            file.close()
        
        sys.stdout.write('logged_user_in\0')
    except Exception as e:
        sys.stdout.write(f'failed\n{str(e)}\0')

    sys.exit(0)

if sys.argv[1] == '--check_user_logged_in':
    data = yaml.safe_load(open(PATH, 'r').read())

    if not 'logged_in' in data:
        sys.stdout.write('incomplete_signup\0')
        sys.exit(0)

    if data['logged_in']:
        sys.stdout.write('logged_in\0')
        sys.exit(0)
    
    sys.stdout.write('not_logged_in\0')
    sys.exit(0)

desktop_path = os.path.expanduser("~\Desktop")

# If the above path to `Desktop` folder does not exist,
# then it is safe to assume the `Desktop` folder is in `OneDrive`.
# If that is not the case either, the client has a weird desktop system
# or they have corrupted the layout of there folder.
if not os.path.exists(desktop_path):
    desktop_path = os.path.expanduser('~\OneDrive\Desktop')

with open(PATH, 'rb') as file:
    yaml_data = yaml.safe_load(file)
    file.close()

if sys.argv[1] == '--create_shortcut':

    # If the file already exists, do nothing.
    if os.path.isfile(os.path.join(desktop_path, 'EZNotes.lnk')):
        sys.exit(0)

    # pythoncom.CoInitialize() # remove the '#' at the beginning of the line if running in a thread.
    path = os.path.join(desktop_path, 'EZNotes.lnk')
    target = r'C:\EZNotes\Prepare-Deployment\EZNotesApp\EZNotes_App\appEZNotes_s.exe'
    icon = r'C:\Users\mocac\Downloads\eznote__2__GEt_icon.ico' # not needed, but nice

    shell = win32com.client.Dispatch("WScript.Shell")
    shortcut = shell.CreateShortCut(path)
    shortcut.Targetpath = target
    shortcut.IconLocation = icon
    shortcut.WindowStyle = 1 # 7 - Minimized, 3 - Maximized, 1 - Normal
    shortcut.save()

    sys.exit(0)

if sys.argv[1] == '--check_intro_ran':
    sys.stdout.write('false' if yaml_data['intro_ran'] is False else 'true')
    sys.stdout.flush()
    sys.exit(0)

if sys.argv[1] == '--set_intro_ran':
    yaml_data['intro_ran'] = False if sys.argv[2] == 'false' else True

    with open(PATH, 'w') as file:
        yaml_data = yaml.safe_dump(yaml_data)
        file.write(yaml_data)
        file.flush()
        file.close()
    
    sys.exit(0)
