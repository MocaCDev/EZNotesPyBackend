"""
This file will be in charge of all "upfront" operations that is needed to get the
software launched on the clients computer/phone.. presumably.

The actions of this file include, but are not limited to:
    * checking if the user logged into the software,
    * fixing any sort of bugs that may come about in regards to the sign-up/log-in operation,
    * getting the users categories and adding categoreis.
"""

import yaml
import subprocess
import sys
import os

USER = os.path.expanduser('~/')
PATH = os.path.join(USER, 'EZNotes_Data/EZNotes_data.yaml')#'/Users/aidanwhite/EZNotes_Data/EZNotes_data.yaml'

if len(sys.argv) < 2:
    sys.exit(0)

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
        
        sys.stdout.write('saved_aid')
    except:
        sys.stdout.write('error_saving_aid')

    sys.exit(0)

if sys.argv[1] == '--AID_exists':
    if os.path.isfile(PATH):
        eznotes_data = yaml.safe_load(open(PATH, 'r').read())
        sys.stdout.write('exists' if 'account_id' in eznotes_data else 'not_exists')
    else:
        sys.stdout.write('not_exists')
    
    sys.exit(0)

# If `--AID_exists` returns `exists`, the below command will be invoked
if sys.argv[1] == '--get_AID':
    AID = yaml.safe_load(open(PATH, 'r').read())
    sys.stdout.write(AID['account_id'] + '')
    sys.exit(0)

if sys.argv[1] == '--set_max_code_tries_exceeded':
    try:
        eznotes_data = yaml.safe_load(open(PATH, 'r').read())
        eznotes_data['max_code_tries_reached'] = True

        with open(PATH, 'w') as file:
            yaml.safe_dump(eznotes_data, file)
            file.flush()
            file.close()
        
        sys.stdout.write('done')
    except:
        sys.stdout.write('error')
    
    sys.exit(0)

if sys.argv[1] == '--has_exceeded_code_attempts':
    eznotes_data = yaml.safe_load(open(PATH, 'r').read())

    if 'max_code_tries_reached' in eznotes_data and eznotes_data['max_code_tries_reached']:
        sys.stdout.write('reached')
    else:
        sys.stdout.write('not_reached')
    
    sys.exit(0)

if sys.argv[1] == '--remove_eznotes_data':
    if os.path.isfile(PATH):
        os.remove(PATH)

    sys.stdout.write('good')
    sys.exit(0)

if sys.argv[1] == '--get_users_path':
    sys.stdout.write(USER)
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
        sys.stdout.write('exists')
    else:
        sys.stdout.write('does_not_exist')
    
    sys.exit(0)

if sys.argv[1] == '--log_user_in':
    try:
        eznotes_data = yaml.safe_load(open(PATH, 'r').read())
        eznotes_data['logged_in'] = True

        with open(PATH, 'w') as file:
            yaml.safe_dump(eznotes_data, file)
            file.flush()
            file.close()
        
        sys.stdout.write('logged_user_in')
    except Exception as e:
        sys.stdout.write(f'failed\n{str(e)}')

    sys.exit(0)

if sys.argv[1] == '--check_user_logged_in':
    if os.path.isfile(PATH):
        data = yaml.safe_load(open(PATH, 'r').read())

        if not 'logged_in' in data:
            sys.stdout.write('incomplete_signup')
            sys.exit(0)

        sys.stdout.write('logged_in' if data['logged_in'] else 'not_logged_in')
        sys.exit(0)
    
    sys.stdout.write('incomplete_signup')
    sys.exit(0)

#desktop_path = os.path.expanduser("~/")