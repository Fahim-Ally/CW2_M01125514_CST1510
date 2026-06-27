from app_model.db import get_connection
from app_model.schema import setup_database
from app_model.users import get_all_users, login_user, register_user
from app_model.cyber_incidents import get_all_cyber_incidents
from app_model.metadatas import get_all_datasets_metadata
from app_model.it_tickets import get_all_it_tickets


# Shows the terminal menu for the SQLite version
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
            # Display users saved in the SQLite database
            for user in get_all_users(conn):
                print(user)
        elif choice == "4":
            # Display row counts to confirm CSV files were migrated
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