import sqlite3
import jwt
import bcrypt
import os
from flask import Flask, request, jsonify, g
from flask_cors import CORS
from datetime import datetime, timedelta, timezone
from functools import wraps

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

SECRET_KEY = "ml_alarm_secret_2026"
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ml_alarm.db")


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DB_PATH)
        g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def close_db(exc):
    db = g.pop("db", None)
    if db:
        db.close()


def init_db():
    with sqlite3.connect(DB_PATH) as db:
        db.executescript("""
            CREATE TABLE IF NOT EXISTS users (
                id         INTEGER PRIMARY KEY AUTOINCREMENT,
                name       TEXT    NOT NULL,
                email      TEXT    NOT NULL UNIQUE,
                password   TEXT    NOT NULL,
                gender     TEXT,
                dob        TEXT,
                created_at TEXT    NOT NULL DEFAULT (datetime('now'))
            );
            CREATE TABLE IF NOT EXISTS alarms (
                id         INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id    INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                label      TEXT    NOT NULL DEFAULT 'Будильник',
                date       TEXT    NOT NULL,
                time       TEXT    NOT NULL,
                datetime   TEXT    NOT NULL,
                enabled    INTEGER NOT NULL DEFAULT 1,
                fired      INTEGER NOT NULL DEFAULT 0,
                created_at TEXT    NOT NULL DEFAULT (datetime('now'))
            );
        """)


def make_token(user_id):
    payload = {
        "sub": str(user_id),
        "exp": datetime.now(timezone.utc) + timedelta(days=7)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")


def require_auth(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        auth = request.headers.get("Authorization", "")
        if not auth.startswith("Bearer "):
            return jsonify({"error": "Не авторизовано"}), 401
        token = auth[7:]
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            g.user_id = payload["sub"]
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Токен прострочено"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Невірний токен"}), 401
        return f(*args, **kwargs)
    return wrapper


def row_to_dict(row):
    return dict(row) if row else None


def user_public(u):
    return {
        "id": u["id"],
        "name": u["name"],
        "email": u["email"],
        "gender": u["gender"],
        "dob": u["dob"],
        "created_at": u["created_at"],
    }


def alarm_to_dict(a):
    return {
        "id": a["id"],
        "label": a["label"],
        "date": a["date"],
        "time": a["time"],
        "datetime": a["datetime"],
        "enabled": bool(a["enabled"]),
        "fired": bool(a["fired"]),
        "created_at": a["created_at"],
    }


@app.post("/api/auth/register")
def register():
    data = request.get_json() or {}
    name = (data.get("name") or "").strip()
    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""
    gender = data.get("gender") or ""
    dob = data.get("dob") or ""

    if not name or len(name) < 2:
        return jsonify({"error": "Ім'я занадто коротке"}), 400
    if "@" not in email or "." not in email:
        return jsonify({"error": "Невірний email"}), 400
    if len(password) < 6:
        return jsonify({"error": "Пароль — мінімум 6 символів"}), 400

    db = get_db()
    if db.execute("SELECT id FROM users WHERE email=?", (email,)).fetchone():
        return jsonify({"error": "Email вже зареєстровано"}), 409

    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    cur = db.execute(
        "INSERT INTO users (name,email,password,gender,dob) VALUES (?,?,?,?,?)",
        (name, email, hashed, gender, dob)
    )
    db.commit()
    user = row_to_dict(db.execute("SELECT * FROM users WHERE id=?", (cur.lastrowid,)).fetchone())
    token = make_token(user["id"])
    return jsonify({"token": token, "user": user_public(user)}), 201


@app.post("/api/auth/login")
def login():
    data = request.get_json() or {}
    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""

    db = get_db()
    user = row_to_dict(db.execute("SELECT * FROM users WHERE email=?", (email,)).fetchone())
    if not user or not bcrypt.checkpw(password.encode(), user["password"].encode()):
        return jsonify({"error": "Невірний email або пароль"}), 401

    token = make_token(user["id"])
    return jsonify({"token": token, "user": user_public(user)})


@app.get("/api/auth/me")
@require_auth
def me():
    db = get_db()
    user = row_to_dict(db.execute("SELECT * FROM users WHERE id=?", (g.user_id,)).fetchone())
    if not user:
        return jsonify({"error": "Користувача не знайдено"}), 404
    return jsonify(user_public(user))


@app.patch("/api/auth/me")
@require_auth
def update_me():
    data = request.get_json() or {}
    name = (data.get("name") or "").strip()
    gender = data.get("gender") or ""
    dob = data.get("dob") or ""

    if not name or len(name) < 2:
        return jsonify({"error": "Ім'я занадто коротке"}), 400

    db = get_db()
    db.execute(
        "UPDATE users SET name=?, gender=?, dob=? WHERE id=?",
        (name, gender, dob, g.user_id)
    )
    db.commit()
    user = row_to_dict(db.execute("SELECT * FROM users WHERE id=?", (g.user_id,)).fetchone())
    return jsonify(user_public(user))


@app.get("/api/alarms")
@require_auth
def get_alarms():
    db = get_db()
    rows = db.execute(
        "SELECT * FROM alarms WHERE user_id=? ORDER BY datetime ASC", (g.user_id,)
    ).fetchall()
    return jsonify([alarm_to_dict(r) for r in rows])


@app.post("/api/alarms")
@require_auth
def create_alarm():
    data = request.get_json() or {}
    label = (data.get("label") or "Будильник").strip()
    date = data.get("date") or ""
    time = data.get("time") or ""

    if not date or not time:
        return jsonify({"error": "Вкажіть дату та час"}), 400

    dt_str = f"{date}T{time}"
    try:
        dt = datetime.fromisoformat(dt_str)
    except ValueError:
        return jsonify({"error": "Невірний формат дати/часу"}), 400

    if dt <= datetime.now():
        return jsonify({"error": "Час має бути в майбутньому"}), 400

    db = get_db()
    cur = db.execute(
        "INSERT INTO alarms (user_id, label, date, time, datetime) VALUES (?,?,?,?,?)",
        (g.user_id, label, date, time, dt_str)
    )
    db.commit()
    alarm = row_to_dict(db.execute("SELECT * FROM alarms WHERE id=?", (cur.lastrowid,)).fetchone())
    return jsonify(alarm_to_dict(alarm)), 201


@app.patch("/api/alarms/<int:alarm_id>")
@require_auth
def update_alarm(alarm_id):
    db = get_db()
    alarm = row_to_dict(db.execute(
        "SELECT * FROM alarms WHERE id=? AND user_id=?", (alarm_id, g.user_id)
    ).fetchone())
    if not alarm:
        return jsonify({"error": "Будильник не знайдено"}), 404

    data = request.get_json() or {}
    enabled = data.get("enabled")
    fired = data.get("fired")

    if enabled is not None:
        db.execute("UPDATE alarms SET enabled=? WHERE id=?", (int(enabled), alarm_id))
    if fired is not None:
        db.execute("UPDATE alarms SET fired=? WHERE id=?", (int(fired), alarm_id))

    db.commit()
    alarm = row_to_dict(db.execute("SELECT * FROM alarms WHERE id=?", (alarm_id,)).fetchone())
    return jsonify(alarm_to_dict(alarm))


@app.delete("/api/alarms/<int:alarm_id>")
@require_auth
def delete_alarm(alarm_id):
    db = get_db()
    result = db.execute(
        "DELETE FROM alarms WHERE id=? AND user_id=?", (alarm_id, g.user_id)
    )
    db.commit()
    if result.rowcount == 0:
        return jsonify({"error": "Будильник не знайдено"}), 404
    return jsonify({"ok": True})


if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000, debug=True)
