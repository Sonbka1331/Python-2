import sqlite3


def update_work_schedule(cursor: sqlite3.Cursor) -> None:
    cursor.execute("SELECT id, name, preference FROM employees")
    employees = cursor.fetchall()

    cursor.execute("SELECT id, day FROM work_days")
    work_days = cursor.fetchall()
    cursor.execute("SELECT day FROM trainings")
    trainings = [row[0] for row in cursor.fetchall()]

    schedule = {}
    for day in work_days:
        if day[1] in trainings:
            continue

        free_employees = [employee for employee in employees if
                          employee[0] not in schedule.values()]

        preferred_employees = [employee for employee in free_employees if
                               employee[2] == day[1]]

        if preferred_employees:
            employee_id = preferred_employees[0][0]
        else:
            employee_id = free_employees[0][0]

        schedule[day[0]] = employee_id

    cursor.execute("DELETE FROM table_friendship_schedule")
    for day, employee_id in schedule.items():
        cursor.execute(
            "INSERT INTO table_friendship_schedule (day, employee_id) VALUES (?, ?)",
            (day, employee_id))
