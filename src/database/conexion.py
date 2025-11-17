import sqlite3
from src.paths import DB_PATH

def conectarBase():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    return conn, cursor