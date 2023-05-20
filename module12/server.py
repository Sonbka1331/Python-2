from flask import Flask
from datetime import datetime

app = Flask(__name__)


@app.route('/timestamp/<timestamp>')
def get_date(timestamp):
    timestamp = int(timestamp)
    current_date = datetime.fromtimestamp(timestamp)
    return str(current_date)


if __name__ == '__main__':
    app.run()
