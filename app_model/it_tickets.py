import pandas as pd

# Loads it_tickets.csv into SQLite
def migrate_it_tickets(conn):
    data = pd.read_csv("DATA/it_tickets.csv")
    data.to_sql("it_tickets", conn, if_exists="replace", index=False)

# Reads the it_tickets table back from SQLite
def get_all_it_tickets(conn):
    sql = "SELECT * FROM it_tickets"
    return pd.read_sql(sql, conn)