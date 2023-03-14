from flask import Flask
from random import choice
from datetime import datetime, timedelta
from os import path

app = Flask(__name__)

BASE_DIR = path.dirname(path.abspath(__file__))
BOOK_FILE = path.join(BASE_DIR, "war_and_peace.txt")

with open(BOOK_FILE, "r") as book:
    text = book.read()
    WORDS = list(map(str, text.split()))

CARS = ['Chevrolet', 'Renault', 'Ford', 'Lada']
CATS = ['корниш-рекс', 'русская голубая', 'шотландская вислоухая', 'мейн-кун', 'манчкин']


@app.route("/hello_world")
def hello_world():
    return "Hello, World!"


@app.route("/cars")
def car_list():
    return ", ".join(CARS)


@app.route("/cats")
def random_cat():
    return choice(CATS)


@app.route("/get_time/now")
def time_now():
    current_time = datetime.now()
    return f"Точное время: {current_time}"


@app.route("/get_time/future")
def time_after_hour():
    current_time = datetime.now()
    current_time_after_hour = current_time + timedelta(hours=1)
    return f"Точное время через час: {current_time_after_hour}"


@app.route("/get_random_word")
def random_word():
    return choice(WORDS)


@app.route("/counter")
def counter():
    counter.visits += 1
    return str(counter.visits)


counter.visits = 0

if __name__ == '__main__':
    app.run()
