import sqlite3

# ══════════════════════════════════════════
#  MODEL — Analysis  (M in MVC)
# ══════════════════════════════════════════

class Analysis:

    @staticmethod
    def save(user_id, image_path, prediction, confidence,
             prob_covid, prob_normal, prob_pneum, db_path):
        conn   = sqlite3.connect(db_path)
        cursor = conn.execute(
            '''INSERT INTO analyses
               (user_id, image_path, prediction, confidence,
                prob_covid, prob_normal, prob_pneum)
               VALUES (?,?,?,?,?,?,?)''',
            (user_id, image_path, prediction, confidence,
             prob_covid, prob_normal, prob_pneum)
        )
        conn.commit()
        rid = cursor.lastrowid
        conn.close()
        return rid

    @staticmethod
    def get_by_user(user_id, db_path, limit=100):
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        rows = conn.execute(
            'SELECT * FROM analyses WHERE user_id=? ORDER BY created_at DESC LIMIT ?',
            (user_id, limit)
        ).fetchall()
        conn.close()
        return [dict(r) for r in rows]

    @staticmethod
    def get_by_id(analysis_id, db_path):
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        row  = conn.execute('SELECT * FROM analyses WHERE id=?', (analysis_id,)).fetchone()
        conn.close()
        return dict(row) if row else None

    @staticmethod
    def count_by_user(user_id, db_path):
        conn = sqlite3.connect(db_path)
        n    = conn.execute('SELECT COUNT(*) FROM analyses WHERE user_id=?', (user_id,)).fetchone()[0]
        conn.close()
        return n
