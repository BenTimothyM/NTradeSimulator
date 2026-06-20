# ==============================================================================
# Developed By Ben Timothy
# NTrade Simulator - Professional Retro-Cyber Financial Dashboard & Game Engine
# ==============================================================================

import sqlite3
import json
import os

DB_FILE = "ntrade_simulator.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS saves (
            slot_id INTEGER PRIMARY KEY,
            slot_name TEXT NOT NULL,
            state_json TEXT NOT NULL,
            is_hardcore INTEGER DEFAULT 0,
            is_dead INTEGER DEFAULT 0
        )
    """)
    conn.commit()
    conn.close()

def save_game(slot_id, slot_name, state_dict, is_hardcore=0, is_dead=0):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    state_json = json.dumps(state_dict)
    cursor.execute("""
        INSERT OR REPLACE INTO saves (slot_id, slot_name, state_json, is_hardcore, is_dead)
        VALUES (?, ?, ?, ?, ?)
    """, (slot_id, slot_name, state_json, int(is_hardcore), int(is_dead)))
    conn.commit()
    conn.close()

def load_game(slot_id):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT state_json, is_hardcore, is_dead FROM saves WHERE slot_id = ?", (slot_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return json.loads(row[0]), bool(row[1]), bool(row[2])
    return None, False, False

def delete_save_file(slot_id):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM saves WHERE slot_id = ?", (slot_id,))
    conn.commit()
    conn.close()

def get_slots():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT slot_id, slot_name, is_hardcore, is_dead FROM saves ORDER BY slot_id ASC")
    rows = cursor.fetchall()
    conn.close()
    return rows