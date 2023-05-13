import sqlite3


def log_bird(cursor: sqlite3.Cursor, bird_name: str, date_time: str) -> None:
    cursor.execute("INSERT INTO birds (bird_name, date_time) VALUES (?, ?)",
                   (bird_name, date_time))


def check_if_such_bird_already_seen(cursor: sqlite3.Cursor,
                                    bird_name: str) -> bool:
    cursor.execute("SELECT * FROM birds WHERE bird_name = ?", (bird_name,))
    return cursor.fetchone() is not None
