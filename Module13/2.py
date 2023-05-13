import csv
import sqlite3


def delete_wrong_fees(cursor: sqlite3.Cursor, wrong_fees_file: str) -> None:
    with open(wrong_fees_file, newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader:
            date, car_number = row
            cursor.execute(
                "DELETE FROM table_fees WHERE car_number = ? AND date = ?",
                (car_number, date)
            )
