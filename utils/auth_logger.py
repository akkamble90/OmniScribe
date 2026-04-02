import sqlite3
import pandas as pd
from datetime import datetime
import os

DB_PATH = os.path.join("data", "system.db")

def init_db():
    if not os.path.exists("data"): os.makedirs("data")
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY, password TEXT)')
    c.execute('CREATE TABLE IF NOT EXISTS audit_logs (user TEXT, action TEXT, document TEXT, timestamp TEXT)')
    # Default user for testing
    c.execute('INSERT OR IGNORE INTO users VALUES ("admin", "admin123")')
    conn.commit()
    conn.close()

def log_action(user, action, document="N/A"):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO audit_logs VALUES (?, ?, ?, ?)", 
              (user, action, document, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()

def get_audit_report():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM audit_logs", conn)
    conn.close()
    return df