"""
MediPlant AI - Database Module
SQLite database for users, history, saved plants, and feedback
"""

import sqlite3
import hashlib
import os
from datetime import datetime


DB_PATH = "database/mediaplant.db"
os.makedirs("database", exist_ok=True)


def get_connection():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_database():
    """Create all tables if they don't exist."""
    conn = get_connection()
    c    = conn.cursor()

    c.executescript("""
    CREATE TABLE IF NOT EXISTS users (
        id            INTEGER PRIMARY KEY AUTOINCREMENT,
        username      TEXT UNIQUE NOT NULL,
        email         TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        full_name     TEXT,
        bio           TEXT,
        created_at    TEXT DEFAULT CURRENT_TIMESTAMP,
        last_login    TEXT
    );

    CREATE TABLE IF NOT EXISTS predictions (
        id             INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id        INTEGER,
        plant_name     TEXT NOT NULL,
        confidence     REAL NOT NULL,
        model_used     TEXT,
        image_path     TEXT,
        gradcam_path   TEXT,
        is_saved       INTEGER DEFAULT 0,
        user_feedback  TEXT,
        created_at     TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(user_id) REFERENCES users(id)
    );

    CREATE TABLE IF NOT EXISTS saved_plants (
        id         INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id    INTEGER NOT NULL,
        plant_name TEXT NOT NULL,
        notes      TEXT,
        saved_at   TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(user_id) REFERENCES users(id)
    );

    CREATE TABLE IF NOT EXISTS feedback (
        id             INTEGER PRIMARY KEY AUTOINCREMENT,
        prediction_id  INTEGER,
        user_id        INTEGER,
        is_correct     INTEGER,
        correct_plant  TEXT,
        comments       TEXT,
        created_at     TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(prediction_id) REFERENCES predictions(id)
    );

    CREATE TABLE IF NOT EXISTS chat_history (
        id         INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id    INTEGER,
        role       TEXT NOT NULL,
        message    TEXT NOT NULL,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(user_id) REFERENCES users(id)
    );
    """)

    conn.commit()
    conn.close()


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


# ── User operations ───────────────────────────────────────────────────────────
def register_user(username, email, password, full_name=""):
    conn = get_connection()
    c    = conn.cursor()
    try:
        c.execute(
            "INSERT INTO users (username, email, password_hash, full_name) VALUES (?,?,?,?)",
            (username, email, hash_password(password), full_name)
        )
        conn.commit()
        return True, "Registration successful!"
    except sqlite3.IntegrityError as e:
        if "username" in str(e):
            return False, "Username already exists."
        return False, "Email already registered."
    finally:
        conn.close()


def login_user(username, password):
    conn = get_connection()
    c    = conn.cursor()
    c.execute(
        "SELECT * FROM users WHERE username=? AND password_hash=?",
        (username, hash_password(password))
    )
    user = c.fetchone()
    if user:
        c.execute("UPDATE users SET last_login=? WHERE id=?",
                  (datetime.now().isoformat(), user["id"]))
        conn.commit()
    conn.close()
    return dict(user) if user else None


def get_user(user_id):
    conn = get_connection()
    c    = conn.cursor()
    c.execute("SELECT * FROM users WHERE id=?", (user_id,))
    user = c.fetchone()
    conn.close()
    return dict(user) if user else None


def update_profile(user_id, full_name, bio):
    conn = get_connection()
    c    = conn.cursor()
    c.execute("UPDATE users SET full_name=?, bio=? WHERE id=?", (full_name, bio, user_id))
    conn.commit()
    conn.close()


# ── Prediction operations ─────────────────────────────────────────────────────
def save_prediction(user_id, plant_name, confidence, model_used):
    conn = get_connection()
    c    = conn.cursor()
    c.execute(
        """INSERT INTO predictions
           (user_id, plant_name, confidence, model_used, created_at)
           VALUES (?,?,?,?,?)""",
        (user_id, plant_name, confidence, model_used, datetime.now().isoformat())
    )
    pred_id = c.lastrowid
    conn.commit()
    conn.close()
    return pred_id


def get_user_predictions(user_id, limit=50):
    conn  = get_connection()
    c     = conn.cursor()
    c.execute(
        "SELECT * FROM predictions WHERE user_id=? ORDER BY created_at DESC LIMIT ?",
        (user_id, limit)
    )
    rows  = c.fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_all_predictions(limit=100):
    conn  = get_connection()
    c     = conn.cursor()
    c.execute("SELECT * FROM predictions ORDER BY created_at DESC LIMIT ?", (limit,))
    rows  = c.fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_stats():
    conn = get_connection()
    c    = conn.cursor()
    c.execute("SELECT COUNT(*) as total FROM predictions")
    total = c.fetchone()["total"]
    c.execute("SELECT COUNT(*) as users FROM users")
    users = c.fetchone()["users"]
    c.execute("SELECT plant_name, COUNT(*) as cnt FROM predictions GROUP BY plant_name ORDER BY cnt DESC LIMIT 5")
    top_plants = [dict(r) for r in c.fetchall()]
    c.execute("SELECT AVG(confidence) as avg_conf FROM predictions")
    avg_conf = c.fetchone()["avg_conf"] or 0
    conn.close()
    return {
        "total_predictions": total,
        "total_users"      : users,
        "top_plants"       : top_plants,
        "avg_confidence"   : avg_conf
    }


# ── Saved plants ──────────────────────────────────────────────────────────────
def save_plant_to_collection(user_id, plant_name, notes=""):
    conn = get_connection()
    c    = conn.cursor()
    c.execute(
        "INSERT INTO saved_plants (user_id, plant_name, notes, saved_at) VALUES (?,?,?,?)",
        (user_id, plant_name, notes, datetime.now().isoformat())
    )
    conn.commit()
    conn.close()


def get_saved_plants(user_id):
    conn  = get_connection()
    c     = conn.cursor()
    c.execute("SELECT * FROM saved_plants WHERE user_id=? ORDER BY saved_at DESC", (user_id,))
    rows  = c.fetchall()
    conn.close()
    return [dict(r) for r in rows]


def remove_saved_plant(save_id, user_id):
    conn = get_connection()
    c    = conn.cursor()
    c.execute("DELETE FROM saved_plants WHERE id=? AND user_id=?", (save_id, user_id))
    conn.commit()
    conn.close()


# ── Chat history ──────────────────────────────────────────────────────────────
def save_chat_message(user_id, role, message):
    conn = get_connection()
    c    = conn.cursor()
    c.execute(
        "INSERT INTO chat_history (user_id, role, message) VALUES (?,?,?)",
        (user_id, role, message)
    )
    conn.commit()
    conn.close()


def get_chat_history(user_id, limit=50):
    conn  = get_connection()
    c     = conn.cursor()
    c.execute(
        "SELECT * FROM chat_history WHERE user_id=? ORDER BY created_at DESC LIMIT ?",
        (user_id, limit)
    )
    rows  = c.fetchall()
    conn.close()
    return [dict(r) for r in reversed(rows)]


# Initialise on import
init_database()
