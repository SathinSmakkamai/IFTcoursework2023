import sqlite3
from modules.db.connect_to_db import connect_to_db

class create_table:

    def create_SQL_table_new(conf):

        # Read SQL script from file
        with open(conf['SQLite']['create_table_path'], 'r') as file:
            sql_script = file.read()

        # connect to SQLite database
        conn, cur = connect_to_db.connect_to_SQLite(conf)

        # Execute SQL script
        cur.executescript(sql_script)

        # Commit changes and close connection
        conn.commit()
        conn.close()
