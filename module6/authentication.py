from flask import Flask
import logging
from datetime import datetime

logger = logging.getLogger('authentication')
app = Flask(__name__)


@app.route("/divide/<int:a>/<int:b>")
def divide(a, b):
    return a / b


@app.errorhandler(ZeroDivisionError)
def handle_exception(error: ZeroDivisionError):
    time = datetime.now().strftime("%H:%M:%S")
    logger.exception(f'Zero division ar {time}', exc_info=error)
    return "Zero division", 400


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, filename='stderr.txt')
    time = datetime.now().strftime("%H:%M:%S")
    logging.info(f"Started at {time}")
    app.run()
