import sqlite3

# Create & Init the file
conn = sqlite3.connect("diary.db")
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS diary_entries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
''')
conn.commit()
conn.close()


def add_diary_entry(content: str):
    conn = sqlite3.connect('diary.db')
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO diary_entries (content)
        VALUES (?)
        """,
        (content,)
    )
    conn.commit()
    conn.close()
    print(f"Entry added to the diary.")

# Fetch all diary entries as a list of dicts with 'date' and 'text'
def get_all_entries():
    conn = sqlite3.connect('diary.db')
    cursor = conn.cursor()
    cursor.execute("SELECT created_at, content FROM diary_entries ORDER BY created_at DESC")
    rows = cursor.fetchall()
    conn.close()
    return [{'date': row[0], 'text': row[1]} for row in rows]