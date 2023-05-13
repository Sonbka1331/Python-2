import sqlite3
import random


def generate_test_data(cursor: sqlite3.Cursor, number_of_groups: int) -> None:

    commands = []
    for i in range(number_of_groups):
        strong_team = f"Strong {i + 1}"
        middle_team1 = f"Middle1 {i + 1}"
        middle_team2 = f"Middle2 {i + 1}"
        weak_team = f"Weak {i + 1}"
        commands.append((strong_team, "Country", "Strong"))
        commands.append((middle_team1, "Country", "Middle"))
        commands.append((middle_team2, "Country", "Middle"))
        commands.append((weak_team, "Country", "Weak"))

    # Жеребьевка
    random.shuffle(commands)
    groups = [f"Group {i + 1}" for i in range(number_of_groups)]
    draw = []
    for i in range(number_of_groups):
        draw.append((commands[i * 4][0], groups[i]))
        draw.append((commands[i * 4 + 1][0], groups[i]))
        draw.append((commands[i * 4 + 2][0], groups[i]))
        draw.append((commands[i * 4 + 3][0], groups[i]))

    cursor.executemany("INSERT INTO uefa_commands VALUES (NULL,?,?,?)",
                       commands)
    cursor.executemany("INSERT INTO uefa_draw VALUES (?,?)", draw)
