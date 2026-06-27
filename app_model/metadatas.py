import pandas as pd

# Loads datasets_metadata.csv into SQLite
def migrate_datasets_metadata(conn):
    data = pd.read_csv("DATA/datasets_metadata.csv")
    data.to_sql("datasets_metadata", conn, if_exists="replace", index=False)

# Reads the datasets_metadata table back from SQLite
def get_all_datasets_metadata(conn):
    sql = "SELECT * FROM datasets_metadata"
    return pd.read_sql(sql, conn)