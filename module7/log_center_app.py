from flask import Flask
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import InputRequired

app = Flask(__name__)


class LogsForm(FlaskForm):
    script_name = StringField(validators=[InputRequired()])
    level = StringField(validators=[InputRequired()])
    name = StringField(validators=[InputRequired()])
    time = StringField(validators=[InputRequired()])
    lineno = StringField(validators=[InputRequired()])
    message = StringField(validators=[InputRequired()])


@app.route('/save_log', methods=['POST'])
def save_logs():
    form = LogsForm()

    if form.validate_on_submit():
        script, level, name, time = form.script_name.data, form.level.data, form.name.data, form.time.data
        lineno, message = form.lineno.data, form.message.data
        with open('worker.log', 'a') as logfile:
            logfile.write(
                f"{script} | {level} | {name} | {time} | {lineno} | {message}"
            )
        return 'Logs saved!'
    else:
        for name in form:
            print(name)
        return 'Error with saves.'


@app.route('/show_logs', methods=['GET'])
def show_logs():
    with open('worker.log', 'r') as logfile:
        data = logfile.read()
    return data


if __name__ == '__main__':
    app.config['WTF_CSRF_ENABLED'] = False
    app.run()
