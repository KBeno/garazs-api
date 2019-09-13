import json
from werkzeug.security import generate_password_hash, check_password_hash
from os.path import isfile

USERS_PATH = './config/users.json'

def init_users_file(force=False):
    def create_file():
        with open(USERS_PATH, 'w') as users_json:
            json.dump({}, users_json)
    if not force:
        if not isfile(USERS_PATH):
            create_file()
            return True
        else:
            return False
    else:
        create_file()
        return True

def check_password(user, pwd):
    with open(USERS_PATH, 'r') as users_json:
        users_pws = json.load(users_json)
    if user in users_pws.keys():
        return check_password_hash(users_pws[user], pwd)
    else:
        return False


def set_password(user, pwd):
    with open(USERS_PATH, 'r') as users_json:
        users_pws = json.load(users_json)
    if user in users_pws.keys():
        users_pws[user] = generate_password_hash(pwd)
        msg = 'Password updated'
    else:
        msg = 'No user named: {u}'.format(u=user)
    with open(USERS_PATH, 'w') as users_json:
        json.dump(users_pws, users_json, indent=4)
    return msg


def create_user(username, pwd):
    with open(USERS_PATH, 'r+') as users_json:
        users_pws = json.load(users_json)
    if username not in users_pws.keys():
        users_pws[username] = generate_password_hash(pwd)
        msg = 'User created'
    else:
        msg = 'User already exists'
    with open(USERS_PATH, 'w') as users_json:
        json.dump(users_pws, users_json, indent=4)
    return msg

def delete_user(user, reqire_confirm=True):
    with open(USERS_PATH, 'r+') as users_json:
        users_pws = json.load(users_json)
    if user in users_pws.keys():
        if reqire_confirm:
            confirmation = input('Are you sure? [Y/n]')
        else:
            confirmation = 'Y'
        if not confirmation == 'n':
            del users_pws[user]
            msg = 'User deleted'
        else:
            msg = 'Delete canceled'
    else:
        msg = 'No user named: {u}'.format(u=user)
    with open(USERS_PATH, 'w') as users_json:
        json.dump(users_pws, users_json, indent=4)
    return msg

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='User management')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-c', '--create', help='Create a new user and set its password',
                        action='store_true')
    group.add_argument('-p', '--set_password', help='Update the password of a user',
                        action='store_true')
    group.add_argument('-d', '--delete', help='Delete a user',
                        action='store_true')
    args = parser.parse_args()

    if args.create:
        username = input('New username: ')
        password = input('Password: ')
        msg = create_user(username, password)
        print(msg)

    if args.set_password:
        username = input('Update password for existing user: ')
        password = input('New password: ')
        msg = set_password(username, password)
        print(msg)

    if args.delete:
        username = input('Existing username to delete: ')
        msg = delete_user(username)
        print(msg)