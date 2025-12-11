import sqlite3
import json
from typing import Optional, Dict, Any

class SQLiteStore:
    def __init__(self, path: str = "runs.db"):
        self.path = path
        self.conn = sqlite3.connect(self.path, check_same_thread=False)
        self.conn.execute(
            "create table if not exists runs (id text primary key, state text, updated_at real)"
        )
        self.conn.commit()

    def save_state(self, run_id: str, state: Dict[str, Any]):
        payload = json.dumps(state)
        self.conn.execute(
            "insert or replace into runs (id, state, updated_at) values (?, ?, strftime('%s','now'))",
            (run_id, payload),
        )
        self.conn.commit()

    def load_state(self, run_id: str) -> Optional[Dict[str, Any]]:
        cur = self.conn.execute("select state from runs where id = ?", (run_id,))
        row = cur.fetchone()
        if row:
            return json.loads(row[0])
        return None
