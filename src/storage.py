import sqlite3
from config.settings import DB_CONFIG


def save_to_database(data):
    if DB_CONFIG["type"] == "sqlite":
        conn = sqlite3.connect(DB_CONFIG["sqlite_path"])
        cursor = conn.cursor()

        cursor.execute(
            """
        CREATE TABLE IF NOT EXISTS agents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            company TEXT,
            location TEXT
        )
        """
        )

        for agent in data:
            cursor.execute(
                "INSERT INTO agents (name, company, location) VALUES (?, ?, ?)",
                (agent["name"], agent["company"], agent["location"]),
            )

        conn.commit()
        conn.close()
        print("数据已存入数据库！")
