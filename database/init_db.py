import sqlite3, os

def init_db(db_path: str):
    """Create all tables if they don't exist."""
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    conn = sqlite3.connect(db_path)
    c    = conn.cursor()

    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            username  TEXT    UNIQUE NOT NULL,
            password  TEXT    NOT NULL,
            nom       TEXT    DEFAULT '',
            prenom    TEXT    DEFAULT '',
            role      TEXT    DEFAULT 'medecin'
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS analyses (
            id           INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id      INTEGER NOT NULL,
            image_path   TEXT    NOT NULL,
            prediction   TEXT    NOT NULL,
            confidence   REAL    NOT NULL,
            prob_covid   REAL    DEFAULT 0,
            prob_normal  REAL    DEFAULT 0,
            prob_pneum   REAL    DEFAULT 0,
            created_at   DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')

    conn.commit()
    conn.close()
    print(" Base de données initialisée :", db_path)
