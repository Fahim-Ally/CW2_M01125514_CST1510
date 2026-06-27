import pandas as pd

# Loads cyber_incidents.csv into SQLite
def migrate_cyber_incidents(conn):
    data = pd.read_csv("DATA/cyber_incidents.csv")
    data.to_sql("cyber_incidents", conn, if_exists="replace", index=False)


# Reads the cyber_incidents table back from SQLite
def get_all_cyber_incidents(conn):
    sql = "SELECT * FROM cyber_incidents"
    return pd.read_sql(sql, conn)