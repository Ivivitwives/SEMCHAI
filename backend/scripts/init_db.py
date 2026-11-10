import sqlite3
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
DB_PATH = BASE / "data" / "semchai.db"
SCHEMA_PATH = BASE / "database" / "schema.sql"

def main():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(DB_PATH) as conn:
        conn.executescript(SCHEMA_PATH.read_text(encoding="utf-8"))
    print(f"Database ready: {DB_PATH}")

if __name__ == "__main__":
    main()