from werkzeug.security import generate_password_hash, check_password_hash
from db_control import add_user, get_password
from db_control import get_userid as userid


def hash_password_show(password):
    print(password)
    hashed_password = generate_password_hash(password, method='scrypt')
    print(hashed_password)
    pass


def hash_password_store(username, password):
    hashed_password = generate_password_hash(password, method='scrypt')
    add_user(username, hashed_password)
    pass


def check_password(username, password):
    stored_password = get_password(username)
    if stored_password is None:
        print("username / password does not exist")

    else:
        check_result = check_password_hash(stored_password, password)
        return check_result

def get_userid(username):
    id = userid(username)
    if id is None:
        print("username does not exist")

    else:
        return id


# Used for creating accounts manually if needed
if __name__ == '__main__':
    inputted_username = input("username for account: ")
    inputted_password = input("password to hash: ")
    hash_password_store(inputted_username, inputted_password)