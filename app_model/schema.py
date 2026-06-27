from app_model.cyber_incidents import migrate_cyber_incidents
from app_model.it_tickets import migrate_it_tickets
from app_model.metadatas import migrate_datasets_metadata
from app_model.users import create_user_table


# Creates database tables and loads CSV files into SQLite
def setup_database(conn):
    create_user_table(conn)
    migrate_cyber_incidents(conn)
    migrate_datasets_metadata(conn)
    migrate_it_tickets(conn)