import sqlite3
import pandas as pd

DB_NAME = "renting_animals.db"

def init_database():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute("CREATE TABLE IF NOT EXISTS chien(name, price, location, image_url)")
    c.execute("CREATE TABLE IF NOT EXISTS mouton(name, price, location, image_url)")
    c.execute("CREATE TABLE IF NOT EXISTS volaille(name, price, location, image_url)")
    c.execute("CREATE TABLE IF NOT EXISTS autre(name, price, location, image_url)")

    conn.commit()
    conn.close()

def save_to_db(df, table_name):
    conn = sqlite3.connect(DB_NAME)
    df.to_sql(table_name, conn, if_exists="append", index=False)
    conn.commit()
    conn.close()

def load_from_db(table_name):
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
    conn.close()
    return df
