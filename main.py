import bcrypt

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

# Registers a new user and save their hashed password
def register_user():
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
def login_user():
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

# Show the terminal menu for registration and login
def main():
    # Keep showing the menu until the user chooses to exit
    while True:
        print("\n1. To Register")
        print("2. To Log in")
        print("3. To Exit")
        
        # Get the user's menu choice
        choice = input(": ").strip()

        if choice == "1":
            register_user()
        elif choice == "2":
            if login_user():
                print("Login successful!")
            else:
                print("Incorrect login.")
        elif choice == "3":
            # Stop the loop and end the program
            print("Goodbye!")
            break
        else:
            # Error message for wrong input
            print("Please choose 1, 2, or 3.")


# Run main() only when this file is executed directly.
if __name__ == "__main__":
    main()
