import sqlite3
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
DB_PATH = BASE / "data" / "semchai.db"

CATEGORIES = {
    "anxiety": "Worry, fear, or nervousness",
    "stress": "Pressure from school, work, or life",
    "sadness": "Feeling down, low, or lonely",
    "general": "General questions or conversation",
}

# PLACEHOLDER responses: replace with a professionally reviewed set
RESPONSES = {
    "anxiety": [
        "It sounds like you're feeling really worried. Would you like to tell me more about what's on your mind?",
        "Feeling anxious can be exhausting. Taking a slow breath may help a little. What is making you feel this way?",
    ],
    "stress": [
        "That sounds like a lot to carry. What feels like the heaviest part right now?",
        "Stress can build up quickly. Would it help to talk through what you need to get done?",
    ],
    "sadness": [
        "I'm sorry you're feeling this way. I'm here to listen. What has been happening?",
        "Feeling low is hard. You don't have to go through it alone. Do you want to share more?",
    ],
    "general": [
        "I'm here to listen and support you. What would you like to talk about?",
    ],
}

SETTINGS = {
    "crisis_threshold": "0.40",
    "similarity_threshold": "0.35",
}

def main():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("PRAGMA foreign_keys = ON")
        cur = conn.cursor()

        for name, desc in CATEGORIES.items():
            cur.execute(
                "INSERT OR IGNORE INTO categories (name, description) VALUES (?, ?)",
                (name, desc),
            )

        for name, texts in RESPONSES.items():
            cat_id = cur.execute(
                "SELECT id FROM categories WHERE name = ?", (name,)
            ).fetchone()[0]
            for text in texts:
                cur.execute(
                    "INSERT OR IGNORE INTO responses (category_id, text) VALUES (?, ?)",
                    (cat_id, text),
                )

        cur.execute("SELECT COUNT(*) FROM crisis_resources")
        if cur.fetchone()[0] == 0:
            cur.execute(
                "INSERT INTO crisis_resources (name, contact, source_url, verified_on) VALUES (?, ?, ?, ?)",
                (
                    "NCMH Crisis Hotline",
                    "VERIFY BEFORE USE",
                    "https://doh.gov.ph/NCMH-Crisis-Hotline",
                    None,
                ),
            )

        for key, value in SETTINGS.items():
            cur.execute(
                "INSERT OR IGNORE INTO settings (key, value) VALUES (?, ?)",
                (key, value),
            )

        conn.commit()
    print("Seed data added.")

if __name__ == "__main__":
    main()