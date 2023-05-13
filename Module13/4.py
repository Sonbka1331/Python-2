import sqlite3


def ivan_sovin_the_most_effective(cursor: sqlite3.Cursor, name: str) -> None:
    # Получаем данные о сотруднике по его имени
    cursor.execute('SELECT * FROM table_effective_manager WHERE name = ?',
                   (name,))
    employee = cursor.fetchone()

    # Если сотрудник не найден, выходим из функции
    if not employee:
        print(f"{name} не найден!")
        return

    # Получаем зарплату Ивана Совина
    cursor.execute(
        'SELECT salary FROM table_effective_manager WHERE name = "Ivan Sovin"')
    ivan_salary = cursor.fetchone()[0]

    # Получаем зарплату сотрудника
    employee_salary = employee[2]

    # Если зарплата сотрудника больше зарплаты Ивана, увольняем его
    if employee_salary > ivan_salary:
        print(f"{name} уволен!")
        cursor.execute('DELETE FROM table_effective_manager WHERE name = ?',
                       (name,))

    # Иначе повышаем его зарплату
    else:
        new_salary = round(employee_salary * 1.1, 2)
        cursor.execute(
            'UPDATE table_effective_manager SET salary = ? WHERE name = ?',
            (new_salary, name))
        print(f"У {name} повышена зарплата, теперь составляет {new_salary}")
