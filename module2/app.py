from flask import Flask
from datetime import datetime
import os


WEEKDAYS_TUPLE = ('понедельника', 'вторника', 'среды', 'четверга', 'пятницы', 'субботы', 'воскресенья')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# storage заполнена изначально как сказано в практике 3 модуля

storage = {
    2020: {
        11: 13000,
    },
    2022: {
        10: 3000,
        12: 25000
    },
    2023: {
        12: 5000,
    }
}

app = Flask(__name__)


@app.route('/hello-world/<string:name>')
def hello_world(name):
    weekday = datetime.today().weekday()

    if weekday in [2, 4, 5]:
        declination = 'Хорошей'
    else:
        declination = 'Хорошего'
    return f"Привет, {name}. {declination} {WEEKDAYS_TUPLE[weekday]}!"


@app.route("/max_number/<path:numbers>/")
def calculate(numbers):
    numbers = numbers.split("/")
    max_number = 0
    for number in numbers:
        try:
            number = int(number)
            if number > max_number:
                max_number = int(number)
        except ValueError:
            continue
    return f"Максимальное число в переданном списке: {max_number}"


@app.route("/preview/<int:size>/<path:relative_path>")
def file_viewer(size, relative_path):
    abs_path = os.path.abspath(relative_path)
    file = os.path.join(BASE_DIR, relative_path)

    with open(file, "r") as file:
        symbols = file.read(size)

    return f"<b>{abs_path}</b> {size}<br>{symbols}"


@app.route("/add/<string:date>/<int:expense>")
def save_wastes(date, expense):
    try:
        year = int(date[0:4])
        month = int(date[4:6])
    except Exception:
        return f"Указаны неверные данные"
    if month <= 12:
        storage.setdefault(year, {}).setdefault(month, 0)
        storage[year][month] += expense
        return f"Ваша трата записана"
    else:
        return f"Указаны неверные данные"


@app.route("/calculate/<int:year>")
def calculate_by_year(year):
    try:
        total = sum(storage[year].values())
        return f"Сумма ваших трат за {year} год составляет: {total} у.е."
    except KeyError:
        return f"За {year} вы пока ничего не потратили"


@app.route("/calculate/<int:year>/<int:month>")
def calculate_by_month(year, month):
    try:
        total = storage[year][month]
        return f"Сумма ваших трат в {month} месяце {year} года составляет: {total} у.е"
    except KeyError:
        return f"В этом месяце {year} года вы пока ничего не потратили"


if __name__ == '__main__':
    app.run()
