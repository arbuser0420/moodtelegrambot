import sqlite3

conn = sqlite3.connect('mood_tracker.db', check_same_thread=False)
cursor = conn.cursor()

def create_table():
  cursor.execute('''CREATE TABLE IF NOT EXISTS moods(
                    user_id INTEGER,
                    date TEXT,
                    mood INTEGER
                  )''')
  conn.commit()

def save_mood (user_id, date, mood):
  cursor.execute('INSERT INTO moods (user_id, date, mood) VALUES (?, ?, ?)', (user_id, date, mood))
  conn.commit()

def get_moods(user_id):
  cursor.execute('SELECT date, mood FROM moods WHERE user_id = ?', (user_id,))
  return cursor.fetchall()