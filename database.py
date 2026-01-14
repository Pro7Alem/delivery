import sqlite3
from typing import List, Dict, Any, Optional

DB_FILE = "database/database.db"

def get_conn():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")

    return conn

def exec_query(sql: str, params: tuple = ()) -> List[Dict[str, Any]]:
    """Para buscar dados (SELECT)"""
    with get_conn() as conn:
        cur = conn.execute(sql, params)

        return [dict(row) for row in cur.fetchall()]

def exec_command(sql: str, params: tuple = ()) -> int:
    """Para salvar/alterar dados (INSERT, UPDATE, DELETE)"""
    with get_conn() as conn:
        cur = conn.execute(sql, params)
        conn.commit()
        return cur.lastrowid
