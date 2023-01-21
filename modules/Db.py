import sqlite3
import os

class Database:
    def __init__(self,filename):
        self.FILENAME = filename
    
    def connect(self):
        self.conn = sqlite3.connect(self.FILENAME)

    def disconnect(self):
        self.conn.close()

    def commit(self):
        self.conn.commit()
    
    def seed(self):
        self.conn.execute("""CREATE TABLE queue (
            MusicTitle TEXT,
            MusicName TEXT,
            MusicArtist TEXT,
            MusicDuration TEXT
        )""")

    def add_music(self,tp):
        self.conn.execute("INSERT INTO queue VALUES (?,?,?,?)",tp)

    def get_first_music(self):
        result = list(self.conn.execute("SELECT * FROM queue LIMIT 1"))[0][0]
        self.conn.execute('DELETE FROM queue WHERE MusicTitle="{0}"'.format(result))
        self.commit()
        return result

    def peek_next_music(self):
        result = list(self.conn.execute("SELECT * FROM queue LIMIT 1"))[0][0]
        return result

    def count_rows(self):
        results = self.conn.execute("SELECT COUNT(*) FROM queue").fetchone()[0]
        return results