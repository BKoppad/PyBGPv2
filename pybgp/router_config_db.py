import sqlite3


def create_table():
    """Creating a table if does not exist else connect to it"""
    conn = sqlite3.connect("router_config.db")
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS cisco_config \
                (config_name TEXT, config_value TEXT)")
    conn.commit()
    conn.close()


def insert_table(config_name, config_value):
    """Insert a row to the table"""
    conn = sqlite3.connect("router_config.db")
    cur = conn.cursor()
    cur.execute("INSERT INTO cisco_config VALUES (?,?)",
                (config_name, config_value))
    conn.commit()
    conn.close()


def view():
    """View the Entire Table present in the DB"""
    conn = sqlite3.connect("router_config.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM cisco_config")
    rows = cur.fetchall()
    conn.close()
    return rows


def get_config(config_name):
    """Get the required row/config"""
    conn = sqlite3.connect("router_config.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM cisco_config WHERE config_name=?",
                (config_name,))
    rows = cur.fetchall()
    conn.close()
    return rows[0][1].split(",")


def delet(config_name):
    """Delete the require row/config"""
    conn = sqlite3.connect("router_config.db")
    cur = conn.cursor()
    cur.execute("DELETE FROM cisco_config WHERE config_name=?", (config_name,))
    conn.commit()
    conn.close


def update(config_name, config_value):
    """Update the existing row/config"""
    conn = sqlite3.connect("router_config.db")
    cur = conn.cursor()
    cur.execute("UPDATE cisco_config SET config_value=? WHERE config_name=?",
                (config_value, config_name))
    conn.commit()
    conn.close
