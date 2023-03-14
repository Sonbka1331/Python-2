from flask import Flask
from datetime import datetime
import os


WEEKDAYS_TUPLE = ('понедельника', 'вторника', 'среды', 'четверга', 'пятницы', 'субботы', 'воскресенья')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

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


if __name__ == '__main__':
    app.run()
