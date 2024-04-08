
import sqlite3

def count_rows(database_file):
    # Connect to the database
    conn = sqlite3.connect(database_file)
    cursor = conn.cursor()

    # Get the list of all tables in the database
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    table_name = cursor.fetchone()[0]

    # Execute a query to count rows in the table
    cursor.execute(f"SELECT COUNT(*) FROM {table_name}")

    # Fetch the result
    row_count = cursor.fetchone()[0]

    # Close the connection
    conn.close()

    return row_count, table_name

# Example usage
database_file = 'trades_suspects.db'
row_count, table_name = count_rows(database_file)
print(f"Number of rows in {table_name}: {row_count}")