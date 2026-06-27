import bcrypt
import sqlite3


# Creates a secure bcrypt hash from a plain-text password
def generate_hash(psw):
    # Converting user's password into bytes for bcrypt
    byte_psw = psw.encode("utf-8")

    # Creating a random salt so each hash is unique
    salt = bcrypt.gensalt()

    # Hashing the password with the salt
    hashed_password = bcrypt.hashpw(byte_psw, salt)

    # Converting the hash to text so it can be stored
    return hashed_password.decode("utf-8")


# Checks whether a plain-text password matches a bcrypt hash
def is_valid_hash(psw, hashed_password):
    # Converting the entered password and stored hash into bytes
    byte_psw = psw.encode("utf-8")
    byte_hash = hashed_password.encode("utf-8")

    # Return True if the password matches the hash
    return bcrypt.checkpw(byte_psw, byte_hash)


# Registers a new user and saves their hashed password in users.txt
def register_user_file():
    # Collecting the new user's details
    name = input("Enter your name: ").strip()
    password = input("Enter your password: ")

    # Hashing the password before saving it
    hashed_password = generate_hash(password)

    # Storing username and hashed password in the flat file
    with open("users.txt", "a") as f:
        f.write(f"{name},{hashed_password}\n")

    print("User successfully registered!")


# Checks login details using users.txt
def login_user_file():
    # Collecting the login details
    name = input("Enter your name: ").strip()
    password = input("Enter your password: ")

    try:
        # Reading all saved users from users.txt
        with open("users.txt", "r") as f:
            users = f.readlines()
    except FileNotFoundError:
        # If users.txt does not exist, no users have registered yet
        return False

    # Checking each saved user until a match is found
    for user in users:
        # Ignoring empty lines
        if not user.strip():
            continue

        # Splitting each line into username and saved password hash
        user_name, user_hash = user.strip().split(",", 1)

        # Login succeeds only when username and password are both correct
        if name == user_name and is_valid_hash(password, user_hash):
            return True

    return False


# Creates the users table if it does not already exist
def create_user_table(conn):
    cur = conn.cursor()

    sql = """CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password_hash TEXT NOT NULL,
        role TEXT DEFAULT 'user'
    );"""

    cur.execute(sql)
    conn.commit()


# Adds a new user to the users table
def add_user(conn, name, hashed_password):
    cur = conn.cursor()

    # ? placeholders help protect against SQL injection
    sql = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
    cur.execute(sql, (name, hashed_password))
    conn.commit()


# Returns all users from the database
def get_all_users(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM users")
    return cur.fetchall()


# Finds one user by username
def get_user(conn, name):
    cur = conn.cursor()

    # Searches for a user with the entered username
    cur.execute("SELECT * FROM users WHERE username = ?", (name,))
    return cur.fetchone()


# Updates a username in the database
def update_user(conn, old_name, new_name):
    cur = conn.cursor()
    cur.execute(
        "UPDATE users SET username = ? WHERE username = ?",
        (new_name, old_name),
    )
    conn.commit()


# Deletes a user from the database
def delete_user(conn, user_name):
    cur = conn.cursor()
    cur.execute("DELETE FROM users WHERE username = ?", (user_name,))
    conn.commit()


# Registers a new user using SQLite instead of users.txt
def register_user(conn):
    # Collecting the new user's details
    name = input("Enter your name: ").strip()
    password = input("Enter your password: ")

    # Hashing the password before storing it in the database
    hashed_password = generate_hash(password)

    try:
        # Saving the username and hashed password in SQLite
        add_user(conn, name, hashed_password)
        print("User successfully registered!")
    except sqlite3.IntegrityError:
        # This happens if the username already exists
        print("Username already exists.")


# Logs in a user using SQLite instead of users.txt
def login_user(conn):
    # Collecting the login details
    name = input("Enter your name: ").strip()
    password = input("Enter your password: ")

    # Searching for the user in the database
    user = get_user(conn, name)

    # If the user does not exist, login fails
    if user is None:
        return False

    # The password hash is stored in column index 2
    user_hash = user[2]

    # Checking whether the entered password matches the saved hash
    return is_valid_hash(password, user_hash)