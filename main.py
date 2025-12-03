import time
import sqlite3
from datetime import datetime
import psutil
from pynput import mouse, keyboard
from browser_history import get_history

DB_FILE = "activity.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS activity_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            active_app TEXT,
            mouse_moves INTEGER,
            key_presses INTEGER
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS website_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            url TEXT
        )
    """)
    conn.commit()
    conn.close()

mouse_moves = 0
key_presses = 0

def on_move(x, y):
    global mouse_moves
    mouse_moves += 1

def on_key_press(key):
    global key_presses
    key_presses += 1

def get_active_app():
    try:
        active = psutil.Process(psutil.Process().pid)
        return active.name()
    except:
        return "Unknown"

def log_activity():
    global mouse_moves, key_presses
    
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("""
        INSERT INTO activity_log (timestamp, active_app, mouse_moves, key_presses)
        VALUES (?, ?, ?, ?)
    """, (datetime.now(), get_active_app(), mouse_moves, key_presses))
    conn.commit()
    conn.close()

    mouse_moves = 0
    key_presses = 0

def log_websites():
    outputs = get_history().histories
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()

    for dt, url in outputs[-10:]:
        c.execute("INSERT INTO website_log (timestamp, url) VALUES (?, ?)", (dt, url))

    conn.commit()
    conn.close()

def main():
    init_db()

    mouse_listener = mouse.Listener(on_move=on_move)
    keyboard_listener = keyboard.Listener(on_press=on_key_press)

    mouse_listener.start()
    keyboard_listener.start()

    while True:
        log_activity()
        log_websites()
        time.sleep(10)

if __name__ == "__main__":
    main()
