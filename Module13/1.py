import sqlite3


def check_if_vaccine_has_spoiled(cursor: sqlite3.Cursor, truck_number: str) -> bool:
    query = """
        SELECT COUNT(*)
        FROM table_truck_with_vaccine
        WHERE truck_number = ? AND 
              timestamp BETWEEN datetime('now', '-3 hours') AND datetime('now') AND
              (temperature < -16 OR temperature > -20);
    """
    cursor.execute(query, (truck_number,))
    count = cursor.fetchone()[0]
    return count > 0
