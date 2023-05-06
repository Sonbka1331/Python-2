import sqlite3


with sqlite3.connect("example.db") as conn:

    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;")

    cursor.execute("""
        CREATE TABLE actors (
            act_id INTEGER PRIMARY KEY,
            act_first_name VARCHAR (50),
            act_last_name VARCHAR (50),
            act_gender VARCHAR (1)
        )
    """)

    cursor.execute("""
        CREATE TABLE movie (
            mov_id INTEGER PRIMARY KEY,
            movie_title VARCHAR (50)
        )
    """)

    cursor.execute("""
        CREATE TABLE director (
            dir_id INTEGER PRIMARY KEY,
            dir_first_name VARCHAR (50),
            dir_last_name VARCHAR (50)
        )
    """)

    cursor.execute("""
        CREATE TABLE movie_cast (
            act_id INTEGER REFERENCES actors(act_id),
            mov_id INTEGER REFERENCES movie(mov_id),
            role VARCHAR (50)
        )
    """)

    cursor.execute("""
        CREATE TABLE oscar_awarded (
            award_id INTEGER PRIMARY KEY,
            mov_id INTEGER REFERENCES movie(mov_id)
        )
    """)

    cursor.execute("""
        CREATE TABLE movie_director (
            dir_id INTEGER REFERENCES director(dir_id),
            mov_id INTEGER REFERENCES movie(mov_id)
        )
    """)

    conn.commit()
