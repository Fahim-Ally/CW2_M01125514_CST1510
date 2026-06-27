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


def main():
    # Asking for a password and generate its hash
    password = input("Enter a password to hash: > ")
    hashed_password = generate_hash(password)
    
    # Showing the hash instead of the original password
    print("\nGenerated hash:")
    print(hashed_password)

    password_check = input("\nEnter the password again for verification:  ")

    if is_valid_hash(password_check, hashed_password):
        print("Password verified successfully.")
    else:
        print("Password does not match.")


if __name__ == "__main__":
    main()