import sqlite3
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

# ══════════════════════════════════════════
#  MODEL — User  (M in MVC)
# ══════════════════════════════════════════

class User(UserMixin):
    def __init__(self, id, username, nom='', prenom='', role='medecin'):
        self.id       = id
        self.username = username
        self.nom      = nom
        self.prenom   = prenom
        self.role     = role

    # ── Read
    @staticmethod
    def get_by_id(user_id, db_path):
        conn = sqlite3.connect(db_path)
        row  = conn.execute('SELECT * FROM users WHERE id=?', (user_id,)).fetchone()
        conn.close()
        if row:
            return User(row[0], row[1], row[3], row[4], row[5])
        return None

    @staticmethod
    def get_by_username(username, db_path):
        conn = sqlite3.connect(db_path)
        row  = conn.execute('SELECT * FROM users WHERE username=?', (username,)).fetchone()
        conn.close()
        if row:
            return User(row[0], row[1], row[3], row[4], row[5]), row[2]
        return None, None

    # ── Create
    @staticmethod
    def create(username, password, nom, prenom, db_path):
        hashed = generate_password_hash(password)
        conn   = sqlite3.connect(db_path)
        try:
            conn.execute(
                'INSERT INTO users (username, password, nom, prenom) VALUES (?,?,?,?)',
                (username, hashed, nom, prenom)
            )
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        finally:
            conn.close()

    # ── Verify
    @staticmethod
    def verify_password(plain, hashed):
        return check_password_hash(hashed, plain)
