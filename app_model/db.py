import sqlite3

# Connects to the SQLite database inside the DATA folder
def get_connection():
    return sqlite3.connect("DATA/project_data.db")