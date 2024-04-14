import sqlite3

def print_db_row(database_file):
    # Connect to the database
    conn = sqlite3.connect(database_file)
    cursor = conn.cursor()

    # Get the list of all tables in the database
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()

    # Print information for each table
    for table in tables:
        table_name = table[0]
        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        row_count = cursor.fetchone()[0]
        print(f"Table Name: {table_name}, Row Count: {row_count}")

    # Close the connection
    conn.close()

# Example usage
database_file = '../trades_suspects.db'

print_db_row(database_file)