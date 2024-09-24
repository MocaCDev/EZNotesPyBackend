"""
This file will be in charge of all "upfront" operations that is needed to get the
software launched on the clients computer/phone.. presumably.

The actions of this file include, but are not limited to:
    * checking if the user logged into the software,
    * fixing any sort of bugs that may come about in regards to the sign-up/log-in operation,
    * getting the users categories and adding categoreis.
"""

import yaml
from json import dumps, loads
import subprocess
import sys
import os

USER = os.path.expanduser('~/')
PATH = os.path.join(USER, 'EZNotes_Data/EZNotes_data.yaml')#'/Users/aidanwhite/EZNotes_Data/EZNotes_data.yaml'

# This will store all of the category names
"""
Format:
    {
        "categories": [
            <names of all the categories>
        ]
    }
"""
CATEGORIES_PATH = os.path.join(USER, 'EZNotes_Data/EZNotes_Categories.json')

# This will store all of the set names
"""
Format:
    {
        "sets": [
            {"<set_name>": "<category_name>"}
        ]
    }

    Where <category_name> is the name of the category where the set will be found in
"""
SETS_PATH = os.path.join(USER, 'EZNotes_Data/EZNotes_Categorise_Sets.json')

# This will store all of the actual notes
"""
Format:
    {
        "notes": [
            {
                "data": "<note_content>",
                "parent": "<set_name>"
            }
        ]
    }

    Where <note_content> is the actual notes, and <set_name> is the specific set
    where the notes can be found.
    We will assume that the order in which each object of the array "notes" is in
    is the order in which it should be for the user. (we will assume it is in chronological order)
    Until further feedback is given, this feature is deemed "unstable".
"""
NOTES_PATH = os.path.join(USER, 'EZNotes_Data/EZNotes_Notes.json')

if len(sys.argv) < 2:
    sys.exit(0)

def write_json_file(filepath, data: dict):
    with open(filepath, 'w') as file:
        file.write(dumps(data, indent=2))
        file.close()

# Operations for dealing with categories, sets and notes
if sys.argv[1] == '--create_new_category':
    try:
        if not os.path.isfile(CATEGORIES_PATH):
            data = {
                'categories': [str(sys.argv[2])]
            }
        else:
            data = loads(open(CATEGORIES_PATH, 'r').read())

            if not str(sys.argv[2]) in data['categories']:
                data['categories'].append(sys.argv[2])
            else:
                sys.stdout.write('added')
                sys.exit(0)

        write_json_file(CATEGORIES_PATH, data)
        
        sys.stdout.write('added')
        sys.exit(0)
    except Exception as e:
        sys.stdout.write('failed_to_add')
        sys.exit(0)

if sys.argv[1] == '--attempt_get_categories':
    if not os.path.isfile(CATEGORIES_PATH):
        sys.stdout.write('nothing')
        sys.exit(0)

    data = loads(open(CATEGORIES_PATH, 'r').read())
    categories = '\n'.join([i for i in data['categories']])
    
    sys.stdout.write(categories)
    sys.exit(0)

# `sys.argv[2]` needs to be the sets name
# `sys.argv[3]` needs to be the category in which the set belongs to
if sys.argv[1] == '--create_new_set':
    try:
        if not os.path.isfile(SETS_PATH):
            data = {
                'sets': [
                    {str(sys.argv[2]): str(sys.argv[3])}
                ]
            }
        else:
            data = loads(open(SETS_PATH, 'r').read())

            # Make sure the set does not already exist "inside" the category
            for i in data['sets']:
                for k, _ in i.items():
                    if k == str(sys.argv[2]):
                        sys.stdout.write('added')
                        sys.exit(0)
                        break # not needed, but just to be safe
            
            data['sets'].append({str(sys.argv[2]): str(sys.argv[3])})

        write_json_file(SETS_PATH, data)
        
        sys.stdout.write('added')
        sys.exit(0)
    except Exception as e:
        sys.stdout.write('failed_to_add')
        sys.exit(0)

# `sys.argv[2]` needs to be the content of the image
# `sys.argv[3]` needs to be the set in which the notes belong to
if sys.argv[1] == '--create_notes':
    try:
        if not os.path.isfile(NOTES_PATH):
            data = {
                'notes': [
                    {
                        'data': str(sys.argv[2]),
                        'parent': str(sys.argv[3])
                    }
                ]
            }
        else:
            data = loads(open(NOTES_PATH, 'r').read())

            # Make sure the notes content does not already exist (has not already been uploaded)
            for i in data['notes']:
                for k, v in i.items():
                    if k == 'data' and v == str(sys.argv[2]):
                        sys.stdout.write('added')
                        sys.exit(0)
                        break # not needed, but just to be safe

            data['notes'].append({
                'data': str(sys.argv[2]),
                'parent': str(sys.argv[3])
            })
        
        write_json_file(NOTES_PATH, data)

        sys.stdout.write('added')
        sys.exit(0)

    except Exception as e:
        sys.stdout.write('failed_to_add')
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
        if not os.path.isfile(PATH):
            data = {
                'account_id': sys.argv[2],
                'logged_in': True
            }
            with open(PATH, 'w') as file:
                file.write(yaml.safe_dump(data))
                file.close()
            
            sys.stdout.write('logged_user_in\0')
            sys.exit(0)

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