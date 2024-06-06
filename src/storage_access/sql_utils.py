import sqlite3

def update_database(track_id, file_path, db_path='audio_tracks.db'):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tracks (
            track_id TEXT PRIMARY KEY,
            file_path TEXT
        )
    ''')
    
    cursor.execute('''
        INSERT OR REPLACE INTO tracks (track_id, file_path)
        VALUES (?, ?)
    ''', (track_id, file_path))
    
    conn.commit()
    conn.close()
