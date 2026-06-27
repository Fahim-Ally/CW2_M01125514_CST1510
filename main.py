import bcrypt
import sqlite3
import pandas as pd

# === PASSWORD HASHING ===
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

# === REGISTER/LOGIN ===
# Registers a new user and save their hashed password
def register_user_file():
    # Collecting the new user's details.
    name = input("Enter your name: ").strip()
    password = input("Enter your password: ")

    # Hash the password before saving it
    hashed_password = generate_hash(password)

    # Stores the username & hashed password in the flat file
    with open("users.txt", "a") as f:
        f.write(f"{name},{hashed_password}\n")

    print("User successfully registered!")

# Check a user's login details with users.txt
def login_user_file():
    # Collecting the login details.
    name = input("Enter your name: ").strip()
    password = input("Enter your password: ")

    try:
        # Reading all saved users from the flat file
        with open("users.txt", "r") as f:
            users = f.readlines()
    except FileNotFoundError:
        # If no user has registered yet, there is no login to check
        return False
    
    # Check each saved user until a matching username and password is found
    for user in users:
        # Ignoring empty lines
        if not user.strip():
            continue

        # Split each line into username and saved password hash.
        user_name, user_hash = user.strip().split(",", 1)

        # Login succeeds only when both username and password are correct.
        if name == user_name and is_valid_hash(password, user_hash):
            return True

    return False

# === SQLite DATABASE VERSION ===
# Connects to the SQLite database inside the DATA folder
def get_connection():
    return sqlite3.connect("DATA/project_data.db")


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


# Loads cyber_incidents.csv into SQLite
def migrate_cyber_incidents(conn):
    data = pd.read_csv("DATA/cyber_incidents.csv")
    data.to_sql("cyber_incidents", conn, if_exists="replace", index=False)


# Loads datasets_metadata.csv into SQLite
def migrate_datasets_metadata(conn):
    data = pd.read_csv("DATA/datasets_metadata.csv")
    data.to_sql("datasets_metadata", conn, if_exists="replace", index=False)


# Loads it_tickets.csv into SQLite
def migrate_it_tickets(conn):
    data = pd.read_csv("DATA/it_tickets.csv")
    data.to_sql("it_tickets", conn, if_exists="replace", index=False)


# Reads cyber_incidents table back from SQLite
def get_all_cyber_incidents(conn):
    sql = "SELECT * FROM cyber_incidents"
    return pd.read_sql(sql, conn)


# Reads datasets_metadata table back from SQLite
def get_all_datasets_metadata(conn):
    sql = "SELECT * FROM datasets_metadata"
    return pd.read_sql(sql, conn)


# Reads it_tickets table back from SQLite
def get_all_it_tickets(conn):
    sql = "SELECT * FROM it_tickets"
    return pd.read_sql(sql, conn)


# Creates tables and loads the CSV files into the database
def setup_database(conn):
    create_user_table(conn)
    migrate_cyber_incidents(conn)
    migrate_datasets_metadata(conn)
    migrate_it_tickets(conn)


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

# Show the terminal menu for registration and login
def main():
    # Connect to the SQLite database
    conn = get_connection()

    # Create database tables and load the CSV files
    setup_database(conn)

    # Keep showing the menu until the user chooses to exit
    while True:
        print("\n1. To Register")
        print("2. To Log in")
        print("3. To View Users")
        print("4. To View Dataset Counts")
        print("5. To Exit")

        # Get the user's menu choice
        choice = input(": ").strip()

        if choice == "1":
            register_user(conn)
        elif choice == "2":
            if login_user(conn):
                print("Login successful!")
            else:
                print("Incorrect login.")
        elif choice == "3":
            # Displaying users saved in the SQLite database
            for user in get_all_users(conn):
                print(user)
        elif choice == "4":
            # Displaying row counts to confirm CSV files were migrated
            print(f"Cyber incidents: {len(get_all_cyber_incidents(conn))}")
            print(f"Dataset metadata: {len(get_all_datasets_metadata(conn))}")
            print(f"IT tickets: {len(get_all_it_tickets(conn))}")
        elif choice == "5":
            # Close the database before ending the program
            conn.close()
            print("Goodbye!")
            break
        else:
            print("Please choose a valid option.")


# Run main() only when this file is executed directly
if __name__ == "__main__":
    main()